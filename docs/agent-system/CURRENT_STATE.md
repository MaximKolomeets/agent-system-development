# CURRENT_STATE

Дата: 2026-06-06

Проект: Создание агентской системы

Репозиторий: `MaximKolomeets/agent-system-development`

Текущий этап: PR-1b stabilize repository workflow.

Bootstrap успешно перенесен в `main` через PR #1.

`main` теперь содержит стартовый каркас `agent-system-development`.

Ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<role>/*` - рабочие ветки следующих задач.

После bootstrap прямые изменения в `developer` запрещены без отдельного разрешения пользователя.

Все следующие задачи должны идти через `work/<role>/*`.

Правила именования:

- Codex/Claude/etc не используются в названиях агентов;
- Codex сейчас может использоваться только как engine-исполнитель по прямому заданию пользователя;
- роли агентов не зависят от конкретного vendor/tool.

Текущая задача: PR-1b stabilize repository workflow.

Следующий шаг после PR-1b: настроить GitHub branch protection/rulesets вручную в UI GitHub.
