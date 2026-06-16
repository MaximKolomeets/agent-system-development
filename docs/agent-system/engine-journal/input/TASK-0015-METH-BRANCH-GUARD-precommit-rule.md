# TASK-0015-METH-BRANCH-GUARD-precommit-rule

Дословная копия входной задачи METH-BRANCH-GUARD.

---

# Задача для docs-maintainer-01: METH-BRANCH-GUARD (правило 3)
Запуск: Local only. Engine: Claude Code. Модель: Claude Sonnet 4.6. Effort: Medium.
Режим: Agent, строгий whitelist. Каталог: C:\neural\repos\agent-system-development

## Цель
Закрепить правило 3: проверка ветки перед коммитом; запрет прямого коммита в developer/main даже локально.

## Ветки: base developer; work work/docs-maintainer-01/branch-guard

## Allowed files
docs/agent-system/BRANCH_POLICY.md
docs/agent-system/templates/TASK_HEADER_COMMON.md
AGENTS.md
+ журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (ожидаемо 0015)

## Изменения (канон + ссылки)
- BRANCH_POLICY (канон, рядом с правилами 1/2): перед ЛЮБЫМ commit агент проверяет `git rev-parse --abbrev-ref HEAD`; если HEAD не его work-ветка (особенно developer/main) → STOP, переключиться на work-ветку. Прямой коммит в developer/main запрещён даже локально. Ссылка-обоснование: инцидент 0013 (resume сессии оставил HEAD на developer).
- templates/TASK_HEADER_COMMON.md: строка в preflight/проверки — «Перед commit: HEAD == work-ветка задачи; если developer/main → STOP».
- AGENTS.md: короткая ссылка на канон.
Без дублирования прозой; согласовать с правилами 1/2.

## Preflight
стандартный sync developer → git switch -c work/docs-maintainer-01/branch-guard
git rev-parse --abbrev-ref HEAD   # == work/...branch-guard, иначе STOP

## Journal / Проверки / Commit / DoD / STOP — как обычно
Перед commit: git rev-parse --abbrev-ref HEAD == work-ветка.
commit: docs(agent-system): codify pre-commit branch guard (rule 3)
gh pr create base=developer.
DoD: правило 3 в каноне + строка в TASK_HEADER_COMMON + ссылка в AGENTS; только whitelist+журнал; diff --check чист; PR через gh; Russian-first.
STOP: HEAD не work-ветка; правка вне whitelist; противоречие; push требует credentials.
