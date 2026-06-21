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
- PR URL: `https://github.com/MaximKolomeets/agent-system-development/pull/168`
- PR status: `OPEN`
- Primary commit SHA: `24db5b05df95719362b03a28b247fe7dd28f517c`
- Head SHA at PR creation: `24db5b05df95719362b03a28b247fe7dd28f517c`
- Actual/current PR head SHA after journal finalization push: см. final report; не фиксируется внутри self-referential commit.
- Mergeable at PR creation check: `MERGEABLE`

## Проверки

- `rg -n "Post-merge Journal Closure|закрывается после merge|строго после merge|не должна оставаться в pre-merge" ...`: 0 совпадений.
- `rg -n -i "chatgpt|codex|claude|gpt|gemini|copilot|<engine-name>|Модель:" docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`: 0 совпадений.
- `git diff --check`: passed.
- `git diff --name-only` + `git ls-files --others --exclude-standard`: только whitelist.
- branch-guard before commit: `work/docs-maintainer-01/batch-closure-policy`.

## Риски

- Нужно проверить reviewer'ом, что новый batch-default не противоречит strict release-gate и audit consistency gate.

## Source-reminder

Обновить Source-снапшот у зарегистрированных потребителей: по `docs/agent-system/SOURCE_CONSUMERS.md`.

## Передача

Следующий: reviewer — review PR; затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE по 0027…0032; затем release dev→main.
