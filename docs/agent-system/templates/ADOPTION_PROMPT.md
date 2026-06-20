# ADOPTION_PROMPT

Канонический adoption prompt для запуска внедрения методологии `agent-system-development` в target repository.

Файл объединяет короткий, безопасный короткий и полный canonical copy/paste варианты. Прежний файл `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен как redirect-заглушка для внешних bookmark и продолжает вести сюда; `SHORT_TARGET_ADOPTION_PROMPT.md` удалён (METH-BACKLOG-POLISH).

## Когда какой вариант использовать

- **Короткий prompt** — пользователь хочет одной строкой передать ChatGPT/engine, что нужно интегрировать методологию.
- **Безопасный короткий prompt** — то же самое, но с явным safety gate (self-discovery + adoption audit перед изменениями).
- **Полный canonical copy/paste prompt** — пользователь готов вставить большой prompt в новый чат в контексте target repository и получить готовую первую задачу engine в режиме `audit-only`.

## Обязательная шапка задачи

Любой adoption prompt используется после русскоязычной task header:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>
```

`<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

Adoption prompt должен включать Russian-first reminder: все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке; English допустим только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names.

Adoption prompt должен требовать Post-merge Journal Closure: после merge/release/sync target `RESULT` и `INDEX` фиксируют status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`.

Adoption prompt должен требовать `methodology_reference`: repository, source branch, source commit SHA, checked_at и reference_type. Канон спецификации — `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference».

## Короткий prompt

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development. Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пиши на русском языке; English допускается только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names. Зафиксируй methodology_reference с source commit SHA. После merge/release/sync закрой target RESULT/INDEX по Post-merge Journal Closure.
```

## Безопасный короткий prompt

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development. Сначала выполни repository self-discovery и adoption audit, без изменения кода и без запуска Docker. Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пиши на русском языке; English допускается только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names. Зафиксируй methodology_reference с source commit SHA. После merge/release/sync закрой target RESULT/INDEX по Post-merge Journal Closure. В final report добавь Methodology feedback: что улучшить в template repository для следующей интеграции, без private data.
```

## Полный canonical copy/paste prompt

Этот prompt пользователь копирует и вставляет в новый чат, открытый в контексте target repository. Prompt не запускает полный перенос шаблона — он просит ChatGPT подготовить первую безопасную задачу для engine в режиме `audit-only`.

```text
Продолжаем внедрение агентской методологии в этот проект.

Целевой репозиторий:

<ВСТАВИТЬ_URL_TARGET_REPOSITORY>

Шаблонный methodology repository:

https://github.com/MaximKolomeets/agent-system-development

Твоя задача в этом чате:

1. Изучи target repository.
2. Изучи актуальный `agent-system-development` как reusable methodology/template repository.
3. Не вноси изменения в файлы сам.
4. Сначала подготовь задачу для engine.
5. Задача должна быть на русском языке и начинаться с обязательной шапки:
6. Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах должны быть на русском языке. Английский допустим только для команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и code identifiers.
7. Если target instructions конфликтуют с Russian-first policy, включи в Engine-задачу STOP-условие и требование запросить решение пользователя.
8. Включи в Engine-задачу Post-merge Journal Closure: после merge/release/sync RESULT/INDEX должны фиксировать status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`.

Задача для <agent-name>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>

Перед формированием задачи:

1. Обратись к актуальному `agent-system-development`.
2. Проверь, что используется текущая версия methodology repository.
3. Если GitHub, connector или локальная синхронизация недоступны, явно напиши это пользователю.
4. Включи в задачу engine preflight для проверки и синхронизации methodology repository.
5. Требуй, чтобы engine зафиксировал `methodology_reference` с repository, source branch, source commit SHA, checked_at и reference_type.

Формат ответа ChatGPT:

1. Все данные для engine выведи в одном самодостаточном блоке `Блок для Engine — копировать целиком`.
2. Не выноси из Engine-блока команды, allowed files, forbidden files, проверки, STOP-условия и формат отчета.
3. Ручные terminal-шаги выводи отдельно только если они предназначены пользователю, а не engine.
4. Не смешивай engine prompt и manual commands.
5. Если нужна доработка `agent-system-development`, выведи отдельный самодостаточный copy/paste-блок для engine-разработчика methodology repository.

Главная цель:

Применить в target repository обновленную методологию из `agent-system-development`, но безопасно и поэтапно.

Важно:

`agent-system-development` - это reusable methodology/template repository, а не центральный репозиторий управления downstream-проектом.

Все project-specific ветки, отчеты, PR, state docs, governance docs и рабочее состояние должны создаваться только в target repository.

Private data, secrets, `.env`, client data, private repository URL и internal code names нельзя переносить обратно в public methodology repository.

Сначала нужен не полный перенос шаблона, а безопасная первая задача engine в режиме `audit-only`.

Нужно подготовить задачу engine, которая:

1. Проверит target repository.
2. Выполнит repository self-discovery.
3. Прочитает локальные инструкции target repository.
4. Проверит branch model.
5. Проверит наличие или отсутствие `docs/agent-system/`.
6. Зафиксирует methodology reference:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: <developer или явно заданная branch>
  source_commit: <commit-sha>
  checked_at: <ISO-8601 timestamp>
  reference_type: commit
  notes: <short Russian note>
```

