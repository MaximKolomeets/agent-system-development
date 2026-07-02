# TASK для METH-HOTFIX-ROLLBACK-DR-H14-01

Задача для methodology-architect-01: METH-HOTFIX-ROLLBACK-DR-H14-01

```yaml
task_contract:
  version: 1
  task_id: METH-HOTFIX-ROLLBACK-DR-H14-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-8-hotfix-rollback-dr

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: a669e3d7f7e63b30b56ed0f80e1fe0ea908122b0
    reference_type: methodology_development
    checked_at: 2026-07-02T20:15:13.2332809+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-8-hotfix-rollback-dr
    base_commit: a669e3d7f7e63b30b56ed0f80e1fe0ea908122b0
    checked_at: 2026-07-02T20:15:13.2332809+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/BRANCH_POLICY.md
      - docs/agent-system/DISASTER_RECOVERY.md
      - docs/agent-system/HOTFIX_AND_ROLLBACK_POLICY.md
      - docs/agent-system/HUMAN_GATE_POLICY.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/RELEASE_AUTHORITY_POLICY.md
      - docs/agent-system/WORKFLOW.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0145-METH-HOTFIX-ROLLBACK-DR-H14-01.md
      - docs/agent-system/engine-journal/output/RESULT-0145-METH-HOTFIX-ROLLBACK-DR-H14-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0145-METH-HOTFIX-ROLLBACK-DR-H14-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0145-METH-HOTFIX-ROLLBACK-DR-H14-01.md
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
    - human_gate_required_for_final_rollback_action
    - direct_main_push_or_tag_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-8/H14 меняет release/hotfix/rollback canon и добавляет reusable
source docs, но не требует runtime, CI, branch-protection или real rollback
actions.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T20:15:13.2332809+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-8-hotfix-rollback-dr`.
- Base commit: `a669e3d7f7e63b30b56ed0f80e1fe0ea908122b0`.
- PR #313 state before start: merged at `2026-07-02T12:25:37Z`.
- Working tree before branch creation: clean.

## PR/H mapping guard

- Выполняемый блок: `PR-8 = H14`.
- `H6` не является PR-8; `H6` запланирован как `PR-9` в P2.
- Следующий hardening PR по таблице после H14: `PR-9/H6`.

## Цель

Выполнить PR-8/H14 из hardening-блока v1.5.2: добавить канон hotfix,
rollback и disaster recovery, включая emergency rollback, rollback до tag
`vX.Y.Z`, checklist для не-программиста, branch namespace
`work/hotfix/<issue>`, связь RESULT actor/evidence с H9 и recovery сценарии.

## Требуемые изменения

- Добавить `HOTFIX_AND_ROLLBACK_POLICY.md`.
- Добавить `DISASTER_RECOVERY.md`.
- Добавить rollback/hotfix section в `BRANCH_POLICY.md`, включая
  `work/hotfix/<issue>`.
- Добавить hotfix workflow section в `WORKFLOW.md`.
- Связать H14 с `RELEASE_AUTHORITY_POLICY.md` и `HUMAN_GATE_POLICY.md`.
- Зарегистрировать новые docs в README, METHODOLOGY_MAP, mermaid map, manifest,
  generated file map и cloud mirrors.
- Обновить `NEXT_STEPS.md`: PR-8/H14 как текущий фокус, следующий PR-9/H6.
- Создать и финализировать RESULT/INDEX после PR creation.

## Acceptance criteria

- `HOTFIX_AND_ROLLBACK_POLICY.md` описывает emergency rollback, rollback до tag
  `vX.Y.Z`, non-programmer checklist, `work/hotfix/<issue>`, revert PR,
  expedited review, human merge в `main` и RESULT actor/evidence.
- `DISASTER_RECOVERY.md` описывает broken local repo, GitHub outage, token loss
  и restore from tag без раскрытия credentials.
- `BRANCH_POLICY.md` содержит rollback/hotfix branch policy и запрет agent merge
  или force/tag action.
- `WORKFLOW.md` содержит hotfix workflow.
- H9 docs явно связаны с H14 actor/evidence requirements.
- Manifest, file map и cloud bundle синхронизированы.
- RESULT/INDEX финализируются после PR creation.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch,
финальный head SHA, changed files summary, checks, generated artifacts,
accounting fields, risks, Source Delta, PR/H mapping note и блок «Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-8/H14; затем архитектор —
human merge; затем methodology-architect-01 — PR-9/H6 Safe-scan & Russian-first
lint.
