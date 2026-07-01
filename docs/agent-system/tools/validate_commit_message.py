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
DEFAULT_LANGUAGE_POLICY_PATH = ROOT / "docs/agent-system/LANGUAGE_POLICY.md"
DEFAULT_ALLOWED_SCOPES = ("agent-system",)
ALLOWED_TYPES = (
    "docs",
    "chore",
    "fix",
    "feat",
    "journal",
    "release",
    "refactor",
    "test",
)
ALLOWED_SUBJECT_RE = re.compile(
    rf"^(?P<type>{'|'.join(ALLOWED_TYPES)})\((?P<scope>[^)]+)\): .+$"
)
SCOPE_VALUE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
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
    config_path: str = ""
    allowed_scopes: list[str] = field(default_factory=list)
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


def normalize_scope(value: str) -> str:
    return value.strip().strip('"').strip("'")


def unique_scopes(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in values:
        scope = normalize_scope(raw)
        if not scope or scope in seen:
            continue
        result.append(scope)
        seen.add(scope)
    return result


def extract_yaml_blocks(text: str) -> list[str]:
    fence_re = re.compile(
        r"```(?:yaml|yml)[^\n]*\n(.*?)\n```",
        re.DOTALL | re.IGNORECASE,
    )
    return [match.group(1) for match in fence_re.finditer(text)]


def parse_inline_scope_list(value: str) -> list[str]:
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return []
    return unique_scopes([item.strip() for item in stripped[1:-1].split(",")])


def parse_allowed_scopes_from_yaml(block: str) -> list[str]:
    lines = block.splitlines()
    for index, raw in enumerate(lines):
        match = re.match(r"^(\s*)allowed_scopes:\s*(.*)$", raw)
        if not match:
            continue
        base_indent = len(match.group(1))
        inline_scopes = parse_inline_scope_list(match.group(2))
        if inline_scopes:
            return inline_scopes

        scopes: list[str] = []
        for child in lines[index + 1 :]:
            if not child.strip() or child.lstrip().startswith("#"):
                continue
            indent = len(child) - len(child.lstrip(" "))
            if indent <= base_indent:
                break
            item = re.match(r"^\s*-\s+(.+?)\s*$", child)
            if item:
                scopes.append(item.group(1))
        return unique_scopes(scopes)
    return []


def read_allowed_scopes(
    config_path: Path,
    extra_scopes: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    scopes = list(DEFAULT_ALLOWED_SCOPES)
    errors: list[str] = []
    if config_path.is_file():
        text = config_path.read_text(encoding="utf-8", errors="replace")
        for block in extract_yaml_blocks(text):
            configured = parse_allowed_scopes_from_yaml(block)
            if configured:
                scopes = configured
                break

    scopes = unique_scopes(scopes + (extra_scopes or []))
    invalid = [scope for scope in scopes if not SCOPE_VALUE_RE.match(scope)]
    if invalid:
        errors.extend(f"CONFIG_INVALID_SCOPE:{scope}" for scope in invalid)
        scopes = [scope for scope in scopes if SCOPE_VALUE_RE.match(scope)]
    if not scopes:
        errors.append("CONFIG_ALLOWED_SCOPES_EMPTY")
        scopes = list(DEFAULT_ALLOWED_SCOPES)
    return scopes, errors


def validate_message(ref: str, text: str, allowed_scopes: list[str]) -> CommitViolation | None:
    lines = normalize_message(text)
    codes: list[str] = []
    subject = lines[0] if lines else ""

    if not subject:
        codes.append("EMPTY_SUBJECT")
    else:
        if len(subject) > MAX_SUBJECT_LEN:
            codes.append("SUBJECT_TOO_LONG")
        subject_match = ALLOWED_SUBJECT_RE.match(subject)
        if not subject_match:
            codes.append("SUBJECT_FORMAT")
        elif subject_match.group("scope") not in allowed_scopes:
            codes.append("SUBJECT_SCOPE_NOT_ALLOWED")
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


def add_config_errors(report: ValidationReport, errors: list[str]) -> None:
    if errors:
        report.violations.append(CommitViolation(ref="<config>", codes=errors))


def validate_range(
    base: str,
    allowed_scopes: list[str],
    config_path: Path,
    config_errors: list[str],
) -> ValidationReport:
    report = ValidationReport(base=base, config_path=str(config_path), allowed_scopes=allowed_scopes)
    add_config_errors(report, config_errors)
    if config_errors:
        return report
    rev_list = run_git(["rev-list", "--reverse", f"{base}..HEAD"])
    if rev_list.returncode != 0:
        report.violations.append(CommitViolation(ref="<range>", codes=["RANGE_UNREADABLE"]))
        return report

    shas = [line.strip() for line in rev_list.stdout.splitlines() if line.strip()]
    report.commits_checked = shas
    for sha in shas:
        violation = validate_message(sha, read_commit_message(sha), allowed_scopes)
        if violation:
            report.violations.append(violation)
    return report


def validate_single(
    ref: str,
    text: str,
    base: str,
    allowed_scopes: list[str],
    config_path: Path,
    config_errors: list[str],
) -> ValidationReport:
    report = ValidationReport(base=base, config_path=str(config_path), allowed_scopes=allowed_scopes)
    add_config_errors(report, config_errors)
    report.commits_checked = [ref]
    if config_errors:
        return report
    violation = validate_message(ref, text, allowed_scopes)
    if violation:
        report.violations.append(violation)
    return report


def validate_file(
    path: Path,
    allowed_scopes: list[str],
    config_path: Path,
    config_errors: list[str],
) -> ValidationReport:
    text = path.read_text(encoding="utf-8", errors="replace")
    return validate_single(str(path), text, "message-file", allowed_scopes, config_path, config_errors)


def render_human(report: ValidationReport) -> str:
    lines = [
        "validate_commit_message",
        "",
        f"base: {report.base}",
        f"config_path: {report.config_path}",
        f"allowed_scopes: {', '.join(report.allowed_scopes)}",
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
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_LANGUAGE_POLICY_PATH,
        help="Markdown config with commit_metadata.allowed_scopes.",
    )
    parser.add_argument(
        "--allowed-scope",
        action="append",
        default=[],
        help="Additional allowed conventional-commit scope; can be repeated.",
    )
    parser.add_argument("--message-file", type=Path, help="Validate one message file instead of git range.")
    parser.add_argument("--message-text", help=r"Validate one message string; '\n' is converted to newline.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args()

    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    allowed_scopes, config_errors = read_allowed_scopes(config_path, args.allowed_scope)
    if args.message_file and args.message_text:
        parser.error("--message-file and --message-text are mutually exclusive")
    if args.message_file:
        report = validate_file(args.message_file, allowed_scopes, config_path, config_errors)
    elif args.message_text:
        report = validate_single(
            "<message-text>",
            args.message_text.replace("\\n", "\n"),
            "message-text",
            allowed_scopes,
            config_path,
            config_errors,
        )
    else:
        report = validate_range(args.base, allowed_scopes, config_path, config_errors)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")
    return 0 if report.result == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
