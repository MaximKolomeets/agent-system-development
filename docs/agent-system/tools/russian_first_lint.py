#!/usr/bin/env python3
"""Легкая проверка Russian-first prose в активных методологических документах."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

EXCLUDED_PREFIXES = (
    "docs/agent-system/engine-journal/",
    "docs/agent-system/cloud/",
    "docs/agent-system/source/",
)

EXCLUDED_FILES = {
    "docs/agent-system/BACKLOG.md",
    "docs/agent-system/CURRENT_STATE.md",
    "docs/agent-system/DECISION_LOG.md",
    "docs/agent-system/NEXT_STEPS.md",
    "docs/agent-system/PROJECT_FILE_MAP.md",
    "docs/agent-system/RELEASE_READINESS.md",
    "docs/agent-system/RULESET_STATUS.md",
    "docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md",
}

CYRILLIC_RE = re.compile(r"[А-Яа-яЁё]")
LATIN_WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z]{2,}\b")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\([^)]+\)")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")


def run_git(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def changed_paths(base: str) -> list[str]:
    paths: set[str] = set()
    paths.update(run_git(["diff", "--name-only", f"{base}...HEAD"]))
    paths.update(run_git(["diff", "--name-only"]))
    paths.update(run_git(["diff", "--cached", "--name-only"]))
    paths.update(run_git(["ls-files", "--others", "--exclude-standard"]))
    return sorted(paths)


def tracked_markdown_paths() -> list[str]:
    tracked = run_git(["ls-files", "*.md"])
    untracked = run_git(["ls-files", "--others", "--exclude-standard", "*.md"])
    return sorted(set(tracked + untracked))


def is_active_markdown(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if not normalized.endswith(".md"):
        return False
    if normalized in EXCLUDED_FILES:
        return False
    return not any(normalized.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def strip_literal_regions(line: str) -> str:
    line = HTML_COMMENT_RE.sub("", line)
    line = MARKDOWN_LINK_RE.sub("", line)
    line = INLINE_CODE_RE.sub("", line)
    return line


def should_skip_line(line: str, in_fence: bool) -> bool:
    stripped = line.strip()
    if in_fence or not stripped:
        return True
    if stripped.startswith("|"):
        return True
    if stripped.startswith(("::", "<", ">", "---")):
        return True
    if set(stripped) <= {"-", ":", " ", "#"}:
        return True
    return False


def looks_like_english_prose(line: str) -> bool:
    text = strip_literal_regions(line).strip()
    if not text:
        return False
    if CYRILLIC_RE.search(text):
        return False

    words = LATIN_WORD_RE.findall(text)
    if len(words) < 4:
        return False

    # Команды и списки identifiers обычно содержат мало обычной пунктуации.
    prose_markers = sum(text.count(marker) for marker in (".", ",", ":"))
    if prose_markers == 0 and len(words) < 7:
        return False
    return True


def scan_file(path: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    absolute = ROOT / path
    if not absolute.exists() or not absolute.is_file():
        return findings

    in_fence = False
    for line_number, line in enumerate(
        absolute.read_text(encoding="utf-8", errors="replace").splitlines(),
        start=1,
    ):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if should_skip_line(line, in_fence):
            continue
        if looks_like_english_prose(line):
            findings.append(
                {
                    "path": path,
                    "line": line_number,
                    "code": "RUSSIAN_FIRST_ENGLISH_PROSE",
                }
            )
    return findings


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Проверяет active docs на англоязычную prose без печати содержимого строк.",
    )
    parser.add_argument("--base", default="origin/developer", help="Base ref для changed-only режима.")
    parser.add_argument("--all-active", action="store_true", help="Проверить все активные Markdown docs.")
    parser.add_argument("--json", action="store_true", help="Вывести machine-readable JSON.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    candidates = tracked_markdown_paths() if args.all_active else changed_paths(args.base)
    files = [path for path in candidates if is_active_markdown(path)]

    findings: list[dict[str, object]] = []
    for path in files:
        findings.extend(scan_file(path))

    result = {
        "result": "failed" if findings else "passed",
        "mode": "all-active" if args.all_active else "changed-only",
        "files_checked_count": len(files),
        "findings_count": len(findings),
        "findings": findings,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("russian_first_lint")
        print(f"result: {result['result']}")
        print(f"mode: {result['mode']}")
        print(f"files_checked_count: {result['files_checked_count']}")
        print(f"findings_count: {result['findings_count']}")
        for finding in findings:
            print(f"- {finding['path']}:{finding['line']}: {finding['code']}")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
