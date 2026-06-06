# SOURCE_agent_system_index

Дата фиксации: 2026-06-06
Проект: Создание агентской системы
Основной источник правды: GitHub

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

## Читать в начале каждого нового чата

1. AGENTS.md
2. README.md
3. docs/agent-system/CURRENT_STATE.md
4. docs/agent-system/NEXT_STEPS.md
5. docs/agent-system/DECISION_LOG.md
6. docs/agent-system/BRANCH_POLICY.md
7. docs/agent-system/ROLE_MODEL.md
8. docs/agent-system/WORKFLOW.md

## Текущий этап

Bootstrap agent-system repository в ветке `developer`.

## Важно

- Codex/Claude/Gemini/Copilot не использовать в названиях агентов.
- Конкретный инструмент указывается отдельно как engine.
- Не читать `.env`.
- Не коммитить `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Все решения фиксировать в GitHub.
