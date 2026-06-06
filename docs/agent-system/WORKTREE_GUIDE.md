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
- `developer` worktree нужен для просмотра интеграционной ветки.
- Каждый агент работает в своей папке.
- Не использовать одну и ту же рабочую директорию для разных ролей одновременно.
