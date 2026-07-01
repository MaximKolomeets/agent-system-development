# TASK для METH-RELEASE-PREP-V1-5-0-01

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-PREP-V1-5-0-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-release-prep-v1-5-0-01

  scope:
    allowed_files:
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/06_CURRENT_STATE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/08_NEXT_STEPS.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/engine-journal/input/TASK-0131-METH-RELEASE-PREP-V1-5-0-01.md
      - docs/agent-system/engine-journal/output/RESULT-0131-METH-RELEASE-PREP-V1-5-0-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0131-METH-RELEASE-PREP-V1-5-0-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0131-METH-RELEASE-PREP-V1-5-0-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - developer_not_equal_origin_developer
    - journal_0122_0129_not_closed
    - latest_tag_not_v1_4_1
    - changed_file_outside_allowlist
    - need_to_create_release_pr_in_same_task
    - need_to_push_main_or_create_tag
    - need_to_rewrite_merged_history
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Подготовить release-prep PR для methodology release `v1.5.0`:

- обновить `RELEASE_READINESS.md` под `v1.5.0`;
- обновить live/current runway в `CURRENT_STATE.md` и `NEXT_STEPS.md`;
- создать journal TASK/RESULT/INDEX entry `0131`;
- регенерировать cloud bundle mirrors;
- не создавать release PR `developer -> main` в этой задаче.

## Baseline

- `origin/main`: `1cad3af985fa48e7b0ca3358420d2cc5094b7ad6`.
- `origin/developer`: `4ed2662b5345798e99197fa14137e8154d946209`.
- Latest tag: `v1.4.1`.
- Next intended tag: `v1.5.0`.
- Last journal row before this task: `0130`.

## Acceptance criteria

- `RELEASE_READINESS.md` describes release candidate `origin/main` /
  `origin/developer`, latest tag `v1.4.1` and next tag `v1.5.0`.
- Payload summary covers 0122-0129 and journal batch-closure 0130.
- `CURRENT_STATE.md` and `NEXT_STEPS.md` point to release-prep `v1.5.0` and
  post-release Block B.
- Cloud mirrors for changed bundle sources are regenerated and pass parity checks.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task contract
  validation, commit-message validation and diff whitespace check pass.

## Non-goals

- Не создавать release PR `developer -> main`.
- Не мержить release PR.
- Не пушить `main`.
- Не создавать tag `v1.5.0` и GitHub Release.
- Не читать target repositories и private downstream data.

## Передача

Следующий: methodology-reviewer-01 — scoped release-prep review; затем архитектор —
human merge release-prep PR в `developer`; затем отдельная задача создаёт release PR
`developer -> main` для `v1.5.0`.
