import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_journal_triplet as validator


def row(seq="0163", task="METH-TEST-01", rationale=None):
    rationale = rationale or f"rationale/RATIONALE-{seq}-{task}.md"
    return f"| {seq} | {task} | input/TASK-{seq}-{task}.md | output/RESULT-{seq}-{task}.md | {rationale} | work/x | https://example.invalid/pr | architect_ready | 1m | test |"


class IndexSchemaTests(unittest.TestCase):
    def test_valid_new_triplet_mapping_passes(self):
        text = "\n".join(["| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |", row()])
        self.assertEqual([], validator.validate_index_schema(text))

    def test_legacy_marker_passes(self):
        self.assertEqual([], validator.validate_index_schema("| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n" + row("0001", "METH-OLD-01", "legacy/not_required")))

    def test_nine_columns_blocked(self):
        text = "| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| 0001 | OLD | input/a | output/a | work/x | pr | status | 1m | note |"
        self.assertIn("INDEX_ROW_COLUMN_COUNT_INVALID", validator.validate_index_schema(text))

    def test_wrong_mapping_blocked(self):
        self.assertIn("INDEX_RATIONALE_MAPPING_INVALID", validator.validate_index_schema("| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n" + row(rationale="rationale/RATIONALE-0001-WRONG.md")))
