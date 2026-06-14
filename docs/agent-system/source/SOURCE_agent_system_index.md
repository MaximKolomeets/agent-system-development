# SOURCE_agent_system_index

```yaml
source_snapshot:
  source_of_truth: GitHub
  source_repository: MaximKolomeets/agent-system-development
  source_commit: cb950132ee779b3632d0df396ab65115ba46864d
  generated_at: 2026-06-14T14:23:07.1492210+07:00
  staleness_policy: use GitHub files if this snapshot differs from repository state
```

Этот файл — навигационный индекс, а не статусный dashboard.

GitHub repository files, commits, branches и Pull Requests являются source of truth. Актуальное состояние проекта смотреть в `docs/agent-system/CURRENT_STATE.md` и `docs/agent-system/NEXT_STEPS.md`, а не в этом индексе. Если индекс расходится с repository files, использовать repository files и зафиксировать drift.

## Репозиторий

https://github.com/MaximKolomeets/agent-system-development

Repository visibility: public.

## Основные ветки

- `main` - стабильная версия;
- `developer` - интеграционная ветка;
- `work/<role>/*` - рабочие ветки задач (`dev-implementer-01`, `solution-architect-01`, `qa-reviewer-01`, `code-reviewer-01`, `security-reviewer-01`, `docs-maintainer-01`).

## Rulesets

- `Protect main` - Active, по ручной проверке пользователя в GitHub UI;
- `Protect developer` - Active, по ручной проверке пользователя в GitHub UI.

## Читать в начале каждого нового чата

Базовый контур:

1. `AGENTS.md`
2. `README.md`
3. `docs/agent-system/CURRENT_STATE.md`
4. `docs/agent-system/NEXT_STEPS.md`
5. `docs/agent-system/DECISION_LOG.md`

Branch/workflow/role контур:

6. `docs/agent-system/BRANCH_POLICY.md`
7. `docs/agent-system/ROLE_MODEL.md`
8. `docs/agent-system/WORKFLOW.md`
9. `docs/agent-system/PR_WORKFLOW.md`
10. `docs/agent-system/OPERATIONAL_FAST_LANE.md`
11. `docs/agent-system/CODE_REVIEW_WORKFLOW.md`
12. `docs/agent-system/LANGUAGE_POLICY.md`

Engine/contract контур:

13. `docs/agent-system/ENGINE_ENTRYPOINT.md`
14. `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`
15. `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
16. `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`
17. `docs/agent-system/CHATGPT_OPERATING_CONTRACT.md`
18. `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md`
19. `docs/agent-system/FILE_COMMENTING_STANDARD.md`

Adoption контур:

20. `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md`
21. `docs/agent-system/ADOPTION_GUIDE.md`
22. `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
23. `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`
24. `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`
25. `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`
26. `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`

Templates и journal:

27. `docs/agent-system/templates/` (включая `CODE_REVIEW_TASK_TEMPLATE.md`, `CODE_REVIEW_REPORT_TEMPLATE.md`, `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`, governance/constitution templates);
28. `docs/agent-system/engine-journal/` (`README.md`, `INDEX.md`, `templates/`).

Полный набор документов и шаблонов смотреть в каталоге `docs/agent-system/` в GitHub.

## Важно

- GitHub является source of truth для файлов, веток, PR, отчётов и состояния.
- Не использовать названия конкретных внешних проектов; для downstream-проектов использовать нейтральные формулировки.
- Vendor/tool names (Codex/Claude/Gemini/Copilot) не использовать в названиях агентов, веток, task id и report files; конкретный инструмент указывается отдельно как engine.
- `agent-system-development` - reusable methodology/template repository, а не центральный repository управления downstream-проектами.
- Задачи для engine писать на русском и начинать с `Задача для <agent-name>: <task-id>`; task id связывать с issue, PR, task id или внутренним номером работы проекта.
- Простые проверки/cleanup выполнять через Operational Fast Lane без methodology PR.
- File-changing задачи идут через `work/<role>/*`, PR и engine journal.
- Project-specific governance state создаётся только в target repository.
- Не читать `.env`; не коммитить `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Все решения фиксировать в GitHub.
