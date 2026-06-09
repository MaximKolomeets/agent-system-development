# BACKLOG

## Кандидаты задач

| Task id | Title | Owner/agent role | Priority | Status | Expected branch | Expected PR | Blocked by | Notes |
|---|---|---|---|---|---|---|---|---|
| `<task-id>` | `<short title>` | `<agent-name>` | `<low/medium/high>` | `<candidate/planned/in progress/done/blocked>` | `work/<agent-name>/<task-id>` | `<PR or TBD>` | `<blocker or none>` | `<notes>` |

## Значения status

- `candidate` - еще не выбрана;
- `planned` - выбрана для ближайшей работы;
- `in progress` - есть active branch или PR;
- `done` - merged или completed;
- `blocked` - нельзя продолжать без решения или внешнего изменения.

## Правила

- Каждая planned task требует task id.
- Каждый task id должен связываться с issue, PR, task id или внутренним номером работы.
- Каждая implementation task требует явный scope и expected branch.
- Review/research agents не ставят задачи implementation agents напрямую.
- Не включать private data, secrets, private repository URL или internal code names.

## Правило обновления

Обновлять backlog, если:

- task выбрана для PR;
- task завершена;
- task заблокирована;
- priority изменилась;
- появился новый candidate.
