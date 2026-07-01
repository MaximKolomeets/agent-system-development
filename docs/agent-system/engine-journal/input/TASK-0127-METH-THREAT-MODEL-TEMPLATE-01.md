# TASK для METH-THREAT-MODEL-TEMPLATE-01

```yaml
task_contract:
  version: 1
  task_id: METH-THREAT-MODEL-TEMPLATE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-threat-model-template-01

  scope:
    allowed_files:
      - docs/agent-system/templates/THREAT_MODEL_TEMPLATE.md
      - docs/agent-system/SECURITY_POLICY.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/input/TASK-0127-METH-THREAT-MODEL-TEMPLATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0127-METH-THREAT-MODEL-TEMPLATE-01.md
      - docs/agent-system/engine-journal/INDEX.md
    forbidden_files:
      - .env
      - .env.*
      - .venv/**
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - docs/agent-system/tools/**
      - product/runtime/CI files
      - credentials
      - tokens
      - access key material
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data
      - production/runtime data

  policies:
    journal: required
    cloud_regen: required
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    language: russian_first

  checks:
    required:
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0127-METH-THREAT-MODEL-TEMPLATE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0127-METH-THREAT-MODEL-TEMPLATE-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - product_threat_data_or_private_details_needed
    - need_to_change_tools_or_runtime_or_ci
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Добавить reusable `docs/agent-system/templates/THREAT_MODEL_TEMPLATE.md`:
активы, таблица `Угроза -> Контроль -> Тест -> CI-gate -> severity -> этап`,
residual risks и связь с `CONTROL_MATRIX_PATTERN.md` /
`ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`. Добавить ссылки из
`SECURITY_POLICY.md` и `METHODOLOGY_MAP.md`, зарегистрировать template и
target-generated mapping в manifest и обновить generated maps/mirrors штатными
генераторами.

## Non-goals

- Не дублировать controls из `SECURITY_POLICY.md`.
- Не добавлять product/runtime threat data.
- Не включать private downstream data или project-specific сведения.
- Не менять tools/runtime/CI.

## Контекст sequence

Актуальный `docs/agent-system/engine-journal/INDEX.md` после external review
ledger завершается на `0126`. По правилу `INDEX last+1` фактический journal seq
этой задачи: `0127`.

## Acceptance criteria

- Template содержит assets, threat table, residual risks и rule section.
- Threat table содержит `Угроза`, `Контроль`, `Тест`, `CI-gate`, `severity`,
  `этап`.
- Template связывает threat model с `CONTROL_MATRIX_PATTERN.md` и
  `ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`.
- `SECURITY_POLICY.md` и `METHODOLOGY_MAP.md` ссылаются на template.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` и generated cloud
  mirrors согласованы с новым template и journal row.
- Product/runtime threat data не добавлены.

## Expected reviewer mode

Scoped methodology review: reviewer проверяет template, security policy/map
links, отсутствие product threat data, manifest/generated parity.

## Передача

Следующий: reviewer — scoped threat model template review.
