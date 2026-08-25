from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


class ConfigError(RuntimeError):
    pass


def _read_secret(name: str, *, required: bool = True) -> str:
    file_value = os.getenv(f"{name}_FILE", "").strip()
    direct_value = os.getenv(name, "").strip()
    if file_value and direct_value:
        raise ConfigError(f"set only one of {name} or {name}_FILE")
    if file_value:
        try:
            value = Path(file_value).read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise ConfigError(f"cannot read {name}_FILE") from exc
    else:
        value = direct_value
    if required and not value:
        raise ConfigError(f"missing required secret {name}_FILE")
    return value


def _csv(name: str, default: str = "") -> tuple[str, ...]:
    return tuple(item.strip() for item in os.getenv(name, default).split(",") if item.strip())


def _positive_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ConfigError(f"{name} must be an integer") from exc
    if value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}")
    return value


@dataclass(frozen=True)
class ClientIdentity:
    client_id: str
    token: str
    permissions: frozenset[str]


def _load_clients() -> tuple[ClientIdentity, ...]:
    clients_file = os.getenv("MCP_CLIENTS_FILE", "").strip()
    legacy_token = _read_secret("MCP_TOKEN", required=False)
    if clients_file and legacy_token:
        raise ConfigError("set MCP_CLIENTS_FILE or MCP_TOKEN_FILE, not both")
    if clients_file:
        try:
            payload = json.loads(Path(clients_file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigError("cannot read MCP_CLIENTS_FILE") from exc
        raw_clients = payload.get("clients") if isinstance(payload, dict) else None
        if not isinstance(raw_clients, list) or not raw_clients:
            raise ConfigError("MCP_CLIENTS_FILE must contain a non-empty clients array")
        clients: list[ClientIdentity] = []
        seen_ids: set[str] = set()
        seen_tokens: set[str] = set()
        for item in raw_clients:
            if not isinstance(item, dict):
                raise ConfigError("every MCP client must be an object")
            client_id = str(item.get("id", "")).strip()
            token = str(item.get("token", "")).strip()
            permissions = frozenset(str(p).strip() for p in item.get("permissions", []) if str(p).strip())
            if not client_id or not token or not permissions:
                raise ConfigError("MCP client requires id, token and permissions")
            if len(token) < 32:
                raise ConfigError(f"token for client {client_id} must be at least 32 characters")
            if not permissions <= {"read", "write"}:
                raise ConfigError(f"invalid permissions for client {client_id}")
            if client_id in seen_ids or token in seen_tokens:
                raise ConfigError("MCP client ids and tokens must be unique")
            seen_ids.add(client_id)
            seen_tokens.add(token)
            clients.append(ClientIdentity(client_id, token, permissions))
        return tuple(clients)
    if legacy_token:
        if len(legacy_token) < 32:
            raise ConfigError("MCP_TOKEN must be at least 32 characters")
        return (ClientIdentity("default", legacy_token, frozenset({"read", "write"})),)
    raise ConfigError("missing MCP_CLIENTS_FILE or MCP_TOKEN_FILE")


@dataclass(frozen=True)
class Settings:
    webdav_base_url: str
    webdav_root_path: str
    webdav_username: str
    webdav_password: str
    clients: tuple[ClientIdentity, ...]
    mcp_host: str
    mcp_port: int
    allowed_hosts: tuple[str, ...]
    allowed_origins: tuple[str, ...]
    max_request_bytes: int
    max_file_bytes: int
    max_search_files: int
    max_search_bytes: int
    max_results: int
    webdav_timeout_seconds: int
    require_etag_on_mutation: bool
    allowed_write_extensions: tuple[str, ...]

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.getenv("WEBDAV_BASE_URL", "https://webdav.yandex.ru").rstrip("/")
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ConfigError("WEBDAV_BASE_URL must be a plain HTTPS origin")
        root_path = os.getenv("WEBDAV_ROOT_PATH", "").strip().strip("/")
        if not root_path:
            raise ConfigError("WEBDAV_ROOT_PATH is required")
        if "\\" in root_path:
            raise ConfigError("WEBDAV_ROOT_PATH must use forward slashes")
        if any(segment in {"", ".", ".."} for segment in root_path.replace("\\", "/").split("/")):
            raise ConfigError("WEBDAV_ROOT_PATH contains an invalid segment")
        allowed_hosts = _csv("MCP_ALLOWED_HOSTS", "localhost,127.0.0.1")
        if not allowed_hosts:
            raise ConfigError("MCP_ALLOWED_HOSTS cannot be empty")
        extensions = tuple(
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in _csv("ALLOWED_WRITE_EXTENSIONS", ".md")
        )
        return cls(
            webdav_base_url=base_url,
            webdav_root_path=root_path,
            webdav_username=_read_secret("WEBDAV_USERNAME"),
            webdav_password=_read_secret("WEBDAV_PASSWORD"),
            clients=_load_clients(),
            mcp_host=os.getenv("MCP_HOST", "0.0.0.0"),
            mcp_port=_positive_int("MCP_PORT", 8200),
            allowed_hosts=allowed_hosts,
            allowed_origins=_csv("MCP_ALLOWED_ORIGINS"),
            max_request_bytes=_positive_int("MAX_REQUEST_BYTES", 2_500_000),
            max_file_bytes=_positive_int("MAX_FILE_BYTES", 2_000_000),
            max_search_files=_positive_int("MAX_SEARCH_FILES", 250),
            max_search_bytes=_positive_int("MAX_SEARCH_BYTES", 10_000_000),
            max_results=_positive_int("MAX_RESULTS", 200),
            webdav_timeout_seconds=_positive_int("WEBDAV_TIMEOUT_SECONDS", 30),
            require_etag_on_mutation=os.getenv("REQUIRE_ETAG_ON_MUTATION", "true").lower() == "true",
            allowed_write_extensions=extensions,
        )
