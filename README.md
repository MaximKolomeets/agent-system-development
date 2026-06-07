# agent-system-development

Проект `agent-system-development` предназначен для создания универсальной многоагентной системы разработки.

Репозиторий GitHub `MaximKolomeets/agent-system-development` является основным источником правды: здесь хранятся файлы, история изменений, ветки, Pull Request, отчеты и текущее состояние проекта.

`docs/agent-system/source/` используется только как индекс и краткий слепок состояния. Source не заменяет GitHub и не должен становиться полным хранилищем всех рабочих файлов.

Разработка ведется через ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<agent-role>/*` - рабочие ветки отдельных задач.

Инструменты-исполнители могут меняться. Роли агентов описываются через назначение и ответственность, а не через конкретный vendor или tool. Конкретный инструмент указывается отдельно как `engine`.

После bootstrap прямые изменения в `developer` запрещены без отдельного решения пользователя. Новые задачи выполняются в рабочих ветках `work/<role>/*`, затем проходят review и merge в `developer`. Перенос в `main` выполняется только после проверки интеграционной ветки.

## Repository visibility

`agent-system-development` является public repository. Это допустимо, потому что репозиторий содержит методологию агентской разработки, шаблоны, workflow и документацию.

В репозитории запрещены реальные credentials, tokens, passwords, `.env`, клиентские данные и рабочие данные.

Статус public repository не должен автоматически переноситься на target implementation repository или private downstream repository. Такие репозитории должны рассматриваться отдельно.

## Reusable new project bootstrap

Проект содержит универсальную методологию запуска новых проектов через GitHub, роли, worktree, отчеты агентов и ручной запуск engine-исполнителей.

Lifecycle описан в `docs/agent-system/PROJECT_LIFECYCLE.md`.

Практический onboarding guide находится в `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`.

Guide для применения методологии к target repository находится в `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md`.

Checklist готовности этапа находится в `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`.

Шаблон bootstrap-задачи для target repository находится в `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`.

Шаблоны для запуска нового проекта лежат в `docs/agent-system/templates/`.

Конкретные downstream/private projects не называются в public repository. Для примеров используются только нейтральные формулировки.
