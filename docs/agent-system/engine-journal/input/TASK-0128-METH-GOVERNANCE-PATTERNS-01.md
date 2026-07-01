# TASK для METH-GOVERNANCE-PATTERNS-01

```yaml
task_contract:
  version: 1
  task_id: METH-GOVERNANCE-PATTERNS-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-governance-patterns-01

  scope:
    allowed_files:
      - docs/agent-system/POLICY_STATUS_PATTERN.md
      - docs/agent-system/ERROR_CATALOG_PATTERN.md
      - docs/agent-system/templates/ERROR_CATALOG_TEMPLATE.md
      - docs/agent-system/DECISION_NOTE_GUIDE.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/input/TASK-0128-METH-GOVERNANCE-PATTERNS-01.md
      - docs/agent-system/engine-journal/output/RESULT-0128-METH-GOVERNANCE-PATTERNS-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0128-METH-GOVERNANCE-PATTERNS-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0128-METH-GOVERNANCE-PATTERNS-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - need_to_change_tools_or_runtime_or_ci
    - need_to_materialize_target_specific_policy_status
    - need_to_include_real_error_cases_or_private_data
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Добавить governance-паттерны:

- `docs/agent-system/POLICY_STATUS_PATTERN.md` для статусов политик и alignment
  "политика vs фактическая стадия repository";
- `docs/agent-system/ERROR_CATALOG_PATTERN.md` и
  `docs/agent-system/templates/ERROR_CATALOG_TEMPLATE.md` для стабильных
  error/blocker codes, согласованных с `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`;
- `docs/agent-system/DECISION_NOTE_GUIDE.md` для границы между строкой в
  `DECISION_LOG.md`, отдельной decision note и Level 3/4 owner approval.

Добавить ссылки из `METHODOLOGY_MAP.md`, `DECISION_LOG.md` и
`TARGET_PROJECT_GOVERNANCE_PACK.md`, зарегистрировать source/template и
target-generated mappings в `ADOPTION_TRANSFER_MANIFEST.yml`, затем обновить
generated file map/cloud mirrors штатными генераторами.

## Non-goals

- Не материализовать target-local `POLICY_STATUS.md` или `ERROR_CATALOG.md`.
- Не добавлять реальные error cases, private data или target-specific facts.
- Не навязывать паттерны ретроспективно всем target repositories.
- Не менять tools/runtime/CI.

## Контекст sequence

Актуальный `docs/agent-system/engine-journal/INDEX.md` после threat model template
завершается на `0127`. По правилу `INDEX last+1` фактический journal seq этой
задачи: `0128`.

## Acceptance criteria

- `POLICY_STATUS_PATTERN.md` описывает назначение, канонические статусы,
  минимальные поля и alignment policy vs repo-state.
- `ERROR_CATALOG_PATTERN.md` описывает стабильность codes, обязательные поля,
  связь с `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` и fixture requirement.
- `templates/ERROR_CATALOG_TEMPLATE.md` содержит таблицу fields:
  `severity`, `user_message`, `dev_message`, `retryable`, `blocks_state`,
  `audit_required`, `test_fixture`.
- `DECISION_NOTE_GUIDE.md` отделяет обычную строку `DECISION_LOG.md` от decision
  note и фиксирует Level 3/4 owner approval semantics.
- `METHODOLOGY_MAP.md`, `DECISION_LOG.md` и `TARGET_PROJECT_GOVERNANCE_PACK.md`
  ссылаются на новые patterns без target-specific data.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` и generated cloud
  mirrors согласованы с новыми source/template/journal files.

## Expected reviewer mode

Scoped methodology review: reviewer проверяет governance boundaries, связь
error catalog с acceptance pattern, policy status alignment, decision note
approval semantics, manifest/generated parity и отсутствие private target data.

## Передача

Следующий: reviewer — scoped governance patterns review.
