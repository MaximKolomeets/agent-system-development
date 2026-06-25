# TASK_CONTRACT

## Назначение

`task_contract` — machine-readable frontmatter для задач исполнителя. Он дополняет prose-first task block и даёт инструментам заранее понятные режим, scope, ветки, проверки, STOP-условия и политики journal/cloud/review.

Prose остаётся обязательным для человека: цель, контекст и смысловые ограничения пишутся обычным текстом. `task_contract` нужен как компактный источник истины для machine checks.

Если `task_contract` присутствует, исполнитель использует его как источник истины для режима, scope, checks и STOP-условий. Если `task_contract` и prose противоречат друг другу, исполнитель пишет `STOP` и просит уточнение архитектора.

## Формат

Рекомендуемый формат — fenced YAML block в начале TASK file или self-contained Engine-блока:

```yaml
task_contract:
  version: 1
  task_id: METH-TASK-CONTRACT-FRONTMATTER-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-task-contract-frontmatter-01

  scope:
    allowed_files:
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/tools/validate_task_contract.py
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - verification/**
      - product repositories

  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false

  checks:
    required:
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - python docs/agent-system/tools/validate_task_contract.py <task-file> --json

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
```

## Обязательные поля

Для новых write-action Engine-задач обязательны:

- `version`
- `task_id`
- `role`
- `mode`
- `execution_mode`
- `repository.full_name`
- `repository.local_path`
- `repository.base_branch`
- `repository.working_branch`
- `scope.allowed_files`
- `scope.forbidden_files`
- `policies.journal`
- `policies.cloud_regen`
- `policies.review`
- `policies.merge`
- `checks.required`
- `stop_conditions`

## Допустимые значения

`mode`:

- `agent`
- `review_only`
- `ask`
- `manual`

`execution_mode`:

- `local_only`
- `cloud_allowed`
- `hybrid`

`policies.journal`:

- `required`
- `optional`
- `not_required`
- `batch_only`

`policies.cloud_regen`:

- `required`
- `if_bundle_source_changed`
- `not_required`

`policies.review`:

- `scoped_semantic`
- `scoped_technical_safety`
- `machine_only`
- `full_review`
- `not_required`

`policies.merge`:

- `human_only`
- `not_applicable`

`policies.closure_pr`:

- `true`
- `false`
- `boundary_only`

## Policy checks

Минимальная policy validation:

- `repository.working_branch` должен начинаться с `work/`;
- `repository.base_branch` не должен быть `main`, кроме release-подготовки, где это явно объяснено prose;
- `scope.allowed_files` не должен быть пустым для write-action задач;
- `scope.forbidden_files` должен включать `.env` или `.env.*`;
- `policies.merge` для substantive/write-action задач должен быть `human_only`;
- `checks.required` должен включать `python docs/agent-system/tools/check_task_ready.py --base origin/developer` или явное объяснение в prose, почему ready-gate не применим.

## Validator

Лёгкий валидатор:

```text
python docs/agent-system/tools/validate_task_contract.py <task-file>
python docs/agent-system/tools/validate_task_contract.py <task-file> --json
```

Ограничения валидатора:

- использует только Python stdlib;
- read-only: не выполняет `git fetch`, `pull`, `switch`, `merge`, `rebase`, `stash`, `reset`, `clean`, `push`;
- не читает `.env`;
- не печатает matching secret lines или secret values;
- ищет fenced block, содержащий `task_contract:`;
- поддерживает минимальный YAML-subset: indentation, string scalars, nested dicts, scalar lists `- item`;
- не является полноценным YAML parser и не должен заменять human review сложных prose-ограничений.

Human output:

```text
validate_task_contract
task_id: METH-TASK-CONTRACT-FRONTMATTER-01
version: 1
role: methodology-architect-01
mode: agent
working_branch: work/methodology-architect-01/meth-task-contract-frontmatter-01
required_fields: passed
enum_values: passed
branch_policy: passed
scope_policy: passed
checks_policy: passed
blockers_count: 0
warnings_count: 0
result: valid
```

JSON output:

```json
{"result":"valid","blockers_count":0,"warnings_count":0,"task_id":"METH-TASK-CONTRACT-FRONTMATTER-01"}
```

## Когда требуется

`task_contract` обязателен для новых задач, которые:

- меняют repository files;
- создают commit/push/PR;
- являются substantive/tooling/docs-only PR task;
- являются review/fix-pass task с branch changes;
- выполняют release/adoption/source-update flow.

`task_contract` не обязателен для маленькой Fast Lane проверки без write-action, без PR и без journal trace.
