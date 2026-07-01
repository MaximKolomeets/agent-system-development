# TASK для METH-EXTERNAL-REVIEW-LEDGER-01

```yaml
task_contract:
  version: 1
  task_id: METH-EXTERNAL-REVIEW-LEDGER-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-external-review-ledger-01

  scope:
    allowed_files:
      - docs/agent-system/EXTERNAL_REVIEW_LEDGER_PATTERN.md
      - docs/agent-system/templates/EXTERNAL_REVIEW_LEDGER_TEMPLATE.md
      - docs/agent-system/REVIEW_AUTOLOOP.md
      - docs/agent-system/QUALITY_FIRST_WORKFLOW.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/cloud/12_REVIEW_AUTOLOOP.md
      - docs/agent-system/engine-journal/input/TASK-0126-METH-EXTERNAL-REVIEW-LEDGER-01.md
      - docs/agent-system/engine-journal/output/RESULT-0126-METH-EXTERNAL-REVIEW-LEDGER-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0126-METH-EXTERNAL-REVIEW-LEDGER-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0126-METH-EXTERNAL-REVIEW-LEDGER-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - ledger_forced_on_small_tasks
    - need_to_change_tools_or_runtime_or_ci
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Добавить reusable `EXTERNAL_REVIEW_LEDGER_PATTERN.md` и template для
много-ревьюируемых документов/решений: statuses `applied`/`deferred`/`rejected`,
anti-loop rule, critical categories и diminishing-returns stop. Добавить ссылки
из `REVIEW_AUTOLOOP.md`, `QUALITY_FIRST_WORKFLOW.md`, `METHODOLOGY_MAP.md`,
зарегистрировать новые files в manifest и обновить generated maps/mirrors
штатными генераторами.

## Non-goals

- Не отменять `REVIEW_AUTOLOOP.md` или `QUALITY_FIRST_WORKFLOW.md`.
- Не запрещать review; цель - упорядочить multi-round external review и stop
  rule.
- Не делать ledger обязательным для каждой мелкой task или ordinary PR.
- Не менять tools/runtime/CI.
- Не включать private downstream data или project-specific сведения.

## Контекст sequence

Актуальный `docs/agent-system/engine-journal/INDEX.md` после control matrix
pattern завершается на `0125`. По правилу `INDEX last+1` фактический journal seq
этой задачи: `0126`.

## Acceptance criteria

- Pattern описывает отличие от autoloop/feedback loop.
- Pattern описывает statuses `applied`/`deferred`/`rejected`, critical
  categories и diminishing-returns stop.
- Template пригоден к заполнению для много-ревьюируемого документа/решения.
- `REVIEW_AUTOLOOP.md`, `QUALITY_FIRST_WORKFLOW.md` и `METHODOLOGY_MAP.md`
  ссылаются на pattern без превращения ledger в тяжелый процесс для мелких задач.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` и generated cloud
  mirrors согласованы с новыми source/template files и journal row.
- Tools/runtime/CI и product files не меняются.

## Expected reviewer mode

Scoped methodology review: reviewer проверяет pattern/template, anti-loop
границу, ссылки, отсутствие scope drift и generated parity.

## Передача

Следующий: reviewer — scoped external review ledger pattern review.
