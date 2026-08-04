# BACKLOG

Этот файл хранит будущие задачи и отложенные идеи. Выполненные пункты остаются в
`engine-journal/INDEX.md`, `RESULT-*`, `CURRENT_STATE.md` historical section и
GitHub PR metadata, а не в live backlog.

## Agent proposal intake

Инициативные предложения агентов фиксируются в RESULT/final report в разделе
`## Unprompted Project Proposals` по `AGENT_INITIATIVE_PROTOCOL.md`.

Proposal не становится backlog item автоматически. Перед добавлением сюда
architect/orchestrator triage должен выбрать disposition, проверить privacy,
сформулировать role-scoped task id и отделить proposal от текущего execution
scope.

Допустимые disposition:

- `reject` — не добавлять в backlog;
- `backlog_candidate` — добавить как candidate с owner role и expected branch;
- `MIR_candidate` — вести через `METHODOLOGY_IMPROVEMENT_LEDGER.md`;
- `immediate_separate_task` — создать отдельный TASK/branch/PR после явного
  решения архитектора.

## Methodology hardening v1.5.2

Статус: завершено / historical trace. H1–H16 реализованы отдельными scoped PR:
journal 0138–0152 фиксирует PR #306–#309 и #311–#321, а journal 0153 / PR #322
фиксирует boundary closure серии. Перечень ниже сохранён как историческое
evidence и не является future queue.

- PR-2/H2: journal history scope clarity.
- PR-3/H3: time and cost accounting hard-gate, включая token/cost fields,
  `TIME_ACCOUNTING_POLICY.md`, `COST_TRACKING_POLICY.md`, ledger/metrics и
  ready-gate enforcement.
- PR-4/H4: stable-reference schema sync (`source_ref`, `reference_type`,
  separate methodology development base).
- PR-5/H5: mandatory overlays by trigger, manifest-driven discovery,
  `METHODOLOGY_MAP.mermaid` и `tools/orchestrator_checklist.py`.
- PR-6/H9: release authority and human-gate policy.
- PR-7/H13: business acceptance / UAT gate.
- PR-8/H14: hotfix, rollback and disaster recovery.
- PR-9/H6: safe-scan and Russian-first lint.
- PR-10/H7: management layer, non-technical architect guide, handoff/cockpit.
- PR-11/H8+H10: private control-plane templates and MIR lifecycle ledger.
- PR-12/H11: policy invariants and self-test gate.
- PR-13/H12: agent initiative protocol and mandatory methodology feedback.
- PR-14/H15: journal archiving and memory hygiene.
- PR-15/H16: lifecycle and cross-project dependency policies.

## Verification-derived methodology hardening

Статус: accepted backlog / short-horizon implementation queue. Источник — практические
инциденты проекта `verification` за цикл около двадцати задач
`постановка -> Engine -> независимая проверка -> human merge`. Architect triage:
добавить в methodology backlog; не переносить downstream-specific данные и не
дублировать уже реализованные механизмы.

Существующая база, которую нужно расширять, а не создавать заново:
`TASK_CONTRACT.md`, `check_task_ready.py`,
`AUTONOMOUS_TERMINAL_EXECUTION_PROTOCOL.md`, fail-closed reservation validation,
zero-match fix 0076, review feedback schema и bounded fix-pass. Перечисленные ниже
задачи не разрешают ослаблять эти механизмы.

Порядок: P0 начать первой implementation-серией после завершения текущей release
boundary v1.6.0; P1 выполнить в следующей короткой серии. Не оставлять пункты в
неопределённом future без владельца и критерия приёмки. Backlog-only фиксация не
создаёт новые validators, gates или journal sequence.

### P0 — доказательство, что контроль действительно работает

#### METH-CONTROL-EFFECTIVENESS-EVIDENCE-GATE-01

Статус: partial coverage / implementation required.

- Для нового или изменённого контроля требовать negative-path evidence: нарушение
  смоделировано, условие доказанно наступило, контроль отклонил действие ожидаемым
  способом.
