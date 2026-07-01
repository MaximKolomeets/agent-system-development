# TASK для METH-NAVIGATION-INDEX-01

```yaml
task_contract:
  version: 1
  task_id: METH-NAVIGATION-INDEX-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-navigation-index-01

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/input/TASK-0124-METH-NAVIGATION-INDEX-01.md
      - docs/agent-system/engine-journal/output/RESULT-0124-METH-NAVIGATION-INDEX-01.md
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
      - docs/agent-system/templates/**
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0124-METH-NAVIGATION-INDEX-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0124-METH-NAVIGATION-INDEX-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - need_to_merge_or_rewrite_existing_docs
    - need_to_change_templates_or_tools
    - need_to_change_runtime_or_ci
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Добавить `docs/agent-system/METHODOLOGY_MAP.md` как единый навигатор по
методологии: категории, назначение документов, когда применять, границы
дублирования и target docs-taxonomy (MIR-06). Добавить ссылку из root
`README.md`, зарегистрировать новый source-док в manifest и обновить generated
maps/mirrors штатными генераторами.

## Non-goals

- Не сливать и не переписывать существующие документы.
- Не менять templates/tools/runtime/CI.
- Не менять состав `orchestrator_context_bundle`.
- Не включать private downstream data или project-specific сведения.

## Контекст sequence

Внешний handoff-пакет назван `PR 0123`, но актуальный
`docs/agent-system/engine-journal/INDEX.md` после xref hygiene завершается на
`0123`. По правилу `INDEX last+1` фактический journal seq этой задачи: `0124`.

## Acceptance criteria

- `METHODOLOGY_MAP.md` покрывает source-set methodology repository по категориям.
- У кластеров с риском перекрытия есть явная строка "Граница".
- Есть target docs-taxonomy для target repositories.
- Root `README.md` ссылается на карту из reading-list.
- `ADOPTION_TRANSFER_MANIFEST.yml`, `PROJECT_FILE_MAP.md` и generated cloud
  mirrors согласованы с новым source-доком и journal row.
- `docs/agent-system/templates/**`, `docs/agent-system/tools/**`, runtime/CI и
  существующие methodology docs вне allowed files не меняются.

## Expected reviewer mode

Scoped docs review: reviewer проверяет полноту карты, корректность границ,
target taxonomy, отсутствие scope drift и generated parity.

## Передача

Следующий: reviewer — scoped navigation index review.
