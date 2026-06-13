# WORKFLOW

1. Пользователь принимает решение.
2. ChatGPT помогает сформулировать задачу.
3. Задача оформляется по шаблону.
4. Исполнитель работает в своей ветке.
5. Исполнитель обновляет отчет.
6. Проверяющий агент делает review.
7. Пользователь принимает решение о merge.
8. После merge обновляются `CURRENT_STATE` и `DECISION_LOG`, если нужно.

## После bootstrap

- Прямые изменения в `developer` запрещены без отдельного разрешения пользователя.
- Рабочий поток идет через ветки `work/<role>/*`.
- Рабочая ветка создается от актуальной `developer`.
- `developer` принимает изменения через PR из рабочих веток.
- `developer` -> `main` выполняется только после проверки интеграционной ветки.

## Review-only workflow

Code review / external review / consulting review по умолчанию выполняется как review-only task:

```text
developer -> work/code-reviewer-01/<task-id> -> PR в developer
```

Review-only PR содержит только review report files и journal/state updates, если они явно разрешены задачей.

Reviewer не исправляет production code, runtime, Docker, CI, scripts или dependencies. Findings превращаются в отдельные implementation PR только после решения пользователя.

Подробный контракт:

```text
docs/agent-system/CODE_REVIEW_WORKFLOW.md
```
