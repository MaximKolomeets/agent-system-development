# TASK для METH-JOURNAL-HISTORY-SCOPE-CLARITY-01

```yaml
task_contract:
  version: 1
  task_id: METH-JOURNAL-HISTORY-SCOPE-CLARITY-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-v1-5-2-pr-2-journal-scope

  scope:
    allowed_files:
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/CODE_REVIEW_WORKFLOW.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/05_ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0139-METH-JOURNAL-HISTORY-SCOPE-CLARITY-01.md
      - docs/agent-system/engine-journal/output/RESULT-0139-METH-JOURNAL-HISTORY-SCOPE-CLARITY-01.md
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
    post_merge_closure: not_required_for_ordinary_pr
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0139-METH-JOURNAL-HISTORY-SCOPE-CLARITY-01.md
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
    - changed_file_outside_allowlist
    - task_changes_h3_or_later_scope
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Выполнить PR-2/H2 из пакета `BLOCK_METH_v1_5_2.md`: снять противоречие между
scaffold-only journal transfer в target repositories и легитимной operational
history внутри самого `agent-system-development`.

## Baseline

- `origin/developer`: `f993dba56d03682d80f757cf034616fe954f1ea4`.
- PR #306: merged, PR-1/H1 завершён.
- Last journal row before this task: `0138`.
- `execution_started_at`: `2026-07-02T16:03:43.3465401+07:00`.

## Acceptance criteria

- `ENGINE_JOURNAL_CONTRACT.md` явно различает target `scaffold_only` transfer и
  methodology repository operational history.
- Reviewer check больше не требует пустые `input/`/`output/` в
  `agent-system-development`, если rows относятся к methodology lifecycle.
- `CODE_REVIEW_WORKFLOW.md` синхронизирован с новым journal history scope check.
- `ADOPTION_TRANSFER_MANIFEST.yml` содержит machine-readable `journal_transfer_mode`.
- Target adoption не копирует operational rows/TASK/RESULT source methodology
  repository verbatim.
- `PROJECT_FILE_MAP.md` и `cloud/**` согласованы с manifest/source changes.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task
  contract validation, commit-message validation and diff whitespace check pass.

## Non-goals

- Не реализовывать H3 time/cost hard-gate.
- Не менять release authority, UAT, rollback или stable-reference schema.
- Не переносить target repositories.
- Не читать private downstream data.

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-2/H2; затем архитектор —
human merge; затем methodology-architect-01 — PR-3/H3 time and cost accounting.
