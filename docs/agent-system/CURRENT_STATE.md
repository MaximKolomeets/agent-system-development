# CURRENT_STATE

## Machine-readable task contract

Текущее состояние методологии включает preferred `task_contract` frontmatter для новых write-action Engine-задач. Канон: `docs/agent-system/TASK_CONTRACT.md`; lightweight read-only validator: `docs/agent-system/tools/validate_task_contract.py`. Prose остаётся human explanation, а `task_contract` является source of truth для mode/scope/checks/STOP; конфликт contract/prose означает `STOP`. `TASK_CONTRACT.md` входит в default cloud/orchestrator bundle как `13_TASK_CONTRACT.md`.

Дата: 2026-06-26

Проект: Создание агентской системы

Репозиторий: `MaximKolomeets/agent-system-development`

Repository visibility: public.

## Актуальное состояние

### Постоянные возможности (Standing capabilities)

Методология выпущена и поддерживается как reusable methodology/template repository. Этот слой описывает устойчивые возможности; он меняется только при реальном изменении методологии, а не после каждого work/release/sync PR.

- Governance правила 1-4 закреплены: `main` обновляется только human-merged release PR `developer -> main`, рабочие ветки изолированы в `work/<role>/<task>`, pre-commit branch-guard обязателен, repository sync/checkout guard останавливает работу на dirty tree.
- Agent-owned task branch workflow закреплен: одна substantive task ведется в основной `work/<role>/<task-id>` branch, внутренние `work/<role>/<task-id>/*` sub-branches допустимы только внутри задачи, а `developer` получает один итоговый PR; review feedback исправляется в той же task branch до `ready_for_merge`.
- Review autoloop закреплён как bounded state-machine для active work PR: reviewer feedback остаётся в PR агента, engine fix-pass идёт в той же task branch, blockers имеют IDs/classes/verification commands, machine-only blockers закрываются machine-check closure, semantic/mixed blockers требуют minimal re-review, цикл ограничен `max_review_cycles`, approve-equivalent даёт `architect:ready-to-merge`, но merge в `developer` остаётся human-only.
- Lightweight task readiness gate добавлен как read-only tooling: `docs/agent-system/tools/check_task_ready.py` агрегирует branch guard, changed files summary, `git diff --check`, conditional generated parity checks, filename-only sensitive scan, strict added-line secret scan и TASK/RESULT placeholder scan перед push/PR/fix-pass/review-comment.
- Strict added-line scan блокирует headers `Authorization` независимо от auth-схемы и выводит только counts/filenames/categories, без matching values.
- Sanitized downstream feedback loop закреплён как reusable methodology boundary: `DOWNSTREAM_FEEDBACK_LOOP.md` задаёт intake/classification/backlog/release adoption flow, `DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md` задаёт forbidden content, redaction rules и reviewer checklist. Target repositories получают эти правила только после `main`, release tag или published Source/cloud snapshot.
- Generated EOL guard добавлен как read-only tooling: `docs/agent-system/tools/generated_eol_guard.py` классифицирует generated/cloud изменения как `content_changed`, `eol_only_changed` или `whitespace_only_changed`, а `check_task_ready.py` вызывает его условно при generated/bundle-source diff.
- Operational/source/template scope деперсонализирован: канон заголовка `Задача для <роль>`, роли отделены от исполнителя, vendor/tool literals в active operational scope заменены нейтральными placeholders.
- Ordinary terminal state закреплён: обычный task PR завершается на `architect_ready` / `human_merge_allowed` с PR URL и reviewed head SHA; отдельный post-merge closure PR после каждого ordinary merge не создаётся.
- GitHub merge facts authority закреплён: GitHub PR metadata является source of truth для PR state, `merged_at`, merge commit SHA и PR URL; отсутствие этих фактов в ordinary `RESULT` не является blocker.
- Boundary reconciliation разрешена только перед release/audit boundary, при explicit architect request или для batch reconciliation; release/audit gates могут требовать closure-stamp/status+PR URL только внутри заданного boundary scope.
- `ADOPTION_TRANSFER_MANIFEST.yml` является авторитетным manifest с категориями `source`, `template`, `target_generated`, `history_state`, `journal`, `scaffold`, `generated`.
- `PROJECT_FILE_MAP.md` генерируется из manifest через `docs/agent-system/tools/gen_file_map.py`; `--check` входит в release-gate/fast-lane parity.
- Проверки generated text artifacts являются content-oriented и EOL-safe на Windows: `gen_file_map.py --check` и `gen_cloud_bundle.py --check` входят в release-gate; freshness metadata в generated bundle является информационной, а gate проверяет содержательный parity.
- `methodology_reference` поддерживает обязательный `source_commit` и опциональные human-readable `source_tag`/`release_tag`; commit SHA остаётся reproducibility anchor.
- Для новых TASK/RESULT каноническое measured-поле окончания выполнения — `execution_finished_at`; drift-имя `execution_completed_at` остаётся только append-only историей и не является alias для новых записей.
- Source Delta является обязательным standing output в final report, `RESULT` и review-gate.
- Architect -> Orchestrator context handoff закреплён: bundle определяется в manifest, `docs/agent-system/cloud/**` является generated staging folder, `gen_cloud_bundle.py --check` проверяет content-parity, а `asof`/`developer_head_sha` в `cloud/00_README.md` информационные.
- Adoption templates синхронизированы с актуальными категориями manifest и Source Delta; descriptive headings в active adopter-facing docs приведены к Russian-first виду с сохранением technical literals/aliases; active audit/editorial ниты закрываются отдельными fix-cycle задачами без переписывания append-only history.
- Stable methodology reference для target/downstream задач закреплён: по умолчанию `origin/main` / `main`; `developer`, `work/*`, dirty local methodology tree и open methodology PR branch не являются downstream source of truth. GitHub-facing artifacts, PR title/body, commit messages, review summaries и final reports соблюдают Russian-first policy.

