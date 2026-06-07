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

## engine

`engine=<manual or selected engine>`

## Mandatory preflight

Перед bootstrap `engine` обязан выполнить контракт:

```text
docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md
```

Self-discovery, adoption mode selection и adoption audit выполняются до любых изменений файлов.

Использовать:

```text
docs/agent-system/ADOPTION_GUIDE.md
docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
```

## Goal

Описать цель bootstrap.

## Adoption mode

`audit-only`, `docs-only adoption` или `runtime adoption`.

По умолчанию для первого dry run использовать `audit-only`.

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

Для `audit-only`:

- `docs/agent-system/ADOPTION_AUDIT.md`

Для `docs-only adoption`, после отдельного решения пользователя:

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

`CURRENT_STATE.md`, `NEXT_STEPS.md` и `DECISION_LOG.md` не копировать из template repository verbatim. Они должны быть переписаны под target repository.

## Checks

- `git status --short`
- `git branch --show-current`
- `git diff --check`
- `git ls-files`
- forbidden tracked paths check
- sensitive grep filename-only:

```bash
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --
```

Sensitive grep must print only filenames. Do not print matching lines in terminal output, engine logs, or final reports.

## Final report format

`engine` должен вернуть:

- working branch;
- created files;
- changed files;
- checks executed;
- checks not executed and why;
- risks;
- adoption mode;
- transfer manifest notes;
- methodology feedback;
- suggested methodology improvements;
- automation opportunities;
- safety gaps;
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
