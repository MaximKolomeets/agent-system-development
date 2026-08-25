from __future__ import annotations

import contextvars
import functools
import json
import logging
import secrets
import time
from datetime import datetime, timezone
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

from .config import ConfigError, Settings
from .security import PathViolation, ensure_write_extension, normalize_relative_path, required_permissions
from .webdav import RemoteEntry, WebDavError, WebDavStore


logging.basicConfig(level=logging.INFO, format="%(message)s")
LOGGER = logging.getLogger("scoped-vault-mcp")
IDENTITY: contextvars.ContextVar[str] = contextvars.ContextVar("vault_identity", default="unknown")

SETTINGS = Settings.from_env()
STORE = WebDavStore(
    SETTINGS.webdav_base_url,
    SETTINGS.webdav_root_path,
    SETTINGS.webdav_username,
    SETTINGS.webdav_password,
    SETTINGS.webdav_timeout_seconds,
    SETTINGS.max_file_bytes,
)

SECURITY = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=list(SETTINGS.allowed_hosts),
    allowed_origins=list(SETTINGS.allowed_origins),
)
MCP = FastMCP(
    "scoped-vault-mcp",
    host=SETTINGS.mcp_host,
    port=SETTINGS.mcp_port,
    transport_security=SECURITY,
)


class VaultError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def _entry_json(entry: RemoteEntry) -> dict[str, Any]:
    result: dict[str, Any] = {
        "path": entry.path,
        "name": entry.name,
        "type": "dir" if entry.is_dir else "file",
        "size": entry.size,
        "modified_at": entry.modified_at,
    }
    if entry.etag:
        result["etag"] = entry.etag
    return result


def _log(tool: str, path: str, result: str, started: float) -> None:
    LOGGER.info(json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "identity": IDENTITY.get(),
        "tool": tool,
        "path": path[:500],
        "result": result,
        "duration_ms": int((time.monotonic() - started) * 1000),
    }, ensure_ascii=False))


def guarded(fn):
    name = fn.__name__

    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        started = time.monotonic()
        path = str(kwargs.get("path") or kwargs.get("source") or (args[0] if args and isinstance(args[0], str) else ""))
        try:
            result = await fn(*args, **kwargs)
            _log(name, path, "OK", started)
            return result
        except PathViolation as exc:
            _log(name, path, "DENY:EPATH", started)
            raise ValueError(f"[EPATH] {exc}") from None
        except WebDavError as exc:
            _log(name, path, f"ERR:{exc.code}", started)
            raise ValueError(f"[{exc.code}] {exc}") from None
        except VaultError as exc:
            _log(name, path, f"ERR:{exc.code}", started)
            raise ValueError(f"[{exc.code}] {exc}") from None
        except Exception as exc:
            _log(name, path, f"ERR:{type(exc).__name__}", started)
            raise

    return wrapper


async def _require_existing_etag(path: str, supplied: str, entry: RemoteEntry) -> str | None:
    if supplied and entry.etag and not secrets.compare_digest(supplied, entry.etag):
        raise VaultError("CONFLICT", "etag does not match current remote version")
    if SETTINGS.require_etag_on_mutation and not supplied:
        raise VaultError("EPRECONDITION", "expected_etag is required for existing content")
    if supplied and not entry.etag:
        raise VaultError("EPRECONDITION", "remote storage did not provide an etag")
    return entry.etag


async def _backup(path: str, expected_etag: str | None = None) -> str:
    headers = {"If-Match": expected_etag} if expected_etag else {}
    source = await STORE.request(
        "GET",
        path,
        headers=headers,
        max_response_bytes=SETTINGS.max_file_bytes,
    )
    STORE._expect(source, {200}, "history GET")

    history = STORE.history_path(path)
    parent = history.rpartition("/")[0]
    await STORE.mkdirs(parent)
    await STORE.put(history, source.body, create_only=True)
    return history


