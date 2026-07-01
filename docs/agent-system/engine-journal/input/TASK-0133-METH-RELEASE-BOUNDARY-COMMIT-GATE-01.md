# TASK для METH-RELEASE-BOUNDARY-COMMIT-GATE-01

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-BOUNDARY-COMMIT-GATE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-mir-10-release-boundary-gate-01

  scope:
    allowed_files:
      - docs/agent-system/BRANCH_POLICY.md
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/validate_commit_message.py
      - docs/agent-system/cloud/04_BRANCH_POLICY.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0133-METH-RELEASE-BOUNDARY-COMMIT-GATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0133-METH-RELEASE-BOUNDARY-COMMIT-GATE-01.md
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
      - python docs/agent-system/tools/validate_commit_message.py --base v1.4.1 --cutoff-ref v1.5.0
      - python docs/agent-system/tools/validate_commit_message.py --message-text "fix bad message" expected_failure
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0133-METH-RELEASE-BOUNDARY-COMMIT-GATE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0133-METH-RELEASE-BOUNDARY-COMMIT-GATE-01.md --json
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
    - release_boundary_still_scans_pre_gate_history_without_cutoff
    - work_pr_bad_message_passes
    - need_to_rewrite_merged_history
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Реализовать MIR-10 для patch release `v1.5.1`: hardening commit-message gate на
release boundary, чтобы release PR `developer -> main` не блокировался на
GitHub merge commits и до-гейтовой истории.

## Baseline

- `origin/developer`: `3aac7a01a1f10c06ff053be39b75168ee7fe7db8`.
- PR #298 merged at `2026-07-01T16:36:05Z`.
- Latest release tag before patch series: `v1.5.0`.
- Last journal row before this task: `0132`.

## Acceptance criteria

- `validate_commit_message.py` по умолчанию использует `git rev-list --no-merges`.
- `validate_commit_message.py --cutoff-ref <ref>` исключает до-гейтовую историю.
- `check_task_ready.py --release-boundary` не запускает commit-message range check
  без явного cutoff.
- Обычный work-PR gate через `--base origin/developer` остаётся строгим.
- Bad message smoke падает.
- `BRANCH_POLICY.md` и `CI_POLICY.md` описывают release-boundary поведение.
- Cloud mirror для `BRANCH_POLICY.md` и journal index регенерирован.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task contract
  validation, commit-message validation и diff whitespace check pass.

## Non-goals

- Не реализовывать MIR-12 ID-reference linter.
- Не реализовывать MIR-13 superseded-banner standard.
- Не создавать release `v1.5.1`, release PR или tag.
- Не читать target repositories и private downstream data.
- Не переписывать historical commits или merge commits.

## Передача

Следующий: methodology-reviewer-01 — scoped review MIR-10; затем архитектор —
human merge PR в `developer`; затем серия продолжается MIR-12 и MIR-13.
