# TASK-0043: METH-AUDIT-NITS-01

## Режим

Роль: docs-maintainer. Исполнитель: на усмотрение архитектора. Reasoning effort: средний-высокий. Branch-guard обязателен.

Batch-policy: открытые journal-записи не являются blocker; closure не подмешивать.

## Repo / ветки

- Репозиторий: `MaximKolomeets/agent-system-development`
- Каталог: `C:\neural\repos\agent-system-development`
- base: `developer`
- work: `work/docs-maintainer-01/audit-nits-01`

## Preflight

1. `git fetch --all --prune`
2. `git switch developer`
3. `git pull --ff-only origin developer`
4. `git switch -c work/docs-maintainer-01/audit-nits-01`
5. `git rev-parse --abbrev-ref HEAD` должен вернуть work-ветку.
6. Sequence взять из `INDEX`; ожидается `0043`.

## Discovery

```text
rg -n "docs/agent-system/reviews/" docs/agent-system/CODE_REVIEW_WORKFLOW.md
rg -n "ADOPTION_AUDIT.md" docs/agent-system/ENGINE_ENTRYPOINT.md
rg -n "Recommended Engine Mode|Copy/Paste Completeness Check" docs/agent-system docs/agent-system/templates
```

## Allowed files

- `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/tools/gen_file_map.py` и `docs/agent-system/PROJECT_FILE_MAP.md` только если scope-нота выводится в карту
- файлы с EN-заголовками по скану
- journal 0043

## Изменения

1. Dead links `docs/agent-system/reviews/*` в `CODE_REVIEW_WORKFLOW.md`: если есть реальное место review-отчётов, перенаправить; иначе убрать ссылку, сохранив связную прозу.
2. В manifest добавить scope declaration: карта/манифест покрывают methodology source set (`docs/agent-system/**` + назначенные root-файлы), repo infra (`.github/**` и т.п.) вне scope. Явно отметить `.github/workflows/forbidden-files.yml` как намеренно вне карты.
3. В `ENGINE_ENTRYPOINT.md` пометить `ADOPTION_AUDIT.md` как target_generated artifact, создаваемый в target repository.
4. EN-заголовки `Recommended Engine Mode`, `Copy/Paste Completeness Check` и подобные по скану перевести на русский по `LANGUAGE_POLICY`; английский оставить только для технических токенов.

Не трогать:

- `CODE_REVIEW_WORKFLOW.md:12` `engine=<engine-name>`
- historical `INDEX`/journal branch typo
- per-file `description` в manifest

## Проверки

- dead `reviews/*` references в active scope отсутствуют или валидно перенаправлены;
- EN-заголовки переведены или обоснованно оставлены;
- `ENGINE_ENTRYPOINT.md` помечает `ADOPTION_AUDIT.md` как target_generated;
- `python docs/agent-system/tools/gen_file_map.py --check` exit 0;
- diff только whitelist;
- `git diff --check`;
- branch guard.

## Journal + Source Delta + handoff

`RESULT-0043` должен содержать Source Delta и строку:

```text
Архитектору — загрузить в контекст оркестратора: <изменённые source/template>; asof: <дата>; developer_head_sha: <sha>.
```

## Commit / PR

Commit:

```text
docs(agent-system): audit nits — dead links, map scope, entrypoint annotation, RU headings
```

Создать PR в `developer`.

## Передача

`reviewer — review (dead links 0; scope задекларирован; entrypoint помечен; заголовки по LANGUAGE_POLICY); затем архитектор — merge; затем engine — FIX-4 (state refresh); journal closure — batch перед release`.

## STOP

- HEAD не work-ветка;
- правка вне whitelist;
- size-guard требует split;
- нит не решается однозначно.
