# TASK для METH-RELEASE-PREP-V1-5-1-01

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-PREP-V1-5-1-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-release-prep-v1-5-1-01

  scope:
    allowed_files:
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/cloud/00_README.md
      - docs/agent-system/cloud/06_CURRENT_STATE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/08_NEXT_STEPS.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0137-METH-RELEASE-PREP-V1-5-1-01.md
      - docs/agent-system/engine-journal/output/RESULT-0132-METH-COMMIT-MESSAGE-SCOPES-01.md
      - docs/agent-system/engine-journal/output/RESULT-0133-METH-RELEASE-BOUNDARY-COMMIT-GATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0134-METH-ID-REFERENCE-GATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0135-METH-SUPERSEDED-BANNER-01.md
      - docs/agent-system/engine-journal/output/RESULT-0136-METH-EXECUTION-TIMING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0137-METH-RELEASE-PREP-V1-5-1-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0137-METH-RELEASE-PREP-V1-5-1-01.md
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - git diff --check origin/developer...HEAD
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - developer_not_equal_origin_developer
    - pr_298_302_not_merged
    - changed_file_outside_allowlist
    - release_readiness_not_v1_5_1
    - journal_boundary_reconciliation_incomplete
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Подготовить release-prep PR для methodology patch release `v1.5.1` после merge
MIR-10, MIR-11, MIR-12, MIR-13 и MIR-14.

## Baseline

- `origin/main`: `170ec8e23981f7a379db843ea67314b5cb47ef7c`.
- `origin/developer`: `344c347fdf01a4b1e73a40bebb08fc520d0d51e8`.
- Latest release tag before this task: `v1.5.0`.
- Next intended release tag: `v1.5.1`.
- PR #298-#302: merged.
- Last journal row before this task: `0136`.
- `execution_started_at`: `2026-07-02T08:39:33.9080104+07:00`.

## Acceptance criteria

- `RELEASE_READINESS.md` обновлён под `v1.5.1` with candidate SHA, latest tag,
  next tag, payload summary, journal gate and safety recommendation.
- `CURRENT_STATE.md` and `NEXT_STEPS.md` refreshed for the post-`v1.5.1` runway.
- Journal rows 0132-0136 reconciled with GitHub merge facts for release boundary.
- New journal row 0137 added with TASK/RESULT.
- Cloud mirrors regenerated for changed bundle files.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task
  contract validation, commit-message validation and diff whitespace check pass.

## Non-goals

- Не создавать release PR in this release-prep PR.
- Не мержить release PR.
- Не пушить `main` напрямую.
- Не создавать tag in this release-prep PR.
- Не публиковать GitHub Release.
- Не читать target repositories и private downstream data.

## Передача

Следующий: methodology-reviewer-01 — scoped release-prep review; затем
архитектор — human merge release-prep PR; затем отдельной задачей release PR
`developer -> main` для `v1.5.1`.
