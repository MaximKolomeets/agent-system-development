# TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE

Использовать этот шаблон при создании governance pack в target repository.

Этот файл является reusable source template из methodology repository. Файлы target repository, созданные по нему, требуют адаптации под target facts, branch names, roadmap stages, backlog, current state, decisions и guardrails. Target state нужно писать заново, а не копировать из methodology repository verbatim.

## Обязательная шапка задачи для engine

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

`<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Структура файлов target repository

```text
README.md
AGENTS.md
PROJECT_CONSTITUTION.md
PROJECT_DASHBOARD.md
ROADMAP.md
RUNBOOK.md
DECISIONS.md
docs/agent-system/
  README.md
  CURRENT_STATE.md
  NEXT_STEPS.md
  BACKLOG.md
  DECISION_LOG.md
  PROJECT_GUARDRAILS.md
  ENGINE_REGISTRY.md
  engine-journal/
  BRANCH_POLICY.md
  WORKFLOW.md
  PR_WORKFLOW.md
  ROLE_MODEL.md
  PUBLICATION_POLICY.md
  MANUAL_REVIEW_CHECKLIST.md
  templates/
  agents/
```

## Обязательные файлы

| Файл | Назначение | Режим переноса |
|---|---|---|
| `README.md` | Назначение проекта и входная точка | переписать под target repository |
| `AGENTS.md` | Правила для engine | адаптировать local rules |
| `PROJECT_CONSTITUTION.md` | Закон проекта: mission, success criteria, strategic goal, authority и scope control | создать по target facts |
| `PROJECT_DASHBOARD.md` | Краткое состояние проекта | создать по фактам |
| `ROADMAP.md` | Этапы и критерии завершения | создать по target plan |
| `RUNBOOK.md` | Повторяемые операции | адаптировать команды |
| `docs/agent-system/CURRENT_STATE.md` | Текущее фактическое состояние | создать по фактам |
| `docs/agent-system/NEXT_STEPS.md` | Ближайшие действия | создать по target plan |
| `docs/agent-system/BACKLOG.md` | Candidate tasks | создать по target plan |
| `docs/agent-system/DECISION_LOG.md` | Решения проекта | создать по target decisions |
| `docs/agent-system/PROJECT_GUARDRAILS.md` | Goal, non-goals, stop conditions | создать по target constraints |
| `docs/agent-system/ENGINE_REGISTRY.md` | Роли агентов и mapping engines | адаптировать роли |
| `docs/agent-system/engine-journal/` | Journal task/result artifacts | создать project-specific journal |
| `docs/agent-system/BRANCH_POLICY.md` | Branch model | адаптировать branch names |
| `docs/agent-system/WORKFLOW.md` | Work process | адаптировать workflow |
| `docs/agent-system/PR_WORKFLOW.md` | PR flow | адаптировать target rules |
| `docs/agent-system/ROLE_MODEL.md` | Responsibilities агентов | адаптировать роли |
| `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md` | Review checklist | адаптировать criteria |

## Опциональные файлы

| Файл | Когда добавлять |
|---|---|
| `DECISIONS.md` | Если проекту нужен root-level decision log |
| `docs/agent-system/PUBLICATION_POLICY.md` | Если важны visibility/publication rules |
| `docs/agent-system/SECURITY_POLICY.md` | Если нужны явные security rules |
| `docs/agent-system/GITHUB_RULESETS.md` | Если настроены rulesets |
| `docs/agent-system/CI_POLICY.md` | Если CI входит в scope |

## Связь state documents

- `PROJECT_DASHBOARD.md` кратко показывает current goal, active PR, blockers и links.
- `PROJECT_CONSTITUTION.md` фиксирует mission, success criteria, out-of-scope, architectural principles, current strategic goal, authority и scope expansion control.
- `ROADMAP.md` задает stages, completion criteria и next PR candidates.
- `docs/agent-system/CURRENT_STATE.md` фиксирует фактическое состояние после PR.
- `docs/agent-system/NEXT_STEPS.md` фиксирует ближайший план.
- `docs/agent-system/BACKLOG.md` хранит candidate tasks с owner role и expected branch.
- `docs/agent-system/DECISION_LOG.md` фиксирует decisions, reasons и consequences.
- `docs/agent-system/PROJECT_GUARDRAILS.md` задает goal, non-goals, forbidden scope и stop conditions.
- `docs/agent-system/ENGINE_REGISTRY.md` связывает stable agent roles с replaceable engines.
- `docs/agent-system/engine-journal/` связывает engine task files, result files, branches, PR и commits.

## Target-specific files

Не копировать эти файлы verbatim из methodology repository:

- `PROJECT_DASHBOARD.md`;
- `PROJECT_CONSTITUTION.md`;
- `ROADMAP.md`;
- `RUNBOOK.md`;
- `DECISIONS.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`;
- `docs/agent-system/engine-journal/**`;
- `docs/agent-system/agents/**`.

Эти файлы должны быть написаны по фактам target repository.

## Правила веток и задач

Branch pattern:

```text
work/<agent-name>/<task-id>
```

Правила:

- не использовать vendor/tool names в branch names;
- не использовать vendor/tool names в agent folder names;
- task id связывает task, branch, report и PR;
- engine journal связывает task file, result file, branch, PR и commit/result;
- engine выбирается для конкретной задачи и фиксируется в task header.
- `ENGINE_REGISTRY.md` содержит Agent Authority Matrix, согласованную с `PROJECT_CONSTITUTION.md`.

## Governance review checklist

- [ ] Изменение соответствует mission.
- [ ] Изменение соответствует current strategic goal.
- [ ] Изменение не нарушает out-of-scope.
- [ ] Изменение не меняет architecture level без approval.
- [ ] Level 3+ decisions имеют explicit user approval.
- [ ] Major scope expansion остановлен до решения пользователя.

## Правило обновления после PR

После каждого значимого PR обновить минимум:

- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`, если план изменился.

Обновлять при необходимости:

- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- agent report в `docs/agent-system/agents/<agent-name>/`.
