# TASK-0092: METH-EXEC-FIELD-NAME-CANON-01

Статус: in progress; PR pending.

Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0092-METH-EXEC-FIELD-NAME-CANON-01.md`

## Задача

Закрепить `execution_finished_at` как единственное каноническое имя measured-поля окончания выполнения и запретить для новых записей drift-вариант с suffix `completed_at` после префикса `execution_`.

## Baseline и claim

- execution_started_at measured: `2026-06-24T21:02:55.6395667+07:00`
- baseline `developer` / `origin/developer`: `d1d0adb56fc375c80363dab3cc2f1f3d2a35457a`
- baseline `origin/main`: `8c21a45bf189432afcdabfb164f85d175271df74`
- work branch: `work/docs-maintainer-01/exec-field-name-canon-01`
- last seq из INDEX: `0091`
- собственный seq: `0092`
- P1 PR #240 state: `MERGED`, merge commit `d1d0adb56fc375c80363dab3cc2f1f3d2a35457a`

## Allowed scope

- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- собственные TASK/RESULT 0092
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/cloud/**` после regen

## Передача

Следующий: docs-maintainer — выполнить канон-правку, проверки, commit/push/PR и финализировать RESULT/INDEX.
