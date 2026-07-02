# TASK для METH-BATCH-CLOSURE-0142-0152-V1-5-2-01

```yaml
task_contract:
  version: 1
  task_id: METH-BATCH-CLOSURE-0142-0152-V1-5-2-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/batch-closure-0142-0152-v1-5-2-01

  methodology_development_base:
    base_branch: developer
    working_branch: work/docs-maintainer-01/batch-closure-0142-0152-v1-5-2-01
    base_commit: d102590705e404537c8072d6ce6cf6cf5bb5fee2
    checked_at: 2026-07-03T00:22:25.2094126+07:00

  scope:
    allowed_files:
      - docs/agent-system/engine-journal/output/RESULT-0142-METH-NAVIGATION-DISCOVERY-H5-01.md
      - docs/agent-system/engine-journal/output/RESULT-0143-METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01.md
      - docs/agent-system/engine-journal/output/RESULT-0144-METH-BUSINESS-ACCEPTANCE-UAT-H13-01.md
      - docs/agent-system/engine-journal/output/RESULT-0145-METH-HOTFIX-ROLLBACK-DR-H14-01.md
      - docs/agent-system/engine-journal/output/RESULT-0146-METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01.md
      - docs/agent-system/engine-journal/output/RESULT-0147-METH-MANAGEMENT-LAYER-H7-01.md
      - docs/agent-system/engine-journal/output/RESULT-0148-METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01.md
      - docs/agent-system/engine-journal/output/RESULT-0149-METH-POLICY-INVARIANTS-SELF-TEST-H11-01.md
      - docs/agent-system/engine-journal/output/RESULT-0150-METH-AGENT-INITIATIVE-FEEDBACK-H12-01.md
      - docs/agent-system/engine-journal/output/RESULT-0151-METH-JOURNAL-ARCHIVING-H15-01.md
      - docs/agent-system/engine-journal/output/RESULT-0152-METH-LIFECYCLE-CROSS-PROJECT-H16-01.md
      - docs/agent-system/engine-journal/input/TASK-0153-METH-BATCH-CLOSURE-0142-0152-V1-5-2-01.md
      - docs/agent-system/engine-journal/output/RESULT-0153-METH-BATCH-CLOSURE-0142-0152-V1-5-2-01.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
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
    boundary_reconciliation: release_or_audit_only
    language: russian_first

  checks:
    required:
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0153-METH-BATCH-CLOSURE-0142-0152-V1-5-2-01.md
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - any_pr_in_closure_set_not_merged
    - stale_final_status_in_closure_set
    - need_to_rewrite_merged_history
    - need_to_change_product_runtime_or_ci_workflow
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Закрыть перед release boundary v1.5.2 merged-but-unclosed journal entries
`0142`-`0152`, включая зависшую строку `0147`: добавить factual closure stamp в
RESULT, перевести строки `INDEX.md` в closed status и создать собственную
terminal-fold запись `0153`.

## Предусловия

- `developer` синхронизирован с `origin/developer` на
  `d102590705e404537c8072d6ce6cf6cf5bb5fee2`.
- PR #311-#321 подтверждены через `gh pr view` как `MERGED`.
- Эта задача не начинает release-prep PR и не меняет release/state docs.

## Non-goals

- Не начинать release-prep PR.
- Не менять `RELEASE_READINESS.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`.
- Не создавать release PR `developer -> main`.
- Не мержить PR, не пушить `main`, не создавать tag и GitHub Release.
- Не переписывать merged history и не менять содержательные каноны.

## Acceptance criteria

- RESULT 0142-0152 имеют `status: closed; PR #... merged; facts in closure stamp`.
- RESULT 0142-0152 содержат merge facts: PR URL, state, base/head branch,
  reviewed head SHA, `merged_at`, merge commit и `gh pr view` как source.
- INDEX rows 0142-0152 имеют status `closed; PR #... merged; facts in RESULT`.
- Собственная запись 0153 является lifecycle-only terminal fold.
- `cloud/07_ENGINE_JOURNAL_INDEX.md` синхронизирован с `INDEX.md`.
- Release-prep явно оставлен за пределами этой задачи до merge batch-closure PR.

## Передача

Следующий: methodology-reviewer-01 — scoped review batch-closure PR; затем
архитектор — human merge; затем release-prep PR v1.5.2.
