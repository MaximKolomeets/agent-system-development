# TASK_HEADER_COMMON

Канонический общий header для engine task-шаблонов (`DEVELOPMENT_TASK_TEMPLATE.md`, `AGENT_RESEARCH_TASK_TEMPLATE.md` и других task-шаблонов). Эти блоки одинаковы для всех типов engine-задач; конкретный task-шаблон ссылается на этот канон и добавляет только свои уникальные секции.

## Mandatory header

```text
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: <свободное значение или пусто>
```

Задача формулируется на русском языке. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

Header role-agnostic: указывается **роль** (функция в методологии), а не имя конкретного инструмента/модели. Каноническая форма заголовка — `Задача для <роль>: <task-id>`; manifest-правило `mandatory_engine_task_header` должно трактовать `<роль>` как vendor-neutral функцию в методологии. Конкретного **исполнителя** (tool/model/human) назначает архитектор; в task header он не фиксируется (`Исполнитель: на усмотрение архитектора`). Различение роли и исполнителя — канон `docs/agent-system/ROLE_MODEL.md` → «Роль vs исполнитель».

## Machine-readable task contract

Для новых задач, которые меняют repository files, создают commit/push/PR, выполняют tooling/docs-only/review/fix-pass/release/adoption flow, task block или TASK file должен содержать fenced YAML block `task_contract` по канону `docs/agent-system/TASK_CONTRACT.md`.

`task_contract` не заменяет prose: prose объясняет цель и контекст, а machine-readable block является источником истины для mode, execution_mode, repository, working_branch, allowed_files, forbidden_files, policies, checks и STOP conditions. Если `task_contract` и prose противоречат друг другу, `engine` пишет `STOP` и запрашивает решение архитектора.

Минимальный skeleton:

```yaml
task_contract:
  version: 1
  task_id: <task-id>
  role: <роль>
  mode: agent
  execution_mode: local_only
  repository:
    full_name: <owner/repository>
    local_path: <local-path>
    base_branch: developer
    working_branch: work/<role>/<task-id>
  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    ref: origin/main
    stable_only: true
    source_commit: <origin/main commit sha>
    checked_at: <ISO-8601 timestamp>
  scope:
    allowed_files:
      - <allowed path>
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    language: russian_first
  checks:
    required:
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
```

Перед push/PR для TASK file с contract рекомендуется выполнить:

```text
python docs/agent-system/tools/validate_task_contract.py <task-file>
```

## Russian-first

Все ответы, final report, TASK/RESULT/INDEX, target-local docs/templates и комментарии в файлах писать на русском языке. Английский допустим только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и code identifiers.

## Commit/push/PR metadata language

Commit subject/body, PR title и PR body должны быть Russian-first. Technical identifiers разрешены: branch names, task ids, filenames, paths, commands, config keys, API names, role ids, package names и SHA values не переводятся. Conventional prefix вроде `docs(agent-system):` разрешён как technical identifier, но смысловая часть после `:` должна быть Russian-first. Уже pushed/merged commits не переписываются и не force-push без отдельного явного решения архитектора; если нарушение metadata-language обнаружено после push и безопасно не исправлено, RESULT фиксирует нарушение и правило применяется со следующего commit.

## Stable methodology reference

Для target/downstream/adoption задач `methodology_reference` указывает на stable methodology source: `origin/main` / `main`, release tag или явно заданный published Source/cloud snapshot. `developer`, `work/*`, dirty local methodology tree и open methodology PR branch не используются как source of truth для downstream. Dirty `agent-system-development/developer` или `work/*` не блокирует target task, если stable reference доступен и читается. Канон: `docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md`.

## Рекомендуемый режим исполнения

Заполнить блок `Рекомендуемый режим исполнения` в mandatory header: роль / функция, исполнитель (на усмотрение архитектора), reasoning effort (низкий | средний | высокий), launch mode / запуск, execution mode / режим и почему / why this mode is required.

В шаблоне не указываются имена инструментов/моделей. Если нужно зафиксировать фактически использованного исполнителя постфактум — делать это в RESULT, не в task header.

## Execution timestamps

TASK и RESULT фиксируют два разных типа времени:

- measured/engine — время, которое engine может зафиксировать автоматически или надежно по факту собственного запуска;
- reported/human — время, которое сообщает человек или оркестратор; поле опционально и может оставаться пустым.

