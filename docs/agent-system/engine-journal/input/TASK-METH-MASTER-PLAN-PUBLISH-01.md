# TASK: METH-MASTER-PLAN-PUBLISH-01

## Статус

- Статус: `in_progress`
- Создано: `2026-07-05T15:42:25.6525503+07:00`
- Роль: `docs-maintainer-01`
- Исполнитель: на усмотрение архитектора
- Ветка: `work/docs-maintainer-01/master-plan-01`
- Base: `origin/developer` / `9e644319c0b9411aeebeea9fd0c84f54a04248e2`

## task_contract

```yaml
task_contract:
  version: 1
  task_id: METH-MASTER-PLAN-PUBLISH-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: low

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/master-plan-01

  methodology_development_base:
    base_branch: developer
    working_branch: work/docs-maintainer-01/master-plan-01
    base_commit: 9e644319c0b9411aeebeea9fd0c84f54a04248e2
    checked_at: 2026-07-05T15:42:25.6525503+07:00

  scope:
    allowed_files:
      - docs/master-plan/MASTER_PLAN.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/engine-journal/**
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
    forbidden_files:
      - .env
      - .env.*
      - .github/**
      - AGENTS.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - README.md
      - docs/agent-system/engine-journal/output/RESULT-0155-METH-SELF-ENFORCEMENT-HARDENING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0156-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/output/RESULT-0157-METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0158-METH-RELEASE-PREP-V1-5-3-01.md
      - docs/agent-system/engine-journal/output/RESULT-0159-METH-POST-RELEASE-STATE-REFRESH-V1-5-3-01.md
      - docs/agent-system/engine-journal/output/RESULT-0160-METH-RELEASE-ASSISTANT-01.md
      - docs/agent-system/engine-journal/output/RESULT-0161-METH-RELEASE-GATE-CLEANUP-01.md

  policies:
    journal: required
    cloud_regen: conditional
    generated_checks: required
    review: scoped_semantic
    merge: human_only
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - source/master-plan byte identity check

  stop_conditions:
    - dirty_tree_before_start
    - source_file_missing_or_header_mismatch
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - manifest_category_unclear
    - secret_or_env_risk
```

## Цель

Опубликовать утверждённый мастер-план версии 1.2.1 из
`C:\neural\repos\agent\MASTER_PLAN.md` в публичный repository path
`docs/master-plan/MASTER_PLAN.md` без изменения содержимого, добавить запись
из раздела 14 мастер-плана в `DECISION_LOG.md` и зафиксировать journal row 0162.

## Acceptance criteria

- `docs/master-plan/MASTER_PLAN.md` byte-identical source-файлу.
- В `DECISION_LOG.md` новая запись вставлена сразу после `# DECISION_LOG`.
- Journal row 0162, TASK и RESULT финализированы без placeholders.
- Manifest/cloud не меняются, если штатные tools не требуют обновления.

## Передача

Следующий: reviewer - scoped semantic review.