### Текущий указатель (Current pointer)

Авторитет текущего journal state: `docs/agent-system/engine-journal/INDEX.md` и соответствующие `RESULT-*` closure-stamps. Этот файл не дублирует номера work/release/sync PR как source of truth; если здесь встречается конкретный номер PR в исторической летописи ниже, он является информационной историей, а не актуальным pointer.

Latest release определяется состоянием remote веток/tags (`main`, `developer`) и release/sync фактами в journal. Перед каждым release выполнить state-refresh для `CURRENT_STATE.md` и `NEXT_STEPS.md`, затем regenerated `docs/agent-system/cloud/**` и оба parity check.

Текущий фокус: `METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01` добавляет reusable downstream feedback loop и sanitization policy. `METH-DOWNSTREAM-FEEDBACK-LOOP-VERIFICATION-01` закрыта как sanitized/reusable variant: production generator/tests/fixtures, target repositories, runtime, Docker, CI, branch protection, release/tag и real/private data не менялись. Следующий возможный шаг после merge и scoped review: release candidate `v1.4.0`, чтобы новые methodology docs стали stable source для downstream adoption.

State-level n-01 по live/current vendor literal перепроверен: в live/current секциях конкретный vendor/tool literal отсутствует; единственное найденное упоминание находится в append-only historical section ниже и не ретрофитится.

Текущий этап: консолидация методологии (`RESULT-0004`, `METH-CONSOLIDATION-PLAN-01`) завершена — все execution-PR C1–C6 смержены в `developer`. До неё methodology hardening task `METH-OPERABILITY-01` была завершена и merged, проведён `REVIEW-INITIAL-01` (review-only) и consistency-проход `METH-CONSISTENCY-01`.

Итог консолидации (journal 0004–0011, все closure-записи закрыты):

- **C1 (0006)** — reading-list разнесён на Core (10) + Reference; канон — раздел «Обязательное чтение» в `README.md`, `source/SOURCE_agent_system_index.md` ссылается без дубля.
- **C2 (0007)** — `methodology_reference` сведён к одному канону (`ENGINE_ENTRYPOINT.md`), `source_snapshot` — к `source/README.md`; дубли заменены ссылками; в manifest пометка «human canon».
- **C3 (0008)** — два adoption-prompt слиты в канон `templates/ADOPTION_PROMPT.md` (короткий + безопасный короткий + полный); прежние файлы — redirect-заглушки.
- **C4 (0011)** — adoption-guides слиты: existing-repo шаги → `ADOPTION_GUIDE.md` (раздел «Пошаговый existing-repo adoption», branch-flow канон там же); стадийная модель → `NEW_PROJECT_ONBOARDING_GUIDE.md` (секция «Жизненный цикл (стадии 1–11)»); `DOWNSTREAM_ADAPTATION_CHECKLIST.md` дедуплицирован и оставлен отдельным pre-merge gate; `TARGET_REPOSITORY_ADOPTION_GUIDE.md` и `PROJECT_LIFECYCLE.md` — redirect-заглушки.
- **C5 (0009 C5A + 0010 C5B)** — templates cleanup: `REVIEW_TEMPLATE` слит в `CODE_REVIEW_REPORT_TEMPLATE.md`; общий task-header вынесен в канон `templates/TASK_HEADER_COMMON.md` (DEVELOPMENT/RESEARCH ссылаются, тела раздельные); new-project prompt'ы слиты в `templates/NEW_PROJECT_PROMPT.md`; `AGENT_REPORT_TEMPLATE`/`DECISION_TEMPLATE` wired ссылками.
- **C6 (0005)** — review-задачи теперь всегда журналируют TASK+RESULT (`Journal trace: always`); `Report delivery: chat` относится только к телу отчёта.

