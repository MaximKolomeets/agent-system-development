# TASK для METH-EOL-NORMALIZATION-01

```yaml
task_contract:
  version: 1
  task_id: METH-EOL-NORMALIZATION-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/meth-eol-normalization-01

  scope:
    allowed_files:
      - .gitattributes
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/input/TASK-0122-METH-EOL-NORMALIZATION-01.md
      - docs/agent-system/engine-journal/output/RESULT-0122-METH-EOL-NORMALIZATION-01.md
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
      - credentials
      - tokens
      - private keys
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data
      - production/runtime data

  policies:
    journal: required
    cloud_regen: required
    generated_checks: conditional
    review: scoped_technical_safety
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    language: russian_first

  checks:
    required:
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0122-METH-EOL-NORMALIZATION-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0122-METH-EOL-NORMALIZATION-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - content_change_from_renormalize
    - forbidden_files_detected
    - secret_or_env_risk
    - private_downstream_detail_needed
    - destructive_git_needed
```

## Задача

Нормализовать repository EOL policy: закрепить LF для текстовых source-типов в `.gitattributes` и выполнить scoped renormalize без содержательных правок документов.

## Контекст sequence

Внешний handoff-пакет называл эту работу `PR 0124`, но актуальный `docs/agent-system/engine-journal/INDEX.md` перед началом выполнения завершался на `0121`. По `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` следующий номер вычисляется как `last seq + 1`, а предсказанный номер из task-блока игнорируется без пропусков. Поэтому фактический journal seq этой задачи: `0122`.

## Acceptance criteria

- `.gitattributes` задает LF для Markdown, Python, YAML и JSON, а также binary rules для PNG/ZIP.
- `git add --renormalize .` не создает содержательных правок.
- Diff не содержит реального изменения Markdown/doc content из-за EOL.
- TASK/RESULT/INDEX созданы как seq `0122`.
- Generated file map и cloud mirrors согласованы после изменения `INDEX`.
- Проверки из `task_contract.checks.required` проходят.
- `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`, secrets и private downstream data не читаются и не меняются.

## Expected reviewer mode

Scoped technical safety review: reviewer подтверждает, что изменение является EOL-policy/journal/generated-parity PR без содержательных правок docs.

## Передача

Следующий: reviewer — scoped EOL-policy review.
