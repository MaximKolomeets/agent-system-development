# DOCS_ONLY_ADOPTION_TASK_TEMPLATE

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

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Adoption mode

`docs-only adoption`

## Base branch

`<main/developer/develop according to target repository>`

## Working branch

`work/<role>/<task>`

## Role

`docs-maintainer-01`

## Goal

Добавить адаптированную документационную систему `docs/agent-system/` в target repository без runtime changes.

## Inputs

- `docs/agent-system/ADOPTION_AUDIT.md` from target repository;
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` from template repository;
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md` from template repository;
- local `AGENTS.md`;
- local `README.md`;
- local architecture/status docs.

## Allowed files

Разрешены только docs-only files, например:

- `docs/agent-system/README.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/SECURITY_POLICY.md`
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`
- `docs/agent-system/templates/**`
- `docs/agent-system/agents/docs-maintainer-01/**`

## Requires adaptation

Нельзя копировать дословно:

- `CURRENT_STATE.md`
- `NEXT_STEPS.md`
- `DECISION_LOG.md`
- Source index
- docs-maintainer reports
- ruleset status
- branch status
- project-specific history

Эти файлы либо не добавляются в первом docs-only PR, либо переписываются под target repository.

## Forbidden changes

- runtime code
- Docker
- CI
- Source mirror
- architecture docs
- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`

## Branch adaptation

Перед изменениями проверить:

- default branch;
- integration branch;
- `developer` vs `develop`;
- CI branch filters;
- rulesets/branch protection status.

## Required preflight

- выполнить repository self-discovery;
- проверить clean worktree;
- прочитать local instructions;
- применить transfer manifest;
- применить downstream checklist;
- выбрать только docs-only adoption mode.

## Checks

- git status --short
- git branch --show-current
- git diff --check
- git ls-files
- forbidden tracked paths check
- sensitive grep filename-only
- проверить, что нет runtime/code/CI changes

## Final report

- adoption mode;
- working branch;
- created files;
- changed files;
- adapted files;
- files intentionally not copied;
- checks;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- local instruction conflicts;
- risks;
- Methodology feedback;
- next recommended PR;
- commit SHA;
- push status;
- PR link/number.