Накопленные redirect-заглушки очищены в `METH-BACKLOG-POLISH`: 6 history-only заглушек удалены, живые ссылки перенаправлены на каноны; `templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` оставлена заглушкой для внешних bookmark. Политика «broken-ссылки в append-only истории допустимы» зафиксирована в `DECISION_LOG.md`.

В `METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01` путь `TARGET_REPOSITORY_ADOPTION_GUIDE.md` создан заново как живой короткий stable-reference entrypoint; это не возврат старой redirect-заглушки, удаленной в `METH-BACKLOG-POLISH`.

Bootstrap перенесен в `main` через PR #1. PR-1b перенесен в `main` через PR #2. Public repository и Active rulesets status зафиксированы через PR-1c.

Rulesets:

- `Protect main` - Active, по ручной проверке пользователя в GitHub UI;
- `Protect developer` - Active, по ручной проверке пользователя в GitHub UI.

`main` и `developer` синхронизированы на момент старта PR-1d. Worktree workflow уже зафиксирован через PR-1d.

Создан worktree для docs-maintainer:

```text
C:\Neural\worktrees\agent-system-development\docs-maintainer-01
```

Активная рабочая ветка:

```text
нет постоянной активной ветки; каждая новая задача создается в work/<role>/<task>.
```

Ветки:

- `main` - стабильная ветка;
- `developer` - интеграционная ветка;
- `work/<role>/<task>` - основная task branch;
- `work/<role>/<task>/*` - внутренние sub-branches той же задачи, если нужны.

После bootstrap прямые изменения в `developer` запрещены без отдельного разрешения пользователя.

Все следующие задачи должны идти через `work/<role>/*`.

Правила именования:

- Конкретные vendor/tool names не используются в названиях агентов;
- Конкретный инструмент может использоваться только как исполнитель (engine) по прямому заданию пользователя;
- роли агентов не зависят от конкретного vendor/tool.

PR-1e добавил GitHub Actions guardrail для forbidden tracked files.

PR-2a завершен и добавил lifecycle/templates запуска нового проекта.

PR-2b завершен и добавил practical onboarding guide для запуска нового проекта.

PR-2c завершен и обновил GitHub Actions checkout action для совместимости с Node.js 24.

PR-2d подготовил target repository adoption readiness pack.

PR-2e завершен и добавил engine entrypoint, repository self-discovery contract и short prompt adoption mode.

PR-2f завершен и добавил methodology feedback loop.

PR-2g завершен и добавил adoption modes, transfer manifest, downstream checklist и minimal first PR rule.

PR-2h завершен и добавил reusable task templates для `audit-only` и `docs-only adoption`.

PR-2i завершен и уточнил роль `agent-system-development` как reusable methodology/template repository, а также закрепил обязательную русскоязычную шапку задач для `engine`.

PR-2j завершен и добавил target project governance pack: dashboard, roadmap, backlog, current state, next steps, decision log, project guardrails, engine registry и handoff rules для target implementation repositories.

PR-2k завершен и добавил Project Constitution Framework: reusable framework, `PROJECT_CONSTITUTION_TEMPLATE.md`, Agent Authority Matrix, Decision Authority Levels, Scope Expansion Control и Governance Review Checklist для target implementation repositories.

PR-2l завершен и добавил canonical copy/paste prompt для запуска adoption в target repository из нового project chat.

PR-2m завершен и merged в `developer` через PR #46.

PR-2m закрепил один самодостаточный Engine-блок на одну engine-задачу.

PR-2m закрепил обязательную проверку актуального `agent-system-development` перед формированием и выполнением задач.

PR-2m закрепил language consistency rule для target governance docs.

PR-2m закрепил `FILE_COMMENTING_STANDARD` для русских комментариев в нужных строках/блоках скриптов и технических файлов.

