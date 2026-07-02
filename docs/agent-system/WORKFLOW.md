# WORKFLOW

1. Пользователь принимает решение.
2. Оркестратор помогает сформулировать задачу.
3. Задача оформляется по шаблону.
4. Исполнитель работает в своей ветке.
5. Исполнитель обновляет отчет.
6. Проверяющий агент делает review.
7. Пользователь принимает решение о merge; human-only actions проходят через
   `HUMAN_GATE_POLICY.md`.
8. После merge обновляются `CURRENT_STATE` и `DECISION_LOG`, если нужно.

## Agent-owned task branch workflow

Для substantive file-changing task действует быстрый agent-owned workflow:

1. Orchestrator и пользователь фиксируют цель, scope, allowed/forbidden files, checks и STOP-условия.
2. Engine создает основную ветку `work/<role>/<task-id>` от актуальной `developer`.
3. Engine выполняет работу end-to-end, при необходимости создавая внутренние `work/<role>/<task-id>/*` sub-branches и сливая их обратно в основную task branch.
4. Engine не ждет подтверждения после каждого микрошагa, пока не выходит за scope и не сработали STOP-условия.
5. Один substantive task завершается одним итоговым PR в `developer`.
6. Reviewer проверяет итоговый PR; comments/blockers исправляются engine в той же task branch.
7. После исправлений и повторных checks PR доводится до `ready_for_merge`.
8. Обычный post-merge closure PR не создается автоматически; journal closure выполняется batch-проходом перед release/audit/methodology boundary или по явному исключению.

## Review autoloop

Для active work PR применяется bounded state-machine из `docs/agent-system/REVIEW_AUTOLOOP.md`:

1. Engine открывает или обновляет PR и помечает состояние `engine:ready-for-review`.
2. Reviewer проверяет PR и оставляет feedback только в этом PR.
3. Если есть blockers, PR получает `reviewer:changes-requested`, а engine делает fix-pass в той же task branch.
4. Цикл повторяется до reviewer approve или до `max_review_cycles`.
5. После approve-equivalent PR получает `architect:ready-to-merge`.
6. Merge в `developer` выполняет только человек-архитектор.
7. При STOP-condition PR получает `automation:stopped-human-required` и передается человеку.

## Шаблоны отчётов и решений

- Универсальный отчёт роли (не-PR работ, исследований, status-апдейтов): `docs/agent-system/templates/AGENT_REPORT_TEMPLATE.md` (Summary, Changed files, Checks, Risks, Open questions, Next step).
- Запись решения для `docs/agent-system/DECISION_LOG.md`: `docs/agent-system/templates/DECISION_TEMPLATE.md` (Date, Decision, Context, Options considered, Reason, Consequences, Follow-up actions).
- Review report: `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md` (полный 10-секционный шаблон + раздел «Облегчённый PR/comment review»).

## Режимы применения

### Лёгкий режим одного оператора

Этот режим используется, когда один оператор ведет задачу end-to-end. Он не требует искусственно запускать несколько агентов для маленькой docs-only или status-задачи.

Минимальные правила остаются обязательными:

- direct changes в `main`/`developer` запрещены без отдельного решения пользователя;
- file-changing substantive task идет через основную `work/<role>/<task>` и один итоговый PR;
- внутренние `work/<role>/<task>/*` допустимы только как sub-branches внутри agent-owned task branch;
- TASK/RESULT/INDEX создаются и финализируются, если задача меняет repository files или создает PR;
- Operational Fast Lane допускается только для read-only/status/cleanup без file edits;
- final report содержит проверки, риски и локальный sync block после PR/merge.

### Управляемый многоагентный режим

Этот режим используется для задач с высоким риском, несколькими исполнителями, review gate, runtime scope или target adoption.

Дополнительно требуется:

- явное разделение orchestrator, engine и reviewer responsibilities;
- review-only boundary для reviewer roles;
- отдельные implementation tasks для findings из standalone review-only задач; review feedback по активному work PR исправляется в той же task branch;
- полный self-contained блок для исполнителя (engine) или Task File Handoff Mode;
- воспроизводимые journal artifacts и PR metadata.

## Проверка против избыточного усложнения

Перед добавлением нового документа, роли, workflow, template или gate нужно ответить:

- решает ли изменение повторяющуюся проблему, уже встреченную в работе;
- можно ли обойтись правкой существующего документа или checklist;
- не превращает ли изменение простой solo-operator workflow в обязательную multi-agent церемонию;
- есть ли явный trigger, когда правило обязательно, и когда оно не применяется;
- не добавляет ли изменение runtime/CI/Docker scope в docs-only задачу.

Если ответ неясен, изменение фиксируется как proposed follow-up, а не как обязательное правило.

## После bootstrap

- Прямые изменения в `developer` запрещены без отдельного разрешения пользователя.
- Рабочий поток идет через основные task branches `work/<role>/<task>`.
- Внутренние sub-branches `work/<role>/<task>/*` допустимы только внутри той же задачи и сливаются обратно до итогового PR.
- Рабочая ветка создается от актуальной `developer`.
- `developer` принимает изменения через PR из рабочих веток.
- `developer` -> `main` выполняется только через human-merged release PR после release-gate из `BRANCH_POLICY.md`; Business Acceptance Gate проходит между стабилизацией `developer` и release PR в `main`; annotated tag, publication и sync decision выполняет человек по `RELEASE_AUTHORITY_POLICY.md`, не агент.

