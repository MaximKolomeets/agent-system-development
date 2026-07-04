#!/usr/bin/env python3
"""Read-only advisor для проверки release boundary."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SEMVER_RE = re.compile(r"^v(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)$")
PLACEHOLDER_RE = re.compile(
    r"\b(?:pending|TBD|TODO|placeholder|after PR creation|after push|not run yet)\b|<[^>\r\n]+>",
    re.IGNORECASE,
)


@dataclass
class CommandStatus:
    command: str
    exit_code: int
    status: str


@dataclass
class ReleaseGateReport:
    version: str
    base: str
    tag_exists: bool = False
    base_tag: str = ""
    base_commit: str = ""
    main_sha: str = ""
    candidate_sha: str = ""
    payload_count: int = 0
    payload_files_count: int = 0
    journal_placeholder_status: str = "not_checked"
    gate_statuses: list[CommandStatus] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    human_action_text: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "passed" if not self.blockers else "blocked"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["gate_statuses"] = [asdict(item) for item in self.gate_statuses]
        data["blockers_count"] = len(self.blockers)
        data["warnings_count"] = len(self.warnings)
        data["result"] = self.result
        return data


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Единая точка вызова git: здесь используются только read-only команды."""
    allowed = {"for-each-ref", "show-ref", "rev-parse", "rev-list", "diff"}
    if not args or args[0] not in allowed:
        raise RuntimeError(f"Запрещённый git command для release_gate.py: {args!r}")
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def run_python_script(script: str, args: list[str]) -> CommandStatus:
    """Запускает только read-only validators и сохраняет status без печати values."""
    completed = subprocess.run(
        [sys.executable, script, *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    status = "passed" if completed.returncode == 0 else "failed"
    return CommandStatus(
        command=" ".join([sys.executable, script, *args]),
        exit_code=completed.returncode,
        status=status,
    )


def parse_semver(tag: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.match(tag)
    if not match:
        return None
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
    )


def require_stdout(command: subprocess.CompletedProcess[str], blocker: str, report: ReleaseGateReport) -> str:
    if command.returncode != 0 or not command.stdout.strip():
        report.blockers.append(blocker)
        return ""
    return command.stdout.strip().splitlines()[0].strip()


def list_tags() -> list[str]:
    completed = run_git(["for-each-ref", "--format=%(refname:short)", "refs/tags"])
    if completed.returncode != 0:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def tag_exists(tag: str) -> bool:
    completed = run_git(["show-ref", "--verify", "--quiet", f"refs/tags/{tag}"])
    return completed.returncode == 0


def peeled_commit(ref: str, report: ReleaseGateReport, blocker: str) -> str:
    return require_stdout(run_git(["rev-parse", f"{ref}^{{commit}}"]), blocker, report)


def find_base_tag(version: str, tags: list[str], report: ReleaseGateReport) -> str:
    target_semver = parse_semver(version)
    if target_semver is None:
        report.blockers.append("INVALID_RELEASE_VERSION")
        return ""

    semver_tags: list[tuple[tuple[int, int, int], str]] = []
    include_target = report.tag_exists
    for tag in tags:
        parsed = parse_semver(tag)
        if parsed is not None and (parsed < target_semver or (include_target and parsed == target_semver)):
            semver_tags.append((parsed, tag))

    if not semver_tags:
        report.blockers.append("BASE_RELEASE_TAG_NOT_FOUND")
        return ""
    return max(semver_tags, key=lambda item: item[0])[1]


def count_payload(base_tag: str, base: str, report: ReleaseGateReport) -> None:
    count_text = require_stdout(
        run_git(["rev-list", "--count", f"{base_tag}..{base}"]),
        "PAYLOAD_COUNT_UNAVAILABLE",
        report,
    )
    if count_text.isdigit():
        report.payload_count = int(count_text)
    if report.payload_count == 0:
        report.blockers.append("EMPTY_RELEASE_PAYLOAD")

    files = run_git(["diff", "--name-only", f"{base_tag}..{base}"])
    if files.returncode == 0:
        report.payload_files_count = len([line for line in files.stdout.splitlines() if line.strip()])


def check_journal_placeholders(base_tag: str, base: str, report: ReleaseGateReport) -> None:
    diff = run_git(
        [
            "diff",
            "--unified=0",
            f"{base_tag}..{base}",
            "--",
            "docs/agent-system/engine-journal/INDEX.md",
        ]
    )
    if diff.returncode != 0:
        report.warnings.append("JOURNAL_INDEX_DIFF_UNAVAILABLE")
        report.journal_placeholder_status = "warning"
        return

    added_lines = [
        line[1:]
        for line in diff.stdout.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    if any(PLACEHOLDER_RE.search(line) for line in added_lines):
        report.blockers.append("JOURNAL_PLACEHOLDER_DETECTED")
        report.journal_placeholder_status = "blocked"
        return
    report.journal_placeholder_status = "passed"


def run_generated_and_state_gates(report: ReleaseGateReport) -> None:
    checks = [
        ("docs/agent-system/tools/gen_file_map.py", ["--check"]),
        ("docs/agent-system/tools/gen_cloud_bundle.py", ["--check"]),
        ("docs/agent-system/tools/check_task_ready.py", ["--base", "origin/main", "--release-boundary"]),
    ]
    for script, args in checks:
        status = run_python_script(script, args)
        report.gate_statuses.append(status)
        if status.exit_code != 0:
            if script.endswith("gen_file_map.py"):
                report.blockers.append("GEN_FILE_MAP_CHECK_FAILED")
            elif script.endswith("gen_cloud_bundle.py"):
                report.blockers.append("GEN_CLOUD_BUNDLE_CHECK_FAILED")
            else:
                report.blockers.append("RELEASE_BOUNDARY_READY_GATE_FAILED")


def build_human_action_text(version: str) -> list[str]:
    return [
        "Инструмент только собирает evidence и не выполняет release actions.",
        "Архитектор вручную создаёт или проверяет release PR `developer -> main`, затем принимает решение о merge.",
        f"Архитектор вручную ставит annotated tag `{version}` на release merge commit после merge в `main`.",
        "Publication decision и sync `main -> developer` остаются human-only действиями.",
        "Engine/agent не должен merge/tag/publish/sync/push; канон: RELEASE_AUTHORITY_POLICY.md и HUMAN_GATE_POLICY.md.",
    ]


def build_report(version: str, base: str) -> ReleaseGateReport:
    report = ReleaseGateReport(version=version, base=base)
    report.human_action_text = build_human_action_text(version)

    tags = list_tags()
    report.tag_exists = tag_exists(version)
    if report.tag_exists:
        report.blockers.append("RELEASE_TAG_ALREADY_EXISTS")

    report.base_tag = find_base_tag(version, tags, report)
    if report.base_tag:
        report.base_commit = peeled_commit(f"refs/tags/{report.base_tag}", report, "BASE_TAG_COMMIT_UNAVAILABLE")

    report.main_sha = peeled_commit("origin/main", report, "MAIN_SHA_UNAVAILABLE")
    report.candidate_sha = peeled_commit(base, report, "CANDIDATE_SHA_UNAVAILABLE")

    if report.base_commit and report.main_sha and report.main_sha != report.base_commit:
        report.blockers.append("MAIN_NOT_AT_LAST_RELEASE_TAG")

    if report.base_tag:
        count_payload(report.base_tag, base, report)
        check_journal_placeholders(report.base_tag, base, report)

    run_generated_and_state_gates(report)
    return report


def print_text_report(report: ReleaseGateReport) -> None:
    print("release_gate.py")
    print("")
    print(f"version: {report.version}")
    print(f"base: {report.base}")
    print(f"tag_exists: {str(report.tag_exists).lower()}")
    print(f"base_tag: {report.base_tag or '<none>'}")
    print(f"base_commit: {report.base_commit or '<none>'}")
    print(f"main_sha: {report.main_sha or '<none>'}")
    print(f"candidate_sha: {report.candidate_sha or '<none>'}")
    print(f"payload_count: {report.payload_count}")
    print(f"payload_files_count: {report.payload_files_count}")
    print(f"journal_placeholder_status: {report.journal_placeholder_status}")
    print("")
    print("gate_statuses:")
    for status in report.gate_statuses:
        print(f"- {status.command}: {status.status} ({status.exit_code})")
    print("")
    print(f"blockers_count: {len(report.blockers)}")
    for blocker in report.blockers:
        print(f"- blocker: {blocker}")
    print(f"warnings_count: {len(report.warnings)}")
    for warning in report.warnings:
        print(f"- warning: {warning}")
    print("")
    print("Human action text:")
    for item in report.human_action_text:
        print(f"- {item}")
    print("")
    print(f"result: {report.result}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only advisor для release boundary.")
    parser.add_argument("--version", required=True, help="Целевая release version, например v1.5.4.")
    parser.add_argument("--base", default="origin/developer", help="Candidate ref; default origin/developer.")
    parser.add_argument("--json", action="store_true", help="Печатать machine-readable JSON.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    report = build_report(args.version, args.base)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_text_report(report)
    return 0 if not report.blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