PR-2m закрепил отдельный нейтральный блок для предложений по доработке methodology repository без раскрытия private downstream data.

PR-2n merged в `developer` через PR #47 и обновил state docs, Source index и readiness checklist после PR-2m.

PR-2o merged в `developer` через PR #48 и зафиксировал release readiness snapshot.

PR-2p открыл release PR #49 из `developer` в `main` без merge.

PR-2q merged в `developer` через PR #50 и исправил blocker review comments перед merge release PR #49:

- после синхронизации methodology repository engine должен явно вернуться в target repository перед target checks или target changes;
- methodology sync считается валидным только если локальный `HEAD` равен `origin/<METHODOLOGY_BASE_BRANCH>` после `git pull --ff-only`.

PR-2r добавляет стандарт engine journal:

- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- `docs/agent-system/engine-journal/`;
- task/result templates для воспроизводимой связи task -> result -> branch -> PR -> commit/result.

PR-2w merged в `developer` через PR #62, release PR #63 и sync PR #64.

PR-2w закрепил Russian-first language policy как отдельный reusable contract для оркестратора, `engine`, TASK/RESULT/INDEX, target-local docs/templates и комментариев в файлах.

PR-2x добавляет Post-merge Journal Closure:

- после merge рабочего PR, release PR или sync PR target `RESULT` и `INDEX` не должны оставаться в pre-merge статусах;
- journal closure фиксирует PR status `merged`, merge commit SHA, `merged_at` при доступности, release/sync PR данные при наличии;
- stale statuses `PR open`, `ready for review`, `draft open`, `pending at file materialization` и `see Engine final report` становятся blockers после merge.

PR-3a hardens new repository bootstrap branch rules:

- `new empty repository bootstrap` отделен от `existing repository adoption`;
- для `standard developer workflow` ветка `developer` обязательна до первой рабочей ветки;
- `fallback-to-main` для рабочих PR запрещен;
- отсутствие `developer` является bootstrap blocker или explicit bootstrap creation step.

PR-3a merged в developer через PR #71. Bootstrap gate для новых repository закреплен.

PR-3b merged в developer через PR #74. Post-merge state cleanup завершен.

PR-3c merged в developer через PR #77. Vendor-neutral review-only workflow для code review / external review / consulting review закреплен.

- reviewer roles отделены от engine names;
- branch и report filenames не используют vendor/tool names;
- review-only PR идет через `work/code-reviewer-01/<task-id>` в `developer`;
- findings превращаются в отдельные implementation PR только после решения пользователя.

После PR-3c следующим шагом было использовать `CODE_REVIEW_TASK_TEMPLATE.md` для первого безопасного review target implementation repository или выбрать следующий methodology hardening PR.

PR-3d merged в developer через PR #80. Post-merge state cleanup после PR-3c завершен.

PR-3e merged в developer через PR #83, перенесен в main через PR #84 и синхронизирован обратно в developer через PR #85.

PR-3e закрепил:

- Operational Fast Lane остается read-only/status/cleanup-only;
- write-action recommendations требуют полного self-contained Engine-блока;
- Engine-блоки должны соблюдать Russian-first policy для пользовательских заголовков и описаний;
- PR head SHA policy уточняется без self-referential commit loop.

PR-3g усиливает reusable правила: task lifecycle после merge/release/sync считается закрытым только когда GitHub PR state и target journal RESULT/INDEX state согласованы.

`METH-GUARDRAILS-01` merged в `developer` через PR #92, перенесен в `main` через PR #93 и синхронизирован обратно в `developer` через PR #94.

`METH-GUARDRAILS-01` закрепил:

- review-агенты работают review-only по умолчанию и не становятся исполнителями разработки без отдельной задачи;
- review findings не превращаются в самостоятельные задачи исполнителя (engine) без решения пользователя;
- review branch/report naming остается role-based и vendor-neutral;
- фактическая branch policy для review использует `work/<role>/<task>`, а не отдельный `review/*` namespace;
- review-отчет по умолчанию возвращается в чат, а сохранение в repository требует явного docs-only разрешения;
- final report после PR/merge должен содержать конкретный блок локальных действий для синхронизации repository пользователя.

`METH-OPERABILITY-01` merged в `developer` через PR #95, перенесён в `main` через PR #96, синхронизирован обратно в `developer` через PR #97 и закрыт в journal через PR #98.

`METH-OPERABILITY-01` закрепил:

