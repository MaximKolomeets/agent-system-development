# Задача для methodology-architect-01: METH-RELEASE-GATE-READY-MODE-01

```yaml
task_contract:
  version: 1
  task_id: METH-RELEASE-GATE-READY-MODE-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-release-gate-ready-mode-01
  scope:
    allowed_files:
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/JOURNAL_FINALIZATION_POLICY.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/output/RESULT-0116-METH-DOWNSTREAM-FEEDBACK-COMPLETENESS-GATES-BACKLOG-01.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0119-METH-RELEASE-GATE-READY-MODE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0119-METH-RELEASE-GATE-READY-MODE-01.md
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - target repositories
      - verification/**
      - product repositories
      - runtime/Docker/CI
      - branch protection config
  policies:
    journal: required
    cloud_regen: required
    generated_checks: conditional
    review: scoped_technical_safety
    merge: human_only
    closure_pr: false
    language: russian_first
    post_merge_closure: not_required
  checks:
    required:
      - git diff --check origin/developer...HEAD
      - git diff --name-only origin/developer...HEAD
      - git diff --stat origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0119-METH-RELEASE-GATE-READY-MODE-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0119-METH-RELEASE-GATE-READY-MODE-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary
      - python docs/agent-system/tools/check_task_ready.py --base origin/main --release-boundary --json
      - git status --short -uall
  stop_conditions:
    - forbidden changed paths detected
    - target repository access required
    - private data or credentials detected
    - product runtime CI or branch protection changed
    - release tag or merge attempted
    - generated parity drift remains
    - sensitive output exposes protected content
```

## Цель

Добавить явный release-boundary режим для `check_task_ready.py`, чтобы release payload `developer -> origin/main` можно было проверять без ложного work-branch blocker, но без отключения safety scans.

## Требования

- Default режим `check_task_ready.py` не ослаблять.
- `--release-boundary` разрешить только для `current_branch = developer` и `base = origin/main`.
- В release-boundary режиме снимать только blockers про protected branch и outside work branch.
- Forbidden paths, sensitive filenames, strict added-line secret scan, finalization marker scan, diff checks и generated checks оставить активными.
- `RESULT-0116` перевести на finalized source/policy wording без незаполненного `head_sha`.
- Release PR, merge, tag, target repositories, runtime, Docker, CI и branch protection не выполнять.

## Передача

Следующий: reviewer — scoped tooling/release-gate review текущего PR.