TASK должен содержать:

```text
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: <свободное значение или пусто>
```

RESULT должен содержать:

```text
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время окончания выполнения (execution_finished_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Длительность выполнения (execution_duration) [measured/engine, опционально]: <duration>
Время человека, по факту (human_time_reported) [reported/human, опционально]: <свободное значение или пусто>
```

Время reviewer не записывается отдельным полем внутри work-записи: reviewer является отдельным engine-run со своим TASK/RESULT и собственными `execution_*` полями. Время merge не дублируется в execution-полях: оно фиксируется как `merged_at` в closure-stamp `RESULT` по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure facts authority».

Каноническое имя поля окончания выполнения — `execution_finished_at`. Вариант имени, образованный как `execution_` + `completed_at`, не является допустимым alias и не используется в новых TASK/RESULT. Исторические append-only записи с таким drift-именем не ретрофитятся.

Reviewer фиксирует minor finding, если новая finalized запись вводит неканоническое поле окончания выполнения вместо `execution_finished_at`; это не blocker и не повод переписывать исторические RESULT.

## Agent-owned task branch workflow

Для substantive file-changing task действует модель:

- основная task branch: `work/<role>/<task-id>`;
- внутренние sub-branches: `work/<role>/<task-id>/*`, только если нужны исполнителю (engine) и только внутри той же задачи;
- один substantive task = один итоговый PR в `developer`;
- engine владеет task branch до `ready_for_merge`, сам выполняет микрошаги, внутренние merge sub-branches, checks и исправление review feedback, пока не сработали STOP-условия;
- reviewer проверяет итоговый PR и оставляет comments/blockers; отдельный PR для feedback reviewer не создаёт без явного решения пользователя;
- post-merge closure PR после обычного work PR не default: journal допускает `merged; closure pending` до batch-closure перед release/audit/methodology boundary или другим явным исключением.

## Review autoloop

- Если задача проходит review/fix/re-review, явно указать `max_review_cycles` (default = `3`, если не задано).
- Reviewer оставляет feedback только в PR агента.
- Engine исправляет feedback в той же task branch и возвращает PR в `engine:ready-for-review`.
- После reviewer approve-equivalent PR получает `architect:ready-to-merge`; merge в `developer` остаётся human-only.
- STOP: conflict, secrets-risk, forbidden paths, failed checks, scope drift, generated drift, force-push need или превышение `max_review_cycles`.
- Канон: `docs/agent-system/REVIEW_AUTOLOOP.md`.

## Передача (handoff)

Сквозное правило handoff для **любой** engine-задачи (development, research, review, infra, source-steward и т. д.).

Final report и RESULT обязаны заканчиваться блоком «Передача» с явной строкой:

```text
Следующий: <роль> — <что делает>
```

- `<роль>` — vendor-neutral роль следующего исполнителя (`reviewer`, `dev-implementer`, `docs-maintainer`, `infra`, `source-steward` и т. д.; канон ролей — `docs/agent-system/ROLE_MODEL.md`).
- Если следующего шага нет — писать `Следующий: нет — <причина>`.
- Решение, запускать ли следующий шаг и каким исполнителем, остаётся за пользователем/архитектором.

### Batch-friendly handoff

Для обычного work PR внутри серии:

```text
Следующий: архитектор — merge; затем engine — следующая задача или следующий шаг серии; journal closure — batch перед release/audit boundary; release держим до завершения серии и batch-closure.
```

Для финального PR серии:

```text
Следующий: архитектор — merge; затем engine — batch closure journal <seq-range>; затем release dev→main.
```

## Closure-status policy

Если batch-closure policy: после merge ordinary work PR journal может временно оставаться pre-merge/closure-pending; это не blocker для следующего work PR той же фазы; blocker только для release / audit-review consistency-gate / adoption/source-update / methodology boundary / явного closure-задания / противоречивых journal facts.

Journal closed для release/reviewer gate означает: все substantive entries закрыты closure-stamp/status+PR URL, а lifecycle-only entries со статусом `terminal-fold accepted` допустимы. STOP при `open`, `ready`, `closure pending`, `stamp at merge` или merged-but-unclosed substantive entry; не STOP при `terminal-fold accepted`. Если terminal fold не lifecycle-only или содержит незакрытый содержательный payload, STOP и запросить closure/fix.

