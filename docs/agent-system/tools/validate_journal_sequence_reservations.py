#!/usr/bin/env python3
"""Read-only provider-neutral validation занятых sequence journal."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INDEX = "docs/agent-system/engine-journal/INDEX.md"
LEDGER = "docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json"
SEQ_RE = re.compile(r"^\d{4}$")
STATES = {"reserved", "consumed", "abandoned"}
PROVIDER_STATES = {"open", "closed", "merged"}
CLAIM_FIELDS = {"metadata_version", "sequence", "task_id", "reservation_id"}
ALLOWED_TRANSITIONS = {("reserved", "abandoned"), ("reserved", "consumed")}


@dataclass(frozen=True)
class Finding:
    path: str
    code: str


@dataclass(frozen=True)
class IndexClaim:
    task_id: str
    status: str


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


def index_claims(root: Path, report: Report) -> dict[str, IndexClaim]:
    path = root / INDEX
    claims: dict[str, IndexClaim] = {}
    if not path.exists():
        add(report, INDEX, "INDEX_UNAVAILABLE")
        return claims
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 10 or not SEQ_RE.fullmatch(cells[0]):
            continue
        value = IndexClaim(task_id=cells[1], status=cells[7])
        previous = claims.get(cells[0])
        if previous and previous.task_id != value.task_id:
            add(report, INDEX, "INDEX_DUPLICATE_SEQUENCE")
        claims[cells[0]] = value
    return claims


def valid_claim(value: object, *, strict: bool = False) -> tuple[str, str, str] | None:
    if not isinstance(value, dict) or value.get("metadata_version") != 1:
        return None
    if strict and set(value) != CLAIM_FIELDS:
        return None
    sequence, task_id, reservation_id = value.get("sequence"), value.get("task_id"), value.get("reservation_id")
    if not isinstance(sequence, str) or not SEQ_RE.fullmatch(sequence):
        return None
    if not isinstance(task_id, str) or not task_id or not isinstance(reservation_id, str) or not reservation_id:
        return None
    return sequence, task_id, reservation_id


def ledger_entries(root: Path, report: Report) -> list[object] | None:
    path = root / LEDGER
    if not path.exists():
        return []
    raw = load(path, report, "LEDGER_UNAVAILABLE")
    if not isinstance(raw, dict) or raw.get("schema_version") != 1 or not isinstance(raw.get("reservations"), list):
        add(report, LEDGER, "LEDGER_METADATA_INVALID")
        return None
    return raw["reservations"]


def ledger_claims(entries: list[object], report: Report) -> dict[str, tuple[str, str, str, str]]:
    """Проверяет identity и допустимый append-only state stream каждой reservation."""
    claims: dict[str, tuple[str, str, str, str]] = {}
    for value in entries:
        claim = valid_claim(value)
        state = value.get("state") if isinstance(value, dict) else None
        if claim is None or state not in STATES:
            add(report, LEDGER, "LEDGER_RESERVATION_INVALID")
            continue
        expanded = (*claim, str(state))
        previous = claims.get(claim[0])
        if previous is None:
            if state != "reserved":
                add(report, LEDGER, "LEDGER_INITIAL_STATE_INVALID")
            claims[claim[0]] = expanded
            continue
        if previous[:3] != expanded[:3]:
            add(report, LEDGER, "LEDGER_SEQUENCE_CONFLICT")
            continue
        if (previous[3], expanded[3]) not in ALLOWED_TRANSITIONS:
            add(report, LEDGER, "LEDGER_STATE_TRANSITION_INVALID")
            continue
        claims[claim[0]] = expanded
    return claims


def base_ledger_entries(root: Path, base: str, report: Report) -> list[object] | None:
    """Читает ledger из base fail-closed, кроме явного bootstrap без файла."""
    verify = subprocess.run(["git", "rev-parse", "--verify", f"{base}^{{commit}}"], cwd=root, capture_output=True, text=True)
    if verify.returncode != 0:
        add(report, "base", "BASE_REF_UNAVAILABLE")
        return None
    show = subprocess.run(["git", "show", f"{base}:{LEDGER}"], cwd=root, capture_output=True, text=True)
    if show.returncode != 0:
        listed = subprocess.run(["git", "ls-tree", "--name-only", base, "--", LEDGER], cwd=root, capture_output=True, text=True)
        if listed.returncode == 0 and not listed.stdout.strip():
            return []
        add(report, f"{base}:{LEDGER}", "BASE_LEDGER_UNAVAILABLE")
        return None
    try:
        raw = json.loads(show.stdout)
    except json.JSONDecodeError:
        add(report, f"{base}:{LEDGER}", "BASE_LEDGER_METADATA_INVALID")
        return None
    if not isinstance(raw, dict) or raw.get("schema_version") != 1 or not isinstance(raw.get("reservations"), list):
        add(report, f"{base}:{LEDGER}", "BASE_LEDGER_METADATA_INVALID")
        return None
    return raw["reservations"]


def validate_ledger_history(root: Path, base: str | None, entries: list[object], report: Report) -> None:
    if not base:
        return
    previous = base_ledger_entries(root, base, report)
    if previous is None:
        return
    if len(entries) < len(previous) or entries[: len(previous)] != previous:
        add(report, LEDGER, "LEDGER_HISTORY_NOT_APPEND_ONLY")


def provider_claims(
    snapshot: Path | None,
    required: bool,
    report: Report,
    ledger: dict[str, tuple[str, str, str, str]],
) -> dict[str, list[tuple[str, str, str, str]]]:
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
    claims: dict[str, list[tuple[str, str, str, str]]] = {}
    for row in rows:
        if (
            not isinstance(row, dict)
            or row.get("state") not in PROVIDER_STATES
            or not isinstance(row.get("head_sha"), str)
            or not isinstance(row.get("reservation_claims"), list)
        ):
            add(report, snapshot.as_posix(), "PROVIDER_PR_METADATA_INVALID")
            continue
        for value in row["reservation_claims"]:
            claim = valid_claim(value, strict=True)
            if claim is None:
                add(report, snapshot.as_posix(), "PROVIDER_RESERVATION_METADATA_INVALID")
                continue
            claims.setdefault(claim[0], []).append((*claim, str(row["state"])))
    for sequence, values in claims.items():
        identities = {value[:3] for value in values}
        if len(values) > 1 and len(identities) == 1:
            add(report, snapshot.as_posix(), "PROVIDER_RESERVATION_DUPLICATE")
        elif len(identities) > 1:
            add(report, snapshot.as_posix(), "PROVIDER_SEQUENCE_CONFLICT")
    return claims


def is_consumed_by_index(indexed: dict[str, IndexClaim], claim: tuple[str, str, str, str]) -> bool:
    index = indexed.get(claim[0])
    return bool(index and index.task_id == claim[1] and index.status.startswith("merged"))


def validate(root: Path, snapshot: Path | None = None, require_provider_snapshot: bool = False, base: str | None = None) -> Report:
    report = Report()
    indexed = index_claims(root, report)
    entries = ledger_entries(root, report)
    ledger = ledger_claims(entries or [], report)
    if entries is not None:
        validate_ledger_history(root, base, entries, report)
    provider = provider_claims(snapshot, require_provider_snapshot, report, ledger)
    occupied: set[str] = set(indexed) | set(ledger) | set(provider)
    for sequence, claim in ledger.items():
        index = indexed.get(sequence)
        if index and index.task_id != claim[1]:
            add(report, LEDGER, "LEDGER_INDEX_TASK_ID_MISMATCH")
        if claim[3] == "consumed" and not is_consumed_by_index(indexed, claim):
            add(report, LEDGER, "LEDGER_CONSUMED_INDEX_MISMATCH")
        task_file = root / f"docs/agent-system/engine-journal/input/TASK-{sequence}-{claim[1]}.md"
        if index and index.task_id == claim[1] and not task_file.exists():
            add(report, task_file.as_posix(), "RESERVATION_TASK_TRIPLET_MISSING")
        # Локальный structural режим не подменяет provider evidence пустым snapshot.
        if snapshot is not None and claim[3] == "reserved" and not is_consumed_by_index(indexed, claim):
            matches = [value for value in provider.get(sequence, []) if value[:3] == claim[:3]]
            if not matches:
                add(report, LEDGER, "LEDGER_PROVIDER_CLAIM_MISSING")
    for sequence, values in provider.items():
        for claim in values:
            index = indexed.get(sequence)
            ledger_claim = ledger.get(sequence)
            if index and index.task_id != claim[1]:
                add(report, INDEX, "INDEX_PROVIDER_TASK_ID_MISMATCH")
            if ledger_claim and ledger_claim[:3] != claim[:3]:
                add(report, LEDGER, "LEDGER_PROVIDER_RESERVATION_MISMATCH")
            # Closed without merge cannot free a sequence before a matching abandoned tombstone.
            if claim[3] == "closed" and ledger_claim and ledger_claim[:3] == claim[:3] and ledger_claim[3] == "abandoned":
                continue
            occupied.add(sequence)
    report.occupied_sequences = sorted(occupied)
    report.next_sequence = f"{max((int(value) for value in occupied), default=0) + 1:04d}"
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Проверяет provider-neutral reservations sequence journal.")
    parser.add_argument("--snapshot", type=Path)
    parser.add_argument("--require-provider-snapshot", action="store_true")
    parser.add_argument("--base", help="Base ref для структурной append-only проверки ledger.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = validate(ROOT, args.snapshot, args.require_provider_snapshot, args.base)
    if args.json:
        print(json.dumps(report.payload(), ensure_ascii=False, indent=2))
    else:
        print(f"validate_journal_sequence_reservations: {report.result}; next_sequence={report.next_sequence}")
        for finding in report.findings:
            print(f"- {finding.path}: {finding.code}")
    return 0 if report.result == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
