# METHODOLOGY_MAP - каталог и границы методологии

Назначение: единая карта методологии. Root `README.md` задает порядок чтения
Core/Reference; этот файл дает полный каталог по категориям с назначением,
ситуацией применения и границами (что не дублировать). При сомнении "куда
положить/что использовать" начинать отсюда, затем переходить в профильный канон.

Граница карты: `METHODOLOGY_MAP.md` не заменяет source-файлы и не переписывает
их правила. Карта показывает, какой документ является canonical home для темы,
и фиксирует кандидатов на будущую консолидацию без слияния документов в этом PR.

Визуальная карта связей: [`METHODOLOGY_MAP.mermaid`](METHODOLOGY_MAP.mermaid).

## Mandatory overlays by trigger

Core reading-list задаёт базовый контекст. Overlays ниже подключаются по trigger
и не должны превращаться в отдельный ручной inventory: состав source/template/
generated файлов проверяется по `ADOPTION_TRANSFER_MANIFEST.yml`.

| Trigger | Mandatory overlays | Граница |
| --- | --- | --- |
| Orchestrator готовит блок для исполнителя | `ORCHESTRATOR_RESPONSE_STANDARD.md`, `templates/TASK_HEADER_COMMON.md`, `tools/orchestrator_checklist.py` | Проверить, что один copy/paste-блок содержит baseline, scope, checks, STOP, final report и передачу. |
| Engine меняет файлы или создаёт PR | `QUALITY_FIRST_WORKFLOW.md`, `TASK_CONTRACT.md`, `JOURNAL_FINALIZATION_POLICY.md`, `tools/check_task_ready.py` | Применить acceptance/self-review, machine-readable contract, journal finalization и ready-gate. |
| Меняется сама методология | `ADOPTION_TRANSFER_MANIFEST.yml`, `METHODOLOGY_MAP.md`, `PROJECT_FILE_MAP.md`, `tools/gen_file_map.py`, `tools/gen_cloud_bundle.py`, `tools/generated_eol_guard.py` | Manifest является source inventory; generated maps/cloud обновляются tools, не руками. |
| Target adoption или source-update | `TARGET_ADOPTION_DETECTOR.md`, `ADOPTION_GUIDE.md`, `DOWNSTREAM_ADAPTATION_CHECKLIST.md`, `STABLE_METHODOLOGY_REFERENCE_POLICY.md` | Выбрать Variant A/B/C или STOP, читать stable methodology reference и применять manifest categories. |
| Review-only или feedback loop | `CODE_REVIEW_WORKFLOW.md`, `REVIEW_AUTOLOOP.md`, `SEMANTIC_COMPLETENESS_GATES.md` | Review остаётся scoped; implementation/fix-pass требует отдельного allowed scope или той же active PR branch. |
| Release, state refresh или boundary reconciliation | `RELEASE_AUTHORITY_POLICY.md`, `HUMAN_GATE_POLICY.md`, `RELEASE_READINESS.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`, `ENGINE_JOURNAL_CONTRACT.md` | Agent готовит checks/evidence; merge/tag/publish/sync/rollback и другие human-only actions выполняет человек. |

## Категории

### 1. Вход в repository и порядок чтения

- `AGENTS.md` - local instructions для работы в methodology repository.
- Root `README.md` - роль repository, обязательный reading-list Core/Reference и
  быстрый старт для применения методологии.
- `docs/agent-system/README.md` - обзор состава `docs/agent-system/`.
- `docs/agent-system/METHODOLOGY_MAP.mermaid` - визуальная карта связей между
  reading-list, manifest, orchestrator/engine/adoption/review overlays и
  generated artifacts.

Когда применять: в начале любого чата/задачи и при проверке, какой контекст
обязателен.

Граница: порядок чтения остается в root `README.md`; эта карта является полным
каталогом и не дублирует Core/Reference список построчно.

### 2. Конституция, governance и решения

- `PROJECT_CONSTITUTION_FRAMEWORK.md` - рамка mission/scope/levels/guardrails.
- `HUMAN_GATE_POLICY.md` - список действий, которые агент не выполняет сам:
  merge/tag/publish/sync, branch protection/rulesets, CI/CD, prod secrets,
  mission/strategy, удаление данных, финансы и rollback.
- `DECISION_LOG.md` - журнал решений methodology repository.
- `TARGET_PROJECT_GOVERNANCE_PACK.md` - состав governance pack для target
  repository.
- `CONTROL_MATRIX_PATTERN.md` - паттерн traceability matrix для связи
  policy-инвариантов с реализацией, тестами, CI-gates, stage, fail-mode и
  владельцем.
- `POLICY_STATUS_PATTERN.md` - паттерн target-local статусов политик
  (`canonical`/`proposed`/`draft`) и alignment "политика vs фактическая стадия
  repository".
