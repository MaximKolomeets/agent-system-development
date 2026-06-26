# TASK-0110-METH-TASK-CONTRACT-CLOUD-BUNDLE-01

```yaml
task_contract:
  version: 1
  task_id: METH-TASK-CONTRACT-CLOUD-BUNDLE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-task-contract-cloud-bundle-01
  scope:
    allowed_files:
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/engine-journal/input/TASK-0110-METH-TASK-CONTRACT-CLOUD-BUNDLE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0110-METH-TASK-CONTRACT-CLOUD-BUNDLE-01.md
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
    review: machine_only
    merge: human_only
    closure_pr: false
  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0110-METH-TASK-CONTRACT-CLOUD-BUNDLE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0110-METH-TASK-CONTRACT-CLOUD-BUNDLE-01.md --json
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

Добавить `docs/agent-system/TASK_CONTRACT.md` в default cloud/orchestrator bundle, чтобы cloud-only context видел канон `task_contract` без отдельной ручной загрузки source-файла.

## Решение архитектора по STOP

Первичный STOP был корректным: `orchestrator_context_bundle` валидируется против `CANONICAL_BUNDLE_ORDER` в `docs/agent-system/tools/gen_cloud_bundle.py`. Архитектор разрешил узко расширить allowed files и изменить только `CANONICAL_BUNDLE_ORDER`, добавив `docs/agent-system/TASK_CONTRACT.md` после `docs/agent-system/REVIEW_AUTOLOOP.md`.

## Scope

- В `ADOPTION_TRANSFER_MANIFEST.yml` добавить `TASK_CONTRACT.md` в `orchestrator_context_bundle`.
- В `gen_cloud_bundle.py` изменить только `CANONICAL_BUNDLE_ORDER`.
- Регенерировать `PROJECT_FILE_MAP.md` и `docs/agent-system/cloud/**`.
- Минимально обновить state/history docs: `BACKLOG.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md`.
- Создать journal entry 0110.

## Запрещено

- Не менять `docs/agent-system/TASK_CONTRACT.md`.
- Не менять `docs/agent-system/tools/validate_task_contract.py`.
- Не менять `docs/agent-system/tools/check_task_ready.py`.
- Не менять runtime/Docker/CI/branch protection.
- Не читать `.env` и не выводить secrets/matching lines.
- Не создавать release PR, merge или отдельный closure PR.

## Execution timestamps

- execution_started_at: `2026-06-26T00:53:36.1666434+07:00`
- orchestration_time_reported: не применимо

## Передача

Следующий: methodology-reviewer-01 — machine-only/generated parity review PR; затем архитектор — human merge; batch-closure — перед следующим release/audit boundary.
