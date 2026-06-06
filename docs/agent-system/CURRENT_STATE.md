# CURRENT_STATE

Дата: 2026-06-06

Проект: Создание агентской системы

Репозиторий: `MaximKolomeets/agent-system-development`

Repository visibility: public.

Текущий этап: PR-1c public repository and active rulesets status.

Bootstrap перенесен в `main` через PR #1. PR-1b перенесен в `main` через PR #2.

`agent-system-development` переведен в public, потому что содержит методологию, workflow, шаблоны, роли агентов и правила разработки без секретов и клиентских данных.

`main` и `developer` синхронизированы.

Rulesets:

- `Protect main` - Active, по ручной проверке пользователя в GitHub UI;
- `Protect developer` - Active, по ручной проверке пользователя в GitHub UI.

Ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<role>/*` - рабочие ветки задач.

После bootstrap прямые изменения в `developer` запрещены без отдельного разрешения пользователя.

Все следующие задачи должны идти через `work/<role>/*`.

Правила именования:

- Codex/Claude/etc не используются в названиях агентов;
- Codex сейчас может использоваться только как engine-исполнитель по прямому заданию пользователя;
- роли агентов не зависят от конкретного vendor/tool.

Текущая задача: PR-1c public repository and active rulesets status.

Следующий шаг: создать локальные worktree для ролей агентов.
