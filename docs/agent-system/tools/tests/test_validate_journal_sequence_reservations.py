import json
import sys
import tempfile
import unittest
from pathlib import Path

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
        return {"id": "17", "state": state, "head_sha": "abc", "reservation_claims": [claim]}

    def codes(self, snapshot=None, required=False):
        return [item.code for item in validator.validate(self.root, snapshot, required).findings]

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
        self.ledger(self.reservation(state="abandoned"))
        self.assertEqual("0018", validator.validate(self.root).next_sequence)

    def test_16_reservation_must_match_task_triplet(self):
        self.index("0017", "METH-OPEN-01")
        self.ledger(self.reservation())
        self.assertIn("RESERVATION_TASK_TRIPLET_MISSING", self.codes())

    def test_17_legacy_index_rows_are_not_false_blockers(self):
        self.index("0016", "METH-LEGACY-01")
        self.assertEqual([], self.codes())


if __name__ == "__main__":
    unittest.main()
