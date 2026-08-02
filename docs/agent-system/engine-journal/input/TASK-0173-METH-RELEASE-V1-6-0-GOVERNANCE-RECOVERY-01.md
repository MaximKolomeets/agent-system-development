# TASK-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01

Идентификатор задачи: METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01
Номер sequence: 0173
Создано: 2026-08-02T18:54:22+02:00
execution_started_at: 2026-08-02T18:54:22+02:00
actor_type: agent
role: release-manager
time_source: measured
time_report_confidence: high

```yaml
task_contract:
  version: 2
  task_id: METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01
  role: release-manager
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/release-manager-01/meth-release-v1-6-0-governance-recovery-01
  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 59e645944697eac565d121e97d2dfa2ff3e9d99b
    source_tag: v1.5.5
    reference_type: methodology_development
    checked_at: 2026-08-02T18:54:22+02:00
  methodology_development_base:
    base_branch: developer
    working_branch: work/release-manager-01/meth-release-v1-6-0-governance-recovery-01
    base_commit: dab6e6de54373266f60ce0047239827b40e6ed24
    checked_at: 2026-08-02T18:54:22+02:00
  scope:
    allowed_files:
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json
      - docs/agent-system/engine-journal/output/RESULT-0172-METH-BOUNDARY-RECONCILIATION-0163-0171-V1-6-0-01.md
      - docs/agent-system/engine-journal/input/TASK-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01.md
      - docs/agent-system/engine-journal/rationale/RATIONALE-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01.md
      - docs/agent-system/engine-journal/output/RESULT-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0173-METH-RELEASE-V1-6-0-GOVERNANCE-RECOVERY-01.md --json
      - python docs/agent-system/tools/validate_journal_triplet.py --json
      - python docs/agent-system/tools/validate_journal_sequence_reservations.py --json
      - python docs/agent-system/tools/check_journal_append_only.py --base origin/developer --json
      - python docs/agent-system/tools/validate_policy_invariants.py --json
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/generated_eol_guard.py
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - provider_snapshot_unavailable
    - secret_or_env_risk
    - full_readiness_not_ready
```

## Цель

Восстановить release-gates и live state после преждевременного
`developer -> main -> developer`, не выполняя rollback, tag, release PR,
sync, human UAT или reviewer consistency-gate.

## Definition of Ready и критерии приёмки

- PR #355, #356, #359, #360 и #361 подтверждены GitHub metadata как merged.
- Reservation 0173 выделена machine allocator и merged PR #362.
- RESULT/INDEX/ledger 0172 отражают merge PR #359 append-only.
- Live state фиксирует untagged candidate, historical release/sync facts и
  непройденные human gates без объявления `v1.6.0` опубликованным.
- RESULT-0173 содержит Human UAT Checklist без agent verdict.
- Все mandatory checks и один full readiness возвращают успешный результат.

## Ограничения

Не менять policy, validators, schemas, templates, tests, workflows, source code,
`main` или `developer` напрямую. Не выполнять merge, human UAT, reviewer gate,
release PR, tag, GitHub Release, sync, rollback, amend, rebase или force-push.
Credential применяется только через environment и не выводится.

## Iteration budgets

- targeted check reruns: до 3;
- full readiness runs: до 1;
- CI fix-pass: до 1;
- generator write-runs: до 2.

## Передача

Следующий: reviewer — проверить recovery evidence, Human UAT Checklist и
сохранение human-only release authority перед human merge recovery PR.
