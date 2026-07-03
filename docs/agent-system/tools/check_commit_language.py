#!/usr/bin/env python3
"""Узкая проверка Russian-first текста commit message без анализа diff."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONVENTIONAL_RE = re.compile(r"^[a-z]+(?:\([A-Za-z0-9._-]+\))?!?:\s*(?P<text>.+)$")
CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z]{2,}\b")


@dataclass
class Finding:
    ref: str
    line: int
    code: str


@dataclass
class Report:
    base: str
    cutoff_ref: str = ""
    commits_checked: list[str] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "passed" if not self.findings else "failed"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["commits_checked_count"] = len(self.commits_checked)
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


def rev_list(base: str, cutoff_ref: str = "") -> list[str]:
    args = ["rev-list", "--reverse", "--no-merges"]
    if cutoff_ref:
        args.extend(["HEAD", "--not", base, cutoff_ref])
    else:
        args.append(f"{base}..HEAD")
    result = run_git(args)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def read_message(sha: str) -> list[str]:
    result = run_git(["log", "-1", "--format=%B", sha])
    if result.returncode != 0:
        return []
    return result.stdout.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n").split("\n")


def looks_like_path_or_identifier(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if "`" in stripped:
        return True
    if "://" in stripped:
        return True
    if "/" in stripped or "\\" in stripped:
        return True
    if re.fullmatch(r"[A-Za-z0-9._:-]+", stripped):
        return True
    return False


def prose_needs_russian(text: str) -> bool:
    stripped = text.strip()
    if not stripped or CYRILLIC_RE.search(stripped):
        return False
    if looks_like_path_or_identifier(stripped):
        return False
    words = LATIN_WORD_RE.findall(stripped)
    if len(words) < 4:
        return False
    # Узкий паттерн: блокируем только очевидную английскую prose, не identifiers.
    return any(marker in stripped for marker in (".", ",", ":", ";")) or len(words) >= 7


def subject_text(subject: str) -> str:
    match = CONVENTIONAL_RE.match(subject)
    return match.group("text") if match else subject


def check_message(sha: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    if not lines:
        return findings

    if prose_needs_russian(subject_text(lines[0])):
        findings.append(Finding(ref=sha, line=1, code="SUBJECT_PROSE_NOT_RUSSIAN_FIRST"))

    in_fence = False
    for number, line in enumerate(lines[1:], start=2):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped or stripped.startswith(("-", "*", "|", "#")):
            continue
        if prose_needs_russian(stripped):
            findings.append(Finding(ref=sha, line=number, code="BODY_PROSE_NOT_RUSSIAN_FIRST"))
    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Проверяет Russian-first prose в commit messages без печати текста сообщений.",
    )
    parser.add_argument("--base", default="origin/developer")
    parser.add_argument("--commit-message-cutoff-ref", default="")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    report = Report(base=args.base, cutoff_ref=args.commit_message_cutoff_ref)
    report.commits_checked = rev_list(args.base, args.commit_message_cutoff_ref)
    for sha in report.commits_checked:
        report.findings.extend(check_message(sha, read_message(sha)))

    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2))
    else:
        print("check_commit_language")
        print(f"base: {report.base}")
        print(f"cutoff_ref: {report.cutoff_ref or '<none>'}")
        print(f"commits_checked_count: {len(report.commits_checked)}")
        print(f"findings_count: {len(report.findings)}")
        print(f"result: {report.result}")
        for finding in report.findings:
            print(f"- {finding.ref}:{finding.line}: {finding.code}")
    return 0 if report.result == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
