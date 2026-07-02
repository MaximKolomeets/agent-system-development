# TASK для METH-TIME-COST-ACCOUNTING-HARD-GATE-01

```yaml
task_contract:
  version: 1
  task_id: METH-TIME-COST-ACCOUNTING-HARD-GATE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-3-time-cost-accounting

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    ref: origin/developer
    stable_only: false
    source_commit: 9fc59150f508f4846fef2b34d9738f49b81e7fb2
    checked_at: 2026-07-02T16:32:32.7623677+07:00

  scope:
    allowed_files:
      - AGENTS.md
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/CODE_REVIEW_WORKFLOW.md
      - docs/agent-system/COST_TRACKING_POLICY.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/METRICS.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/TIME_ACCOUNTING_POLICY.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0140-METH-TIME-COST-ACCOUNTING-HARD-GATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0140-METH-TIME-COST-ACCOUNTING-HARD-GATE-01.md
      - docs/agent-system/engine-journal/templates/ENGINE_RESULT_FILE_TEMPLATE.md
      - docs/agent-system/engine-journal/templates/ENGINE_TASK_FILE_TEMPLATE.md
      - docs/agent-system/templates/AGENT_REPORT_TEMPLATE.md
      - docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/TIME_LEDGER_TEMPLATE.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/gen_cloud_bundle.py
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0140-METH-TIME-COST-ACCOUNTING-HARD-GATE-01.md
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python -m py_compile docs/agent-system/tools/check_task_ready.py
      - git diff --check origin/developer...HEAD

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: H3 меняет policy, шаблоны, manifest, generated artifacts и
`check_task_ready.py`, поэтому нужен полный локальный цикл с journal и PR.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T16:32:32.7623677+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Цель

Выполнить PR-3/H3 из пакета `BLOCK_METH_v1_5_2.md`: ввести hard-gate учёта
времени и стоимости для новых finalized RESULT, сохранить legacy как advisory,
добавить policy/template/metrics слой, колонку `Time` в INDEX и calculator в
`check_task_ready.py`.

## Контекст

- PR #307 / H2 смержен в `developer`.
- Baseline `developer`: `9fc59150f508f4846fef2b34d9738f49b81e7fb2`.
- Last journal row before this task: `0139`.
- Actual journal seq for this task: `0140`.
- H3 является P1 docs+tool task и выполняется ролью `methodology-architect-01`.

## Acceptance criteria

- Добавлены `TIME_ACCOUNTING_POLICY.md`, `COST_TRACKING_POLICY.md`,
  `templates/TIME_LEDGER_TEMPLATE.md` и `METRICS.md`.
- TASK/RESULT templates и common header содержат time/cost accounting fields.
- `human_time_reported` обязателен для `actor_type: human|hybrid`.
- Новые finalized RESULT без required accounting fields блокируются
  `check_task_ready.py`; legacy RESULT остаются advisory.
- `check_task_ready.py` выполняет token/cost rollup и проверяет total cost math,
  если cost fields числовые.
- `engine-journal/INDEX.md` содержит колонку `Time`; legacy rows отмечены
  `legacy/advisory`, row 0140 содержит фактическое `time_spent`.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` и `cloud/**`
  согласованы с новыми source/template/generated files.
- Финальный RESULT 0140 и INDEX финализированы после создания PR.

## Проверки

- `python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0140-METH-TIME-COST-ACCOUNTING-HARD-GATE-01.md`
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`
- `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`
- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `python -m py_compile docs/agent-system/tools/check_task_ready.py`
- `git diff --check origin/developer...HEAD`

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-3/H3; затем архитектор —
human merge; затем methodology-architect-01 — PR-4/H4 stable-reference schema.
