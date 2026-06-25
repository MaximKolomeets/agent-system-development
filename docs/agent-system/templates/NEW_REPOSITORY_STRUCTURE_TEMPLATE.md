# NEW_REPOSITORY_STRUCTURE_TEMPLATE

Универсальная стартовая структура repository:

```text
README.md
AGENTS.md
PROJECT_CONSTITUTION.md
PROJECT_DASHBOARD.md
ROADMAP.md
RUNBOOK.md
DECISIONS.md
.gitignore
docs/
  agent-system/
    README.md
    CURRENT_STATE.md
    NEXT_STEPS.md
    BACKLOG.md
    DECISION_LOG.md
    PROJECT_GUARDRAILS.md
    ENGINE_REGISTRY.md
    BRANCH_POLICY.md
    WORKFLOW.md
    PR_WORKFLOW.md
    ROLE_MODEL.md
    PUBLICATION_POLICY.md
    MANUAL_REVIEW_CHECKLIST.md
    templates/
    agents/
.github/
  workflows/
```

## Required root files

- `README.md` - назначение проекта и краткий workflow.
- `AGENTS.md` - правила для engine-исполнителей.
- `PROJECT_CONSTITUTION.md` - mission, success criteria, strategic goal, authority и scope control.
- `PROJECT_DASHBOARD.md` - краткий project status, active branch/PR, risks и links.
- `ROADMAP.md` - этапы проекта, criteria и next PR candidates.
- `RUNBOOK.md` - повторяемые операции и проверки.
- `DECISIONS.md` - root-level decision log, если проект выбирает такой формат.
- `.gitignore` - forbidden local/runtime paths.

## Required docs

- `docs/agent-system/README.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/PROJECT_GUARDRAILS.md`
- `docs/agent-system/ENGINE_REGISTRY.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/PUBLICATION_POLICY.md`
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`

## Optional docs

- `docs/agent-system/GITHUB_RULESETS.md`
- `docs/agent-system/WORKTREE_GUIDE.md`
- `docs/agent-system/CI_POLICY.md`
- `docs/agent-system/source/`

## Templates

`docs/agent-system/templates/` хранит reusable templates для задач, review, решений, handoff и bootstrap.

Governance pack templates:

- `TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`
- `PROJECT_CONSTITUTION_TEMPLATE.md`
- `PROJECT_DASHBOARD_TEMPLATE.md`
- `ROADMAP_TEMPLATE.md`
- `BACKLOG_TEMPLATE.md`
- `PROJECT_GUARDRAILS_TEMPLATE.md`
- `ENGINE_REGISTRY_TEMPLATE.md`

## Agent reports

`docs/agent-system/agents/` хранит отчеты ролей. Имена папок должны быть role-based и не должны содержать vendor/tool names.

## CI

`.github/workflows/` добавляется, если нужен CI. Для public repository рекомендуется начать с guardrails, которые не читают секреты и проверяют только tracked files.

## Adaptation

Структура может адаптироваться под public/private repository. В public repository нельзя хранить приватные данные, реальные секреты, внутренние кодовые имена или материалы private downstream repository.

Project-specific state files нужно создавать заново по фактам target repository, а не копировать из methodology repository verbatim.

## Branch bootstrap gate

Для нового пустого repository со стандартной схемой `main -> developer -> work/<role>/<task>` ветка `developer` создается до первой рабочей ветки.

Если `developer` отсутствует, сначала нужен явно разрешенный bootstrap step: создать `developer` от актуального `main` и синхронизировать `origin/developer`.

Рабочие ветки создаются от `developer`, а рабочие PR направляются в `developer`. Рабочий PR в `main` запрещен для `standard developer workflow`.
