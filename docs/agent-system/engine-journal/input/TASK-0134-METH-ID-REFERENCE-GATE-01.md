# TASK для METH-ID-REFERENCE-GATE-01

```yaml
task_contract:
  version: 1
  task_id: METH-ID-REFERENCE-GATE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-mir-12-id-reference-gate-01

  scope:
    allowed_files:
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/validate_id_references.py
      - docs/agent-system/cloud/06_CURRENT_STATE.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/input/TASK-0134-METH-ID-REFERENCE-GATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0134-METH-ID-REFERENCE-GATE-01.md
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
      - python docs/agent-system/tools/validate_id_references.py
      - python docs/agent-system/tools/validate_id_references.py --json
      - python docs/agent-system/tools/validate_id_references.py --sample-text "## CTRL-ABC\nСсылка на CTRL-ABC"
      - python docs/agent-system/tools/validate_id_references.py --sample-text "Ссылка на CTRL-XXX" expected_failure
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0134-METH-ID-REFERENCE-GATE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0134-METH-ID-REFERENCE-GATE-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - developer_not_equal_origin_developer
    - changed_file_outside_allowlist
    - valid_id_reference_fixture_fails
    - dangling_id_reference_fixture_passes
    - ready_gate_does_not_run_id_reference_check
    - need_to_rewrite_merged_history
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Реализовать MIR-12 для patch release `v1.5.1`: добавить read-only gate
целостности methodology ID references и подключить его в общий ready-gate.

## Baseline

- `origin/developer`: `cbf57c848d8537b4ace5bc348148ba1b692d2a1b`.
- PR #299 merged at `2026-07-01T16:55:46Z`.
- Latest release tag before patch series: `v1.5.0`.
- Last journal row before this task: `0133`.

## Acceptance criteria

- Добавлен `docs/agent-system/tools/validate_id_references.py`.
- Regex canon покрывает `F-09.N`, `CTRL-*` и
  `IMPORT_/UNIT_/REFERENCE_/ARTIFACT_/AUDIT_/RENDER_/PIPELINE_*`.
- Dangling references блокируются без печати содержимого matched строк.
- Valid fixture с определением `CTRL-ABC` проходит.
- Broken fixture со ссылкой `CTRL-XXX` без определения падает.
- `check_task_ready.py` запускает `validate_id_references.py`.
- Manifest, generated file map, cloud mirror и journal обновлены.
- Ready-gate, generated EOL guard, file-map check, cloud bundle check, task
  contract validation, commit-message validation и diff whitespace check pass.

## Non-goals

- Не реализовывать MIR-13 superseded-banner standard.
- Не создавать release `v1.5.1`, release PR или tag.
- Не читать target repositories и private downstream data.
- Не переписывать historical commits или merge commits.

## Передача

Следующий: methodology-reviewer-01 — scoped review MIR-12; затем архитектор —
human merge PR в `developer`; затем серия продолжается MIR-13.
