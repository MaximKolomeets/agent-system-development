# SHORT_TARGET_ADOPTION_PROMPT

## Full copy/paste prompt

Для применения методологии в новом target repository используйте полный canonical prompt:

```text
docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md
```

Этот файл остается короткой entrypoint-версией. Canonical full prompt находится в `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`.

## Обязательная шапка задачи

Короткий prompt используется после русскоязычной task header:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

`<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

Короткий prompt должен включать Russian-first reminder: все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке; English допустим только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names.

Короткий prompt должен требовать Post-merge Journal Closure: после merge/release/sync target `RESULT` и `INDEX` фиксируют status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`.

Короткий prompt должен требовать `methodology_reference`: repository, source branch, source commit SHA, checked_at и reference_type.

## Короткий prompt

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development. Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пиши на русском языке; English допускается только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names. Зафиксируй methodology_reference с source commit SHA. После merge/release/sync закрой target RESULT/INDEX по Post-merge Journal Closure.
```

## Безопасный короткий prompt

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development. Сначала выполни repository self-discovery и adoption audit, без изменения кода и без запуска Docker. Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах пиши на русском языке; English допускается только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names. Зафиксируй methodology_reference с source commit SHA. После merge/release/sync закрой target RESULT/INDEX по Post-merge Journal Closure. В final report добавь Methodology feedback: что улучшить в template repository для следующей интеграции, без private data.
```

## Как должен действовать engine

`engine` должен сам найти в template repository:

- `docs/agent-system/ENGINE_ENTRYPOINT.md`;
- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- `docs/agent-system/ADOPTION_GUIDE.md`;
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`;
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`;
- `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md`;
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
- какие изменения можно предложить первым bootstrap PR.
- methodology_reference с source commit SHA.

Первым результатом не должен быть полный перенос всех файлов template repository.

## Ограничения

- Не читать `.env`.
- Не запускать Docker в safe short prompt mode.
- Не менять код до завершения self-discovery и adoption audit.
- Не переносить private data в public methodology repository.
- Не перетирать локальные инструкции target repository.
