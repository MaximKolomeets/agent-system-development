# SOURCE_agent_system_index

Дата фиксации: 2026-06-07
Проект: Создание агентской системы
Основной источник правды: GitHub
Repository visibility: public

## Репозиторий

https://github.com/MaximKolomeets/agent-system-development

## Основные ветки

- `main` - стабильная версия
- `developer` - интеграционная ветка
- `work/dev-implementer-01/*` - задачи разработки
- `work/solution-architect-01/*` - архитектурные исследования
- `work/qa-reviewer-01/*` - проверки качества
- `work/security-reviewer-01/*` - проверки безопасности
- `work/docs-maintainer-01/*` - документация и Source summaries

## Rulesets

- `Protect main` - Active, по ручной проверке пользователя в GitHub UI.
- `Protect developer` - Active, по ручной проверке пользователя в GitHub UI.

## Читать в начале каждого нового чата

1. AGENTS.md
2. README.md
3. docs/agent-system/CURRENT_STATE.md
4. docs/agent-system/NEXT_STEPS.md
5. docs/agent-system/DECISION_LOG.md
6. docs/agent-system/BRANCH_POLICY.md
7. docs/agent-system/ROLE_MODEL.md
8. docs/agent-system/WORKFLOW.md
9. docs/agent-system/PR_WORKFLOW.md
10. docs/agent-system/GITHUB_RULESETS.md
11. docs/agent-system/PUBLICATION_POLICY.md
12. docs/agent-system/WORKTREE_GUIDE.md
13. docs/agent-system/CI_POLICY.md
14. docs/agent-system/PROJECT_LIFECYCLE.md
15. docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md
16. docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
17. docs/agent-system/ENGINE_ENTRYPOINT.md
18. docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md
19. docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md
20. docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md
21. docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md

## Текущий этап

Current stage: PR-2e engine entrypoint and repository self-discovery contract.

## Состояние веток

- `main` - стабильная ветка.
- `developer` - интеграционная ветка.
- Следующие изменения выполняются только через `work/<role>/*`.

## Следующий шаг

Повторить first target repository dry run коротким prompt.

## Важно

- Не использовать названия конкретных внешних проектов.
- Для downstream-проектов использовать нейтральные формулировки.
- Codex/Claude/Gemini/Copilot не использовать в названиях агентов.
- Конкретный инструмент указывается отдельно как engine.
- Не читать `.env`.
- Не коммитить `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Все решения фиксировать в GitHub.
