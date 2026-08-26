# TASK-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01

Задача для methodology-maintainer: METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01

Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Hybrid
Режим: Agent
Почему: требуется превратить проверенные downstream-паттерны в нейтральные,
проверяемые и безопасные reusable skills без переноса приватных фактов.
execution_started_at: 2026-08-25T19:45:00+02:00
orchestration_time_reported: not_available
actor_type: agent
role: methodology-maintainer
time_source: measured
time_report_confidence: high

```yaml
task_contract:
  version: 2
  task_id: METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01
  role: methodology-maintainer
  mode: agent
  execution_mode: hybrid
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: /workspace/agent-system-development
    base_branch: developer
    working_branch: work/methodology-maintainer-01/reusable-remote-integration-skills
  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: 59e645944697eac565d121e97d2dfa2ff3e9d99b
    source_tag: v1.5.5
    reference_type: methodology_development
    checked_at: 2026-08-25T19:45:00+02:00
  methodology_development_base:
    base_branch: developer
    working_branch: work/methodology-maintainer-01/reusable-remote-integration-skills
    base_commit: 9a23a8efebc9c41df13843a543afb73bd6bd6392
    checked_at: 2026-08-25T19:45:00+02:00
  scope:
    allowed_files:
      - README.md
      - skills/**
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/engine-journal/SEQUENCE_RESERVATIONS.json
      - docs/agent-system/engine-journal/input/TASK-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01.md
      - docs/agent-system/engine-journal/rationale/RATIONALE-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01.md
      - docs/agent-system/engine-journal/output/RESULT-0180-METH-PORTABLE-REMOTE-INTEGRATION-SKILLS-01.md
    forbidden_files:
      - .env
      - .env.*
      - data/**
      - runtime/**
      - dist/**
      - backups/**
      - exports/**
  policies:
    journal: required
    rationale: required
    cloud_regen: required
    generated_checks: required
    review: scoped_technical_safety
    merge: human_only
    language: russian_first
  checks:
    required:
      - skill quick validation for both skills
      - offline tests for the scoped Vault MCP template
      - positive and negative plan validation
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
      - GitHub CI on exact PR head
  stop_conditions:
    - provider_snapshot_unavailable
    - sequence_0180_ownership_conflict
    - private_project_identifier_detected
    - secret_or_credential_detected
    - skill_validation_failed
    - changed_file_outside_allowlist
```

## Цель

Создать два переносимых skill-пакета: безопасный outbound reverse SSH relay через
промежуточный VPS и project-scoped MCP для одной папки Яндекс.Диска.

## Acceptance criteria

- каждый skill имеет полный `SKILL.md`, UI metadata, references и fail-closed validator;
- новый relay воспроизводится из generic Docker/VPS templates без project secrets;
- Vault MCP разворачивается из проверенного generic Docker template;
- явно зафиксировано, что app password Яндекса не является folder-level ACL;
- Vault и RAW имеют разные lifecycle и storage pattern;
- отсутствуют private downstream identifiers, credentials и runtime evidence;
- Issue: https://github.com/MaximKolomeets/agent-system-development/issues/385

## Передача

Следующий: methodology reviewer — проверить security boundaries, переносимость и
отсутствие приватных данных в PR #386.
