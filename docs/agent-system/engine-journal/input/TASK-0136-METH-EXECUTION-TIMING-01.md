# TASK для METH-EXECUTION-TIMING-01

```yaml
task_contract:
  version: 1
  task_id: METH-EXECUTION-TIMING-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-mir-14-execution-timing-01

  scope:
    allowed_files:
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/cloud/00_README.md
      - docs/agent-system/cloud/01_ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/cloud/05_ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/cloud/06_CURRENT_STATE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/09_ENGINE_ENTRYPOINT.md
      - docs/agent-system/engine-journal/input/TASK-0136-METH-EXECUTION-TIMING-01.md
      - docs/agent-system/engine-journal/output/RESULT-0136-METH-EXECUTION-TIMING-01.md
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
      - function-level execution timing smoke for start equals finish
      - function-level execution timing smoke for realistic duration
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0136-METH-EXECUTION-TIMING-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0136-METH-EXECUTION-TIMING-01.md --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - developer_not_equal_origin_developer
    - changed_file_outside_allowlist
    - execution_started_at_not_persisted_in_task
    - ready_gate_hard_blocks_execution_timing_advisory
    - ready_gate_misses_equal_start_finish_with_substantive_diff
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Реализовать MIR-14 для patch release `v1.5.1`: закрепить дисциплину захвата
execution-времени в journal/entrypoint/orchestrator contract и добавить soft
detector в ready-gate.

## Baseline

- `origin/developer`: `867082c089ab16c4fea094ee697db0e10082f5ca`.
- PR #301 merged at `2026-07-01T17:51:52Z`.
- Latest release tag before this task: `v1.5.0`.
- Last journal row before this task: `0135`.
- `execution_started_at`: `2026-07-02T00:56:28.4158553+07:00`.

## Acceptance criteria

- `ENGINE_JOURNAL_CONTRACT.md` явно закрепляет: `execution_started_at`
  фиксируется в начале выполнения, сохраняется в TASK и не перезаписывается при
  финализации RESULT.
- `ENGINE_JOURNAL_CONTRACT.md` явно закрепляет: `execution_finished_at`
  фиксируется в конце выполнения, а `execution_duration` вычисляется из пары
  measured timestamps.
- `ENGINE_ENTRYPOINT.md` и `ORCHESTRATOR_OPERATING_CONTRACT.md` описывают
  первый шаг engine: застолбить start timestamp до содержательной работы.
- `check_task_ready.py` выдаёт advisory finding `unreliable execution timing`,
  если RESULT с содержательным diff имеет start equals finish или длительность
  ниже порога.
- Function-level smoke подтверждает finding для start equals finish и чистый
  результат для корректной длительности.
- Cloud mirrors и journal обновлены.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task
  contract validation, commit-message validation и diff whitespace check pass.

## Non-goals

- Не создавать release `v1.5.1`, release PR или tag.
- Не менять runtime/product files.
- Не читать target repositories и private downstream data.
- Не переписывать historical RESULT entries с уже равными timestamps.

## Передача

Следующий: methodology-reviewer-01 — scoped review MIR-14; затем архитектор —
human merge PR в `developer`; затем серия переходит к release-prep `v1.5.1`.