- Положительный признак рядом с контролем, наличие компонента в конфигурации и
  успешный запуск команды не считать доказательством срабатывания.
- Пустые данные не считать доказательным сценарием, если требование относится к
  существующим записям.
- При невозможности оценить контроль итог должен быть blocked/fail-closed, а не
  success.
- Критерий приёмки: reusable schema evidence содержит condition proof, trigger
  proof, expected rejection и фактический verdict; есть regression fixtures,
  которые ломают каждую из четырёх частей по отдельности.

#### METH-NONEMPTY-VALIDATION-DISCOVERY-GUARD-01

Статус: отдельные zero-match исправления существуют / общий guard отсутствует.

- Ввести единый precondition guard для инструментов, находящих scope через Git:
  отличать «объектов действительно нет» от «Git/история/scope недоступны».
- Успех требует ненулевого и ожидаемого числа inspected files/tests/checks либо
  явного обоснованного empty-scope contract.
- Ноль собранных тестов и обязательный suite, полностью ушедший в skip, считать
  blocker.
- Ручные path/config inventories сверять с фактическим деревом и тестовым
  discovery.
- Критерий приёмки: общий reusable helper подключён к применимым validators;
  regression tests покрывают unavailable Git, shallow/усечённую историю,
  zero-match, zero-collected, all-skipped и новый файл вне ручного перечня.

### P0 — совпадение условий проверки и исполнения

#### METH-VALIDATION-ENVIRONMENT-PARITY-AND-SAFE-PROBE-01

Статус: implementation required; не дублирует Docker environment blocker backlog.

- Evidence-прогон обязан использовать проектную конфигурацию и существенные
  условия фактического execution path: зависимости, БД/её отсутствие,
  контейнерные mounts, права и рабочий каталог.
- До принятия исхода отдельно доказывать, что моделируемое условие реально
  наступило внутри той же среды.
- Диагностические пробы выполнять read-only либо в отдельном временном каталоге;
  неуспешная проба не должна менять tracked worktree.
- Не фильтровать или усекать источник вывода, по которому определяется отказ;
  краткое резюме строить только после сохранения полного результата.
- Критерий приёмки: environment manifest в evidence, parity assertions,
  worktree-before/after proof и regression fixtures для недоступного mount,
  неверной конфигурации, write-on-failure и скрытой ошибки в полном выводе.

### P1 — точность проверок и размещение гарантий

#### METH-VALIDATOR-PRECISION-AND-COVERAGE-REGRESSION-01

Статус: implementation required.

- При изменении validator сравнивать обе стороны delta: что перестало
  обнаруживаться и что стало обнаруживаться.
- Решения принимать по содержимому/семантике, а не только по имени файла,
  переменной или цитированию запрещённого текста.
- Негативные и позитивные fixtures должны включать документацию о самом правиле,
  доменно осмысленные имена и граничные символы.
- Проверки состояния формулировать для созданных тестом записей и их свойств, а не
  как глобальное количество объектов в общем хранилище.
- Критерий приёмки: before/after finding inventory, false-positive и
  false-negative budgets, targeted fixtures и доказательство отсутствия
  необъяснённого сокращения coverage.

#### METH-GUARANTEE-PLACEMENT-AND-EVIDENCE-HONESTY-01

Статус: policy consolidation required.

- Гарантию, выражаемую ограничением хранилища, по умолчанию закреплять на уровне
  хранилища и проверять обходом application path.
- Связанные неделимые условия выражать атомарным/составным ограничением, когда
  технология это допускает.
- Типы и application checks описывать как защиту от случайного обхода, если
  намеренный обход предотвращается только нижележащим слоем.
- Не изготавливать retroactive evidence, не заполнять control-looking поля
  константой и не усиливать claim выше реально доказанного scope.
- Допускать честный исход «изменение не требуется» с evidence.
- Критерий приёмки: reusable decision table «где живёт гарантия», bypass-test
  requirement и evidence-strength vocabulary включены в task/review contracts.

### P1 — автономность без самоподдерживающейся бюрократии

#### METH-EXECUTION-BUDGET-AND-TRACEABILITY-COST-01

