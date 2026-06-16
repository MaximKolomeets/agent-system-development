# ROLE_MODEL

## Vendor-neutral boundaries

Роли описывают ответственность, а не конкретный vendor/tool. Название роли, branch namespace, task id, report filename и journal entry не должны содержать vendor/tool names.

`engine` - это конкретный инструмент или исполнитель, который выполняет задачу. Engine name указывается в task header отдельно и не становится role name.

Документы adapter layer могут называться по конкретному интерфейсу, например `CHATGPT_*`, но такие файлы описывают применение роли через отдельный tool/interface и не меняют canonical role model.

## Orchestrator

- помогает пользователю выбрать режим работы: Operational Fast Lane, Engine-блок, Task File Handoff или review-only;
- проверяет GitHub/local baseline, если connector или локальная среда доступны;
- формирует self-contained задачу для `engine`;
- не выполняет repository file changes напрямую, если задача требует engine workflow, journal и PR;
- не подменяет решение пользователя о merge, scope expansion или превращении findings в implementation task.

В solo-operator режиме orchestrator может быть тем же человеком или тем же chat interface, который ведет задачу, но обязан явно фиксировать safety gates.

## Engine

- выполняет конкретную задачу в repository в разрешенном scope;
- работает в указанной branch model и не меняет `main`/`developer` напрямую;
- создает или обновляет TASK/RESULT/INDEX, если задача меняет repository files или создает PR;
- пишет final report на русском языке;
- не расширяет scope и не придумывает недостающие PR/merge facts.

Engine может быть любым tool/human executor. Замена engine не меняет роль агента.

## Границы веток и main

Два governance-правила являются обязательными для всех ролей. Канон — `docs/agent-system/BRANCH_POLICY.md`:

- агент никогда не мержит и не пушит в `main`; `main` обновляется только через release-PR, который мержит человек-архитектор (канон: BRANCH_POLICY → «Обновление main»);
- агент работает только в своих ветках `work/<role>/<task>` и не трогает ветки других агентов; передача — через merged PR в `developer` (канон: BRANCH_POLICY → «Изоляция веток агентов»).

## Reviewer

- проверяет PR, branch, commit, diff или набор файлов;
- работает review-only по умолчанию;
- пишет findings, risks, missing tests и proposed next PRs;
- не исправляет production files, runtime, Docker, CI, dependencies или architecture docs без отдельного `fix-allowed` scope;
- не назначает сам себе implementation task.

External reviewer не заменяет orchestrator и не принимает решение пользователя о merge/scope.

## Режимы применения ролей

### Lightweight solo-operator mode

- один оператор может последовательно выполнять функции orchestrator, engine и reviewer;
- роли используются как checklist ответственности, а не как требование запускать разных исполнителей;
- для простых read-only/status/cleanup действий применяется Operational Fast Lane;
- для file-changing tasks сохраняются рабочая ветка, PR, journal finalization и локальный sync block;
- допускается компактный review, если риск низкий и scope docs-only, но reviewer boundary остается явно проверенным.

### Multi-agent governed mode

- роли выполняют разные агенты, люди или tools;
- одна задача = одна ветка = один PR;
- review findings превращаются в implementation work только через отдельное решение пользователя;
- reports, TASK/RESULT/INDEX и PR body должны быть воспроизводимыми и Russian-first;
- branch namespace остается `work/<role>/<task>`.

## dev-implementer-01

- исполнитель задач разработки;
- engine может быть Codex, Claude Code, локальная LLM, человек или другой инструмент;
- не принимает архитектурные решения самостоятельно.

## solution-architect-01

- архитектура;
- декомпозиция крупных задач;
- предложения;
- риски;
- не запускает `dev-implementer-01` напрямую.

## qa-reviewer-01

- проверка качества;
- тесты;
- регрессии;
- review reports;
- не исправляет код без отдельного задания.

## code-reviewer-01

- общий code review / external review / consulting review;
- анализирует architecture, entry points, tests, dependencies, docs и риски;
- работает review-only by default;
- создает review report и proposed next PRs;
- не исправляет найденные проблемы без отдельной implementation task.

## security-reviewer-01

- секреты;
- forbidden files;
- `.env` policy;
- branch/ruleset recommendations;
- работает review-only by default;
- создает review report и proposed next PRs;
- не исправляет найденные проблемы без отдельной implementation task.

## docs-maintainer-01

- актуальность документации;
- `CURRENT_STATE`;
- `NEXT_STEPS`;
- Source summaries;
- prompts for next chat.

## Reviewer role boundary

- `code-reviewer-01`, `qa-reviewer-01` и `security-reviewer-01` не implement fixes по умолчанию.
- Reviewer roles создают reports, findings и proposed next PRs.
- Исправления выполняет `dev-implementer-01` или другая явно назначенная implementation role в отдельной задаче, ветке и PR.
- Engine name указывается отдельно от role name и не попадает в branch namespace.
- Reviewer role проверяет PR, branch, commit, diff или набор файлов.
- Reviewer role не запускает Codex/Engine, не меняет очередь исполнителя и не формулирует себе implementation task.
- Решение о превращении findings в задачу принимает пользователь вместе с ChatGPT.
- Review report по умолчанию возвращается в чат; сохранение report в repository требует отдельного docs-only разрешения.
- Допустимые режимы review-задачи: `review-only`, `docs-only`, `fix-allowed`. Режим `fix-allowed` требует явного scope, allowed files, forbidden files и отдельного разрешения пользователя.
