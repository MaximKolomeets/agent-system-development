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

Добавить адаптированную документационную систему `docs/agent-system/` и, если входит в scope, target project governance pack в target repository без runtime changes.

Governance docs target repository должны быть приведены к единому языку. Для русскоязычного target repository по умолчанию используется русский язык.

Не переводить code identifiers, paths, commands, config keys, package names, API names, branch names, file names и vendor/tool names.

При переводе или унификации языка нельзя менять смысл архитектурных решений.

В создаваемые и изменяемые скрипты, workflow и технические файлы добавить русские комментарии для нужных строк/блоков. Если формат файла не поддерживает комментарии, пояснения добавить в соседнюю документацию или schema descriptions.

## Project constitution check

Project mission:
Current strategic goal:
Scope impact: <No scope expansion | Minor scope expansion | Major scope expansion>
Decision level: <Level 1 | Level 2 | Level 3 | Level 4>
Requires explicit user approval: <yes/no>

## Inputs

- `docs/agent-system/ADOPTION_AUDIT.md` from target repository;
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` from template repository;
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md` from template repository;
- `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md` from template repository;
- `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md` from template repository;
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
- `docs/agent-system/PROJECT_GUARDRAILS.md`
- `docs/agent-system/ENGINE_REGISTRY.md`
- `docs/agent-system/templates/**`
- `docs/agent-system/agents/docs-maintainer-01/**`
- `docs/agent-system/engine-journal/**`

Governance pack files разрешены только как docs-only artifacts:

- `PROJECT_CONSTITUTION.md`
- `PROJECT_DASHBOARD.md`
- `ROADMAP.md`
- `RUNBOOK.md`
- `DECISIONS.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/PROJECT_GUARDRAILS.md`
- `docs/agent-system/ENGINE_REGISTRY.md`

## Requires adaptation

Нельзя копировать дословно:

- `PROJECT_DASHBOARD.md`
- `PROJECT_CONSTITUTION.md`
- `ROADMAP.md`
- `RUNBOOK.md`
- `DECISIONS.md`
- `CURRENT_STATE.md`
- `NEXT_STEPS.md`
- `BACKLOG.md`
- `DECISION_LOG.md`
- `PROJECT_GUARDRAILS.md`
- `ENGINE_REGISTRY.md`
- Source index
- docs-maintainer reports
- engine journal index entries and task/result files
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
- применить governance pack template, если он в scope;
- создать или адаптировать `PROJECT_CONSTITUTION.md`, если governance pack в scope;
- выбрать только docs-only adoption mode.

## Checks

- git status --short
- git branch --show-current
- git diff --check
- git ls-files
- forbidden tracked paths check
- sensitive grep filename-only
- проверить, что нет runtime/code/CI changes
- проверить, что governance state files переписаны по фактам target repository
- проверить, что reusable templates не смешаны с target-specific state files
- проверить, что engine journal structure создана и task/result files не содержат private data
- проверить, что materialized governance files адаптированы под target repository
- проверить Governance Review Checklist из `PROJECT_CONSTITUTION.md`
- проверить language consistency governance docs
- проверить, где добавлены русские комментарии для нужных строк/блоков
- проверить, где комментарии не применимы из-за формата файла

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
- language consistency changes;
- commenting changes;
- engine journal files;
- files where comments are not applicable and why;
- risks;
- Methodology feedback;
- next recommended PR;
- commit SHA;
- push status;
- PR link/number.
