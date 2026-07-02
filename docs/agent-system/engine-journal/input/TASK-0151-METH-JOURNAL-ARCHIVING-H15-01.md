# TASK для METH-JOURNAL-ARCHIVING-H15-01

Задача для methodology-architect-01: METH-JOURNAL-ARCHIVING-H15-01

```yaml
task_contract:
  version: 1
  task_id: METH-JOURNAL-ARCHIVING-H15-01
  role: methodology-architect-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high

  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-14-journal-archiving

  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    source_ref: origin/developer
    stable_only: false
    source_commit: 25b60ad8d41f42fb3e39daebb0be3757605acfc3
    reference_type: methodology_development
    checked_at: 2026-07-02T22:52:17.9172844+07:00

  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-architect-01/meth-v1-5-2-pr-14-journal-archiving
    base_commit: 25b60ad8d41f42fb3e39daebb0be3757605acfc3
    checked_at: 2026-07-02T22:52:17.9172844+07:00

  scope:
    allowed_files:
      - README.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
      - docs/agent-system/JOURNAL_ARCHIVING_POLICY.md
      - docs/agent-system/METHODOLOGY_MAP.md
      - docs/agent-system/METHODOLOGY_MAP.mermaid
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/README.md
      - docs/agent-system/engine-journal/README.md
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/tools/gen_file_map.py
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/input/TASK-0151-METH-JOURNAL-ARCHIVING-H15-01.md
      - docs/agent-system/engine-journal/output/RESULT-0151-METH-JOURNAL-ARCHIVING-H15-01.md
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
      - python docs/agent-system/tools/validate_task_contract.py docs/agent-system/engine-journal/input/TASK-0151-METH-JOURNAL-ARCHIVING-H15-01.md
      - python docs/agent-system/tools/orchestrator_checklist.py docs/agent-system/engine-journal/input/TASK-0151-METH-JOURNAL-ARCHIVING-H15-01.md
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/russian_first_lint.py --base origin/developer
      - python docs/agent-system/tools/generated_eol_guard.py --base origin/developer
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - git diff --check origin/developer...HEAD
      - python -m py_compile docs/agent-system/tools/gen_file_map.py docs/agent-system/tools/gen_cloud_bundle.py
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer

  stop_conditions:
    - dirty_tree_before_start
    - current_branch_is_main_or_developer_with_changes
    - changed_file_outside_allowlist
    - forbidden_path_changed
    - secret_or_env_risk
    - actual_archive_move_requested_before_release
    - release_tag_or_epoch_boundary_unknown_for_archive_move
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
Почему: PR-14/H15 меняет public methodology docs и локальные generators, но не
требует target repositories, private consumers, CI/CD, branch protection,
release tag creation или переноса старых archive files.

Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-02T22:52:17.9172844+07:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: not_applicable
actor_type: agent
role: methodology-architect-01
time_source: mixed
time_report_confidence: medium

## Verified baseline

- Repository: `MaximKolomeets/agent-system-development`.
- Local path: `C:\neural\repos\agent-system-development`.
- Base branch: `developer`.
- Working branch: `work/methodology-architect-01/meth-v1-5-2-pr-14-journal-archiving`.
- Base commit: `25b60ad8d41f42fb3e39daebb0be3757605acfc3`.
- PR #319 state before start: merged at `2026-07-02T15:47:58Z`; merge commit `25b60ad8d41f42fb3e39daebb0be3757605acfc3`.
- Local `developer` matched `origin/developer` before branch creation.

## Scope

Выполнить PR-14/H15 из `BLOCK_METH_v1_5_2.md`:

1. Добавить `docs/agent-system/JOURNAL_ARCHIVING_POLICY.md`.
2. Ввести понятие `Journal Epoch` на release `vX.Y.Z`.
3. Описать post-release archive flow: старые finalized `RESULT` перемещаются в
   `docs/agent-system/engine-journal/archive/vX.Y.Z/`, а активный `INDEX.md`
   оставляет summary и ссылки на archive.
4. Не переносить старые RESULT в рамках этого PR: фактический archive move
   выполняется отдельным post-release archive PR, когда release boundary известен.
5. Обновить `ENGINE_JOURNAL_CONTRACT.md`, manifest, navigation и generators,
   чтобы archive не попадал в context bundle.

## Constraints

- Не читать `.env`; не менять `.env`, `.venv`, `data/`, `runtime/`, `dist/`,
  `backups/`, `exports/`.
- Не переносить существующие RESULT 0001-0150 в этом PR.
- Не создавать release tag, release PR, sync PR или merge в `main`.
- Archive files считаются public journal history; не добавлять private data.
- Archive не должен входить в `orchestrator_context_bundle` или `cloud/**`.

## Acceptance criteria

- `JOURNAL_ARCHIVING_POLICY.md` описывает Journal Epoch, archive path,
  active INDEX summary и STOP-условия.
- `ENGINE_JOURNAL_CONTRACT.md` ссылается на archiving policy и объясняет
  controlled exception к активной journal surface.
- Manifest содержит source policy и отдельную archive category, excluded from
  context bundle.
- `gen_file_map.py` знает category `journal_archive`.
- `gen_cloud_bundle.py` запрещает archive paths в bundle validation и README
  явно говорит, что archive не загружается.
- README/METHODOLOGY_MAP/docs README связаны с новым policy.
- TASK/RESULT/INDEX Russian-first и содержат time/cost accounting fields.

## Source Delta

- Methodology source inventory меняется: добавляется
  `JOURNAL_ARCHIVING_POLICY.md`.
- Generated/source tooling меняется: `gen_file_map.py` и `gen_cloud_bundle.py`
  учитывают `journal_archive` как не-bundle surface.
- Source-reminder: после release/publication обновить Source-снапшот у
  зарегистрированных потребителей; до release downstream stable source не
  меняется.

## Требования к final report

Финальный отчет должен быть на русском языке и содержать:

- PR URL, branch и final head SHA;
- список измененных policy/contract/manifest/tool/navigation/generated/journal
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

Следующий: methodology-reviewer-01 — scoped review PR-14/H15 после открытия PR.
