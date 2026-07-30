#!/usr/bin/env python3
"""Read-only provider-neutral validation занятых sequence journal."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INDEX = "docs/agent-system/engine-journal/INDEX.md"
LEDGER = "docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json"
SEQ_RE = re.compile(r"^\d{4}$")
STATES = {"reserved", "consumed", "abandoned"}
PROVIDER_STATES = {"open", "closed", "merged"}


@dataclass(frozen=True)
class Finding:
    path: str
    code: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    occupied_sequences: list[str] = field(default_factory=list)
    next_sequence: str = "0001"

    @property
    def result(self) -> str:
        return "passed" if not self.findings else "failed"

    def payload(self) -> dict[str, object]:
        value = asdict(self)
        value["findings_count"] = len(self.findings)
        value["result"] = self.result
        return value


def add(report: Report, path: str, code: str) -> None:
    report.findings.append(Finding(path=path, code=code))


def load(path: Path, report: Report, code: str) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        add(report, path.as_posix(), code)
        return None


def index_claims(root: Path, report: Report) -> dict[str, str]:
    path = root / INDEX
    claims: dict[str, str] = {}
    if not path.exists():
        add(report, INDEX, "INDEX_UNAVAILABLE")
        return claims
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 10 or not SEQ_RE.fullmatch(cells[0]):
            continue
        previous = claims.get(cells[0])
        if previous and previous != cells[1]:
            add(report, INDEX, "INDEX_DUPLICATE_SEQUENCE")
        claims[cells[0]] = cells[1]
    return claims


def valid_claim(value: object) -> tuple[str, str, str] | None:
    if not isinstance(value, dict) or value.get("metadata_version") != 1:
        return None
    sequence, task_id, reservation_id = value.get("sequence"), value.get("task_id"), value.get("reservation_id")
    if not isinstance(sequence, str) or not SEQ_RE.fullmatch(sequence):
        return None
    if not isinstance(task_id, str) or not task_id or not isinstance(reservation_id, str) or not reservation_id:
        return None
    return sequence, task_id, reservation_id


def ledger_claims(root: Path, report: Report) -> dict[str, tuple[str, str, str]]:
    path = root / LEDGER
    if not path.exists():
        return {}
    raw = load(path, report, "LEDGER_UNAVAILABLE")
    if not isinstance(raw, dict) or raw.get("schema_version") != 1 or not isinstance(raw.get("reservations"), list):
        add(report, LEDGER, "LEDGER_METADATA_INVALID")
        return {}
    claims: dict[str, tuple[str, str, str]] = {}
    for value in raw["reservations"]:
        claim = valid_claim(value)
        state = value.get("state") if isinstance(value, dict) else None
        if claim is None or state not in STATES:
            add(report, LEDGER, "LEDGER_RESERVATION_INVALID")
            continue
        expanded = (*claim, str(state))
        previous = claims.get(claim[0])
        if previous and previous != expanded:
            add(report, LEDGER, "LEDGER_SEQUENCE_CONFLICT")
        claims[claim[0]] = expanded
    return claims


def provider_claims(snapshot: Path | None, required: bool, report: Report, ledger: dict[str, tuple[str, str, str]]) -> dict[str, tuple[str, str, str]]:
    if snapshot is None:
        if required:
            add(report, "provider_snapshot", "PROVIDER_SNAPSHOT_REQUIRED")
        return {}
    raw = load(snapshot, report, "PROVIDER_SNAPSHOT_INVALID")
    if not isinstance(raw, dict) or raw.get("schema_version") != 1 or not isinstance(raw.get("provider"), str):
        add(report, snapshot.as_posix(), "PROVIDER_SNAPSHOT_METADATA_INVALID")
        return {}
    if raw.get("availability") != "available":
        add(report, snapshot.as_posix(), "PROVIDER_SNAPSHOT_UNAVAILABLE")
        return {}
    rows = raw.get("pull_requests")
    if not isinstance(rows, list):
        add(report, snapshot.as_posix(), "PROVIDER_SNAPSHOT_METADATA_INVALID")
        return {}
    claims: dict[str, tuple[str, str, str]] = {}
    for row in rows:
        if not isinstance(row, dict) or row.get("state") not in PROVIDER_STATES or not isinstance(row.get("head_sha"), str):
            add(report, snapshot.as_posix(), "PROVIDER_PR_METADATA_INVALID")
            continue
        for value in row.get("reservation_claims", []):
            claim = valid_claim(value)
            if claim is None:
                add(report, snapshot.as_posix(), "PROVIDER_RESERVATION_METADATA_INVALID")
                continue
            state = str(row["state"])
            ledger_claim = ledger.get(claim[0])
            # Closed without merge stays occupied unless the append-only ledger marks it abandoned.
            if state == "closed" and ledger_claim == (*claim, "abandoned"):
                continue
            expanded = (*claim, state)
            previous = claims.get(claim[0])
            if previous and previous[:3] != expanded[:3]:
                add(report, snapshot.as_posix(), "PROVIDER_SEQUENCE_CONFLICT")
            claims[claim[0]] = expanded
    return claims


def validate(root: Path, snapshot: Path | None = None, require_provider_snapshot: bool = False) -> Report:
    report = Report()
    indexed = index_claims(root, report)
    ledger = ledger_claims(root, report)
    provider = provider_claims(snapshot, require_provider_snapshot, report, ledger)
    occupied: set[str] = set(indexed) | set(ledger) | set(provider)
    for sequence, claim in ledger.items():
        indexed_task = indexed.get(sequence)
        if indexed_task and indexed_task != claim[1]:
            add(report, LEDGER, "LEDGER_INDEX_TASK_ID_MISMATCH")
        task_file = root / f"docs/agent-system/engine-journal/input/TASK-{sequence}-{claim[1]}.md"
        if indexed_task == claim[1] and not task_file.exists():
            add(report, task_file.as_posix(), "RESERVATION_TASK_TRIPLET_MISSING")
    for sequence, claim in provider.items():
        indexed_task = indexed.get(sequence)
        ledger_claim = ledger.get(sequence)
        if indexed_task and indexed_task != claim[1]:
            add(report, INDEX, "INDEX_PROVIDER_TASK_ID_MISMATCH")
        if ledger_claim and ledger_claim[:3] != claim[:3]:
            add(report, LEDGER, "LEDGER_PROVIDER_RESERVATION_MISMATCH")
    report.occupied_sequences = sorted(occupied)
    report.next_sequence = f"{max((int(value) for value in occupied), default=0) + 1:04d}"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Проверяет provider-neutral reservations sequence journal.")
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--require-provider-snapshot", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = validate(ROOT, args.snapshot, args.require_provider_snapshot)
    if args.json:
        print(json.dumps(report.payload(), ensure_ascii=False, indent=2))
    else:
        print(f"validate_journal_sequence_reservations: {report.result}; next_sequence={report.next_sequence}")
        for finding in report.findings:
            print(f"- {finding.path}: {finding.code}")
    return 0 if report.result == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
