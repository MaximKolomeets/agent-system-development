# SHORT_TARGET_ADOPTION_PROMPT

## Короткий prompt

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development
```

## Безопасный короткий prompt

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development. Сначала выполни repository self-discovery и adoption audit, без изменения кода и без запуска Docker. В final report добавь Methodology feedback: что улучшить в template repository для следующей интеграции, без private data.
```

## Как должен действовать engine

`engine` должен сам найти в template repository:

- `docs/agent-system/ENGINE_ENTRYPOINT.md`;
- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md`;
- `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`.

После этого `engine` выполняет repository self-discovery в текущем target repository и читает локальные инструкции.

## Первый результат

Первым результатом в target repository должен быть adoption audit.

Adoption audit должен показать:

- текущий repository и ветку;
- локальные инструкции;
- safety gate;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- какие документы template repository применимы;
- какие изменения можно предложить первым bootstrap PR.

Первым результатом не должен быть полный перенос всех файлов template repository.

## Ограничения

- Не читать `.env`.
- Не запускать Docker в safe short prompt mode.
- Не менять код до завершения self-discovery и adoption audit.
- Не переносить private data в public methodology repository.
- Не перетирать локальные инструкции target repository.
