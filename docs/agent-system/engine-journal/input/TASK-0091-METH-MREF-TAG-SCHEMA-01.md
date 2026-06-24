# TASK-0091: METH-MREF-TAG-SCHEMA-01

Статус: in progress; PR pending.

Связанный RESULT file: `docs/agent-system/engine-journal/output/RESULT-0091-METH-MREF-TAG-SCHEMA-01.md`

## Задача

Добавить в `methodology_reference_schema` опциональные поля `source_tag` и `release_tag`, согласовать human-канон в `ENGINE_ENTRYPOINT.md` и сохранить `source_commit` обязательным reproducibility anchor.

## Baseline и claim

- execution_started_at measured: `2026-06-24T20:46:52.0694784+07:00`
- baseline `developer` / `origin/developer`: `318c763d0e601eacf8b2e43e1f4548628e3ec4a8`
- baseline `origin/main`: `8c21a45bf189432afcdabfb164f85d175271df74`
- work branch: `work/docs-maintainer-01/mref-tag-schema-01`
- last seq из INDEX: `0090`
- собственный seq: `0091`
- PR #238 state: `MERGED`, merge commit `6ad7cb7c194822c803d041b1cd3de39f210ed353`
- PR #239 state: `MERGED`, merge commit `318c763d0e601eacf8b2e43e1f4548628e3ec4a8`
- Старая пустая ветка `work/docs-maintainer-01/mref-tag-schema-01` пересоздана от свежего `developer`; собственных commits/diff на ней не было.

## Allowed scope

- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` — только блок `methodology_reference_schema`.
- `docs/agent-system/ENGINE_ENTRYPOINT.md`.
- Собственные TASK/RESULT 0091.
- `docs/agent-system/engine-journal/INDEX.md`.
- `docs/agent-system/cloud/**` после regen.

## Передача

Следующий: docs-maintainer — выполнить schema/human-canon правку, проверки, commit/push/PR и финализировать RESULT/INDEX.
