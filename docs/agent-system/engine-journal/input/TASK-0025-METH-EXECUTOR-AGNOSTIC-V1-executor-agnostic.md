# Задача для docs-maintainer-01: METH-EXECUTOR-AGNOSTIC-V1

## Режим
Роль: docs-maintainer (функция, НЕ инструмент).
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий — затрагивает несколько canon-файлов, нужна консистентность и аккуратный scrub.
Запуск: Local only. Строгий allowed-files whitelist, branch-guard.

## Цель
Сделать методологию executor-agnostic и зашить два сквозных правила (Передача + Source-reminder): привести шаблоны задач/review к role-agnostic форме, добавить роли infra/source-steward, завести реестр потребителей Source.

## Repository / каталог
MaximKolomeets/agent-system-development / C:\neural\repos\agent-system-development

## Ветки
base developer; work work/docs-maintainer-01/executor-agnostic-v1

## Allowed files
docs/agent-system/templates/TASK_HEADER_COMMON.md
docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md
docs/agent-system/templates/AGENT_RESEARCH_TASK_TEMPLATE.md
docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
docs/agent-system/ROLE_MODEL.md
AGENTS.md
docs/agent-system/SOURCE_CONSUMERS.md            (новый файл)
+ source-снапшот этих шаблонов, ЕСЛИ он есть (source/...; см. раздел Source)
+ журнал: input/TASK-<seq>, output/RESULT-<seq>, INDEX.md (seq — NEXT из INDEX, НЕ предсказывать)

## Forbidden
вне whitelist; .env/секреты; прямые правки developer/main; дублирование правил прозой (канон + ссылки).

## Preflight
git fetch --all --prune; git switch developer && git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/executor-agnostic-v1
git rev-parse --abbrev-ref HEAD     # == work/docs-maintainer-01/executor-agnostic-v1, иначе STOP

## Изменения
1. Role-agnostic заголовок (канон в TASK_HEADER_COMMON; DEVELOPMENT/RESEARCH/CODE_REVIEW выравниваются/ссылаются):
   - вместо имени модели — строки «Роль: <функция>», «Исполнитель: на усмотрение архитектора», «Reasoning effort: низкий/средний/высокий»;
   - никаких имён инструментов в шаблонах.
2. Правило «Передача» (канон в TASK_HEADER_COMMON): отчёт по ЛЮБОЙ задаче заканчивается блоком «Следующий: <роль> — <что делает>».
3. Правило «Source-reminder» (канон в TASK_HEADER_COMMON): если задача меняла методологию/каноны — (а) обновить source-снапшот; (б) в RESULT и «Передаче» явно «Обновить Source-снапшот в проектах: <из SOURCE_CONSUMERS>».
4. CODE_REVIEW_TASK_TEMPLATE: role-agnostic reviewer-заголовок + «Передача» + конвенция «ревью PR на GitHub по head SHA через gh».
5. ROLE_MODEL: добавить различение «роль (в методологии) vs исполнитель (назначает архитектор)»; добавить роли `infra` (Docker/CI/деплой; тугой whitelist; без .env) и `source-steward` (кросс-проектная синхронизация Source).
6. SOURCE_CONSUMERS.md (новый): реестр downstream-проектов, которым нужен Source-снапшот; засеять записью `verification` (github.com/MaximKolomeets/verification).
7. Scrub: в whitelisted-файлах заменить любые имена инструментов на роли. Имена инструментов ВНЕ whitelist НЕ править — вынести списком в RESULT как находки для следующей задачи.

Целевая форма шаблонов — как в двух согласованных блоках (executor + reviewer). Канон + ссылки, без дублирования прозой; не противоречить BRANCH_POLICY/WORKFLOW/governance.

## Source-снапшот (ОБЯЗАТЕЛЬНО — методология меняется)
- Проверить, входят ли изменяемые шаблоны в source-снапшот (source/ + ADOPTION_TRANSFER_MANIFEST). Если да — обновить их там же.
- В RESULT и «Передаче»: «Обновить Source-снапшот в проектах: verification».

## Journal
TASK-<seq> (дословно), RESULT-<seq> (что изменено, где каноны/ссылки, scrub-находки вне whitelist, baseline SHA, timestamp ISO-8601), INDEX строка <seq>. Append-only, без placeholders, Russian-first.

## Проверки / Commit / PR
git diff --name-only (только whitelist+журнал); git diff --check
перед commit: git rev-parse --abbrev-ref HEAD == work-ветка (branch-guard)
commit: docs(agent-system): executor-agnostic templates + handoff/source rules + roles
push work-ветку; открыть PR в developer.

## Передача (ОБЯЗАТЕЛЬНО в конце отчёта)
- что сделано + № PR + head SHA;
- «Следующий: reviewer — review PR #NN по новому role-agnostic review-шаблону»;
- «Обновить Source-снапшот в проектах: verification»;
- список tool-name находок вне whitelist (если есть).

## DoD / STOP
DoD: шаблоны role-agnostic (без имён инструментов); правила «Передача» и «Source-reminder» в каноне; роли infra/source-steward в ROLE_MODEL; SOURCE_CONSUMERS заведён; только whitelist+журнал; diff чист; branch-guard; PR открыт; «Передача» заполнена.
STOP: HEAD не work-ветка; правка вне whitelist; противоречие с governance/WORKFLOW; нужно тронуть файл вне whitelist (вынести в находки, не править); push требует credentials.
