# TASK для METH-SUPERSEDED-BANNER-01

```yaml
task_contract:
  version: 1
  task_id: METH-SUPERSEDED-BANNER-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-mir-13-superseded-banner-01

  scope:
    allowed_files:
      - docs/agent-system/PR_WORKFLOW.md
      - docs/agent-system/LANGUAGE_POLICY.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/templates/SUPERSEDED_BANNER.md
      - docs/agent-system/cloud/06_CURRENT_STATE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/cloud/20_LANGUAGE_POLICY.md
      - docs/agent-system/engine-journal/input/TASK-0135-METH-SUPERSEDED-BANNER-01.md
      - docs/agent-system/engine-journal/output/RESULT-0135-METH-SUPERSEDED-BANNER-01.md
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
      - product/runtime files
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
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0135-METH-SUPERSEDED-BANNER-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0135-METH-SUPERSEDED-BANNER-01.md --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - developer_not_equal_origin_developer
    - changed_file_outside_allowlist
    - superseded_template_not_russian_first
    - ready_gate_hard_blocks_superseded_advisory_warning
    - ready_gate_misses_malformed_superseded_banner
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Реализовать MIR-13 для patch release `v1.5.1`: добавить стандарт
machine-readable superseded banner, visible Russian-first строку и мягкую
проверку в ready-gate.

## Baseline

- `origin/developer`: `84267fa77214a394b62927ac06d2c4b8389475ef`.
- PR #300 merged at `2026-07-01T17:20:31Z`.
- Latest release tag before patch series: `v1.5.0`.
- Last journal row before this task: `0134`.
- `execution_started_at`: `2026-07-02T00:38:24.3707362+07:00`.

## Acceptance criteria

- Добавлен `docs/agent-system/templates/SUPERSEDED_BANNER.md`.
- Machine-readable comment имеет формат
  `<!-- SUPERSEDED_BY: <file>; PR: <n>; DATE: <YYYY-MM-DD> -->`.
- Шаблон содержит видимую Russian-first строку для rendered Markdown.
- `PR_WORKFLOW.md` и `LANGUAGE_POLICY.md` описывают правило применения.
- `check_task_ready.py` подсвечивает malformed/missing superseded banner как
  advisory warning, не hard blocker.
- Manifest, generated file map, cloud mirror и journal обновлены.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task
  contract validation, commit-message validation и diff whitespace check pass.

## Non-goals

- Не реализовывать MIR-14 execution timing discipline.
- Не создавать release `v1.5.1`, release PR или tag.
- Не читать target repositories и private downstream data.
- Не переписывать historical superseded/stub documents.

## Передача

Следующий: methodology-reviewer-01 — scoped review MIR-13; затем архитектор —
human merge PR в `developer`; затем серия продолжается MIR-14.
