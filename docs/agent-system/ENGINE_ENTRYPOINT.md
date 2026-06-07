# ENGINE_ENTRYPOINT

## Назначение

Этот документ является входной точкой для `engine`, который применяет `agent-system-development` как template repository для target repository.

Entrypoint нужен, чтобы короткий prompt пользователя был достаточен для безопасного старта. `engine` должен сам найти методологию template repository, проверить текущий target repository и начать не с переноса файлов, а с adoption audit.

## Короткий prompt

Пользователь может дать короткий prompt:

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development
```

Если `engine` получил такой prompt, он должен:

1. определить текущий target repository;
2. прочитать локальные инструкции target repository;
3. найти в template repository этот entrypoint и `ENGINE_SELF_DISCOVERY_CONTRACT.md`;
4. выполнить safety gate;
5. подготовить adoption audit;
6. только после этого планировать bootstrap PR.

## Обязательный порядок

1. Repository self-discovery.
2. Local instructions discovery.
3. Template repository discovery.
4. Safety gate.
5. Adoption audit.
6. Only then planned bootstrap PRs.

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
- `TARGET_REPOSITORY_ADOPTION_GUIDE.md`;
- `STAGE_2_COMPLETION_CHECKLIST.md`;
- `templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`.

Template repository является методологической основой, а не источником для слепого копирования.

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
- какие изменения можно предложить первым bootstrap PR;
- какие риски требуют решения пользователя.

Adoption audit не должен переносить private data в public methodology repository.

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
