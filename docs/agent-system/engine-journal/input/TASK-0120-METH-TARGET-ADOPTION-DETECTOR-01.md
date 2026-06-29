# TASK для METH-TARGET-ADOPTION-DETECTOR-01

```yaml
task_contract:
  version: 1
  task_id: METH-TARGET-ADOPTION-DETECTOR-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-target-adoption-detector-01

  scope:
    allowed_files:
      - docs/agent-system/TARGET_ADOPTION_DETECTOR.md
      - docs/agent-system/ADOPTION_GUIDE.md
      - docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md
      - docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/templates/TASK_HEADER_COMMON.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/templates/ADOPTION_PROMPT.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/input/TASK-*-METH-TARGET-ADOPTION-DETECTOR-01.md
      - docs/agent-system/engine-journal/output/RESULT-*-METH-TARGET-ADOPTION-DETECTOR-01.md
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
      - verification/**
      - product repositories
      - real project files
      - private downstream data
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0120-METH-TARGET-ADOPTION-DETECTOR-01.md
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0120-METH-TARGET-ADOPTION-DETECTOR-01.md --json
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
    - destructive_git_needed
```

## Задача

Создать reusable detector policy/spec для выбора режима target adoption перед реальным применением methodology layer из stable source.

## Scope

Разрешены только methodology docs/templates/state/manifest/cloud/journal файлы из `task_contract.scope.allowed_files`.

Запрещено читать или менять реальные target implementation repositories, private downstream data, `.env`, runtime, Docker, CI, branch protection, release/tag/merge.

## Требуемый результат

- Создан `docs/agent-system/TARGET_ADOPTION_DETECTOR.md`.
- Detector описывает Required checks, Variant A/B/C, STOP conditions, safety rules и machine-readable recommendation format.
- Adoption docs/templates получают короткие ссылки на detector без полного переписывания.
- Manifest, file map и cloud bundle согласованы.
- Journal TASK/RESULT/INDEX обновлены.
- Target repositories не читались и не менялись.

## Передача

Следующий: reviewer - scoped methodology adoption-detector review.
