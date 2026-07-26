# TASK-0164-METH-READY-GATE-PERFORMANCE-01

```yaml
task_contract:
  version: 2
  task_id: METH-READY-GATE-PERFORMANCE-01
  role: dev-implementer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-ready-gate-performance-01
  scope:
    allowed_files:
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/tests/test_check_task_ready.py
      - docs/agent-system/OPERATIONAL_FAST_LANE.md
      - docs/agent-system/engine-journal/**
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
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - readiness_result_not_ready
```

Номер sequence: 0164

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-26T10:35:21+02:00

Цель: сократить повторные Git-сканы и добавить наблюдаемый progress в `check_task_ready.py`, не исключая и не ослабляя ни одну обязательную проверку или её verdict.

Проверки и STOP-условия определены в `task_contract`; aggregate gate запускается только через `neural/python-tools:3.12` с timeout не менее 360 секунд.
