```yaml
task_contract:
  version: 1
  task_id: METH-NO-ORDINARY-POST-MERGE-CLOSURE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-no-ordinary-post-merge-closure-01

  scope:
    allowed_files:
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/REVIEW_AUTOLOOP.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/OPERATIONAL_FAST_LANE.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
      - docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md
      - docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/engine-journal/input/TASK-*-METH-NO-ORDINARY-POST-MERGE-CLOSURE-01.md
      - docs/agent-system/engine-journal/output/RESULT-*-METH-NO-ORDINARY-POST-MERGE-CLOSURE-01.md
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
    cloud_regen: required
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0114-METH-NO-ORDINARY-POST-MERGE-CLOSURE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0114-METH-NO-ORDINARY-POST-MERGE-CLOSURE-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
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
```

# TASK-0114 - METH-NO-ORDINARY-POST-MERGE-CLOSURE-01

Время начала выполнения (execution_started_at) [measured/engine]: 2026-06-27T11:13:22.1465458+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: не указано

## Цель

Убрать обязательный post-merge closure debt для ordinary PR: обычный task PR должен завершаться на `architect_ready` / `human_merge_allowed` с PR URL и reviewed head SHA, а GitHub PR metadata должна быть source of truth для `merged_at`, merge commit SHA, PR state и PR URL.

## Scope

Изменить только разрешенные policy/docs/templates/state/cloud/journal файлы. Не переписывать старые `RESULT/INDEX`, не делать batch cleanup, не создавать отдельный closure PR и не менять runtime/Docker/CI/branch protection.

## Требуемый канон

- Ordinary PR не требует отдельной правки `RESULT/INDEX` после каждого human merge.
- Отсутствие `merged_at` и merge commit SHA в `RESULT` ordinary PR не является blocker.
- Boundary reconciliation нужна только перед release/audit boundary, при explicit architect request или для batch reconciliation.
- Reviewer не должен требовать post-merge closure для ordinary PR.
- Orchestrator после merge ordinary PR синхронизирует `developer` и переходит к следующей задаче.
- Старые append-only journal entries не переписываются ради нового канона.

## Проверки

Выполнить проверки из `task_contract.checks.required`, safety scan и allowlist scan. Если generated bundle или file map изменились, регенерировать и проверить их.

## Передача

Следующий: methodology-architect-01 — реализовать изменения, открыть PR в `developer` и передать на scoped semantic + lifecycle review.
