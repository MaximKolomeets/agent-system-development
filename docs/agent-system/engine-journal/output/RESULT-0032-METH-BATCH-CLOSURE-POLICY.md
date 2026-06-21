# RESULT-0032: METH-BATCH-CLOSURE-POLICY

## Summary

Batch-closure policy закреплена в каноне. Старые открытые записи 0027–0031 не закрывались: это ожидаемое batch-состояние до pre-release closure.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/batch-closure-policy`
- Baseline SHA: `618b68429be7cc788335fa125aecdb789f561caf`
- Timestamp: `2026-06-21T11:49:12.0567039+07:00`

## Изменения по файлам

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: старый strict post-merge closure заменён на `Closure policy`; default = batch; per-task closure ограничен исключениями; release/audit/explicit closure остаются строгими gates; review blocker-правила стали batch-aware.
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`: добавлены batch-friendly handoff-формулировки и статусная развилка для closure-pending journal.
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`: closure wording выровнен с batch policy; final report требует batch-friendly handoff, если применимо.
- `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`: добавлен role-agnostic шаблон per-task closure-only задачи.
- `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`: добавлен role-agnostic шаблон pre-release batch-closure задачи.
- `docs/agent-system/BRANCH_POLICY.md`: добавлен release-gate: release `developer -> main` запрещён до полного закрытия journal.
- `docs/agent-system/engine-journal/input/TASK-0032-METH-BATCH-CLOSURE-POLICY.md`: создана входная запись задачи.
- `docs/agent-system/engine-journal/output/RESULT-0032-METH-BATCH-CLOSURE-POLICY.md`: создан RESULT этой задачи.
- `docs/agent-system/engine-journal/INDEX.md`: добавлена строка 0032.

## PR / branch

- Branch: `work/docs-maintainer-01/batch-closure-policy`
- PR URL: `pending until PR creation`
- PR status: `pending until PR creation`
- Commit SHA: `pending until commit`
- Actual/current PR head SHA after final push: `pending until PR creation`

## Проверки

- `git diff --check`: pending.
- `git diff --name-only`: pending.
- branch-guard: pending before commit.
- vendor/tool/model names in new templates: pending.

## Риски

- Нужно проверить reviewer'ом, что новый batch-default не противоречит strict release-gate и audit consistency gate.

## Source-reminder

Обновить Source-снапшот у зарегистрированных потребителей: по `docs/agent-system/SOURCE_CONSUMERS.md`.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE по 0027…0032; затем release dev→main.
