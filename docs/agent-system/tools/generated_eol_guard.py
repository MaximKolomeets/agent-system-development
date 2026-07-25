#!/usr/bin/env python3
"""Read-only guard: отличает content drift от EOL/whitespace шума."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GENERATED_PREFIXES = ("docs/agent-system/cloud/",)
GENERATED_EXACT = {"docs/agent-system/PROJECT_FILE_MAP.md"}
SOURCE_EXACT = {
    "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml",
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
TEXT_PREFIXES = (
    "docs/agent-system/engine-journal/",
    "docs/agent-system/templates/",
    "docs/agent-system/tools/",
)
TEXT_SUFFIXES = (".md", ".yml", ".yaml", ".py")
SENSITIVE_FILENAME_RE = re.compile(
    r"secret|token|password|passwd|credential|credentials|private_key|id_rsa|authorization|cookie|session|(^|/)\.env",
    re.IGNORECASE,
)


@dataclass
class FileResult:
    path: str
    scope: str
    status: str
    category: str
    reason: str = ""
    matching_source: str = ""
    suspicious_generated_drift: bool = False


@dataclass
class GuardReport:
    base: str
    changed_files: list[str] = field(default_factory=list)
    files: list[FileResult] = field(default_factory=list)
    generated_files: dict[str, list[str]] = field(default_factory=dict)
    suspicious_generated_content_drift: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        if self.blockers:
            return "blocked"
        if self.warnings:
            return "warning"
        return "passed"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["files"] = [asdict(item) for item in self.files]
        data["changed_files_count"] = len(self.changed_files)
        data["content_changed_count"] = count_category(self.files, "content_changed")
        data["eol_only_changed_count"] = count_category(self.files, "eol_only_changed")
        data["whitespace_only_changed_count"] = count_category(self.files, "whitespace_only_changed")
        data["binary_or_unreadable_count"] = count_category(self.files, "binary_or_unreadable")
        data["not_checked_count"] = count_category(self.files, "not_checked")
        data["blockers_count"] = len(self.blockers)
        data["warnings_count"] = len(self.warnings)
        data["result"] = self.result
        return data


@dataclass
class ScopeMetadata:
    """Пакетные Git-метаданные одного diff scope, чтобы не запускать Git для каждого пути."""

    exact_numstat: dict[str, tuple[str, str]] = field(default_factory=dict)
    ignore_space_numstat: dict[str, tuple[str, str]] = field(default_factory=dict)


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


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip()


def split_lines(text: str) -> list[str]:
    return [normalize_path(line) for line in text.splitlines() if line.strip()]


def unique_sorted(paths: list[str]) -> list[str]:
    return sorted({normalize_path(path) for path in paths if path.strip()})


def count_category(files: list[FileResult], category: str) -> int:
    return sum(1 for item in files if item.category == category)


def is_generated(path: str) -> bool:
    return path in GENERATED_EXACT or path.startswith(GENERATED_PREFIXES)


def is_text_scope(path: str) -> bool:
    return (
        path in GENERATED_EXACT
        or path in SOURCE_EXACT
        or path.startswith(GENERATED_PREFIXES)
        or path.startswith(TEXT_PREFIXES)
        or (path.startswith("docs/agent-system/") and path.endswith(TEXT_SUFFIXES))
    )


def changed_files_from_status() -> list[str]:
    result = run_git(["status", "--short", "-uall"])
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        payload = line[3:] if len(line) > 3 else line
        if " -> " in payload:
            _, payload = payload.split(" -> ", 1)
        paths.append(payload.strip().strip('"'))
    return paths


def untracked_files() -> set[str]:
    result = run_git(["ls-files", "--others", "--exclude-standard"])
    if result.returncode != 0:
        return set()
    return set(split_lines(result.stdout))


def changed_files(base: str) -> tuple[list[str], dict[str, str]]:
    commands = {
        "committed": ["diff", "--name-only", f"{base}...HEAD"],
        "working": ["diff", "--name-only"],
        "staged": ["diff", "--cached", "--name-only"],
    }
    paths_by_scope: dict[str, str] = {}
    for scope, command in commands.items():
        result = run_git(command)
        if result.returncode == 0:
            for path in split_lines(result.stdout):
                paths_by_scope[path] = scope
    for path in changed_files_from_status():
        paths_by_scope.setdefault(normalize_path(path), "status")
    # `git status --short -uall` выше уже включает untracked paths; повторный
    # `git ls-files --others` на Windows Docker bind mount не даёт новых данных.
    return unique_sorted(list(paths_by_scope)), paths_by_scope


def diff_args_for(scope: str, base: str, path: str) -> list[str]:
    if scope == "committed":
        return ["diff", f"{base}...HEAD", "--", path]
    if scope == "staged":
        return ["diff", "--cached", "--", path]
    return ["diff", "--", path]


def diff_args(scope: str, base: str) -> list[str]:
    # Один tree-to-working-tree diff уже включает committed, staged и рабочие
    # изменения относительно base; отдельные scope не нужны для EOL verdict.
    return ["diff", base]


def parse_numstat(text: str) -> dict[str, tuple[str, str]]:
    metadata: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        cells = line.split("\t", 2)
        if len(cells) == 3:
            metadata[normalize_path(cells[2])] = (cells[0], cells[1])
    return metadata


def collect_scope_metadata(scope: str, base: str) -> ScopeMetadata:
    args = diff_args(scope, base)
    calls = {
        "exact_numstat": [args[0], "--numstat", *args[1:]],
        "ignore_space_numstat": [args[0], "--numstat", "--ignore-space-at-eol", *args[1:]],
    }
    parsed: dict[str, dict[str, object]] = {}
    for field_name, command in calls.items():
        result = run_git(command)
        if result.returncode != 0:
            parsed[field_name] = {}
        else:
            parsed[field_name] = parse_numstat(result.stdout)
    return ScopeMetadata(**parsed)


def parse_cloud_readme_map() -> dict[str, str]:
    readme = ROOT / "docs/agent-system/cloud/00_README.md"
    if not readme.is_file():
        return {}
    mapping: dict[str, str] = {"docs/agent-system/cloud/00_README.md": "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml"}
    text = readme.read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[1].endswith(".md"):
            continue
        cloud_name = cells[1]
        source_path = cells[2]
        if source_path.startswith("docs/"):
            mapping[f"docs/agent-system/cloud/{cloud_name}"] = source_path
    return mapping


def matching_source_for_generated(path: str, cloud_map: dict[str, str]) -> str:
    # Freshness-поля cloud README зависят от base commit и допускаются без изменения manifest.
    if path == "docs/agent-system/cloud/00_README.md":
        return ""
    if path == "docs/agent-system/PROJECT_FILE_MAP.md":
        return "docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml"
    return cloud_map.get(path, "")


def classify_file(path: str, scope: str, changed: set[str], cloud_map: dict[str, str], metadata: ScopeMetadata) -> FileResult:
    if SENSITIVE_FILENAME_RE.search(path):
        return FileResult(path=path, scope=scope, status="", category="not_checked", reason="sensitive_filename")
    if not is_text_scope(path):
        return FileResult(path=path, scope=scope, status="", category="not_checked", reason="outside_text_scope")
    if scope == "untracked":
        return FileResult(path=path, scope=scope, status="??", category="not_checked", reason="untracked")

    status = ""
    exact = metadata.exact_numstat.get(path)
    if exact == ("-", "-"):
        return FileResult(path=path, scope=scope, status=status, category="binary_or_unreadable", reason="binary_diff")
    if exact is None:
        # Git status can still mark files as modified when Windows line endings are the only practical noise.
        category = "eol_only_changed" if is_generated(path) and scope == "status" else "no_change"
        return FileResult(path=path, scope=scope, status=status, category=category, reason="status_only_no_text_diff")

    if path not in metadata.ignore_space_numstat:
        category = "whitespace_only_changed"
    else:
        category = "content_changed"

    matching_source = matching_source_for_generated(path, cloud_map) if is_generated(path) else ""
    suspicious = bool(is_generated(path) and category == "content_changed" and matching_source and matching_source not in changed)
    return FileResult(
        path=path,
        scope=scope,
        status=status,
        category=category,
        matching_source=matching_source,
        suspicious_generated_drift=suspicious,
    )


def build_report(base: str, strict: bool) -> GuardReport:
    print("generated_eol_guard: collecting batch Git metadata", file=sys.stderr)
    metadata_by_scope = {
        "combined": collect_scope_metadata("combined", base),
    }
    scopes = {path: "combined" for path in metadata_by_scope["combined"].exact_numstat}
    for path in changed_files_from_status():
        scopes.setdefault(normalize_path(path), "status")
    paths = unique_sorted(list(scopes))
    print(f"generated_eol_guard: classifying {len(paths)} paths", file=sys.stderr)
    cloud_map = parse_cloud_readme_map()
    changed = set(paths)
    report = GuardReport(base=base, changed_files=paths)
    report.files = [
        classify_file(path, scope, changed, cloud_map, metadata_by_scope.get(scope, ScopeMetadata()))
        for path in paths
        for scope in [scopes.get(path, "committed")]
    ]

    grouped: dict[str, list[str]] = {
        "content_changed": [],
        "eol_only_changed": [],
        "whitespace_only_changed": [],
        "not_checked": [],
        "binary_or_unreadable": [],
    }
    for item in report.files:
        if is_generated(item.path):
            grouped.setdefault(item.category, []).append(item.path)
        if item.suspicious_generated_drift:
            report.suspicious_generated_content_drift.append(item.path)

    report.generated_files = {key: sorted(value) for key, value in grouped.items() if value}
    if report.suspicious_generated_content_drift:
        report.blockers.append("suspicious generated content drift detected")

    generated_eol_noise = grouped.get("eol_only_changed", []) + grouped.get("whitespace_only_changed", [])
    if generated_eol_noise:
        message = "generated EOL/whitespace-only changes detected"
        if strict:
            report.blockers.append(message)
        else:
            report.warnings.append(message)
    return report


def render_human(report: GuardReport) -> str:
    data = report.to_json_dict()
    lines = [
        "generated_eol_guard",
        "",
        f"base: {report.base}",
        f"changed_files_count: {data['changed_files_count']}",
        "",
        f"content_changed_count: {data['content_changed_count']}",
        f"eol_only_changed_count: {data['eol_only_changed_count']}",
        f"whitespace_only_changed_count: {data['whitespace_only_changed_count']}",
        f"not_checked_count: {data['not_checked_count']}",
        "",
        "generated_files:",
    ]
    for category in ("content_changed", "eol_only_changed", "whitespace_only_changed", "not_checked", "binary_or_unreadable"):
        values = report.generated_files.get(category, [])
        lines.append(f"  {category}:")
        lines.extend(f"    - {path}" for path in values)
        if not values:
            lines.append("    - <none>")
    lines.extend(
        [
            "",
            "recommendation:",
            "  - review content_changed files",
            "  - EOL-only files may be restored or normalized only by explicit scoped fix",
            "  - do not run repository-wide renormalize without architect approval",
            "",
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify generated EOL/whitespace noise without changing git state.")
    parser.add_argument("--base", default="origin/developer")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    report = build_report(args.base, args.strict)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")
    return 1 if report.blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