`source_commit` обязателен. Если commit SHA получить нельзя, engine пишет `STOP` или фиксирует audit blocker.
7. Проверит наличие root governance docs:
   - `README.md`
   - `AGENTS.md`
   - `PROJECT_CONSTITUTION.md`
   - `PROJECT_DASHBOARD.md`
   - `ROADMAP.md`
   - `RUNBOOK.md`
   - `DECISIONS.md`
8. Проверит готовность к governance pack:
   - `CURRENT_STATE.md`
   - `NEXT_STEPS.md`
   - `BACKLOG.md`
   - `DECISION_LOG.md`
   - `PROJECT_GUARDRAILS.md`
   - `ENGINE_REGISTRY.md`
9. Проверит готовность к Project Constitution Framework:
   - Project Mission
   - Success Criteria
   - Out Of Scope
   - Architectural Principles
   - Current Strategic Goal
   - Agent Authority Matrix
   - Decision Authority Levels
   - Scope Expansion Control
   - Governance Review Checklist
10. Проверит language consistency governance docs target repository.
11. Проверит Russian-first policy в target `AGENTS.md` или эквивалентных target instructions.
12. Проверит, есть ли в target repository скрипты, workflow или templates без достаточных русских комментариев для нужных строк/блоков.
13. После audit порекомендует привести target docs/templates к Russian-first policy.
14. Создаст только audit artifacts:

docs/agent-system/ADOPTION_AUDIT.md
docs/agent-system/engine-journal/

Engine journal scaffold/templates могут быть созданы или обновлены для target repository, но methodology repository operational history нельзя копировать. Первый audit создает target-specific task/result files и target-specific INDEX entry.

Journal entries не должны оставаться в статусах `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report` после merge.

Если `docs/agent-system/` еще нет, engine может создать только минимальную папку, файл audit и engine journal artifacts для этой audit-задачи.

Запрещено в первой задаче:

- переносить весь template repository;
- менять runtime-код;
- менять Docker;
- менять CI;
- менять services/workers/orchestrator/API;
- менять architecture docs без отдельного решения;
- читать `.env`;
- коммитить `.env`;
- коммитить `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`;
- менять production data;
- добавлять secrets;
- добавлять private data;
- делать full docs-only adoption без audit.
- удалять или перезаписывать task/result files engine journal без решения пользователя.

Задача engine должна использовать безопасный branch mode selection:

1. Определить, это `new empty repository bootstrap` или `existing repository adoption`.
2. Если это `new empty repository bootstrap` и пользователь выбрал стандартный workflow `main -> developer -> work/<role>/*`:
   - проверить наличие `developer`;
   - если `developer` отсутствует, сначала создать `developer` от актуального `main` как явно разрешенный bootstrap-шаг или написать `STOP`, если такого разрешения нет;
   - рабочую ветку создавать только от `developer`;
   - PR направлять только в `developer`;
   - не открывать рабочий PR в `main`.
3. Если это `existing repository adoption`:
   - проверить фактическую branch model target repository;
   - если target repository использует `developer`, `develop`, `main-only flow` или custom flow, адаптировать branch policy под фактическую модель;
   - если branch model неясна или противоречит задаче, написать `STOP` и запросить решение пользователя.
