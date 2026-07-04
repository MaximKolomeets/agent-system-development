# TASK METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01

Файл задачи: `docs/agent-system/engine-journal/input/TASK-METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01.md`

Идентификатор задачи: `METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01`

Sequence: `0157`

Роль: `dev-implementer-01`

Исполнитель: на усмотрение архитектора

Режим: `agent`

Запуск: `local_only`

Reasoning effort: `high`

execution_started_at: `2026-07-03T23:52:15.2036210+07:00`

Base branch: `developer`

Working branch: `work/dev-implementer-01/meth-commit-language-tool-reconcile-01`

Task source: attached Engine block `METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01`

## task_contract

```yaml
task_contract:
  version: 1
  task_id: METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01
  role: dev-implementer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-commit-language-tool-reconcile-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 1859a0034b14eed11e9842c4589fdeddb295cc6d
    reference_type: methodology_development
    checked_at: 2026-07-03T00:00:00+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-commit-language-tool-reconcile-01
    base_commit: 48560317211e9e81e5d2345a3115a886659062d7
    checked_at: 2026-07-03T23:52:15.2036210+07:00

  scope:
    allowed_files:
      - docs/agent-system/tools/validate_commit_message.py
      - .github/workflows/methodology-checks.yml
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/ADOPTION_GUIDE.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
      - docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
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
      - docs/agent-system/engine-journal/output/RESULT-0155-METH-SELF-ENFORCEMENT-HARDENING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0156-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/input/TASK-METH-SELF-ENFORCEMENT-HARDENING-01.md
      - docs/agent-system/engine-journal/input/TASK-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md

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
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01.md --json

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - journal_history_rewrite_needed
    - residual_reference_to_removed_tool
    - body_language_check_causes_broad_false_positive
    - secret_or_env_risk
    - destructive_git_needed
```

## Цель

Сделать `docs/agent-system/tools/validate_commit_message.py` единственным
каноническим commit-language gate, перенести в него узкую проверку Russian-first
для тела commit и вывести из активного оборота duplicate commit-language tool.

## Требования

- Добавить в canonical tool проверку тела commit с кодом `BODY_NOT_RUSSIAN_FIRST`.
- Удалить duplicate commit-language tool и все активные ссылки на него.
- CI должен полагаться на canonical tool через `check_task_ready.py` или явный
  вызов `validate_commit_message.py`.
- Manifest source list и generated artifacts должны быть согласованы.
- Старые journal artifacts 0155/0156 не менять.
- Новые TASK/RESULT не должны заново создавать активную буквальную ссылку на
  удаляемый filename.

## Проверки

- `python docs/agent-system/tools/validate_commit_message.py --base origin/developer`
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`
- `python docs/agent-system/tools/validate_policy_invariants.py`
- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check origin/developer...HEAD`
- residual reference grep outside historical journal artifacts must be empty.

## Передача

Следующий: dev-implementer-01 — выполнить tooling reconcile и открыть PR в
`developer`; затем reviewer — scoped semantic review.
