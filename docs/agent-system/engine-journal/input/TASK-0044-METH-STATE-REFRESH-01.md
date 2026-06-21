# TASK-0044: METH-STATE-REFRESH-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: средний. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать.

## Цель

Привести `CURRENT_STATE.md` и `NEXT_STEPS.md` к пост-релизной реальности. Только freshness: vendor/tool literals в history_state не чистить и не переписывать.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/state-refresh-01`

## Preflight

1. `git fetch --all --prune`
2. `git switch developer`
3. `git pull --ff-only origin developer`
4. `git switch -c work/docs-maintainer-01/state-refresh-01`
5. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
6. Sequence взять из `INDEX`; ожидается `0044`.

## Allowed files

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- journal 0044

## Изменения

- `CURRENT_STATE.md`: зафиксировать, что methodology released в `main`; завершены depersonalization cleanup, batch-closure policy, closure facts authority, authoritative manifest/parity, generated file map/check, Source Delta rule, Architect -> Orchestrator handoff, adoption templates sync и audit nits.
- `NEXT_STEPS.md`: следующий шаг — pre-release batch-closure 0039-0044, затем release `developer -> main`, затем downstream adoption / реальный verification-проект.
- Убрать устаревший шаг про подготовку release PR после PR #154/#155.
- Исторические vendor/tool literals не трогать.

## Проверки

- нет формулировок `Текущий следующий шаг: подготовить release PR`;
- state отражает post-release + fix-all;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0044` должен содержать Source Delta (`CURRENT_STATE.md`/`NEXT_STEPS.md` → `history_state`, `none`) и строку:

```text
Архитектору — загрузить в контекст оркестратора (STATE-refresh): CURRENT_STATE.md, NEXT_STEPS.md; asof: <дата>; developer_head_sha: <sha>.
```

## Commit / PR

Commit:

```text
docs(agent-system): refresh CURRENT_STATE/NEXT_STEPS post release+fix-all (audit X)
```

Создать PR в `developer`.

## Передача

`fix-all завершён. reviewer — review (state отражает пост-релиз; история не тронута); затем архитектор — merge; затем engine — pre-release BATCH-CLOSURE 0039…0044; затем release dev→main`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- соблазн чистить history literals.
