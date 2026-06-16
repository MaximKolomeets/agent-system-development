# TASK_HEADER_COMMON

Канонический общий header для engine task-шаблонов (`DEVELOPMENT_TASK_TEMPLATE.md`, `AGENT_RESEARCH_TASK_TEMPLATE.md` и других task-шаблонов). Эти блоки одинаковы для всех типов engine-задач; конкретный task-шаблон ссылается на этот канон и добавляет только свои уникальные секции.

## Mandatory header

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

Задача формулируется на русском языке. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Russian-first

Все ответы, final report, TASK/RESULT/INDEX, target-local docs/templates и комментарии в файлах писать на русском языке. Английский допустим только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и code identifiers.

## Recommended Engine Mode

Заполнить блок `Рекомендуемый режим <engine-name>` в mandatory header: launch mode / запуск, model / модель, reasoning, execution mode / режим и why this mode is required / почему.

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
- [ ] Recommended Engine Mode is included.
- [ ] Verified baseline is included or explicitly marked as not applicable.
- [ ] Repository/base branch/working branch are included.
- [ ] Allowed files are included.
- [ ] Forbidden files are included.
- [ ] Checks are included.
- [ ] STOP conditions are included.
- [ ] Final report requirements are included.
- [ ] No required execution context exists only in surrounding chat.
- [ ] Перед commit: `git rev-parse --abbrev-ref HEAD` == work-ветка задачи; если `developer`/`main` → STOP (канон: `docs/agent-system/BRANCH_POLICY.md` → «Pre-commit branch guard»).

## Project constitution check

Project mission:
Current strategic goal:
Scope impact: <No scope expansion | Minor scope expansion | Major scope expansion>
Decision level: <Level 1 | Level 2 | Level 3 | Level 4>
Requires explicit user approval: <yes/no>