@MCP.tool()
@guarded
async def vault_list(path: str = "") -> str:
    """List entries under the instance-scoped Vault root. Internal history is hidden."""
    normalized = normalize_relative_path(path) if path else ""
    entries = await STORE.propfind(normalized, 1)
    visible = [_entry_json(item) for item in entries if item.name.casefold() != "_history"]
    return json.dumps(visible[:SETTINGS.max_results], ensure_ascii=False)


@MCP.tool()
@guarded
async def vault_tree(path: str = "", depth: int = 2) -> str:
    """Return a bounded tree. Depth is limited to 6."""
    root = normalize_relative_path(path) if path else ""
    depth = max(0, min(int(depth), 6))
    lines: list[str] = []
    queue: list[tuple[str, int, str]] = [(root, 0, "")]
    while queue and len(lines) < SETTINGS.max_results:
        current, level, prefix = queue.pop(0)
        for entry in await STORE.propfind(current, 1):
            if entry.name.casefold() == "_history":
                continue
            lines.append(f"{prefix}{entry.name}{'/' if entry.is_dir else ''}")
            if entry.is_dir and level < depth:
                queue.append((entry.path, level + 1, prefix + "  "))
            if len(lines) >= SETTINGS.max_results:
                break
    return "\n".join(lines)


@MCP.tool()
@guarded
async def vault_stat(path: str) -> str:
    """Return remote type, size, modified_at and ETag."""
    normalized = normalize_relative_path(path, allow_root=False)
    return json.dumps(_entry_json(await STORE.stat(normalized)), ensure_ascii=False)


@MCP.tool()
@guarded
async def vault_read(path: str) -> str:
    """Read one bounded UTF-8 text file from this Vault instance."""
    normalized = normalize_relative_path(path, allow_root=False)
    try:
        return (await STORE.read(normalized)).decode("utf-8")
    except UnicodeDecodeError:
        raise VaultError("EENCODING", "file is not valid UTF-8") from None


@MCP.tool()
@guarded
async def vault_read_many(paths: list[str]) -> str:
    """Read up to 20 bounded UTF-8 files."""
    result: dict[str, str | None] = {}
    consumed = 0
    for raw in paths[:20]:
        try:
            normalized = normalize_relative_path(raw, allow_root=False)
            payload = await STORE.read(normalized)
            if consumed + len(payload) > SETTINGS.max_search_bytes:
                result[raw] = "[ETOOBIG] combined read limit reached"
                break
            consumed += len(payload)
            result[raw] = payload.decode("utf-8")
        except (PathViolation, WebDavError, UnicodeDecodeError) as exc:
            result[raw] = f"[{getattr(exc, 'code', type(exc).__name__)}] unavailable"
    return json.dumps(result, ensure_ascii=False)


@MCP.tool()
@guarded
async def vault_find(query: str, path: str = "") -> str:
    """Find file names in a bounded direct-WebDAV traversal."""
    if not query.strip():
        raise VaultError("EINVAL", "query is required")
    root = normalize_relative_path(path) if path else ""
    needle = query.casefold()
    files = await STORE.walk(root, max_files=SETTINGS.max_search_files)
    hits = [item.path for item in files if needle in item.name.casefold()]
    return "\n".join(hits[:SETTINGS.max_results]) or "(no matches)"


