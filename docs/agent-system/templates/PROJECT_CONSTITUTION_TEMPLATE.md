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
- paid SaaS dependencies только после explicit approval;
- production infrastructure только после explicit approval;
- large architecture rewrites только после explicit approval;
- integrations вне approved roadmap;
- new services только после explicit approval;
- new business directions только после explicit approval;
- runtime or infrastructure changes вне approved stage.

## Архитектурные принципы (Architectural Principles)

- `<target architectural principle>`;
- Local-first, если confirmed for this project;
- docs-first перед implementation;
- no microservices до approved stage;
- no Kubernetes до approved stage;
- no paid external dependency без explicit approval;
- no runtime adoption без separate architecture decision.

## Текущая стратегическая цель (Current Strategic Goal)

```text
<current strategic goal>
```

## Стадия lifecycle (Lifecycle Stage)

`<idea | bootstrap | foundation | mvp | beta | production | scaling | maintenance | custom>`

## Полномочия агентов (Agent Authority)

Agent roles и engine mapping определяются в:

```text
docs/agent-system/ENGINE_REGISTRY.md
```

`ENGINE_REGISTRY.md` должен включать Agent Authority Matrix.

## Матрица полномочий агентов (Agent Authority Matrix)

| Agent role | Allowed scope | Forbidden scope | Requires approval |
|---|---|---|---|
| `<роль>` | `<paths or responsibilities>` | `<paths or responsibilities>` | `<approval conditions>` |

## Архитектор/owner

Архитектор или owner проекта может не быть программистом.

Он утверждает **что** и **зачем**: mission, priority, scope, acceptance,
business risk, Level 3/4 decisions и human-only actions.

Executor/reviewer отвечают за проверяемое **как** внутри утвержденного scope:
implementation details, checks, evidence и risk summary.

## Уровни полномочий решений (Decision Authority Levels)

| Level | Name | Examples | Approval |
|---|---|---|---|
| Level 1 | Implementation | `<small implementation>` | task scope |
| Level 2 | Subsystem | `<subsystem change>` | task + review |
| Level 3 | Architecture | `<architecture change>` | explicit user approval |
| Level 4 | Project Strategy | `<strategy change>` | explicit user approval |

Level 3+ decisions требуют explicit user approval до изменений.

## Контроль расширения scope (Scope Expansion Control)

```text
No scope expansion
Minor scope expansion
Major scope expansion
```

Major scope expansion запрещен без explicit user decision.

## Чеклист governance-review (Governance Review Checklist)

- [ ] Change соответствует `Project Mission`.
- [ ] Change соответствует `Current Strategic Goal`.
- [ ] Change не нарушает `Out Of Scope`.
- [ ] Change не меняет architecture level без authority.
- [ ] Level 3+ decisions имеют explicit user approval.
- [ ] Major scope expansion остановлен до изменений и отправлен на user decision.
- [ ] `ENGINE_REGISTRY.md` Agent Authority Matrix остается current.

## STOP-условия (Stop Conditions)

- major scope expansion;
- conflict with Project Mission;
- conflict with Out Of Scope;
- Level 3+ decision without approval;
- risk of private data or secrets exposure;
- local instructions conflict.

## Правила обновления (Update Rules)

- update после mission changes;
- update после strategic goal changes;
- update после architecture principles changes;
- update после agent authority changes;
- update после Level 3+ decisions.
