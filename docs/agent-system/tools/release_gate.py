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
INDEX_PATH = "docs/agent-system/engine-journal/INDEX.md"
LEDGER_PATH = "docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json"
COMMIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
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
    current_branch: str = ""
    tag_source: str = "local_refs_requires_prefetch"
    tag_precondition_text: str = (
        "Tag-проверка читает только локальные `refs/tags`; перед запуском "
        "выполните `git fetch --tags --prune`, иначе существующий remote-tag "
        "может быть не виден."
    )
    tag_exists: bool = False
    base_tag: str = ""
    base_commit: str = ""
    main_sha: str = ""
    candidate_sha: str = ""
    release_mode: str = "normal"
    base_tag_ancestor_main: str = "not_checked"
    main_ancestor_candidate: str = "not_checked"
    recovery_evidence_status: str = "not_checked"
    recovery_preconditions: list[str] = field(default_factory=list)
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
    allowed = {"for-each-ref", "show-ref", "show", "rev-parse", "rev-list", "diff", "merge-base"}
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


def is_ancestor(older: str, newer: str) -> bool:
    return run_git(["merge-base", "--is-ancestor", older, newer]).returncode == 0


def candidate_file(candidate_sha: str, path: str) -> str | None:
    """Читает evidence только из immutable candidate tree без fallback на checkout."""
    if not COMMIT_SHA_RE.fullmatch(candidate_sha) or path.startswith(("/", "\\")) or ".." in Path(path).parts:
        return None
    completed = run_git(["show", f"{candidate_sha}:{path}"])
    return completed.stdout if completed.returncode == 0 else None


def recovery_evidence(version: str, candidate_sha: str) -> tuple[bool, list[str]]:
    """Проверяет version-scoped evidence в exact candidate snapshot."""
    version_identity = version.removeprefix("v").replace(".", "-").upper()
    index_text = candidate_file(candidate_sha, INDEX_PATH)
    ledger_text = candidate_file(candidate_sha, LEDGER_PATH)
    if index_text is None or ledger_text is None:
        return False, []
    rows: list[list[str]] = []
    for line in index_text.splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) == 10 and re.fullmatch(r"\d{4}", cells[0]):
                rows.append(cells)
    roles = {
        "recovery": f"METH-RELEASE-V{version_identity}-GOVERNANCE-RECOVERY-01",
        "uat": f"METH-RELEASE-V{version_identity}-HUMAN-UAT-EVIDENCE-01",
        "reviewer": f"METH-RELEASE-V{version_identity}-FULL-PAYLOAD-CONSISTENCY-GATE-01",
    }
    selected = {name: next((row for row in rows if row[1] == task_id), None) for name, task_id in roles.items()}
    if any(row is None for row in selected.values()):
        return False, []
    proofs: list[str] = []
    for name, row in selected.items():
        assert row is not None
        if "merged" not in row[7]:
            return False, proofs
        proofs.append(f"{name}_index_merged")
        result_relative = row[3]
        if not re.fullmatch(r"output/RESULT-\d{4}-[A-Z0-9][A-Z0-9-]*\.md", result_relative):
            return False, proofs
        text = candidate_file(candidate_sha, f"docs/agent-system/engine-journal/{result_relative}")
        if text is None:
            return False, proofs
        if name != "recovery" and (
            "RESULT closed after merge: yes" not in text or "INDEX closed after merge: yes" not in text
        ):
            return False, proofs
        if name == "uat" and not re.search(r"^human_uat_status:\s*PASS\s*$", text, re.MULTILINE):
            return False, proofs
        if name == "reviewer" and not re.search(r"^release_gate_verdict:\s*PASS_PENDING_HUMAN_MERGE\s*$", text, re.MULTILINE):
            return False, proofs
        proofs.append(f"{name}_result_merged" if name == "recovery" else f"{name}_result_closed")
    try:
        ledger = json.loads(ledger_text)
    except json.JSONDecodeError:
        return False, proofs
    terminal = {
        (item.get("sequence"), item.get("task_id"))
        for item in ledger.get("reservations", [])
        if isinstance(item, dict) and item.get("state") == "consumed"
    }
    for name in ("uat", "reviewer"):
        row = selected[name]
        assert row is not None
        if (row[0], row[1]) not in terminal:
            return False, proofs
        proofs.append(f"{name}_reservation_consumed")
    return True, proofs


