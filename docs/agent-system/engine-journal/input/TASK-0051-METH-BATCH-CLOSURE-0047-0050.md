# TASK-0051: METH-BATCH-CLOSURE-0047-0050

## Режим

Роль: docs-maintainer/closer. Исполнитель: на усмотрение архитектора. Reasoning effort: высокий. Branch-guard обязателен.

Per-task closure: закрывающий batch-проход перед release закрывается сам как terminal entry (`closed-at-creation`).

## Цель

Закрыть journal entries `0047`…`0050` после merge их PR и подготовить release runway: факты merge авторитетно записать в RESULT closure-stamps, а в INDEX оставить status + PR URL без полного mergeCommit.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/batch-closure-0047-0050`

## Preflight

1. Перед sync/checkout проверить repository root, remote, branch и `git status --short`; dirty tree -> STOP.
2. `git fetch --all --prune`
3. `git switch developer`
4. `git pull --ff-only origin developer`
5. `git switch -c work/docs-maintainer-01/batch-closure-0047-0050`
6. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
7. Terminal sequence взять из `INDEX`; текущая запись: `0051`.

## Closure set

Получить факты через `gh`, не из памяти:

| seq | PR |
|---|---|
| `0047` | `#189` |
| `0048` | `#190` |
| `0049` | `#191` |
| `0050` | `#192` |

Для каждого PR:

```powershell
gh pr view <PR> --json mergeCommit,mergedAt,url,state,headRefOid
```

Если любой `state != MERGED` -> STOP.

## Allowed files

- `docs/agent-system/engine-journal/output/RESULT-0047-*.md`
- `docs/agent-system/engine-journal/output/RESULT-0048-*.md`
- `docs/agent-system/engine-journal/output/RESULT-0049-*.md`
- `docs/agent-system/engine-journal/output/RESULT-0050-*.md`
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0051-METH-BATCH-CLOSURE-0047-0050.md`
- `docs/agent-system/engine-journal/output/RESULT-0051-METH-BATCH-CLOSURE-0047-0050.md`
- `docs/agent-system/cloud/**`

## Изменения

1. В `RESULT-0047`…`RESULT-0050` добавить closure-stamp с `mergeCommit`, `mergedAt`, `url`, `headRefOid` из `gh`.
2. В `INDEX` перевести `0047`…`0050` в `closed; PR #... merged; facts in RESULT`; полный `mergeCommit` в INDEX не писать.
3. Добавить terminal entry `0051`, closed-at-creation; собственный mergeCommit = `stamp at merge`.
4. Регенерировать `docs/agent-system/cloud/**` из-за `INDEX -> cloud/ENGINE_JOURNAL_INDEX.md` (+ `cloud/README.md` freshness).

Не трогать history/vendor literals.

## Проверки

- `0047`…`0050` в INDEX = closed + PR URL, без полного mergeCommit как gate;
- `RESULT-0047`…`RESULT-0050` closure-stamps совпадают с `gh`;
- terminal `0051` = closed-at-creation / stamp-at-merge;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- `python docs/agent-system/tools/gen_cloud_bundle.py --check` exit 0;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Передача

`reviewer — consistency-gate (сверить RESULT-стампы 0047…0050 vs gh: mergeCommit/mergedAt/url; INDEX = status+URL, НЕ сверять INDEX по SHA — FIX-5; терминал closed-at-creation; оба --check 0); затем архитектор — merge; затем release-gate: state-refresh CONFIRM → release dev→main`.
