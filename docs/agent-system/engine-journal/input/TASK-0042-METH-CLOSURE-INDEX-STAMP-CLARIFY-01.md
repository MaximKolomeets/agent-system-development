# Задача для docs-maintainer-01: METH-CLOSURE-INDEX-STAMP-CLARIFY-01

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
branch-guard.

Batch-policy: открытые journal-записи не блокируют; closure не подмешивать.

## Цель

Закрепить единый closure-канон: merge-факты авторитетны в `RESULT-<seq>`
closure-stamp; `INDEX.md` несёт status + PR URL и не дублирует полный
mergeCommit.

## Discovery

Проверить формулировки про `RESULT`/`INDEX`, merge facts и mergeCommit в:

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`;
- `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`;
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`;
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`, если closure review-gate выражен там.

## Allowed files

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`
- `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`
- `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0042-METH-CLOSURE-INDEX-STAMP-CLARIFY-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0042-METH-CLOSURE-INDEX-STAMP-CLARIFY-01.md`

## Изменения

- В `ENGINE_JOURNAL_CONTRACT.md` добавить канон `Closure facts authority`.
- В closure-шаблонах закрепить: факты пишутся в `RESULT` closure-stamp, в `INDEX` только status + PR URL + safe summary; optional mergedAt date допустима.
- В code-review template и manual review checklist закрепить review-gate: reviewer сверяет merge-факты по `RESULT` closure-stamp и GitHub/local git; не требует mergeCommit в `INDEX`.
- Legacy-записи с фактами в `INDEX` оставить как append-only history, без retrofit.

## Проверки

- Ни один active contract/template/checklist не требует mergeCommit в `INDEX` как gate.
- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- `git diff --check` -> clean.
- diff только whitelist.
- branch guard: HEAD == `work/docs-maintainer-01/closure-index-stamp-clarify-01`.

## Передача

Следующий: reviewer — review (единый канон facts-in-RESULT/INDEX-status;
review-gate не требует mergeCommit в INDEX; нет противоречий); затем архитектор —
merge; затем engine — FIX-6 (audit nits); journal closure — batch перед release.
