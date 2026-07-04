# TASK: METH-RELEASE-PREP-V1-5-3-01

## Статус

- Статус: `in_progress`
- Создано: `2026-07-04T16:18:03.6525034+07:00`
- Роль: `release-manager-01`
- Исполнитель: на усмотрение архитектора
- Ветка: `work/release-manager-01/meth-release-prep-v1-5-3-01`
- Base: `origin/developer` / `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`

## task_contract

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-PREP-V1-5-3-01
  role: release-manager-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/release-manager-01/meth-release-prep-v1-5-3-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 1859a0034b14eed11e9842c4589fdeddb295cc6d
    reference_type: methodology_development
    checked_at: 2026-07-04T16:18:03.6525034+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/release-manager-01/meth-release-prep-v1-5-3-01
    base_commit: f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe
    checked_at: 2026-07-04T16:18:03.6525034+07:00

  scope:
    allowed_files:
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/RULESET_STATUS.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/**
      - docs/agent-system/engine-journal/output/RESULT-0155-METH-SELF-ENFORCEMENT-HARDENING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0156-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/output/RESULT-0157-METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01.md
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - AGENTS.md
      - .github/**
      - docs/agent-system/tools/**

  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: required
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-RELEASE-PREP-V1-5-3-01.md --json

  stop_conditions:
    - target_release_tag_already_exists
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - journal_history_rewrite_needed
    - release_action_needed
    - github_facts_unverifiable
    - secret_or_env_risk
    - destructive_git_needed
```

## Цель

Подготовить release-evidence для `v1.5.3`: base `v1.5.2`, candidate
`origin/developer` `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`, payload
`v1.5.2..origin/developer` с journal rows 0155-0157.

## Preflight evidence

- `refs/tags/v1.5.3`: отсутствует.
- `refs/tags/v1.5.2^{}`: `1859a0034b14eed11e9842c4589fdeddb295cc6d`.
- `refs/tags/v1.5.1^{}`: `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- `origin/main`: `1859a0034b14eed11e9842c4589fdeddb295cc6d`.
- `origin/developer`: `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`.
- PR #326: merged `2026-07-03T16:16:07Z`, merge `e7f1b01582f209ff689ff199bd3597c3e5f8321f`.
- PR #327: merged `2026-07-03T16:37:37Z`, merge `48560317211e9e81e5d2345a3115a886659062d7`.
- PR #328: merged `2026-07-04T09:00:34Z`, merge `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe`.

## Scope

Разрешены только release-prep evidence/state/journal/generated файлы из
`task_contract.scope.allowed_files`. Release PR, merge в `main`, tag, publication
и sync не выполняются.

Архитектор разрешил scope expansion для release-boundary reconciliation rows
0155-0157 в рамках PR #329. Разрешено только append-only добавить
closure-stamp в RESULT 0155-0157 и обновить status/summary в INDEX. Историческое
тело RESULT 0155-0157 не переписывать, прежние measured fields не менять.

## Acceptance criteria

- `RELEASE_READINESS.md` описывает `v1.5.3`, base `v1.5.2`, candidate
  `f10a06e2690bc8ff5c5cdb9afff893c39bee0dfe` и payload 0155-0157.
- `CURRENT_STATE.md`, `NEXT_STEPS.md`, `RULESET_STATUS.md` отражают актуальный
  candidate `v1.5.3`.
- `PROJECT_FILE_MAP.md` и `docs/agent-system/cloud/**` regenerated при drift.
- `RESULT` и `INDEX` финализированы без placeholders.
- Rows 0155-0157 boundary-closed for v1.5.3 release-prep scope.
- Required checks passed.

## Metadata cleanup note

Follow-up cleanup task: `METH-RELEASE-PREP-V1-5-3-METADATA-CLEANUP-01`.
Цель cleanup: убрать шумовые self-reference metadata в RESULT-0158 и обновить PR
body metadata без изменения release payload или boundary facts. Allowed scope:
только TASK-0158, RESULT-0158 и PR #329 body metadata. Release action не
выполнялся.

## Передача

Следующий: release-manager-01 - завершить release-prep v1.5.3 и открыть PR в
`developer`; затем methodology-reviewer-01 - scoped review release-prep.
