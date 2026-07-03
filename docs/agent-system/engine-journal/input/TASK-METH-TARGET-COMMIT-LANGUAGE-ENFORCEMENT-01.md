# TASK METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01

Файл задачи: `docs/agent-system/engine-journal/input/TASK-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md`

Идентификатор задачи: `METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01`

Sequence: `0156`

Роль: `docs-maintainer-01`

Исполнитель: на усмотрение архитектора

Режим: `agent`

Запуск: `local_only`

Reasoning effort: `medium`

execution_started_at: `2026-07-03T23:19:36.3136645+07:00`

Base branch: `developer`

Working branch: `work/docs-maintainer-01/meth-target-commit-language-enforcement-01`

Task source: attached Engine block `ENGINE_BLOCK_METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md`

PR #326 dependency: satisfied; PR #326 merged into `developer` at `2026-07-03T16:16:07Z`, merge commit `e7f1b01582f209ff689ff199bd3597c3e5f8321f`.

## task_contract

```yaml
task_contract:
  version: 1
  task_id: METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-target-commit-language-enforcement-01

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 1859a0034b14eed11e9842c4589fdeddb295cc6d
    reference_type: methodology_development
    checked_at: 2026-07-03T00:00:00+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-target-commit-language-enforcement-01
    base_commit: e7f1b01582f209ff689ff199bd3597c3e5f8321f
    checked_at: 2026-07-03T23:19:36.3136645+07:00

  scope:
    allowed_files:
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/ADOPTION_GUIDE.md
      - docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
      - docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/METHODOLOGY_IMPROVEMENT_LEDGER.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/engine-journal/**
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
      - AGENTS.md
      - .github/**
      - docs/agent-system/tools/**

  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
    optional:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md --json

  stop_conditions:
    - pr_326_not_merged_into_developer
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - new_tool_or_code_needed
    - tool_overlap_needs_architect_decision
    - secret_or_env_risk
    - destructive_git_needed
```

## Цель

Закрыть пробел: target adoption должен требовать Russian-first commit-language enforcement в target repository. Задача является docs/policy правкой и не создает новых tools.

## Scope

Изменить только разрешенные policy/adoption/governance/journal/generated файлы. Не менять `.github/**`, `docs/agent-system/tools/**`, `AGENTS.md`, `.env*`, runtime/data/export paths.

## Требования

- В `DOWNSTREAM_ADAPTATION_CHECKLIST.md` добавить проверяемые пункты про commit-language / Russian-first enforcement.
- В `CI_POLICY.md` закрепить target adaptation requirement: target CI/runtime adoption должен переиспользовать существующие commit-language tools и сохранять safe output contract.
- В `ADOPTION_GUIDE.md` добавить шаг existing-repo adoption про включение commit-language enforcement.
- В `TARGET_PROJECT_GOVERNANCE_PACK.md` и `templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md` добавить требование Russian-first commit enforcement как target guardrail.
- В `ADOPTION_TRANSFER_MANIFEST.yml` добавить короткую notes-запись: tools переносимы как source, target CI создается как target adaptation, `.github/**` methodology repository не копируется.
- Если manifest изменен, регенерировать `PROJECT_FILE_MAP.md` и `docs/agent-system/cloud/**` через генераторы.
- Добавить sanitized triage row в `METHODOLOGY_IMPROVEMENT_LEDGER.md`.
- Обновить `CURRENT_STATE.md`/`NEXT_STEPS.md`, если меняется состояние проекта.
- Финализировать RESULT/INDEX с обязательными разделами `## Methodology feedback`, `## Unprompted Project Proposals` и `## Передача`.

## Обязательное proposal в RESULT

В `## Unprompted Project Proposals` зафиксировать `METH-COMMIT-LANGUAGE-TOOL-RECONCILE-01`: проверить пересечение `check_commit_language.py` и `validate_commit_message.py`, выбрать канонический инструмент и устранить дублирование отдельной tooling-задачей. В текущем PR tools не менять.

## Проверки

- `python docs/agent-system/tools/check_task_ready.py --base origin/developer`
- `python docs/agent-system/tools/validate_policy_invariants.py`
- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check origin/developer...HEAD`
- optional: `python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-METH-TARGET-COMMIT-LANGUAGE-ENFORCEMENT-01.md --json`

## Передача

Следующий: docs-maintainer-01 — выполнить docs/policy правку и открыть PR в `developer`; затем reviewer — scoped semantic review.
