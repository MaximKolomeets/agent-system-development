# TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Visibility

`public` или `private`.

## Base branch

`developer`

## Working branch

`work/<role>/<task>`

## Role

`<role-name>`

## Engine

`engine=<manual or selected engine>`

## Goal

Описать цель bootstrap.

## Allowed files

Пример:

- `README.md`
- `AGENTS.md`
- `.gitignore`
- `docs/agent-system/**`
- `.github/workflows/**`, если нужен CI

## Forbidden files and paths

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

## Required documents

- `README.md`
- `AGENTS.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/PUBLICATION_POLICY.md`

## Checks

- `git status --short`
- `git branch --show-current`
- `git diff --check`
- `git ls-files`
- forbidden tracked paths check
- sensitive grep:

```bash
git grep -n -i "token\|password\|secret\|api_key\|apikey\|credential\|пароль\|токен"
```

## Final report format

Engine должен вернуть:

- working branch;
- created files;
- changed files;
- checks executed;
- checks not executed and why;
- risks;
- next step;
- commit SHA;
- push status;
- PR link/number.

## Rules

- Do not read `.env`.
- Do not commit forbidden files.
- Do not push directly to `main`.
- Do not push directly to `developer`.
- Do not expose secrets.
- Do not use real credentials in examples.
- User makes final decisions.
