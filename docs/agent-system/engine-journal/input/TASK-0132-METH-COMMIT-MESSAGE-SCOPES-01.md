# TASK для METH-COMMIT-MESSAGE-SCOPES-01

```yaml
task_contract:
  version: 1
  task_id: METH-COMMIT-MESSAGE-SCOPES-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-mir-11-commit-scopes-01

  scope:
    allowed_files:
      - docs/agent-system/LANGUAGE_POLICY.md
      - docs/agent-system/tools/validate_commit_message.py
      - docs/agent-system/cloud/00_README.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/20_LANGUAGE_POLICY.md
      - docs/agent-system/engine-journal/input/TASK-0132-METH-COMMIT-MESSAGE-SCOPES-01.md
      - docs/agent-system/engine-journal/output/RESULT-0132-METH-COMMIT-MESSAGE-SCOPES-01.md
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
      - product/runtime files
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
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_commit_message.py --message-text "docs(verification): проверить scope" --allowed-scope verification
      - python docs/agent-system/tools/validate_commit_message.py --message-text "docs(verification): проверить scope" expected_failure_without_verification_scope
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0132-METH-COMMIT-MESSAGE-SCOPES-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0132-METH-COMMIT-MESSAGE-SCOPES-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - developer_not_equal_origin_developer
    - changed_file_outside_allowlist
    - config_breaks_default_agent_system_scope
    - verification_scope_passes_without_allowlist
    - need_to_rewrite_merged_history
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Реализовать MIR-11 для patch release `v1.5.1`: сделать scope в
`validate_commit_message.py` конфигурируемым через `LANGUAGE_POLICY.md` и сохранить
default `[agent-system]` для публичного methodology repository.

## Baseline

- `origin/developer`: `3d06ab63164363e0a05875d7cf9cc02ff8680be4`.
- Latest release tag before patch series: `v1.5.0`.
- Last journal row before this task: `0131`.

## Acceptance criteria

- `validate_commit_message.py` читает `commit_metadata.allowed_scopes` из
  `LANGUAGE_POLICY.md`.
- При отсутствии config tool использует default `[agent-system]`.
- `docs(verification): проверить scope` проходит при добавленном
  `verification` в allowed scopes.
- `docs(verification): проверить scope` падает без `verification` в allowed
  scopes.
- `LANGUAGE_POLICY.md` содержит раздел allowed-scopes с примером target-расширения.
- Cloud mirror для `LANGUAGE_POLICY.md` и journal index регенерирован.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task contract
  validation, commit-message validation и diff whitespace check pass.

## Non-goals

- Не реализовывать MIR-10 release-boundary hardening.
- Не реализовывать MIR-12 ID-reference linter.
- Не реализовывать MIR-13 superseded-banner standard.
- Не создавать release `v1.5.1`, release PR или tag.
- Не читать target repositories и private downstream data.

## Передача

Следующий: methodology-reviewer-01 — scoped review MIR-11; затем архитектор —
human merge PR в `developer`; затем серия продолжается MIR-10, MIR-12 и MIR-13.
