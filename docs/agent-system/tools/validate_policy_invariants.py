#!/usr/bin/env python3
"""Read-only self-test сквозных policy-инвариантов методологии."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
POLICY_FILE = "docs/agent-system/POLICY_INVARIANTS.md"
MANIFEST_FILE = "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml"

INVARIANT_IDS = (
    "INV-RELEASE-AUTHORITY",
    "INV-BRANCH-MODEL",
    "INV-TIME-COST-ACCOUNTING",
    "INV-SOURCE-REFERENCE",
    "INV-PRIVACY-PUBLICATION",
    "INV-TARGET-ADOPTION",
)

REQUIRED_CANONICAL_FILES = (
    POLICY_FILE,
    MANIFEST_FILE,
    "README.md",
    "docs/agent-system/README.md",
    "docs/agent-system/RELEASE_AUTHORITY_POLICY.md",
    "docs/agent-system/HUMAN_GATE_POLICY.md",
    "docs/agent-system/BRANCH_POLICY.md",
    "docs/agent-system/HOTFIX_AND_ROLLBACK_POLICY.md",
    "docs/agent-system/DISASTER_RECOVERY.md",
    "docs/agent-system/TIME_ACCOUNTING_POLICY.md",
    "docs/agent-system/COST_TRACKING_POLICY.md",
    "docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md",
    "docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md",
    "docs/agent-system/PUBLICATION_POLICY.md",
    "docs/agent-system/SOURCE_CONSUMERS.md",
    "docs/agent-system/SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE.md",
    "docs/agent-system/METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE.md",
    "docs/agent-system/METHODOLOGY_IMPROVEMENT_LEDGER.md",
    "docs/agent-system/TARGET_ADOPTION_DETECTOR.md",
    "docs/agent-system/TASK_CONTRACT.md",
    "docs/agent-system/templates/TASK_HEADER_COMMON.md",
    "docs/agent-system/tools/check_task_ready.py",
    "docs/agent-system/tools/validate_id_references.py",
    "docs/agent-system/tools/validate_policy_invariants.py",
)

ACTIVE_DOC_SUFFIXES = {".md", ".yml", ".yaml", ".txt"}
ACTIVE_DOC_EXCLUDED_PARTS = {"cloud", "engine-journal", "agents", "source"}
MANIFEST_EXISTENCE_CATEGORIES = {"source", "template", "scaffold", "generated"}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


@dataclass(frozen=True)
class RequiredText:
    path: str
    tokens: tuple[str, ...]
    code: str


@dataclass
class Issue:
    file: str
    line: int
    code: str
    detail: str


@dataclass
class ValidationReport:
    root: str = ""
    invariant_ids: list[str] = field(default_factory=list)
    canonical_files_checked: list[str] = field(default_factory=list)
    manifest_paths_checked: list[str] = field(default_factory=list)
    active_docs_scanned: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "valid" if not self.issues else "invalid"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["issues"] = [asdict(issue) for issue in self.issues]
        data["invariants_count"] = len(self.invariant_ids)
        data["canonical_files_checked_count"] = len(self.canonical_files_checked)
        data["manifest_paths_checked_count"] = len(self.manifest_paths_checked)
        data["active_docs_scanned_count"] = len(self.active_docs_scanned)
        data["issues_count"] = len(self.issues)
        data["warnings_count"] = len(self.warnings)
        data["result"] = self.result
        return data


REQUIRED_TEXT = (
    RequiredText(
        "docs/agent-system/RELEASE_AUTHORITY_POLICY.md",
        ("Merge release PR `developer -> main`", "Только человек-архитектор", "release_authority_action"),
        "RELEASE_AUTHORITY_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/HUMAN_GATE_POLICY.md",
        ("Merge в `main`", "Создание annotated release tag", "Rollback/hotfix final decision"),
        "HUMAN_GATE_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/BRANCH_POLICY.md",
        ("`main` обновляется ТОЛЬКО через release-PR", "work/<role>/<task>", "Pre-commit branch guard", "Repository sync / checkout guard"),
        "BRANCH_MODEL_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/tools/check_task_ready.py",
        ("changed files on protected branch", "changed files outside work/* branch", "ACCOUNTING_REQUIRED_RESULT_FIELDS"),
        "READY_GATE_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/TIME_ACCOUNTING_POLICY.md",
        ("time_spent", "actor_type", "human_time_reported"),
        "TIME_ACCOUNTING_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/COST_TRACKING_POLICY.md",
        ("input_tokens", "output_tokens", "total_task_cost"),
        "COST_TRACKING_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md",
        ("source_ref", "origin/main", "developer", "work/*"),
        "SOURCE_REFERENCE_MARKER_MISSING",
    ),
    RequiredText(
        MANIFEST_FILE,
        ("methodology_reference_schema:", "source_ref: origin/main", "methodology_development_base_schema:", "target_generated:"),
        "MANIFEST_SCHEMA_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md",
        ("source_ref: origin/main", "stable_only: true", "developer", "work/*"),
        "TARGET_ADOPTION_REFERENCE_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/PUBLICATION_POLICY.md",
        ("Реальные methodology consumers", "private adoption matrix", "generic templates"),
        "PUBLICATION_PRIVACY_MARKER_MISSING",
    ),
    RequiredText(
        "docs/agent-system/SOURCE_CONSUMERS.md",
        ("Заполненные private registries", "не коммитятся", "generic-placeholder"),
        "SOURCE_CONSUMERS_PRIVACY_MARKER_MISSING",
    ),
)


def normalize_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(path: str) -> Path:
    return ROOT / path


def safe_read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def first_token_line(text: str, token: str) -> int:
    for line_number, line in enumerate(text.splitlines(), start=1):
        if token in line:
            return line_number
    return 0


def add_issue(report: ValidationReport, file: str, line: int, code: str, detail: str) -> None:
    report.issues.append(Issue(file=file, line=line, code=code, detail=detail))


def check_required_files(report: ValidationReport) -> None:
    for path in REQUIRED_CANONICAL_FILES:
        report.canonical_files_checked.append(path)
        if not repo_path(path).exists():
            add_issue(report, path, 0, "MISSING_CANONICAL_FILE", path)


def check_policy_file(report: ValidationReport) -> None:
    path = repo_path(POLICY_FILE)
    if not path.exists():
        return
    text = safe_read(path)
    report.invariant_ids = list(INVARIANT_IDS)
    for invariant_id in INVARIANT_IDS:
        if invariant_id not in text:
            add_issue(report, POLICY_FILE, 0, "MISSING_INVARIANT_ID", invariant_id)


def check_required_text(report: ValidationReport) -> None:
    for marker in REQUIRED_TEXT:
        path = repo_path(marker.path)
        if not path.exists():
            continue
        text = safe_read(path)
        missing = [token for token in marker.tokens if token not in text]
        if missing:
            line = first_token_line(text, marker.tokens[0])
            # Печатаем только token labels, не строку документа.
            add_issue(report, marker.path, line, marker.code, ", ".join(missing))


def parse_manifest_paths(report: ValidationReport) -> tuple[set[str], set[str], set[str]]:
    source_required: set[str] = set()
    target_generated: set[str] = set()
    target_source_templates: set[str] = set()
    path = repo_path(MANIFEST_FILE)
    if not path.exists():
        return source_required, target_generated, target_source_templates

    category = ""
    field = ""
    in_target_source_templates = False
    for raw_line in safe_read(path).splitlines():
        category_match = re.match(r"^  ([a-z_]+):\s*$", raw_line)
        if category_match:
            category = category_match.group(1)
            field = ""
            in_target_source_templates = False
            continue
        field_match = re.match(r"^\s{4}([a-z_]+):\s*(?:>|.*)?$", raw_line)
        if field_match:
            field = field_match.group(1)
            if field != "source_templates":
                in_target_source_templates = False

        if category == "target_generated":
            target_match = re.match(r"^\s{6}- path:\s+(.+?)\s*$", raw_line)
            if field == "files" and target_match:
                target_generated.add(target_match.group(1).strip())
                in_target_source_templates = False
                continue
            if re.match(r"^\s{8}source_templates:\s*$", raw_line):
                in_target_source_templates = True
                continue
            source_template_match = re.match(r"^\s{10}-\s+(.+?)\s*$", raw_line)
            if in_target_source_templates and source_template_match:
                target_source_templates.add(source_template_match.group(1).strip())
                continue

        if category in MANIFEST_EXISTENCE_CATEGORIES and field == "files":
            item_match = re.match(r"^\s{6}-\s+(.+?)\s*$", raw_line)
            if item_match:
                item = item_match.group(1).strip()
                if "*" not in item and not item.startswith("#"):
                    source_required.add(item)

    return source_required, target_generated, target_source_templates


def check_manifest_paths(report: ValidationReport) -> None:
    source_required, _target_generated, target_source_templates = parse_manifest_paths(report)
    for path in sorted(source_required | target_source_templates):
        report.manifest_paths_checked.append(path)
        if not repo_path(path).exists():
            add_issue(report, MANIFEST_FILE, 0, "MISSING_MANIFEST_SOURCE_PATH", path)


def is_active_doc(path: Path) -> bool:
    if path.suffix.lower() not in ACTIVE_DOC_SUFFIXES:
        return False
    try:
        parts = set(path.relative_to(ROOT).parts)
    except ValueError:
        return False
    if ACTIVE_DOC_EXCLUDED_PARTS & parts:
        return False
    if path.name == ".env" or path.name.startswith(".env."):
        return False
    return True


def collect_active_docs() -> list[Path]:
    roots = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "docs" / "agent-system"]
    files: list[Path] = []
    for root in roots:
        if root.is_file() and is_active_doc(root):
            files.append(root)
        elif root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file() and is_active_doc(path))
    return sorted(set(files))


def should_ignore_link(target: str) -> bool:
    stripped = target.strip().strip("<>")
    if not stripped or stripped.startswith("#"):
        return True
    if "://" in stripped or stripped.startswith(("mailto:", "app://")):
        return True
    if "<" in stripped or ">" in stripped:
        return True
    return False


def resolve_link(base_file: Path, target: str) -> Path:
    clean = target.strip().strip("<>").split("#", 1)[0]
    return (base_file.parent / clean).resolve()


def check_markdown_links(report: ValidationReport) -> None:
    for path in collect_active_docs():
        label = normalize_path(path)
        report.active_docs_scanned.append(label)
        text = safe_read(path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in MARKDOWN_LINK_RE.finditer(line):
                target = match.group(1)
                if should_ignore_link(target):
                    continue
                resolved = resolve_link(path, target)
                if not resolved.exists():
                    add_issue(report, label, line_number, "BROKEN_MARKDOWN_LINK", target)


def build_report() -> ValidationReport:
    report = ValidationReport(root=normalize_path(ROOT))
    check_required_files(report)
    check_policy_file(report)
    check_required_text(report)
    check_manifest_paths(report)
    check_markdown_links(report)
    return report


def render_human(report: ValidationReport) -> str:
    lines = [
        "validate_policy_invariants",
        "",
        f"root: {report.root}",
        f"policy_file: {POLICY_FILE}",
        f"invariants_count: {len(report.invariant_ids)}",
        f"canonical_files_checked_count: {len(report.canonical_files_checked)}",
        f"manifest_paths_checked_count: {len(report.manifest_paths_checked)}",
        f"active_docs_scanned_count: {len(report.active_docs_scanned)}",
        f"issues_count: {len(report.issues)}",
        f"warnings_count: {len(report.warnings)}",
        f"result: {report.result}",
    ]
    if report.issues:
        lines.append("")
        lines.append("issues:")
        for issue in report.issues:
            line = issue.line if issue.line else "?"
            lines.append(f"- {issue.file}:{line}: {issue.code}: {issue.detail}")
    if report.warnings:
        lines.append("")
        lines.append("warnings:")
        lines.extend(f"- {warning}" for warning in report.warnings)
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only validation for methodology policy invariants and self-test links.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args(argv)

    report = build_report()
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")
    return 0 if report.result == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
