# WORKTREE_GUIDE

## Рекомендуемая локальная структура на Windows

```text
C:\Neural\repos\agent-system-development
C:\Neural\worktrees\agent-system-development\developer
C:\Neural\worktrees\agent-system-development\dev-implementer-01
C:\Neural\worktrees\agent-system-development\solution-architect-01
C:\Neural\worktrees\agent-system-development\qa-reviewer-01
C:\Neural\worktrees\agent-system-development\security-reviewer-01
C:\Neural\worktrees\agent-system-development\docs-maintainer-01
```

## Команды PowerShell

```powershell
mkdir C:\Neural\worktrees\agent-system-development
```

```powershell
git worktree add C:\Neural\worktrees\agent-system-development\developer developer
```

```powershell
git worktree add -b work/docs-maintainer-01/example-task C:\Neural\worktrees\agent-system-development\docs-maintainer-01 developer
```

## Правила использования

- Основной repo может оставаться на `main`.
- Основной repo может быть временно на `developer`, если пользователь синхронизирует ветки вручную.
- `developer` worktree нужен для просмотра интеграционной ветки.
- Рабочие задачи должны выполняться не в основной папке, а в отдельном worktree.
- Каждый агент работает в своей папке.
- Не использовать одну и ту же рабочую директорию для разных ролей одновременно.

## Фактическая схема PR-1d

Docs-maintainer worktree:

```text
C:\Neural\worktrees\agent-system-development\docs-maintainer-01
```

Текущая рабочая ветка:

```text
work/docs-maintainer-01/pr-1d-worktree-setup
```

## Practical worktree rules

- Основная папка репозитория не используется для выполнения задач агентов.
- Каждая substantive task выполняется в основной ветке `work/<role>/<task>`; внутренние `work/<role>/<task>/*` допустимы только как sub-branches той же задачи.
- Каждый агент должен работать в своей worktree-папке.
- Перед запуском engine-исполнителя всегда проверять `git branch --show-current`.
- Перед запуском engine-исполнителя всегда проверять `git status --short`.
- После завершения задачи worktree можно удалить только после merge PR.

## Useful commands

```powershell
git worktree list
```

```powershell
git branch --show-current
```

```powershell
git status --short
```

```powershell
git fetch origin
```