Статус: partial coverage in autonomous protocol / refinement required.

- Постановка задаёт правила выбора на развилках и допускает доказанный
  `no_change_required`; «уточнить у владельца» оставлять только для
  непреодолимых authority/ambiguity blockers.
- Закрепить machine-readable budgets: максимальное число полных тяжёлых прогонов,
  допустимый fix-pass и запрет бесконечного перезапуска после таймаута.
- Порядок работ определять зависимостями данных; reviewer отвечает в thread/comment,
  не переписывая чужую запись параллельно.
- Ввести lightweight traceability matrix: обычная продуктовая задача не создаёт
  отдельный closure/state-refresh PR; полный TASK/RATIONALE/RESULT оставлять для
  архитектуры, безопасности, миграций, release boundaries и сложных инцидентов.
- Измерять долю времени/PR, ушедшую на продукт и на обслуживание контроля.
  Сработавшее ограничение «один task triplet на задачу, не запись на каждую
  находку» сделать явным default.
- Между implementation и независимым review сохранять отдельную review boundary,
  но не создавать искусственную паузу без проверяемого результата.
- Критерий приёмки: task contract budget fields, deterministic choice rules,
  lightweight/escalated journal decision table и метрика reduction of
  journal-only PR cycles без потери auditability.

## Future methodology simplification

- Context handoff footer enforcement.
- Journal gate automation.
- Adoption feedback loop automation.
- Optional vendor/public metadata hygiene and historical English wording cleanup
  там, где это не нарушает append-only history и Russian-first policy.
- Optional inclusion of operating-layer contracts in target governance packs:
  `ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` and
  `CROSS_PROJECT_CONSOLIDATION_CONTRACT.md`; реальные visibility matrix и digest
  держать только в private control plane.

## Post-autoloop automation roadmap

Статус: backlog / future tooling roadmap. Этот раздел только структурирует отложенные идеи после перехода к fast agent-owned workflow и review autoloop. Не реализовывать scripts, validators, новые gates или runtime logic в рамках backlog-only задач.

Контекст: после перехода к цепочке `Engine PR -> Reviewer review -> Engine fix-pass -> Reviewer re-review / machine-check closure -> architect-ready -> human merge` повторяющийся шум пришёл из prose-only task contracts, ручного preflight, позднего `git diff --check`, generated/cloud EOL-only diff, неструктурированного reviewer feedback, GitHub own-PR review limitation, полного re-review для machine-only blockers, journal/closure state drift и ручного выбора adoption mode.

### P0 - снизить самый частый операционный шум

#### METH-TASK-CONTRACT-FRONTMATTER-01

- Ввести единый machine-readable task frontmatter или `task.yaml`.
- Минимальные поля: `mode`, `role`, `branch`, `allowed_files`, `forbidden_files`, `checks`, `stop_conditions`, `journal_policy`, `cloud_policy`, `review_policy`.
- Будущий validator: `validate_task_contract.py`.

#### METH-CHECK-TASK-READY-01

Статус: implemented by methodology task `METH-CHECK-TASK-READY-01`; запись оставлена как trace исходной roadmap-идеи.

- Ввести единый ready-for-review / ready-for-push gate.
- Будущий script: `check_task_ready.py`.
- Агрегировать branch guard, allowed-files diff, `git diff --check`, generated checks, sensitive scans и placeholder scan.
- Cross-reference: generated checks и placeholder scan не дублировать в отдельных prose-инструкциях, а подключать как подшаги этого gate.

#### METH-GENERATED-EOL-GUARD-01

Статус: implemented by methodology task `METH-GENERATED-EOL-GUARD-01`; запись оставлена как trace исходной roadmap-идеи.

- Развить существующий backlog item `METH-GENERATED-EOL-CANON-01` в practical tooling roadmap.
- Будущий guard различает content diff и EOL-only diff в generated/cloud/journal artifacts.
- Не выполнять большой renormalize без отдельного отчёта и явного решения архитектора.

#### METH-REVIEW-FEEDBACK-SCHEMA-01

