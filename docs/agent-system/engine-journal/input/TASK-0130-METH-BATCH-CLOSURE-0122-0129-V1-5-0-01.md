# TASK для METH-BATCH-CLOSURE-0122-0129-V1-5-0-01

```yaml
task_contract:
  version: 1
  task_id: METH-BATCH-CLOSURE-0122-0129-V1-5-0-01
  role: docs-maintainer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: medium

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/docs-maintainer-01/batch-closure-0122-0129-v1-5-0-01

  scope:
    allowed_files:
      - docs/agent-system/engine-journal/output/RESULT-0122-METH-EOL-NORMALIZATION-01.md
      - docs/agent-system/engine-journal/output/RESULT-0123-METH-XREF-AND-READINGLIST-HYGIENE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0124-METH-NAVIGATION-INDEX-01.md
      - docs/agent-system/engine-journal/output/RESULT-0125-METH-CONTROL-MATRIX-PATTERN-01.md
      - docs/agent-system/engine-journal/output/RESULT-0126-METH-EXTERNAL-REVIEW-LEDGER-01.md
      - docs/agent-system/engine-journal/output/RESULT-0127-METH-THREAT-MODEL-TEMPLATE-01.md
      - docs/agent-system/engine-journal/output/RESULT-0128-METH-GOVERNANCE-PATTERNS-01.md
      - docs/agent-system/engine-journal/output/RESULT-0129-METH-COMMIT-METADATA-ENFORCEMENT-01.md
      - docs/agent-system/engine-journal/input/TASK-0130-METH-BATCH-CLOSURE-0122-0129-V1-5-0-01.md
      - docs/agent-system/engine-journal/output/RESULT-0130-METH-BATCH-CLOSURE-0122-0129-V1-5-0-01.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0130-METH-BATCH-CLOSURE-0122-0129-V1-5-0-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0130-METH-BATCH-CLOSURE-0122-0129-V1-5-0-01.md --json
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git status --short -uall

  stop_conditions:
    - dirty_tree_before_start
    - changed_file_outside_allowlist
    - any_pr_in_closure_set_not_merged
    - stale_final_status_in_closure_set
    - unresolved_release_base_tag_decision_for_release_prep
    - need_to_rewrite_merged_history
    - need_to_change_product_runtime_or_ci_workflow
    - forbidden_files_detected
    - private_data_or_secret_risk
    - destructive_git_needed
```

## Задача

Закрыть перед release boundary v1.5.0 merged-but-unclosed journal entries
`0122`-`0129`: добавить factual closure-stamp в RESULT, перевести строки
`INDEX.md` в closed status и создать собственную terminal-fold запись `0130`.

## Предусловия

- `developer` синхронизирован с `origin/developer` на
  `b25a9fd953f788fb5c0a1eb9b35ab4469c88c4ff`.
- PR #286-#293 подтверждены через `gh pr view` как `MERGED`.
- Latest tag preflight выявил `v1.4.1`, а исходное релизное задание ожидало
  `v1.4.0`; release-prep не начинается до решения архитектора по base tag.

## Non-goals

- Не начинать release-prep PR.
- Не менять `RELEASE_READINESS.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`.
- Не создавать release PR `developer -> main`.
- Не мержить PR, не пушить `main`, не создавать tag и GitHub Release.
- Не переписывать merged history и не менять содержательные каноны.

## Acceptance criteria

- RESULT 0122-0129 имеют `status: closed; PR #... merged; facts in closure stamp`.
- RESULT 0122-0129 содержат merge facts: PR URL, state, head branch, reviewed head SHA,
  `merged_at`, merge commit и `gh pr view` как source.
- INDEX rows 0122-0129 имеют status `closed; PR #... merged; facts in RESULT`.
- Собственная запись 0130 является lifecycle-only terminal fold.
- `cloud/07_ENGINE_JOURNAL_INDEX.md` синхронизирован с `INDEX.md`.
- Release-prep явно оставлен за пределами этой задачи до merge batch-closure PR и
  решения по фактическому latest tag.

## Передача

Следующий: docs-maintainer-01 — выполнить batch-closure, открыть PR в `developer`,
не мержить.
