#!/usr/bin/env python3
"""Read-only validation for fenced task_contract frontmatter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "version",
    "task_id",
    "role",
    "mode",
    "execution_mode",
    "repository.full_name",
    "repository.local_path",
    "repository.base_branch",
    "repository.working_branch",
    "scope.allowed_files",
    "scope.forbidden_files",
    "policies.journal",
    "policies.cloud_regen",
    "policies.review",
    "policies.merge",
    "checks.required",
    "stop_conditions",
)
ENUMS = {
    "mode": {"agent", "review_only", "ask", "manual"},
    "execution_mode": {"local_only", "cloud_allowed", "hybrid"},
    "policies.journal": {"required", "optional", "not_required", "batch_only"},
    "policies.cloud_regen": {"required", "if_bundle_source_changed", "not_required"},
    "policies.review": {"scoped_semantic", "scoped_technical_safety", "machine_only", "full_review", "not_required"},
    "policies.merge": {"human_only", "not_applicable"},
    "policies.closure_pr": {"true", "false", "boundary_only", True, False},
}
FORBIDDEN_TASK_FILENAMES = {".env"}


@dataclass
class ValidationReport:
    task_file: str
    task_id: str = ""
    version: str = ""
    role: str = ""
    mode: str = ""
    working_branch: str = ""
    required_fields: str = "failed"
    enum_values: str = "failed"
    branch_policy: str = "failed"
    scope_policy: str = "failed"
    checks_policy: str = "failed"
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "valid" if not self.blockers else "invalid"

    def to_json_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["blockers_count"] = len(self.blockers)
        data["warnings_count"] = len(self.warnings)
        data["result"] = self.result
        return data


class ContractParseError(ValueError):
    """Raised when the supported YAML subset cannot be parsed."""


def safe_read_text(path: Path) -> str:
    name = path.name.lower()
    if name in FORBIDDEN_TASK_FILENAMES or name.startswith(".env."):
        raise ContractParseError("refusing to read sensitive filename")
    return path.read_text(encoding="utf-8", errors="replace")


def extract_contract_block(text: str) -> str:
    fence_re = re.compile(r"```(?:yaml|yml)?[^\n]*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
    for match in fence_re.finditer(text):
        block = match.group(1)
        if re.search(r"(?m)^task_contract:\s*$", block):
            return block
    raise ContractParseError("fenced task_contract block not found")


def significant_lines(block: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    return lines


def parse_scalar(raw: str) -> Any:
    value = raw.strip().strip('"').strip("'")
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"\d+", value):
        return int(value)
    return value


def parse_yaml_subset(block: str) -> dict[str, Any]:
    lines = significant_lines(block)
    if not lines:
        raise ContractParseError("empty task_contract block")
    index, value = parse_node(lines, 0, lines[0][0])
    if index != len(lines):
        raise ContractParseError("unexpected trailing lines in task_contract")
    if not isinstance(value, dict):
        raise ContractParseError("task_contract root must be a mapping")
    return value


def parse_node(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[int, Any]:
    if index >= len(lines):
        return index, {}
    current_indent, text = lines[index]
    if current_indent != indent:
        raise ContractParseError("invalid indentation")
    if text.startswith("- "):
        return parse_list(lines, index, indent)
    return parse_dict(lines, index, indent)


def parse_dict(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[int, dict[str, Any]]:
    result: dict[str, Any] = {}
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ContractParseError("unexpected indentation")
        if text.startswith("- "):
            break
        match = re.match(r"^([A-Za-z0-9_]+):(?:\s*(.*))?$", text)
        if not match:
            raise ContractParseError("unsupported mapping line")
        key, raw_value = match.groups()
        raw_value = raw_value or ""
        index += 1
        if raw_value:
            result[key] = parse_scalar(raw_value)
            continue
        if index >= len(lines) or lines[index][0] <= current_indent:
            result[key] = {}
            continue
        index, child = parse_node(lines, index, lines[index][0])
        result[key] = child
    return index, result


def parse_list(lines: list[tuple[int, str]], index: int, indent: int) -> tuple[int, list[Any]]:
    result: list[Any] = []
    while index < len(lines):
        current_indent, text = lines[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ContractParseError("unexpected indentation inside list")
        if not text.startswith("- "):
            break
        item = text[2:].strip()
        index += 1
        if item:
            result.append(parse_scalar(item))
            continue
        if index >= len(lines) or lines[index][0] <= current_indent:
            result.append("")
            continue
        index, child = parse_node(lines, index, lines[index][0])
        result.append(child)
    return index, result


def get_path(data: dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, dict)):
        return bool(value)
    return str(value).strip() != ""


def validate_contract(data: dict[str, Any], task_file: Path) -> ValidationReport:
    contract = data.get("task_contract")
    report = ValidationReport(task_file=str(task_file))
    if not isinstance(contract, dict):
        report.blockers.append("task_contract root is missing or invalid")
        return report

    report.task_id = str(get_path(contract, "task_id") or "")
    report.version = str(get_path(contract, "version") or "")
    report.role = str(get_path(contract, "role") or "")
    report.mode = str(get_path(contract, "mode") or "")
    report.working_branch = str(get_path(contract, "repository.working_branch") or "")

    missing = [field for field in REQUIRED_FIELDS if not is_non_empty(get_path(contract, field))]
    if missing:
        report.blockers.append("missing required fields: " + ", ".join(missing))
    else:
        report.required_fields = "passed"

    enum_errors: list[str] = []
    for field, allowed in ENUMS.items():
        value = get_path(contract, field)
        if value is None:
            continue
        if value not in allowed and str(value) not in {str(item) for item in allowed}:
            enum_errors.append(f"{field}={value}")
    if enum_errors:
        report.blockers.append("invalid enum values: " + ", ".join(enum_errors))
    else:
        report.enum_values = "passed"

    base_branch = str(get_path(contract, "repository.base_branch") or "")
    task_id = report.task_id.upper()
    branch_errors: list[str] = []
    if not report.working_branch.startswith("work/"):
        branch_errors.append("repository.working_branch must start with work/")
    if base_branch == "main" and "RELEASE" not in task_id:
        branch_errors.append("repository.base_branch main is allowed only for explicit release tasks")
    if branch_errors:
        report.blockers.extend(branch_errors)
    else:
        report.branch_policy = "passed"

    allowed_files = get_path(contract, "scope.allowed_files")
    forbidden_files = get_path(contract, "scope.forbidden_files")
    scope_errors: list[str] = []
    if not isinstance(allowed_files, list) or not allowed_files:
        scope_errors.append("scope.allowed_files must be a non-empty list")
    if not isinstance(forbidden_files, list) or not forbidden_files:
        scope_errors.append("scope.forbidden_files must be a non-empty list")
    else:
        lowered = {str(item).lower() for item in forbidden_files}
        if ".env" not in lowered and ".env.*" not in lowered:
            scope_errors.append("scope.forbidden_files must include .env or .env.*")
    merge_policy = get_path(contract, "policies.merge")
    if report.mode in {"agent", "review_only"} and merge_policy != "human_only":
        scope_errors.append("policies.merge must be human_only for substantive/review tasks")
    if scope_errors:
        report.blockers.extend(scope_errors)
    else:
        report.scope_policy = "passed"

    required_checks = get_path(contract, "checks.required")
    if not isinstance(required_checks, list):
        report.blockers.append("checks.required must be a list")
    elif not any("check_task_ready.py" in str(item) for item in required_checks):
        report.blockers.append("checks.required must include check_task_ready.py or prose explanation")
    else:
        report.checks_policy = "passed"

    return report


def render_human(report: ValidationReport) -> str:
    lines = [
        "validate_task_contract",
        f"task_id: {report.task_id}",
        f"version: {report.version}",
        f"role: {report.role}",
        f"mode: {report.mode}",
        f"working_branch: {report.working_branch}",
        f"required_fields: {report.required_fields}",
        f"enum_values: {report.enum_values}",
        f"branch_policy: {report.branch_policy}",
        f"scope_policy: {report.scope_policy}",
        f"checks_policy: {report.checks_policy}",
        f"blockers_count: {len(report.blockers)}",
        f"warnings_count: {len(report.warnings)}",
        f"result: {report.result}",
    ]
    if report.blockers:
        lines.append("")
        lines.append("blockers:")
        lines.extend(f"- {item}" for item in report.blockers)
    if report.warnings:
        lines.append("")
        lines.append("warnings:")
        lines.extend(f"- {item}" for item in report.warnings)
    return "\n".join(lines) + "\n"


def build_report(task_file: Path) -> ValidationReport:
    try:
        text = safe_read_text(task_file)
        block = extract_contract_block(text)
        data = parse_yaml_subset(block)
        return validate_contract(data, task_file)
    except (OSError, ContractParseError) as exc:
        return ValidationReport(task_file=str(task_file), blockers=[str(exc)])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate fenced task_contract frontmatter without changing repository state.",
        epilog="Limitations: supports only indentation, nested mappings, string scalars and scalar lists.",
    )
    parser.add_argument("task_file", help="TASK file or Engine block markdown file to validate.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args(argv)

    report = build_report(Path(args.task_file))
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, separators=(",", ":")))
    else:
        print(render_human(report), end="")
    return 0 if report.result == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
