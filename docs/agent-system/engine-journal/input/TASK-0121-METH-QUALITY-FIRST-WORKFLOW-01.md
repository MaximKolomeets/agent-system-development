# TASK для METH-QUALITY-FIRST-WORKFLOW-01

```yaml
task_contract:
  version: 1
  task_id: METH-QUALITY-FIRST-WORKFLOW-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-quality-first-workflow-01

  scope:
    allowed_files:
      - docs/agent-system/QUALITY_FIRST_WORKFLOW.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/REVIEW_AUTOLOOP.md
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md
      - docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md
      - docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/input/TASK-*-METH-QUALITY-FIRST-WORKFLOW-01.md
      - docs/agent-system/engine-journal/output/RESULT-*-METH-QUALITY-FIRST-WORKFLOW-01.md
      - docs/agent-system/engine-journal/INDEX.md
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
      - target repositories
      - product repositories
      - runtime/Docker/CI
      - branch protection config

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
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0121-METH-QUALITY-FIRST-WORKFLOW-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0121-METH-QUALITY-FIRST-WORKFLOW-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - target_repository_access_needed
    - private_downstream_detail_needed
    - secret_or_env_risk
    - release_pr_merge_or_tag_needed
    - destructive_git_needed
```

## Задача

Создать reusable quality-first workflow для новых file-changing задач и PR.

## Acceptance criteria

PR можно открывать только если:

- создан `docs/agent-system/QUALITY_FIRST_WORKFLOW.md`;
- Definition of Ready, acceptance criteria, self-review before PR, PR body quality, STOP-or-ACT, decision cache и blocker-ID fix-pass описаны как обязательные правила;
- существующие docs/templates получили только короткие ссылки на workflow;
- manifest, file map и cloud bundle согласованы;
- TASK/RESULT/INDEX seq `0121` созданы;
- target repositories не читались и не менялись;
- existing release PR #283 не мержится и новый release PR не открывается.

## Expected reviewer mode

Scoped quality workflow review: reviewer проверяет обязательность quality-first правил, отсутствие scope drift, safety, generated parity и то, что workflow снижает fix-pass/re-review noise до PR.

## Передача

Следующий: reviewer - scoped quality-first workflow review.