def current_branch(report: ReleaseGateReport) -> str:
    """Фиксирует branch context read-only, чтобы release-boundary gate не путал контекст запуска.

    При detached HEAD `git rev-parse --abbrev-ref HEAD` возвращает `HEAD`. Любое значение,
    кроме `developer` (включая `main` и detached HEAD), трактуется как off-developer контекст:
    ready-gate пропускается с warning READY_GATE_SKIPPED_OFF_DEVELOPER, а не blocker.
    """
    return require_stdout(run_git(["rev-parse", "--abbrev-ref", "HEAD"]), "CURRENT_BRANCH_UNAVAILABLE", report)


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
    ]
    for script, args in checks:
        status = run_python_script(script, args)
        report.gate_statuses.append(status)
        if status.exit_code != 0:
            if script.endswith("gen_file_map.py"):
                report.blockers.append("GEN_FILE_MAP_CHECK_FAILED")
            elif script.endswith("gen_cloud_bundle.py"):
                report.blockers.append("GEN_CLOUD_BUNDLE_CHECK_FAILED")

    release_boundary_script = "docs/agent-system/tools/check_task_ready.py"
    release_boundary_args = ["--base", "origin/main", "--release-boundary"]
    release_boundary_command = " ".join([sys.executable, release_boundary_script, *release_boundary_args])
    if report.current_branch != "developer":
        # exit_code=0 здесь условный: проверка не запускалась.
        # Авторитетный признак пропуска - поле status="skipped_off_developer";
        # JSON-потребители должны читать status, а не только exit_code.
        report.gate_statuses.append(
            CommandStatus(
                command=release_boundary_command,
                exit_code=0,
                status="skipped_off_developer",
            )
        )
        report.warnings.append(
            "READY_GATE_SKIPPED_OFF_DEVELOPER: release-boundary ready-gate "
            "канонически проверяется на `developer`; текущая ветка "
            f"`{report.current_branch or '<unknown>'}`."
        )
        return

    status = run_python_script(release_boundary_script, release_boundary_args)
    report.gate_statuses.append(status)
    if status.exit_code != 0:
        report.blockers.append("RELEASE_BOUNDARY_READY_GATE_FAILED")


def build_human_action_text(version: str) -> list[str]:
    return [
        "Инструмент только собирает evidence и не выполняет release actions.",
        "Архитектор вручную создаёт или проверяет release PR `developer -> main`, затем принимает решение о merge.",
        f"Архитектор вручную ставит annotated tag `{version}` на release merge commit после merge в `main`.",
        "Publication decision и sync `main -> developer` остаются human-only действиями.",
        "Engine/agent не должен merge/tag/publish/sync/push; канон: RELEASE_AUTHORITY_POLICY.md и HUMAN_GATE_POLICY.md.",
    ]


def build_report(version: str, base: str, governance_recovery: bool = False) -> ReleaseGateReport:
    report = ReleaseGateReport(version=version, base=base)
    report.human_action_text = build_human_action_text(version)
    report.current_branch = current_branch(report)

    tags = list_tags()
    report.tag_exists = tag_exists(version)
    if report.tag_exists:
        report.blockers.append("RELEASE_TAG_ALREADY_EXISTS")

    report.base_tag = find_base_tag(version, tags, report)
    if report.base_tag:
        report.base_commit = peeled_commit(f"refs/tags/{report.base_tag}", report, "BASE_TAG_COMMIT_UNAVAILABLE")

    report.main_sha = peeled_commit("origin/main", report, "MAIN_SHA_UNAVAILABLE")
    report.candidate_sha = peeled_commit(base, report, "CANDIDATE_SHA_UNAVAILABLE")

    if report.base_commit and report.main_sha and report.candidate_sha:
        report.base_tag_ancestor_main = "passed" if is_ancestor(report.base_commit, report.main_sha) else "failed"
        report.main_ancestor_candidate = "passed" if is_ancestor(report.main_sha, report.candidate_sha) else "failed"
    if report.base_commit and report.main_sha and report.main_sha != report.base_commit:
        if not governance_recovery:
            report.blockers.append("MAIN_NOT_AT_LAST_RELEASE_TAG")
        else:
            report.release_mode = "governance_recovery"
            evidence_ok, proofs = recovery_evidence(version, report.candidate_sha)
            report.recovery_preconditions = proofs
            report.recovery_evidence_status = "passed" if evidence_ok else "failed"
            if report.base_tag_ancestor_main != "passed":
                report.blockers.append("RECOVERY_BASE_TAG_NOT_ANCESTOR_MAIN")
            if report.main_ancestor_candidate != "passed":
                report.blockers.append("RECOVERY_MAIN_NOT_ANCESTOR_CANDIDATE")
            if not evidence_ok:
                report.blockers.append("RECOVERY_EVIDENCE_INCOMPLETE")

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
    print(f"current_branch: {report.current_branch or '<unknown>'}")
    print(f"tag_source: {report.tag_source}")
    print(f"tag_precondition: {report.tag_precondition_text}")
    print(f"tag_exists: {str(report.tag_exists).lower()}")
    print(f"base_tag: {report.base_tag or '<none>'}")
    print(f"base_commit: {report.base_commit or '<none>'}")
    print(f"main_sha: {report.main_sha or '<none>'}")
    print(f"candidate_sha: {report.candidate_sha or '<none>'}")
    print(f"release_mode: {report.release_mode}")
    print(f"base_tag_ancestor_main: {report.base_tag_ancestor_main}")
    print(f"main_ancestor_candidate: {report.main_ancestor_candidate}")
    print(f"recovery_evidence_status: {report.recovery_evidence_status}")
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
    parser.add_argument(
        "--governance-recovery",
        action="store_true",
        help="Явно включить fail-closed governance-recovery path; стандартные gates не пропускаются.",
    )
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args()
    report = build_report(args.version, args.base, args.governance_recovery)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_text_report(report)
    return 0 if not report.blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
