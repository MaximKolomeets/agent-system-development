# TASK-0109-METH-TASK-CONTRACT-FRONTMATTER-01

```yaml
task_contract:
  version: 1
  task_id: METH-TASK-CONTRACT-FRONTMATTER-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-task-contract-frontmatter-01
  scope:
    allowed_files:
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/tools/validate_task_contract.py
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/input/TASK-0109-METH-TASK-CONTRACT-FRONTMATTER-01.md
      - docs/agent-system/engine-journal/output/RESULT-0109-METH-TASK-CONTRACT-FRONTMATTER-01.md
      - docs/agent-system/engine-journal/INDEX.md
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - verification/**
      - product repositories
  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0109-METH-TASK-CONTRACT-FRONTMATTER-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0109-METH-TASK-CONTRACT-FRONTMATTER-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - git diff --name-only origin/developer...HEAD
      - git diff --stat origin/developer...HEAD
      - git status --short -uall
  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
```

## Задача

Добавить machine-readable `task_contract` frontmatter для Engine-задач, лёгкий read-only validator и интеграцию в task templates / orchestrator docs / journal policy.

## Контекст

После внедрения review autoloop, ready-gate и generated EOL guard стало полезно фиксировать machine-readable scope задачи до выполнения. Это снижает зависимость от prose parsing и даёт валидатору явные режим, ветки, allowed/forbidden files, checks и STOP conditions.

## Scope

- Создать `docs/agent-system/TASK_CONTRACT.md`.
- Создать `docs/agent-system/tools/validate_task_contract.py`.
- Обновить templates и orchestrator/journal docs так, чтобы новые write-action задачи включали `task_contract`.
- Зарегистрировать новые source files в `ADOPTION_TRANSFER_MANIFEST.yml`.
- Регенерировать `PROJECT_FILE_MAP.md` и cloud bundle после manifest/INDEX/source changes.
- Зафиксировать journal entry 0109.

## Ограничения

- Не менять runtime/Docker/CI/branch protection.
- Не читать `.env`.
- Не печатать secrets или matching secret lines.
- Не создавать release PR, tag или closure PR.
- Не переписывать старые journal entries.
- Не строить большой workflow engine; нужен только lightweight validator.

## Execution timestamps

- execution_started_at: `2026-06-25T23:48:06.5810751+07:00`
- orchestration_time_reported: не применимо

## Передача

Следующий: methodology-reviewer-01 — review PR по scope `task_contract`/validator/templates/generated parity; затем архитектор — human merge; batch-closure — перед следующим release/audit boundary.
