# RESULT-0027-METH-DEPERSONALIZE-2b-1

## Метаданные

- Задача: `METH-DEPERSONALIZE-2b-1` (TASK-0027).
- Роль: docs-maintainer.
- Исполнитель: на усмотрение архитектора.
- Base branch: `developer`.
- Work branch: `work/docs-maintainer-01/depersonalize-2b-1`.
- Baseline SHA (`origin/developer`): `983da98a2d435ba91b652b0205f3d0f6f0867a0f`.
- Timestamp (ISO-8601): `2026-06-20T22:01:32+07:00`.
- Тип: docs-only, methodology-hardening (phase-2b-1, finding A).
- PR: [#163](https://github.com/MaximKolomeets/agent-system-development/pull/163) — open, в `developer` (review/merge выполняет человек).
- Head SHA at PR creation: `<finalized-after-push>`.

## Что сделано

Заменены не-role-agnostic шапки режима на role-agnostic форму по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md`. Затронут ТОЛЬКО заголовочный блок режима (finding A). Actor-текст (finding C) и manifest (finding D) в этом PR не трогались — они отложены в 2b-2/2b-3/2b-4.

### Трансформация блока

Старый блок (во всех 13 файлах, идентичный либо вариант):

```
Рекомендуемый режим <engine-name>:

Запуск: <...>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <...>
Почему: <...>
```

→ role-agnostic:

```
Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <...>
Режим: <...>
Почему: <...>
```

Убраны `<engine-name>` и `Модель: <model recommendation>`; добавлены `Роль` / `Исполнитель: на усмотрение архитектора` / `Reasoning effort`. Порядок и формулировки выровнены с каноном `TASK_HEADER_COMMON`.

### Изменённые файлы (13, все в whitelist)

| Файл | Что заменено |
|---|---|
| `README.md` | стандартный блок режима |
| `docs/agent-system/ENGINE_ENTRYPOINT.md` | стандартный блок режима |
| `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md` | стандартный блок режима |
| `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md` | стандартный блок режима |
| `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md` | header-скелет (расширен role-agnostic строками) |
| `docs/agent-system/ADOPTION_GUIDE.md` | стандартный блок режима |
| `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md` | блок режима + descriptive «Заполнить блок …» |
| `docs/agent-system/templates/ADOPTION_PROMPT.md` | 2 идентичных блока режима (replace_all) |
| `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md` | блок режима + descriptive «Заполнить блок …» |
| `docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md` | header-скелет (расширен role-agnostic строками) |
| `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md` | placeholder-блок (стр. 20) + заполненный пример (стр. 283: `Модель`→`Роль: docs-maintainer`, `Reasoning: High`→`Reasoning effort: высокий`) |
| `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md` | стандартный блок режима |
| `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md` | блок режима + descriptive «Заполнить блок …» |

Descriptive-строки `Заполнить блок \`Рекомендуемый режим <engine-name>\`` в 3 task-шаблонах приведены к `Рекомендуемый режим исполнения` + роль/исполнитель/reasoning effort.

## Проверки

- `rg "Рекомендуемый режим <engine-name>|^Модель:"` вне engine-journal → **0**.
- `git status --porcelain` → 13 whitelist-файлов (+ журнал TASK/RESULT/INDEX).
- `git diff --check` → чисто.
- Actor-текст (ChatGPT/Codex и т. п.) не трогался — finding C вне scope этого PR (подтверждено: правки только в блоках режима).
- Branch-guard: HEAD == `work/docs-maintainer-01/depersonalize-2b-1`.

## Source-reminder

Методология (каноны/шаблоны) менялась → правило применимо. Generic: **Обновить Source-снапшот у зарегистрированных потребителей** (реестр `docs/agent-system/SOURCE_CONSUMERS.md` ведётся в потребляющем развёртывании; обезличенная upstream-методология потребителей не перечисляет). Verbatim source-снапшота этих файлов в `source/` нет (там только навигационный индекс) — обновлять нечего.

## Остаток (follow-up под-PR)

- **2b-2** — adapter-доки оркестратора (`ORCHESTRATOR_RESPONSE_STANDARD` ~30, `ORCHESTRATOR_OPERATING_CONTRACT`, `templates/ORCHESTRATOR_RESPONSE_TEMPLATE` actor): сохранить одну adapter-пометку, остальное → «оркестратор».
- **2b-3** — active-rule workflow/policy/guides (~15 файлов): actor-scrub ChatGPT→оркестратор, Codex/Engine→исполнитель(engine); строки-запреты сохранить.
- **2b-4** — history/state (`DECISION_LOG`, `CURRENT_STATE`, `RELEASE_READINESS`, agent-reports, `STAGE_2`) консервативно (литеральные исторические артефакты не править) + manifest D (`ADOPTION_TRANSFER_MANIFEST.yml`: выровнять `mandatory_engine_task_header`, добавить `SOURCE_CONSUMERS.md` в `categories.generic.files`).

## Передача

- Сделано: role-agnostic шапки в 13 не-журнальных файлах по канону `TASK_HEADER_COMMON`; actor-текст C не трогался. PR [#163](https://github.com/MaximKolomeets/agent-system-development/pull/163).
- Следующий: reviewer — review PR #163 (шапки role-agnostic; actor-текст C не трогался).
- Обновить Source-снапшот у зарегистрированных потребителей: … (generic).
- Остаток: 2b-2 (adapter, generic-пометка), 2b-3 (active-rule), 2b-4 (history консервативно + manifest D).
