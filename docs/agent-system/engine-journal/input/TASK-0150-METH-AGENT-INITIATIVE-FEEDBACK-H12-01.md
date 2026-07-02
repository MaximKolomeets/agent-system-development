# TASK для METH-AGENT-INITIATIVE-FEEDBACK-H12-01

Задача для methodology-architect-01: METH-AGENT-INITIATIVE-FEEDBACK-H12-01

```yaml
task_contract:
  version: 1
  task_id: METH-AGENT-INITIATIVE-FEEDBACK-H12-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-13-agent-initiative-feedback

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 9d74c9d9c329d27ba886915d7d63888c38603c46
    reference_type: methodology_development
    checked_at: 2026-07-02T22:27:49.3632389+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-13-agent-initiative-feedback
    base_commit: 9d74c9d9c329d27ba886915d7d63888c38603c46
    checked_at: 2026-07-02T22:27:49.3632389+07:00

  scope:
    allowed_files:
      - AGENTS.md
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/AGENT_INITIATIVE_PROTOCOL.md
      - docs/agent-system/BACKLOG.md
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/ROLE_MODEL.md
      - docs/agent-system/engine-journal/templates/ENGINE_RESULT_FILE_TEMPLATE.md
      - docs/agent-system/templates/AGENT_PROPOSAL_TEMPLATE.md
      - docs/agent-system/tools/check_task_ready.py
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0150-METH-AGENT-INITIATIVE-FEEDBACK-H12-01.md
      - docs/agent-system/engine-journal/output/RESULT-0150-METH-AGENT-INITIATIVE-FEEDBACK-H12-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0150-METH-AGENT-INITIATIVE-FEEDBACK-H12-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0150-METH-AGENT-INITIATIVE-FEEDBACK-H12-01.md
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - python -m py_compile docs/agent-system/tools/check_task_ready.py
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - semantic_invariant_requires_human_decision
    - target_repository_access_needed
    - private_consumer_identity_needed
    - destructive_git_needed
    - branch_protection_change_needed
    - direct_main_push_or_tag_needed
```

## Рекомендуемый режим исполнения

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: PR-13/H12 меняет public methodology docs, RESULT template и локальный
readiness gate; доступ к target repositories, private consumers, CI/CD,
branch protection или secrets не нужен.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T22:27:49.3632389+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-13-agent-initiative-feedback`.
- Base commit: `9d74c9d9c329d27ba886915d7d63888c38603c46`.
- PR #318 state before start: merged at `2026-07-02T15:23:09Z`; merge commit `9d74c9d9c329d27ba886915d7d63888c38603c46`.
- Local `developer` matched `origin/developer` before branch creation.

## Scope

Выполнить PR-13/H12 из `BLOCK_METH_v1_5_2.md`:

1. Добавить `docs/agent-system/AGENT_INITIATIVE_PROTOCOL.md`.
2. Добавить `docs/agent-system/templates/AGENT_PROPOSAL_TEMPLATE.md`.
3. Добавить обязательный раздел `## Unprompted Project Proposals` в
   `ENGINE_RESULT_FILE_TEMPLATE.md`.
4. Закрепить обязательный блок `Methodology feedback` в AGENTS/RESULT contract.
5. Обновить `ROLE_MODEL.md`: право и обязанность агента фиксировать инициативные
   предложения, особенно для reviewer roles, без самовольного расширения scope.
6. Связать предложения с intake в `BACKLOG.md`.
7. Обновить navigation/manifest/generated artifacts.

## Constraints

- Не читать `.env`; не менять `.env`, `.venv`, `data/`, `runtime/`, `dist/`,
  `backups/`, `exports/`.
- Не добавлять реальные private consumers, private repository names,
  client/customer data или credentials.
- Не выполнять merge/tag/publish/sync; эти действия остаются human-only.
- Инициативные предложения не должны становиться file changes внутри текущей
  задачи без явного scope.
- Reviewer roles не назначают execution task напрямую: proposals идут через
  architect/orchestrator triage и `BACKLOG.md`.
- `Methodology feedback` и `Unprompted Project Proposals` должны быть
  Russian-first и public-safe.

## Acceptance criteria

- `AGENT_INITIATIVE_PROTOCOL.md` описывает канал: заметил проблему, оформил
  proposal, отправил в backlog/MIR triage, не реализовал без отдельной задачи.
- `AGENT_PROPOSAL_TEMPLATE.md` задает reusable формат предложения.
- RESULT template и journal contract требуют `## Methodology feedback` и
  `## Unprompted Project Proposals`; пустое значение фиксируется как `нет`.
- `ROLE_MODEL.md` явно закрепляет право/обязанность proposals для всех ролей и
  усиленную обязанность reviewer roles.
- `BACKLOG.md` описывает intake инициативных предложений.
- `check_task_ready.py` блокирует новый RESULT без обязательных feedback/proposal
  sections.
- Manifest/source map/cloud bundle синхронизированы.
- TASK/RESULT/INDEX Russian-first и содержат time/cost accounting fields.

## Source Delta

- Methodology source inventory меняется: добавляются
  `AGENT_INITIATIVE_PROTOCOL.md` и `templates/AGENT_PROPOSAL_TEMPLATE.md`.
- Journal/result contract меняется: новые RESULT требуют `## Methodology feedback`
  и `## Unprompted Project Proposals`.
- Source-reminder: после release/publication обновить Source-снапшот у
  зарегистрированных потребителей; до release downstream stable source не
  меняется.

## Требования к final report

Финальный отчет должен быть на русском языке и содержать:

- PR URL, branch и final head SHA;
- список измененных protocol/template/role/backlog/navigation/generated/journal
  artifacts;
- результаты `validate_task_contract.py`, `orchestrator_checklist.py`,
  `validate_policy_invariants.py`, `russian_first_lint.py`,
  `generated_eol_guard.py`, `gen_file_map.py --check`,
  `gen_cloud_bundle.py --check`, `git diff --check origin/developer...HEAD`,
  `py_compile` и `check_task_ready.py`;
- статус GitHub checks, если PR создан;
- блок `Локальные действия после PR/merge`;
- блок `Methodology feedback`;
- блок `Unprompted Project Proposals`;
- блок `Передача`;
- Source-reminder: обновить Source-снапшот у зарегистрированных потребителей
  после release/publication новой методологии; до release downstream stable
  source не меняется.

## Передача

Следующий: methodology-reviewer-01 — scoped review PR-13/H12 после открытия PR.
