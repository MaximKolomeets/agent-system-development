```yaml
task_contract:
  version: 1
  task_id: METH-FIX-AUTHORIZATION-HEADER-GUARD-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-fix-authorization-header-guard-01

  scope:
    allowed_files:
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/engine-journal/input/TASK-*-METH-FIX-AUTHORIZATION-HEADER-GUARD-01.md
      - docs/agent-system/engine-journal/output/RESULT-*-METH-FIX-AUTHORIZATION-HEADER-GUARD-01.md
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
    review: scoped_technical_safety
    merge: human_only
    closure_pr: false
    language: russian_first
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0115-METH-FIX-AUTHORIZATION-HEADER-GUARD-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0115-METH-FIX-AUTHORIZATION-HEADER-GUARD-01.md --json
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

# TASK-0115 - METH-FIX-AUTHORIZATION-HEADER-GUARD-01

Время начала выполнения (execution_started_at) [measured/engine]: 2026-06-27T12:36:45.8658724+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: не указано

## Цель

Усилить strict added-line scan в `docs/agent-system/tools/check_task_ready.py`, чтобы заголовок `Authorization` блокировался как sensitive risk независимо от auth-схемы и регистра имени header.

## Scope

Изменить только ready-gate tooling, минимальные state docs, generated/file-map при необходимости и journal 0115. Не менять target repository `verification`, product/runtime/CI, branch protection, release/tag flow и старую append-only историю.

## Требуемое поведение

- Любая добавленная строка с реальным header `Authorization` должна попадать в `strict_added_line_secret_value_count`.
- Matching values не должны печататься в human/json output; допустимы только count, filenames и category.
- Safe placeholder allowlist не обязателен: строгая блокировка header допустима как более безопасный вариант.
- `.env` не читать, external dependencies не добавлять.

## Targeted smoke

До постоянных изменений выполнить временный local smoke с искусственным добавленным header value через file-intent diff. Ожидаемый результат: `check_task_ready.py --json` возвращает blocker и `strict_added_line_secret_value_count` больше нуля. Временный smoke-файл удалить до commit.

## Проверки

Выполнить проверки из `task_contract.checks.required`, allowlist scan и safety scan. Если `PROJECT_FILE_MAP.md` или cloud bundle потребуют regeneration, выполнить штатную генерацию.

## Передача

Следующий: methodology-architect-01 — реализовать safety hotfix, открыть PR в `developer` и передать на scoped technical safety review.
