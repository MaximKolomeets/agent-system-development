# TASK-0014-METH-GOVERNANCE-BOUNDARIES-branch-main-rules

Дословная копия входной задачи METH-GOVERNANCE-BOUNDARIES.

---

# Задача для docs-maintainer-01: METH-GOVERNANCE-BOUNDARIES

## Рекомендуемый режим engine
Запуск: Local only. Рекомендуемый engine: Claude Code.
Модель: Claude Sonnet 4.6
Effort (reasoning): Medium
Режим: Agent, строгий allowed-files whitelist.

## Цель
Закрепить два governance-правила явно: (1) агент никогда не пушит/мержит в main; (2) агент работает только в своих ветках.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки: base developer; work work/docs-maintainer-01/governance-boundaries

## Allowed files
docs/agent-system/BRANCH_POLICY.md
docs/agent-system/ROLE_MODEL.md
AGENTS.md
+ журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX)

## Изменения (канон + ссылки, без дублирования прозой)
Правило 1 — push в main:
- канон в BRANCH_POLICY.md: main обновляется ТОЛЬКО через release-PR (developer→main), который мержит человек-архитектор. Агент может ПОДГОТОВИТЬ release-PR, но НЕ мержит и НЕ пушит в main.
- в AGENTS.md (forbidden list) и ROLE_MODEL.md — короткая ссылка на этот канон, не повтор прозой.

Правило 2 — чужие ветки:
- канон в BRANCH_POLICY.md: каждый агент действует только в своих work/<role>/<task>; запрещено пушить, менять, force-пушить или удалять ветку другого агента. Передача между агентами — только через merged PR в developer, не через правку чужих веток.
- в ROLE_MODEL.md и AGENTS.md — короткая ссылка на канон.

Формулировки согласовать с существующим BRANCH_POLICY/ROLE_MODEL, не вводить противоречий.

## Forbidden
файлы вне whitelist; дублирование правил прозой в нескольких местах (только канон + ссылки); .env; main/developer напрямую; ввод credentials; редактирование RESULT прошлых задач.

## Preflight
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/governance-boundaries

## Journal
TASK-<next>: дословная копия. RESULT-<next>: что добавлено в канон, где ссылки, baseline SHA, timestamp ISO-8601. INDEX: запись <next>. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only; git diff --check
Вручную: правила в одном каноне (BRANCH_POLICY), остальные файлы ссылаются; противоречий со старым текстом нет.

## Commit / push / PR
commit: docs(agent-system): codify no-push-to-main and own-branch-only rules
git push -u origin work/docs-maintainer-01/governance-boundaries
gh теперь доступен → gh pr create base=developer.

## DoD
правила 1 и 2 закреплены каноном + ссылками; только whitelist+журнал; diff --check чист; TASK/RESULT/INDEX без placeholders; PR создан через gh; Russian-first.

## STOP
правка вне whitelist; противоречие со старым BRANCH_POLICY/ROLE_MODEL без явного разрешения; push требует credentials; секрет найден.
