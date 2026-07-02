#!/usr/bin/env python3
"""Генерирует PROJECT_FILE_MAP.md из ADOPTION_TRANSFER_MANIFEST.yml."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml"
OUTPUT = ROOT / "docs/agent-system/PROJECT_FILE_MAP.md"
CATEGORY_ORDER = [
    "source",
    "template",
    "target_generated",
    "history_state",
    "journal",
    "journal_archive",
    "scaffold",
    "generated",
]


@dataclass
class FileEntry:
    path: str
    description: str = ""


@dataclass
class Category:
    name: str
    description: str = ""
    files: list[FileEntry] = field(default_factory=list)


def _clean_folded_description(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


def parse_manifest(text: str) -> dict[str, Category]:
    categories = {name: Category(name=name) for name in CATEGORY_ORDER}
    current: str | None = None
    subkey: str | None = None
    description_buffer: list[str] = []
    current_path_entry: FileEntry | None = None

    def flush_description() -> None:
        nonlocal description_buffer
        if current and description_buffer:
            categories[current].description = _clean_folded_description(description_buffer)
            description_buffer = []

    for line in text.splitlines():
        match = re.match(r"  ([a-z_]+):\s*$", line)
        if match:
            flush_description()
            name = match.group(1)
            current = name if name in categories else None
            subkey = None
            current_path_entry = None
            continue

        if current is None:
            continue

        match = re.match(r"    ([a-z_]+):\s*(.*)$", line)
        if match:
            flush_description()
            subkey = match.group(1)
            current_path_entry = None
            if subkey == "description":
                value = match.group(2).strip()
                if value and value != ">":
                    categories[current].description = value
                elif value == ">":
                    description_buffer = []
            continue

        if subkey == "description":
            if line.startswith("      "):
                description_buffer.append(line)
            continue

        if subkey != "files":
            continue

        match = re.match(r"      - path:\s*(.+)$", line)
        if match:
            current_path_entry = FileEntry(path=match.group(1).strip())
            categories[current].files.append(current_path_entry)
            continue

        match = re.match(r"        description:\s*(.+)$", line)
        if match and current_path_entry is not None:
            current_path_entry.description = match.group(1).strip()
            continue

        match = re.match(r"      - (.+)$", line)
        if match:
            categories[current].files.append(FileEntry(path=match.group(1).strip()))
            current_path_entry = None

    flush_description()
    return categories


def render_file_map(categories: dict[str, Category]) -> str:
    lines: list[str] = [
        "# PROJECT_FILE_MAP",
        "",
        "AUTO-GENERATED — не править руками; регенерировать через `python docs/agent-system/tools/gen_file_map.py`.",
        "",
        "## Контракт",
        "",
        "- Источник истины: `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`.",
        "- Карта является производной repo-local view и не заменяет manifest.",
        "- Parity-check: `python docs/agent-system/tools/gen_file_map.py --check`.",
        "- `--check` сравнивает закоммиченную карту с регенерированной и проверяет наличие concrete source/template/generated files.",
        "",
    ]

    for name in CATEGORY_ORDER:
        category = categories[name]
        lines.append(f"## {name}")
        lines.append("")
        if category.description:
            lines.append(category.description)
            lines.append("")
        lines.append("| path | description from manifest |")
        lines.append("| --- | --- |")
        for entry in category.files:
            description = entry.description
            lines.append(f"| `{entry.path}` | {description} |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def concrete_files_to_check(categories: dict[str, Category]) -> list[str]:
    checked_categories = {"source", "template", "generated"}
    paths: list[str] = []
    for name in CATEGORY_ORDER:
        if name not in checked_categories:
            continue
        for entry in categories[name].files:
            if "*" not in entry.path:
                paths.append(entry.path)
    return paths


def check_existing_files(categories: dict[str, Category]) -> list[str]:
    missing: list[str] = []
    for path in concrete_files_to_check(categories):
        if not (ROOT / path).exists():
            missing.append(path)
    return missing


def generate() -> str:
    categories = parse_manifest(MANIFEST.read_text(encoding="utf-8"))
    return render_file_map(categories)


def write_output(content: str) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8", newline="\n")


def check_output(content: str, categories: dict[str, Category]) -> int:
    errors = 0
    missing = check_existing_files(categories)
    if missing:
        errors += 1
        print("Missing concrete source/template/generated files:", file=sys.stderr)
        for path in missing:
            print(f"- {path}", file=sys.stderr)

    current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
    if current != content:
        errors += 1
        diff = difflib.unified_diff(
            current.splitlines(keepends=True),
            content.splitlines(keepends=True),
            fromfile=str(OUTPUT),
            tofile="regenerated PROJECT_FILE_MAP.md",
        )
        print("PROJECT_FILE_MAP.md drift detected:", file=sys.stderr)
        print("".join(diff), file=sys.stderr)

    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate PROJECT_FILE_MAP.md from ADOPTION_TRANSFER_MANIFEST.yml.")
    parser.add_argument("--check", action="store_true", help="Check generated output and source/template/generated file parity.")
    args = parser.parse_args(argv)

    categories = parse_manifest(MANIFEST.read_text(encoding="utf-8"))
    content = render_file_map(categories)
    if args.check:
        return check_output(content, categories)
    write_output(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
