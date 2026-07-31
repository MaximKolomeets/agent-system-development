import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_journal_sequence_reservations as validator


HEADER = "| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |"
SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"


class ReservationValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.index("0016", "METH-BASE-01")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def index(self, sequence, task):
        row = f"| {sequence} | {task} | input/TASK-{sequence}-{task}.md | output/RESULT-{sequence}-{task}.md | rationale/RATIONALE-{sequence}-{task}.md | work/test | PR | merged | 1m | test |"
        self.write(validator.INDEX, f"{HEADER}\n{SEPARATOR}\n{row}\n")

    def ledger(self, *items):
        self.write(validator.LEDGER, json.dumps({"schema_version": 1, "reservations": list(items)}))

    def reservation(self, sequence="0017", task="METH-OPEN-01", reservation_id="r-0017", state="reserved"):
        return {"metadata_version": 1, "sequence": sequence, "task_id": task, "reservation_id": reservation_id, "state": state}

    def snapshot(self, rows, availability="available"):
        path = self.root / "snapshot.json"
        path.write_text(json.dumps({"schema_version": 1, "provider": "test", "availability": availability, "observed_at": "2026-01-01T00:00:00Z", "pull_requests": rows}), encoding="utf-8")
        return path

    def provider_row(self, claim, state="open"):
        provider_claim = {field: claim[field] for field in validator.CLAIM_FIELDS if field in claim}
        return {"id": "17", "state": state, "head_sha": "abc", "reservation_claims": [provider_claim]}

    def codes(self, snapshot=None, required=False, base=None):
        return [item.code for item in validator.validate(self.root, snapshot, required, base).findings]

    def test_01_open_0017_makes_next_0018(self):
        report = validator.validate(self.root, self.snapshot([self.provider_row(self.reservation())]), True)
        self.assertEqual("0018", report.next_sequence)

    def test_02_two_open_different_sequences(self):
        two = self.reservation("0018", "METH-OPEN-02", "r-0018")
        report = validator.validate(self.root, self.snapshot([self.provider_row(self.reservation()), self.provider_row(two)]), True)
        self.assertEqual([], report.findings)

    def test_03_two_open_same_sequence_is_hard_failure(self):
        duplicate = self.reservation("0017", "METH-OTHER-01", "other")
        self.assertIn("PROVIDER_SEQUENCE_CONFLICT", self.codes(self.snapshot([self.provider_row(self.reservation()), self.provider_row(duplicate)]), True))

    def test_04_index_provider_same_sequence_different_task_blocks(self):
        self.index("0017", "METH-INDEX-01")
        self.assertIn("INDEX_PROVIDER_TASK_ID_MISMATCH", self.codes(self.snapshot([self.provider_row(self.reservation())]), True))

    def test_05_same_reservation_is_idempotent(self):
        self.ledger(self.reservation())
        report = validator.validate(self.root, self.snapshot([self.provider_row(self.reservation())]), True)
        self.assertEqual([], report.findings)

    def test_06_closed_unmerged_remains_occupied_without_tombstone(self):
        report = validator.validate(self.root, self.snapshot([self.provider_row(self.reservation(), "closed")]), True)
        self.assertEqual("0018", report.next_sequence)

    def test_07_merged_pr_is_consumed(self):
        report = validator.validate(self.root, self.snapshot([self.provider_row(self.reservation(), "merged")]), True)
        self.assertEqual("0018", report.next_sequence)

    def test_08_required_provider_unavailable_fails_closed(self):
        self.assertIn("PROVIDER_SNAPSHOT_UNAVAILABLE", self.codes(self.snapshot([], "unavailable"), True))

    def test_09_no_parallel_preserves_last_plus_one(self):
        self.assertEqual("0017", validator.validate(self.root).next_sequence)

    def test_10_bootstrap_blocks_second_0017(self):
        self.ledger(self.reservation())
        report = validator.validate(self.root)
        self.assertEqual("0018", report.next_sequence)

    def test_11_validator_does_not_write_triplet_files(self):
        task = "docs/agent-system/engine-journal/input/TASK-0017-METH-OPEN-01.md"
        self.write(task, "original")
        validator.validate(self.root)
        self.assertEqual("original", (self.root / task).read_text(encoding="utf-8"))

    def test_12_unknown_metadata_is_rejected(self):
        bad = {"metadata_version": 99, "sequence": "0017", "task_id": "METH-OPEN-01", "reservation_id": "r"}
        self.assertIn("PROVIDER_RESERVATION_METADATA_INVALID", self.codes(self.snapshot([self.provider_row(bad)]), True))

    def test_13_parallel_race_claim_is_detected(self):
        self.ledger(self.reservation())
        other = self.reservation("0017", "METH-RACE-02", "r-race")
        self.assertIn("PROVIDER_SEQUENCE_CONFLICT", self.codes(self.snapshot([self.provider_row(self.reservation()), self.provider_row(other)]), True))

    def test_14_provider_name_does_not_change_semantics(self):
        snapshot = self.snapshot([self.provider_row(self.reservation())])
        data = json.loads(snapshot.read_text(encoding="utf-8")); data["provider"] = "gitlab"; snapshot.write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual("0018", validator.validate(self.root, snapshot, True).next_sequence)

    def test_15_abandoned_sequence_is_never_reused(self):
        self.ledger(self.reservation(), self.reservation(state="abandoned"))
        report = validator.validate(self.root)
        self.assertEqual([], report.findings)
        self.assertEqual("0018", report.next_sequence)

    def test_16_reservation_must_match_task_triplet(self):
        self.index("0017", "METH-OPEN-01")
        self.ledger(self.reservation())
        self.assertIn("RESERVATION_TASK_TRIPLET_MISSING", self.codes())

    def test_17_legacy_index_rows_are_not_false_blockers(self):
        self.index("0016", "METH-LEGACY-01")
        self.assertEqual([], self.codes())

    def test_18_active_ledger_reservation_without_provider_claim_blocks(self):
        self.ledger(self.reservation())
        self.assertIn("LEDGER_PROVIDER_CLAIM_MISSING", self.codes(self.snapshot([]), True))

    def test_19_matching_provider_claim_for_active_ledger_passes(self):
        self.ledger(self.reservation())
        self.assertNotIn("LEDGER_PROVIDER_CLAIM_MISSING", self.codes(self.snapshot([self.provider_row(self.reservation())]), True))

    def test_20_provider_claim_with_other_identity_blocks(self):
        self.ledger(self.reservation())
        other = self.reservation(task="METH-OTHER-01", reservation_id="r-other")
        codes = self.codes(self.snapshot([self.provider_row(other)]), True)
        self.assertIn("LEDGER_PROVIDER_CLAIM_MISSING", codes)
        self.assertIn("LEDGER_PROVIDER_RESERVATION_MISMATCH", codes)

    def test_21_duplicate_provider_claim_blocks(self):
        self.ledger(self.reservation())
        rows = [self.provider_row(self.reservation()), self.provider_row(self.reservation())]
        self.assertIn("PROVIDER_RESERVATION_DUPLICATE", self.codes(self.snapshot(rows), True))

    def test_22_reserved_to_abandoned_is_valid_append_only_transition(self):
        self.ledger(self.reservation(), self.reservation(state="abandoned"))
        self.assertNotIn("LEDGER_STATE_TRANSITION_INVALID", self.codes())

    def test_23_different_identities_for_one_ledger_sequence_block(self):
        self.ledger(self.reservation(), self.reservation(task="METH-OTHER-01", reservation_id="r-other"))
        self.assertIn("LEDGER_SEQUENCE_CONFLICT", self.codes())

    def test_24_terminal_state_cannot_return_to_reserved(self):
        self.ledger(self.reservation(), self.reservation(state="abandoned"), self.reservation(state="reserved"))
        self.assertIn("LEDGER_STATE_TRANSITION_INVALID", self.codes())

    def test_25_incompatible_terminal_transition_blocks(self):
        self.ledger(self.reservation(), self.reservation(state="abandoned"), self.reservation(state="consumed"))
        self.assertIn("LEDGER_STATE_TRANSITION_INVALID", self.codes())

    def history_codes(self, baseline, current):
        self.ledger(*current)
        with mock.patch.object(validator, "base_ledger_entries", return_value=list(baseline)):
            return self.codes(base="origin/developer")

    def test_26_deleting_base_ledger_record_blocks(self):
        self.assertIn("LEDGER_HISTORY_NOT_APPEND_ONLY", self.history_codes([self.reservation()], []))

    def test_27_changing_base_ledger_record_blocks(self):
        changed = self.reservation(task="METH-CHANGED-01")
        self.assertIn("LEDGER_HISTORY_NOT_APPEND_ONLY", self.history_codes([self.reservation()], [changed]))

    def test_28_reordering_base_ledger_records_blocks(self):
        second = self.reservation("0018", "METH-SECOND-01", "r-0018")
        self.assertIn("LEDGER_HISTORY_NOT_APPEND_ONLY", self.history_codes([self.reservation(), second], [second, self.reservation()]))

    def test_29_appending_ledger_record_after_base_passes_history_guard(self):
        second = self.reservation("0018", "METH-SECOND-01", "r-0018")
        self.assertNotIn("LEDGER_HISTORY_NOT_APPEND_ONLY", self.history_codes([self.reservation()], [self.reservation(), second]))

    def test_30_absent_ledger_on_valid_base_is_explicit_bootstrap(self):
        report = validator.Report()
        responses = [
            __import__("subprocess").CompletedProcess([], 0, "base\n", ""),
            __import__("subprocess").CompletedProcess([], 128, "", "missing path"),
            __import__("subprocess").CompletedProcess([], 0, "", ""),
        ]
        with mock.patch.object(validator.subprocess, "run", side_effect=responses):
            self.assertEqual([], validator.base_ledger_entries(self.root, "origin/developer", report))
        self.assertEqual([], report.findings)


if __name__ == "__main__":
    unittest.main()
