import unittest

from app.security import PathViolation, ensure_write_extension, normalize_relative_path, required_permissions


class PathSecurityTests(unittest.TestCase):
    def test_accepts_normal_unicode_project_path(self):
        self.assertEqual(normalize_relative_path("Проекты/решение.md"), "Проекты/решение.md")

    def test_accepts_root_only_when_allowed(self):
        self.assertEqual(normalize_relative_path(""), "")
        with self.assertRaises(PathViolation):
            normalize_relative_path("", allow_root=False)

    def test_rejects_traversal_and_absolute_forms(self):
        attacks = [
            "../etc/passwd",
            "a/../../etc/passwd",
            "/etc/passwd",
            "C:/Windows/System32",
            "file:///etc/passwd",
            "\\\\server\\share",
            "a\\..\\secret",
            "%2e%2e/%2e%2e/etc/passwd",
            "%252e%252e/etc/passwd",
            "README.md%00/../../etc/passwd",
        ]
        for attack in attacks:
            with self.subTest(attack=attack), self.assertRaises(PathViolation):
                normalize_relative_path(attack)

    def test_history_is_hidden_from_clients_but_available_internally(self):
        with self.assertRaises(PathViolation):
            normalize_relative_path("_history/a.md")
        self.assertEqual(
            normalize_relative_path("_history/a.md", allow_history=True),
            "_history/a.md",
        )

    def test_write_extensions_are_allowlisted(self):
        ensure_write_extension("decisions/ADR-001.md", (".md",))
        with self.assertRaises(PathViolation):
            ensure_write_extension("payload.exe", (".md",))

    def test_permission_mapping_distinguishes_read_and_write(self):
        self.assertEqual(
            required_permissions({"method": "tools/call", "params": {"name": "vault_read"}}),
            {"read"},
        )
        self.assertEqual(
            required_permissions({"method": "tools/call", "params": {"name": "vault_write"}}),
            {"write"},
        )
        self.assertEqual(
            required_permissions([
                {"method": "tools/call", "params": {"name": "vault_read"}},
                {"method": "tools/call", "params": {"name": "vault_move"}},
            ]),
            {"read", "write"},
        )


if __name__ == "__main__":
    unittest.main()