@MCP.tool()
@guarded
async def vault_search_text(query: str, path: str = "") -> str:
    """Search bounded UTF-8 text directly in WebDAV. Qdrant should handle production semantic search."""
    if not query.strip():
        raise VaultError("EINVAL", "query is required")
    root = normalize_relative_path(path) if path else ""
    needle = query.casefold()
    files = await STORE.walk(root, max_files=SETTINGS.max_search_files)
    consumed = 0
    hits: list[str] = []
    for entry in files:
        if consumed + entry.size > SETTINGS.max_search_bytes:
            break
        if entry.size > SETTINGS.max_file_bytes:
            continue
        consumed += entry.size
        try:
            text = (await STORE.read(entry.path)).decode("utf-8")
        except (UnicodeDecodeError, WebDavError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if needle in line.casefold():
                hits.append(f"{entry.path}:{line_number}: {line.strip()[:160]}")
                break
        if len(hits) >= SETTINGS.max_results:
            break
    return "\n".join(hits) or "(no matches)"


@MCP.tool()
@guarded
async def vault_changed_since(timestamp: str, path: str = "") -> str:
    """List files modified after an ISO-8601 timestamp."""
    try:
        threshold = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        raise VaultError("EINVAL", "timestamp must be ISO-8601") from None
    root = normalize_relative_path(path) if path else ""
    hits: list[str] = []
    for entry in await STORE.walk(root, max_files=SETTINGS.max_search_files):
        if entry.modified_at and datetime.fromisoformat(entry.modified_at) > threshold:
            hits.append(f"{entry.path} ({entry.modified_at})")
    return "\n".join(hits[:SETTINGS.max_results]) or "(nothing changed)"


@MCP.tool()
@guarded
async def vault_write(path: str, content: str, mode: str = "create", create_parents: bool = False,
                      expected_etag: str = "") -> str:
    """Create or replace UTF-8 content. Existing content requires ETag by default."""
    normalized = normalize_relative_path(path, allow_root=False)
    ensure_write_extension(normalized, SETTINGS.allowed_write_extensions)
    if mode not in {"create", "replace"}:
        raise VaultError("EINVAL", "mode must be create or replace")
    exists = await STORE.exists(normalized)
    if mode == "create" and exists:
        raise VaultError("EEXIST", "file exists; use replace")
    if mode == "replace" and not exists:
        raise VaultError("ENOENT", "file does not exist; use create")
    parent = normalized.rpartition("/")[0]
    if parent and not await STORE.exists(parent):
        if not create_parents:
            raise VaultError("ENOENT", "parent is missing; set create_parents=true")
        await STORE.mkdirs(parent)
    backup = None
    remote_etag = None
    if exists:
        entry = await STORE.stat(normalized)
        remote_etag = await _require_existing_etag(normalized, expected_etag, entry)
        backup = await _backup(normalized, remote_etag)
    written = await STORE.put(normalized, content.encode("utf-8"), expected_etag=remote_etag, create_only=not exists)
    return json.dumps({"ok": True, "mode": mode, "backup": backup, **_entry_json(written)}, ensure_ascii=False)


@MCP.tool()
@guarded
async def vault_append(path: str, content: str, expected_etag: str = "", create_parents: bool = False) -> str:
    """Append with optimistic concurrency. Existing content requires ETag by default."""
    normalized = normalize_relative_path(path, allow_root=False)
    ensure_write_extension(normalized, SETTINGS.allowed_write_extensions)
    exists = await STORE.exists(normalized)
    parent = normalized.rpartition("/")[0]
    if parent and not await STORE.exists(parent):
        if not create_parents:
            raise VaultError("ENOENT", "parent is missing; set create_parents=true")
        await STORE.mkdirs(parent)
    backup = None
    remote_etag = None
    current = b""
    if exists:
        entry = await STORE.stat(normalized)
        remote_etag = await _require_existing_etag(normalized, expected_etag, entry)
        current = await STORE.read(normalized)
        backup = await _backup(normalized, remote_etag)
    written = await STORE.put(normalized, current + content.encode("utf-8"), expected_etag=remote_etag, create_only=not exists)
    return json.dumps({"ok": True, "backup": backup, **_entry_json(written)}, ensure_ascii=False)


@MCP.tool()
@guarded
async def vault_mkdir(path: str, create_parents: bool = True) -> str:
    """Create a directory inside this instance root."""
    normalized = normalize_relative_path(path, allow_root=False)
    if create_parents:
        await STORE.mkdirs(normalized)
    else:
        response = await STORE.request("MKCOL", normalized, max_response_bytes=4096)
        STORE._expect(response, {201}, "MKCOL")
    return json.dumps({"ok": True, "path": normalized}, ensure_ascii=False)


@MCP.tool()
@guarded
async def vault_move(source: str, destination: str, expected_etag: str = "", create_parents: bool = False) -> str:
    """Move one file with history and optimistic concurrency. Directory moves are denied."""
    src = normalize_relative_path(source, allow_root=False)
    dst = normalize_relative_path(destination, allow_root=False)
    ensure_write_extension(dst, SETTINGS.allowed_write_extensions)
    entry = await STORE.stat(src)
    if entry.is_dir:
        raise VaultError("EPERM", "directory moves are not supported")
    if await STORE.exists(dst):
        raise VaultError("EEXIST", "destination exists")
    remote_etag = await _require_existing_etag(src, expected_etag, entry)
    parent = dst.rpartition("/")[0]
    if parent and not await STORE.exists(parent):
        if not create_parents:
            raise VaultError("ENOENT", "destination parent is missing")
        await STORE.mkdirs(parent)
    backup = await _backup(src, remote_etag)
    await STORE.move(src, dst, expected_etag=remote_etag)
    return json.dumps({"ok": True, "source": src, "destination": dst, "backup": backup}, ensure_ascii=False)


# vault_delete is intentionally absent.


class AuthAndLimitMiddleware:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def _json_response(status: int, message: str):
        return JSONResponse({"error": message}, status_code=status)

    def _authenticate(self, authorization: str):
        bearer_prefix = "Bearer" + " "
        if not authorization.startswith(bearer_prefix):
            return None
        candidate = authorization[len(bearer_prefix):]
        for client in SETTINGS.clients:
            if secrets.compare_digest(candidate, client.token):
                return client
        return None

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return
        path = scope.get("path", "")
        if path == "/healthz":
            await self.app(scope, receive, send)
            return
        headers = {key.decode("latin-1").lower(): value.decode("latin-1") for key, value in scope.get("headers", [])}
        client = self._authenticate(headers.get("authorization", ""))
        if client is None:
            await self._json_response(401, "unauthorized")(scope, receive, send)
            return
        body_parts: list[bytes] = []
        more = True
        while more:
            message = await receive()
            if message.get("type") != "http.request":
                continue
            body_parts.append(message.get("body", b""))
            if sum(map(len, body_parts)) > SETTINGS.max_request_bytes:
                await self._json_response(413, "request too large")(scope, receive, send)
                return
            more = bool(message.get("more_body"))
        body = b"".join(body_parts)
        if body:
            try:
                needed = required_permissions(json.loads(body))
            except json.JSONDecodeError:
                needed = set()
            if not needed <= client.permissions:
                await self._json_response(403, "insufficient scope")(scope, receive, send)
                return
        delivered = False

        async def replay_receive():
            nonlocal delivered
            if delivered:
                return await receive()
            delivered = True
            return {"type": "http.request", "body": body, "more_body": False}

        context_marker = IDENTITY.set(client.client_id)
        try:
            await self.app(scope, replay_receive, send)
        finally:
            IDENTITY.reset(context_marker)


async def healthz(_request):
    return JSONResponse({"status": "ok", "service": "scoped-vault-mcp"})


APP = MCP.streamable_http_app()
APP.add_route("/healthz", healthz, methods=["GET"])
APP.add_middleware(AuthAndLimitMiddleware)


def main() -> None:
    import uvicorn

    uvicorn.run(APP, host=SETTINGS.mcp_host, port=SETTINGS.mcp_port, log_level="warning", proxy_headers=False)


if __name__ == "__main__":
    try:
        main()
    except ConfigError as exc:
        raise SystemExit(f"configuration error: {exc}") from None
