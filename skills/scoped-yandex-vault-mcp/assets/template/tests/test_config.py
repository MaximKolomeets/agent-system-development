import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.config import ConfigError, Settings


class ConfigTests(unittest.TestCase):
    def _environment(self, temp: str):
        root = Path(temp)
        (root / "user").write_text("project-user", encoding="utf-8")
        (root / "password").write_text("project-password", encoding="utf-8")
        (root / "clients.json").write_text(json.dumps({
            "clients": [
                {"id": "writer", "token": "a" * 32, "permissions": ["read", "write"]},
                {"id": "reader", "token": "b" * 32, "permissions": ["read"]},
            ]
        }), encoding="utf-8")
        return {
            "WEBDAV_ROOT_PATH": "Company/Projects/example/vault",
            "WEBDAV_USERNAME_FILE": str(root / "user"),
            "WEBDAV_PASSWORD_FILE": str(root / "password"),
            "MCP_CLIENTS_FILE": str(root / "clients.json"),
        }

    def test_loads_secret_files_and_client_scopes(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.dict(os.environ, self._environment(temp), clear=True):
                settings = Settings.from_env()
        self.assertEqual(settings.webdav_username, "project-user")
        self.assertEqual(settings.clients[1].permissions, frozenset({"read"}))
        self.assertTrue(settings.require_etag_on_mutation)

    def test_rejects_non_https_webdav(self):
        with tempfile.TemporaryDirectory() as temp:
            environment = self._environment(temp)
            environment["WEBDAV_BASE_URL"] = "http://webdav.example.test"
            with patch.dict(os.environ, environment, clear=True), self.assertRaises(ConfigError):
                Settings.from_env()

    def test_rejects_backslash_root(self):
        with tempfile.TemporaryDirectory() as temp:
            environment = self._environment(temp)
            environment["WEBDAV_ROOT_PATH"] = "Company\\Projects\\example\\vault"
            with patch.dict(os.environ, environment, clear=True), self.assertRaises(ConfigError):
                Settings.from_env()


if __name__ == "__main__":
    unittest.main()
