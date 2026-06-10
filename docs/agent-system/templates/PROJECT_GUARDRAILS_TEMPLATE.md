# PROJECT_GUARDRAILS

## Цель проекта

`<project goal>`

## Связь с Project Constitution

Primary authority document:

```text
PROJECT_CONSTITUTION.md
```

Guardrails не должны противоречить mission, current strategic goal, out-of-scope, decision authority и scope expansion control из `PROJECT_CONSTITUTION.md`.

## Non-goals

- `<non-goal>`;
- `<non-goal>`.

## Запрещенные направления

- `<forbidden direction>`;
- no work outside task scope;
- no runtime changes without explicit task scope;
- no direct changes to protected branches.

## Ограничения данных и безопасности

- Не читать `.env`.
- Не коммитить `.env`.
- Не коммитить `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Не использовать real credentials.
- Не печатать secret values.
- Sensitive grep должен быть filename-only.
- Public repository content считается публичным.

## Архитектурные ограничения

- `<architecture constraint>`;
- architecture changes require decision log entry;
- runtime adoption requires separate architecture decision.
- Level 3+ decisions require explicit user approval.
- Major scope expansion requires engine stop and user decision.

## Ограничения веток

- Паттерн рабочей ветки: `work/<agent-name>/<task-id>`.
- `main` - stable branch.
- `developer` - integration branch, если target repository не использует другую модель.
- Engine не делает direct push в `main` или `developer`.
- Agent names и branch names не содержат vendor/tool names.

## Stop conditions for engine

Engine должен остановиться и сообщить до изменений, если:

- repository не соответствует задаче;
- branch не соответствует задаче;
- working tree dirty без явного разрешения;
- есть forbidden tracked paths;
- задача требует private data, которые нельзя использовать;
- local instructions конфликтуют с задачей;
- scope неясен или шире task header.
