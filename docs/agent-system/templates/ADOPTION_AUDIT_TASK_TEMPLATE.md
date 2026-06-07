# ADOPTION_AUDIT_TASK_TEMPLATE

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Adoption mode

`audit-only`

## Base branch

`<main or target base branch>`

## Working branch

`work/<role>/<task>`

## Role

`docs-maintainer-01`

## Goal

Выполнить repository self-discovery и создать только `docs/agent-system/ADOPTION_AUDIT.md`.

## Allowed files

- `docs/agent-system/ADOPTION_AUDIT.md`

## Forbidden changes

- `AGENTS.md`
- `README.md`
- `.github/workflows/**`
- Docker files
- runtime code
- architecture docs
- Source mirror
- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`

## Required preflight

- выполнить `ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- прочитать local `AGENTS.md`;
- прочитать local `README.md`;
- прочитать local architecture/status docs, если есть;
- проверить working tree;
- если working tree dirty - использовать clean worktree или STOP;
- sensitive grep только filename-only.

## Output

Создать audit file с разделами:

- repository self-discovery;
- current project state;
- template repository summary;
- fit analysis;
- adoption recommendation;
- risks;
- open questions;
- Methodology feedback.

## Checks

- git status --short
- git branch --show-current
- git diff --check
- git ls-files
- forbidden tracked paths check
- sensitive grep filename-only

## Final report

- working branch;
- created files;
- changed files;
- checks;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- risks;
- Methodology feedback;
- commit SHA;
- push status;
- PR link/number.
