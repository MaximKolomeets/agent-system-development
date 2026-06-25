# TARGET_PROJECT_GOVERNANCE_PACK

## Назначение

Target project governance pack - это обязательный набор документов для target repository, который удерживает проект в рамках цели, roadmap, backlog, текущего состояния, принятых решений и scope control.

`agent-system-development` хранит только reusable methodology/templates. Project-specific state downstream-проектов не хранится в public methodology repository и создается заново в каждом target repository.

## Зачем нужен governance pack

Governance pack нужен, чтобы:

- зафиксировать project mission, success criteria и current strategic goal;
- зафиксировать цель и non-goals проекта;
- держать roadmap и backlog видимыми;
- связывать задачи, ветки, PR и отчеты;
- вести воспроизводимый engine journal task/result artifacts;
- отделять agent roles от engines;
- фиксировать authority агентов и уровни решений;
- контролировать scope expansion;
- фиксировать stop conditions для engine;
- обновлять current state после значимых PR;
- готовить handoff для нового чата или новой рабочей сессии.

## Документы проекта на root-level

Root-level документы помогают быстро понять проект без чтения всей методологии:

- `README.md` - назначение проекта и короткий workflow;
- `AGENTS.md` - обязательные правила для engine;
- `PROJECT_CONSTITUTION.md` - закон проекта: mission, success criteria, strategic goal, decision authority и scope expansion control;
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
- `docs/agent-system/engine-journal/`;
- `docs/agent-system/ROLE_MODEL.md`;
- `docs/agent-system/BRANCH_POLICY.md`;
- `docs/agent-system/WORKFLOW.md`;
- `docs/agent-system/PR_WORKFLOW.md`;
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`;
- `docs/agent-system/templates/`;
- `docs/agent-system/agents/`.

## Минимальный governance pack

```text
README.md
AGENTS.md
PROJECT_CONSTITUTION.md
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
docs/agent-system/engine-journal/
docs/agent-system/ROLE_MODEL.md
docs/agent-system/BRANCH_POLICY.md
docs/agent-system/WORKFLOW.md
docs/agent-system/PR_WORKFLOW.md
docs/agent-system/MANUAL_REVIEW_CHECKLIST.md
docs/agent-system/templates/
docs/agent-system/agents/
```

## Шаблон и target-specific state

Можно использовать как reusable templates:

- `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`;
- `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md`;
- `docs/agent-system/templates/PROJECT_DASHBOARD_TEMPLATE.md`;
- `docs/agent-system/templates/ROADMAP_TEMPLATE.md`;
- `docs/agent-system/templates/BACKLOG_TEMPLATE.md`;
- `docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md`;
- `docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md`;
- `docs/agent-system/engine-journal/templates/ENGINE_TASK_FILE_TEMPLATE.md`;
- `docs/agent-system/engine-journal/templates/ENGINE_RESULT_FILE_TEMPLATE.md`.

## Source-шаблон vs target materialization

Governance templates в methodology repository являются reusable sources. Они используются как reference или как основа для создания target files.

Materialized target governance files всегда требуют target adaptation. `PROJECT_CONSTITUTION.md`, `PROJECT_DASHBOARD.md`, `ROADMAP.md`, `BACKLOG.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md`, `PROJECT_GUARDRAILS.md` и `ENGINE_REGISTRY.md` не копируются verbatim и пишутся по фактам target repository.

Project-specific state живет только в target repository.

Нужно переписать под target repository:

- `README.md`;
- `AGENTS.md`;
- `PROJECT_CONSTITUTION.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `RUNBOOK.md`;
- `DECISIONS.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`;
- `docs/agent-system/engine-journal/INDEX.md`.

Нельзя копировать verbatim из methodology repository:

- project-specific state;
- completed milestones;
- current branch status;
- active PR status;
- downstream risks;
- downstream reports;
- private data, client data, private repository URL или internal code names.

## Правило обновления после PR

После каждого значимого PR target repository должен обновлять минимум:

- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`, если изменился ближайший план.

При необходимости также обновляются:

- `ROADMAP.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `PROJECT_DASHBOARD.md`;
- agent report в `docs/agent-system/agents/<роль>/`.

## Правило engine registry

Agent role стабильна, engine заменяем. Названия ролей, веток и папок агентов не должны содержать vendor/tool names.

`ENGINE_REGISTRY.md` должен содержать Agent Authority Matrix, согласованную с `PROJECT_CONSTITUTION.md`:

- allowed scope для каждой роли;
- forbidden scope для каждой роли;
- when approval is required;
- escalation или stop rule для Level 3+ и major scope expansion.

Branch pattern:

```text
work/<роль>/<task-id>
```

Task header:

```text
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
```

## Правило handoff

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

## Правило engine journal

Target repository должен хранить task/result history в `docs/agent-system/engine-journal/`.

Journal связывает task file, result file, branch, PR и commit/result. Он помогает проверить, какая engine-задача породила какой Pull Request и какой ответ engine был получен.

Task/result files append-only. Их нельзя удалять или перезаписывать без отдельного решения пользователя.

The methodology repository provides only engine journal scaffold/templates and
contract. Target repositories maintain their own operational history. Do not
copy methodology operational history into target repositories.

## Чеклист governance-review

Перед merge значимого PR проверить:

- соответствует ли изменение `PROJECT_CONSTITUTION.md` mission;
- соответствует ли изменение current strategic goal;
- нарушает ли изменение out-of-scope;
- меняет ли изменение architecture level;
- требуется ли explicit user approval;
- есть ли major scope expansion, требующий остановки и решения пользователя.
