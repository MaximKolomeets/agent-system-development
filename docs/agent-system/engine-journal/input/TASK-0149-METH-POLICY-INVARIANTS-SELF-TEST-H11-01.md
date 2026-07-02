# TASK для METH-POLICY-INVARIANTS-SELF-TEST-H11-01

Задача для methodology-architect-01: METH-POLICY-INVARIANTS-SELF-TEST-H11-01

```yaml
task_contract:
  version: 1
  task_id: METH-POLICY-INVARIANTS-SELF-TEST-H11-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-12-policy-invariants-self-test

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 8cde0491069c41029d50f03c5e5cf50bfbdab72a
    reference_type: methodology_development
    checked_at: 2026-07-02T21:54:35.3626215+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-12-policy-invariants-self-test
    base_commit: 8cde0491069c41029d50f03c5e5cf50bfbdab72a
    checked_at: 2026-07-02T21:54:35.3626215+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/POLICY_INVARIANTS.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/tools/validate_policy_invariants.py
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0149-METH-POLICY-INVARIANTS-SELF-TEST-H11-01.md
      - docs/agent-system/engine-journal/output/RESULT-0149-METH-POLICY-INVARIANTS-SELF-TEST-H11-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0149-METH-POLICY-INVARIANTS-SELF-TEST-H11-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0149-METH-POLICY-INVARIANTS-SELF-TEST-H11-01.md
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - python -m py_compile docs/agent-system/tools/check_task_ready.py docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - semantic_invariant_requires_human_decision
    - target_repository_access_needed
    - private_consumer_identity_needed
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
Почему: PR-12/H11 меняет public methodology docs и read-only tooling, но не требует
доступа к target repositories, private consumers, CI/CD, branch protection или secrets.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T21:54:35.3626215+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-12-policy-invariants-self-test`.
- Base commit: `8cde0491069c41029d50f03c5e5cf50bfbdab72a`.
- PR #317 state before start: merged at `2026-07-02T14:50:49Z`; merge commit `8cde0491069c41029d50f03c5e5cf50bfbdab72a`.
- Local `developer` matched `origin/developer` before branch creation.

## Scope

Выполнить PR-12/H11 из `BLOCK_METH_v1_5_2.md`:

1. Добавить `docs/agent-system/POLICY_INVARIANTS.md` со сквозными invariants:
   release/tag authority, branch model, time accounting, source reference,
   privacy и target adoption.
2. Добавить `docs/agent-system/tools/validate_policy_invariants.py` как read-only
   validator смысловых противоречий между policy-документами.
3. Встроить validator в `check_task_ready.py`.
4. Добавить self-test методологии: existence/link/canonical-path audit, который
   расширяет текущий `validate_id_references.py`, но не ломает target-generated
   placeholders в manifest.
5. Обновить README/METHODOLOGY_MAP/manifest/current state и generated artifacts.

## Constraints

- Не читать `.env`; не менять `.env`, `.venv`, `data/`, `runtime/`, `dist/`,
  `backups/`, `exports/`.
- Не добавлять реальные private consumers, private repository names, client/customer
  data или credentials.
- Не выполнять merge/tag/publish/sync; эти действия остаются human-only.
- Новый validator должен быть read-only и печатать только paths/line/code/category,
  без содержимого потенциальных секретов.
- `target_generated` paths из manifest не считать missing source files; проверять
  их `source_templates`.

## Acceptance criteria

- `POLICY_INVARIANTS.md` существует и описывает все 6 осей H11.
- `validate_policy_invariants.py` проходит на текущем repository и имеет JSON mode.
- `check_task_ready.py --base origin/developer` запускает invariant validator и
  блокирует PR при его failure.
- Manifest/source map/cloud bundle синхронизированы.
- TASK/RESULT/INDEX Russian-first и содержат time/cost accounting fields.

## Требования к final report

Финальный отчет должен быть на русском языке и содержать:

- PR URL, branch и final head SHA;
- список измененных policy/tool/navigation/generated/journal artifacts;
- результаты `validate_policy_invariants.py`, `check_task_ready.py`,
  `russian_first_lint.py`, `gen_file_map.py --check`,
  `gen_cloud_bundle.py --check`, `generated_eol_guard.py --base origin/developer`,
  `git diff --check origin/developer...HEAD` и `py_compile`;
- статус GitHub checks, если PR создан;
- блок `Локальные действия после PR/merge`;
- блок `Передача`;
- Source-reminder: обновить Source-снапшот у зарегистрированных потребителей
  после release/publication новой методологии; до release downstream stable source
  не меняется.

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-12/H11 после открытия PR.
