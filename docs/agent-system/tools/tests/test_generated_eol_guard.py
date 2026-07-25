import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generated_eol_guard as guard


def completed(args, stdout="", returncode=0):
    return subprocess.CompletedProcess(args=args, returncode=returncode, stdout=stdout, stderr="")


class GeneratedEolGuardTests(unittest.TestCase):
    def fake_git(self, changed):
        def run(args):
            command = " ".join(args)
            paths = "\n".join(changed) + "\n"
            if "status --short" in command or "ls-files --others" in command:
                return completed(args)
            if "--name-only" in command:
                return completed(args, paths)
            if "--numstat" in command:
                if "--ignore-space-at-eol" in command:
                    return completed(args, f"1\t1\t{changed[0]}\n")
                return completed(args, "".join(f"1\t1\t{path}\n" for path in changed))
            return completed(args)
        return run

    def test_mixed_scope_preserves_content_and_eol_verdict(self):
        changed = ["docs/agent-system/engine-journal/INDEX.md", "docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md"]
        with mock.patch.object(guard, "run_git", side_effect=self.fake_git(changed)):
            with mock.patch.object(guard, "parse_cloud_readme_map", return_value={changed[1]: changed[0]}):
                report = guard.build_report("origin/developer", strict=False)
        categories = {item.path: item.category for item in report.files}
        self.assertEqual("content_changed", categories[changed[0]])
        self.assertEqual("whitespace_only_changed", categories[changed[1]])
        self.assertEqual("warning", report.result)

    def test_git_calls_are_batched_for_many_paths(self):
        changed = [f"docs/agent-system/templates/FILE-{number:03d}.md" for number in range(40)]
        spy = mock.Mock(side_effect=self.fake_git(changed))
        with mock.patch.object(guard, "run_git", spy):
            guard.build_report("origin/developer", strict=False)
        self.assertLessEqual(spy.call_count, 20)

    def test_status_is_the_single_source_for_untracked_paths(self):
        changed = ["docs/agent-system/templates/UNTRACKED.md"]
        with mock.patch.object(guard, "run_git", side_effect=self.fake_git(changed)):
            with mock.patch.object(guard, "untracked_files", side_effect=AssertionError("повторный scan не нужен")):
                report = guard.build_report("origin/developer", strict=False)
        self.assertIn(changed[0], report.changed_files)

    def test_git_metadata_is_not_text_scan_scope(self):
        self.assertFalse(guard.is_text_scope(".git/index"))
        self.assertFalse(guard.is_generated(".git/objects/pack/example.pack"))
