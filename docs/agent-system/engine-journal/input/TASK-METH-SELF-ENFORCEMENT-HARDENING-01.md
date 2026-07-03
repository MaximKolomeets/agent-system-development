# TASK для METH-SELF-ENFORCEMENT-HARDENING-01

```yaml
task_contract:
  version: 1
  task_id: METH-SELF-ENFORCEMENT-HARDENING-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-self-enforcement-hardening-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 1859a0034b14eed11e9842c4589fdeddb295cc6d
    reference_type: methodology_development
    checked_at: 2026-07-03T18:34:30.5363271+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-self-enforcement-hardening-01
    base_commit: 3dbab06a20278cacb1c4d87d0f1815b6d4d6a378
    checked_at: 2026-07-03T18:34:30.5363271+07:00

  scope:
    allowed_files:
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - .github/workflows/methodology-checks.yml
      - docs/agent-system/tools/check_commit_language.py
      - docs/agent-system/tools/check_journal_append_only.py
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/METHODOLOGY_IMPROVEMENT_LEDGER.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/engine-journal/**
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
      - AGENTS.md
      - docs/agent-system/MANUAL_REVIEW_CHECKLIST.md
      - docs/agent-system/TASK_CONTRACT.md

  policies:
    journal: required
    cloud_regen: required
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
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-SELF-ENFORCEMENT-HARDENING-01.md --json

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
    - ci_check_causes_broad_false_positive
```

Идентификатор задачи: `METH-SELF-ENFORCEMENT-HARDENING-01`

Номер sequence: `0155`

Создано: `2026-07-03T18:34:30.5363271+07:00`

execution_started_at: `2026-07-03T18:34:30.5363271+07:00`

orchestration_time_reported: not_reported

actor_type: agent

role: methodology-architect-01

time_source: measured

time_report_confidence: medium

Автор: пользователь-архитектор

Цель: закрыть self-enforcement gaps A/B/C одним methodology PR в `developer`:
pre-emit self-review в `ENGINE_ENTRYPOINT.md`, CI workflow поверх существующих
валидаторов плюс два узких новых check script, manifest annotations и generated
artifacts.

Allowed files и STOP-условия заданы в `task_contract`; `AGENTS.md`,
`MANUAL_REVIEW_CHECKLIST.md` и `TASK_CONTRACT.md` не менять.

Ожидаемый RESULT file:

`docs/agent-system/engine-journal/output/RESULT-0155-METH-SELF-ENFORCEMENT-HARDENING-01.md`

Передача:

Следующий: methodology-architect-01 - выполнить задачу в этой branch; затем
methodology-reviewer-01 - scoped semantic review PR в `developer`.
