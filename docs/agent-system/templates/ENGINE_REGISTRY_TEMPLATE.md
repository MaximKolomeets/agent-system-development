# ENGINE_REGISTRY

## Rule

Agent role стабильна. Engine заменяем.

Роли называются по ответственности. Engines выбираются для конкретной задачи и фиксируются в task header.

## Roles

| Agent role | Responsibility | Default engine class | Notes |
|---|---|---|---|
| `docs-maintainer-01` | Документация и синхронизация state | selected per task | Без runtime changes |
| `dev-implementer-01` | Implementation tasks | selected per task | Работает только в task scope |
| `qa-reviewer-01` | Review и regression checks | selected per task | Не исправляет без отдельной задачи |
| `security-reviewer-01` | Secrets и forbidden files review | selected per task | Sensitive grep только filename-only |
| `solution-architect-01` | Architecture proposals и tradeoffs | selected per task | Не реализует без отдельной задачи |

## Agent Authority Matrix

Authority roles ограничены `PROJECT_CONSTITUTION.md`, task header, local instructions и branch policy.

| Agent role | Allowed scope | Forbidden scope | Approval required |
|---|---|---|---|
| `docs-maintainer-01` | Документация, state sync, templates, reports | Runtime code, services, private data, implementation outside docs | Scope expansion, Level 3+ decisions |
| `dev-implementer-01` | Implementation внутри назначенной задачи | Project strategy, unrelated subsystems, direct protected branch changes | Architecture changes, major scope expansion |
| `qa-reviewer-01` | Review, regression checks, risk findings | Исправления без отдельной задачи, scope changes | Any file edits, Level 3+ findings |
| `security-reviewer-01` | Secrets review, forbidden files review, filename-only sensitive grep | Reading `.env`, printing secret values, using real credentials | Suspected secret or policy conflict |
| `solution-architect-01` | Architecture proposals, tradeoffs, decision drafts | Implementation without separate task, strategy changes without approval | Level 3+ decisions and strategic changes |

## Правило веток

```text
work/<agent-name>/<task-id>
```

## Правило task header

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
```

## Forbidden

- не использовать vendor/tool names в branch names;
- не использовать vendor/tool names в agent folder names;
- engine не делает direct push в `main` или `developer`;
- не запускать задачу без task id;
- не использовать task id, который нельзя связать с issue, PR, task id или внутренним номером работы.

## Update rule

Обновлять registry, если:

- роль добавлена или удалена;
- responsibility изменилась;
- default engine class изменился;
- branch namespace изменился.
