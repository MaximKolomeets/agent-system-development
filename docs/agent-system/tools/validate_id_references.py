#!/usr/bin/env python3
"""Read-only проверка dangling references для канонических methodology ID."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SCAN_ROOT = ROOT / "docs/agent-system"
ID_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])"
    r"(?:F-09\.\d+|CTRL-[A-Z0-9-]+|(?:IMPORT|UNIT|REFERENCE|ARTIFACT|AUDIT|RENDER|PIPELINE)_[A-Z0-9][A-Z0-9_.-]*)"
    r"(?![A-Za-z0-9_.-])"
)
SCANNED_SUFFIXES = {".md", ".yml", ".yaml", ".txt"}
EXCLUDED_DIRS = {"cloud", "source", "agents"}


@dataclass
class IdOccurrence:
    identifier: str
    file: str
    line: int
    kind: str


@dataclass
class IdIssue:
    identifier: str
    file: str
    line: int
    code: str


@dataclass
class ValidationReport:
    root: str = ""
    scanned_files: list[str] = field(default_factory=list)
    definitions: list[IdOccurrence] = field(default_factory=list)
    references: list[IdOccurrence] = field(default_factory=list)
    issues: list[IdIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "valid" if not self.issues else "invalid"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["scanned_files_count"] = len(self.scanned_files)
        data["definitions_count"] = len(self.definitions)
        data["references_count"] = len(self.references)
        data["issues_count"] = len(self.issues)
        data["warnings_count"] = len(self.warnings)
        data["result"] = self.result
        return data


def normalize_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_root(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def is_safe_scan_file(path: Path) -> bool:
    if path.name == ".env" or path.name.startswith(".env."):
        return False
    if path.suffix.lower() not in SCANNED_SUFFIXES:
        return False
    parts = set(path.relative_to(ROOT).parts) if path.is_relative_to(ROOT) else set(path.parts)
    if EXCLUDED_DIRS & parts:
        return False
    if "engine-journal" in parts and ({"input", "output"} & parts):
        return False
    return True


def collect_scan_files(root: Path) -> tuple[list[Path], list[str]]:
    if not root.exists():
        return [], [f"scan root not found: {normalize_path(root)}"]
    if root.is_file():
        if is_safe_scan_file(root):
            return [root], []
        return [], [f"scan root is not an allowed text file: {normalize_path(root)}"]

    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and is_safe_scan_file(path):
            files.append(path)
    return files, []


def first_table_cell(line: str) -> str:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return ""
    cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
    return cells[0] if cells else ""


def starts_with_identifier(prefix_re: str, line: str, identifier: str) -> bool:
    escaped = re.escape(identifier)
    return re.match(rf"{prefix_re}`?{escaped}`?(?:\s|:|-|–|—|$)", line) is not None


def is_definition_occurrence(line: str, identifier: str) -> bool:
    stripped = line.strip()
    if first_table_cell(stripped) == identifier:
        return True
    if starts_with_identifier(r"^#{1,6}\s+", stripped, identifier):
        return True
    if starts_with_identifier(r"^[-*]\s+", stripped, identifier):
        return True
    if starts_with_identifier(r"^\d+\.\s+", stripped, identifier):
        return True

    escaped = re.escape(identifier)
    yaml_keys = (
        "id",
        "feature_id",
        "control_id",
        "import_id",
        "unit_id",
        "reference_id",
        "artifact_id",
        "audit_id",
        "render_id",
        "pipeline_id",
    )
    yaml_key_re = "|".join(re.escape(key) for key in yaml_keys)
    if re.match(rf"^(?:{yaml_key_re}):\s+`?{escaped}`?(?:\s|$)", stripped):
        return True
    return False


def scan_text(file_label: str, text: str) -> tuple[list[IdOccurrence], list[IdOccurrence]]:
    definitions: list[IdOccurrence] = []
    references: list[IdOccurrence] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in ID_TOKEN_RE.finditer(line):
            identifier = match.group(0)
            if is_definition_occurrence(line, identifier):
                definitions.append(IdOccurrence(identifier, file_label, line_number, "definition"))
            else:
                references.append(IdOccurrence(identifier, file_label, line_number, "reference"))
    return definitions, references


def build_report(root: Path, sample_text: str = "") -> ValidationReport:
    report = ValidationReport(root=normalize_path(root))
    if sample_text:
        report.scanned_files = ["<sample-text>"]
        definitions, references = scan_text("<sample-text>", sample_text)
        report.definitions.extend(definitions)
        report.references.extend(references)
    else:
        files, warnings = collect_scan_files(root)
        report.warnings.extend(warnings)
        report.scanned_files = [normalize_path(path) for path in files]
        for path in files:
            text = path.read_text(encoding="utf-8", errors="replace")
            definitions, references = scan_text(normalize_path(path), text)
            report.definitions.extend(definitions)
            report.references.extend(references)

    defined_ids = {occurrence.identifier for occurrence in report.definitions}
    for occurrence in report.references:
        if occurrence.identifier not in defined_ids:
            report.issues.append(
                IdIssue(
                    identifier=occurrence.identifier,
                    file=occurrence.file,
                    line=occurrence.line,
                    code="DANGLING_ID_REFERENCE",
                )
            )
    return report


def render_human(report: ValidationReport) -> str:
    lines = [
        "validate_id_references",
        "",
        f"root: {report.root}",
        f"scanned_files_count: {len(report.scanned_files)}",
        f"definitions_count: {len(report.definitions)}",
        f"references_count: {len(report.references)}",
        f"issues_count: {len(report.issues)}",
        f"warnings_count: {len(report.warnings)}",
        f"result: {report.result}",
    ]
    if report.issues:
        lines.append("")
        lines.append("issues:")
        for issue in report.issues:
            lines.append(f"- {issue.file}:{issue.line}: {issue.identifier}: {issue.code}")
    if report.warnings:
        lines.append("")
        lines.append("warnings:")
        lines.extend(f"- {warning}" for warning in report.warnings)
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate methodology ID references: F-09.N, CTRL-* and "
            "IMPORT_/UNIT_/REFERENCE_/ARTIFACT_/AUDIT_/RENDER_/PIPELINE_*."
        ),
    )
    parser.add_argument("--root", default="docs/agent-system", help="Root file or directory to scan.")
    parser.add_argument("--sample-text", help=r"Validate one text string; '\n' is converted to newline.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args(argv)

    root = resolve_root(args.root)
    sample_text = args.sample_text.replace("\\n", "\n") if args.sample_text else ""
    report = build_report(root, sample_text=sample_text)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")
    return 0 if report.result == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
