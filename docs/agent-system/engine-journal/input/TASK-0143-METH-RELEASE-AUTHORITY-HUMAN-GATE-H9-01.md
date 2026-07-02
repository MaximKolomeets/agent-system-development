# TASK для METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01

Задача для methodology-architect-01: METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-6-release-authority-human-gate

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: aaac1a762a35a00427cbec71be6460c746d3fcda
    reference_type: methodology_development
    checked_at: 2026-07-02T18:26:28.4297811+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-6-release-authority-human-gate
    base_commit: aaac1a762a35a00427cbec71be6460c746d3fcda
    checked_at: 2026-07-02T18:26:28.4297811+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/BRANCH_POLICY.md
      - docs/agent-system/HUMAN_GATE_POLICY.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/RELEASE_AUTHORITY_POLICY.md
      - docs/agent-system/RELEASE_READINESS.md
      - docs/agent-system/WORKFLOW.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0143-METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01.md
      - docs/agent-system/engine-journal/output/RESULT-0143-METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0143-METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0143-METH-RELEASE-AUTHORITY-HUMAN-GATE-H9-01.md
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
    - human_gate_required_for_final_action
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-6/H9 меняет authority canon для release/main/tag/sync и вводит
human-only gate, но не требует runtime, CI или branch-protection изменений.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T18:26:28.4297811+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-6-release-authority-human-gate`.
- Base commit: `aaac1a762a35a00427cbec71be6460c746d3fcda`.
- PR #311 state before start: merged at `2026-07-02T11:19:34Z`.
- Working tree before branch creation: clean.

## PR/H mapping guard

- Следующий блок по плану: `PR-6 = H9`.
- `H6` не является PR-6; `H6` запланирован как `PR-9` в P2.
- Перед передачей следующей задачи снова сверить таблицу PR/H в
  `METHODOLOGY_HARDENING_PLAN.md` и `BLOCK_METH_v1_5_2.md`.

## Цель

Выполнить PR-6/H9 из hardening-блока v1.5.2: добавить единый release authority
canon и явный human gate для действий, которые агент не выполняет сам.

## Требуемые изменения

- Добавить `docs/agent-system/RELEASE_AUTHORITY_POLICY.md`: кто может
  merge/tag/publish/sync, что может готовить агент, что выполняет человек, и
  какие actor/evidence fields фиксирует release-sensitive `RESULT`.
- Добавить `docs/agent-system/HUMAN_GATE_POLICY.md`: явный список human-only
  действий: merge в `main`, branch protection/rulesets, CI/CD, prod-secrets,
  mission/strategy, удаление данных, финансы и rollback.
- Привести `RELEASE_READINESS.md`, `NEXT_STEPS.md`, `BRANCH_POLICY.md`,
  `WORKFLOW.md` и `PROJECT_CONSTITUTION_FRAMEWORK.md` к единой формулировке:
  агент готовит checks/evidence, человек выполняет human-only final action.
- Зарегистрировать новые policies в `ADOPTION_TRANSFER_MANIFEST.yml`,
  `METHODOLOGY_MAP.md`, root `README.md` и `METHODOLOGY_MAP.mermaid`.
- Регенерировать `PROJECT_FILE_MAP.md` и `docs/agent-system/cloud/**`.

## Acceptance criteria

- `RELEASE_AUTHORITY_POLICY.md` существует и описывает merge/tag/publish/sync
  authority plus RESULT actor/evidence.
- `HUMAN_GATE_POLICY.md` существует и содержит явный human-only список из H9.
- `BRANCH_POLICY.md`, `WORKFLOW.md`, `RELEASE_READINESS.md`, `NEXT_STEPS.md` и
  `PROJECT_CONSTITUTION_FRAMEWORK.md` ссылаются на новые policies без
  противоречий.
- Manifest, methodology map, file map и cloud bundle синхронизированы.
- `orchestrator_checklist.py` проходит на этом TASK.
- RESULT/INDEX финализируются после PR creation.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch,
финальный head SHA, changed files summary, checks, generated artifacts,
accounting fields, risks, Source Delta, PR/H mapping note и блок «Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-6/H9; затем архитектор —
human merge; затем methodology-architect-01 — следующий hardening PR по таблице
PR/H (`PR-7/H13`, не `H6`).
