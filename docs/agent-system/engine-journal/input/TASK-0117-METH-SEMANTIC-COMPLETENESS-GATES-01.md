# Задача для methodology-architect-01: METH-SEMANTIC-COMPLETENESS-GATES-01

```yaml
task_contract:
  version: 1
  task_id: METH-SEMANTIC-COMPLETENESS-GATES-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-semantic-completeness-gates-01
  scope:
    allowed_files:
      - docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md
      - docs/agent-system/JOURNAL_FINALIZATION_POLICY.md
      - docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/REVIEW_AUTOLOOP.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md
      - docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md
      - docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/input/TASK-0117-METH-SEMANTIC-COMPLETENESS-GATES-01.md
      - docs/agent-system/engine-journal/output/RESULT-0117-METH-SEMANTIC-COMPLETENESS-GATES-01.md
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
  policies:
    journal: required
    cloud_regen: required
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    language: russian_first
  checks:
    required:
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0117-METH-SEMANTIC-COMPLETENESS-GATES-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0117-METH-SEMANTIC-COMPLETENESS-GATES-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
  stop_conditions:
    - forbidden changed paths detected
    - private data or credentials detected
    - tests/tools/code/runtime scope drift outside allowed scope
    - generated parity drift remains
    - ready-gate prints matching values instead of counts, filenames and category
    - temporary smoke file remains in commit
```

## Цель

Объединить три backlog-кандидата в один scoped methodology hardening PR:

- `METH-DOWNSTREAM-FEEDBACK-COMPLETENESS-GATES-01`;
- `METH-JOURNAL-FINALIZATION-PHRASES-01`;
- `METH-ACCEPTANCE-SPEC-COMPLETENESS-PATTERN-01`.

`METH-DOWNSTREAM-FEEDBACK-LOOP-VERIFICATION-01` остаётся отдельной future task и не входит в этот PR.

## Scope

Создать reusable docs:

- `docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md`;
- `docs/agent-system/JOURNAL_FINALIZATION_POLICY.md`;
- `docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`.

Минимально расширить `check_task_ready.py`: changed TASK/RESULT files получают отдельную safe category для deferred finalization markers; human output и JSON не печатают matching values.

Обновить contracts/templates/state/manifest/cloud/file-map/journal так, чтобы future Engine tasks ссылались на semantic checklist, journal finalization policy и acceptance/spec mapping pattern.

## Out of scope

- full semantic parser;
- production generator;
- tests/fixtures/code/runtime;
- Docker/CI/branch protection;
- release/tag/version;
- target repositories;
- private downstream details.

## Semantic completeness

Перед PR проверить, что RESULT, PR body, state docs, new docs, manifest/cloud bundle и targeted smoke report не обещают scope шире фактического diff и выполненных checks.

## Передача

Следующий: reviewer — scoped semantic + lightweight ready-gate review текущего PR.
