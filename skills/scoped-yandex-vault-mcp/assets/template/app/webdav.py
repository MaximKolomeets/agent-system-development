from __future__ import annotations

import asyncio
import base64
import hashlib
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .security import normalize_relative_path


DAV = "{DAV:}"


class WebDavError(RuntimeError):
    def __init__(self, code: str, message: str, status: int | None = None):
        self.code = code
        self.status = status
        super().__init__(message)


@dataclass(frozen=True)
class WebDavResponse:
    status: int
    headers: dict[str, str]
    body: bytes


@dataclass(frozen=True)
class RemoteEntry:
    path: str
    name: str
    is_dir: bool
    size: int
    modified_at: str | None
    etag: str | None


class WebDavStore:
    def __init__(self, base_url: str, root_path: str, username: str, password: str, timeout: int, max_file_bytes: int):
        self.base_url = base_url.rstrip("/")
        self.root_path = normalize_relative_path(root_path, allow_root=False)
        self.timeout = timeout
        self.max_file_bytes = max_file_bytes
        token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        self._authorization = f"Basic {token}"
        self._origin_host = urlsplit(self.base_url).hostname
        self._opener = build_opener(_NoRedirect())

    def _url(self, relative: str = "") -> str:
        rel = normalize_relative_path(relative, allow_history=True) if relative else ""
        full = self.root_path if not rel else f"{self.root_path}/{rel}"
        encoded = "/".join(quote(segment, safe="") for segment in full.split("/"))
        return f"{self.base_url}/{encoded}"

    def _sync_request(self, method: str, relative: str = "", *, headers: dict[str, str] | None = None,
                      body: bytes | None = None, max_response_bytes: int | None = None) -> WebDavResponse:
        request_headers = {
            "Authorization": self._authorization,
            "User-Agent": "scoped-vault-mcp/0.1",
        }
        request_headers.update(headers or {})
        req = Request(self._url(relative), data=body, headers=request_headers, method=method)
        try:
            with self._opener.open(req, timeout=self.timeout) as response:
                final_host = urlsplit(response.geturl()).hostname
                if final_host != self._origin_host:
                    raise WebDavError("EREDIRECT", "cross-origin redirect denied")
                limit = max_response_bytes if max_response_bytes is not None else self.max_file_bytes
                payload = response.read(limit + 1)
                if len(payload) > limit:
                    raise WebDavError("ETOOBIG", "remote response exceeds configured limit")
                return WebDavResponse(response.status, {k.lower(): v for k, v in response.headers.items()}, payload)
        except HTTPError as exc:
            payload = exc.read(4096)
            return WebDavResponse(exc.code, {k.lower(): v for k, v in exc.headers.items()}, payload)
        except URLError as exc:
            raise WebDavError("EUPSTREAM", "WebDAV connection failed") from exc

    async def request(self, method: str, relative: str = "", **kwargs) -> WebDavResponse:
        return await asyncio.to_thread(self._sync_request, method, relative, **kwargs)

    @staticmethod
    def _expect(response: WebDavResponse, allowed: Iterable[int], action: str) -> None:
        if response.status not in set(allowed):
            mapping = {401: "EAUTH", 403: "EPERM", 404: "ENOENT", 409: "ECONFLICT", 412: "CONFLICT", 413: "ETOOBIG"}
            raise WebDavError(mapping.get(response.status, "EUPSTREAM"), f"{action} failed", response.status)

    async def propfind(self, relative: str = "", depth: int = 0) -> list[RemoteEntry]:
        body = b'''<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:"><d:prop><d:displayname/><d:getcontentlength/><d:getlastmodified/><d:getetag/><d:resourcetype/></d:prop></d:propfind>'''
        response = await self.request("PROPFIND", relative, headers={"Depth": str(depth), "Content-Type": "application/xml"},
                                      body=body, max_response_bytes=max(self.max_file_bytes, 4_000_000))
        self._expect(response, {207}, "PROPFIND")
        try:
            root = ET.fromstring(response.body)
        except ET.ParseError as exc:
            raise WebDavError("EUPSTREAM", "invalid WebDAV XML") from exc
        requested = normalize_relative_path(relative, allow_history=True) if relative else ""
        entries: list[RemoteEntry] = []
        for item in root.findall(f"{DAV}response"):
            prop = item.find(f".//{DAV}prop")
            if prop is None:
                continue
            name = (prop.findtext(f"{DAV}displayname") or "").strip("/")
            is_dir = prop.find(f"{DAV}resourcetype/{DAV}collection") is not None
            size_text = prop.findtext(f"{DAV}getcontentlength") or "0"
            modified_raw = prop.findtext(f"{DAV}getlastmodified")
            modified_at = None
            if modified_raw:
                try:
                    modified_at = parsedate_to_datetime(modified_raw).astimezone(timezone.utc).isoformat(timespec="seconds")
                except (TypeError, ValueError):
                    modified_at = None
            etag = prop.findtext(f"{DAV}getetag")
            path = requested if depth == 0 else (f"{requested}/{name}".strip("/"))
            entries.append(RemoteEntry(path, name, is_dir, int(size_text or 0), modified_at, etag))
        if depth == 1 and entries:
            entries = entries[1:]
        return entries

    async def stat(self, relative: str) -> RemoteEntry:
        entries = await self.propfind(relative, 0)
        if not entries:
            raise WebDavError("ENOENT", "not found", 404)
        entry = entries[0]
        return RemoteEntry(relative, relative.rsplit("/", 1)[-1], entry.is_dir, entry.size, entry.modified_at, entry.etag)

    async def exists(self, relative: str) -> bool:
        try:
            await self.stat(relative)
            return True
        except WebDavError as exc:
            if exc.code == "ENOENT":
                return False
            raise

    async def read(self, relative: str) -> bytes:
        response = await self.request("GET", relative, max_response_bytes=self.max_file_bytes)
        self._expect(response, {200}, "GET")
        return response.body

    async def mkdirs(self, relative: str) -> None:
        normalized = normalize_relative_path(relative, allow_root=False, allow_history=True)
        current: list[str] = []
        for segment in normalized.split("/"):
            current.append(segment)
            response = await self.request("MKCOL", "/".join(current), max_response_bytes=4096)
            if response.status not in {201, 405}:
                self._expect(response, {201, 405}, "MKCOL")

    async def copy(self, source: str, destination: str, *, overwrite: bool = False) -> None:
        headers = {"Destination": self._url(destination), "Overwrite": "T" if overwrite else "F"}
        response = await self.request("COPY", source, headers=headers, max_response_bytes=4096)
        self._expect(response, {201, 204}, "COPY")

    async def move(self, source: str, destination: str, *, expected_etag: str | None = None) -> None:
        headers = {"Destination": self._url(destination), "Overwrite": "F"}
        if expected_etag:
            headers["If-Match"] = expected_etag
        response = await self.request("MOVE", source, headers=headers, max_response_bytes=4096)
        self._expect(response, {201, 204}, "MOVE")

    async def put(self, relative: str, content: bytes, *, expected_etag: str | None = None,
                  create_only: bool = False) -> RemoteEntry:
        if len(content) > self.max_file_bytes:
            raise WebDavError("ETOOBIG", "content exceeds configured limit")
        headers = {"Content-Type": "text/markdown; charset=utf-8"}
        if create_only:
            headers["If-None-Match"] = "*"
        elif expected_etag:
            headers["If-Match"] = expected_etag
        response = await self.request("PUT", relative, headers=headers, body=content, max_response_bytes=4096)
        self._expect(response, {200, 201, 204}, "PUT")
        entry = await self.stat(relative)
        verify = await self.read(relative)
        if hashlib.sha256(verify).digest() != hashlib.sha256(content).digest():
            raise WebDavError("EVERIFY", "read-after-write checksum mismatch")
        return entry

    async def walk(self, relative: str = "", *, max_files: int = 250) -> list[RemoteEntry]:
        queue = [normalize_relative_path(relative) if relative else ""]
        files: list[RemoteEntry] = []
        visited_nodes = 0
        max_nodes = max(max_files * 4, 100)
        while queue and len(files) < max_files and visited_nodes < max_nodes:
            current = queue.pop(0)
            for entry in await self.propfind(current, 1):
                visited_nodes += 1
                if entry.name.casefold() == "_history":
                    continue
                if entry.is_dir:
                    queue.append(entry.path)
                else:
                    files.append(entry)
                    if len(files) >= max_files:
                        break
                if visited_nodes >= max_nodes:
                    break
        return files

    @staticmethod
    def history_path(path: str) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        parent, _, name = path.rpartition("/")
        prefix = f"_history/{parent}/{name}" if parent else f"_history/{name}"
        return f"{prefix}/{stamp}_{name}"


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None
