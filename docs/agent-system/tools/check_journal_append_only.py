#!/usr/bin/env python3
"""Проверяет append-only режим для существующих TASK/RESULT journal artifacts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
JOURNAL_ARTIFACT_RE = re.compile(
    r"^docs/agent-system/engine-journal/(?:input|output)/.+\.md$"
)


@dataclass
class Finding:
    path: str
    code: str


@dataclass
class Report:
    base: str
    checked_paths: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "passed" if not self.findings else "failed"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["checked_paths_count"] = len(self.checked_paths)
        data["findings_count"] = len(self.findings)
        data["result"] = self.result
        return data


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def normalize(path: str) -> str:
    return path.replace("\\", "/")


def name_status(base: str) -> list[tuple[str, str]]:
    result = run_git(["diff", "--name-status", "--find-renames", f"{base}...HEAD"])
    if result.returncode != 0:
        return []
    rows: list[tuple[str, str]] = []
    for raw in result.stdout.splitlines():
        parts = raw.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0]
        path = normalize(parts[-1])
        rows.append((status, path))
    return rows


def has_removed_lines(base: str, path: str) -> bool:
    result = run_git(["diff", "--unified=0", f"{base}...HEAD", "--", path])
    if result.returncode != 0:
        return True
    for line in result.stdout.splitlines():
        if line.startswith("---") or line.startswith("@@"):
            continue
        if line.startswith("-"):
            return True
    return False


def check(base: str) -> Report:
    report = Report(base=base)
    for status, path in name_status(base):
        if not JOURNAL_ARTIFACT_RE.match(path):
            continue
        report.checked_paths.append(path)
        if status.startswith("A"):
            continue
        if status.startswith("D"):
            report.findings.append(Finding(path=path, code="JOURNAL_ARTIFACT_DELETED"))
            continue
        if status.startswith("R"):
            report.findings.append(Finding(path=path, code="JOURNAL_ARTIFACT_RENAMED"))
            continue
        if has_removed_lines(base, path):
            report.findings.append(Finding(path=path, code="JOURNAL_ARTIFACT_REMOVED_LINES"))
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Проверяет, что существующие TASK/RESULT не переписываются и не удаляются.",
    )
    parser.add_argument("--base", default="origin/developer")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    report = check(args.base)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2))
    else:
        print("check_journal_append_only")
        print(f"base: {report.base}")
        print(f"checked_paths_count: {len(report.checked_paths)}")
        print(f"findings_count: {len(report.findings)}")
        print(f"result: {report.result}")
        for finding in report.findings:
            print(f"- {finding.path}: {finding.code}")
    return 0 if report.result == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
