#!/usr/bin/env python3
"""Локальный read-only ready-gate перед push/PR/review-comment."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GENERATED_TRIGGER_PATHS = {
    "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml",
    "docs/agent-system/PROJECT_FILE_MAP.md",
    "docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md",
    "docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md",
    "docs/agent-system/BRANCH_POLICY.md",
    "docs/agent-system/ENGINE_JOURNAL_CONTRACT.md",
    "docs/agent-system/templates/TASK_HEADER_COMMON.md",
    "docs/agent-system/CURRENT_STATE.md",
    "docs/agent-system/NEXT_STEPS.md",
    "docs/agent-system/ENGINE_ENTRYPOINT.md",
    "docs/agent-system/TASK_CONTRACT.md",
    "docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md",
    "docs/agent-system/JOURNAL_FINALIZATION_POLICY.md",
    "docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md",
    "docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md",
    "docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md",
    "docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md",
    "docs/agent-system/LANGUAGE_POLICY.md",
    "docs/agent-system/REVIEW_AUTOLOOP.md",
    "docs/agent-system/TIME_ACCOUNTING_POLICY.md",
    "docs/agent-system/COST_TRACKING_POLICY.md",
    "docs/agent-system/METRICS.md",
    "docs/agent-system/engine-journal/INDEX.md",
}
GENERATED_TRIGGER_PREFIXES = ("docs/agent-system/cloud/",)
FORBIDDEN_SEGMENTS = {"data", "runtime", "dist", "backups", "exports", ".venv"}
SENSITIVE_FILENAME_RE = re.compile(
    r"secret|token|password|passwd|credential|credentials|private_key|id_rsa|authorization|cookie|session|(^|/)\.env",
    re.IGNORECASE,
)
STRICT_SECRET_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"BEGIN RSA PRIVATE KEY", re.IGNORECASE),
    re.compile(r"BEGIN OPENSSH PRIVATE KEY", re.IGNORECASE),
    re.compile(r"PRIVATE KEY", re.IGNORECASE),
    # Заголовок Authorization блокируется независимо от auth-схемы.
    re.compile(r"^\s*Authorization\s*:", re.IGNORECASE),
    re.compile(r"Bearer\s+", re.IGNORECASE),
    re.compile(r"password\s*=", re.IGNORECASE),
    re.compile(r"token\s*=", re.IGNORECASE),
    re.compile(r"secret\s*=", re.IGNORECASE),
    re.compile(r"api_key\s*=", re.IGNORECASE),
)
PLACEHOLDER_PATTERNS = (
    re.compile(r"<TBD>", re.IGNORECASE),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<sha>", re.IGNORECASE),
    re.compile(r"<url>", re.IGNORECASE),
    re.compile(r"<timestamp>", re.IGNORECASE),
    re.compile(r"\bpending\b", re.IGNORECASE),
)
DEFERRED_FINALIZATION_PATTERNS = (
    re.compile(r"\bto\s+be\s+run\s+after\s+final\s+edits\b", re.IGNORECASE),
    re.compile(r"\bpending\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\bwill\s+be\s+recorded\s+later\b", re.IGNORECASE),
    re.compile(r"\bafter\s+PR\s+creation\b", re.IGNORECASE),
    re.compile(r"\bafter\s+push\b", re.IGNORECASE),
    re.compile(r"\bpending\s+final\s+head\b", re.IGNORECASE),
    re.compile(r"\bpending\s+PR\s+URL\b", re.IGNORECASE),
    re.compile(r"\bpending\s+checks\b", re.IGNORECASE),
    re.compile(r"\bplaceholder\b", re.IGNORECASE),
    re.compile(r"\bnot\s+run\s+yet\b", re.IGNORECASE),
    re.compile(r"\bto\s+be\s+updated\b", re.IGNORECASE),
)
SUPERSEDED_TEMPLATE_PATH = "docs/agent-system/templates/SUPERSEDED_BANNER.md"
SUPERSEDED_TAG_RE = re.compile(
    r"<!--\s*SUPERSEDED_BY:\s*(?P<file>[^;<>]+?)\s*;\s*PR:\s*(?P<pr>\d+)\s*;\s*DATE:\s*(?P<date>\d{4}-\d{2}-\d{2})\s*-->",
)
SUPERSEDED_TAG_ANY_RE = re.compile(r"<!--\s*SUPERSEDED_BY\s*:", re.IGNORECASE)
SUPERSEDED_STATUS_RE = re.compile(r"^\s*(?:status|Статус)\s*:\s*`?superseded`?\s*$", re.IGNORECASE)
VISIBLE_SUPERSEDED_RE = re.compile(r"замен[её]н|superseded", re.IGNORECASE)
EXECUTION_STARTED_RE = re.compile(r"^\s*execution_started_at:\s*`?([^`\r\n]+?)`?\s*$", re.MULTILINE)
EXECUTION_FINISHED_RE = re.compile(r"^\s*execution_finished_at:\s*`?([^`\r\n]+?)`?\s*$", re.MULTILINE)
MIN_EXECUTION_DURATION_SECONDS = 60
ACCOUNTING_REQUIRED_RESULT_FIELDS = (
    "execution_started_at",
    "execution_finished_at",
    "execution_duration",
    "time_spent",
    "actor_type",
    "role",
    "time_source",
    "time_report_confidence",
    "human_time_reported",
    "input_tokens",
    "output_tokens",
    "ai_cost_estimate",
    "human_cost_estimate",
    "total_task_cost",
    "resource_cost",
)
ACCOUNTING_ALLOWED_ACTOR_TYPES = {"human", "agent", "hybrid"}
ACCOUNTING_ALLOWED_TIME_SOURCES = {"measured", "reported", "mixed"}
ACCOUNTING_ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ACCOUNTING_EMPTY_VALUES = {"", "none", "null"}
ACCOUNTING_UNKNOWN_VALUES = {"n/a", "na", "not_available", "unavailable", "unknown", "неизвестно", "недоступно"}
ACCOUNTING_NOT_APPLICABLE_VALUES = {"not_applicable", "не применимо"}
ACCOUNTING_PLACEHOLDER_RE = re.compile(r"^<.*>$|pending|tbd|todo|not_created_yet", re.IGNORECASE)
TIME_SPENT_RE = re.compile(
    r"^(?:PT(?=\d)(?:\d+H)?(?:\d+M)?(?:\d+S)?|\d+(?:\.\d+)?\s*(?:h|m|min|hour|hours|ч|мин)(?:\s+\d+(?:\.\d+)?\s*(?:h|m|min|hour|hours|ч|мин))?)$",
    re.IGNORECASE,
)
TOKEN_VALUE_RE = re.compile(r"^\d+$")
MONEY_VALUE_RE = re.compile(r"^(?:[A-Z]{3}\s*)?[$€₽]?\s*(\d+(?:\.\d+)?)$", re.IGNORECASE)
STOP_OR_FAILURE_RE = re.compile(r"\b(stop|failure|failed|blocked|ошибка|стоп)\b", re.IGNORECASE)


@dataclass
class CommandResult:
    name: str
    exit_code: int
    status: str


@dataclass
class ReadyReport:
    repo_root: str = ""
    branch: str = ""
    base: str = ""
    release_boundary_mode: bool = False
    commit_message_cutoff_ref: str = ""
    changed_files: list[str] = field(default_factory=list)
    staged_files: list[str] = field(default_factory=list)
    unstaged_files: list[str] = field(default_factory=list)
    untracked_files: list[str] = field(default_factory=list)
    diff_checks: list[CommandResult] = field(default_factory=list)
    commit_message_checks: list[CommandResult] = field(default_factory=list)
    id_reference_checks: list[CommandResult] = field(default_factory=list)
    generated_checks_required: bool = False
    generated_checks_reason: str = ""
    generated_checks: list[CommandResult] = field(default_factory=list)
    generated_eol_guard_result: str = "skipped"
    generated_eol_guard_reason: str = ""
    forbidden_changed_paths: list[str] = field(default_factory=list)
    sensitive_filenames: list[str] = field(default_factory=list)
    strict_added_line_secret_files: list[str] = field(default_factory=list)
    placeholder_candidates: list[str] = field(default_factory=list)
    deferred_finalization_placeholders: list[str] = field(default_factory=list)
    superseded_banner_warnings: list[str] = field(default_factory=list)
    execution_timing_warnings: list[str] = field(default_factory=list)
    accounting_required_result_files: list[str] = field(default_factory=list)
    accounting_legacy_advisory_files: list[str] = field(default_factory=list)
    accounting_field_blockers: list[str] = field(default_factory=list)
    accounting_field_warnings: list[str] = field(default_factory=list)
    cost_calculator_summary: dict[str, object] = field(default_factory=dict)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "ready" if not self.blockers else "blocked"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["diff_checks"] = [asdict(item) for item in self.diff_checks]
        data["commit_message_checks"] = [asdict(item) for item in self.commit_message_checks]
        data["id_reference_checks"] = [asdict(item) for item in self.id_reference_checks]
        data["generated_checks"] = [asdict(item) for item in self.generated_checks]
        data["changed_files_count"] = len(self.changed_files)
        data["staged_files_count"] = len(self.staged_files)
        data["unstaged_files_count"] = len(self.unstaged_files)
        data["untracked_files_count"] = len(self.untracked_files)
        data["forbidden_changed_paths_count"] = len(self.forbidden_changed_paths)
        data["sensitive_filenames_count"] = len(self.sensitive_filenames)
        data["strict_added_line_secret_value_count"] = len(self.strict_added_line_secret_files)
        data["placeholder_candidates_count"] = len(self.placeholder_candidates)
        data["deferred_finalization_placeholder_count"] = len(self.deferred_finalization_placeholders)
        data["superseded_banner_warnings_count"] = len(self.superseded_banner_warnings)
        data["execution_timing_warnings_count"] = len(self.execution_timing_warnings)
        data["accounting_required_result_files_count"] = len(self.accounting_required_result_files)
        data["accounting_legacy_advisory_files_count"] = len(self.accounting_legacy_advisory_files)
        data["accounting_field_blockers_count"] = len(self.accounting_field_blockers)
        data["accounting_field_warnings_count"] = len(self.accounting_field_warnings)
        data["blockers_count"] = len(self.blockers)
        data["warnings_count"] = len(self.warnings)
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


def run_command(args: list[str], name: str) -> CommandResult:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return CommandResult(name=name, exit_code=result.returncode, status="passed" if result.returncode == 0 else "failed")


def run_json_command(args: list[str], name: str) -> tuple[CommandResult, dict[str, object] | None]:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        return CommandResult(name=name, exit_code=result.returncode, status="failed"), None
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return CommandResult(name=name, exit_code=1, status="failed"), None
    status = str(data.get("result", "passed"))
    return CommandResult(name=name, exit_code=result.returncode, status=status), data


def split_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def git_lines(args: list[str], report: ReadyReport, blocker: str) -> list[str]:
    result = run_git(args)
    if result.returncode != 0:
        report.blockers.append(blocker)
        return []
    return split_lines(result.stdout)


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def unique_sorted(paths: list[str]) -> list[str]:
    return sorted({normalize_path(path) for path in paths if path.strip()})


def is_forbidden_path(path: str) -> bool:
    normalized = normalize_path(path)
    name = Path(normalized).name
    if name == ".env" or name.startswith(".env."):
        return True
    return any(part in FORBIDDEN_SEGMENTS for part in normalized.split("/"))


def requires_generated_checks(paths: list[str]) -> bool:
    for path in paths:
        normalized = normalize_path(path)
        if normalized in GENERATED_TRIGGER_PATHS:
            return True
        if normalized.startswith(GENERATED_TRIGGER_PREFIXES):
            return True
    return False


def is_task_result_file(path: str) -> bool:
    normalized = normalize_path(path)
    return re.fullmatch(r"docs/agent-system/engine-journal/(input/TASK|output/RESULT)-.*\.md", normalized) is not None


def task_result_files(paths: list[str]) -> list[str]:
    return [normalize_path(path) for path in paths if is_task_result_file(path)]


def scan_secret_patterns_in_added_lines(diff_text: str) -> set[str]:
    current_file = ""
    flagged: set[str] = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = normalize_path(line[6:])
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if current_file == "docs/agent-system/tools/check_task_ready.py" and "re.compile(" in line:
            continue
        if any(pattern.search(line[1:]) for pattern in STRICT_SECRET_PATTERNS):
            flagged.add(current_file or "<unknown>")
    return flagged


def scan_added_secret_values(base: str) -> list[str]:
    commands = [
        ["diff", "--unified=0", f"{base}...HEAD"],
        ["diff", "--unified=0"],
        ["diff", "--cached", "--unified=0"],
    ]
    flagged: set[str] = set()
    for command in commands:
        result = run_git(command)
        if result.returncode != 0:
            return ["<diff-command-failed>"]
        flagged.update(scan_secret_patterns_in_added_lines(result.stdout))
    return sorted(flagged)


def scan_placeholders(paths: list[str]) -> list[str]:
    flagged: list[str] = []
    for path in task_result_files(paths):
        full_path = ROOT / path
        if not full_path.is_file():
            continue
        text = full_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            stripped = line.strip()
            # Строки ниже описывают саму validation-схему, а не незаполненные значения.
            if "placeholder" in stripped.lower() and any(token in stripped for token in ("<sha>", "<url>", "<timestamp>", "<TBD>")):
                continue
            if "closure pending" in stripped:
                continue
            if any(pattern.search(stripped) for pattern in PLACEHOLDER_PATTERNS):
                flagged.append(path)
                break
    return sorted(set(flagged))


def scan_deferred_finalization_placeholders(paths: list[str]) -> list[str]:
    flagged: list[str] = []
    for path in task_result_files(paths):
        full_path = ROOT / path
        if not full_path.is_file():
            continue
        text = full_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            stripped = line.strip()
            if any(pattern.search(stripped) for pattern in DEFERRED_FINALIZATION_PATTERNS):
                flagged.append(path)
                break
    return sorted(set(flagged))


def validate_superseded_banner_text(path: str, text: str) -> list[str]:
    normalized = normalize_path(path)
    if normalized == SUPERSEDED_TEMPLATE_PATH:
        return []

    lines = text.splitlines()
    visible_source_lines: list[tuple[int, str]] = []
    in_fence = False
    for line_number, line in enumerate(lines, start=1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            visible_source_lines.append((line_number, line))

    tag_lines: list[int] = []
    full_matches: list[re.Match[str]] = []
    warnings: list[str] = []
    for line_number, line in visible_source_lines:
        if SUPERSEDED_TAG_ANY_RE.search(line):
            tag_lines.append(line_number)
        full_matches.extend(SUPERSEDED_TAG_RE.finditer(line))

    has_superseded_status = any(SUPERSEDED_STATUS_RE.search(line) for _, line in visible_source_lines)
    if not tag_lines and not has_superseded_status:
        return []

    if tag_lines and not full_matches:
        return [f"{normalized}:{tag_lines[0]}: SUPERSEDED_TAG_INVALID"]
    if has_superseded_status and not full_matches:
        return [f"{normalized}:1: SUPERSEDED_TAG_MISSING"]

    for match in full_matches:
        try:
            date.fromisoformat(match.group("date"))
        except ValueError:
            warnings.append(f"{normalized}:1: SUPERSEDED_DATE_INVALID")

    visible_lines = [line for _, line in visible_source_lines if not line.strip().startswith("<!--")]
    if not any(VISIBLE_SUPERSEDED_RE.search(line) for line in visible_lines):
        warnings.append(f"{normalized}:1: SUPERSEDED_VISIBLE_LINE_MISSING")
    return warnings


def scan_superseded_banners(paths: list[str]) -> list[str]:
    warnings: list[str] = []
    for path in unique_sorted(paths):
        normalized = normalize_path(path)
        if is_task_result_file(normalized):
            continue
        if not normalized.endswith(".md"):
            continue
        full_path = ROOT / normalized
        if not full_path.is_file():
            continue
        text = full_path.read_text(encoding="utf-8", errors="replace")
        warnings.extend(validate_superseded_banner_text(normalized, text))
    return sorted(set(warnings))


def is_generated_or_journal_path(path: str) -> bool:
    normalized = normalize_path(path)
    if normalized.startswith("docs/agent-system/cloud/"):
        return True
    if normalized.startswith("docs/agent-system/engine-journal/"):
        return True
    return normalized == "docs/agent-system/PROJECT_FILE_MAP.md"


def has_substantive_changes(paths: list[str]) -> bool:
    return any(not is_generated_or_journal_path(path) for path in unique_sorted(paths))


def parse_execution_timestamp(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    return datetime.fromisoformat(normalized)


def validate_execution_timing_text(path: str, text: str, substantive_changes: bool) -> list[str]:
    normalized = normalize_path(path)
    if not substantive_changes:
        return []
    if not re.fullmatch(r"docs/agent-system/engine-journal/output/RESULT-.*\.md", normalized):
        return []

    started_match = EXECUTION_STARTED_RE.search(text)
    finished_match = EXECUTION_FINISHED_RE.search(text)
    if not started_match or not finished_match:
        return []

    try:
        started_at = parse_execution_timestamp(started_match.group(1))
        finished_at = parse_execution_timestamp(finished_match.group(1))
    except ValueError:
        return [f"{normalized}:1: EXECUTION_TIMING_UNPARSEABLE"]

    duration_seconds = (finished_at - started_at).total_seconds()
    if duration_seconds < MIN_EXECUTION_DURATION_SECONDS:
        rounded = int(duration_seconds)
        return [f"{normalized}:1: UNRELIABLE_EXECUTION_TIMING duration_seconds={rounded}"]
    return []


def scan_execution_timing(paths: list[str]) -> list[str]:
    all_paths = unique_sorted(paths)
    substantive_changes = has_substantive_changes(all_paths)
    warnings: list[str] = []
    for path in task_result_files(all_paths):
        normalized = normalize_path(path)
        if not normalized.startswith("docs/agent-system/engine-journal/output/RESULT-"):
            continue
        full_path = ROOT / normalized
        if not full_path.is_file():
            continue
        text = full_path.read_text(encoding="utf-8", errors="replace")
        warnings.extend(validate_execution_timing_text(normalized, text, substantive_changes))
    return sorted(set(warnings))


def diff_name_status(base: str) -> dict[str, str]:
    result = run_git(["diff", "--name-status", f"{base}...HEAD"])
    if result.returncode != 0:
        return {}
    statuses: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        path = parts[-1]
        statuses[normalize_path(path)] = status
    return statuses


def is_result_file(path: str) -> bool:
    normalized = normalize_path(path)
    return re.fullmatch(r"docs/agent-system/engine-journal/output/RESULT-.*\.md", normalized) is not None


def extract_simple_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", key):
            continue
        fields[key] = value.strip().strip("`").strip()
    return fields


def is_missing_accounting_value(value: str) -> bool:
    normalized = value.strip().strip("`").strip()
    if ACCOUNTING_PLACEHOLDER_RE.search(normalized):
        return True
    return normalized.lower() in ACCOUNTING_EMPTY_VALUES


def parse_money(value: str) -> float | None:
    normalized = value.strip().strip("`").strip()
    lowered = normalized.lower()
    if lowered in ACCOUNTING_EMPTY_VALUES or lowered in ACCOUNTING_UNKNOWN_VALUES or lowered in ACCOUNTING_NOT_APPLICABLE_VALUES:
        return None
    match = MONEY_VALUE_RE.fullmatch(normalized)
    if not match:
        return None
    return float(match.group(1))


def parse_token_count(value: str) -> int | None:
    normalized = value.strip().strip("`").strip()
    lowered = normalized.lower()
    if lowered in ACCOUNTING_EMPTY_VALUES or lowered in ACCOUNTING_UNKNOWN_VALUES or lowered in ACCOUNTING_NOT_APPLICABLE_VALUES:
        return None
    if not TOKEN_VALUE_RE.fullmatch(normalized):
        return None
    return int(normalized)


def has_stop_or_failure_state(fields: dict[str, str]) -> bool:
    haystack = " ".join(
        fields.get(name, "")
        for name in ("status", "terminal_state", "Closure blockers", "blockers")
    )
    return bool(STOP_OR_FAILURE_RE.search(haystack))


def validate_accounting_fields(path: str, text: str, hard: bool) -> tuple[list[str], list[str], dict[str, float | int]]:
    fields = extract_simple_fields(text)
    normalized = normalize_path(path)
    blockers: list[str] = []
    warnings: list[str] = []
    metrics: dict[str, float | int] = {}

    missing = [
        field
        for field in ACCOUNTING_REQUIRED_RESULT_FIELDS
        if field not in fields or is_missing_accounting_value(fields[field])
    ]
    if missing:
        target = blockers if hard else warnings
        target.append(f"{normalized}:1: ACCOUNTING_FIELDS_MISSING {','.join(missing)}")

    actor_type = fields.get("actor_type", "").strip().lower()
    if actor_type and actor_type not in ACCOUNTING_ALLOWED_ACTOR_TYPES:
        (blockers if hard else warnings).append(f"{normalized}:1: ACCOUNTING_ACTOR_TYPE_INVALID {actor_type}")

    time_source = fields.get("time_source", "").strip().lower()
    if time_source and time_source not in ACCOUNTING_ALLOWED_TIME_SOURCES:
        (blockers if hard else warnings).append(f"{normalized}:1: ACCOUNTING_TIME_SOURCE_INVALID {time_source}")

    confidence = fields.get("time_report_confidence", "").strip().lower()
    if confidence and confidence not in ACCOUNTING_ALLOWED_CONFIDENCE:
        (blockers if hard else warnings).append(f"{normalized}:1: ACCOUNTING_CONFIDENCE_INVALID {confidence}")

    time_spent = fields.get("time_spent", "").strip()
    if time_spent and not TIME_SPENT_RE.fullmatch(time_spent):
        (blockers if hard else warnings).append(f"{normalized}:1: ACCOUNTING_TIME_SPENT_FORMAT_INVALID {time_spent}")

    human_time = fields.get("human_time_reported", "").strip()
    human_time_missing = (
        not human_time
        or is_missing_accounting_value(human_time)
        or human_time.lower() in ACCOUNTING_NOT_APPLICABLE_VALUES
        or human_time.lower() in ACCOUNTING_UNKNOWN_VALUES
    )
    if actor_type in {"human", "hybrid"} and human_time_missing:
        if has_stop_or_failure_state(fields) and fields.get("time_report_missing_reason"):
            warnings.append(f"{normalized}:1: ACCOUNTING_HUMAN_TIME_MISSING_WITH_REASON")
        else:
            (blockers if hard else warnings).append(f"{normalized}:1: ACCOUNTING_HUMAN_TIME_REQUIRED")

    for token_field in ("input_tokens", "output_tokens"):
        value = fields.get(token_field, "")
        if value and parse_token_count(value) is None:
            lowered = value.lower()
            if lowered not in ACCOUNTING_EMPTY_VALUES and lowered not in ACCOUNTING_UNKNOWN_VALUES and lowered not in ACCOUNTING_NOT_APPLICABLE_VALUES:
                (blockers if hard else warnings).append(f"{normalized}:1: ACCOUNTING_TOKEN_VALUE_INVALID {token_field}")

    input_tokens = parse_token_count(fields.get("input_tokens", ""))
    output_tokens = parse_token_count(fields.get("output_tokens", ""))
    ai_cost = parse_money(fields.get("ai_cost_estimate", ""))
    human_cost = parse_money(fields.get("human_cost_estimate", ""))
    total_cost = parse_money(fields.get("total_task_cost", ""))

    if input_tokens is not None:
        metrics["input_tokens"] = input_tokens
    if output_tokens is not None:
        metrics["output_tokens"] = output_tokens
    if ai_cost is not None:
        metrics["ai_cost_estimate"] = ai_cost
    if human_cost is not None:
        metrics["human_cost_estimate"] = human_cost
    if total_cost is not None:
        metrics["total_task_cost"] = total_cost

    # Если числовые cost-поля заполнены, проверяем арифметику на уровне RESULT.
    if ai_cost is not None and human_cost is not None and total_cost is not None:
        expected_total = ai_cost + human_cost
        if abs(expected_total - total_cost) > 0.01:
            (blockers if hard else warnings).append(
                f"{normalized}:1: ACCOUNTING_TOTAL_COST_MISMATCH expected={expected_total:.2f} actual={total_cost:.2f}"
            )

    return blockers, warnings, metrics


def scan_accounting_fields(paths: list[str], base: str) -> tuple[list[str], list[str], list[str], list[str], dict[str, object]]:
    all_paths = unique_sorted(paths)
    statuses = diff_name_status(base)
    untracked_results = {
        normalize_path(path)
        for path in git_lines(["ls-files", "--others", "--exclude-standard"], ReadyReport(), "cannot list untracked files")
        if is_result_file(path)
    }
    new_result_files: list[str] = []
    legacy_advisory_files: list[str] = []
    blockers: list[str] = []
    warnings: list[str] = []
    totals: dict[str, float | int] = {
        "input_tokens": 0,
        "output_tokens": 0,
        "ai_cost_estimate": 0.0,
        "human_cost_estimate": 0.0,
        "total_task_cost": 0.0,
    }
    numeric_files_count = 0

    for path in all_paths:
        normalized = normalize_path(path)
        if not is_result_file(normalized):
            continue
        full_path = ROOT / normalized
        if not full_path.is_file():
            continue
        is_new = statuses.get(normalized, "").startswith("A") or normalized in untracked_results
        if is_new:
            new_result_files.append(normalized)
        else:
            legacy_advisory_files.append(normalized)
        text = full_path.read_text(encoding="utf-8", errors="replace")
        file_blockers, file_warnings, metrics = validate_accounting_fields(normalized, text, hard=is_new)
        blockers.extend(file_blockers)
        warnings.extend(file_warnings)
        if metrics:
            numeric_files_count += 1
        for key, value in metrics.items():
            totals[key] += value

    summary: dict[str, object] = {
        "numeric_files_count": numeric_files_count,
        "input_tokens": int(totals["input_tokens"]),
        "output_tokens": int(totals["output_tokens"]),
        "ai_cost_estimate": round(float(totals["ai_cost_estimate"]), 4),
        "human_cost_estimate": round(float(totals["human_cost_estimate"]), 4),
        "total_task_cost": round(float(totals["total_task_cost"]), 4),
    }
    return sorted(new_result_files), sorted(legacy_advisory_files), sorted(set(blockers)), sorted(set(warnings)), summary


def add_repository_guard(report: ReadyReport) -> None:
    root_result = run_git(["rev-parse", "--show-toplevel"])
    if root_result.returncode != 0:
        report.blockers.append("not a git repository")
        return
    report.repo_root = normalize_path(root_result.stdout.strip())

    branch_result = run_git(["branch", "--show-current"])
    if branch_result.returncode != 0:
        report.blockers.append("cannot determine current branch")
        return
    report.branch = branch_result.stdout.strip()

    remote_result = run_git(["remote", "-v"])
    if remote_result.returncode != 0 or "github.com/MaximKolomeets/agent-system-development" not in remote_result.stdout:
        report.blockers.append("unexpected or missing origin remote")

    status_result = run_git(["status", "--short"])
    if status_result.returncode != 0:
        report.blockers.append("cannot read git status")


def add_changed_files(report: ReadyReport) -> None:
    report.changed_files = unique_sorted(git_lines(["diff", "--name-only", f"{report.base}...HEAD"], report, "cannot compute base diff"))
    report.unstaged_files = unique_sorted(git_lines(["diff", "--name-only"], report, "cannot compute unstaged diff"))
    report.staged_files = unique_sorted(git_lines(["diff", "--cached", "--name-only"], report, "cannot compute staged diff"))
    report.untracked_files = unique_sorted(git_lines(["ls-files", "--others", "--exclude-standard"], report, "cannot list untracked files"))

    has_changes = any((report.changed_files, report.unstaged_files, report.staged_files, report.untracked_files))
    if has_changes and report.branch in {"main", "developer"} and not report.release_boundary_mode:
        report.blockers.append("changed files on protected branch")
    if has_changes and not report.branch.startswith("work/") and not report.release_boundary_mode:
        report.blockers.append("changed files outside work/* branch")


def add_diff_checks(report: ReadyReport) -> None:
    commands = [(["git", "diff", "--check", f"{report.base}...HEAD"], f"git diff --check {report.base}...HEAD")]
    if report.unstaged_files:
        commands.append((["git", "diff", "--check"], "git diff --check"))
    if report.staged_files:
        commands.append((["git", "diff", "--cached", "--check"], "git diff --cached --check"))

    for args, name in commands:
        check = run_command(args, name)
        report.diff_checks.append(check)
        if check.exit_code != 0:
            report.blockers.append(f"{name} failed")


def add_commit_message_checks(report: ReadyReport, cutoff_ref: str = "") -> None:
    report.commit_message_cutoff_ref = cutoff_ref
    if report.release_boundary_mode and not cutoff_ref:
        report.commit_message_checks.append(
            CommandResult(
                name="validate_commit_message.py skipped for release boundary",
                exit_code=0,
                status="skipped_release_boundary",
            )
        )
        return

    args = ["python", "docs/agent-system/tools/validate_commit_message.py", "--base", report.base]
    name = f"validate_commit_message.py --base {report.base}"
    if cutoff_ref:
        args.extend(["--cutoff-ref", cutoff_ref])
        name = f"{name} --cutoff-ref {cutoff_ref}"
    check = run_command(args, name)
    report.commit_message_checks.append(check)
    if check.exit_code != 0:
        report.blockers.append("validate_commit_message.py failed")


def add_generated_checks(report: ReadyReport) -> None:
    all_paths = unique_sorted(report.changed_files + report.unstaged_files + report.staged_files + report.untracked_files)
    report.generated_checks_required = requires_generated_checks(all_paths)
    if not report.generated_checks_required:
        report.generated_checks_reason = "no generated/bundle-source files changed"
        report.generated_eol_guard_reason = "no generated files changed"
        return
    report.generated_checks_reason = "generated/bundle-source files changed"
    checks = [
        (["python", "docs/agent-system/tools/gen_file_map.py", "--check"], "gen_file_map.py --check"),
        (["python", "docs/agent-system/tools/gen_cloud_bundle.py", "--check"], "gen_cloud_bundle.py --check"),
    ]
    for args, name in checks:
        check = run_command(args, name)
        report.generated_checks.append(check)
        if check.exit_code != 0:
            report.blockers.append(f"{name} failed")

    guard_check, guard_data = run_json_command(
        ["python", "docs/agent-system/tools/generated_eol_guard.py", "--base", report.base, "--json"],
        "generated_eol_guard.py --json",
    )
    report.generated_checks.append(guard_check)
    report.generated_eol_guard_result = guard_check.status
    report.generated_eol_guard_reason = "generated/cloud changes classified"
    if guard_check.exit_code != 0 or guard_check.status == "blocked":
        report.blockers.append("generated_eol_guard.py failed")
    elif guard_check.status == "warning":
        report.warnings.append("generated_eol_guard.py detected generated EOL/whitespace-only noise")
    if guard_data is None:
        report.generated_eol_guard_reason = "generated_eol_guard JSON summary unavailable"


def add_id_reference_checks(report: ReadyReport) -> None:
    check = run_command(
        ["python", "docs/agent-system/tools/validate_id_references.py"],
        "validate_id_references.py",
    )
    report.id_reference_checks.append(check)
    if check.exit_code != 0:
        report.blockers.append("validate_id_references.py failed")


def add_safety_scans(report: ReadyReport) -> None:
    all_paths = unique_sorted(report.changed_files + report.unstaged_files + report.staged_files + report.untracked_files)
    report.forbidden_changed_paths = [path for path in all_paths if is_forbidden_path(path)]
    if report.forbidden_changed_paths:
        report.blockers.append("forbidden changed paths detected")

    # TASK/RESULT filenames include task ids; their contents stay covered by strict added-line scan.
    report.sensitive_filenames = [path for path in all_paths if not is_task_result_file(path) and SENSITIVE_FILENAME_RE.search(path)]
    if report.sensitive_filenames:
        report.blockers.append("sensitive filenames detected")

    report.strict_added_line_secret_files = scan_added_secret_values(report.base)
    if report.strict_added_line_secret_files:
        report.blockers.append("strict added-line secret value scan detected high-risk pattern")

    report.placeholder_candidates = scan_placeholders(all_paths)
    hard_placeholders = [path for path in report.placeholder_candidates if "<" in (ROOT / path).read_text(encoding="utf-8", errors="replace")]
    if hard_placeholders:
        report.blockers.append("unresolved angle-bracket placeholders detected in changed TASK/RESULT")
    elif report.placeholder_candidates:
        report.warnings.append("placeholder candidates detected in changed TASK/RESULT")

    report.deferred_finalization_placeholders = scan_deferred_finalization_placeholders(all_paths)
    if report.deferred_finalization_placeholders:
        report.blockers.append("deferred finalization placeholders detected in changed TASK/RESULT")

    report.superseded_banner_warnings = scan_superseded_banners(all_paths)
    if report.superseded_banner_warnings:
        report.warnings.append("superseded banner advisory warnings detected")

    report.execution_timing_warnings = scan_execution_timing(all_paths)
    if report.execution_timing_warnings:
        report.warnings.append("unreliable execution timing advisory warnings detected")

    (
        report.accounting_required_result_files,
        report.accounting_legacy_advisory_files,
        report.accounting_field_blockers,
        report.accounting_field_warnings,
        report.cost_calculator_summary,
    ) = scan_accounting_fields(all_paths, report.base)
    if report.accounting_field_blockers:
        report.blockers.append("required accounting fields missing or invalid in new RESULT")
    if report.accounting_field_warnings:
        report.warnings.append("accounting advisory warnings detected")


def render_human(report: ReadyReport) -> str:
    lines = [
        "check_task_ready",
        "",
        f"repo_root: {report.repo_root}",
        f"branch: {report.branch}",
        f"base: {report.base}",
        f"release_boundary_mode: {str(report.release_boundary_mode).lower()}",
        f"commit_message_cutoff_ref: {report.commit_message_cutoff_ref or '<none>'}",
        "",
        f"changed_files_count: {len(report.changed_files)}",
        f"staged_files_count: {len(report.staged_files)}",
        f"unstaged_files_count: {len(report.unstaged_files)}",
        f"untracked_files_count: {len(report.untracked_files)}",
        "",
        "changed_files:",
    ]
    lines.extend(f"- {path}" for path in report.changed_files)
    if not report.changed_files:
        lines.append("- <none>")
    lines.append("")
    for check in report.diff_checks:
        lines.append(f"{check.name}: {check.status}")
    for check in report.commit_message_checks:
        lines.append(f"{check.name}: {check.status}")
    for check in report.id_reference_checks:
        lines.append(f"{check.name}: {check.status}")
    lines.extend(
        [
            "",
            f"generated_checks_required: {'yes' if report.generated_checks_required else 'no'}",
            f"generated_checks_reason: {report.generated_checks_reason}",
            f"generated_eol_guard_result: {report.generated_eol_guard_result}",
            f"generated_eol_guard_reason: {report.generated_eol_guard_reason}",
        ]
    )
    for check in report.generated_checks:
        lines.append(f"{check.name}: {check.status}")
    lines.extend(
        [
            "",
            f"forbidden_changed_paths_count: {len(report.forbidden_changed_paths)}",
            f"sensitive_filenames_count: {len(report.sensitive_filenames)}",
            f"strict_added_line_secret_value_count: {len(report.strict_added_line_secret_files)}",
            f"placeholder_candidates_count: {len(report.placeholder_candidates)}",
            f"deferred_finalization_placeholder_count: {len(report.deferred_finalization_placeholders)}",
            f"superseded_banner_warnings_count: {len(report.superseded_banner_warnings)}",
            f"execution_timing_warnings_count: {len(report.execution_timing_warnings)}",
            f"accounting_required_result_files_count: {len(report.accounting_required_result_files)}",
            f"accounting_legacy_advisory_files_count: {len(report.accounting_legacy_advisory_files)}",
            f"accounting_field_blockers_count: {len(report.accounting_field_blockers)}",
            f"accounting_field_warnings_count: {len(report.accounting_field_warnings)}",
            f"cost_calculator_summary: {json.dumps(report.cost_calculator_summary, ensure_ascii=False, sort_keys=True)}",
            "",
            f"blockers_count: {len(report.blockers)}",
            f"warnings_count: {len(report.warnings)}",
            f"result: {report.result}",
        ]
    )
    if report.blockers:
        lines.append("")
        lines.append("blockers:")
        lines.extend(f"- {item}" for item in report.blockers)
    if report.warnings:
        lines.append("")
        lines.append("warnings:")
        lines.extend(f"- {item}" for item in report.warnings)
    if report.deferred_finalization_placeholders:
        lines.append("")
        lines.append("deferred_finalization_placeholder_files:")
        lines.extend(f"- {path}" for path in report.deferred_finalization_placeholders)
    if report.superseded_banner_warnings:
        lines.append("")
        lines.append("superseded_banner_warnings:")
        lines.extend(f"- {item}" for item in report.superseded_banner_warnings)
    if report.execution_timing_warnings:
        lines.append("")
        lines.append("execution_timing_warnings:")
        lines.extend(f"- {item}" for item in report.execution_timing_warnings)
    if report.accounting_field_blockers:
        lines.append("")
        lines.append("accounting_field_blockers:")
        lines.extend(f"- {item}" for item in report.accounting_field_blockers)
    if report.accounting_field_warnings:
        lines.append("")
        lines.append("accounting_field_warnings:")
        lines.extend(f"- {item}" for item in report.accounting_field_warnings)
    return "\n".join(lines) + "\n"


def build_report(
    base: str,
    release_boundary: bool = False,
    commit_message_cutoff_ref: str = "",
) -> ReadyReport:
    report = ReadyReport(base=base)
    add_repository_guard(report)
    if not report.repo_root:
        return report
    if release_boundary:
        if report.branch == "developer" and base == "origin/main":
            report.release_boundary_mode = True
        else:
            report.blockers.append("release boundary mode supports only developer -> origin/main")
    add_changed_files(report)
    add_diff_checks(report)
    add_commit_message_checks(report, commit_message_cutoff_ref)
    add_id_reference_checks(report)
    add_generated_checks(report)
    add_safety_scans(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only task ready gate for agent-system methodology work.",
        epilog="For task-level contract validation, run: python docs/agent-system/tools/validate_task_contract.py <task-file>",
    )
    parser.add_argument("--base", default="origin/developer", help="Diff base ref for committed changes.")
    parser.add_argument(
        "--release-boundary",
        action="store_true",
        help="Allow the developer -> origin/main release gate to run without work-branch blockers.",
    )
    parser.add_argument(
        "--commit-message-cutoff-ref",
        default="",
        help="When release-boundary commit metadata validation is desired, validate only commits after this ref.",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as non-ready.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args(argv)

    report = build_report(
        args.base,
        release_boundary=args.release_boundary,
        commit_message_cutoff_ref=args.commit_message_cutoff_ref,
    )
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")

    if report.blockers or (args.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
