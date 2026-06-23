# PROJECT_CONSTITUTION

Этот файл создается в target repository по фактам target project. Не копировать project-specific state из methodology repository или другого target repository.

## Миссия проекта (Project Mission)

`<short mission statement>`

## Критерии успеха (Success Criteria)

- `<success criterion>`;
- `<success criterion>`;
- `<success criterion>`.

## Вне scope (Out Of Scope)

- `<out-of-scope direction>`;
- new products before explicit approval;
- new platforms before explicit approval;
- paid SaaS dependencies before explicit approval;
- production infrastructure before explicit approval;
- large architecture rewrites before explicit approval;
- integrations outside approved roadmap;
- new services before explicit approval;
- new business directions before explicit approval;
- runtime or infrastructure changes outside approved stage.

## Архитектурные принципы (Architectural Principles)

- `<target architectural principle>`;
- Local-first, if confirmed for this project;
- docs-first before implementation;
- no microservices before approved stage;
- no Kubernetes before approved stage;
- no paid external dependency without explicit approval;
- no runtime adoption without separate architecture decision.

## Текущая стратегическая цель (Current Strategic Goal)

```text
<current strategic goal>
```

## Стадия lifecycle (Lifecycle Stage)

`<idea | bootstrap | foundation | mvp | beta | production | scaling | maintenance | custom>`

## Полномочия агентов (Agent Authority)

Agent roles and engine mapping are defined in:

```text
docs/agent-system/ENGINE_REGISTRY.md
```

`ENGINE_REGISTRY.md` must include an Agent Authority Matrix.

## Матрица полномочий агентов (Agent Authority Matrix)

| Agent role | Allowed scope | Forbidden scope | Requires approval |
|---|---|---|---|
| `<роль>` | `<paths or responsibilities>` | `<paths or responsibilities>` | `<approval conditions>` |

## Уровни полномочий решений (Decision Authority Levels)

| Level | Name | Examples | Approval |
|---|---|---|---|
| Level 1 | Implementation | `<small implementation>` | task scope |
| Level 2 | Subsystem | `<subsystem change>` | task + review |
| Level 3 | Architecture | `<architecture change>` | explicit user approval |
| Level 4 | Project Strategy | `<strategy change>` | explicit user approval |

Level 3+ decisions require explicit user approval before changes.

## Контроль расширения scope (Scope Expansion Control)

```text
No scope expansion
Minor scope expansion
Major scope expansion
```

Major scope expansion is forbidden without explicit user decision.

## Чеклист governance-review (Governance Review Checklist)

- [ ] Change matches `Project Mission`.
- [ ] Change matches `Current Strategic Goal`.
- [ ] Change does not violate `Out Of Scope`.
- [ ] Change does not alter architecture level without authority.
- [ ] Level 3+ decisions have explicit user approval.
- [ ] Major scope expansion was stopped before changes and sent to user decision.
- [ ] `ENGINE_REGISTRY.md` Agent Authority Matrix remains current.

## STOP-условия (Stop Conditions)

- major scope expansion;
- conflict with Project Mission;
- conflict with Out Of Scope;
- Level 3+ decision without approval;
- risk of private data or secrets exposure;
- local instructions conflict.

## Правила обновления (Update Rules)

- update after mission changes;
- update after strategic goal changes;
- update after architecture principles changes;
- update after agent authority changes;
- update after Level 3+ decisions.
