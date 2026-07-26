import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_task_ready as ready


def completed(args, stdout="", returncode=0):
    return subprocess.CompletedProcess(args=args, returncode=returncode, stdout=stdout, stderr="")


class CheckTaskReadyTests(unittest.TestCase):
    def test_git_cache_prevents_duplicate_identical_subprocess(self):
        spy = mock.Mock(return_value=completed(["git", "status", "--short"]))
        with mock.patch.object(ready.subprocess, "run", spy):
            with ready.git_cache_session():
                ready.run_git(["status", "--short"])
                ready.run_git(["status", "--short"])
                ready.run_git(["diff", "--name-only"])
        self.assertEqual(2, spy.call_count)

    def test_progress_is_written_to_stderr_without_polluting_json_stdout(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        def repository_guard(report):
            report.repo_root = "/test/repository"

        with (
            mock.patch.object(ready, "add_repository_guard", side_effect=repository_guard),
            mock.patch.object(ready, "add_changed_files"),
            mock.patch.object(ready, "add_diff_checks"),
            mock.patch.object(ready, "add_commit_message_checks"),
            mock.patch.object(ready, "add_id_reference_checks"),
            mock.patch.object(ready, "add_policy_invariant_checks"),
            mock.patch.object(ready, "add_journal_triplet_checks"),
            mock.patch.object(ready, "add_generated_checks"),
            mock.patch.object(ready, "add_safety_scans"),
            mock.patch.object(ready, "add_russian_first_lint"),
        ):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = ready.main(["--json"])
        self.assertEqual(0, exit_code)
        self.assertEqual("ready", __import__("json").loads(stdout.getvalue())["result"])
        self.assertIn("check_task_ready: проверка репозитория", stderr.getvalue())

    def test_nested_journal_validator_failure_remains_blocking(self):
        report = ready.ReadyReport(
            base="origin/developer",
            changed_files=["docs/agent-system/engine-journal/INDEX.md"],
        )
        failed = ready.CommandResult("validate_journal_triplet.py --json", 1, "failed")
        with mock.patch.object(ready, "run_command", return_value=failed):
            ready.add_journal_triplet_checks(report)
        self.assertEqual([failed], report.journal_triplet_checks)
        self.assertIn("validate_journal_triplet.py failed", report.blockers)


if __name__ == "__main__":
    unittest.main()