- `ERROR_CATALOG_PATTERN.md` - паттерн стабильного словаря error/blocker codes,
  согласованного с acceptance/spec цепочкой.
- `DECISION_NOTE_GUIDE.md` - правило выбора между строкой в `DECISION_LOG.md` и
  отдельной decision note, включая Level 3/4 owner approval.

Когда применять: при изменении authority/scope/governance, human-only actions,
adoption pack или архитектурных решений; `CONTROL_MATRIX_PATTERN.md` применять для Stage 2+
target repositories или когда принят MIR-01; `POLICY_STATUS_PATTERN.md` и
`ERROR_CATALOG_PATTERN.md` применять, когда target repository нужно явно
развести статус политики, blocker codes и фактическую готовность.

Граница: "почему/что разрешено" живет здесь; "как выполнять шаги" живет в
workflow-документах; "что считается done и чем проверяется" живет в control
matrix и error catalog, не в prose policy-дубликатах. Крупные Level 3/4 решения
оформляются по `DECISION_NOTE_GUIDE.md`, а не прячутся только в PR body.

### 3. Ветки, workflow, PR и worktree

- `WORKFLOW.md` - общий рабочий цикл.
- `BRANCH_POLICY.md` - модель веток, изоляция и запрет прямого push.
- `PR_WORKFLOW.md` - оформление и проведение PR.
- `WORKTREE_GUIDE.md` - worktree-операции.
- `OPERATIONAL_FAST_LANE.md` - упрощенный трек для мелких/read-only задач.
- `templates/SUPERSEDED_BANNER.md` - machine-readable и visible banner для
  документов, заменённых новым canonical source.

Когда применять: при создании ветки, sync/checkout/pull/merge guard, подготовке
PR, пометке superseded-документов или выборе full workflow vs Operational Fast
Lane.

Граница: ветки и изоляция -> `BRANCH_POLICY.md`; последовательность шагов ->
`WORKFLOW.md`; механика PR -> `PR_WORKFLOW.md`. Не повторять правила веток в
трех местах, ссылаться на canonical home.

### 4. Роли

- `ROLE_MODEL.md` - единственный источник ролей, vendor-neutral naming и scope.

Когда применять: при формулировании task header, review boundary, handoff и
распределении ответственности.

Граница: имена ролей и ответственности живут только здесь; остальные документы
ссылаются и не создают параллельный role catalog.

### 5. Задачи, контракты, engine и journal

- `TASK_CONTRACT.md` - машиночитаемый контракт задачи: mode/scope/checks/STOP.
- `TASK_FILE_HANDOFF_CONTRACT.md` - режим передачи задачи файлом.
- `ENGINE_ENTRYPOINT.md` - точка входа engine.
- `ENGINE_SELF_DISCOVERY_CONTRACT.md` - самоопределение доступных входов.
- `ENGINE_JOURNAL_CONTRACT.md` - формат journal: TASK/RESULT/INDEX.
- `JOURNAL_FINALIZATION_POLICY.md` - финализация journal и готовность PR.
- `TIME_ACCOUNTING_POLICY.md` - обязательный учет времени для новых RESULT,
  колонка `Time` в INDEX и rollup per PR/release/project.
- `COST_TRACKING_POLICY.md` - token/cost fields, calculator и cost rollup.
- `METRICS.md` - reusable process metrics для времени, review cycles, blockers,
  token/cost и saved time estimate.

Когда применять: для любой задачи, которая меняет repository files, создает PR
или обновляет engine-journal.

Граница: контракт задачи -> `TASK_CONTRACT.md`; запись хода и итогов ->
`ENGINE_JOURNAL_CONTRACT.md` и `JOURNAL_FINALIZATION_POLICY.md`; handoff-файл ->
`TASK_FILE_HANDOFF_CONTRACT.md`. Дисциплина measured execution timestamps
(`execution_started_at`, `execution_finished_at`, `execution_duration`) живёт в
`ENGINE_JOURNAL_CONTRACT.md`; учет времени -> `TIME_ACCOUNTING_POLICY.md`;
стоимость -> `COST_TRACKING_POLICY.md`; метрики -> `METRICS.md`; entrypoint и
orchestrator contract только напоминают первый шаг engine.

### 6. Ревью, качество и полнота

- `QUALITY_FIRST_WORKFLOW.md` - pre-PR quality gate: DoR, acceptance и
  self-review.
- `CODE_REVIEW_WORKFLOW.md` - процесс review.
- `REVIEW_AUTOLOOP.md` - ограниченный reviewer/engine fix-pass.
- `EXTERNAL_REVIEW_LEDGER_PATTERN.md` - consolidation ledger для повторных
  external human review rounds и anti-loop/diminishing-returns stop.
