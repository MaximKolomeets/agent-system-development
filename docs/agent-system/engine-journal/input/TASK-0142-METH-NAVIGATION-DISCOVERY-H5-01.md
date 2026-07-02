# TASK для METH-NAVIGATION-DISCOVERY-H5-01

Задача для methodology-architect-01: METH-NAVIGATION-DISCOVERY-H5-01

```yaml
task_contract:
  version: 1
  task_id: METH-NAVIGATION-DISCOVERY-H5-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-5-navigation-discovery

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 013a31faa55c956968a82e651289246f644c827e
    reference_type: methodology_development
    checked_at: 2026-07-02T17:57:40.6787474+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-5-navigation-discovery
    base_commit: 013a31faa55c956968a82e651289246f644c827e
    checked_at: 2026-07-02T17:57:40.6787474+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_GUIDE.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/TARGET_REPOSITORY_ADOPTION_GUIDE.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0142-METH-NAVIGATION-DISCOVERY-H5-01.md
      - docs/agent-system/engine-journal/output/RESULT-0142-METH-NAVIGATION-DISCOVERY-H5-01.md
      - docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md
      - docs/agent-system/templates/ADOPTION_PROMPT.md
      - docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/tools/orchestrator_checklist.py
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
      - real passwords
      - private repository URLs
      - private downstream project names
      - client/customer data

  policies:
    journal: required
    cloud_regen: if_bundle_source_changed
    generated_checks: conditional
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    boundary_reconciliation: release_or_audit_only
    language: russian_first

  checks:
    required:
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0142-METH-NAVIGATION-DISCOVERY-H5-01.md
      - python -c "import ast, pathlib; paths = ['docs/agent-system/tools/orchestrator_checklist.py', 'docs/agent-system/tools/gen_cloud_bundle.py']; [ast.parse(pathlib.Path(path).read_text(encoding='utf-8')) for path in paths]; print('syntax: ok')"
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0142-METH-NAVIGATION-DISCOVERY-H5-01.md
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - destructive_git_needed
    - branch_protection_change_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-5/H5 меняет навигационные каноны, manifest inventory,
entrypoint discovery, generated bundle и добавляет tooling для orchestrator.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T17:57:40.6787474+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-5-navigation-discovery`.
- Base commit: `013a31faa55c956968a82e651289246f644c827e`.
- PR #310 state before start: merged at `2026-07-02T10:47:38Z`.
- Working tree before branch creation: clean.

## Цель

Выполнить PR-5/H5 из hardening-блока v1.5.2: усилить навигацию и discovery,
чтобы orchestrator/engine выбирали обязательные overlays по trigger, а
инвентарь файлов читали из `ADOPTION_TRANSFER_MANIFEST.yml`.

## Требуемые изменения

- Добавить таблицу `Mandatory overlays by trigger` в root `README.md` и
  `docs/agent-system/METHODOLOGY_MAP.md`.
- Добавить `docs/agent-system/METHODOLOGY_MAP.mermaid` как визуальную карту
  связей reading-list, manifest, orchestrator, engine, adoption, review и
  generated artifacts.
- Обновить `ENGINE_ENTRYPOINT.md`: discovery через
  `ADOPTION_TRANSFER_MANIFEST.yml`, без длинного ручного списка source files.
- Добавить `docs/agent-system/tools/orchestrator_checklist.py` как pre-send
  validator блока для исполнителя.
- Обновить adoption docs/templates так, чтобы они ссылались на manifest как
  discovery map.
- Зарегистрировать новые source/generated files в manifest и регенерировать
  `PROJECT_FILE_MAP.md` и `cloud/**`.

## Acceptance criteria

- `README.md` и `METHODOLOGY_MAP.md` содержат таблицу `Mandatory overlays by trigger`.
- `ENGINE_ENTRYPOINT.md` направляет discovery через `ADOPTION_TRANSFER_MANIFEST.yml`.
- `METHODOLOGY_MAP.mermaid` существует и описывает основные связи методологии.
- `orchestrator_checklist.py` запускается и валидирует self-contained task block.
- Adoption docs/templates используют manifest как discovery map.
- Manifest, file map и cloud bundle синхронизированы.
- RESULT/INDEX финализируются после PR creation.

## Финальный отчет

Финальный отчет должен быть на русском языке и содержать: PR URL, branch,
финальный head SHA, список измененных навигационных surfaces, выполненные
checks, generated artifacts, accounting fields, risks, Source Delta, context
handoff и блок «Передача».

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-5/H5; затем архитектор —
human merge; затем methodology-architect-01 — следующий hardening PR по
актуальному `BLOCK_METH_v1_5_2.md`.
