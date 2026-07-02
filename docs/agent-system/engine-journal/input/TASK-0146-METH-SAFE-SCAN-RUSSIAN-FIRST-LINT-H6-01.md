# TASK для METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01

Задача для methodology-architect-01: METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01

```yaml
task_contract:
  version: 1
  task_id: METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-9-safe-scan-russian-lint

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 8db7df25e494e0a28e84ec9e703961fba3ad78e6
    reference_type: methodology_development
    checked_at: 2026-07-02T20:45:35.5246341+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-9-safe-scan-russian-lint
    base_commit: 8db7df25e494e0a28e84ec9e703961fba3ad78e6
    checked_at: 2026-07-02T20:45:35.5246341+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/LANGUAGE_POLICY.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/PUBLICATION_POLICY.md
      - docs/agent-system/cloud/**
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/russian_first_lint.py
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0146-METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01.md
      - docs/agent-system/engine-journal/output/RESULT-0146-METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01.md
    forbidden_files:
      - .env
      - .env.*
      - .venv/**
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - credentials
      - tokens
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data

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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0146-METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0146-METH-SAFE-SCAN-RUSSIAN-FIRST-LINT-H6-01.md
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
    - direct_main_push_or_tag_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-9/H6 меняет docs/tooling методологии, усиливает безопасные scan-команды
и добавляет lightweight Russian-first lint, но не требует runtime, CI/CD,
branch-protection, секретов или product changes.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T20:45:35.5246341+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-9-safe-scan-russian-lint`.
- Base commit: `8db7df25e494e0a28e84ec9e703961fba3ad78e6`.
- PR #314 state before start: merged at `2026-07-02T13:32:49Z`.
- Working tree before branch creation: clean.

## PR/H mapping guard

- Выполняемый блок: `PR-9 = H6`.
- `H6` является P2 item Safe-scan & Russian-first lint.
- P1 уже закрыт: H1, H2, H3, H4, H5, H9, H13, H14.

## Цель

Выполнить PR-9/H6 из hardening-блока v1.5.2:
заменить line-printing secret-review команды на filename/count-only scan,
добавить lightweight Russian-first lint для active docs и привести
англоязычную prose в `CI_POLICY.md` и `ENGINE_JOURNAL_CONTRACT.md` к
Russian-first.

## Требуемые изменения

- В `CI_POLICY.md` и `PUBLICATION_POLICY.md` заменить default `git grep -n`
  на filename-only/count-only `git grep -I -l ...` и запретить печать matching
  lines/values.
- Добавить `docs/agent-system/tools/russian_first_lint.py`.
- Подключить Russian-first lint к `check_task_ready.py` как changed-only gate
  для active Markdown docs.
- Исключить append-only journal/history/generated/source snapshots и literal
  technical regions из lint scope.
- Обновить `LANGUAGE_POLICY.md`, README, `METHODOLOGY_MAP.md`, manifest,
  `PROJECT_FILE_MAP.md` и cloud bundle.
- Создать и финализировать RESULT/INDEX после PR creation.

## Acceptance criteria

- В docs нет default-команд, которые печатают matching secret lines через
  `git grep -n`.
- Safe-scan policy требует filenames/counts only и запрещает копировать values
  в terminal, logs, journal, PR body или final report.
- `russian_first_lint.py --base origin/developer` проходит на измененных
  active docs и выводит только `path:line` + code.
- `check_task_ready.py --base origin/developer` запускает Russian-first lint и
  блокирует changed active docs с англоязычной prose.
- `CI_POLICY.md` и `ENGINE_JOURNAL_CONTRACT.md` являются Russian-first, кроме
  technical identifiers и literal external names.
- Manifest, file map и cloud bundle синхронизированы.
- RESULT/INDEX финализируются после PR creation.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch,
финальный head SHA, changed files summary, checks, generated artifacts,
accounting fields, risks, Source Delta, PR/H mapping note и блок «Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-9/H6; затем архитектор —
human merge; затем methodology-architect-01 — следующий P2 item по таблице
PR/H hardening plan.
