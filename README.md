# agent-system-development

Проект `agent-system-development` предназначен для создания универсальной многоагентной системы разработки.

Репозиторий GitHub `MaximKolomeets/agent-system-development` является основным источником правды для самой методологии: здесь хранятся файлы, история изменений, ветки, Pull Request, отчеты и текущее состояние methodology repository.

`docs/agent-system/source/` используется только как индекс и краткий слепок состояния. Source snapshots являются производным контекстом, а не source of truth. Каноничными остаются файлы GitHub, commits, PR и branch state.

Source snapshot считается пригодным для работы только если в начале файла указаны source commit, generated timestamp и staleness policy. Если snapshot расходится с GitHub-файлами, использовать GitHub и отметить drift.

Разработка ведется через ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<agent-role>/*` - рабочие ветки отдельных задач.

Инструменты-исполнители могут меняться. Роли агентов описываются через назначение и ответственность, а не через конкретный vendor или tool. Конкретный инструмент указывается отдельно как `engine`.

`orchestrator` помогает пользователю выбрать режим, сформулировать задачу, проверить GitHub/local state и принять follow-up. `engine` выполняет конкретную задачу в repository. `reviewer` проверяет объект review и не становится implementer без отдельного решения пользователя.

Методология поддерживает два практических режима применения:

- `lightweight solo-operator mode` - один человек использует роли как checklist и может совмещать orchestrator/reviewer decisions, но сохраняет branch, PR, journal и safety gates для file-changing tasks;
- `multi-agent governed mode` - роли разделены между агентами/исполнителями, каждая задача имеет отдельную ветку, PR, report/journal и review boundary.

Если задача простая и не меняет repository files, применять Operational Fast Lane. Если задача меняет файлы, создает PR или обновляет journal, использовать полный self-contained Engine-блок или Task File Handoff Mode.

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

Все пользовательские ответы, Engine final reports, TASK/RESULT/INDEX, target-local methodology docs/templates и комментарии в файлах должны быть Russian-first. English сохраняется только для code identifiers, команд, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.

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

Документы с prefix `CHATGPT_` являются adapter/implementation-specific layer для одного orchestrator-интерфейса. Они не меняют vendor-neutral role model и не являются основанием использовать vendor/tool names в названиях ролей, веток, task id или report files.

Template ответа ChatGPT находится в `docs/agent-system/templates/CHATGPT_RESPONSE_TEMPLATE.md`.

Шаблон стартового prompt для нового project chat находится в `docs/agent-system/templates/PROJECT_CHAT_START_PROMPT_TEMPLATE.md`.

Контракт воспроизводимого журнала engine-задач и ответов находится в `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`.

Контракт handoff-режима для больших задач находится в `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`.

Шаблоны и индекс engine journal находятся в `docs/agent-system/engine-journal/`.

Ready-for-review PR должен содержать финализированные journal `RESULT` и `INDEX`: без unresolved placeholders, с фактическими PR URL, commit SHA, status и checks.

Стандарт русских комментариев в технических файлах находится в `docs/agent-system/FILE_COMMENTING_STANDARD.md`.

Методологическая Russian-first policy находится в `docs/agent-system/LANGUAGE_POLICY.md`.

Шаблон короткого prompt для adoption mode находится в `docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md`.

Checklist готовности этапа находится в `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`.

Шаблон bootstrap-задачи для target repository находится в `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`.

Шаблон audit-only adoption task находится в `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`.

Шаблон docs-only adoption task находится в `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`.

Review-only workflow для code review / external review / consulting review находится в `docs/agent-system/CODE_REVIEW_WORKFLOW.md`.

Шаблон review-задачи находится в `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md`.

Шаблон review-отчета находится в `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md`.

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
