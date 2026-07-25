import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_journal_triplet as validator

HEADER = "| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |"
SEPARATOR = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"

class TripletWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.root = Path(self.temp.name)
        self.git("init"); self.git("config", "user.name", "test"); self.git("config", "user.email", "test@example.invalid")
        self.index([]); self.git("add", "."); self.git("commit", "-m", "base"); self.base = self.git("rev-parse", "HEAD").stdout.strip()
    def tearDown(self): self.temp.cleanup()
    def git(self, *args): return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True)
    def write(self, name, text):
        path=self.root/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8")
    def index(self, rows): self.write("docs/agent-system/engine-journal/INDEX.md", "\n".join([HEADER, SEPARATOR, *rows])+"\n")
    def row(self, seq="0001", task="METH-TEST-01", rationale=None):
        rationale=rationale or f"rationale/RATIONALE-{seq}-{task}.md"
        return f"| {seq} | {task} | input/TASK-{seq}-{task}.md | output/RESULT-{seq}-{task}.md | {rationale} | work/test | pr | review_changes_requested | 1m | test |"
    def triplet(self, raw=True, sections=True, seq="0001", task="METH-TEST-01"):
        root="docs/agent-system/engine-journal"; self.write(f"{root}/input/TASK-{seq}-{task}.md", f"{seq} {task}")
        marker="raw_chain_of_thought_stored: no" if raw else ""; required="\n".join(validator.REQUIRED_RATIONALE_SECTIONS) if sections else ""
        self.write(f"{root}/rationale/RATIONALE-{seq}-{task}.md", f"{seq} {task}\n{marker}\n{required}"); self.write(f"{root}/output/RESULT-{seq}-{task}.md", f"{seq} {task}")
    def check(self): self.git("add", "."); self.git("commit", "-m", "head"); return [f.code for f in validator.validate(self.root, self.base).findings]
    def test_valid_complete_triplet(self): self.triplet(); self.index([self.row()]); self.assertEqual([], self.check())
    def test_missing_artifact(self): self.triplet(); (self.root/"docs/agent-system/engine-journal/input/TASK-0001-METH-TEST-01.md").unlink(); self.index([self.row()]); self.assertIn("TRIPLET_INCOMPLETE", self.check())
    def test_missing_rationale(self): self.triplet(); (self.root/"docs/agent-system/engine-journal/rationale/RATIONALE-0001-METH-TEST-01.md").unlink(); self.index([self.row()]); self.assertIn("TRIPLET_INCOMPLETE", self.check())
    def test_missing_result(self): self.triplet(); (self.root/"docs/agent-system/engine-journal/output/RESULT-0001-METH-TEST-01.md").unlink(); self.index([self.row()]); self.assertIn("TRIPLET_INCOMPLETE", self.check())
    def test_identity_mismatch(self): self.triplet(); self.write("docs/agent-system/engine-journal/input/TASK-0001-METH-TEST-01.md", "0001 METH-WRONG-01"); self.index([self.row()]); self.assertIn("FILE_IDENTITY_MISMATCH", self.check())
    def test_wrong_index_link(self): self.triplet(); self.index([self.row(rationale="rationale/RATIONALE-0001-WRONG.md")]); self.assertIn("INDEX_RATIONALE_MAPPING_INVALID", self.check())
    def test_gap(self): self.triplet(seq="0002"); self.index([self.row(seq="0002")]); self.assertIn("SEQUENCE_GAP_OR_COLLISION", self.check())
    def test_duplicate_sequence(self): self.triplet(); self.index([self.row(), self.row()]); self.assertIn("INDEX_DUPLICATE_SEQUENCE_OR_TASK_ID", self.check())
    def test_nine_column_legacy(self): self.index(["| 0001 | OLD | input/a | output/a | branch | pr | status | 1m | note |"]); self.assertIn("INDEX_ROW_COLUMN_COUNT_INVALID", self.check())
    def test_legacy_marker(self): self.index([self.row(task="METH-OLD-01", rationale="legacy/not_required")]); self.assertEqual([], self.check())
    def test_repository_legacy_rows_are_migrated(self):
        source_index = Path(__file__).resolve().parents[2] / "engine-journal" / "INDEX.md"
        rows = [line for line in source_index.read_text(encoding="utf-8").splitlines() if line.startswith("| 0")]
        legacy = [line for line in rows if 1 <= int(line.split("|")[1].strip()) <= 162]
        self.assertEqual(162, len(legacy))
        for row in legacy:
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            self.assertEqual(10, len(cells))
            self.assertEqual("legacy/not_required", cells[4])
    def test_missing_raw_marker(self): self.triplet(raw=False); self.index([self.row()]); self.assertIn("RAW_CHAIN_OF_THOUGHT_MARKER_INVALID", self.check())
    def test_missing_required_rationale_section(self): self.triplet(sections=False); self.index([self.row()]); self.assertIn("RATIONALE_REQUIRED_SECTIONS_MISSING", self.check())
    def test_invalid_filename(self): self.write("docs/agent-system/engine-journal/rationale/RATIONALE-bad.md", "x"); self.index([]); self.assertIn("INVALID_JOURNAL_FILENAME", self.check())
    def test_index_only_missing_artifacts(self): self.index([self.row()]); self.assertIn("INDEX_ARTIFACTS_MISSING", self.check())