## Business Acceptance Gate

Business Acceptance Gate применяется после стабилизации `developer` и до
approval/merge release PR `developer -> main`.

Gate основан на:

- `docs/agent-system/UAT_WORKFLOW.md`;
- `docs/agent-system/BUSINESS_ACCEPTANCE_CHECKLIST.md`;
- `docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`;
- `docs/agent-system/HUMAN_GATE_POLICY.md`;
- `docs/agent-system/RELEASE_AUTHORITY_POLICY.md`.

Порядок:

1. Engine/release-prep генерирует Human UAT Checklist из acceptance scenarios.
2. Owner/PO вручную проходит button-click, visual UI, API/CLI или
   documentation-as-product checks.
3. RESULT фиксирует `business_acceptance_gate`, actor, checklist reference,
   evidence и decision.
4. Если verdict `rejected` или checklist отсутствует без `not_applicable`
   reason, release PR в `main` блокируется.

Agent не может заменить owner/PO verdict. Для docs-only или methodology-only
release допустим `not_applicable`, но только с причиной и safe evidence.

## Release authority и human gate

Release-sensitive действия выполняются по `docs/agent-system/RELEASE_AUTHORITY_POLICY.md`
и `docs/agent-system/HUMAN_GATE_POLICY.md`.

Агент может:

- подготовить release/sync PR;
- собрать checks и evidence summary;
- обновить docs/journal в разрешенном scope;
- после human action выполнить read-only verification, если это входит в задачу.

Агент не выполняет сам:

- merge в `main`;
- создание annotated release tag;
- GitHub Release / public publication;
- финальный sync `main -> developer`;
- branch protection/rulesets, CI/CD, prod-secrets, mission/strategy, удаление
  данных, финансы и rollback decision.

Если `RESULT` утверждает, что release-sensitive действие выполнено, он фиксирует
actor, action и evidence по `RELEASE_AUTHORITY_POLICY.md`.

## Рабочий процесс review-only

Code review / external review / consulting review по умолчанию выполняется как review-only task:

```text
developer -> work/<reviewer-role>/<task-id> -> PR в developer
```

Review-задача по умолчанию возвращает тело review report в чат (`Report delivery: chat`) и не сохраняет этот полный report-body отдельным файлом в repository.

При этом review-задача всегда журналирует TASK/RESULT/INDEX: `Journal trace: always`. Journal artifacts идут в docs-only PR в `developer` или другой явно выбранный base branch, независимо от того, сохраняется ли тело review report в repository.

Сохранение тела отчета в repository требует `Report delivery: repository` или `Report delivery: chat+repository`. Такое разрешение относится только к report-body файлу; обязательный journal trace действует отдельно.

Review-only PR содержит journal artifacts всегда; review report files и state docs добавляются только если они явно разрешены задачей.

Reviewer не исправляет production code, runtime, Docker, CI, scripts или dependencies. В активном work PR reviewer оставляет feedback, а исправления делает engine в той же task branch. Findings из standalone review-only задач превращаются в отдельные implementation PR только после решения пользователя.

Reviewer не запускает исполнителя (engine), не меняет очередь исполнителя и не формулирует себе implementation task. Он может предложить кандидаты на будущие задачи, но решение принимает пользователь вместе с оркестратором.

Review task должен явно указывать:

- режим: `review-only`, `docs-only` или `fix-allowed`;
- объект проверки: PR, branch, commit, diff или files;
- base branch;
- working branch, если нужна;
- allowed files;
- forbidden files;
- разрешенные и запрещенные команды;
- `Report delivery`: `chat`, `repository` или `chat+repository`;
- `Journal trace`: `always`;
- можно ли сохранять тело отчета в repository;
- какие journal artifacts и state docs входят в allowed files.

Для standard developer workflow review стартует от `developer`, конкретного PR/diff/branch/commit/files. `main` используется только если пользователь явно указал, что нужно проверить стабильную версию.

Подробный контракт:

```text
docs/agent-system/CODE_REVIEW_WORKFLOW.md
```

## Локальные действия после PR/merge

Если задача создала PR, была смержена, обновила remote `developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`, финальный отчет в чат должен содержать конкретный блок:

```text
## Локальные действия после PR/merge
```

Для PR в `developer` минимальный блок:

````text
## Локальные действия после PR/merge

Когда PR будет смержен в developer, выполнить локально:

```powershell
cd <repo-path>

git status --short
git fetch --all --prune

git switch developer
git pull --ff-only origin developer

git rev-parse developer
git rev-parse origin/developer
git status --short
```

Ожидаемый результат:

```text
developer == origin/developer
working tree clean
```
````

Если затронут `main`, добавить:

```powershell
git switch main
git pull --ff-only origin main

git switch developer
git pull --ff-only origin developer
```

Если локальная ветка устарела или расходится, вместо общих советов вывести диагностику:

```powershell
git status --short
git branch --show-current
git fetch --all --prune
git rev-parse developer
git rev-parse origin/developer
git log --oneline --decorate --left-right developer...origin/developer
git worktree list
```

Запрещено рекомендовать `git reset --hard`, если пользователь явно не подтвердил, что локальные изменения и локальные commits не нужны.