- `MANUAL_REVIEW_CHECKLIST.md` - чек-лист ручного review.
- `SEMANTIC_COMPLETENESS_GATES.md` - семантическая полнота docs/spec.
- `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` - цепочка
  `scenario -> blocker -> fixture -> status` для acceptance/spec.

Когда применять: перед PR, при review, при fix-pass, при множественных external
human review rounds и при проверке, что spec имеет проверяемую
acceptance-цепочку.

Граница: "готовность до PR" -> `QUALITY_FIRST_WORKFLOW.md`; "как review" ->
`CODE_REVIEW_WORKFLOW.md`; "active PR feedback cycle" ->
`REVIEW_AUTOLOOP.md`; "много внешних мнений до финализации" ->
`EXTERNAL_REVIEW_LEDGER_PATTERN.md`; "полнота spec" -> `SEMANTIC_COMPLETENESS_GATES.md` и
`ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`.

### 7. Оркестрация и формат ответа

- `ORCHESTRATOR_OPERATING_CONTRACT.md` - operating contract оркестратора.
- `ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` - проектный слой оркестрации.
- `ORCHESTRATOR_RESPONSE_STANDARD.md` - стандарт ответа оркестратора.
- `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md` - правила cross-project
  consolidation.

Когда применять: при подготовке self-contained Engine-блока, handoff между
проектами, выборе target/source boundary и формировании ответа пользователю.

Граница: orchestrator не становится implementer без отдельной задачи; cross-project
consolidation не переносит private/project-specific data в public methodology.

### 8. Adoption / onboarding target repository

- `TARGET_ADOPTION_DETECTOR.md` - выбор варианта adoption: A/B/C/STOP.
- `ADOPTION_GUIDE.md` - полный маршрут adoption.
- `NEW_PROJECT_ONBOARDING_GUIDE.md` - onboarding нового проекта.
- `DOWNSTREAM_ADAPTATION_CHECKLIST.md` - чек-лист адаптации в target repository.
- `TARGET_REPOSITORY_ADOPTION_GUIDE.md` - короткий вход и pointer на полный
  маршрут.

Когда применять: перед переносом methodology в target repository, при adoption
audit, docs-only adoption, onboarding нового проекта или проверке target-local
адаптации.

Граница: "какой вариант" -> `TARGET_ADOPTION_DETECTOR.md`; "полный маршрут" ->
`ADOPTION_GUIDE.md`; "новый проект с нуля" ->
`NEW_PROJECT_ONBOARDING_GUIDE.md`; "проверить адаптацию" ->
`DOWNSTREAM_ADAPTATION_CHECKLIST.md`.

### 9. Безопасность, публикация, CI и правила GitHub

- `SECURITY_POLICY.md` - безопасность и запреты sensitive data.
- `templates/THREAT_MODEL_TEMPLATE.md` - target-local threat model:
  `Угроза -> Контроль -> Тест -> CI-gate -> severity -> этап`.
- `CI_POLICY.md` - CI, blocking checks и supply-chain.
- `GITHUB_RULESETS.md` - защита веток и required checks.
- `GITHUB_TOKEN_POLICY.md` - токены/доступы.
- `PUBLICATION_POLICY.md` - что публикуется.
- `RELEASE_AUTHORITY_POLICY.md` - кто может merge/tag/publish/sync и какие
  actor/evidence поля должны быть в release-sensitive `RESULT`.
- `FILE_COMMENTING_STANDARD.md` - комментарии в файлах.

Когда применять: при изменении public-facing docs, CI/checks, branch protection,
доступов, release/tag/sync/publish authority, publication boundary,
security/privacy risk model или комментариев в технических файлах.

Граница: secret/privacy policy -> `SECURITY_POLICY.md`; GitHub branch protection
-> `GITHUB_RULESETS.md`; CI gates -> `CI_POLICY.md`; threat table и residual
risks -> target-local `THREAT_MODEL.md` из
`templates/THREAT_MODEL_TEMPLATE.md`; release-sensitive authority ->
`RELEASE_AUTHORITY_POLICY.md` + `HUMAN_GATE_POLICY.md`; language/commenting style
-> `LANGUAGE_POLICY.md` и `FILE_COMMENTING_STANDARD.md`.

### 10. Кросс-проектный feedback и source consumers

- `METHODOLOGY_FEEDBACK_LOOP.md` - target -> methodology improvements.
- `DOWNSTREAM_FEEDBACK_LOOP.md` - methodology -> target adaptation loop.
- `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md` - sanitization downstream
  feedback.
- `SOURCE_CONSUMERS.md` - scaffold registry of source consumers.

Когда применять: когда downstream опыт нужно вернуть в reusable methodology или
когда methodology update нужно безопасно довести до target repositories.

Граница: improvements вверх -> `METHODOLOGY_FEEDBACK_LOOP.md`; adaptation вниз
-> `DOWNSTREAM_FEEDBACK_LOOP.md`; private/project-specific filtering ->
`DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`; реальные consumers не фиксируются в
public methodology repository.

