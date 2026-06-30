# TASK для METH-XREF-AND-READINGLIST-HYGIENE-01

```yaml
task_contract:
  version: 1
  task_id: METH-XREF-AND-READINGLIST-HYGIENE-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-xref-and-readinglist-hygiene-01

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_GUIDE.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md
      - docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
      - docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0123-METH-XREF-AND-READINGLIST-HYGIENE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0123-METH-XREF-AND-READINGLIST-HYGIENE-01.md
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
      - docs/agent-system/PROJECT_FILE_MAP.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0123-METH-XREF-AND-READINGLIST-HYGIENE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0123-METH-XREF-AND-READINGLIST-HYGIENE-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - need_to_change_project_file_map
    - need_to_change_templates_or_tools
    - adoption_semantics_change_needed
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Единообразно пометить ссылки на target-local артефакты как `target-local` и указать канонический шаблон при первом/проверяемом упоминании. Уточнить path hygiene в README reading-list: root `AGENTS.md`, явный `engine-journal/INDEX.md`, target-local `PROJECT_CONSTITUTION.md`, template path для `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md`.

## Контекст sequence

Внешний handoff-пакет был назван `PR 0122`, но актуальный `docs/agent-system/engine-journal/INDEX.md` после EOL PR завершается на `0122`. По `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` фактический journal seq этой задачи: `0123`.

## Acceptance criteria

- В allowed-доках прямые full-path ссылки на `ADOPTION_AUDIT.md`, `ENGINE_REGISTRY.md` и `PROJECT_GUARDRAILS.md` помечены `target-local`.
- Для `ADOPTION_AUDIT`, `ENGINE_REGISTRY`, `PROJECT_GUARDRAILS` указан канонический template path.
- README reading-list/path hygiene уточняет root/template/journal/target-local intent.
- `docs/agent-system/templates/**`, `docs/agent-system/tools/**` и `docs/agent-system/PROJECT_FILE_MAP.md` не меняются.
- Смысл adoption-процесса не меняется; правки ограничены аннотациями и путями.

## Expected reviewer mode

Scoped docs review: reviewer проверяет target-local xref consistency, reading-list path clarity, отсутствие scope drift и generated parity для `INDEX`.

## Передача

Следующий: reviewer — scoped xref hygiene review.
