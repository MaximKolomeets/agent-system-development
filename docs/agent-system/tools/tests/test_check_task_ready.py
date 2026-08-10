import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_task_ready as ready


def completed(args, stdout="", returncode=0):
    return subprocess.CompletedProcess(args=args, returncode=returncode, stdout=stdout, stderr="")


class CheckTaskReadyTests(unittest.TestCase):
    task_path = "docs/agent-system/engine-journal/input/TASK-0176-METH-TEST-01.md"
    result_path = "docs/agent-system/engine-journal/output/RESULT-0176-METH-TEST-01.md"
    rationale_path = "docs/agent-system/engine-journal/rationale/RATIONALE-0176-METH-TEST-01.md"

    def deferred_reason(self, path, line):
        return ready.deferred_finalization_reason(path, line)

    def scanned_paths(self, path, text, extra_paths=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_text(text, encoding="utf-8")
            for extra_path in extra_paths:
                extra_target = root / extra_path
                extra_target.parent.mkdir(parents=True, exist_ok=True)
                extra_target.write_text("# substantive source\n", encoding="utf-8")
            with mock.patch.object(ready, "ROOT", root):
                return ready.scan_deferred_finalization_placeholders([path, *extra_paths])

    def placeholder_paths(self, path, text, extra_paths=()):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_text(text, encoding="utf-8")
            for extra_path in extra_paths:
                extra_target = root / extra_path
                extra_target.parent.mkdir(parents=True, exist_ok=True)
                extra_target.write_text("# substantive source\n", encoding="utf-8")
            with mock.patch.object(ready, "ROOT", root):
                return ready.scan_placeholders([path, *extra_paths])

    def safety_scan_blockers(self, path, text):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_text(text, encoding="utf-8")
            report = ready.ReadyReport(base="origin/developer", changed_files=[path])
            with (
                mock.patch.object(ready, "ROOT", root),
                mock.patch.object(ready, "scan_added_secret_values", return_value=[]),
                mock.patch.object(ready, "scan_placeholders", return_value=[]),
                mock.patch.object(ready, "scan_superseded_banners", return_value=[]),
                mock.patch.object(ready, "scan_execution_timing", return_value=[]),
                mock.patch.object(ready, "scan_accounting_fields", return_value=([], [], [], [], {})),
            ):
                ready.add_safety_scans(report)
            return report

    def test_exact_premerge_verdict_is_accepted_only_in_task_result_context(self):
        line = "release_gate_verdict: PASS_PENDING_HUMAN_MERGE"
        self.assertIsNone(self.deferred_reason(self.task_path, line))
        self.assertIsNone(self.deferred_reason(self.result_path, line))
        self.assertEqual([], self.scanned_paths(self.task_path, line + "\n"))
        self.assertEqual(
            "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID",
            self.deferred_reason(self.rationale_path, line),
        )

    def terminal_fold_document(self, extra=""):
        line = "Статус финализации: terminal-fold accepted pending own PR merge; PR URL authoritative after merge"
        return (
            "# RESULT-0176-METH-TEST-01\n\n"
            "Идентификатор задачи: METH-TEST-01\n"
            "Номер sequence: 0176\n"
            f"{line}\n{extra}"
        )

    def test_exact_premerge_terminal_fold_requires_canonical_result_header(self):
        text = self.terminal_fold_document()
        self.assertEqual([], self.scanned_paths(self.result_path, text))
        self.assertEqual([], self.placeholder_paths(self.result_path, text))
        self.assertEqual(
            ready.PREMERGE_TERMINAL_FOLD_STATUS_LINE,
            ready.canonical_result_header_status(text),
        )

    def test_premerge_terminal_fold_wrong_context_or_shape_is_blocking(self):
        value = "terminal-fold accepted pending own PR merge; PR URL authoritative after merge"
        cases = (
            (self.task_path, f"Статус финализации: {value}", "DEFERRED_FINALIZATION_TERMINAL_FOLD_CONTEXT_INVALID"),
            (self.rationale_path, f"Статус финализации: {value}", "DEFERRED_FINALIZATION_TERMINAL_FOLD_CONTEXT_INVALID"),
            (self.result_path, value, "DEFERRED_FINALIZATION_TERMINAL_FOLD_INVALID"),
            (self.result_path, f"Статус финализации: {value}; extra", "DEFERRED_FINALIZATION_TERMINAL_FOLD_INVALID"),
            (self.result_path, "Статус финализации: terminal-fold accepted pending merge", "DEFERRED_FINALIZATION_TERMINAL_FOLD_INVALID"),
        )
        for path, line, reason in cases:
            with self.subTest(path=path, line=line):
                self.assertEqual(reason, self.deferred_reason(path, line))
                self.assertEqual([path], self.scanned_paths(path, line + "\n"))

    def test_terminal_fold_outside_canonical_header_is_always_blocking(self):
        line = ready.PREMERGE_TERMINAL_FOLD_STATUS_LINE
        cases = (
            line + "\n",
            f"{chr(96) * 3}text\n{line}\n{chr(96) * 3}\n",
            f"<!--\n{line}\n-->\n",
            f"- пример\n{line}\n",
            f"> пример\n{line}\n",
            f"    {line}\n",
            f"<x data=\">\">\n{line}\n\n",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual([self.result_path], self.scanned_paths(self.result_path, text))
                self.assertEqual([self.result_path], self.placeholder_paths(self.result_path, text))

    def test_additional_marker_anywhere_blocks_canonical_header(self):
        conflicts = (
            "Статус финализации: ready_for_human_review\n",
            f"{chr(96) * 3}\n{ready.PREMERGE_TERMINAL_FOLD_STATUS_LINE}\n{chr(96) * 3}\n",
            f"<!--\n{ready.PREMERGE_TERMINAL_FOLD_STATUS_LINE}\n-->\n",
            f"- пример\n{ready.PREMERGE_TERMINAL_FOLD_STATUS_LINE}\n",
        )
        for extra in conflicts:
            text = self.terminal_fold_document(extra)
            with self.subTest(extra=extra):
                self.assertEqual([self.result_path], self.scanned_paths(self.result_path, text))
                self.assertEqual([self.result_path], self.placeholder_paths(self.result_path, text))

    def test_malformed_or_mismatched_result_header_is_blocking(self):
        valid = self.terminal_fold_document()
        cases = (
            valid.replace("Номер sequence: 0176", "Номер sequence: 0177"),
            valid.replace("Идентификатор задачи: METH-TEST-01", "Идентификатор задачи: METH-OTHER-01"),
            valid.replace("\n\nИдентификатор", "\nИдентификатор"),
            valid.replace("Статус финализации:", " Статус финализации:"),
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertIsNone(ready.canonical_result_header_status(text))
                self.assertEqual([self.result_path], self.scanned_paths(self.result_path, text))
                self.assertEqual([self.result_path], self.placeholder_paths(self.result_path, text))
    def test_premerge_terminal_fold_with_substantive_scope_is_blocking(self):
        line = "Статус финализации: terminal-fold accepted pending own PR merge; PR URL authoritative after merge"
        source_path = "docs/agent-system/tools/check_task_ready.py"
        self.assertEqual(
            "DEFERRED_FINALIZATION_TERMINAL_FOLD_SUBSTANTIVE",
            ready.deferred_finalization_reason(self.result_path, line, substantive_changes=True),
        )
        self.assertEqual([self.result_path], self.scanned_paths(self.result_path, line + "\n", (source_path,)))
        self.assertEqual([self.result_path], self.placeholder_paths(self.result_path, line + "\n", (source_path,)))

    def test_normal_terminal_status_remains_accepted(self):
        line = "Статус финализации: ready_for_human_review"
        self.assertIsNone(self.deferred_reason(self.result_path, line))
        self.assertEqual([], self.scanned_paths(self.result_path, line + "\n"))
    def test_terminal_fold_does_not_bypass_required_accounting(self):
        line = "Статус финализации: terminal-fold accepted pending own PR merge; PR URL authoritative after merge"
        blockers, warnings, _ = ready.validate_accounting_fields(self.result_path, line + "\n", hard=True)
        self.assertTrue(any("ACCOUNTING_FIELDS_MISSING" in item for item in blockers))
        self.assertEqual([], warnings)
    def test_ordinary_pending_marker_remains_blocking(self):
        line = "pending"
        self.assertEqual("DEFERRED_FINALIZATION_MARKER", self.deferred_reason(self.task_path, line))
        self.assertEqual([self.task_path], self.scanned_paths(self.task_path, line + "\n"))

    def test_pending_pr_url_remains_blocking(self):
        self.assertEqual(
            "DEFERRED_FINALIZATION_MARKER",
            self.deferred_reason(self.result_path, "PR URL: pending"),
        )

    def test_pending_checks_remain_blocking(self):
        self.assertEqual(
            "DEFERRED_FINALIZATION_MARKER",
            self.deferred_reason(self.result_path, "checks pending"),
        )

    def test_pending_final_head_remains_blocking(self):
        self.assertEqual(
            "DEFERRED_FINALIZATION_MARKER",
            self.deferred_reason(self.result_path, "pending final head"),
        )

    def test_allowlisted_token_in_arbitrary_text_does_not_bypass_guard(self):
        line = "Пример verdict PASS_PENDING_HUMAN_MERGE в произвольной фразе."
        self.assertEqual(
            "DEFERRED_FINALIZATION_PREMERGE_VERDICT_CONTEXT_INVALID",
            self.deferred_reason(self.task_path, line),
        )

    def test_unknown_or_modified_premerge_verdict_remains_blocking(self):
        self.assertEqual(
            "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID",
            self.deferred_reason(self.result_path, "release_gate_verdict: PASS_UNKNOWN"),
        )
        self.assertEqual(
            "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID",
            self.deferred_reason(
                self.result_path,
                "release_gate_verdict: PASS_PENDING_HUMAN_MERGE; checks will be recorded later",
            ),
        )

    def test_backticked_premerge_verdict_remains_blocking(self):
        line = "release_gate_verdict: `PASS_PENDING_HUMAN_MERGE`"
        self.assertEqual(
            "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID",
            self.deferred_reason(self.result_path, line),
        )

    def test_each_negative_marker_blocks_production_safety_scan(self):
        cases = (
            ("ordinary marker", "pending", "DEFERRED_FINALIZATION_MARKER"),
            ("PR URL", "PR URL: pending", "DEFERRED_FINALIZATION_MARKER"),
            ("checks", "checks pending", "DEFERRED_FINALIZATION_MARKER"),
            ("final head", "pending final head", "DEFERRED_FINALIZATION_MARKER"),
            (
                "arbitrary token",
                "Пример verdict PASS_PENDING_HUMAN_MERGE в произвольной фразе.",
                "DEFERRED_FINALIZATION_PREMERGE_VERDICT_CONTEXT_INVALID",
            ),
            ("unknown verdict", "release_gate_verdict: PASS_UNKNOWN", "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID"),
            (
                "modified verdict",
                "release_gate_verdict: PASS_PENDING_HUMAN_MERGE; checks later",
                "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID",
            ),
            (
                "backticked verdict",
                "release_gate_verdict: `PASS_PENDING_HUMAN_MERGE`",
                "DEFERRED_FINALIZATION_PREMERGE_VERDICT_INVALID",
            ),
        )
        for label, line, reason in cases:
            with self.subTest(label=label):
                self.assertEqual(reason, self.deferred_reason(self.result_path, line))
                report = self.safety_scan_blockers(self.result_path, line + "\n")
                self.assertEqual([self.result_path], report.deferred_finalization_placeholders)
                self.assertIn("deferred finalization placeholders detected in changed TASK/RESULT", report.blockers)

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
        self.assertEqual([failed, failed], report.journal_triplet_checks)
        self.assertIn("validate_journal_triplet.py failed", report.blockers)
        self.assertIn("validate_journal_sequence_reservations.py failed", report.blockers)

    def test_reservation_validator_receives_ready_gate_base(self):
        report = ready.ReadyReport(
            base="origin/developer",
            changed_files=["docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json"],
        )
        passed = ready.CommandResult("passed", 0, "passed")
        with mock.patch.object(ready, "run_command", return_value=passed) as runner:
            ready.add_journal_triplet_checks(report)
        reservation_args = runner.call_args_list[1].args[0]
        self.assertEqual(
            ["python", "docs/agent-system/tools/validate_journal_sequence_reservations.py", "--base", "origin/developer", "--json"],
            reservation_args,
        )


if __name__ == "__main__":
    unittest.main()
