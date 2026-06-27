# TASK-0113-METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01

```yaml
task_contract:
  version: 1
  task_id: METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-stable-main-reference-russian-first-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    ref: developer
    stable_only: false
    source_commit: 6f3357cbd252ddf5a51a7d023747bcd2e037719e
    checked_at: 2026-06-26T23:09:56+07:00

  scope:
    allowed_files:
      - docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md
      - docs/agent-system/LANGUAGE_POLICY.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/REVIEW_AUTOLOOP.md
      - docs/agent-system/OPERATIONAL_FAST_LANE.md
      - docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
      - docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
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
      - docs/agent-system/tools/validate_task_contract.py
      - docs/agent-system/engine-journal/input/TASK-0113-METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01.md
      - docs/agent-system/engine-journal/output/RESULT-0113-METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01.md
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
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0113-METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0113-METH-STABLE-MAIN-REFERENCE-RUSSIAN-FIRST-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - git diff --name-status origin/developer...HEAD
      - git diff --stat origin/developer...HEAD

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

Закрепить stable methodology reference для downstream/target задач и усилить Russian-first policy для GitHub-facing артефактов.

## Scope

Изменения выполняются только в public methodology repository и только в allowlist выше. Product repositories, `verification`, runtime, Docker, CI, branch protection, release PR/merge, closure PR и private downstream data не входят в scope.

## Требования

- Добавить канон `STABLE_METHODOLOGY_REFERENCE_POLICY.md`.
- Обновить `LANGUAGE_POLICY.md` так, чтобы PR title/body, commit messages, review summaries, verdict comments и final reports были Russian-first.
- Обновить orchestrator/reviewer/engine templates так, чтобы downstream/adoption задачи использовали stable reference `origin/main` / `main`, release tag или явно заданный snapshot.
- Запретить для downstream source of truth: `developer`, `work/*`, dirty local methodology tree, open methodology PR branch.
- Зафиксировать, что dirty `agent-system-development/developer` или `work/*` не блокирует downstream задачу, если stable reference читается.
- Обновить manifest, generated cloud bundle, `PROJECT_FILE_MAP.md`, state docs и journal.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch/head SHA, changed files summary, проверки, Safety, Source Delta, Context handoff, Local actions after PR/merge и блок «Передача».

Критично: после merge в `developer` архитектор должен продвинуть methodology в `main`; иначе downstream проекты, корректно читающие `origin/main`, не увидят новую policy.