### 11. Source, manifest, generated maps, cloud и стабильность

- `ADOPTION_TRANSFER_MANIFEST.yml` - источник истины состава transferable source,
  templates, history_state, journal, scaffold и generated.
- `PROJECT_FILE_MAP.md` - генерируемая карта из manifest (не править руками).
- `STABLE_METHODOLOGY_REFERENCE_POLICY.md` - стабильная ссылка на методологию.
- `cloud/**` - генерируемый bundle для облачного оркестратора.

Когда применять: при добавлении/удалении source/template files, adoption transfer,
generated parity checks, cloud context handoff и выборе stable reference.

Граница: source-set меняется через manifest; `PROJECT_FILE_MAP.md` и `cloud/**`
регенерируются штатными tools; stable downstream reference по умолчанию не
указывает на `developer`/`work/*`.

### 12. Проверочные инструменты

- `tools/check_task_ready.py` - интегральный readiness gate.
- `tools/validate_commit_message.py` - read-only gate формата commit metadata
  по `LANGUAGE_POLICY`.
- `tools/validate_id_references.py` - read-only gate целостности methodology
  ID references.
- `tools/gen_cloud_bundle.py` - генерация/check cloud bundle.
- `tools/gen_file_map.py` - генерация/check `PROJECT_FILE_MAP.md`.
- `tools/generated_eol_guard.py` - классификация generated/cloud EOL/whitespace
  noise vs content change.
- `tools/orchestrator_checklist.py` - pre-send sanity-check self-contained
  блока для исполнителя (engine).
- `tools/validate_task_contract.py` - validation `task_contract`.

Когда применять: перед PR и при любых изменениях source/manifest/generated/journal.

Граница: tools являются source-controlled guard infrastructure; правила workflow
пишутся в docs, а scripts реализуют проверяемые gates.

### 13. Релиз, стадии, язык

- `RELEASE_READINESS.md` - готовность к release.
- `STAGE_2_COMPLETION_CHECKLIST.md` - завершение stage 2.
- `LANGUAGE_POLICY.md` - Russian-first policy и допустимый English для technical
  identifiers, включая visible text для superseded banner рядом с machine-readable
  comment.

Когда применять: перед release boundary, stage completion, state refresh и при
проверке языка docs/TASK/RESULT/INDEX/PR metadata.

Граница: release gate не смешивается с ordinary work PR lifecycle; language policy
не переводит code identifiers, flags, paths и literal external names.

### 14. Текущее состояние, backlog и derived context

- `CURRENT_STATE.md` - актуальное состояние methodology repository.
- `NEXT_STEPS.md` - ближайшие шаги.
- `BACKLOG.md` - backlog methodology work.
- `source/**` - derived source snapshots/indexes.
- `agents/**` - исторические agent notes/reports.
- `engine-journal/**` - operational journal scaffold/history.

Когда применять: при state-refresh, release prep, handoff, closure/audit boundary
и восстановлении контекста.

Граница: state/history docs не являются reusable source для verbatim target-copy;
target repository создает собственное состояние по target facts.

## Docs-taxonomy для target repositories (MIR-06)

Куда что класть в target repository:

| Тип | Каталог |
| --- | --- |
| Методология/governance (адаптированная) | `docs/agent-system/` |
| Архитектурные решения (ADR), specs | `docs/architecture/` |
| Доменные модели/типы | `docs/domain/` |
| Prompt-facing правила/схемы | `docs/prompts/` |
| Product-specific docs/runners | `docs/project/` или project-local canonical path |
| Шаблоны | `docs/architecture/templates/` или `docs/agent-system/templates/` |
| Synthetic fixtures | `fixtures/` |
| Control traceability (если принят MIR-01) | `docs/agent-system/CONTROL_MATRIX.md` |
| Статусы политик и repo alignment | `docs/agent-system/POLICY_STATUS.md` |
| Стабильные error/blocker codes | `docs/agent-system/ERROR_CATALOG.md` |
| Крупные decision notes | `docs/agent-system/decisions/` или target-local ADR каталог |

Правило: один тип - один canonical каталог; не плодить параллельные дома.

Граница: эта taxonomy является default для target repositories, но local
instructions target repository и существующая архитектура имеют приоритет после
явной фиксации решения.

## Кандидаты на консолидацию (follow-up, не в этом PR)

- `TARGET_REPOSITORY_ADOPTION_GUIDE.md` -> pointer/свертка в `ADOPTION_GUIDE.md`.
- `MANUAL_REVIEW_CHECKLIST.md` -> раздел в `CODE_REVIEW_WORKFLOW.md`.
- Проверить границы review/quality и adoption-кластеров по этой карте.
