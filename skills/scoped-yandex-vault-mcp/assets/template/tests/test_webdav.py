import asyncio
import unittest

from app.webdav import WebDavResponse, WebDavStore


class FakeStore(WebDavStore):
    def __init__(self):
        super().__init__("https://webdav.example.test", "Project/vault", "user", "password", 3, 1024)
        self.calls = []
        self.responses = []

    async def request(self, method, relative="", **kwargs):
        self.calls.append((method, relative, kwargs))
        return self.responses.pop(0)


class WebDavTests(unittest.IsolatedAsyncioTestCase):
    def test_url_is_scoped_and_encoded(self):
        store = FakeStore()
        self.assertEqual(
            store._url("решения/ADR 001.md"),
            "https://webdav.example.test/Project/vault/%D1%80%D0%B5%D1%88%D0%B5%D0%BD%D0%B8%D1%8F/ADR%20001.md",
        )
        self.assertTrue(store._url("_history/a.md").endswith("/_history/a.md"))

    async def test_put_uses_create_precondition_and_verifies_content(self):
        store = FakeStore()
        xml = b'''<?xml version="1.0"?><d:multistatus xmlns:d="DAV:"><d:response><d:propstat><d:prop><d:displayname>note.md</d:displayname><d:getcontentlength>5</d:getcontentlength><d:getetag>"abc"</d:getetag><d:resourcetype/></d:prop></d:propstat></d:response></d:multistatus>'''
        store.responses = [
            WebDavResponse(201, {}, b""),
            WebDavResponse(207, {}, xml),
            WebDavResponse(200, {}, b"hello"),
        ]
        entry = await store.put("note.md", b"hello", create_only=True)
        self.assertEqual(entry.etag, '"abc"')
        self.assertEqual(store.calls[0][2]["headers"]["If-None-Match"], "*")

    async def test_move_uses_if_match_and_no_overwrite(self):
        store = FakeStore()
        store.responses = [WebDavResponse(201, {}, b"")]
        await store.move("a.md", "b.md", expected_etag='"etag"')
        headers = store.calls[0][2]["headers"]
        self.assertEqual(headers["If-Match"], '"etag"')
        self.assertEqual(headers["Overwrite"], "F")

    async def test_internal_history_can_be_statted(self):
        store = FakeStore()
        xml = b'''<?xml version="1.0"?><d:multistatus xmlns:d="DAV:"><d:response><d:propstat><d:prop><d:displayname>backup.md</d:displayname><d:getcontentlength>5</d:getcontentlength><d:getetag>"history"</d:getetag><d:resourcetype/></d:prop></d:propstat></d:response></d:multistatus>'''
        store.responses = [WebDavResponse(207, {}, xml)]

        entry = await store.stat("_history/note.md/backup.md")

        self.assertEqual(entry.path, "_history/note.md/backup.md")
        self.assertEqual(entry.etag, '"history"')


if __name__ == "__main__":
    unittest.main()