4. Base branch должен быть явно указан в задаче.
5. Если selected branch model = `standard developer workflow`, отсутствие `developer` является blocker или explicit bootstrap branch creation step.
6. Для `standard developer workflow` запрещен `fallback-to-main`.
7. Рабочая ветка должна быть:

work/docs-maintainer-01/<task-id>-adoption-audit

Task id придумай по правилам target repository. Если в проекте нет своей нумерации, предложи нейтральный id вроде:

PR-agent-1a

В задаче engine обязательно указать проверки:

- `git rev-parse --show-toplevel`
- `git remote -v`
- `git branch --show-current`
- `git status --short`
- `git ls-files`
- forbidden tracked paths check
- sensitive grep только filename-only, без вывода matching lines:

git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --

Финальный отчет engine должен содержать:

- repository root;
- remote summary;
- current branch;
- repository lifecycle mode;
- selected branch model;
- developer branch existence;
- fallback-to-main allowed: yes/no with reason;
- выбранная base branch;
- working branch;
- local instructions found;
- methodology reference;
- existing governance docs;
- missing governance docs;
- existing agent-system docs;
- branch model observation;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- Project Constitution readiness;
- Governance Pack readiness;
- Engine Registry readiness;
- language consistency result;
- commenting consistency result;
- Russian-first policy result;
- methodology reference result;
- engine journal task/result files;
- проверка Post-merge Journal Closure;
- recommended docs-only adoption scope;
- stop conditions, если есть;
- Methodology feedback;
- Methodology repository improvement request, если нужна доработка `agent-system-development`;
- next recommended PR.

После анализа target repository выведи мне готовую задачу для engine целиком, чтобы я мог скопировать ее и вставить в окно engine.

В создаваемых или изменяемых скриптах, workflow, config-like files, templates и технических файлах требуй русские комментарии для нужных строк/блоков: что делает строка/блок и зачем он нужен.

Не начинай с полного внедрения. Сначала сформируй только задачу на audit-only adoption.
```

## Как должен действовать engine

`engine` должен сам найти в template repository:

- `docs/agent-system/ENGINE_ENTRYPOINT.md`;
- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- `docs/agent-system/ADOPTION_GUIDE.md` (включая раздел «Пошаговый existing-repo adoption»);
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`;
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`;
- `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`;
- `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`;
- `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`;
- `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`;
- `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`;
- `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md`;
- `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`.

После этого `engine` выполняет repository self-discovery в текущем target repository и читает локальные инструкции.

После выбора adoption mode `engine` должен выбрать соответствующий task template:

- `audit-only` использует `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`;
- `docs-only adoption` использует `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`.

## Первый результат

Первым результатом в target repository должен быть adoption audit.

Без отдельного решения пользователя используется режим `audit-only`, а first PR создает только:

```text
docs/agent-system/ADOPTION_AUDIT.md
```

Adoption audit должен показать:

- текущий repository и ветку;
- локальные инструкции;
- safety gate;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- какие документы template repository применимы;
- какие файлы adoption transfer manifest относит к `template_state_do_not_copy_verbatim` или `requires_target_adaptation`;
- какие governance pack files нужно создать или адаптировать;
- нужен ли `PROJECT_CONSTITUTION.md` и какие mission/strategic goal/authority gaps есть;
- какие изменения можно предложить первым bootstrap PR;
- methodology_reference с source commit SHA.

Первым результатом не должен быть полный перенос всех файлов template repository.

## Ограничения

- Не читать `.env`.
- Не запускать Docker в safe short prompt mode.
- Не менять код до завершения self-discovery и adoption audit.
- Не переносить private data в public methodology repository.
- Не перетирать локальные инструкции target repository.

## Как использовать

1. Открыть новый чат в контексте target repository.
2. Скопировать prompt из подходящего раздела (короткий, безопасный короткий или полный canonical).
3. Для полного варианта заменить `<ВСТАВИТЬ_URL_TARGET_REPOSITORY>` на URL target repository.
4. Вставить prompt в чат.
5. Получить задачу для engine.
6. Запустить engine вручную.
