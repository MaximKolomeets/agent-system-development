# TASK: METH-RELEASE-ASSISTANT-01

## Статус

- Статус: `in_progress`
- Создано: `2026-07-04T18:57:25.9461620+07:00`
- Роль: `dev-implementer-01`
- Исполнитель: на усмотрение архитектора
- Ветка: `work/dev-implementer-01/meth-release-assistant-01`
- Base: `origin/developer` / `d15e4147f9629d20d754da24cd1b26043e8d945d`

## task_contract

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-ASSISTANT-01
  role: dev-implementer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-release-assistant-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: f0c75a965e19b78f9c018c406680b12caaf255c1
    reference_type: methodology_development
    checked_at: 2026-07-04T18:57:25.9461620+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-release-assistant-01
    base_commit: d15e4147f9629d20d754da24cd1b26043e8d945d
    checked_at: 2026-07-04T18:57:25.9461620+07:00

  scope:
    allowed_files:
      - docs/agent-system/tools/release_gate.py
      - docs/agent-system/RELEASE_AUTHORITY_POLICY.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/METHODOLOGY_IMPROVEMENT_LEDGER.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
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
      - docs/agent-system/engine-journal/output/RESULT-0155-METH-SELF-ENFORCEMENT-HARDENING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0156-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/output/RESULT-0157-METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01.md

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
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-RELEASE-ASSISTANT-01.md --json

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

Добавить read-only `docs/agent-system/tools/release_gate.py --version vX.Y.Z`,
который собирает release evidence, проверяет отсутствие target tag, сверяет base
tag / `origin/main`, payload и generated/state gates, а затем печатает
human-action text без выполнения release actions.

## Acceptance criteria

- `release_gate.py` использует только Python stdlib и read-only `git` commands.
- `--version v1.5.3 --json` возвращает blocker `RELEASE_TAG_ALREADY_EXISTS`.
- `--version v1.5.4 --json` показывает `tag_exists: false`; возможный
  `RELEASE_BOUNDARY_READY_GATE_FAILED` на work-ветке допустим, потому что
  `check_task_ready.py --release-boundary` канонически работает только на
  `developer`.
- Tool добавлен в manifest source tools, `PROJECT_FILE_MAP.md` и cloud mirrors
  регенерированы.
- `RELEASE_AUTHORITY_POLICY.md` ссылается на запуск release gate перед release
  boundary.
- Journal row 0160 финализирован без unresolved placeholders.

## Запрещено

- Не выполнять merge/tag/publish/sync/push.
- Не читать `.env`.
- Не редактировать `.github/**`.
- Не переписывать finalized RESULT 0155-0157.

## Передача

Следующий: reviewer - scoped semantic review; затем архитектор - human merge.
