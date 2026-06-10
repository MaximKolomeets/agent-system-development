# CURRENT_STATE

Дата: 2026-06-10

Проект: Создание агентской системы

Репозиторий: `MaximKolomeets/agent-system-development`

Repository visibility: public.

Текущий этап: PR-2l reusable target adoption chat prompt.

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
work/docs-maintainer-01/pr-2l-reusable-target-adoption-chat-prompt
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

PR-1e добавил GitHub Actions guardrail для forbidden tracked files.

PR-2a завершен и добавил lifecycle/templates запуска нового проекта.

PR-2b завершен и добавил practical onboarding guide для запуска нового проекта.

PR-2c завершен и обновил GitHub Actions checkout action для совместимости с Node.js 24.

PR-2d подготовил target repository adoption readiness pack.

PR-2e завершен и добавил engine entrypoint, repository self-discovery contract и short prompt adoption mode.

PR-2f завершен и добавил methodology feedback loop.

PR-2g завершен и добавил adoption modes, transfer manifest, downstream checklist и minimal first PR rule.

PR-2h завершен и добавил reusable task templates для `audit-only` и `docs-only adoption`.

PR-2i завершен и уточнил роль `agent-system-development` как reusable methodology/template repository, а также закрепил обязательную русскоязычную шапку задач для `engine`.

PR-2j завершен и добавил target project governance pack: dashboard, roadmap, backlog, current state, next steps, decision log, project guardrails, engine registry и handoff rules для target repositories.

PR-2k завершен и добавил Project Constitution Framework: reusable framework, `PROJECT_CONSTITUTION_TEMPLATE.md`, Agent Authority Matrix, Decision Authority Levels, Scope Expansion Control и Governance Review Checklist для target repositories.

Текущая задача PR-2l добавляет canonical copy/paste prompt для запуска adoption в target repository из нового project chat.

Следующая цель после PR-2l: review, merge, release methodology repository, затем применять prompt в target repositories.