Статус: implemented by methodology task `METH-REVIEW-FEEDBACK-SCHEMA-01`; запись оставлена как trace исходной roadmap-идеи.

- Стандартизировать blocker IDs: `B-01`, `B-02`, ...
- Задать reviewer output schema и engine fix-pass protocol.
- Разделить machine-verifiable blockers и semantic blockers.
- Включить minimal re-review mode для changed machine-only blockers.
- Зафиксировать GitHub own-PR verdict comment limitation: если token не может формально approve/request changes собственный PR, reviewer фиксирует verdict обычным PR comment.

### P1 - меньше дёргать архитектора

#### METH-STOP-OR-ACT-TABLE-01

- Добавить таблицу "можно действовать без вопроса / STOP and ask".
- Примеры "можно действовать": EOL-only restore в non-scope generated file, stale generated regeneration после source/INDEX changes, own-PR verdict comment вместо формального review.
- Примеры STOP: dirty tree до sync/switch, unknown file outside allowlist, unmerged branch deletion, force-push/rewrite request без явного решения.

#### METH-REVIEW-FEEDBACK-JSON-01

- Добавить опциональный `review_feedback.json` или markdown-block.
- Поля: `blocker_id`, `file`, `line`, `expected_fix`, `verification_command`, `can_engine_fix_without_architect`.
- Использовать как machine-readable handoff от reviewer к engine fix-pass.

#### METH-DECISION-CACHE-01

- Ввести decision cache для повторяющихся lifecycle-ситуаций.
- Первые cached decisions: accepted terminal fold, EOL-only restore, generated cloud after INDEX, journal closure status, own-PR verdict comment.
- Цель: не спрашивать архитектора повторно по уже принятой operational policy.

### P1 - упростить journal/closure

#### METH-JOURNAL-STATE-MACHINE-01

- Ввести compact machine-readable journal lifecycle states: `substantive_open`, `ready_for_review`, `merged_pending_batch`, `closed`, `lifecycle_terminal_accepted`.
- Будущий tool: `journal_lint.py`.
- Output должен различать blocker, non-blocker и accepted terminal fold.

#### METH-BATCH-CLOSURE-PLANNER-01

- Будущий script строит список merged-but-unclosed substantive entries.
- Исключает lifecycle terminal folds.
- Сверяет GitHub facts.
- Предлагает patch plan для RESULT closure-stamps, INDEX status+PR URL и cloud regen.

#### METH-PLACEHOLDER-SCANNER-01

- Сделать RESULT/INDEX placeholder scanner без self-hit ловушек.
- Различать validation literals и реальные unresolved placeholders.
- Подключить scanner как подшаг `METH-CHECK-TASK-READY-01`, не плодя отдельный ручной checklist в каждой задаче.

### P2 - adoption/downstream tooling

#### METH-TARGET-ADOPTION-DETECTOR-01

Статус: implemented as reusable methodology policy/spec by `METH-TARGET-ADOPTION-DETECTOR-01`; возможный future script допустим только отдельной tooling task.

- Detector policy определяет adoption mode Variant A/B/C или STOP.
- Проверяет наличие `docs/agent-system`, engine journal, branch model, dirty tree и stable methodology reference.
- Выдаёт Variant A/B/C recommendation с причинами, preconditions, allowed next task и forbidden actions.
- Dirty target tree, unstable methodology source, private data risk и риск overwrite target-specific history дают STOP.

#### METH-PUBLIC-REPO-PRIVATE-DATA-GUARD-01

- Добавить scanner для public methodology repository.
- Ловить forbidden private project names, runtime data, `.env`, secrets и downstream identifiers.
- Output count-only / filename-only, без вывода secret values.

#### METH-RELEASE-ASSISTANT-01

Статус: implemented by methodology task `METH-RELEASE-ASSISTANT-01`; запись
оставлена как trace исходной roadmap-идеи.

- Будущий `release_gate.py --version vX.Y.Z`.
- Проверяет journal, generated artifacts, release payload, accepted terminal folds, state docs, release PR и tag status.
- Выдаёт human action text для архитектора: что merge/tag/create вручную и что engine делать не должен.

