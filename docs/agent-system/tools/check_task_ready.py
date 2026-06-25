#!/usr/bin/env python3
"""Локальный read-only ready-gate перед push/PR/review-comment."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GENERATED_TRIGGER_PATHS = {
    "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml",
    "docs/agent-system/PROJECT_FILE_MAP.md",
    "docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md",
    "docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md",
    "docs/agent-system/BRANCH_POLICY.md",
    "docs/agent-system/ENGINE_JOURNAL_CONTRACT.md",
    "docs/agent-system/CURRENT_STATE.md",
    "docs/agent-system/NEXT_STEPS.md",
    "docs/agent-system/ENGINE_ENTRYPOINT.md",
    "docs/agent-system/REVIEW_AUTOLOOP.md",
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
    re.compile(r"Authorization:", re.IGNORECASE),
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
    changed_files: list[str] = field(default_factory=list)
    staged_files: list[str] = field(default_factory=list)
    unstaged_files: list[str] = field(default_factory=list)
    untracked_files: list[str] = field(default_factory=list)
    diff_checks: list[CommandResult] = field(default_factory=list)
    generated_checks_required: bool = False
    generated_checks_reason: str = ""
    generated_checks: list[CommandResult] = field(default_factory=list)
    generated_eol_guard_result: str = "skipped"
    generated_eol_guard_reason: str = ""
    forbidden_changed_paths: list[str] = field(default_factory=list)
    sensitive_filenames: list[str] = field(default_factory=list)
    strict_added_line_secret_files: list[str] = field(default_factory=list)
    placeholder_candidates: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "ready" if not self.blockers else "blocked"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["diff_checks"] = [asdict(item) for item in self.diff_checks]
        data["generated_checks"] = [asdict(item) for item in self.generated_checks]
        data["changed_files_count"] = len(self.changed_files)
        data["staged_files_count"] = len(self.staged_files)
        data["unstaged_files_count"] = len(self.unstaged_files)
        data["untracked_files_count"] = len(self.untracked_files)
        data["forbidden_changed_paths_count"] = len(self.forbidden_changed_paths)
        data["sensitive_filenames_count"] = len(self.sensitive_filenames)
        data["strict_added_line_secret_value_count"] = len(self.strict_added_line_secret_files)
        data["placeholder_candidates_count"] = len(self.placeholder_candidates)
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


def task_result_files(paths: list[str]) -> list[str]:
    result: list[str] = []
    for path in paths:
        normalized = normalize_path(path)
        if re.fullmatch(r"docs/agent-system/engine-journal/(input/TASK|output/RESULT)-.*\.md", normalized):
            result.append(normalized)
    return result


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
    if has_changes and report.branch in {"main", "developer"}:
        report.blockers.append("changed files on protected branch")
    if has_changes and not report.branch.startswith("work/"):
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


def add_safety_scans(report: ReadyReport) -> None:
    all_paths = unique_sorted(report.changed_files + report.unstaged_files + report.staged_files + report.untracked_files)
    report.forbidden_changed_paths = [path for path in all_paths if is_forbidden_path(path)]
    if report.forbidden_changed_paths:
        report.blockers.append("forbidden changed paths detected")

    report.sensitive_filenames = [path for path in all_paths if SENSITIVE_FILENAME_RE.search(path)]
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


def render_human(report: ReadyReport) -> str:
    lines = [
        "check_task_ready",
        "",
        f"repo_root: {report.repo_root}",
        f"branch: {report.branch}",
        f"base: {report.base}",
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
    return "\n".join(lines) + "\n"


def build_report(base: str) -> ReadyReport:
    report = ReadyReport(base=base)
    add_repository_guard(report)
    if not report.repo_root:
        return report
    add_changed_files(report)
    add_diff_checks(report)
    add_generated_checks(report)
    add_safety_scans(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only task ready gate for agent-system methodology work.",
        epilog="For task-level contract validation, run: python docs/agent-system/tools/validate_task_contract.py <task-file>",
    )
    parser.add_argument("--base", default="origin/developer", help="Diff base ref for committed changes.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as non-ready.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary.")
    args = parser.parse_args(argv)

    report = build_report(args.base)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")

    if report.blockers or (args.strict and report.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
