# TASK для METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01

Задача для methodology-architect-01: METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01

```yaml
task_contract:
  version: 1
  task_id: METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-11-private-control-mir-ledger

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: d66754023456816fe010e122de7fddb836475258
    reference_type: methodology_development
    checked_at: 2026-07-02T21:36:32.4150396+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-11-private-control-mir-ledger
    base_commit: d66754023456816fe010e122de7fddb836475258
    checked_at: 2026-07-02T21:36:32.4150396+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md
      - docs/agent-system/METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE.md
      - docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md
      - docs/agent-system/METHODOLOGY_IMPROVEMENT_LEDGER.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/PUBLICATION_POLICY.md
      - docs/agent-system/README.md
      - docs/agent-system/SOURCE_CONSUMERS.md
      - docs/agent-system/SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0148-METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01.md
      - docs/agent-system/engine-journal/output/RESULT-0148-METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0148-METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0148-METH-PRIVATE-CONTROL-MIR-LEDGER-H8-H10-01.md
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
    - private_consumer_identity_needed
    - target_repository_access_needed
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
Почему: PR-11/H8+H10 меняет public-safe docs/templates methodology repository,
но не требует читать target repositories, реальные private consumers, runtime,
CI/CD, branch protection или secrets.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T21:36:32.4150396+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-11-private-control-mir-ledger`.
- Base commit: `d66754023456816fe010e122de7fddb836475258`.
- PR #316 state before start: merged at `2026-07-02T14:25:03Z`.
- Local `developer` matched `origin/developer` before branch creation.
- Working tree before branch creation: clean.

## PR/H mapping guard

- Выполняемый блок: `PR-11 = H8+H10`.
- H8: private control plane propagation.
- H10: MIR lifecycle ledger.
- H11 policy invariants не входит в этот scope и остается PR-12.

## Цель

Выполнить PR-11/H8+H10 из hardening-блока v1.5.2: добавить generic private
control-plane templates для source consumers/adoption matrix и public-safe
MIR lifecycle ledger для цепочки `feedback -> MIR -> PR -> release -> adoption`.

## Требуемые изменения

- Добавить `SOURCE_CONSUMER_REGISTRY_PRIVATE_TEMPLATE.md`.
- Добавить `METHODOLOGY_ADOPTION_MATRIX_PRIVATE_TEMPLATE.md`.
- Добавить `METHODOLOGY_IMPROVEMENT_LEDGER.md`.
- Обновить `PUBLICATION_POLICY.md`: реальные consumers/adoption rollout state не
  коммитятся в public methodology repository.
- Связать ledger/templates с `SOURCE_CONSUMERS.md`,
  `METHODOLOGY_FEEDBACK_LOOP.md`, `DOWNSTREAM_FEEDBACK_LOOP.md`,
  `METHODOLOGY_MAP.md`, README, manifest, generated file map и cloud mirrors.

## Acceptance criteria

- Private registry template содержит поля `repository_alias`, visibility,
  methodology release/source commit, last update PR, owner role, update status и
  blocked reason.
- Adoption matrix template содержит current tag/source commit, last source sync,
  local divergences, update PR reference, blockers и next action.
- Real consumers, private repositories, private PRs, internal aliases и rollout
  state не попадают в public repo.
- MIR ledger задает statuses и таблицу lifecycle feedback/MIR/PR/release/adoption.
- Publication policy содержит privacy boundary для private control plane.
- Feedback loop docs ссылаются на MIR ledger и private templates.
- Manifest, file map и cloud bundle синхронизированы.
- RESULT/INDEX закрываются фактическими PR metadata в текущей рабочей ветке.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: проверку PR-10/H7,
PR URL, branch, финальный head SHA, changed files summary, checks, generated
artifacts, accounting fields, risks, Source Delta, PR/H mapping note и блок
«Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-11/H8+H10; затем
архитектор — human merge; затем methodology-architect-01 — PR-12/H11
Policy-invariants + self-test gate по таблице PR/H hardening plan.
