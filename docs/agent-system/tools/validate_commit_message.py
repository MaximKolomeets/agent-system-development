#!/usr/bin/env python3
"""Read-only проверка формата commit message для methodology work PR."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
ALLOWED_SUBJECT_RE = re.compile(
    r"^(docs|chore|fix|feat|journal|release|refactor|test)\(agent-system\): .+$"
)
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
MAX_SUBJECT_LEN = 72
MAX_BODY_LINE_LEN = 72


@dataclass
class CommitViolation:
    ref: str
    codes: list[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    base: str = ""
    commits_checked: list[str] = field(default_factory=list)
    violations: list[CommitViolation] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "valid" if not self.violations else "invalid"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["commits_checked_count"] = len(self.commits_checked)
        data["violations_count"] = len(self.violations)
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


def normalize_message(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    if not normalized:
        return []
    return normalized.split("\n")


def has_body(lines: list[str]) -> bool:
    return len(lines) > 1 and any(line.strip() for line in lines[1:])


def length_exempt(line: str) -> bool:
    if re.search(r"https?://", line):
        return True
    if re.search(r"[A-Za-z]:\\", line):
        return True
    if re.search(r"(^|\s)([\w.-]+/)+[\w.-]+", line):
        return True
    if re.search(r"`[^`]*(/|\\)[^`]*`", line):
        return True
    return False


def validate_message(ref: str, text: str) -> CommitViolation | None:
    lines = normalize_message(text)
    codes: list[str] = []
    subject = lines[0] if lines else ""

    if not subject:
        codes.append("EMPTY_SUBJECT")
    else:
        if len(subject) > MAX_SUBJECT_LEN:
            codes.append("SUBJECT_TOO_LONG")
        if not ALLOWED_SUBJECT_RE.match(subject):
            codes.append("SUBJECT_FORMAT")
        tail = subject.split(":", 1)[1].strip() if ":" in subject else ""
        if not tail or not CYRILLIC_RE.search(tail):
            codes.append("SUBJECT_NOT_RUSSIAN_FIRST")

    if has_body(lines):
        if len(lines) < 2 or lines[1].strip():
            codes.append("BODY_MISSING_BLANK_SEPARATOR")
        for index, line in enumerate(lines[2:], start=3):
            if len(line) > MAX_BODY_LINE_LEN and not length_exempt(line):
                codes.append(f"BODY_LINE_TOO_LONG:{index}")

    return CommitViolation(ref=ref, codes=codes) if codes else None


def read_commit_message(sha: str) -> str:
    result = run_git(["log", "-1", "--format=%B", sha])
    if result.returncode != 0:
        raise RuntimeError(f"cannot read commit message for {sha}")
    return result.stdout


def validate_range(base: str) -> ValidationReport:
    report = ValidationReport(base=base)
    rev_list = run_git(["rev-list", "--reverse", f"{base}..HEAD"])
    if rev_list.returncode != 0:
        report.violations.append(CommitViolation(ref="<range>", codes=["RANGE_UNREADABLE"]))
        return report

    shas = [line.strip() for line in rev_list.stdout.splitlines() if line.strip()]
    report.commits_checked = shas
    for sha in shas:
        violation = validate_message(sha, read_commit_message(sha))
        if violation:
            report.violations.append(violation)
    return report


def validate_single(ref: str, text: str, base: str) -> ValidationReport:
    report = ValidationReport(base=base)
    report.commits_checked = [ref]
    violation = validate_message(ref, text)
    if violation:
        report.violations.append(violation)
    return report


def validate_file(path: Path) -> ValidationReport:
    text = path.read_text(encoding="utf-8", errors="replace")
    return validate_single(str(path), text, "message-file")


def render_human(report: ValidationReport) -> str:
    lines = [
        "validate_commit_message",
        "",
        f"base: {report.base}",
        f"commits_checked_count: {len(report.commits_checked)}",
        f"violations_count: {len(report.violations)}",
        f"result: {report.result}",
    ]
    if report.violations:
        lines.append("")
        lines.append("violations:")
        for violation in report.violations:
            lines.append(f"- {violation.ref}: {', '.join(violation.codes)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Russian-first conventional commit messages.",
    )
    parser.add_argument("--base", default="origin/developer", help="Base ref for commit range.")
    parser.add_argument("--message-file", type=Path, help="Validate one message file instead of git range.")
    parser.add_argument("--message-text", help=r"Validate one message string; '\n' is converted to newline.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args()

    if args.message_file and args.message_text:
        parser.error("--message-file and --message-text are mutually exclusive")
    if args.message_file:
        report = validate_file(args.message_file)
    elif args.message_text:
        report = validate_single("<message-text>", args.message_text.replace("\\n", "\n"), "message-text")
    else:
        report = validate_range(args.base)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")
    return 0 if report.result == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
