#!/usr/bin/env python3
"""Предотправочная проверка self-contained блока для исполнителя."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BANNED_ROLE_TERMS = {
    "chatgpt",
    "claude",
    "codex",
    "gemini",
    "gpt",
    "openai",
    "anthropic",
}
ADOPTION_TRIGGER_RE = re.compile(
    r"adoption|audit-only|docs-only|downstream|target repository|target/downstream|"
    r"methodology_reference|target repository|target-local|целев",
    re.IGNORECASE,
)
DOWNSTREAM_UNSTABLE_REF_RE = re.compile(
    r"stable_only:\s*true[\s\S]{0,500}?source_ref:\s*(?:origin/)?developer\b|"
    r"source_ref:\s*(?:origin/)?developer\b[\s\S]{0,500}?stable_only:\s*true",
    re.IGNORECASE,
)
BANNED_ENGLISH_HEADERS = {
    "required changes",
    "checks",
    "expected checks result",
    "commit/push policy",
    "final report requirements",
    "stop conditions",
    "allowed files",
    "forbidden files",
}


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    pattern: str
    severity: str = "blocker"


@dataclass
class ChecklistReport:
    source: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    matched_rules: list[str] = field(default_factory=list)

    @property
    def result(self) -> str:
        return "valid" if not self.blockers else "blocked"

    def to_json_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["blockers_count"] = len(self.blockers)
        data["warnings_count"] = len(self.warnings)
        data["result"] = self.result
        return data


REQUIRED_RULES = (
    Rule("task_header", "нет шапки `Задача для <роль>: <task-id>`", r"^Задача для\s+[^:\n]+:\s*\S+"),
    Rule("recommended_mode", "нет блока `Рекомендуемый режим исполнения`", r"Рекомендуемый режим исполнения"),
    Rule("role", "нет поля `Роль:`", r"^Роль:\s*\S+"),
    Rule("executor", "нет поля `Исполнитель: на усмотрение архитектора`", r"^Исполнитель:\s*на усмотрение архитектора\b"),
    Rule("reasoning_effort", "нет поля `Reasoning effort:`", r"^Reasoning effort:\s*\S+"),
    Rule("launch", "нет поля `Запуск:`", r"^Запуск:\s*\S+"),
    Rule("mode", "нет поля `Режим:`", r"^Режим:\s*\S+"),
    Rule("why", "нет поля `Почему:`", r"^Почему:\s*\S+"),
    Rule("execution_started_at", "нет `execution_started_at` для measured старта", r"execution_started_at"),
    Rule("baseline", "нет Verified baseline или явного `not applicable`", r"Verified (?:execution )?baseline|Проверенный baseline|not applicable"),
    Rule("repository", "нет repository context", r"repository|Repository|Репозиторий"),
    Rule("base_branch", "нет base branch", r"base_branch|Base branch|Базовая ветка"),
    Rule("working_branch", "нет working branch", r"working_branch|Working branch|Рабочая ветка"),
    Rule("allowed_files", "нет allowed files", r"allowed_files|Allowed files|Разреш[её]нные файлы"),
    Rule("forbidden_files", "нет forbidden files/changes", r"forbidden_files|Forbidden (?:files|changes)|Запрещ[её]нные (?:файлы|изменения)"),
    Rule("checks", "нет проверок", r"checks|required checks|Checks|Проверки"),
    Rule("stop_conditions", "нет STOP-условий", r"stop_conditions|STOP-условия|STOP conditions|STOP"),
    Rule("final_report", "нет требований к финальному отчету", r"Final report|Финальный отчет|Требования к финальному отчету"),
    Rule("russian_first", "нет Russian-first reminder", r"Russian-first|русск|на русском языке"),
    Rule("journal", "нет engine journal / RESULT / INDEX требований", r"engine-journal|RESULT|INDEX|journal"),
    Rule("source_delta", "нет требования Source Delta", r"Source Delta|TASK_HEADER_COMMON\.md"),
    Rule("handoff", "нет блока передачи", r"^## Передача\b|^Передача\b|Следующий:"),
    Rule("task_contract", "нет `task_contract` для substantive блока", r"task_contract:", severity="warning"),
    Rule("commit_policy", "нет явной commit/push/PR policy", r"commit|push|Pull Request|PR\b", severity="warning"),
)


def read_text(path: str | None) -> tuple[str, str]:
    if not path or path == "-":
        return "<stdin>", sys.stdin.read()
    source = Path(path)
    if source.name.lower() == ".env" or source.name.lower().startswith(".env."):
        raise SystemExit("refusing to read sensitive filename")
    return str(source), source.read_text(encoding="utf-8", errors="replace")


def first_task_role(text: str) -> str:
    match = re.search(r"(?m)^Задача для\s+([^:\n]+):", text)
    return match.group(1).strip() if match else ""


def validate(text: str, source: str) -> ChecklistReport:
    report = ChecklistReport(source=source)
    for rule in REQUIRED_RULES:
        if re.search(rule.pattern, text, re.IGNORECASE | re.MULTILINE):
            report.matched_rules.append(rule.id)
            continue
        message = f"{rule.id}: {rule.description}"
        if rule.severity == "warning":
            report.warnings.append(message)
        else:
            report.blockers.append(message)

    role = first_task_role(text).lower()
    if role and any(term in role for term in BANNED_ROLE_TERMS):
        report.blockers.append("task_header_role: role name содержит vendor/tool/model term")

    if ADOPTION_TRIGGER_RE.search(text) and "ADOPTION_TRANSFER_MANIFEST.yml" not in text:
        report.blockers.append("manifest: adoption/downstream блок не ссылается на ADOPTION_TRANSFER_MANIFEST.yml")

    if DOWNSTREAM_UNSTABLE_REF_RE.search(text):
        report.blockers.append("methodology_reference: downstream stable_only task использует developer как source_ref")

    for line in text.splitlines():
        normalized = line.strip().strip("#").strip().lower()
        if normalized in BANNED_ENGLISH_HEADERS:
            report.warnings.append(f"language: англоязычный служебный заголовок `{line.strip()}`")

    if text.count("```") > 2:
        report.warnings.append("fences: возможны вложенные fenced blocks; для engine block использовать BEGIN/END markers")

    return report


def render_human(report: ChecklistReport) -> str:
    lines = [
        "orchestrator_checklist",
        "",
        f"source: {report.source}",
        f"matched_rules_count: {len(report.matched_rules)}",
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Проверить self-contained блок для исполнителя перед отправкой.")
    parser.add_argument("path", nargs="?", help="Файл с блоком для исполнителя; если не указан, читать stdin.")
    parser.add_argument("--json", action="store_true", help="Вывести machine-readable JSON.")
    args = parser.parse_args(argv)

    source, text = read_text(args.path)
    report = validate(text, source)
    if args.json:
        print(json.dumps(report.to_json_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(render_human(report), end="")
    return 1 if report.blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
