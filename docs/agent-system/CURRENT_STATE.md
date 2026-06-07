# CURRENT_STATE

Дата: 2026-06-06

Проект: Создание агентской системы

Репозиторий: `MaximKolomeets/agent-system-development`

Repository visibility: public.

Текущий этап: PR-1e CI forbidden files check.

Bootstrap перенесен в `main` через PR #1. PR-1b перенесен в `main` через PR #2. Public repository и Active rulesets status зафиксированы через PR-1c.

Rulesets:

- `Protect main` - Active, по ручной проверке пользователя в GitHub UI;
- `Protect developer` - Active, по ручной проверке пользователя в GitHub UI.

`main` и `developer` синхронизированы на момент старта PR-1d. Worktree workflow уже зафиксирован через PR-1d.

Создан worktree для docs-maintainer:

```text
C:\Neural\worktrees\agent-system-development\docs-maintainer-01
```

Текущая рабочая ветка:

```text
work/docs-maintainer-01/pr-1e-ci-forbidden-files-check
```

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

Текущая задача добавляет GitHub Actions guardrail для forbidden tracked files.

Следующая цель после PR-1e: pre-push hook documentation.
