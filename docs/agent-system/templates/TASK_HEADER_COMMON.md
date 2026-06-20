# TASK_HEADER_COMMON

Канонический общий header для engine task-шаблонов (`DEVELOPMENT_TASK_TEMPLATE.md`, `AGENT_RESEARCH_TASK_TEMPLATE.md` и других task-шаблонов). Эти блоки одинаковы для всех типов engine-задач; конкретный task-шаблон ссылается на этот канон и добавляет только свои уникальные секции.

## Mandatory header

```text
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>
```

Задача формулируется на русском языке. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

Header role-agnostic: указывается **роль** (функция в методологии), а не имя конкретного инструмента/модели. `<роль>` — vendor-neutral имя роли (эквивалент `<agent-name>` в manifest-правиле `mandatory_engine_task_header`). Конкретного **исполнителя** (tool/model/human) назначает архитектор; в task header он не фиксируется (`Исполнитель: на усмотрение архитектора`). Различение роли и исполнителя — канон `docs/agent-system/ROLE_MODEL.md` → «Роль vs исполнитель».

## Russian-first

Все ответы, final report, TASK/RESULT/INDEX, target-local docs/templates и комментарии в файлах писать на русском языке. Английский допустим только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и code identifiers.

## Рекомендуемый режим исполнения

Заполнить блок `Рекомендуемый режим исполнения` в mandatory header: роль / функция, исполнитель (на усмотрение архитектора), reasoning effort (низкий | средний | высокий), launch mode / запуск, execution mode / режим и почему / why this mode is required.

В шаблоне не указываются имена инструментов/моделей. Если нужно зафиксировать фактически использованного исполнителя постфактум — делать это в RESULT, не в task header.

## Передача (handoff)

Сквозное правило handoff для **любой** engine-задачи (development, research, review, infra, source-steward и т. д.).

Final report и RESULT обязаны заканчиваться блоком «Передача» с явной строкой:

```text
Следующий: <роль> — <что делает>
```

- `<роль>` — vendor-neutral роль следующего исполнителя (`reviewer`, `dev-implementer`, `docs-maintainer`, `infra`, `source-steward` и т. д.; канон ролей — `docs/agent-system/ROLE_MODEL.md`).
- Если следующего шага нет — писать `Следующий: нет — <причина>`.
- Решение, запускать ли следующий шаг и каким исполнителем, остаётся за пользователем/архитектором.

## Source-reminder

Сквозное правило синхронизации Source-снапшота.

Если задача меняла методологию или каноны (canon-файлы, шаблоны, governance этого methodology repository), исполнитель обязан:

1. Обновить source-снапшот, если изменённые файлы входят в него (политика — `docs/agent-system/source/README.md`); снапшоты являются derived context, source of truth — GitHub-файлы.
2. В RESULT и в блоке «Передача» явно добавить строку «Обновить Source-снапшот у зарегистрированных потребителей: …», где список берётся из реестра `docs/agent-system/SOURCE_CONSUMERS.md`. Реестр потребителей ведётся в потребляющем развёртывании; обезличенная upstream-методология своих потребителей не перечисляет, поэтому в ней список остаётся generic-placeholder.

Если методология/каноны не менялись — в RESULT явно отметить «Source-reminder: не применимо (методология не менялась)».

## Verified Baseline

- Repository:
- Local path, если применимо:
- Base branch:
- Working branch:
- Checked branch state:
- Latest relevant PR numbers/statuses, если применимо:
- Release PR status, если применимо:
- Sync PR status, если применимо:
- Open PR state, если relevant:
- Verification source:
- Verification date/time:

## Copy/Paste Completeness Check

- [ ] This TASK/Engine block can be executed without reading surrounding chat text.
- [ ] Рекомендуемый режим исполнения is included (роль / исполнитель «на усмотрение архитектора» / reasoning effort / запуск / режим / почему); имён инструментов/моделей в шаблоне нет.
- [ ] Требование к отчёту включает блок «Передача» (`Следующий: <роль> — <что делает>`) — канон `TASK_HEADER_COMMON` → «Передача».
- [ ] Source-reminder учтён: при изменении методологии/канонов RESULT и «Передача» содержат «Обновить Source-снапшот у зарегистрированных потребителей: …» (`docs/agent-system/SOURCE_CONSUMERS.md`); иначе явно «не применимо» — канон `TASK_HEADER_COMMON` → «Source-reminder».
- [ ] Verified baseline is included or explicitly marked as not applicable.
- [ ] Repository/base branch/working branch are included.
- [ ] Allowed files are included.
- [ ] Forbidden files are included.
- [ ] Checks are included.
- [ ] STOP conditions are included.
- [ ] Final report requirements are included.
- [ ] No required execution context exists only in surrounding chat.
- [ ] Перед sync/checkout/switch/pull/merge/rebase: repository root, remote, текущая ветка и `git status --short` проверены; dirty tree → STOP (канон: `docs/agent-system/BRANCH_POLICY.md` → «Repository sync / checkout guard»).
- [ ] Перед commit: `git rev-parse --abbrev-ref HEAD` == work-ветка задачи; если `developer`/`main` → STOP (канон: `docs/agent-system/BRANCH_POLICY.md` → «Pre-commit branch guard»).

## Project constitution check

Project mission:
Current strategic goal:
Scope impact: <No scope expansion | Minor scope expansion | Major scope expansion>
Decision level: <Level 1 | Level 2 | Level 3 | Level 4>
Requires explicit user approval: <yes/no>
