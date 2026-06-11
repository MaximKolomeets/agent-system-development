# agent-system-development

Проект `agent-system-development` предназначен для создания универсальной многоагентной системы разработки.

Репозиторий GitHub `MaximKolomeets/agent-system-development` является основным источником правды для самой методологии: здесь хранятся файлы, история изменений, ветки, Pull Request, отчеты и текущее состояние methodology repository.

`docs/agent-system/source/` используется только как индекс и краткий слепок состояния. Source не заменяет GitHub и не должен становиться полным хранилищем всех рабочих файлов.

Разработка ведется через ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<agent-role>/*` - рабочие ветки отдельных задач.

Инструменты-исполнители могут меняться. Роли агентов описываются через назначение и ответственность, а не через конкретный vendor или tool. Конкретный инструмент указывается отдельно как `engine`.

После bootstrap прямые изменения в `developer` запрещены без отдельного решения пользователя. Новые задачи выполняются в рабочих ветках `work/<role>/*`, затем проходят review и merge в `developer`. Перенос в `main` выполняется только после проверки интеграционной ветки.

## Роль репозитория

`agent-system-development` - это переиспользуемый методологический и шаблонный репозиторий.

Он не является центральным репозиторием управления агентами downstream-проектов и не должен хранить рабочие ветки, project-specific состояние агентов, исходный код, секреты или рабочие отчеты конкретных target repositories.

Для каждого нового проекта методология переносится или адаптируется в target repository. После adoption проектные ветки, worktree, отчеты и Pull Request создаются в самом target repository.

Универсальные улучшения, найденные при применении методологии в downstream-проекте, можно возвращать обратно в `agent-system-development` отдельными methodology PR. Такие PR должны быть нейтральными и не должны раскрывать private data, client data, private repository URL, внутренние кодовые имена или project-specific state.

## Быстрый старт для применения методологии в другом проекте

1. Откройте файл:

`docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`

2. Скопируйте prompt из раздела `Copy/paste prompt`.
3. Вставьте его в новый чат в контексте target repository.
4. Замените placeholder `<ВСТАВИТЬ_URL_TARGET_REPOSITORY>` на URL target repository.
5. Получите первую задачу для engine в режиме `audit-only`.

Важно: первый шаг всегда audit-only. Полный docs-only adoption выполняется отдельным PR после audit и review.

## Формат задач для Engine

Задачи для `engine` формулируются на русском языке и начинаются с обязательной шапки. Шапка назначает задачу агенту, а конкретный инструмент указывается только как `engine`.

Задача для `engine` всегда выводится одним самодостаточным copy/paste-блоком. Все данные engine должны быть внутри этого блока: цель, контекст, repository, ветки, allowed files, forbidden files, preflight, проверки, STOP-условия и формат отчета.

Пользователь не должен собирать задачу из нескольких мест ответа. Manual steps выводятся отдельно и не должны быть обязательной частью engine execution data.

Перед подготовкой задачи ChatGPT проверяет актуальный `agent-system-development`. Перед выполнением `engine` синхронизирует methodology repository с GitHub, если задача применяет или меняет методологию.

Русские комментарии обязательны для нужных строк/блоков в скриптах, workflow и технических файлах. `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md` является обязательным стандартом для target adoption prompts.

Нельзя всегда писать "Задача для Codex", если задача назначается конкретному агенту. Нужно указывать role-based имя агента:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

`<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта, чтобы задачу, ветку, отчет и Pull Request можно было однозначно сопоставить.

## Repository visibility

`agent-system-development` является public repository. Это допустимо, потому что репозиторий содержит методологию агентской разработки, шаблоны, workflow и документацию.

В репозитории запрещены реальные credentials, tokens, passwords, `.env`, клиентские данные и рабочие данные.

Статус public repository не должен автоматически переноситься на target implementation repository или private downstream repository. Такие репозитории должны рассматриваться отдельно.

## Reusable new project bootstrap

Проект содержит универсальную методологию запуска новых проектов через GitHub, роли, worktree, отчеты агентов и ручной запуск engine-исполнителей.

Lifecycle описан в `docs/agent-system/PROJECT_LIFECYCLE.md`.

Практический onboarding guide находится в `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`.

Guide для применения методологии к target repository находится в `docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md`.

Режимы применения methodology repository описаны в `docs/agent-system/ADOPTION_GUIDE.md`.

Машиночитаемый manifest переносимых файлов находится в `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`.

Checklist downstream-адаптации находится в `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`.

Entrypoint для `engine` и короткого prompt находится в `docs/agent-system/ENGINE_ENTRYPOINT.md`.

Контракт repository self-discovery находится в `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`.

Feedback loop из target repository dry run в methodology repository описан в `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`.

Target project governance pack описан в `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`.

Project Constitution Framework описан в `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`.

Canonical copy/paste prompt для запуска adoption в target repository находится в `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`.

Стандарт ответа ChatGPT находится в `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md`.

Короткий operating contract для ChatGPT находится в `docs/agent-system/CHATGPT_OPERATING_CONTRACT.md`.

Template ответа ChatGPT находится в `docs/agent-system/templates/CHATGPT_RESPONSE_TEMPLATE.md`.

Шаблон стартового prompt для нового project chat находится в `docs/agent-system/templates/PROJECT_CHAT_START_PROMPT_TEMPLATE.md`.

Контракт воспроизводимого журнала engine-задач и ответов находится в `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`.

Шаблоны и индекс engine journal находятся в `docs/agent-system/engine-journal/`.

Стандарт русских комментариев в технических файлах находится в `docs/agent-system/FILE_COMMENTING_STANDARD.md`.

Шаблон короткого prompt для adoption mode находится в `docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md`.

Checklist готовности этапа находится в `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`.

Шаблон bootstrap-задачи для target repository находится в `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`.

Шаблон audit-only adoption task находится в `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`.

Шаблон docs-only adoption task находится в `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`.

Шаблон governance pack находится в `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`.

Шаблон project constitution находится в `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md`.

Шаблоны для запуска нового проекта лежат в `docs/agent-system/templates/`.

Конкретные downstream/private projects не называются в public repository. Для примеров используются только нейтральные формулировки.

## Target project governance pack

`agent-system-development` предоставляет не только агентные роли, branch workflow и task templates, но и reusable набор project governance документов для target repository.

Governance pack помогает target repository удерживать:

- mission и success criteria;
- цель и non-goals;
- roadmap;
- backlog;
- current state;
- next steps;
- decisions;
- project guardrails;
- engine registry;
- decision authority и scope expansion control;
- handoff для нового чата или новой рабочей сессии.

Project-specific governance state создается и обновляется только в target repository. В public methodology repository хранятся только универсальные шаблоны, правила adoption и checklist.

## Project Constitution Framework

`PROJECT_CONSTITUTION.md` - обязательный target-specific документ для target repository. Он фиксирует mission, success criteria, out-of-scope, architectural principles, одну active strategic goal, agent authority, decision authority levels и scope expansion control.

В `agent-system-development` хранится reusable framework и template. Конкретный `PROJECT_CONSTITUTION.md` создается в target repository по фактам проекта и не копирует downstream state из methodology repository.
