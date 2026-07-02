# TASK для METH-LIFECYCLE-CROSS-PROJECT-H16-01

Задача для methodology-architect-01: METH-LIFECYCLE-CROSS-PROJECT-H16-01

```yaml
task_contract:
  version: 1
  task_id: METH-LIFECYCLE-CROSS-PROJECT-H16-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-15-lifecycle-cross-project

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: da6e6a27a7b8c2129fca8304e133ac2bfe958d4c
    reference_type: methodology_development
    checked_at: 2026-07-03T00:00:22.3015575+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-15-lifecycle-cross-project
    base_commit: da6e6a27a7b8c2129fca8304e133ac2bfe958d4c
    checked_at: 2026-07-03T00:00:22.3015575+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_GUIDE.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/AGENT_ONBOARDING_CHECKLIST.md
      - docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md
      - docs/agent-system/CROSS_PROJECT_DEPENDENCY_POLICY.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/PROJECT_CLOSURE_GUIDE.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0152-METH-LIFECYCLE-CROSS-PROJECT-H16-01.md
      - docs/agent-system/engine-journal/output/RESULT-0152-METH-LIFECYCLE-CROSS-PROJECT-H16-01.md
    forbidden_files:
      - .env
      - .env.*
      - .venv/**
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - credentials
      - tokens
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data

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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0152-METH-LIFECYCLE-CROSS-PROJECT-H16-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0152-METH-LIFECYCLE-CROSS-PROJECT-H16-01.md
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - private_project_name_or_url_needed
    - actual_private_dependency_record_needed
    - destructive_git_needed
    - direct_main_or_developer_change_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-15/H16 меняет public methodology source docs, navigation, manifest и
generated artifacts, но не требует target repositories, private control plane,
CI/CD, branch protection, release tag или direct main/developer updates.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-03T00:00:22.3015575+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-15-lifecycle-cross-project`.
- Base commit: `da6e6a27a7b8c2129fca8304e133ac2bfe958d4c`.
- PR #320 state before start: merged at `2026-07-02T16:58:19Z`; merge commit `da6e6a27a7b8c2129fca8304e133ac2bfe958d4c`.
- Local `developer` matched `origin/developer` before branch creation.

## Scope

Выполнить PR-15/H16 из patch plan:

1. Добавить `docs/agent-system/AGENT_ONBOARDING_CHECKLIST.md`.
2. Добавить `docs/agent-system/PROJECT_CLOSURE_GUIDE.md`.
3. Добавить раздел `Fork vs Template vs Adoption` в `ADOPTION_GUIDE.md`.
4. Добавить `docs/agent-system/CROSS_PROJECT_DEPENDENCY_POLICY.md`.
5. Обновить navigation/discovery: root README, docs README,
   `METHODOLOGY_MAP.md`, `METHODOLOGY_MAP.mermaid`,
   `ADOPTION_TRANSFER_MANIFEST.yml`, generated `PROJECT_FILE_MAP.md` и
   `cloud/**`.
6. Не добавлять реальные consumer/project names, private URLs, dependency matrix
   или private control-plane records.

## Acceptance criteria

- `AGENT_ONBOARDING_CHECKLIST.md` описывает onboarding новой роли/исполнителя,
  repository boundary, local instructions, privacy, journal и STOP-условия.
- `PROJECT_CLOSURE_GUIDE.md` описывает pause/completed/maintenance/transferred/
  cancelled/archived modes, closure workflow, journal/evidence, governance docs,
  dependency/consumer checks и non-technical checklist.
- `ADOPTION_GUIDE.md` явно различает Fork, Template/bootstrap и Adoption.
- `CROSS_PROJECT_DEPENDENCY_POLICY.md` задает generic dependency types,
  private dependency record schema, stable reference, breaking-change и STOP
  rules без private data.
- Manifest и maps ссылаются на новые docs; generated artifacts актуальны.
- TASK/RESULT/INDEX Russian-first и содержат time/cost accounting fields.

## Source Delta

- Methodology source inventory меняется: добавляются
  `AGENT_ONBOARDING_CHECKLIST.md`, `PROJECT_CLOSURE_GUIDE.md` и
  `CROSS_PROJECT_DEPENDENCY_POLICY.md`.
- Adoption route меняется: `ADOPTION_GUIDE.md` получает явную развилку
  `Fork vs Template vs Adoption`.
- Cross-project governance меняется: dependency records закрепляются как
  private control-plane surface, не public methodology data.
- Source-reminder: после release/publication обновить Source-снапшот у
  зарегистрированных потребителей. До release downstream stable source не
  меняется.

## Требования к final report

Финальный отчет должен быть на русском языке и содержать:

- PR URL, branch и final head SHA;
- список измененных lifecycle/adoption/cross-project/navigation/generated/journal
  artifacts;
- результаты required checks;
- статус GitHub checks, если PR создан;
- блок `Локальные действия после PR/merge`;
- блок `Methodology feedback`;
- блок `Unprompted Project Proposals`;
- блок `Передача`;
- Source-reminder.

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-15/H16 после открытия PR.
