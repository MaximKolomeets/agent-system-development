# TARGET_PROJECT_GOVERNANCE_PACK

## Назначение

Target project governance pack - это обязательный набор документов для target repository, который удерживает проект в рамках цели, roadmap, backlog, текущего состояния, принятых решений и scope control.

`agent-system-development` хранит только reusable methodology/templates. Project-specific state downstream-проектов не хранится в public methodology repository и создается заново в каждом target repository.

## Зачем нужен governance pack

Governance pack нужен, чтобы:

- зафиксировать цель и non-goals проекта;
- держать roadmap и backlog видимыми;
- связывать задачи, ветки, PR и отчеты;
- отделять agent roles от engines;
- фиксировать stop conditions для engine;
- обновлять current state после значимых PR;
- готовить handoff для нового чата или новой рабочей сессии.

## Root-level project docs

Root-level документы помогают быстро понять проект без чтения всей методологии:

- `README.md` - назначение проекта и короткий workflow;
- `AGENTS.md` - обязательные правила для engine;
- `PROJECT_DASHBOARD.md` - короткая панель состояния проекта;
- `ROADMAP.md` - этапы, критерии завершения и next PR candidates;
- `RUNBOOK.md` - повторяемые операции и проверки;
- `DECISIONS.md` или `docs/agent-system/DECISION_LOG.md` - принятые решения.

## docs/agent-system docs

Документы в `docs/agent-system/` управляют agent workflow и состоянием:

- `docs/agent-system/README.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`;
- `docs/agent-system/ROLE_MODEL.md`;
- `docs/agent-system/BRANCH_POLICY.md`;
- `docs/agent-system/WORKFLOW.md`;
- `docs/agent-system/PR_WORKFLOW.md`;
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`;
- `docs/agent-system/templates/`;
- `docs/agent-system/agents/`.

## Minimal governance pack

```text
README.md
AGENTS.md
PROJECT_DASHBOARD.md
ROADMAP.md
RUNBOOK.md
DECISIONS.md или docs/agent-system/DECISION_LOG.md
docs/agent-system/README.md
docs/agent-system/CURRENT_STATE.md
docs/agent-system/NEXT_STEPS.md
docs/agent-system/BACKLOG.md
docs/agent-system/DECISION_LOG.md
docs/agent-system/PROJECT_GUARDRAILS.md
docs/agent-system/ENGINE_REGISTRY.md
docs/agent-system/ROLE_MODEL.md
docs/agent-system/BRANCH_POLICY.md
docs/agent-system/WORKFLOW.md
docs/agent-system/PR_WORKFLOW.md
docs/agent-system/MANUAL_REVIEW_CHECKLIST.md
docs/agent-system/templates/
docs/agent-system/agents/
```

## Template vs target-specific state

Можно использовать как reusable templates:

- `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`;
- `docs/agent-system/templates/PROJECT_DASHBOARD_TEMPLATE.md`;
- `docs/agent-system/templates/ROADMAP_TEMPLATE.md`;
- `docs/agent-system/templates/BACKLOG_TEMPLATE.md`;
- `docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md`;
- `docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md`.

Нужно переписать под target repository:

- `README.md`;
- `AGENTS.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `RUNBOOK.md`;
- `DECISIONS.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`.

Нельзя копировать verbatim из methodology repository:

- project-specific state;
- completed milestones;
- current branch status;
- active PR status;
- downstream risks;
- downstream reports;
- private data, client data, private repository URL или internal code names.

## Update rule after PR

После каждого значимого PR target repository должен обновлять минимум:

- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`, если изменился ближайший план.

При необходимости также обновляются:

- `ROADMAP.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `PROJECT_DASHBOARD.md`;
- agent report в `docs/agent-system/agents/<agent-name>/`.

## Engine registry rule

Agent role стабильна, engine заменяем. Названия ролей, веток и папок агентов не должны содержать vendor/tool names.

Branch pattern:

```text
work/<agent-name>/<task-id>
```

Task header:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:
```

## Handoff rule

Handoff для нового чата или новой рабочей сессии должен ссылаться на:

- repository;
- visibility;
- current branch;
- active PR;
- current goal;
- next PR;
- blockers;
- risks;
- важные governance docs.

Handoff не должен содержать private data, secret values, private repository URL, client data или internal code names.
