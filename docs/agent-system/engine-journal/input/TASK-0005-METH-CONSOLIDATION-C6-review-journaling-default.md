# TASK-0005-METH-CONSOLIDATION-C6-review-journaling-default

Дословная копия входной задачи METH-CONSOLIDATION-C6 (review-journaling default).

---

# Задача для docs-maintainer-01: METH-CONSOLIDATION-C6 (review-journaling default)

## Рекомендуемый режим engine
Запуск: Local only. Рекомендуемый engine: Claude Code.
Reasoning: Medium. Режим: Agent, строгий allowed-files whitelist.
Почему: точечный docs-фикс дефолта + обязательное журналирование.

## Цель
Реализовать PR-C6 из плана: сменить дефолт review-задач с «chat-only» на «всегда журналировать TASK+RESULT» (чат — в дополнение, не вместо). Объём брать как авторитетный из RESULT-0004 (раздел про PR-C6); этот блок — рамка исполнения.

## Контекст
Источник истины по scope — journal RESULT-0004 (METH-CONSOLIDATION-PLAN-01), локально в репозитории. task-id: METH-CONSOLIDATION-C6.

## Repository / каталог
MaximKolomeets/agent-system-development
C:\neural\repos\agent-system-development

## Ветки
- base: developer
- work: work/docs-maintainer-01/review-journaling-default

## Авторитетный scope (прочитать первым)
docs/agent-system/engine-journal/output/RESULT-0004-*.md — секция PR-C6. Исполнять как там определено. Если scope в RESULT-0004 расходится с этим блоком по сути — следовать RESULT-0004 и отметить расхождение в своём RESULT.

## Allowed files (менять ТОЛЬКО эти)
docs/agent-system/CODE_REVIEW_WORKFLOW.md
docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md
+ журнал: input/TASK-<next>, output/RESULT-<next>, INDEX.md (next по INDEX, ожидаемо 0005)

## Read-only context (читать, не менять)
RESULT-0004; AGENTS.md; ENGINE_JOURNAL_CONTRACT.md

## Суть правки
- review-only / plan-only задачи ОБЯЗАНЫ писать TASK+RESULT в engine-journal (append-only, sequence, timestamp), как и file-changing задачи;
- чат-отчёт — дополнительно, не замена журналу;
- убрать/переформулировать дефолты «report persistence: chat-only by default» и «PR creation: no» так, чтобы journal-only docs-PR для записи review был нормой;
- формулировки согласовать с ENGINE_JOURNAL_CONTRACT.md (его НЕ менять).

## Forbidden
- файлы вне whitelist; если «chat-only» дефолт обнаружится ещё и в AGENTS.md или другом файле вне whitelist — НЕ менять молча: STOP и сообщить (расширение scope — отдельным решением);
- .env; main/developer напрямую; Docker; ввод credentials; редактирование RESULT прошлых задач.

## Preflight (после merge closure-0004)
cd C:\neural\repos\agent-system-development
git status --short --untracked-files=all
git fetch --all --prune
git switch developer
git pull --ff-only origin developer
git rev-parse developer && git rev-parse origin/developer
git switch -c work/docs-maintainer-01/review-journaling-default

## Journal (обязательно)
TASK-<next>: дословная копия этой задачи.
RESULT-<next>: что изменено, baseline SHA, timestamp ISO-8601, task-id, ссылка на PR-C6 в RESULT-0004.
INDEX: запись <next> в хронологию. Russian-first, без placeholders, append-only.

## Проверки
git diff --name-only   # только whitelisted + журнал
git diff --check
git grep -n "chat-only" -- docs/agent-system/CODE_REVIEW_WORKFLOW.md docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md
Вручную: дефолт теперь «journal-always»; противоречий с ENGINE_JOURNAL_CONTRACT нет.

## Commit / push / PR (контур gh)
commit: docs(agent-system): review tasks always journal TASK+RESULT (C6)
git push -u origin work/docs-maintainer-01/review-journaling-default
gh доступен → gh pr create base=developer; gh недоступен → вернуть URL pull/new пользователю, пометить «PR создаёт пользователь». Не зацикливаться.
push требует credentials → STOP, не вводить.

## Definition of Done
- изменены только whitelisted + журнал; diff --check чист;
- review-дефолт = journal-always во всех трёх файлах;
- TASK/RESULT/INDEX записаны (sequence, timestamp, baseline SHA), без placeholders;
- ветка запушена; PR создан или переданы URL/команды;
- RESULT содержит фактический commit SHA и PR URL (или «PR создаёт пользователь»);
- Russian-first.

## STOP-условия
developer != origin/developer; правка вне whitelist (вкл. «chat-only» в AGENTS.md); RESULT-0004 недоступен; конфликт с ENGINE_JOURNAL_CONTRACT; push требует credentials; найден секрет (не печатать).
