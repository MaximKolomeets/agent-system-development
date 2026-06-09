# PROJECT_PROFILE_TEMPLATE

Использовать этот шаблон для нейтрального описания нового проекта перед bootstrap.

## Project name

`<project name>`

## Public/private status

`public` или `private`.

Указать, какие материалы допустимы для выбранного visibility.

## Goal

Кратко описать целевой результат проекта.

## Non-goals

Перечислить, что проект намеренно не делает на текущем этапе.

## Repository name

`<repository name>`

## Expected branches

- `main` - stable branch;
- `developer` - integration branch;
- `work/<role>/*` - task branches.

## Roles

Перечислить роли по ответственности, без vendor/tool names.

Пример:

- `docs-maintainer-01`;
- `dev-implementer-01`;
- `qa-reviewer-01`;
- `security-reviewer-01`;
- `solution-architect-01`.

## Engines

Для каждой роли указать engine-исполнителя нейтрально:

```text
<role>: <engine name or engine class>
```

## Security constraints

- не хранить реальные секреты;
- не хранить `.env`;
- не хранить приватные данные;
- не печатать секреты в отчетах;
- считать public repository публичным источником.

## Forbidden data

- реальные credentials;
- реальные tokens;
- реальные passwords;
- реальные API keys;
- `.env`;
- `.venv/`;
- `data/`;
- `runtime/`;
- `dist/`;
- `backups/`;
- `exports/`;
- клиентские данные;
- персональные данные;
- внутренние кодовые имена.

## First milestone

Описать минимальный полезный milestone.

## First PR

Описать первый PR и его expected changed files.

## Documentation structure

Указать базовые документы:

- `README.md`;
- `AGENTS.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `RUNBOOK.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`;
- `docs/agent-system/BRANCH_POLICY.md`;
- `docs/agent-system/WORKFLOW.md`;
- `docs/agent-system/PR_WORKFLOW.md`;
- `docs/agent-system/ROLE_MODEL.md`;
- `docs/agent-system/PUBLICATION_POLICY.md`.

## Acceptance criteria

- repository создан;
- branch policy определена;
- forbidden data rules зафиксированы;
- governance pack создан по фактам target repository;
- первый PR малый и проверяемый;
- handoff подготовлен;
- пользователь подтвердил следующий шаг.
