# TASK для METH-MANAGEMENT-LAYER-H7-01

Задача для methodology-architect-01: METH-MANAGEMENT-LAYER-H7-01

```yaml
task_contract:
  version: 1
  task_id: METH-MANAGEMENT-LAYER-H7-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-10-management-layer

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 3e6ad6d15aef41db6cec8ff6235a8eb031767d6a
    reference_type: methodology_development
    checked_at: 2026-07-02T21:14:58.3233076+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-10-management-layer
    base_commit: 3e6ad6d15aef41db6cec8ff6235a8eb031767d6a
    checked_at: 2026-07-02T21:14:58.3233076+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/ARCHITECT_COCKPIT.md
      - docs/agent-system/ARCHITECT_HANDOFF_PACK.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/NON_TECHNICAL_ARCHITECT_GUIDE.md
      - docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/ROLE_MODEL.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
      - docs/agent-system/WORKFLOW.md
      - docs/agent-system/cloud/**
      - docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md
      - docs/agent-system/templates/PROJECT_OPERATOR_DASHBOARD_TEMPLATE.md
      - docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0147-METH-MANAGEMENT-LAYER-H7-01.md
      - docs/agent-system/engine-journal/output/RESULT-0147-METH-MANAGEMENT-LAYER-H7-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0147-METH-MANAGEMENT-LAYER-H7-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0147-METH-MANAGEMENT-LAYER-H7-01.md
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
    - destructive_git_needed
    - branch_protection_change_needed
    - direct_main_push_or_tag_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-10/H7 меняет reusable docs/templates управления методологией и
target governance, но не требует runtime, CI/CD, branch protection, секретов или
product changes.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T21:14:58.3233076+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-10-management-layer`.
- Base commit: `3e6ad6d15aef41db6cec8ff6235a8eb031767d6a`.
- PR #315 state before start: merged at `2026-07-02T14:02:49Z`.
- Working tree before branch creation: clean.

## PR/H mapping guard

- Выполняемый блок: `PR-10 = H7`.
- `H7` является P2 item Management layer.
- Source-consumer registry остается `PR-11/H8+H10`, не входит в этот scope.

## Цель

Выполнить PR-10/H7 из hardening-блока v1.5.2: добавить управленческий слой для
не-программиста-архитектора, consolidated handoff pack, cockpit и короткий
operator dashboard template.

## Требуемые изменения

- Добавить `NON_TECHNICAL_ARCHITECT_GUIDE.md`.
- Добавить `ARCHITECT_HANDOFF_PACK.md` как единый dossier/protocol/checklist.
- Добавить `ARCHITECT_COCKPIT.md`.
- Добавить `templates/PROJECT_OPERATOR_DASHBOARD_TEMPLATE.md`.
- Обновить `ROLE_MODEL.md` и `PROJECT_CONSTITUTION_FRAMEWORK.md`: architect может
  не быть программистом; его зона — **что**, не **как**.
- Добавить в root README блок «Если вы не программист — начните здесь».
- Связать H7 с `WORKFLOW.md`, `TARGET_PROJECT_GOVERNANCE_PACK.md`,
  `METHODOLOGY_MAP.md`, visual map, manifest, generated file map и cloud mirrors.

## Acceptance criteria

- Non-technical architect guide содержит glossary, пошаговый путь и human vs auto.
- Handoff pack объединяет dossier, protocol и checklist в одном canonical home.
- Architect cockpit дает ежедневные/еженедельные вопросы, красные флаги и safe
  prompts к engine.
- Operator dashboard template является коротким yes/no dashboard с STOP при
  `нет` или `unknown`.
- Role/constitution docs явно говорят: architect может не быть программистом и
  отвечает за mission/scope/priority/acceptance, не за implementation tactics.
- README содержит блок для не-программиста.
- Manifest, file map и cloud bundle синхронизированы.
- RESULT/INDEX финализируются после PR creation.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch,
финальный head SHA, changed files summary, checks, generated artifacts,
accounting fields, risks, Source Delta, PR/H mapping note и блок «Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-10/H7; затем архитектор —
human merge; затем methodology-architect-01 — PR-11/H8+H10 Private control plane
and MIR ledger по таблице PR/H hardening plan.
