# BACKLOG

- Выполнено: bootstrap agent-system repository.
- Configure GitHub rulesets.
- Create local worktrees.
- Add CI forbidden files check.
- Add pre-push hook.
- Prepare private downstream repository transfer/adaptation prompt.
- Подготовить checklists для агентов.
- Выполнено в `METH-NO-ORDINARY-POST-MERGE-CLOSURE-01`: lifecycle simplification для ordinary PR и GitHub PR metadata как source of truth для merge facts.
- Future methodology simplification после release `v1.2.0`: context handoff footer enforcement, journal gate automation, adoption feedback loop automation. Не реализовывать в release-prep; рассматривать отдельными scoped задачами.
- После merge `METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01`: human-only release PR `developer -> main`, чтобы stable `origin/main` включал новую downstream policy. Это не выполняется engine в этой задаче.
- Выполняется в `METH-FIX-AUTHORIZATION-HEADER-GUARD-01`: P1 safety hotfix для ready-gate, чтобы headers `Authorization` блокировались независимо от auth-схемы и matching values не выводились.

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

- Будущий script определяет adoption mode.
- Проверяет наличие `docs/agent-system`, engine journal, branch model, dirty tree и methodology reference.
- Выдаёт Variant A/B/C recommendation с причинами.

#### METH-PUBLIC-REPO-PRIVATE-DATA-GUARD-01

- Добавить scanner для public methodology repository.
- Ловить forbidden private project names, runtime data, `.env`, secrets и downstream identifiers.
- Output count-only / filename-only, без вывода secret values.

#### METH-RELEASE-ASSISTANT-01

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