### P2 - Windows/PowerShell environment

#### METH-POWERSHELL-SAFE-SNIPPETS-01

- Зафиксировать PowerShell-safe command snippets.
- Покрыть quoting, noisy shell chains, wrapper noise vs real errors и known syntax traps вроде upstream `@{u}`.

#### METH-GIT-ENV-DOCTOR-01

- Будущий `doctor_git_env.py`.
- Проверяет `safe.directory`, branch, remote, index/lock write, line endings и `gh auth`.
- Цель: отделять environment blockers от repository-content defects.

#### METH-DOCKER-VALIDATION-FALLBACK-01

- Ввести fixed status `validation_blocked_environment`.
- Описать, что делать, если Docker pipe недоступен.
- Не ослаблять validation молча: либо rerun в окружении с Docker, либо явно report blocked validation.

### P3 - коммуникация PR/reviewer

#### METH-PR-COMMENT-TEMPLATES-01

- Добавить templates для PR comments:
  - fix-pass started;
  - fix-pass completed;
  - own-PR verdict comment.
- Цель: reviewer получает одинаковый формат, а engine не импровизирует статус.

#### METH-REVIEWER-MINIMAL-REREVIEW-01

- Ввести `re-review_scope: changed_blockers_only`.
- Не повторять full architecture review, если fix-pass менял только machine-verifiable blocker, например whitespace или generated check drift.

#### METH-BLOCKER-ID-CANON-01

- Сделать blocker IDs обязательными в reviewer feedback.
- Engine закрывает конкретные IDs в RESULT/fix-pass report.
- Может быть включено в `METH-REVIEW-FEEDBACK-SCHEMA-01`, если тот PR покрывает весь feedback protocol.

### Рекомендуемый первый implementation batch

1. `METH-REVIEW-FEEDBACK-SCHEMA-01`
2. `METH-CHECK-TASK-READY-01`
3. `METH-GENERATED-EOL-GUARD-01`
4. `METH-TASK-CONTRACT-FRONTMATTER-01` — реализовано в текущей методологической серии: добавлен `TASK_CONTRACT.md`, lightweight validator `validate_task_contract.py` и template/orchestrator integration для новых write-action Engine-задач.
5. `METH-TASK-CONTRACT-CLOUD-BUNDLE-01` — реализовано как follow-up: `TASK_CONTRACT.md` включён в default cloud/orchestrator bundle отдельным numbered-файлом `13_TASK_CONTRACT.md` без изменения схемы контракта и validator logic.

Почему такой порядок:
- сначала убрать лишние reviewer cycles;
- затем ловить technical blockers до PR;
- затем убрать EOL/generated noise;
- затем формализовать task contract для будущих validators.

## METH-GENERATED-EOL-CANON-01 — generated/journal/cloud EOL-noise cleanup

Статус: backlog / future tooling task; не блокирует переход в target implementation repository.

Проблема:
После `gen_cloud_bundle.py` на Windows периодически появляются EOL-only изменения в generated/cloud/journal Markdown files. Содержательный diff обычно ограничен `cloud/00_README.md` и `cloud/07_ENGINE_JOURNAL_INDEX.md`, но Git может помечать дополнительные файлы как modified из-за line endings. Это создаёт operational noise и заставляет Engine вручную отделять content changes от EOL-only изменений.

Предварительное решение:
- расширить `.gitattributes` для Markdown/YAML/Python и generated/journal/template paths;
- проверить, что `gen_cloud_bundle.py` и `gen_file_map.py` явно пишут LF (`\n`) независимо от Windows default newline;
- выполнить bounded `git add --renormalize --dry-run docs/agent-system`;
- выполнять реальный renormalize только отдельным scoped PR после анализа размера diff;
- добавить lightweight EOL check для generated artifacts, если потребуется.

Ограничения:
- не выполнять перед release;
- не смешивать с target project work;
- не делать большой renormalize без отдельного отчёта и явного решения архитектора.