Канон closure policy — `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure policy». Шаблоны closure-задач: `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md` и `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md`.

## Source-reminder

Сквозное правило синхронизации Source-снапшота.

Если задача меняла методологию или каноны (canon-файлы, шаблоны, governance этого methodology repository), исполнитель обязан:

1. Обновить source-снапшот, если изменённые файлы входят в него (политика — `docs/agent-system/source/README.md`); снапшоты являются derived context, source of truth — GitHub-файлы.
2. В RESULT и в блоке «Передача» явно добавить строку «Обновить Source-снапшот у зарегистрированных потребителей: …», где список берётся из реестра `docs/agent-system/SOURCE_CONSUMERS.md`. Реестр потребителей ведётся в потребляющем развёртывании; обезличенная upstream-методология своих потребителей не перечисляет, поэтому в ней список остаётся generic-placeholder.

Если методология/каноны не менялись — в RESULT явно отметить «Source-reminder: не применимо (методология не менялась)».

## Source Delta

Сквозное правило отчётности по изменённым файлам и Source-рекомендациям.

Final report и RESULT обязаны включать блок «Source Delta» перед блоком «Передача». Блок нужен даже для review/journal-only задач; если файловые изменения отсутствуют, писать `Source Delta: не применимо (файлы не менялись)`.

Формат таблицы:

| путь | действие | категория | Source-рекомендация | manifest обновлён? |
| --- | --- | --- | --- | --- |
| `<path>` | `<added | modified | renamed | deleted>` | `<source | template | target_generated | history_state | journal | scaffold | generated>` | `<add | update | remove | rename | none>` | `<yes | no | n-a>` |

Категория берётся из `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`. Если файл не классифицируется однозначно, исполнитель пишет `STOP` и запрашивает решение архитектора.

Семантика Source-рекомендации:

- новый `source` или `template` file — `add`;
- изменённый `source` или `template` file — `update`;
- удалённый `source` или `template` file — `remove`;
- переименованный `source` или `template` file — `rename`;
- `history_state`, `journal`, `scaffold` и `generated` — `none`;
- `target_generated` — `none` для source-снапшота, если task не меняет source template; если меняет соответствующий template, рекомендация ставится на template row.

Если действие `added`, `deleted` или `renamed` затрагивает inventory-файл категории `source`, `template`, `target_generated` или `generated`, `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` обязан быть обновлён в том же PR, а `docs/agent-system/PROJECT_FILE_MAP.md` обязан быть регенерирован через `python docs/agent-system/tools/gen_file_map.py` и проверен через `python docs/agent-system/tools/gen_file_map.py --check`. Если manifest не обновлён или file map не регенерирован — `STOP`. Для обычного `modified` без изменения inventory-списка manifest field = `n-a`.

Если задача меняет любой файл, перечисленный в `ADOPTION_TRANSFER_MANIFEST.yml` → `orchestrator_context_bundle.files`, или меняет сам bundle inventory, `docs/agent-system/cloud/**` обязан быть регенерирован через `python docs/agent-system/tools/gen_cloud_bundle.py` и проверен через `python docs/agent-system/tools/gen_cloud_bundle.py --check`. Pre-release task также обязан выполнять cloud `--check`.

Если generated `--check` на Windows зависает в wrapper/parallel runner без живого полезного процесса, task использует read-only sequential fallback по `ORCHESTRATOR_OPERATING_CONTRACT.md`: `cmd /c python <generator> --check`; RESULT фиксирует fallback, команду и exit code. Это правило не заменяет обычные runtime/test checks.

Если zero-match/no-output scan на Windows (`rg` или wrapper/shell scan) зависает без вывода и без живого полезного процесса, task использует deterministic fallback по `ORCHESTRATOR_OPERATING_CONTRACT.md`: `Select-String`, PowerShell script, Python script/one-liner или другой sequential scan с явным exit code. RESULT фиксирует fallback-команду, exit code и смысл результата; sensitive matches не печатать построчно, использовать filename-only/count-only.

## Orchestrator context handoff

Final report и RESULT обязаны включать строку для архитектора перед блоком
«Передача» или внутри него:

```text
Архитектору — загрузить в контекст оркестратора: <cloud filename> (src: <source path>), ...; asof: <ISO-8601 timestamp>; developer_head_sha: <sha>.
```

Список строится из «Source Delta»:

- включать только файлы, которые входят в `ADOPTION_TRANSFER_MANIFEST.yml` → `orchestrator_context_bundle.files` и реально присутствуют в `docs/agent-system/cloud/`;
- имя в строке брать из `docs/agent-system/cloud/00_README.md` (`priority | cloud filename | source path | category`), исходный путь писать в скобках `src: ...`;
- небандловые файлы, включая генераторы и tooling sources, фиксировать в «Source Delta», но не добавлять в context-load строку;
- если менялся inventory или была регенерирована карта, добавлять numbered cloud-файл для `PROJECT_FILE_MAP.md`, если он есть в bundle;
- если менялись `INDEX` или state-файлы, добавлять их numbered cloud-файлы только если они есть в bundle;
- если файловых изменений нет, писать `Архитектору — загрузить в контекст оркестратора: не применимо (файлы не менялись). asof: <ISO-8601 timestamp>; developer_head_sha: <sha>.`

Пример:

```text
Архитектору — загрузить в контекст оркестратора: 01_ORCHESTRATOR_OPERATING_CONTRACT.md (src: docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md), 11_ADOPTION_TRANSFER_MANIFEST_yml.md (src: docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml); asof: <ISO-8601 timestamp>; developer_head_sha: <sha>.
```

Состав базового context-load bundle не дублируется здесь; авторитетный канон:
`docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` → «Architect →
Orchestrator context handoff».

## Verified Baseline

- Repository:
- Local path, если применимо:
- Base branch:
- Working branch:
- Checked branch state:
- Latest relevant PR numbers/statuses, если применимо:
- Release PR status, если применимо:
- Sync PR status, если применимо:
- Open PR state, если relevant:
- Verification source:
- Verification date/time:

## Проверка полноты copy/paste

- [ ] This TASK/Engine block can be executed without reading surrounding chat text.
- [ ] Рекомендуемый режим исполнения is included (роль / исполнитель «на усмотрение архитектора» / reasoning effort / запуск / режим / почему); имён инструментов/моделей в шаблоне нет.
- [ ] Execution timestamps included: TASK содержит `execution_started_at` и optional `orchestration_time_reported`; RESULT содержит `execution_started_at`, `execution_finished_at`, optional `execution_duration` и optional `human_time_reported`.
- [ ] Требование к отчёту включает блок «Передача» (`Следующий: <роль> — <что делает>`) — канон `TASK_HEADER_COMMON` → «Передача».
- [ ] Source-reminder учтён: при изменении методологии/канонов RESULT и «Передача» содержат «Обновить Source-снапшот у зарегистрированных потребителей: …» (`docs/agent-system/SOURCE_CONSUMERS.md`); иначе явно «не применимо» — канон `TASK_HEADER_COMMON` → «Source-reminder».
- [ ] Source Delta включён в final report и RESULT: таблица по всем затронутым файлам, категории взяты из `ADOPTION_TRANSFER_MANIFEST.yml`, Source-рекомендации и manifest flag заполнены; add/delete/rename inventory-файлов без manifest update → STOP.
- [ ] Orchestrator context handoff включён в final report и RESULT: per-task список построен из Source Delta, freshness stamp (`asof`, `developer_head_sha`) заполнен.
- [ ] Verified baseline is included or explicitly marked as not applicable.
- [ ] Repository/base branch/working branch are included.
- [ ] Allowed files are included.
- [ ] Forbidden files are included.
- [ ] Checks are included.
- [ ] STOP conditions are included.
- [ ] Final report requirements are included.
- [ ] No required execution context exists only in surrounding chat.
- [ ] Перед sync/checkout/switch/pull/merge/rebase: repository root, remote, текущая ветка и `git status --short` проверены; dirty tree → STOP (канон: `docs/agent-system/BRANCH_POLICY.md` → «Repository sync / checkout guard»).
- [ ] Перед commit: `git rev-parse --abbrev-ref HEAD` == work-ветка задачи; если `developer`/`main` → STOP (канон: `docs/agent-system/BRANCH_POLICY.md` → «Pre-commit branch guard»).

## Project constitution check

Project mission:
Current strategic goal:
Scope impact: <No scope expansion | Minor scope expansion | Major scope expansion>
Decision level: <Level 1 | Level 2 | Level 3 | Level 4>
Requires explicit user approval: <yes/no>
