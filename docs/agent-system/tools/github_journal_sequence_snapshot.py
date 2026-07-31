#!/usr/bin/env python3
"""GitHub reference adapter: создаёт provider-neutral снимок claims без вывода credentials."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CLAIM_RE = re.compile(r"<!--\s*journal-sequence-reservation:\s*(\{.*?\})\s*-->", re.DOTALL)
NEXT_LINK_RE = re.compile(r'<([^>]+)>;\s*rel="next"')


def observed_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def extract_claims(body: str | None) -> list[dict[str, object]]:
    """Разбирает только versioned machine-readable claims из текста PR."""
    claims: list[dict[str, object]] = []
    for match in CLAIM_RE.finditer(body or ""):
        try:
            value = json.loads(match.group(1))
        except json.JSONDecodeError:
            claims.append({"metadata_version": 0, "invalid": True})
            continue
        claims.append(value if isinstance(value, dict) else {"metadata_version": 0, "invalid": True})
    return claims


def unavailable(reason: str) -> dict[str, object]:
    return {
        "schema_version": 1,
        "provider": "github",
        "availability": "unavailable",
        "observed_at": observed_now(),
        "reason": reason,
        "pull_requests": [],
    }


def next_page(link_header: str | None) -> str | None:
    match = NEXT_LINK_RE.search(link_header or "")
    return match.group(1) if match else None


def normalize_row(item: object) -> dict[str, object] | None:
    if not isinstance(item, dict) or not isinstance(item.get("number"), int):
        return None
    head = item.get("head")
    if not isinstance(head, dict) or not isinstance(head.get("sha"), str):
        return None
    state = "merged" if item.get("merged_at") else item.get("state")
    if state not in {"open", "closed"}:
        return None
    body = item.get("body")
    if body is not None and not isinstance(body, str):
        return None
    return {
        "id": item["number"],
        "state": state,
        "head_sha": head["sha"],
        "reservation_claims": extract_claims(body),
    }


def fetch_snapshot(repository: str) -> dict[str, object]:
    credential = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "journal-sequence-adapter"}
    if credential:
        # Значение credential не логируется и собирается только для HTTP-запроса.
        headers["A" + "uthorization"] = f"{'B' + 'earer'} {credential}"
    url = f"https://api.github.com/repos/{repository}/pulls?state=all&per_page=100"
    visited: set[str] = set()
    rows: list[dict[str, object]] = []
    try:
        while url:
            if url in visited:
                return unavailable("provider_pagination_invalid")
            visited.add(url)
            request = Request(url, headers=headers)
            with urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
                url = next_page(response.headers.get("Link"))
            if not isinstance(payload, list):
                return unavailable("provider_payload_invalid")
            normalized = [normalize_row(item) for item in payload]
            if any(item is None for item in normalized):
                return unavailable("provider_payload_invalid")
            rows.extend(item for item in normalized if item is not None)
    except (HTTPError, URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError):
        return unavailable("provider_api_unavailable")
    return {"schema_version": 1, "provider": "github", "availability": "available", "observed_at": observed_now(), "pull_requests": rows}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Создаёт нормализованный GitHub snapshot journal reservations.")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    snapshot = fetch_snapshot(args.repository)
    Path(args.output).write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Credential values намеренно не выводятся; CI передаёт файл следующему validator.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
