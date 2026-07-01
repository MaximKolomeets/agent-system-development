# TASK для METH-CONTROL-MATRIX-PATTERN-01

```yaml
task_contract:
  version: 1
  task_id: METH-CONTROL-MATRIX-PATTERN-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-control-matrix-pattern-01

  scope:
    allowed_files:
      - docs/agent-system/CONTROL_MATRIX_PATTERN.md
      - docs/agent-system/templates/CONTROL_MATRIX_TEMPLATE.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/input/TASK-0125-METH-CONTROL-MATRIX-PATTERN-01.md
      - docs/agent-system/engine-journal/output/RESULT-0125-METH-CONTROL-MATRIX-PATTERN-01.md
      - docs/agent-system/engine-journal/INDEX.md
    forbidden_files:
      - .env
      - .env.*
      - .venv/**
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - docs/agent-system/tools/**
      - product/runtime/CI files
      - credentials
      - tokens
      - access key material
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data
      - production/runtime data

  policies:
    journal: required
    cloud_regen: required
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    language: russian_first

  checks:
    required:
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0125-METH-CONTROL-MATRIX-PATTERN-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0125-METH-CONTROL-MATRIX-PATTERN-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - retroactive_force_control_matrix_into_targets
    - need_to_change_tools_or_runtime_or_ci
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Добавить reusable паттерн `CONTROL_MATRIX_PATTERN.md` и template
`CONTROL_MATRIX_TEMPLATE.md`, чтобы target repositories могли связывать
policy-инварианты с implementation, tests, CI-gates, stage, fail-mode и owner.
Добавить ссылки из `TARGET_PROJECT_GOVERNANCE_PACK.md` и `METHODOLOGY_MAP.md`,
зарегистрировать новые files в manifest и обновить generated maps/mirrors
штатными генераторами.

## Non-goals

- Не навязывать control matrix всем target repositories задним числом.
- Не дублировать детали реализации в политиках.
- Не менять tools/runtime/CI.
- Не включать private downstream data или project-specific сведения.

## Контекст sequence

Актуальный `docs/agent-system/engine-journal/INDEX.md` после navigation index
завершается на `0124`. По правилу `INDEX last+1` фактический journal seq этой
задачи: `0125`.

## Acceptance criteria

- Pattern описывает минимальные поля, правила, связь с
  `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` и границу source vs target facts.
- Template пригоден к заполнению в target repository.
- `TARGET_PROJECT_GOVERNANCE_PACK.md` и `METHODOLOGY_MAP.md` ссылаются на
  pattern/template без ретроактивного требования для всех проектов.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` и generated cloud
  mirrors согласованы с новыми source/template files и journal row.
- Tools/runtime/CI и product files не меняются.

## Expected reviewer mode

Scoped methodology review: reviewer проверяет полноту pattern/template,
корректность ссылок, отсутствие scope drift и generated parity.

## Передача

Следующий: reviewer — scoped control matrix pattern review.
