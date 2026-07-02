# TASK для METH-STABLE-REFERENCE-SCHEMA-SYNC-01

```yaml
task_contract:
  version: 1
  task_id: METH-STABLE-REFERENCE-SCHEMA-SYNC-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-4-stable-reference-schema

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 85f14f204b8dc77f032af096c417f9130476478c
    reference_type: methodology_development
    checked_at: 2026-07-02T17:13:57.3987881+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-4-stable-reference-schema
    base_commit: 85f14f204b8dc77f032af096c417f9130476478c
    checked_at: 2026-07-02T17:13:57.3987881+07:00

  scope:
    allowed_files:
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md
      - docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0141-METH-STABLE-REFERENCE-SCHEMA-SYNC-01.md
      - docs/agent-system/engine-journal/output/RESULT-0141-METH-STABLE-REFERENCE-SCHEMA-SYNC-01.md
      - docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md
      - docs/agent-system/templates/ADOPTION_PROMPT.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/tools/validate_task_contract.py
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0141-METH-STABLE-REFERENCE-SCHEMA-SYNC-01.md
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python -c "import ast, pathlib; ..."
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
Почему: H4 синхронизирует stable-reference schema в канонах, manifest,
adoption templates и validator compatibility.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T17:13:57.3987881+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Цель

Выполнить PR-4/H4 из пакета `BLOCK_METH_v1_5_2.md`: заменить в stable
methodology reference schema поле `source_branch` на `source_ref`, добавить
`reference_type` и отделить `methodology_development_base` для задач, которые
меняют сам methodology repository.

## Acceptance criteria

- `ENGINE_ENTRYPOINT.md` задаёт canonical `methodology_reference.source_ref`.
- `ADOPTION_TRANSFER_MANIFEST.yml` содержит machine-readable `source_ref`,
  `reference_type` и `methodology_development_base_schema`.
- `STABLE_METHODOLOGY_REFERENCE_POLICY.md` запрещает `developer`/`work/*` как
  stable source и описывает отдельный methodology development base.
- `TASK_CONTRACT.md` и `TASK_HEADER_COMMON.md` используют `source_ref` и
  `reference_type`.
- Adoption templates больше не предлагают `source_branch: developer`.
- `validate_task_contract.py` понимает `source_ref`; legacy `ref` остаётся alias
  с warning.
- `PROJECT_FILE_MAP.md` и `cloud/**` синхронизированы.
- RESULT/INDEX 0141 финализированы после PR creation.

## Проверки

- `python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0141-METH-STABLE-REFERENCE-SCHEMA-SYNC-01.md`
- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`
- `python docs/agent-system/tools/generated_eol_guard.py --base origin/developer`
- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `python -c "import ast, pathlib; ..."`
- `git diff --check origin/developer...HEAD`

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-4/H4; затем архитектор —
human merge; затем methodology-architect-01 — PR-5/H5 source-consumer reminder.
