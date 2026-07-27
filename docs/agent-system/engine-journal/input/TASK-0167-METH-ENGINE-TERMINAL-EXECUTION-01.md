# TASK-0167-METH-ENGINE-TERMINAL-EXECUTION-01

```yaml
task_contract:
  version: 2
  task_id: METH-ENGINE-TERMINAL-EXECUTION-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-engine-terminal-execution-01
  methodology_development_base:
    base_branch: developer
    base_commit: afe34debd93d2eae8f9c498959f602d2d664416e
  scope:
    allowed_files:
      - AGENTS.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/EXECUTION_CONTINUATION_POLICY.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/QUALITY_FIRST_WORKFLOW.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/engine-journal/input/TASK-0167-METH-ENGINE-TERMINAL-EXECUTION-01.md
      - docs/agent-system/engine-journal/rationale/RATIONALE-0167-METH-ENGINE-TERMINAL-EXECUTION-01.md
      - docs/agent-system/engine-journal/output/RESULT-0167-METH-ENGINE-TERMINAL-EXECUTION-01.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
  policies:
    journal: required
    rationale: required
    cloud_regen: if_bundle_source_changed
    generated_checks: required
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only
    language: russian_first
  checks:
    required:
      - python -m unittest discover -s docs/agent-system/tools/tests -p test_*.py -v
      - python docs/agent-system/tools/validate_task_contract.py <task-file>
      - python docs/agent-system/tools/validate_journal_triplet.py --base origin/developer --json
      - python docs/agent-system/tools/validate_policy_invariants.py --json
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
  stop_conditions:
    - new_architectural_or_governance_decision_required
    - path_outside_adaptive_scope
    - destructive_git_or_data_action_required
    - protected_branch_or_private_data_risk
    - external_dependency_unavailable_after_retries
```

Номер sequence: 0167
Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-27T10:53:20.5182472+02:00

## Цель

Закрепить terminal execution: file-changing Engine-задача самостоятельно
завершается готовым к human review PR с evidence либо безопасным
`stopped_human_required`.

## Definition of Ready

- Ветка создана от чистого актуального `origin/developer`.
- Scope, checks и STOP-границы заданы; RATIONALE добавлен как обязательный triplet.
- Каноны continuation, journal, readiness, quality и task contract доступны локально.

## Acceptance criteria

- `EXECUTION_CONTINUATION_POLICY.md` является единственным authoritative document
  для terminal execution, adaptive scope и настоящего STOP.
- Связанные каноны и шаблоны ссылаются на policy без дублирования алгоритма.
- `DECISION_LOG.md`, CURRENT_STATE и NEXT_STEPS отражают только факты этой задачи.
- TASK/RATIONALE/RESULT/INDEX согласованы, generated artifacts регенерированы,
  readiness возвращает `ready` и `blockers_count: 0`.

## Ограничения

Merge, direct change `main`/`developer`, ослабление checks, destructive Git-операции,
секреты и private data запрещены.
