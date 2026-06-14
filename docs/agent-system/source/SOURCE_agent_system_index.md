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

Канонический reading-list — раздел **«Обязательное чтение»** в `README.md` (Core и Reference).

Здесь список не дублируется, чтобы не было drift между навигационным индексом и каноном. Если возникает расхождение между этим файлом и `README.md`, использовать `README.md`.

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
