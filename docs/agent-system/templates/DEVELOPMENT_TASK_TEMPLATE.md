# DEVELOPMENT_TASK_TEMPLATE

## Общий header

Заполнить общий header по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md`:

- Mandatory header (`Задача для <роль>: <task-id>` + role-agnostic блок рекомендуемого режима исполнения: роль / исполнитель «на усмотрение архитектора» / reasoning effort / запуск / режим / почему + execution timestamps);
- Russian-first;
- Рекомендуемый режим исполнения (без имён инструментов/моделей);
- Передача (отчёт заканчивается блоком `Следующий: <роль> — <что делает>`);
- Source-reminder (при изменении методологии/канонов — применить канон `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source-reminder»);
- Verified Baseline;
- Проверка полноты copy/paste;
- Project constitution check.

Ниже — секции, специфичные для задачи разработки.

## Machine-readable task_contract

Для development/write-action задач добавить в начало TASK file fenced YAML block `task_contract` по `docs/agent-system/TASK_CONTRACT.md`. Prose остаётся human explanation; если contract и prose конфликтуют, `engine` пишет `STOP`.

Минимум: `version`, `task_id`, `role`, `mode`, `execution_mode`, `repository.*`, `scope.allowed_files`, `scope.forbidden_files`, `policies.*`, `checks.required`, `stop_conditions`. Для downstream/target задач дополнительно указать `methodology_reference` со stable ref `origin/main` и `policies.language: russian_first`. Для задач, которые меняют сам methodology repository, допустим `methodology_reference.stable_only: false`.

## Task ID

Указать идентификатор задачи.

## Goal

Описать цель и ожидаемый результат.

## Base branch

Указать базовую ветку.

## Work branch

Указать рабочую ветку в разрешенном namespace.

## Разрешенные файлы

Перечислить файлы и директории, которые можно менять.

## Запрещенные файлы

Перечислить файлы и директории, которые нельзя читать или менять.

## Steps

Описать шаги выполнения.

## Checks

Описать проверки перед отчетом.

Если задача создает ordinary PR, проверки должны включать Closure policy для RESULT/INDEX: ordinary terminal state (`architect_ready` / `human_merge_allowed`), PR URL и reviewed head SHA зафиксированы, отдельный post-merge closure PR не требуется. Для release/audit boundary или explicit architect request указывать boundary reconciliation по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure policy».

Добавить semantic completeness checklist по `docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md`: RESULT и PR body не обещают checks/implementation вне фактического diff; docs-only scope не включает tests/tools/code; state docs не объявляют future task как started. Для acceptance/spec/generator задач применять `docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`. Finalized journal surface проверять по `docs/agent-system/JOURNAL_FINALIZATION_POLICY.md`.

## Ожидаемый отчет

Описать формат итогового отчета.

Отчет должен быть на русском языке и содержать language policy result, включая статус commit/PR metadata и review/final-report language.

Отчёт обязан заканчиваться блоком «Передача» по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Передача» (`Следующий: <роль> — <что делает>`). Если задача меняла методологию/каноны — применить Source-reminder по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source-reminder».

Если PR был merged, отчет должен содержать статус PR после review (`PR status after review`), PR URL и reviewed head SHA. Для ordinary PR merge commit SHA / `merged_at` берутся из GitHub PR metadata и не обязаны backfill'иться в RESULT. Для release/audit boundary или explicit architect request отчет отдельно фиксирует boundary reconciliation status: `boundary_closed`, `required`, `not_required` или `explicit_architect_request`.
