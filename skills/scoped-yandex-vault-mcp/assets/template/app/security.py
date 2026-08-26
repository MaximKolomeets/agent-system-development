from __future__ import annotations

import re
import unicodedata
from typing import Any
from urllib.parse import unquote


class PathViolation(ValueError):
    pass


_DRIVE_RE = re.compile(r"^[A-Za-z]:")

READ_TOOLS = {
    "vault_list", "vault_tree", "vault_stat", "vault_read", "vault_read_many",
    "vault_find", "vault_search_text", "vault_changed_since",
}
WRITE_TOOLS = {"vault_write", "vault_append", "vault_mkdir", "vault_move"}


def normalize_relative_path(path: str | None, *, allow_root: bool = True, allow_history: bool = False) -> str:
    value = unicodedata.normalize("NFKC", (path or "").strip())
    if not value:
        if allow_root:
            return ""
        raise PathViolation("path is required")
    if "\x00" in value or any(ord(char) < 32 for char in value):
        raise PathViolation("control characters are not allowed")
    if "\\" in value:
        raise PathViolation("backslashes are not allowed")
    if value.startswith(("/", "//")) or _DRIVE_RE.match(value) or "://" in value:
        raise PathViolation("absolute paths and URI schemes are not allowed")

    decoded = value
    for _ in range(3):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    decoded = unicodedata.normalize("NFKC", decoded)
    if "\\" in decoded or decoded.startswith("/") or _DRIVE_RE.match(decoded) or "://" in decoded:
        raise PathViolation("encoded absolute path is not allowed")

    segments = decoded.split("/")
    if any(segment in {"", ".", ".."} for segment in segments):
        raise PathViolation("dot and empty path segments are not allowed")
    if not allow_history and any(segment.casefold() == "_history" for segment in segments):
        raise PathViolation("_history is internal")
    return "/".join(segments)


def ensure_write_extension(path: str, allowed_extensions: tuple[str, ...]) -> None:
    lowered = path.casefold()
    if not any(lowered.endswith(ext.casefold()) for ext in allowed_extensions):
        raise PathViolation(f"write extension is not allowed; expected one of {allowed_extensions}")


def required_permissions(payload: Any) -> set[str]:
    messages = payload if isinstance(payload, list) else [payload]
    needed: set[str] = set()
    for message in messages:
        if not isinstance(message, dict) or message.get("method") != "tools/call":
            continue
        tool = ((message.get("params") or {}).get("name") or "")
        if tool in READ_TOOLS:
            needed.add("read")
        elif tool in WRITE_TOOLS:
            needed.add("write")
    return needed
