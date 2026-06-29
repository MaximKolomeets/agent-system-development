# Задача для methodology-architect-01: METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01

```yaml
task_contract:
  version: 1
  task_id: METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-downstream-feedback-loop-sanitized-01
  scope:
    allowed_files:
      - docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md
      - docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md
      - docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md
      - docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md
      - docs/agent-system/JOURNAL_FINALIZATION_POLICY.md
      - docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/REVIEW_AUTOLOOP.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/engine-journal/input/TASK-0118-METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01.md
      - docs/agent-system/engine-journal/output/RESULT-0118-METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01.md
      - docs/agent-system/engine-journal/INDEX.md
    forbidden_files:
      - .env
      - .env.*
      - tests/**
      - runtime/**
      - dist/**
      - data/**
      - backups/**
      - exports/**
      - .venv/**
      - .github/**
      - product/runtime/CI/branch-protection
      - target repositories
      - private downstream data
      - real data
  policies:
    journal: required
    cloud_regen: required
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only
    language: russian_first
  checks:
    required:
      - git diff --check origin/developer...HEAD
      - git diff --name-only origin/developer...HEAD
      - git diff --stat origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0118-METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0118-METH-DOWNSTREAM-FEEDBACK-LOOP-SANITIZED-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall
  stop_conditions:
    - PR 277 not merged to developer
    - forbidden changed paths detected
    - target repository access required
    - private data or credentials detected
    - tests/fixtures/code/runtime scope drift
    - product runtime CI or branch protection changed
    - release tag or merge attempted
    - generated parity drift remains
    - sensitive output exposes protected content
```

## Цель

Описать reusable sanitized downstream feedback loop для methodology repository:

- создать `docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md`;
- создать `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`;
- связать loop с existing methodology feedback, semantic gates, journal finalization, acceptance/spec pattern, orchestrator contracts, task contract и review template;
- добавить новые source docs в manifest, PROJECT_FILE_MAP и cloud bundle;
- закрыть `METH-DOWNSTREAM-FEEDBACK-LOOP-VERIFICATION-01` как sanitized/reusable variant.

## Scope

Работа выполняется только в `agent-system-development`. Target repositories не читаются и не меняются.

Документы должны зафиксировать:

- downstream feedback не становится methodology automatically;
- target repository не является source of truth для reusable methodology;
- private/client/project details запрещены;
- feedback проходит sanitization checkpoint, classification и backlog grouping;
- reusable changes идут через `agent-system-development` и PR в `developer`;
- target repositories получают изменения только после `main`, release tag или published Source/cloud snapshot;
- dirty/open target work branches не являются blocker для methodology repository;
- ordinary post-merge closure PR не нужен;
- boundary reconciliation нужна только перед release/audit boundary, batch reconciliation или explicit architect request.

## Out of scope

- чтение или изменение target repositories;
- private downstream details;
- production generator;
- tests/fixtures/code/runtime;
- Docker/CI/branch protection;
- release PR, merge, tag;
- `.env`, credentials, tokens, protected access material, real data.

## Semantic completeness

Перед PR проверить, что RESULT, PR body, state docs, backlog, decision log, new docs, manifest/cloud bundle и file map согласованы с фактическим diff. PR body не должен утверждать target adoption или release. State docs должны фиксировать только reusable methodology docs и следующий возможный release boundary.

## Передача

Следующий: reviewer — scoped methodology semantic review текущего PR.
