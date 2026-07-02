# TASK для METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01

```yaml
task_contract:
  version: 1
  task_id: METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-v1-5-2-pr-1-state-refresh

  scope:
    allowed_files:
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/RULESET_STATUS.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/00_README.md
      - docs/agent-system/cloud/06_CURRENT_STATE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/08_NEXT_STEPS.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0138-METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01.md
      - docs/agent-system/engine-journal/output/RESULT-0137-METH-RELEASE-PREP-V1-5-1-01.md
      - docs/agent-system/engine-journal/output/RESULT-0138-METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01.md
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
    generated_checks: required
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required_for_ordinary_pr
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0138-METH-POST-RELEASE-STATE-REFRESH-V1-5-2-PR1-01.md
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
    - v1_5_1_release_or_sync_not_merged
    - tag_v1_5_1_not_on_release_merge_commit
    - changed_file_outside_allowlist
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Выполнить PR-1/H1 из пакета `BLOCK_METH_v1_5_2.md`: post-release
state/status refresh после публикации `v1.5.1`, убрать stale-указания на будущий
release-prep `v1.5.1`, разделить ближайшие шаги и backlog, зафиксировать ruleset
status snapshot и регенерировать context cloud bundle.

## Baseline

- `origin/main`: `2467edd8488a51d74483e8095e4887c0f512dfcd`.
- `origin/developer`: `2407cd4950b05fd2bb03583f9ccb1fe84d53eac5`.
- Latest release tag before this task: `v1.5.1`.
- PR #303: merged release-prep for `v1.5.1`.
- PR #304: merged release PR `developer -> main` for `v1.5.1`.
- PR #305: merged sync PR `main -> developer`.
- Last journal row before this task: `0137`.
- `execution_started_at`: `2026-07-02T15:33:24.0768470+07:00`.

## Acceptance criteria

- `CURRENT_STATE.md` and `NEXT_STEPS.md` no longer claim that release-prep or
  release PR `v1.5.1` is ahead.
- `RELEASE_READINESS.md` reflects `v1.5.1` as `published/synced`.
- `BACKLOG.md` contains future tasks, while `NEXT_STEPS.md` contains only nearest
  actions.
- `RULESET_STATUS.md` contains dated machine-readable status for `Protect main`
  and `Protect developer`.
- Journal row 0137 is reconciled with release/sync/tag facts.
- New journal row 0138 is created with TASK/RESULT.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` and
  `docs/agent-system/cloud/**` are regenerated/consistent.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task
  contract validation, commit-message validation and diff whitespace check pass.

## Non-goals

- Не реализовывать H2-H16 в этом PR.
- Не создавать release PR `v1.5.2`.
- Не мержить release PR.
- Не пушить `main` напрямую.
- Не создавать tag.
- Не публиковать GitHub Release.
- Не читать target repositories и private downstream data.

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-1/H1; затем архитектор —
human merge; затем docs-maintainer-01 — PR-2/H2 journal history scope clarity.
