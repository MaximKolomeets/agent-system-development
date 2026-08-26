#!/usr/bin/env python3
"""Validate a secret-free project-scoped Yandex Vault deployment plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath


SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}$")
CLIENT_ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}$")


def validate_root(value: object) -> str:
    root = str(value or "").strip().replace("\\", "/").strip("/")
    parts = PurePosixPath(root).parts
    if not root or len(parts) < 2 or any(part in {"", ".", ".."} for part in parts):
        raise ValueError("webdav_root must be a non-root project path with at least two segments")
    if any(part.casefold() == "_history" for part in parts):
        raise ValueError("webdav_root must not point into _history")
    return root


def validate(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    required = {"project_slug", "webdav_root", "container_name", "backend_network", "egress_network", "clients"}
    if set(payload) != required:
        raise ValueError("vault plan fields mismatch")
    slug = str(payload["project_slug"])
    if not SLUG.fullmatch(slug):
        raise ValueError("project_slug is invalid")
    root = validate_root(payload["webdav_root"])
    for key in ("container_name", "backend_network", "egress_network"):
        value = str(payload[key])
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{2,62}", value):
            raise ValueError(f"{key} is invalid")
    if payload["backend_network"] == payload["egress_network"]:
        raise ValueError("backend and egress networks must differ")
    clients = payload["clients"]
    if not isinstance(clients, list) or not 1 <= len(clients) <= 16:
        raise ValueError("clients count must be in 1..16")
    ids: set[str] = set()
    for row in clients:
        if not isinstance(row, dict) or set(row) != {"id", "permissions"}:
            raise ValueError("client plan contains secret or unknown fields")
        client_id = str(row["id"])
        permissions = row["permissions"]
        if not CLIENT_ID.fullmatch(client_id) or client_id in ids:
            raise ValueError("client ids must be valid and unique")
        if not isinstance(permissions, list) or not permissions or not set(permissions) <= {"read", "write"}:
            raise ValueError("client permissions are invalid")
        ids.add(client_id)
    serialized = json.dumps(payload).casefold()
    if any(marker in serialized for marker in ("password", "token", "authorization", "secret_value")):
        raise ValueError("plan must contain references/scopes, never secret values")
    return {"valid": True, "project_slug": slug, "webdav_root_segments": len(PurePosixPath(root).parts), "clients": len(clients)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.plan), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
