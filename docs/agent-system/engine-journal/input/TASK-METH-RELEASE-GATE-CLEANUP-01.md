# TASK: METH-RELEASE-GATE-CLEANUP-01

## Статус

- Статус: `in_progress`
- Создано: `2026-07-05T12:49:48.2905099+07:00`
- Роль: `dev-implementer-01`
- Исполнитель: на усмотрение архитектора
- Ветка: `work/dev-implementer-01/meth-release-gate-cleanup-01`
- Base: `origin/developer` / `4a57b7169fbc92c0da1405e30804a69b3c9c58af`

## task_contract

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-GATE-CLEANUP-01
  role: dev-implementer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-release-gate-cleanup-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: f0c75a965e19b78f9c018c406680b12caaf255c1
    reference_type: methodology_development
    checked_at: 2026-07-05T12:49:48.2905099+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-release-gate-cleanup-01
    base_commit: 4a57b7169fbc92c0da1405e30804a69b3c9c58af
    checked_at: 2026-07-05T12:49:48.2905099+07:00

  scope:
    allowed_files:
      - docs/agent-system/tools/release_gate.py
      - docs/agent-system/RELEASE_AUTHORITY_POLICY.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/METHODOLOGY_IMPROVEMENT_LEDGER.md
      - docs/agent-system/cloud/**
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
      - .github/**
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/engine-journal/output/RESULT-0155-METH-SELF-ENFORCEMENT-HARDENING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0156-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/output/RESULT-0157-METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0158-METH-RELEASE-PREP-V1-5-3-01.md
      - docs/agent-system/engine-journal/output/RESULT-0159-METH-POST-RELEASE-STATE-REFRESH-V1-5-3-01.md
      - docs/agent-system/engine-journal/output/RESULT-0160-METH-RELEASE-ASSISTANT-01.md

  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: conditional
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-RELEASE-GATE-CLEANUP-01.md --json

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - journal_history_rewrite_needed
    - tool_requires_git_write_action
    - secret_or_env_risk
    - destructive_git_needed
```

## Цель

Доработать `release_gate.py` по findings review PR #333:

- I-01: явно зафиксировать, что tag-проверка читает локальные `refs/tags` и требует предварительного `git fetch --tags --prune` как human/preflight action.
- O-02: развести запуск release-boundary ready-gate вне `developer` и реальный провал готовности на `developer`.

## Acceptance criteria

- `release_gate.py` остаётся read-only: нет `git fetch` и write-команд.
- В text и `--json` output есть `tag_source: local_refs_requires_prefetch` и precondition-текст про `git fetch --tags --prune`.
- На work-ветке `--version v1.5.4 --json` даёт warning `READY_GATE_SKIPPED_OFF_DEVELOPER`, но не blocker `RELEASE_BOUNDARY_READY_GATE_FAILED`.
- На `developer` при реальном провале release-boundary ready-gate blocker `RELEASE_BOUNDARY_READY_GATE_FAILED` сохраняется.
- `RELEASE_AUTHORITY_POLICY.md` требует human/preflight `git fetch --tags --prune` перед `release_gate.py`.
- Journal row 0161 финализирован без unresolved placeholders.

## Запрещено

- Не выполнять merge/tag/publish/sync/push как release action.
- Не читать `.env`.
- Не редактировать `.github/**`, `AGENTS.md`, `ADOPTION_TRANSFER_MANIFEST.yml`.
- Не переписывать finalized RESULT 0155-0160.
- Не добавлять `git fetch` внутрь `release_gate.py`.

## Передача

Следующий: reviewer - scoped semantic review.