- lightweight solo-operator mode и multi-agent governed mode;
- явные boundaries для `orchestrator`, `engine` и `reviewer`;
- policy, что `ORCHESTRATOR_*` документы являются role-based layer, а не role naming exception;
- `methodology_reference` с commit SHA для target adoption/update;
- drift-control для `docs/agent-system/source/**` snapshots;
- ceremony/token budget policy и anti-overengineering checkpoint;
- усиленную sanitization policy для Methodology feedback.

`REVIEW-INITIAL-01` выполнен как review-only проход по обновлённой методологии: вердикт Hold, blocker'ов нет, отчёт возвращён в чат. Findings — класса Желательно/Опционально (stale state/source docs, vendor name в заголовке review-шаблонов, рассинхрон token-документа).

`METH-CONSISTENCY-01` сняла документационные рассинхроны из `REVIEW-INITIAL-01` без изменения методологии по сути.

После METH-CONSISTENCY выполнена серия governance hardening задач:

- PR #130 (`METH-GOVERNANCE-BOUNDARIES`, journal 0014) закрепил правила, что `main` обновляется только через release-PR `developer -> main`, который мержит человек-архитектор, а агенты работают только в своем `work/<role>/<task>` namespace.
- PR #132 (`METH-BRANCH-GUARD`, journal 0015) закрепил pre-commit branch guard: перед commit HEAD должен быть work-веткой задачи, прямой локальный commit в `developer`/`main` запрещен.
- PR #133 закрыл journal state для 0014/0015 после work PR, а PR #134 перенес `developer` в `main`; PR #135 синхронизировал `main` обратно в `developer` без changed files.
- PR #136 (`METH-REVIEW-2026-06-16-01`, journal 0016) выполнил review-only комплексную проверку methodology repository с `Journal trace: always` и `Report delivery: chat`; полный body review report возвращен в чат и не сохранен в repository.

`METH-FIX-REVIEW-BLOCKERS-2026-06-16-01` merged в `developer` через PR #137 и закрыл blockers из PR #136:

- stale release/sync closure для 0014/0015 после PR #134/#135;
- post-merge closure для 0016 после PR #136;
- рассинхрон Core-документов по `Journal trace: always` и `Report delivery`;
- отсутствие явного `Repository sync / checkout guard`;
- ambiguity вокруг переноса engine-journal scaffold/templates и operational history.

Journal 0017 закрыт terminal closure-only шагом: RESULT/INDEX зафиксировали PR #137 status `merged`, merge commit `697be521f6d258b866bd59142207cf279c8869db` и `merged_at` `2026-06-16T05:34:39Z`.

Release/sync после journal 0020 и audit 0021 выполнены:

- PR #150 перенёс `developer -> main`;
- PR #151 синхронизировал `main -> developer`;
- PR #152 зафиксировал review-only audit `0021` с verdict `blocked`;
- PR #153 закрыл journal `0021`.

PR #154 закрыл B-01/M-01/M-02/M-03 из journal 0021. PR #155 закрыл journal 0022.

Контрольный audit после #155 выполнен в ChatGPT: blocking/major не найдено; journal 0020-0022, state docs и templates sequence/checkout guard проверены.

Предыдущий release/sync шаг после PR #154/#155 выполнен более поздним release cycle; актуальный следующий шаг зафиксирован в начале файла.

Дополнение (`ASD-OPLAYER-001`, journal 0024): зафиксирована нейтральная трёхслойная operating-модель. Добавлены `docs/agent-system/ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` (project operating layer: один изолированный проектный контекст на target repository, ролевой контракт «не коммитит/не мержит», knowledge base, правило свежести asof + developer HEAD SHA) и `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md` (Cowork lane: read-only advisory консолидация, visibility-matrix как need-to-know граница, STATE_DIGEST/CONSOLIDATED_VIEW, redaction-граница, приватный control plane). `TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md` расширен разделом «Три слоя управления». Решение — в `DECISION_LOG.md` (2026-06-19). Docs-only; реальные имена/матрицы/дайджесты в публичный репозиторий не добавлялись.

Дополнение (2026-06-23, pre-release state refresh): pre-adoption аудит и cleanup-серия завершены; journal закрыт по актуальному `engine-journal/INDEX.md` через terminal batch-closure для завершённой серии, а текущая state-refresh запись закрывается в release-prep перед release PR; generated checks подтверждены как EOL-safe/content-oriented; следующий переход — release `developer -> main` с human-only annotated tag на release merge commit, затем sync и downstream adoption на release pointer. Существующие исторические literal names в этой append-only летописи не переписывались; живые секции выше остаются нейтральными.
