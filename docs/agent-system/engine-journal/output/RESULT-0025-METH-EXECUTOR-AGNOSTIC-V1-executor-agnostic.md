# RESULT-0025-METH-EXECUTOR-AGNOSTIC-V1

## Метаданные

- Задача: `METH-EXECUTOR-AGNOSTIC-V1` (TASK-0025).
- Роль: docs-maintainer-01. Исполнитель: на усмотрение архитектора.
- Base branch: `developer`. Work branch: `work/docs-maintainer-01/executor-agnostic-v1`.
- Baseline SHA (`origin/developer` == `developer`): `fdc58ab2b9f7776296353ad99794d2df0627864c`.
- Timestamp (ISO-8601): `2026-06-20T13:22:26+07:00`.
- Тип: docs-only, methodology-hardening. PR: [#161](https://github.com/MaximKolomeets/agent-system-development/pull/161) — open, в `developer` (мерж выполняет человек).
- Head SHA work-ветки (commit задачи): `a173f59c7caca0b89388122b63975f72d7e12fab`.

## Что сделано

### 1. Role-agnostic заголовок (канон — `templates/TASK_HEADER_COMMON.md`)

- Mandatory header переведён на role-agnostic форму: `Задача для <роль>: <task-id>`, блок `Рекомендуемый режим исполнения` со строками `Роль:`, `Исполнитель: на усмотрение архитектора`, `Reasoning effort: <низкий | средний | высокий>`, `Запуск`, `Режим`, `Почему`. Убрана строка `Модель: <model recommendation>` и ссылка на `<engine-name>` в названии блока. Имён инструментов/моделей в шаблоне нет.
- Раздел `## Recommended Engine Mode` переименован в `## Рекомендуемый режим исполнения` и переписан под role-agnostic поля.
- Добавлено пояснение эквивалентности `<роль>` ↔ `<agent-name>` (manifest-правило `mandatory_engine_task_header`), чтобы не было противоречия с manifest.
- `DEVELOPMENT_TASK_TEMPLATE.md` и `AGENT_RESEARCH_TASK_TEMPLATE.md` выровнены: bullet «Общий header» теперь ссылается на `<роль>` и role-agnostic блок, добавлены пункты «Передача» и «Source-reminder».

### 2. Правило «Передача» (канон — `templates/TASK_HEADER_COMMON.md` → «Передача»)

- Новый канонический раздел: final report и RESULT любой задачи заканчиваются блоком `Следующий: <роль> — <что делает>` (или `Следующий: нет — <причина>`).
- Wired по ссылке в: `DEVELOPMENT_TASK_TEMPLATE.md` (Ожидаемый отчёт), `AGENT_RESEARCH_TASK_TEMPLATE.md` (Expected output), `CODE_REVIEW_TASK_TEMPLATE.md` (Final report), `AGENTS.md` (bullet), checklist в `TASK_HEADER_COMMON`.

### 3. Правило «Source-reminder» (канон — `templates/TASK_HEADER_COMMON.md` → «Source-reminder»)

- Новый канонический раздел: при изменении методологии/канонов — (а) обновить source-снапшот по `source/README.md`, если файлы входят; (б) в RESULT и «Передаче» строка «Обновить Source-снапшот в проектах: …» из `SOURCE_CONSUMERS.md`; иначе «не применимо».
- Wired по ссылке в DEVELOPMENT/RESEARCH/CODE_REVIEW шаблонах, `AGENTS.md`, checklist.

### 4. `CODE_REVIEW_TASK_TEMPLATE.md`

- Reviewer-заголовок role-agnostic (`Роль: reviewer (…)`, `Исполнитель: на усмотрение архитектора`, `Reasoning effort`); убрана строка `Модель:`.
- Поле `Engine` помечено опциональным/постфактумным («исполнителя назначает архитектор»).
- Новый раздел «Конвенция: review PR на GitHub по head SHA» с `gh pr view/diff` и pin к `headRefOid`; reviewed head SHA фиксируется в report/RESULT.
- Final report дополнен пунктами `reviewed head SHA`, «Передача» и «Source-reminder».
- Scrub: `Codex/Engine` → `исполнителя (engine)` (2 места).

### 5. `ROLE_MODEL.md`

- Новый раздел «Роль vs исполнитель»: роль (функция в методологии, vendor-neutral) vs исполнитель (tool/model/human, назначает архитектор; в header — `Исполнитель: на усмотрение архитектора`).
- Добавлены роли `infra` (Docker/CI/деплой; тугой whitelist; без `.env`/секретов; `work/infra/<task>`) и `source-steward` (кросс-проектная синхронизация Source; ведёт `SOURCE_CONSUMERS.md`; применяет «Source-reminder»).
- Scrub: `CHATGPT_*` → `<INTERFACE>_*`; `engine может быть Codex, Claude Code…` → role-agnostic; `Codex/Engine` → `исполнителя (engine)`; `вместе с ChatGPT` → `вместе с архитектором (orchestrator)`.

### 6. `SOURCE_CONSUMERS.md` (новый файл)

- Реестр downstream-потребителей Source-снапшота, привязанный к правилу «Source-reminder» и роли `source-steward`.
- Засеяна запись `verification` (github.com/MaximKolomeets/verification).

### 7. `AGENTS.md`

- Scrub актор-имени инструмента `ChatGPT` → роль `Orchestrator` (строки про task-file-only commit, operating contract, GitHub state, `.env`/main, sync, copy/paste-блок).
- Scrub `Codex/Engine` → `исполнителя (engine)`.
- Добавлены 3 bullet-а по ссылке на новые каноны (role-agnostic header, «Передача», «Source-reminder») — без дублирования прозой.
- Сохранены legitimately строки-запреты, перечисляющие vendor-имена (AGENTS.md:38 `claude/*` и т. д., AGENTS.md:44 «не должны содержать Codex, Claude, Gemini, Copilot…») — это формулировка самого запрета, а не designation исполнителя.

## Каноны и ссылки

| Канон | Файл / раздел | Кто ссылается |
|---|---|---|
| Role-agnostic header / «Роль vs исполнитель» | `templates/TASK_HEADER_COMMON.md`; `ROLE_MODEL.md` → «Роль vs исполнитель» | DEVELOPMENT/RESEARCH/CODE_REVIEW шаблоны, `AGENTS.md` |
| «Передача» (handoff) | `templates/TASK_HEADER_COMMON.md` → «Передача» | DEVELOPMENT/RESEARCH/CODE_REVIEW шаблоны, `AGENTS.md` |
| «Source-reminder» | `templates/TASK_HEADER_COMMON.md` → «Source-reminder» | DEVELOPMENT/RESEARCH/CODE_REVIEW шаблоны, `AGENTS.md`, `SOURCE_CONSUMERS.md`, `ROLE_MODEL.md` (source-steward) |
| Реестр потребителей Source | `SOURCE_CONSUMERS.md` | «Source-reminder», роль `source-steward` |
| Роли infra / source-steward | `ROLE_MODEL.md` | `AGENTS.md`, `SOURCE_CONSUMERS.md` |

## Source-снапшот

- Изменяемые шаблоны **не имеют** verbatim-копии в `docs/agent-system/source/` — там только навигационный индекс (`SOURCE_agent_system_index.md`) и requirements-снапшот, без копий тел шаблонов.
- В `ADOPTION_TRANSFER_MANIFEST.yml` шаблоны покрыты wildcard `docs/agent-system/templates/**` (категория `requires_target_adaptation`) — контентных копий нет, обновлять нечего.
- Вывод: в этой задаче обновление файлов в `source/` не требуется. Source of truth — GitHub-файлы; снапшоты downstream обновляются у потребителей.
- **Source-reminder (downstream): Обновить Source-снапшот в проектах: verification.**

## Scrub-находки вне whitelist (для следующей задачи, НЕ правились)

### A. Не-role-agnostic header (`Рекомендуемый режим <engine-name>` + `Модель: <model recommendation>`) — выровнять под канон TASK_HEADER_COMMON:
- `README.md:139,142`
- `docs/agent-system/ADOPTION_GUIDE.md:29,32`
- `docs/agent-system/ENGINE_ENTRYPOINT.md:93,96`
- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md:16,19`
- `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md:218,221`
- `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md:170`
- `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md:8,11,21`
- `docs/agent-system/templates/ADOPTION_PROMPT.md:20,23,77,80`
- `docs/agent-system/templates/CHATGPT_RESPONSE_TEMPLATE.md:20`
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md:12` (`engine=<engine-name>`)

### B. Tool-named файлы (filename содержит vendor/tool name; rename вне whitelist):
- `docs/agent-system/CHATGPT_OPERATING_CONTRACT.md` (ссылается `AGENTS.md:62`)
- `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md`
- `docs/agent-system/templates/CHATGPT_RESPONSE_TEMPLATE.md`
- `docs/agent-system/CLAUDE_PROJECT_OPERATING_LAYER.md`

### C. Актор-имя инструмента (`ChatGPT`/`Codex`/`Claude Code`) вместо роли — привести к роли orchestrator/engine (non-journal, non-whitelist):
README.md, ADOPTION_GUIDE.md, CHATGPT_OPERATING_CONTRACT.md, CHATGPT_RESPONSE_STANDARD.md, CODE_REVIEW_WORKFLOW.md, CURRENT_STATE.md, DECISION_LOG.md, DOWNSTREAM_ADAPTATION_CHECKLIST.md, ENGINE_ENTRYPOINT.md, LANGUAGE_POLICY.md, METHODOLOGY_FEEDBACK_LOOP.md, NEW_PROJECT_ONBOARDING_GUIDE.md, OPERATIONAL_FAST_LANE.md, PR_WORKFLOW.md, RELEASE_READINESS.md, STAGE_2_COMPLETION_CHECKLIST.md, TASK_FILE_HANDOFF_CONTRACT.md, WORKFLOW.md, agents/docs-maintainer-01/CURRENT_STATE_SUMMARY.md, agents/docs-maintainer-01/DOC_SYNC_REPORT.md, source/SOURCE_agent_system_index.md, templates/ADOPTION_PROMPT.md, templates/CHATGPT_RESPONSE_TEMPLATE.md, templates/CODE_REVIEW_REPORT_TEMPLATE.md, templates/NEW_PROJECT_PROMPT.md.

### D. Manifest alignment (вне whitelist):
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` правило `mandatory_engine_task_header` (строки ~149-152) описывает старую форму шапки «Задача для <agent-name> + блок рекомендуемого режима»; выровнять формулировку под `<роль>` / role-agnostic. Рассмотреть добавление `docs/agent-system/SOURCE_CONSUMERS.md` в `categories.generic.files`.

### E. Append-only история (НЕ findings для правки):
journal TASK-файлы (`TASK-0002/0003/0010/0011/0012/0013/0014/0015/0018/0019/0020` и др.) содержат литералы `Codex/Claude/GPT-5/Claude Opus/Claude Sonnet` — append-only история, не трогать.

## Проверки

- `git diff --name-only` — только whitelist + журнал (см. INDEX/коммит).
- `git diff --check` — без whitespace-ошибок.
- Branch guard перед commit: HEAD == `work/docs-maintainer-01/executor-agnostic-v1`.
- Scrub whitelist: остаточные vendor-имена только в строках-запретах `AGENTS.md:38,44` (формулировка запрета) — корректно.
- Дублирования правил прозой нет: каноны в `TASK_HEADER_COMMON`/`ROLE_MODEL`, остальные файлы ссылаются.

## Передача

- Сделано: methodology executor-agnostic — role-agnostic шаблоны (без имён инструментов), каноны «Передача» и «Source-reminder» в `TASK_HEADER_COMMON`, роли `infra`/`source-steward` в `ROLE_MODEL`, заведён `SOURCE_CONSUMERS.md` (seed `verification`), scrub vendor-имён в whitelist. PR [#161](https://github.com/MaximKolomeets/agent-system-development/pull/161), head SHA `a173f59c7caca0b89388122b63975f72d7e12fab`.
- Следующий: reviewer — review PR #161 по новому role-agnostic review-шаблону (`gh pr view/diff` по head SHA), особое внимание findings A–D как кандидатам на отдельную follow-up задачу.
- Обновить Source-снапшот в проектах: verification.
- Tool-name находки вне whitelist: см. разделы A–D выше (не правились; для follow-up задачи).
