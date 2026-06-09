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

## Правило веток

```text
work/<agent-name>/<task-id>
```

## Правило task header

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:
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
