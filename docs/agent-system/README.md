# Agent System Documentation

Эта папка хранит рабочую документацию проекта "Создание агентской системы".

Здесь фиксируются:

- архитектура агентской системы;
- правила веток;
- роли агентов;
- workflow;
- текущее состояние;
- принятые решения;
- PR workflow;
- local worktree guide;
- GitHub rulesets recommendations;
- hotfix, rollback и disaster recovery policy;
- non-technical architect guide, cockpit и handoff pack;
- manual review checklist;
- adoption modes;
- transfer manifest;
- downstream adaptation checklist;
- private control-plane templates и MIR lifecycle ledger;
- target project governance pack;
- project constitution framework;
- шаблоны задач, отчетов и review;
- отчеты и рабочие заметки агентов.

GitHub остается основным источником правды. Source-файлы в `source/` служат индексом и кратким слепком состояния.

## Templates

- `templates/ADOPTION_AUDIT_TASK_TEMPLATE.md` - задача первого safe dry run в режиме `audit-only`.
- `templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md` - задача docs-only adoption после adoption audit.
- `templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md` - структура governance pack для target repository.
- `templates/PROJECT_CONSTITUTION_TEMPLATE.md` - target `PROJECT_CONSTITUTION.md` для mission, authority и scope control.
- `templates/PROJECT_DASHBOARD_TEMPLATE.md` - dashboard проекта.
- `templates/PROJECT_OPERATOR_DASHBOARD_TEMPLATE.md` - короткий yes/no dashboard для architect/operator.
- `templates/ROADMAP_TEMPLATE.md` - roadmap проекта.
- `templates/BACKLOG_TEMPLATE.md` - backlog задач.
- `templates/TIME_LEDGER_TEMPLATE.md` - rollup времени, token/cost и metrics
  по PR/release/project.
- `templates/PROJECT_GUARDRAILS_TEMPLATE.md` - project guardrails и stop conditions.
- `templates/ENGINE_REGISTRY_TEMPLATE.md` - registry ролей и engines.
