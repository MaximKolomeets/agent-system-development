import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release_gate as gate


class ReleaseGateRecoveryTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        completed = subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True, text=True, encoding="utf-8"
        )
        return completed.stdout.strip()

    def commit_all(self, root: Path, message: str) -> str:
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", message)
        return self.git(root, "rev-parse", "HEAD")

    def write_complete_recovery_evidence(self, root: Path) -> None:
        journal = root / "docs/agent-system/engine-journal"
        output = journal / "output"
        output.mkdir(parents=True, exist_ok=True)
        tasks = {
            "recovery": "METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01",
            "uat": "METH-RELEASE-V1-6-0-HUMAN-UAT-EVIDENCE-01",
            "reviewer": "METH-RELEASE-V1-6-0-FULL-PAYLOAD-CONSISTENCY-GATE-01",
        }
        rows = []
        sequences = {"recovery": "0173", "uat": "0174", "reviewer": "0175"}
        for name, task_id in tasks.items():
            sequence = sequences[name]
            result_name = f"RESULT-{sequence}-{task_id}.md"
            rows.append(
                f"| {sequence} | {task_id} | input/TASK-{sequence}-{task_id}.md | "
                f"output/{result_name} | rationale/RATIONALE-{sequence}-{task_id}.md | "
                "work/test | https://example.invalid/pr | merged | 1m | test |"
            )
            text = "status: merged\n"
            if name != "recovery":
                text += "RESULT closed after merge: yes\nINDEX closed after merge: yes\n"
            if name == "uat":
                text += "human_uat_status: PASS\n"
            if name == "reviewer":
                text += "release_gate_verdict: PASS_PENDING_HUMAN_MERGE\n"
            (output / result_name).write_text(text, encoding="utf-8")
        (journal / "INDEX.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
        events = [
            {"sequence": sequences[name], "task_id": tasks[name], "state": "consumed"}
            for name in ("uat", "reviewer")
        ]
        (journal / "SEQUENCE_RESERVATIONS.json").write_text(
            json.dumps({"reservations": events}), encoding="utf-8"
        )

    def test_candidate_snapshot_does_not_fall_back_to_newer_checkout(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init")
            self.git(root, "config", "user.name", "Test")
            self.git(root, "config", "user.email", "test@example.invalid")
            (root / "README.md").write_text("candidate without evidence\n", encoding="utf-8")
            candidate = self.commit_all(root, "initial candidate")
            self.write_complete_recovery_evidence(root)
            current = self.commit_all(root, "add later evidence")

            with mock.patch.object(gate, "ROOT", root):
                self.assertEqual((False, []), gate.recovery_evidence("v1.6.0", candidate))
                self.assertTrue(gate.recovery_evidence("v1.6.0", current)[0])

    def test_candidate_snapshot_fails_closed_for_missing_or_malformed_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.git(root, "init")
            self.git(root, "config", "user.name", "Test")
            self.git(root, "config", "user.email", "test@example.invalid")
            self.write_complete_recovery_evidence(root)
            complete = self.commit_all(root, "complete evidence")
            ledger = root / gate.LEDGER_PATH
            ledger.write_text("{not-json", encoding="utf-8")
            malformed = self.commit_all(root, "malformed ledger")

            with mock.patch.object(gate, "ROOT", root):
                self.assertTrue(gate.recovery_evidence("v1.6.0", complete)[0])
                self.assertFalse(gate.recovery_evidence("v1.6.0", malformed)[0])
                self.assertFalse(gate.recovery_evidence("v1.6.0", "0" * 40)[0])
                self.assertFalse(gate.recovery_evidence("v1.6.0", "HEAD")[0])

    def test_candidate_snapshot_fails_closed_for_each_missing_artifact_kind(self):
        missing_paths = (
            gate.INDEX_PATH,
            gate.LEDGER_PATH,
            "docs/agent-system/engine-journal/output/"
            "RESULT-0174-METH-RELEASE-V1-6-0-HUMAN-UAT-EVIDENCE-01.md",
        )
        for missing_path in missing_paths:
            with self.subTest(missing_path=missing_path), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.git(root, "init")
                self.git(root, "config", "user.name", "Test")
                self.git(root, "config", "user.email", "test@example.invalid")
                self.write_complete_recovery_evidence(root)
                Path(root, missing_path).unlink()
                candidate = self.commit_all(root, f"candidate without {Path(missing_path).name}")

                with mock.patch.object(gate, "ROOT", root):
                    self.assertFalse(gate.recovery_evidence("v1.6.0", candidate)[0])

    def build(self, *, main="main", candidate="candidate", recovery=False, evidence=True, ancestry=(True, True), tag_exists=False):
        refs = {"refs/tags/v1.5.5": "base", "origin/main": main, "origin/developer": candidate}

        def peeled(ref, report, blocker):
            return refs[ref]

        ancestry_iter = iter(ancestry)
        with (
            mock.patch.object(gate, "current_branch", return_value="developer"),
            mock.patch.object(gate, "list_tags", return_value=["v1.5.5"]),
            mock.patch.object(gate, "tag_exists", return_value=tag_exists),
            mock.patch.object(gate, "peeled_commit", side_effect=peeled),
            mock.patch.object(gate, "is_ancestor", side_effect=lambda *_: next(ancestry_iter)),
            mock.patch.object(gate, "recovery_evidence", return_value=(evidence, ["evidence"] if evidence else [])),
            mock.patch.object(gate, "count_payload"),
            mock.patch.object(gate, "check_journal_placeholders"),
            mock.patch.object(gate, "run_generated_and_state_gates"),
        ):
            return gate.build_report("v1.6.0", "origin/developer", recovery)

    def test_normal_release_accepts_main_at_last_tag(self):
        report = self.build(main="base")
        self.assertEqual("normal", report.release_mode)
        self.assertNotIn("MAIN_NOT_AT_LAST_RELEASE_TAG", report.blockers)

    def test_recovery_requires_explicit_opt_in(self):
        report = self.build()
        self.assertIn("MAIN_NOT_AT_LAST_RELEASE_TAG", report.blockers)

    def test_governance_recovery_accepts_complete_proof(self):
        report = self.build(recovery=True)
        self.assertEqual("governance_recovery", report.release_mode)
        self.assertEqual("passed", report.recovery_evidence_status)
        self.assertEqual([], report.blockers)

    def test_governance_recovery_blocks_missing_evidence(self):
        report = self.build(recovery=True, evidence=False)
        self.assertIn("RECOVERY_EVIDENCE_INCOMPLETE", report.blockers)

    def test_governance_recovery_blocks_base_tag_outside_main_history(self):
        report = self.build(recovery=True, ancestry=(False, True))
        self.assertIn("RECOVERY_BASE_TAG_NOT_ANCESTOR_MAIN", report.blockers)

    def test_governance_recovery_blocks_diverged_candidate(self):
        report = self.build(recovery=True, ancestry=(True, False))
        self.assertIn("RECOVERY_MAIN_NOT_ANCESTOR_CANDIDATE", report.blockers)

    def test_existing_target_tag_remains_blocking(self):
        report = self.build(recovery=True, tag_exists=True)
        self.assertIn("RELEASE_TAG_ALREADY_EXISTS", report.blockers)


if __name__ == "__main__":
    unittest.main()
