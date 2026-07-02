# TASK для METH-BUSINESS-ACCEPTANCE-UAT-H13-01

Задача для methodology-architect-01: METH-BUSINESS-ACCEPTANCE-UAT-H13-01

```yaml
task_contract:
  version: 1
  task_id: METH-BUSINESS-ACCEPTANCE-UAT-H13-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-7-business-acceptance-uat

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 69696842ed93f9a85757b8887012b2c2f2ff5114
    reference_type: methodology_development
    checked_at: 2026-07-02T18:45:48.9241882+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-7-business-acceptance-uat
    base_commit: 69696842ed93f9a85757b8887012b2c2f2ff5114
    checked_at: 2026-07-02T18:45:48.9241882+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/BRANCH_POLICY.md
      - docs/agent-system/BUSINESS_ACCEPTANCE_CHECKLIST.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/RELEASE_AUTHORITY_POLICY.md
      - docs/agent-system/UAT_WORKFLOW.md
      - docs/agent-system/WORKFLOW.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0144-METH-BUSINESS-ACCEPTANCE-UAT-H13-01.md
      - docs/agent-system/engine-journal/output/RESULT-0144-METH-BUSINESS-ACCEPTANCE-UAT-H13-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0144-METH-BUSINESS-ACCEPTANCE-UAT-H13-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0144-METH-BUSINESS-ACCEPTANCE-UAT-H13-01.md
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
Почему: PR-7/H13 меняет release/business acceptance canon и добавляет новые
reusable docs, но не требует runtime, CI или branch-protection changes.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T18:45:48.9241882+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-7-business-acceptance-uat`.
- Base commit: `69696842ed93f9a85757b8887012b2c2f2ff5114`.
- PR #312 state before start: merged at `2026-07-02T11:40:37Z`.
- Working tree before branch creation: clean.

## PR/H mapping guard

- Выполняемый блок: `PR-7 = H13`.
- `H6` не является PR-7; `H6` запланирован как `PR-9` в P2.
- Следующий P1 hardening PR по таблице: `PR-8/H14`.

## Цель

Выполнить PR-7/H13 из hardening-блока v1.5.2: добавить Business Acceptance Gate
и Human UAT Checklist перед approval release PR в `main`.

## Требуемые изменения

- Добавить `UAT_WORKFLOW.md` и `BUSINESS_ACCEPTANCE_CHECKLIST.md`.
- Добавить Business Acceptance Gate в `WORKFLOW.md` между стабилизацией
  `developer` и release PR в `main`.
- Добавить требование Human UAT Checklist в
  `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`.
- Добавить UAT-gate в `BRANCH_POLICY.md` перед `main`.
- Зарегистрировать новые docs в manifest, methodology map, README и generated
  artifacts.

## Acceptance criteria

- `UAT_WORKFLOW.md` описывает button-click, visual UI и API/CLI acceptance.
- `BUSINESS_ACCEPTANCE_CHECKLIST.md` содержит reusable Human UAT Checklist.
- `WORKFLOW.md` содержит Business Acceptance Gate до release PR в `main`.
- `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md` требует UAT checklist из
  acceptance scenarios.
- `BRANCH_POLICY.md` блокирует release PR без UAT verdict или `not_applicable`
  reason.
- Manifest, file map и cloud bundle синхронизированы.
- RESULT/INDEX финализируются после PR creation.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch,
финальный head SHA, changed files summary, checks, generated artifacts,
accounting fields, risks, Source Delta, PR/H mapping note и блок «Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-7/H13; затем архитектор —
human merge; затем methodology-architect-01 — PR-8/H14 Hotfix, rollback &
disaster recovery.
