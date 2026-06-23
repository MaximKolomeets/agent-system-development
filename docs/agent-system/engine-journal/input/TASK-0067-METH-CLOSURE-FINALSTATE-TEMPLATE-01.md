# TASK-0067-METH-CLOSURE-FINALSTATE-TEMPLATE-01

## Задача

Закрепить в closure-каноне и closure-шаблонах, что closure-проход обязан очищать stale final-state поверхности: верхний status-marker закрываемого `RESULT` и terminal `own PR ... open` summary в `INDEX`.

Роль: `docs-maintainer`.
Исполнитель: на усмотрение архитектора.
Режим: Local only; docs-only.

## Baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/closure-finalstate-template-01`.
- Baseline `developer`: `bd98282024b3a59c4bd5aaf96214584ec8b3433b`.
- Timestamp: `2026-06-23T10:50:03+07:00`.
- Prerequisite: PR #210 merged and journal seq 0066 present in `INDEX.md`.

## Allowed files

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md`
- `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0067-METH-CLOSURE-FINALSTATE-TEMPLATE-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0067-METH-CLOSURE-FINALSTATE-TEMPLATE-01.md`
- `docs/agent-system/cloud/**` after cloud regen

## Scope

Добавить producer-side норму и checklist, не меняя смысл closure:

- merge facts остаются authoritative в `RESULT` closure-stamp;
- `INDEX` остаётся status + PR URL + safe summary, без требования полного `mergeCommit`;
- append-only bodies/stamps не переписываются произвольно;
- добавляется только явное требование снять stale final-state surfaces.
