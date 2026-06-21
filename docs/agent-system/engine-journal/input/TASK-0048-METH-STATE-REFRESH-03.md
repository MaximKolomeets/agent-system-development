# TASK-0048: METH-STATE-REFRESH-03

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: средний. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать. Только freshness; history/vendor literals не чистить.

## Цель

Привести `CURRENT_STATE.md` и `NEXT_STEPS.md` к фактическому состоянию после release/sync PR #187/#188 и текущего fix-cycle. Так как state-файлы входят в orchestrator context bundle, регенерировать `docs/agent-system/cloud/**`.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/state-refresh-03`

## Preflight

1. До любого switch/pull проверить root, remote, текущую ветку и `git status --short`; dirty tree -> STOP.
2. `git fetch --all --prune`
3. `git switch developer`
4. `git pull --ff-only origin developer`
5. `git switch -c work/docs-maintainer-01/state-refresh-03`
6. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
7. Sequence взять из `INDEX`; текущая запись: `0048`.

## Allowed files

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/cloud/**`
- journal 0048

## Изменения

1. `CURRENT_STATE.md`: зафиксировать release PR #187, sync PR #188, journal closed до 0046, post-release audit/cleanup и текущий fix-cycle: FIX-CLOUD #189, FIX-STATE, далее FIX-NITS.
2. `NEXT_STEPS.md`: заменить stale шаги batch-closure 0039-0044 / старый release на актуальный путь: завершить FIX-STATE/FIX-NITS -> batch-close 0047-последний -> release `developer -> main` -> downstream adoption / verification project.
3. `docs/agent-system/cloud/**`: регенерировать, так как `CURRENT_STATE.md` и `NEXT_STEPS.md` входят в bundle.

## Проверки

- stale release-step formulations отсутствуют;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check` exit 0;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0048` должен содержать Source Delta и handoff: архитектору загрузить STATE-refresh файлы `CURRENT_STATE.md`, `NEXT_STEPS.md`; обновлённые bundle-файлы брать из `docs/agent-system/cloud/`.

## Commit / PR

Commit:

```text
docs(agent-system): refresh CURRENT_STATE/NEXT_STEPS post #187/#188 + fix-cycle (audit X-01)
```

Создать PR в `developer`.

## Передача

`reviewer — review (state отражает #187/#188+0046+fix-cycle; история не тронута; оба --check 0); затем архитектор — merge; затем engine — FIX-NITS; journal closure — batch перед release`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- соблазн чистить history/vendor literals;
- любой обязательный check не проходит.
