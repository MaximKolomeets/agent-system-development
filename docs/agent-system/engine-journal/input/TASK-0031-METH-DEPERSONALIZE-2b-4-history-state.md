# TASK-0031: METH-DEPERSONALIZE-2b-4 (history/state, консервативно)

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий.

Batch-closure policy действует: открытые прошлые journal-записи не являются blocker; closure не подмешивать.

## Цель

Консервативно обезличить активную прозу в history/state-файлах: vendor/tool actor names заменить на роли, а исторические literals сохранить нетронутыми.

## Ветки

- Base: `developer`
- Work: `work/docs-maintainer-01/depersonalize-2b-4`

## Baseline

- Repository: `MaximKolomeets/agent-system-development`
- Baseline SHA: `50f71cc6e4d835b6bfef88d1240e37462b29df47`
- Checked at: `2026-06-21T11:31:24.1183847+07:00`

## Scope

Кандидаты history/state:

- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`
- `docs/agent-system/agents/docs-maintainer-01/CURRENT_STATE_SUMMARY.md`
- `docs/agent-system/agents/docs-maintainer-01/DOC_SYNC_REPORT.md`

`engine-journal/**` не трогать, кроме новой записи `0031` и строки `INDEX.md`.

## Правила изменения

- Активное правило/роль/живая инструкция: заменить на `оркестратор`, `исполнитель (engine)` или `reviewer`.
- Исторический literal: оставить без изменений.
- Если сомнение active vs historical: сохранить literal.
- Prohibition/safety-строки сохранить по смыслу.

## Проверки

- `rg -i "chatgpt|codex|claude code"` по scope: остаются только осознанно-исторические literals.
- `git diff --name-only origin/developer...HEAD`: только whitelist + journal 0031.
- `git diff --check`.
- Branch guard перед commit.

## Передача

Деперсонализация (2b) завершена. Следующий: reviewer — review PR; затем архитектор — merge; затем engine — METH-BATCH-CLOSURE-POLICY; затем pre-release batch-closure (0027…последний); затем release dev→main.

Обновить Source у зарегистрированных потребителей.
