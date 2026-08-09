# TASK-0177-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01

Задача для dev-implementer: METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01

Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Hybrid
Режим: Agent
Почему: требуются два fail-closed изменения валидаторов и полный release-boundary regression cycle.
execution_started_at: 2026-08-09T09:59:00.8675445+02:00
orchestration_time_reported: not_available
actor_type: agent
role: dev-implementer
time_source: measured
time_report_confidence: high

```yaml
task_contract:
  version: 2
  task_id: METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01
  role: dev-implementer
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-release-v1-6-0-governance-recovery-gates-01
  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 59e645944697eac565d121e97d2dfa2ff3e9d99b
    source_tag: v1.5.5
    reference_type: methodology_development
    checked_at: 2026-08-09T09:59:00.8675445+02:00
  methodology_development_base:
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-release-v1-6-0-governance-recovery-gates-01
    base_commit: 943695d6b225a4c6cdeeec30ccc6941f1519db54
    checked_at: 2026-08-09T09:59:00.8675445+02:00
  scope:
    allowed_files:
      - docs/agent-system/tools/release_gate.py
      - docs/agent-system/tools/tests/test_release_gate.py
      - docs/agent-system/tools/validate_journal_triplet.py
      - docs/agent-system/tools/tests/test_validate_journal_triplet.py
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0177-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01.md
      - docs/agent-system/engine-journal/rationale/RATIONALE-0177-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01.md
      - docs/agent-system/engine-journal/output/RESULT-0177-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01.md
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
    cloud_regen: required
    generated_checks: required
    review: scoped_semantic
    merge: human_only
    language: russian_first
  checks:
    required:
      - python -m unittest discover -s docs/agent-system/tools/tests -p test_*.py -v
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0177-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-GATES-01.md
      - python docs/agent-system/tools/validate_journal_triplet.py --base origin/developer --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/release_gate.py --version v1.6.0 --governance-recovery --json
  stop_conditions:
    - provider_snapshot_unavailable
    - sequence_0177_ownership_conflict
    - changed_file_outside_allowlist
    - secret_or_env_risk
    - full_readiness_not_ready
```

## Цель

Исправить governance-recovery release gate и range-aware materialization нескольких последовательных journal triplets без ослабления стандартного release path.

## Acceptance criteria

- Стандартный режим по-прежнему требует `main == last release tag`.
- Recovery включается только явным opt-in и доказывает ancestry, UAT, reviewer closure и terminal reservations.
- Несколько последовательных triplets принимаются, а gap, collision, reuse и malformed lifecycle блокируются.
- Issue: https://github.com/MaximKolomeets/agent-system-development/issues/376

## Передача

Следующий: dev-implementer — завершить реализацию, regression tests, readiness и один implementation PR в `developer`.
