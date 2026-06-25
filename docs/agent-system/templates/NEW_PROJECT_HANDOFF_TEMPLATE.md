# NEW_PROJECT_HANDOFF_TEMPLATE

Использовать для передачи проекта в новый чат или новую рабочую сессию.

## Repository

`<repository owner/name>`

## Visibility

`public` или `private`.

## Current main

```text
<main branch commit or status>
```

## Current developer

```text
<developer branch commit or status>
```

## Active branch

```text
<work/<role>/<task>>
```

## Current PR

```text
<PR number, title, link, or none>
```

## Completed PRs

- `<PR number>` - `<summary>`.

## Active rules

- одна substantive task = одна основная task branch и один итоговый PR; internal sub-branches допустимы только внутри той же задачи;
- work branches создаются от актуальной `developer`;
- `developer` принимает изменения через PR;
- `main` принимает стабильное состояние из `developer`;
- пользователь принимает финальные решения.

## Forbidden files

- `.env`
- `.env.*`, кроме безопасного `.env.example`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- `*.log`
- `*.tmp`
- `*.bak`

## Important docs to read

- `AGENTS.md`
- `README.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/PUBLICATION_POLICY.md`

## Current goal

`<current goal>`

## Next PR

`<next PR title and branch>`

## Risks

- `<risk 1>`
- `<risk 2>`

## Exact prompt for continuation

```text
Продолжаем проект <repository>. Visibility: <public/private>. Читать AGENTS.md, README.md и ключевые документы docs/agent-system. Current main: <main status>. Current developer: <developer status>. Active branch: <branch>. Current PR: <PR or none>. Current goal: <goal>. Next PR: <next PR>. Соблюдать forbidden files policy, не читать .env, не использовать реальные credentials, не упоминать конкретные внешние проекты или внутренние кодовые имена. Пользователь принимает финальные решения.
```
