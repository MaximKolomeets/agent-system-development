# agent-system-development

Проект `agent-system-development` предназначен для создания универсальной многоагентной системы разработки.

Репозиторий GitHub `MaximKolomeets/agent-system-development` является основным источником правды для самой методологии: здесь хранятся файлы, история изменений, ветки, Pull Request, отчеты и текущее состояние methodology repository.

`docs/agent-system/source/` используется только как индекс и краткий слепок состояния. Source snapshots являются производным контекстом, а не source of truth. Каноничными остаются файлы GitHub, commits, PR и branch state.

Source snapshot считается пригодным для работы только если в начале файла указаны source commit, generated timestamp и staleness policy. Если snapshot расходится с GitHub-файлами, использовать GitHub и отметить drift.

Разработка ведется через ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<agent-role>/<task-id>` - основная task branch агента;
- `work/<agent-role>/<task-id>/*` - внутренние sub-branches агента, если они нужны для локальной декомпозиции.

Канон delivery: одна substantive task дает один итоговый PR в `developer`. Engine владеет своей task branch до состояния `ready_for_merge`; review feedback исправляется в той же branch, а post-merge closure для обычного work PR уходит в batch перед release/audit boundary.

Инструменты-исполнители могут меняться. Роли агентов описываются через назначение и ответственность, а не через конкретный vendor или tool. Конкретный инструмент указывается отдельно как `engine`.

`orchestrator` помогает пользователю выбрать режим, сформулировать задачу, проверить GitHub/local state и принять follow-up. `engine` выполняет конкретную задачу в repository. `reviewer` проверяет объект review и не становится implementer без отдельного решения пользователя.

Методология поддерживает два практических режима применения:

- `lightweight solo-operator mode` - один человек использует роли как checklist и может совмещать orchestrator/reviewer decisions, но сохраняет branch, PR, journal и safety gates для file-changing tasks;
- `multi-agent governed mode` - роли разделены между агентами/исполнителями, каждая задача имеет отдельную ветку, PR, report/journal и review boundary.

Если задача простая и не меняет repository files, применять Operational Fast Lane. Если задача меняет файлы, создает PR или обновляет journal, использовать полный self-contained Engine-блок или Task File Handoff Mode.

После bootstrap прямые изменения в `developer` запрещены без отдельного решения пользователя. Новые задачи выполняются в основных ветках `work/<role>/<task>`, при необходимости используют внутренние `work/<role>/<task>/*`, затем проходят review и один итоговый merge в `developer`. Перенос в `main` выполняется только после проверки интеграционной ветки.

## Обязательное чтение

Канонический reading-list этого repository живёт здесь. `docs/agent-system/source/SOURCE_agent_system_index.md` ссылается на этот раздел и не дублирует список.

Граница: **Core** — «нужно всегда» (обязательный контекст любого чата/задачи); **Reference** — «нужно по типу задачи» (подключается, когда задача затрагивает соответствующую область). Обоснование границы — `docs/agent-system/engine-journal/output/RESULT-0004-METH-CONSOLIDATION-PLAN-01-consolidation-plan.md` §5.

Полный каталог методологии по категориям, назначению и границам: [`docs/agent-system/METHODOLOGY_MAP.md`](docs/agent-system/METHODOLOGY_MAP.md).

### Mandatory overlays by trigger

Core reading-list ниже остаётся обязательным базовым контекстом. Таблица
добавляет trigger-specific overlays: подключать их только когда задача
затрагивает соответствующий сценарий. Инвентарь файлов и категорий проверять по
[`docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`](docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml),
а не поддерживать отдельные ручные списки.

| Trigger | Mandatory overlays | Граница |
| --- | --- | --- |
| Orchestrator готовит блок для исполнителя | `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`, `docs/agent-system/templates/TASK_HEADER_COMMON.md`, `docs/agent-system/tools/orchestrator_checklist.py` | Проверяет самодостаточность блока до отправки; не заменяет review задачи. |
| Engine меняет файлы или создаёт PR | `docs/agent-system/QUALITY_FIRST_WORKFLOW.md`, `docs/agent-system/TASK_CONTRACT.md`, `docs/agent-system/JOURNAL_FINALIZATION_POLICY.md`, `docs/agent-system/tools/check_task_ready.py`, `docs/agent-system/tools/russian_first_lint.py` | Обязательны scope/checks/STOP, RESULT/INDEX finalization, Russian-first lint и ready-gate. |
| Меняется сама методология | `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`, `docs/agent-system/METHODOLOGY_MAP.md`, `docs/agent-system/PROJECT_FILE_MAP.md`, `docs/agent-system/tools/generated_eol_guard.py` | Source inventory меняется через manifest; generated artifacts регенерируются штатными tools. |
| Target adoption или source-update | `docs/agent-system/TARGET_ADOPTION_DETECTOR.md`, `docs/agent-system/ADOPTION_GUIDE.md`, `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`, `docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md` | Использовать stable methodology reference и manifest categories; не читать `developer` как downstream source. |
| Review-only или feedback loop | `docs/agent-system/CODE_REVIEW_WORKFLOW.md`, `docs/agent-system/REVIEW_AUTOLOOP.md`, `docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md` | Reviewer не становится implementer без отдельной задачи; blockers должны иметь проверяемые IDs. |
| Release, state refresh или boundary reconciliation | `docs/agent-system/RELEASE_AUTHORITY_POLICY.md`, `docs/agent-system/HUMAN_GATE_POLICY.md`, `docs/agent-system/UAT_WORKFLOW.md`, `docs/agent-system/BUSINESS_ACCEPTANCE_CHECKLIST.md`, `docs/agent-system/HOTFIX_AND_ROLLBACK_POLICY.md`, `docs/agent-system/DISASTER_RECOVERY.md`, `docs/agent-system/RELEASE_READINESS.md`, `docs/agent-system/CURRENT_STATE.md`, `docs/agent-system/NEXT_STEPS.md`, `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` | Agent готовит checks/evidence/UAT checklist; owner/PO проходит business acceptance; merge/tag/publish/sync/rollback выполняет человек. |
| Hotfix, rollback или disaster recovery | `docs/agent-system/HOTFIX_AND_ROLLBACK_POLICY.md`, `docs/agent-system/DISASTER_RECOVERY.md`, `docs/agent-system/RELEASE_AUTHORITY_POLICY.md`, `docs/agent-system/HUMAN_GATE_POLICY.md`, `docs/agent-system/BRANCH_POLICY.md`, `docs/agent-system/WORKFLOW.md` | Agent готовит branch/PR/checks/evidence; owner/architect принимает rollback decision и мержит в `main`. |

### Core (читать всегда, 10 файлов)

1. [`AGENTS.md`](AGENTS.md) (root)
2. [`README.md`](README.md) (этот файл)
3. [`docs/agent-system/CURRENT_STATE.md`](docs/agent-system/CURRENT_STATE.md)
4. [`docs/agent-system/NEXT_STEPS.md`](docs/agent-system/NEXT_STEPS.md)
5. [`docs/agent-system/ROLE_MODEL.md`](docs/agent-system/ROLE_MODEL.md)
6. [`docs/agent-system/WORKFLOW.md`](docs/agent-system/WORKFLOW.md)
7. [`docs/agent-system/BRANCH_POLICY.md`](docs/agent-system/BRANCH_POLICY.md)
8. [`docs/agent-system/CODE_REVIEW_WORKFLOW.md`](docs/agent-system/CODE_REVIEW_WORKFLOW.md)
9. [`docs/agent-system/ENGINE_ENTRYPOINT.md`](docs/agent-system/ENGINE_ENTRYPOINT.md)
10. [`docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`](docs/agent-system/ENGINE_JOURNAL_CONTRACT.md)

### Reference (читать по типу задачи)

Decisions / language / commenting:

- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/LANGUAGE_POLICY.md`
- `docs/agent-system/FILE_COMMENTING_STANDARD.md`
- `docs/agent-system/tools/russian_first_lint.py`

Operational / branch / PR / worktree:

- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/WORKTREE_GUIDE.md`

Engine, handoff и orchestrator interface:

- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`
- `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`
- `docs/agent-system/TIME_ACCOUNTING_POLICY.md`
- `docs/agent-system/COST_TRACKING_POLICY.md`
- `docs/agent-system/METRICS.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/ORCHESTRATOR_PROJECT_OPERATING_LAYER.md`
- `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`
- `docs/agent-system/tools/orchestrator_checklist.py`

Adoption:

- `docs/agent-system/ADOPTION_GUIDE.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`
- `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`
- `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`
- `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`
- `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`

Security, publication, release, CI и rulesets:

- `docs/agent-system/SECURITY_POLICY.md`
- `docs/agent-system/PUBLICATION_POLICY.md`
- `docs/agent-system/GITHUB_RULESETS.md`
- `docs/agent-system/GITHUB_TOKEN_POLICY.md`
- `docs/agent-system/CI_POLICY.md`
- `docs/agent-system/HUMAN_GATE_POLICY.md`
- `docs/agent-system/RELEASE_AUTHORITY_POLICY.md`
- `docs/agent-system/HOTFIX_AND_ROLLBACK_POLICY.md`
- `docs/agent-system/DISASTER_RECOVERY.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/UAT_WORKFLOW.md`
- `docs/agent-system/BUSINESS_ACCEPTANCE_CHECKLIST.md`

Templates, journal и навигационный индекс:

- `docs/agent-system/templates/**` (шаблоны задач, отчётов, governance pack, prompts)
- `docs/agent-system/engine-journal/**` (`docs/agent-system/engine-journal/README.md`, `docs/agent-system/engine-journal/INDEX.md`, `templates/`, `input/`, `output/`)
- `docs/agent-system/METHODOLOGY_MAP.md` (полный каталог методологии: назначение, когда применять, границы)
- `docs/agent-system/METHODOLOGY_MAP.mermaid` (визуальная карта связей)
- `docs/agent-system/source/SOURCE_agent_system_index.md` (навигационный индекс; ссылается на этот reading-list)

## Роль репозитория

`agent-system-development` - это переиспользуемый методологический и шаблонный репозиторий.

Он не является центральным репозиторием управления агентами downstream-проектов и не должен хранить рабочие ветки, project-specific состояние агентов, исходный код, секреты или рабочие отчеты конкретных target repositories.

Для каждого нового проекта методология переносится или адаптируется в target repository. После adoption проектные ветки, worktree, отчеты и Pull Request создаются в самом target repository.

Универсальные улучшения, найденные при применении методологии в downstream-проекте, можно возвращать обратно в `agent-system-development` отдельными methodology PR. Такие PR должны быть нейтральными и не должны раскрывать private data, client data, private repository URL, внутренние кодовые имена или project-specific state.

## Быстрый старт для применения методологии в другом проекте

1. Откройте файл:

`docs/agent-system/templates/ADOPTION_PROMPT.md`

2. Скопируйте prompt из раздела `Полный canonical copy/paste prompt`.
3. Вставьте его в новый чат в контексте target repository.
4. Замените placeholder `<ВСТАВИТЬ_URL_TARGET_REPOSITORY>` на URL target repository.
5. Получите первую задачу для engine в режиме `audit-only`.

Важно: первый шаг всегда audit-only. Полный docs-only adoption выполняется отдельным PR после audit и review.

## Формат задач для Engine

Задачи для `engine` формулируются на русском языке и начинаются с обязательной шапки. Шапка назначает задачу агенту, а конкретный инструмент указывается только как `engine`.

Задача для `engine` всегда выводится одним самодостаточным copy/paste-блоком. Все данные engine должны быть внутри этого блока: цель, контекст, repository, ветки, allowed files, forbidden files, preflight, проверки, STOP-условия и формат отчета.

Пользователь не должен собирать задачу из нескольких мест ответа. Manual steps выводятся отдельно и не должны быть обязательной частью engine execution data.

Перед подготовкой задачи оркестратор проверяет актуальный `agent-system-development`. Перед выполнением `engine` синхронизирует methodology repository с GitHub, если задача применяет или меняет методологию.

Русские комментарии обязательны для нужных строк/блоков в скриптах, workflow и технических файлах. `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md` является обязательным стандартом для target adoption prompts.

Все пользовательские ответы, Engine final reports, TASK/RESULT/INDEX, target-local methodology docs/templates и комментарии в файлах должны быть Russian-first. English сохраняется только для code identifiers, команд, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.

Нельзя писать "Задача для <vendor-name>", если задача назначается роли. Нужно указывать vendor-neutral роль:

```text
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>
```

`<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта, чтобы задачу, ветку, отчет и Pull Request можно было однозначно сопоставить.

## Repository visibility

`agent-system-development` является public repository. Это допустимо, потому что репозиторий содержит методологию агентской разработки, шаблоны, workflow и документацию.

В репозитории запрещены реальные credentials, tokens, passwords, `.env`, клиентские данные и рабочие данные.

Статус public repository не должен автоматически переноситься на target implementation repository или private downstream repository. Такие репозитории должны рассматриваться отдельно.

## Reusable new project bootstrap

Проект содержит универсальную методологию запуска новых проектов через GitHub, роли, worktree, отчеты агентов и ручной запуск engine-исполнителей.

Жизненный цикл нового проекта (стадии 1–11) описан в `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md` (вводная секция «Жизненный цикл (стадии 1–11)»).

Практический onboarding guide находится в `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md`.

Guide для применения методологии к существующему target repository находится в `docs/agent-system/ADOPTION_GUIDE.md` (раздел «Пошаговый existing-repo adoption»).

Режимы применения methodology repository описаны в `docs/agent-system/ADOPTION_GUIDE.md`.

Машиночитаемый manifest переносимых файлов находится в `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`.

Checklist downstream-адаптации находится в `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`.

Entrypoint для `engine` и короткого prompt находится в `docs/agent-system/ENGINE_ENTRYPOINT.md`.

Контракт repository self-discovery находится в `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`.

Feedback loop из target repository dry run в methodology repository описан в `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`.

Target project governance pack описан в `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`.

Project Constitution Framework описан в `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`.

Canonical copy/paste prompt для запуска adoption в target repository находится в `docs/agent-system/templates/ADOPTION_PROMPT.md` (раздел «Полный canonical copy/paste prompt»). Прежний файл `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлен как redirect-заглушка для внешних bookmark.

Стандарт ответа роли `orchestrator` находится в `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`.

Короткий operating contract для роли `orchestrator` находится в `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`.

Context-load bundle для онбординга оркестратора, freshness stamp (`asof`, `developer_head_sha`) и stale-поведение описаны в `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` → «Architect → Orchestrator context handoff».

Документы с prefix `ORCHESTRATOR_` являются role-based layer для роли `orchestrator`. Они не меняют vendor-neutral role model и не являются основанием использовать vendor/tool names в названиях ролей, веток, task id или report files.

Template ответа роли `orchestrator` находится в `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md`.

Prompt для запуска нового проекта (короткий стартовый prompt проектного чата и полный bootstrap prompt) находится в `docs/agent-system/templates/NEW_PROJECT_PROMPT.md`.

Контракт воспроизводимого журнала engine-задач и ответов находится в `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`.

Контракт handoff-режима для больших задач находится в `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`.

Шаблоны и индекс engine journal находятся в `docs/agent-system/engine-journal/`.

Ready-for-review PR должен содержать финализированные journal `RESULT` и `INDEX`: без unresolved placeholders, с фактическими PR URL, commit SHA, status и checks.

Стандарт русских комментариев в технических файлах находится в `docs/agent-system/FILE_COMMENTING_STANDARD.md`.

Методологическая Russian-first policy находится в `docs/agent-system/LANGUAGE_POLICY.md`.

Короткий и безопасный короткий варианты adoption prompt находятся в `docs/agent-system/templates/ADOPTION_PROMPT.md` (разделы «Короткий prompt» и «Безопасный короткий prompt»).

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

`PROJECT_CONSTITUTION.md` (target-local; канон-framework: `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md`, канон-шаблон: `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md`) - обязательный target-specific документ для target repository. Он фиксирует mission, success criteria, out-of-scope, architectural principles, одну active strategic goal, agent authority, decision authority levels и scope expansion control.

В `agent-system-development` хранится reusable framework и template. Конкретный `PROJECT_CONSTITUTION.md` создается в target repository по фактам проекта и не копирует downstream state из methodology repository.
