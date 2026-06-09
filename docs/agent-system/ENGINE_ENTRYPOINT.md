# ENGINE_ENTRYPOINT

## Назначение

Этот документ является входной точкой для `engine`, который применяет `agent-system-development` как template repository для target repository.

Entrypoint нужен, чтобы короткий prompt пользователя был достаточен для безопасного старта. `engine` должен сам найти методологию template repository, проверить текущий target repository и начать не с переноса файлов, а с adoption audit.

`agent-system-development` является reusable methodology/template repository. Он не является центральным репозиторием управления агентами target repository и не хранит рабочие ветки, worktree, отчеты, Pull Request, project-specific state, исходный код или секреты downstream-проектов.

После adoption все project-specific артефакты ведутся в target repository. В `agent-system-development` возвращаются только универсальные улучшения методологии через отдельные methodology PR.

## Обязательная шапка задачи

Полная задача для `engine` должна быть на русском языке и начинаться с шапки:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

`<agent-name>` - role-based имя агента, которому назначена задача. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Короткий prompt

Пользователь может дать короткий prompt:

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development
```

Если `engine` получил такой prompt, он должен:

1. определить текущий target repository;
2. прочитать локальные инструкции target repository;
3. найти в template repository этот entrypoint, `ENGINE_SELF_DISCOVERY_CONTRACT.md`, `ADOPTION_GUIDE.md`, `ADOPTION_TRANSFER_MANIFEST.yml` и `DOWNSTREAM_ADAPTATION_CHECKLIST.md`;
4. выбрать adoption mode;
5. выполнить safety gate;
6. подготовить adoption audit;
7. только после этого планировать bootstrap PR.

## Обязательный порядок

1. Repository self-discovery.
2. Local instructions discovery.
3. Template repository discovery.
4. Adoption mode selection.
5. Safety gate.
6. Adoption audit.
7. Only then planned bootstrap PRs.

## Repository self-discovery

До любых изменений `engine` обязан выполнить repository self-discovery по контракту:

```text
docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md
```

Self-discovery подтверждает:

- где находится текущий repository;
- какой remote используется;
- какая ветка активна;
- чистый ли working tree;
- какие tracked files уже есть;
- нет ли запрещенных tracked paths;
- нет ли признаков риска секретов.

## Local instructions discovery

`engine` должен прочитать локальные инструкции target repository до применения шаблона. Если в target repository есть `AGENTS.md`, `README.md` или локальные документы в `docs/agent-system/`, они имеют значение для adoption audit.

Локальные инструкции нельзя механически перетирать документами из template repository. Если инструкции конфликтуют, `engine` должен зафиксировать конфликт в audit и запросить решение пользователя.

## Template repository discovery

После чтения локального target repository `engine` читает template repository и находит:

- `ENGINE_ENTRYPOINT.md`;
- `ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- `ADOPTION_GUIDE.md`;
- `ADOPTION_TRANSFER_MANIFEST.yml`;
- `DOWNSTREAM_ADAPTATION_CHECKLIST.md`;
- `TARGET_REPOSITORY_ADOPTION_GUIDE.md`;
- `TARGET_PROJECT_GOVERNANCE_PACK.md`;
- `STAGE_2_COMPLETION_CHECKLIST.md`;
- `templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`;
- `templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`.

Template repository является методологической основой, а не источником для слепого копирования.

## Adoption mode selection

Перед изменениями `engine` выбирает режим по `ADOPTION_GUIDE.md`:

- `audit-only` - первый безопасный dry run, результатом является только `docs/agent-system/ADOPTION_AUDIT.md`;
- `docs-only adoption` - перенос адаптированной документационной системы и governance pack без runtime changes;
- `runtime adoption` - отдельный runtime scope только после архитектурного решения target repository.

`ADOPTION_TRANSFER_MANIFEST.yml` используется для проверки, какие файлы являются generic, какие отражают template repository state и какие требуют target adaptation. `DOWNSTREAM_ADAPTATION_CHECKLIST.md` используется как review checklist перед docs-only adoption.

## Safety gate

До adoption audit и до любых изменений `engine` проверяет:

- текущий repository соответствует задаче;
- remote соответствует ожидаемому target repository;
- working tree чистый или пользователь явно разрешил работать с текущими изменениями;
- нет forbidden tracked paths;
- sensitive grep выполнен только filename-only;
- нет явного риска секретов;
- есть разрешение пользователя на изменение файлов.

Если safety gate не пройден, `engine` пишет `STOP`, объясняет причину и не меняет файлы.

## Adoption audit

Первым результатом в target repository должен быть adoption audit. Он описывает:

- текущую структуру repository;
- локальные инструкции и ограничения;
- branch policy и состояние working tree;
- public/private visibility, если она известна из локального контекста;
- какие документы template repository применимы;
- какие документы требуют адаптации;
- какие файлы по transfer manifest нельзя копировать verbatim;
- какие изменения можно предложить первым bootstrap PR;
- какие риски требуют решения пользователя.

Adoption audit не должен переносить private data в public methodology repository.

## Methodology feedback

После adoption audit или target repository dry run `engine` должен предложить, что улучшить в template repository для следующей интеграции.

Feedback должен быть нейтральным и не должен раскрывать private data target repository. Он может включать:

- missing template docs;
- manual steps to automate;
- safety gaps;
- conflicts with local instructions;
- suggested methodology PRs.

Methodology feedback не должен автоматически менять methodology repository. Любое улучшение `agent-system-development` выполняется отдельной задачей, отдельной веткой и отдельным PR.

## Запреты

- Не начинать изменения до repository self-discovery.
- Не механически перетирать локальные инструкции target repository.
- Не переносить private data, credentials, `.env`, клиентские данные, персональные данные или внутренние кодовые имена в public methodology repository.
- Не читать `.env`.
- Не печатать matching lines sensitive grep.
- Не начинать bootstrap PR, пока adoption audit не завершен.

## STOP rule

Если текущий repository не соответствует задаче, `engine` должен написать:

```text
STOP
```

После `STOP` нужно кратко указать причину и не менять файлы.
