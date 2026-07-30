Задача для release-manager: METH-POST-RELEASE-STATE-REFRESH-V1-5-5-01

Рекомендуемый режим исполнения:

Роль: release-manager
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: задача обновляет post-release source of truth и требует проверки
remote refs, annotated tag, GitHub merge metadata и generated parity.
Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-30T11:06:40.9562714+02:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]:
actor_type: agent
time_source: measured
time_report_confidence: high

# TASK-0170-METH-POST-RELEASE-STATE-REFRESH-V1-5-5-01

```yaml
task_contract:
  version: 2
  task_id: METH-POST-RELEASE-STATE-REFRESH-V1-5-5-01
  role: release-manager-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/release-manager-01/meth-post-release-state-refresh-v1-5-5-01
  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: f80e148f9e4ba965e701d1e06faa79d517b646cf
    source_tag: v1.5.5
    reference_type: methodology_development
    checked_at: 2026-07-30T11:09:34.6857072+02:00
  methodology_development_base:
    base_branch: developer
    working_branch: work/release-manager-01/meth-post-release-state-refresh-v1-5-5-01
    base_commit: e41b9bec27995f88ad227ba88c57dc1720e9589d
    checked_at: 2026-07-30T11:09:34.6857072+02:00
  scope:
    allowed_files:
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/engine-journal/input/TASK-0170-METH-POST-RELEASE-STATE-REFRESH-V1-5-5-01.md
      - docs/agent-system/engine-journal/rationale/RATIONALE-0170-METH-POST-RELEASE-STATE-REFRESH-V1-5-5-01.md
      - docs/agent-system/engine-journal/output/RESULT-0170-METH-POST-RELEASE-STATE-REFRESH-V1-5-5-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py <task-file> --json
      - python docs/agent-system/tools/validate_journal_triplet.py --json
      - python docs/agent-system/tools/validate_policy_invariants.py --json
      - python docs/agent-system/tools/check_journal_append_only.py --base origin/developer --json
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - git diff --check origin/developer...HEAD
  stop_conditions:
    - dirty_tree_before_start
    - release_or_tag_fact_not_verified
    - main_developer_file_delta_present
    - changed_file_outside_allowlist
    - full_readiness_not_ready
    - declared_iteration_budget_exhausted
    - destructive_git_protected_branch_secret_or_real_data_risk
```

Номер sequence: 0170
Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-30T11:06:40.9562714+02:00
actor_type: agent
role: release-manager-01
time_source: measured_engine_clock
time_report_confidence: high
raw_chain_of_thought_stored: no

## Цель

Обновить post-release source of truth до stable release `v1.5.5`, подтвердив
annotated tag и цепочку PR #351 → #352 → #353 без изменения release/tag/branch
state.

## Definition of Ready

- Repository root, origin, ветка и clean tree проверены.
- `origin/main`, tag object и peeled commit `v1.5.5` подтверждены.
- PR #351, #352 и #353 подтверждены через GitHub metadata.
- `origin/main...origin/developer` не имеет file delta после sync.

## Acceptance criteria

- `CURRENT_STATE.md` и `NEXT_STEPS.md` указывают на `v1.5.5`; `v1.5.4`
  сохранён как предыдущий historical release.
- Hardening-серия v1.5.2 в `BACKLOG.md` отмечена завершённой с evidence и без
  удаления исторического перечня.
- Следующим действием указан owner-selection отдельной backlog-задачи.
- Journal triplet 0170 и INDEX согласованы; generated mirrors получены только
  штатными инструментами.
- Единственный full readiness возвращает `ready`, `blockers_count: 0`.

## Dependency closure

Source state → journal triplet/INDEX → file map при доказанной необходимости →
cloud mirrors → targeted checks → один full readiness → commit → push → PR → CI.

Iteration budgets:

- targeted check reruns: до 2;
- full readiness runs: 1;
- CI fix-pass: 0;
- integration-stack attempts: 0.

## Ограничения

Не менять policy, templates, validators, CI, Docker/runtime, release/version,
protected branches или product scope. Не создавать tag/release, не выполнять
merge, rebase, reset, stash, clean, force-push и не читать `.env`.

## Ожидаемый terminal report

Отчёт на русском языке фиксирует branch, HEAD, commit, PR, sequence, Source
Delta, generated artifacts, release evidence, checks/CI, budgets, unresolved
threads, residual risks, отсутствие merge и передачу human reviewer.
