# PROJECT_CONSTITUTION

Этот файл создается в target repository по фактам target project. Не копировать project-specific state из methodology repository или другого target repository.

## Project Mission

`<short mission statement>`

## Success Criteria

- `<success criterion>`;
- `<success criterion>`;
- `<success criterion>`.

## Out Of Scope

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

## Architectural Principles

- `<target architectural principle>`;
- Local-first, if confirmed for this project;
- docs-first before implementation;
- no microservices before approved stage;
- no Kubernetes before approved stage;
- no paid external dependency without explicit approval;
- no runtime adoption without separate architecture decision.

## Current Strategic Goal

```text
<current strategic goal>
```

## Lifecycle Stage

`<idea | bootstrap | foundation | mvp | beta | production | scaling | maintenance | custom>`

## Agent Authority

Agent roles and engine mapping are defined in:

```text
docs/agent-system/ENGINE_REGISTRY.md
```

`ENGINE_REGISTRY.md` must include an Agent Authority Matrix.

## Agent Authority Matrix

| Agent role | Allowed scope | Forbidden scope | Requires approval |
|---|---|---|---|
| `<agent-name>` | `<paths or responsibilities>` | `<paths or responsibilities>` | `<approval conditions>` |

## Decision Authority Levels

| Level | Name | Examples | Approval |
|---|---|---|---|
| Level 1 | Implementation | `<small implementation>` | task scope |
| Level 2 | Subsystem | `<subsystem change>` | task + review |
| Level 3 | Architecture | `<architecture change>` | explicit user approval |
| Level 4 | Project Strategy | `<strategy change>` | explicit user approval |

Level 3+ decisions require explicit user approval before changes.

## Scope Expansion Control

```text
No scope expansion
Minor scope expansion
Major scope expansion
```

Major scope expansion is forbidden without explicit user decision.

## Governance Review Checklist

- [ ] Change matches `Project Mission`.
- [ ] Change matches `Current Strategic Goal`.
- [ ] Change does not violate `Out Of Scope`.
- [ ] Change does not alter architecture level without authority.
- [ ] Level 3+ decisions have explicit user approval.
- [ ] Major scope expansion was stopped before changes and sent to user decision.
- [ ] `ENGINE_REGISTRY.md` Agent Authority Matrix remains current.

## Stop Conditions

- major scope expansion;
- conflict with Project Mission;
- conflict with Out Of Scope;
- Level 3+ decision without approval;
- risk of private data or secrets exposure;
- local instructions conflict.

## Update Rules

- update after mission changes;
- update after strategic goal changes;
- update after architecture principles changes;
- update after agent authority changes;
- update after Level 3+ decisions.
