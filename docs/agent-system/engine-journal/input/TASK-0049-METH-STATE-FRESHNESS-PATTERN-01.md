# TASK-0049: METH-STATE-FRESHNESS-PATTERN-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать. Исторические/vendor literals не чистить.

## Цель

Сделать state-документы менее привязанными к отдельным PR/release/sync событиям: отделить standing capabilities от volatile pointer и добавить state-refresh как обязательный предпоследний шаг release-gate.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/state-freshness-pattern-01`

## Preflight

1. До любого switch/pull проверить root, remote, текущую ветку и `git status --short`; dirty tree -> STOP.
2. `git fetch --all --prune`
3. `git switch developer`
4. `git pull --ff-only origin developer`
5. `git switch -c work/docs-maintainer-01/state-freshness-pattern-01`
6. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
7. Sequence взять из `INDEX`; текущая запись: `0049`.

## Allowed files

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/cloud/**`
- journal 0049

## Изменения

1. `CURRENT_STATE.md`: верхний live-раздел разделить на `Standing capabilities` и `Current pointer`; standing layer описывает зрелость/возможности методологии, current pointer ссылается на `engine-journal/INDEX.md`, ветки/tags и journal как источники истины вместо дублирования конкретных PR/SHA.
2. `NEXT_STEPS.md`: заменить одноразовый PR-bound список на `Standing Workflow Loop` и короткий `Current Focus`.
3. `BRANCH_POLICY.md`: добавить state-refresh как обязательный предпоследний release-gate step.
4. `docs/agent-system/cloud/**`: регенерировать, так как `CURRENT_STATE.md`, `NEXT_STEPS.md` и `BRANCH_POLICY.md` входят в bundle.

## Проверки

- `CURRENT_STATE.md`/`NEXT_STEPS.md` live-layer без PR#/SHA как source of truth; историческая летопись ниже не переписывается;
- release-gate содержит state-refresh step;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check` exit 0;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0049` должен содержать Source Delta и handoff: архитектору загрузить `CURRENT_STATE.md`, `NEXT_STEPS.md`, `BRANCH_POLICY.md`; обновлённые bundle-файлы брать из `docs/agent-system/cloud/`.

## Commit / PR

Commit:

```text
docs(agent-system): make state docs source-referencing + add state-refresh to release-gate (state-staleness pattern)
```

Создать PR в `developer`.

## Передача

`reviewer — review (state-доки не PR-привязаны, ссылаются на INDEX/tags; release-gate содержит state-refresh шаг; оба --check 0); затем архитектор — merge; затем engine — FIX-NITS; journal closure — batch перед release`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- соблазн чистить history/vendor literals;
- любой обязательный check не проходит.
