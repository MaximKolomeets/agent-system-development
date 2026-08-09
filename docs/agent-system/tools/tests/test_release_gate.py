import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release_gate as gate


class ReleaseGateRecoveryTests(unittest.TestCase):
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
