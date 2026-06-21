# TASK-0037 - METH-FILE-MAP-GEN-01

## Задача

Задача для docs-maintainer: METH-FILE-MAP-GEN-01.

Рекомендуемый режим исполнения:

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
Запуск: Local only.
Режим: Agent.
Почему: требуется добавить генератор, производную карту файлов, parity-check и release/regen hooks без выхода за branch guard.

## Repository

- Repository: MaximKolomeets/agent-system-development
- Local path: `C:\neural\repos\agent-system-development`
- Base branch: `developer`
- Working branch: `work/docs-maintainer-01/file-map-gen-01`
- Baseline SHA: `f0306cfa461b24d0ca435ffee4116c1119bacdd4`
- Checked at: `2026-06-21T16:45:58+07:00`
- Journal seq: `0037` из `INDEX.md`

## Scope

Allowed files:

- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/tools/gen_file_map.py`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/engine-journal/input/TASK-0037-METH-FILE-MAP-GEN-01.md`
- `docs/agent-system/engine-journal/output/RESULT-0037-METH-FILE-MAP-GEN-01.md`
- `docs/agent-system/engine-journal/INDEX.md`

Forbidden:

- любые файлы вне whitelist;
- закрытие или переписывание прошлых journal-записей;
- ослабление governance/prohibition/safety правил;
- чтение `.env`;
- прямые изменения `main` или `developer`;
- commit, если HEAD не `work/docs-maintainer-01/file-map-gen-01`.

## Required changes

1. Добавить генератор `docs/agent-system/tools/gen_file_map.py` без внешних зависимостей.
2. Сгенерировать `docs/agent-system/PROJECT_FILE_MAP.md` как AUTO-GENERATED производную карту из `ADOPTION_TRANSFER_MANIFEST.yml`.
3. В manifest добавить категорию `generated`, зарегистрировать `PROJECT_FILE_MAP.md` как `generated`, а generator как `source`.
4. Расширить `TASK_HEADER_COMMON.md`: inventory add/delete/rename требует manifest update и regeneration/check `PROJECT_FILE_MAP.md`.
5. Добавить release-gate hook в `BRANCH_POLICY.md` и fast-lane check в `OPERATIONAL_FAST_LANE.md`.
6. RESULT-0037 должен содержать Source Delta.

## Checks

- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- Повторный `python docs/agent-system/tools/gen_file_map.py` не меняет `PROJECT_FILE_MAP.md`.
- Source/template/generated concrete files существуют.
- `git diff --name-only` в whitelist.
- `git diff --check`.
- `git rev-parse --abbrev-ref HEAD` -> `work/docs-maintainer-01/file-map-gen-01`.

## STOP

- HEAD не `work/docs-maintainer-01/file-map-gen-01`.
- Требуется изменить файл вне whitelist.
- `--check` не сходится.
- Объём требует split по SIZE-GUARD.

## Передача

Следующий: reviewer - review (`--check` проходит, карта детерминирована, dogfood-регистрация верна); затем архитектор - merge; затем engine - pre-release BATCH-CLOSURE 0034...0037; затем release dev->main.
