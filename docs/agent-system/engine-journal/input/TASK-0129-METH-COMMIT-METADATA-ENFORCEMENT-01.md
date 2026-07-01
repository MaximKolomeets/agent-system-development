# TASK для METH-COMMIT-METADATA-ENFORCEMENT-01

```yaml
task_contract:
  version: 1
  task_id: METH-COMMIT-METADATA-ENFORCEMENT-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-commit-metadata-enforcement-01

  scope:
    allowed_files:
      - docs/agent-system/tools/validate_commit_message.py
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/MANUAL_REVIEW_CHECKLIST.md
      - docs/agent-system/CODE_REVIEW_WORKFLOW.md
      - docs/agent-system/CI_POLICY.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/02_ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/cloud/03_TASK_HEADER_COMMON.md
      - docs/agent-system/cloud/05_ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
      - docs/agent-system/cloud/10_PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md
      - docs/agent-system/engine-journal/input/TASK-0129-METH-COMMIT-METADATA-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/output/RESULT-0129-METH-COMMIT-METADATA-ENFORCEMENT-01.md
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
      - git diff --check origin/developer...HEAD
      - python docs/agent-system/tools/validate_commit_message.py --base origin/developer
      - python docs/agent-system/tools/validate_commit_message.py --message-text "<positive-message>"
      - python docs/agent-system/tools/validate_commit_message.py --message-text "<negative-message>"
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0129-METH-COMMIT-METADATA-ENFORCEMENT-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0129-METH-COMMIT-METADATA-ENFORCEMENT-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - need_heavy_commit_lint_framework
    - need_to_rewrite_merged_history
    - need_to_change_product_runtime_or_ci_workflow
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Внедрить surfacing и enforcement формата commit message по `LANGUAGE_POLICY`:

- добавить `docs/agent-system/tools/validate_commit_message.py`;
- подключить validator в `docs/agent-system/tools/check_task_ready.py`;
- добавить пункт проверки в `ORCHESTRATOR_RESPONSE_STANDARD.md`,
  `templates/TASK_HEADER_COMMON.md`, `MANUAL_REVIEW_CHECKLIST.md` и
  `CODE_REVIEW_WORKFLOW.md`;
- обновить `CI_POLICY.md` и `ENGINE_JOURNAL_CONTRACT.md`;
- зарегистрировать tool в `ADOPTION_TRANSFER_MANIFEST.yml`, обновить
  `PROJECT_FILE_MAP.md` и generated cloud mirrors.

## Non-goals

- Не переписывать merged history.
- Не менять сам канон `LANGUAGE_POLICY`.
- Не добавлять тяжелый commit-lint framework.
- Не менять product/runtime.
- Не менять GitHub Actions workflow в этом PR.

## Контекст sequence

Актуальный `docs/agent-system/engine-journal/INDEX.md` после governance patterns
завершается на `0128`. По правилу `INDEX last+1` фактический journal seq этой
задачи: `0129`.

## Acceptance criteria

- Surfacing-пункт присутствует в четырех указанных документах.
- `validate_commit_message.py` проверяет commits в диапазоне `origin/developer..HEAD`.
- Validator ловит негативные примеры: нет scope, английский текст после `:`,
  тело без пустой строки перед body.
- Validator пропускает корректный Russian-first commit message.
- `check_task_ready.py` запускает validator как обязательный read-only gate.
- `CI_POLICY.md` фиксирует check name `ci/commit-message` как CI-facing policy.
- `ENGINE_JOURNAL_CONTRACT.md` требует фиксировать нарушение commit metadata в
  RESULT, если оно не исправлено безопасно до push.
- Merged commits не переписываются.

## Expected reviewer mode

Scoped review: reviewer проверяет surfacing, enforcement, dogfood на собственном
commit этой задачи, safety read-only behavior validator и generated parity.

## Передача

Следующий: reviewer — scoped commit metadata enforcement review.
