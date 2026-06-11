# SOURCE_agent_system_index

Дата фиксации: 2026-06-11
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
17. docs/agent-system/ADOPTION_GUIDE.md
18. docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
19. docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
20. docs/agent-system/ENGINE_ENTRYPOINT.md
21. docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md
22. docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md
23. docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
24. docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
25. docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md
26. docs/agent-system/source/SOURCE_agent_system_index.md
27. docs/agent-system/CHATGPT_RESPONSE_STANDARD.md
28. docs/agent-system/FILE_COMMENTING_STANDARD.md
29. docs/agent-system/templates/CHATGPT_RESPONSE_TEMPLATE.md
30. docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md
31. docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md
32. docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md
33. docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md
34. docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
35. docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
36. docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md
37. docs/agent-system/templates/PROJECT_DASHBOARD_TEMPLATE.md
38. docs/agent-system/templates/ROADMAP_TEMPLATE.md
39. docs/agent-system/templates/BACKLOG_TEMPLATE.md
40. docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md
41. docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md

## Текущий этап

Current stage: PR-2n post-PR-2m state refresh and methodology release readiness.

PR-2m merged в `developer` через PR #46 и закрепил:

- one engine task = one self-contained Engine block;
- methodology freshness check;
- разделение manual terminal tasks;
- language consistency rule;
- `FILE_COMMENTING_STANDARD`;
- нейтральный methodology feedback без private downstream data.

## Состояние веток

- `main` - стабильная ветка.
- `developer` - интеграционная ветка.
- Следующие изменения выполняются только через `work/<role>/*`.

## Следующий шаг

Завершить PR-2n, после merge PR-2n проверить release readiness, выполнять release `developer` -> `main` только после решения пользователя, затем применять unified ChatGPT response standard в target repository adoption chats.

## Важно

- Не использовать названия конкретных внешних проектов.
- Для downstream-проектов использовать нейтральные формулировки.
- Codex/Claude/Gemini/Copilot не использовать в названиях агентов.
- Конкретный инструмент указывается отдельно как engine.
- `agent-system-development` - reusable methodology/template repository, а не центральный repository управления downstream-проектами.
- Задачи для engine писать на русском и начинать с `Задача для <agent-name>: <task-id>`.
- Task id должен быть связан с issue, PR, task id или внутренним номером работы проекта.
- Target repository governance pack фиксирует dashboard, roadmap, backlog, state, decisions, guardrails и engine registry.
- Project Constitution Framework фиксирует mission, success criteria, out-of-scope, strategic goal, authority, decision levels и scope expansion control.
- Canonical target adoption chat prompt лежит в `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`.
- Unified ChatGPT response standard лежит в `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md`.
- File commenting standard лежит в `docs/agent-system/FILE_COMMENTING_STANDARD.md`.
- Copy/paste-ready response template лежит в `docs/agent-system/templates/CHATGPT_RESPONSE_TEMPLATE.md`.
- Project-specific governance state создается только в target repository.
- Не читать `.env`.
- Не коммитить `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Все решения фиксировать в GitHub.
