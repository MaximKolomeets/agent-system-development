# ROLE_MODEL

## Vendor-neutral boundaries

Роли описывают ответственность, а не конкретный vendor/tool. Название роли, branch namespace, task id, report filename и journal entry не должны содержать vendor/tool names.

`engine` - это конкретный инструмент или исполнитель, который выполняет задачу. Engine name указывается в task header отдельно и не становится role name.

Документы adapter layer могут называться по конкретному интерфейсу, например `<INTERFACE>_*`, но такие файлы описывают применение роли через отдельный tool/interface и не меняют canonical role model.

## Роль vs исполнитель

Методология различает два понятия:

- **Роль** — функция ответственности в методологии (`orchestrator`, `engine`/executor-роль, `reviewer`, `dev-implementer-01`, `docs-maintainer-01`, `infra`, `source-steward` и т. д.). Роль vendor-neutral и задаёт scope, allowed/forbidden files, journal- и PR-обязанности.
- **Исполнитель** — конкретный tool/model/human, который выполняет роль. Исполнителя назначает архитектор; в task header исполнитель не фиксируется (`Исполнитель: на усмотрение архитектора`). Смена исполнителя не меняет роль и её границы.

Канон role-agnostic task header (`Reasoning effort`, правила «Передача» и «Source-reminder») — `docs/agent-system/templates/TASK_HEADER_COMMON.md`.

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
- исполнителя назначает архитектор: это может быть LLM-агент, локальная модель, человек или другой инструмент — выбор исполнителя не меняет роль;
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

## infra

- Docker, CI/CD, деплой, runtime-конфигурация, workflow-файлы;
- работает по тугому whitelist: каждое изменение Docker/CI/деплой ограничено явным allowed-files списком;
- не читает и не коммитит `.env`, секреты, credentials, tokens (канон forbidden — `AGENTS.md`);
- работает только в `work/infra/<task>`, не мержит и не пушит `main`/`developer` напрямую;
- ведёт TASK/RESULT/INDEX и открывает PR; final report заканчивается блоком «Передача».

## source-steward

- кросс-проектная синхронизация Source-снапшота методологии между downstream-потребителями;
- ведёт реестр потребителей `docs/agent-system/SOURCE_CONSUMERS.md`;
- применяет правило «Source-reminder» (канон — `docs/agent-system/templates/TASK_HEADER_COMMON.md`): после изменения методологии/канонов обновляет source-снапшот и оповещает потребителей из реестра;
- не меняет downstream production code; синхронизация идёт через PR в каждом потребителе по их branch-модели;
- source of truth — GitHub-файлы methodology repository; снапшоты — derived context (канон — `docs/agent-system/source/README.md`).

## Reviewer role boundary

- `code-reviewer-01`, `qa-reviewer-01` и `security-reviewer-01` не implement fixes по умолчанию.
- Reviewer roles создают reports, findings и proposed next PRs.
- Review-задачи всегда журналируют TASK/RESULT/INDEX и открывают docs-only PR с journal artifacts (`Journal trace: always`).
- Исправления выполняет `dev-implementer-01` или другая явно назначенная implementation role в отдельной задаче, ветке и PR.
- Engine name указывается отдельно от role name и не попадает в branch namespace.
- Reviewer role проверяет PR, branch, commit, diff или набор файлов.
- Reviewer role не запускает исполнителя (engine), не меняет очередь исполнителя и не формулирует себе implementation task.
- Решение о превращении findings в задачу принимает пользователь вместе с архитектором (orchestrator).
- Тело review report по умолчанию возвращается в чат; сохранение report-body в repository требует `Report delivery: repository` или `chat+repository` и не отменяет обязательный journal trace.
- Допустимые режимы review-задачи: `review-only`, `docs-only`, `fix-allowed`. Режим `fix-allowed` требует явного scope, allowed files, forbidden files и отдельного разрешения пользователя.
