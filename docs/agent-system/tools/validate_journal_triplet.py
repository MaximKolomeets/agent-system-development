#!/usr/bin/env python3
"""Read-only проверка целостности новых TASK/RATIONALE/RESULT journal-троек."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PREFIX = "docs/agent-system/engine-journal/"
RESERVATION_LEDGER = "docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json"
PATTERN = re.compile(r"^(input/TASK|rationale/RATIONALE|output/RESULT)-(\d{4})-([A-Z0-9][A-Z0-9-]*)\.md$")
REQUIRED_RATIONALE_SECTIONS = (
    "## Решаемый вопрос", "## Контекст и evidence", "## Ограничения и инварианты",
    "## Рассмотренные варианты", "## Выбранный путь", "## Причины выбора",
    "## Отклонённые альтернативы", "## Компромиссы, последствия и риски",
    "## Предположения, неопределённости и confidence", "## Условия пересмотра или rollback triggers",
    "## Что явно не решалось", "## Связь с решениями", "## Изменения после review",
)


@dataclass(frozen=True)
class Finding:
    path: str
    code: str


@dataclass
class Report:
    base: str
    checked_paths: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    new_entries_count: int = 0

    @property
    def result(self) -> str:
        return "passed" if not self.findings else "failed"

    def payload(self) -> dict[str, object]:
        value = asdict(self)
        value["findings_count"] = len(self.findings)
        value["result"] = self.result
        return value


def git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)


def changed_paths(root: Path, base: str) -> set[str]:
    result = git(root, ["diff", "--name-only", f"{base}...HEAD"])
    cached = git(root, ["diff", "--cached", "--name-only"])
    untracked = git(root, ["ls-files", "--others", "--exclude-standard"])
    names: set[str] = set()
    for source in (result, cached, untracked):
        if source.returncode == 0:
            names.update(line.replace("\\", "/") for line in source.stdout.splitlines() if line.startswith(PREFIX))
    return names


def index_rows(text: str) -> list[list[str]]:
    return [
        [cell.strip() for cell in row.strip().strip("|").split("|")]
        for row in text.splitlines()
        if row.startswith("|") and not re.fullmatch(r"\|[\s|-]+\|", row)
    ]


def validate_index_schema(text: str) -> list[str]:
    lines = text.splitlines()
    header = "| Seq | Task id | Input file | Output file | Rationale file | Branch | PR | Status | Time | Notes |"
    separator = "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    findings: list[str] = []
    if header not in lines or separator not in lines:
        findings.append("INDEX_SCHEMA_INVALID")
    for row in index_rows(text):
        if not row or not re.fullmatch(r"\d{4}", row[0]):
            continue
        if len(row) != 10:
            findings.append("INDEX_ROW_COLUMN_COUNT_INVALID")
            continue
        seq, task_id, _, _, rationale = row[:5]
        if rationale == "legacy/not_required":
            continue
        expected = f"rationale/RATIONALE-{seq}-{task_id}.md"
        if rationale != expected:
            findings.append("INDEX_RATIONALE_MAPPING_INVALID")
    return findings


def max_seq(text: str) -> int:
    values = []
    for row in index_rows(text):
        if row and re.fullmatch(r"\d{4}", row[0]):
            values.append(int(row[0]))
    return max(values, default=0)


def add(report: Report, path: str, code: str) -> None:
    report.findings.append(Finding(path=path, code=code))


def expected_triplet_files(seq: str, task_id: str) -> dict[str, str]:
    return {
        "input/TASK": f"{PREFIX}input/TASK-{seq}-{task_id}.md",
        "rationale/RATIONALE": f"{PREFIX}rationale/RATIONALE-{seq}-{task_id}.md",
        "output/RESULT": f"{PREFIX}output/RESULT-{seq}-{task_id}.md",
    }


def parse_ledger_state(text: str) -> tuple[set[str], dict[str, str], dict[str, str], set[str]]:
    """Возвращает occupied sequence и активные matching reservations ledger.

    Structural validity ledger и provider claim проверяет отдельный validator.
    Здесь ledger используется только для проверки sequence gap: ``reserved``
    может materialize лишь для той же task id, а terminal ``consumed`` и
    ``abandoned`` остаются occupied tombstone. Некорректная запись не создаёт
    bypass и не отменяет ранее распознанное состояние.
    """
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return set(), {}, {}, set()
    entries = raw.get("reservations") if isinstance(raw, dict) else None
    if not isinstance(entries, list):
        return set(), {}, {}, set()
    occupied_states = {"reserved", "consumed", "abandoned"}
    occupied: set[str] = set()
    active_reservations: dict[str, str] = {}
    terminal_sequences: set[str] = set()
    terminal_reservations: dict[str, str] = {}
    invalid_sequences: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        sequence = entry.get("sequence")
        state = entry.get("state")
        task_id = entry.get("task_id")
        if not isinstance(sequence, str) or not re.fullmatch(r"\d{4}", sequence):
            # Невозможно надёжно связать malformed event с sequence: fail-closed
            # для всех active reservations, чтобы не создавать bypass.
            invalid_sequences.update(active_reservations)
            continue
        if state not in occupied_states or not isinstance(task_id, str) or not task_id:
            invalid_sequences.add(sequence)
            continue
        occupied.add(sequence)
        if sequence in invalid_sequences:
            continue
        if state == "reserved":
            if sequence in terminal_sequences or sequence in active_reservations:
                invalid_sequences.add(sequence)
            else:
                active_reservations[sequence] = task_id
        elif active_reservations.get(sequence) == task_id:
            del active_reservations[sequence]
            terminal_sequences.add(sequence)
            if state == "consumed":
                terminal_reservations[sequence] = task_id
        else:
            # Terminal event без matching active reservation не может подтвердить
            # lifecycle и не должен разрешать materialization.
            invalid_sequences.add(sequence)
    for sequence in invalid_sequences:
        active_reservations.pop(sequence, None)
        terminal_reservations.pop(sequence, None)
    return occupied, active_reservations, terminal_reservations, invalid_sequences


def ledger_sequence_state(root: Path, base: str) -> tuple[set[str], dict[str, str], set[str], set[str]]:
    """Сравнивает baseline/current lifecycle без переиспользования tombstone."""
    path = root / RESERVATION_LEDGER
    current_text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else "{}"
    base_result = git(root, ["show", f"{base}:{RESERVATION_LEDGER}"])
    base_text = base_result.stdout if base_result.returncode == 0 else "{}"
    occupied, active, consumed, invalid = parse_ledger_state(current_text)
    base_occupied, base_active, base_consumed, base_invalid = parse_ledger_state(base_text)
    materializable: dict[str, str] = {}
    for sequence, task_id in {**active, **consumed}.items():
        if sequence in invalid or sequence in base_invalid or sequence in base_consumed:
            continue
        if sequence not in base_occupied or base_active.get(sequence) == task_id:
            materializable[sequence] = task_id
    return occupied, materializable, base_occupied - set(base_active), invalid | base_invalid


def validate(root: Path, base: str) -> Report:
    report = Report(base=base)
    current_index = root / "docs/agent-system/engine-journal/INDEX.md"
    base_index = git(root, ["show", f"{base}:docs/agent-system/engine-journal/INDEX.md"])
    if not current_index.exists() or base_index.returncode != 0:
        add(report, "docs/agent-system/engine-journal/INDEX.md", "INDEX_UNAVAILABLE")
        return report
    paths = changed_paths(root, base)
    candidates: dict[tuple[str, str], dict[str, str]] = {}
    for path in sorted(paths):
        relative = path.removeprefix(PREFIX)
        match = PATTERN.fullmatch(relative)
        if not match:
            if relative.startswith(("input/TASK", "output/RESULT", "rationale/RATIONALE")):
                add(report, path, "INVALID_JOURNAL_FILENAME")
            continue
        kind, seq, task_id = match.groups()
        candidates.setdefault((seq, task_id), {})[kind] = path
        report.checked_paths.append(path)
    current_text = current_index.read_text(encoding="utf-8", errors="replace")
    for code in validate_index_schema(current_text):
        add(report, f"{PREFIX}INDEX.md", code)
    seen_index: set[tuple[str, str]] = set()
    for row in index_rows(current_text):
        if len(row) != 10 or not re.fullmatch(r"\d{4}", row[0]):
            continue
        key = (row[0], row[1])
        if key in seen_index:
            add(report, f"{PREFIX}INDEX.md", "INDEX_DUPLICATE_SEQUENCE_OR_TASK_ID")
        seen_index.add(key)
    base_row_map = {
        (row[0], row[1]): row
        for row in index_rows(base_index.stdout)
        if len(row) == 10 and re.fullmatch(r"\d{4}", row[0])
    }
    base_rows = set(base_row_map)
    current_row_map = {
        (row[0], row[1]): row
        for row in index_rows(current_text)
        if len(row) == 10 and re.fullmatch(r"\d{4}", row[0])
    }
    for key, row in current_row_map.items():
        if key in base_rows and row != base_row_map[key]:
            candidates.setdefault(key, expected_triplet_files(*key))
    for key in tuple(candidates):
        if key in base_rows:
            candidates[key] = expected_triplet_files(*key)
    for row in index_rows(current_text):
        if len(row) != 10 or not re.fullmatch(r"\d{4}", row[0]) or row[4] == "legacy/not_required":
            continue
        seq, task_id = row[:2]
        if (seq, task_id) in base_rows or (seq, task_id) in candidates:
            continue
        candidates[(seq, task_id)] = expected_triplet_files(seq, task_id)
        add(report, f"{PREFIX}INDEX.md", "INDEX_ARTIFACTS_MISSING")
    report.new_entries_count = sum(key not in base_rows for key in candidates)
    base_max = max_seq(base_index.stdout)
    expected = base_max + 1
    occupied_sequences, materializable_reservations, baseline_terminal, invalid_sequences = ledger_sequence_state(root, base)
    for (seq, task_id), files in sorted(candidates.items()):
        if (seq, task_id) not in base_rows:
            sequence_number = int(seq)
            matching_reservation = (
                seq not in invalid_sequences
                and seq not in baseline_terminal
                and materializable_reservations.get(seq) == task_id
            )
            if seq in occupied_sequences:
                # Только активная reservation той же задачи может materialize.
                # Terminal tombstone и reservation другой задачи остаются blocker.
                if not matching_reservation:
                    add(report, f"{PREFIX}INDEX.md", "SEQUENCE_GAP_OR_COLLISION")
                elif sequence_number >= expected:
                    while expected < sequence_number and f"{expected:04d}" in occupied_sequences:
                        expected += 1
                    if sequence_number != expected:
                        add(report, f"{PREFIX}INDEX.md", "SEQUENCE_GAP_OR_COLLISION")
                    else:
                        expected = sequence_number + 1
            elif sequence_number < expected:
                add(report, f"{PREFIX}INDEX.md", "SEQUENCE_GAP_OR_COLLISION")
            else:
                # Новая sequence без matching reservation не materialize даже
                # при арифметически ожидаемом номере.
                add(report, f"{PREFIX}INDEX.md", "SEQUENCE_GAP_OR_COLLISION")
        required = {"input/TASK", "rationale/RATIONALE", "output/RESULT"}
        if set(files) != required:
            add(report, f"{PREFIX}INDEX.md", "TRIPLET_INCOMPLETE")
            continue
        row_matches = [row for row in index_rows(current_text) if len(row) >= 5 and row[0] == seq and row[1] == task_id]
        if len(row_matches) != 1:
            add(report, f"{PREFIX}INDEX.md", "INDEX_ROW_MISSING_OR_DUPLICATE")
        else:
            row = row_matches[0]
            for path in files.values():
                if path.removeprefix(PREFIX) not in row:
                    add(report, f"{PREFIX}INDEX.md", "INDEX_TRIPLET_LINK_MISMATCH")
                    break
        for kind, path in files.items():
            if not (root / path).is_file():
                add(report, path, "INDEX_ARTIFACTS_MISSING")
                continue
            text = (root / path).read_text(encoding="utf-8", errors="replace")
            if seq not in text or task_id not in text:
                add(report, path, "FILE_IDENTITY_MISMATCH")
            if kind == "rationale/RATIONALE":
                if "raw_chain_of_thought_stored: no" not in text:
                    add(report, path, "RAW_CHAIN_OF_THOUGHT_MARKER_INVALID")
                if any(section not in text for section in REQUIRED_RATIONALE_SECTIONS):
                    add(report, path, "RATIONALE_REQUIRED_SECTIONS_MISSING")
    for row in index_rows(current_text):
        if len(row) == 10 and re.fullmatch(r"\d{4}", row[0]) and row[0] not in {seq for seq, _ in candidates}:
            rationale = row[4]
            if rationale != "legacy/not_required" and not rationale.startswith("rationale/RATIONALE-"):
                add(report, f"{PREFIX}INDEX.md", "LEGACY_RATIONALE_MARKER_INVALID")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверяет новые journal-тройки относительно base ref.")
    parser.add_argument("--base", default="origin/developer")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate(ROOT, args.base)
    if args.json:
        print(json.dumps(report.payload(), ensure_ascii=False, indent=2))
    else:
        print(f"validate_journal_triplet: {report.result}; findings={len(report.findings)}")
        for finding in report.findings:
            print(f"- {finding.path}: {finding.code}")
    return 0 if report.result == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
