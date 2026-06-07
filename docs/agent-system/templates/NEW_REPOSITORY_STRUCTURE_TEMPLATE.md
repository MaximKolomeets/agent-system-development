# NEW_REPOSITORY_STRUCTURE_TEMPLATE

Универсальная стартовая структура repository:

```text
README.md
AGENTS.md
.gitignore
docs/
  agent-system/
    CURRENT_STATE.md
    NEXT_STEPS.md
    DECISION_LOG.md
    BRANCH_POLICY.md
    WORKFLOW.md
    PR_WORKFLOW.md
    ROLE_MODEL.md
    PUBLICATION_POLICY.md
    templates/
    agents/
.github/
  workflows/
```

## Required root files

- `README.md` - назначение проекта и краткий workflow.
- `AGENTS.md` - правила для engine-исполнителей.
- `.gitignore` - forbidden local/runtime paths.

## Required docs

- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/PUBLICATION_POLICY.md`

## Optional docs

- `docs/agent-system/GITHUB_RULESETS.md`
- `docs/agent-system/WORKTREE_GUIDE.md`
- `docs/agent-system/CI_POLICY.md`
- `docs/agent-system/source/`

## Templates

`docs/agent-system/templates/` хранит reusable templates для задач, review, решений, handoff и bootstrap.

## Agent reports

`docs/agent-system/agents/` хранит отчеты ролей. Имена папок должны быть role-based и не должны содержать vendor/tool names.

## CI

`.github/workflows/` добавляется, если нужен CI. Для public repository рекомендуется начать с guardrails, которые не читают секреты и проверяют только tracked files.

## Adaptation

Структура может адаптироваться под public/private repository. В public repository нельзя хранить приватные данные, реальные секреты, внутренние кодовые имена или материалы private downstream repository.
