Задача для dev-implementer: METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01

Рекомендуемый режим исполнения:

Роль: dev-implementer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: задача изменяет канонические документы и требует воспроизводимых
проверок в отдельной task branch.
Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-30T07:35:38.6341809+02:00
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]:
actor_type: agent
time_source: measured
time_report_confidence: high

# TASK-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01

```yaml
task_contract:
  version: 2
  task_id: METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01
  role: dev-implementer-01
  mode: agent
  execution_mode: local_only
  reasoning_effort: high
  repository:
    full_name: MaximKolomeets/agent-system-development
    local_path: C:\neural\repos\agent-system-development
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-autonomous-terminal-execution-protocol-01
  methodology_reference:
    repository_full_name: MaximKolomeets/agent-system-development
    source_ref: origin/main
    stable_only: false
    source_commit: de3546ddfe1da4eca4f2145e281ff1288cfbc273
    reference_type: methodology_development
    checked_at: 2026-07-30T07:35:38.6341809+02:00
  methodology_development_base:
    base_branch: developer
    working_branch: work/dev-implementer-01/meth-autonomous-terminal-execution-protocol-01
    base_commit: 969364e88dca6a009adf2afe29b37a70c43ac324
    checked_at: 2026-07-30T07:35:38.6341809+02:00
  scope:
    allowed_files:
      - docs/agent-system/AUTONOMOUS_TERMINAL_EXECUTION_PROTOCOL.md
      - docs/agent-system/EXECUTION_CONTINUATION_POLICY.md
      - docs/agent-system/TASK_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
      - docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md
      - docs/agent-system/ENGINE_ENTRYPOINT.md
      - docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md
      - docs/agent-system/engine-journal/templates/ENGINE_TASK_FILE_TEMPLATE.md
      - docs/agent-system/engine-journal/templates/ENGINE_RESULT_FILE_TEMPLATE.md
      - docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
      - docs/agent-system/tools/gen_cloud_bundle.py
      - docs/agent-system/CURRENT_STATE.md
      - docs/agent-system/NEXT_STEPS.md
      - docs/agent-system/DECISION_LOG.md
      - docs/agent-system/engine-journal/input/TASK-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01.md
      - docs/agent-system/engine-journal/rationale/RATIONALE-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01.md
      - docs/agent-system/engine-journal/output/RESULT-0169-METH-AUTONOMOUS-TERMINAL-EXECUTION-PROTOCOL-01.md
      - docs/agent-system/engine-journal/INDEX.md
      - docs/agent-system/PROJECT_FILE_MAP.md
      - docs/agent-system/cloud/**
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
    review: scoped_semantic
    merge: human_only
    closure_pr: false
    post_merge_closure: not_required
    language: russian_first
  checks:
    required:
      - python -m unittest discover -s docs/agent-system/tools/tests -p test_*.py -v
      - python docs/agent-system/tools/validate_task_contract.py <task-file> --json
      - python docs/agent-system/tools/validate_journal_triplet.py --json
      - python docs/agent-system/tools/validate_policy_invariants.py
      - python docs/agent-system/tools/check_journal_append_only.py
      - python docs/agent-system/tools/gen_file_map.py --check
      - python docs/agent-system/tools/gen_cloud_bundle.py --check
      - python docs/agent-system/tools/check_task_ready.py --base origin/developer --json
  stop_conditions:
    - missing_required_prerequisite_without_safe_bypass
    - owner_architecture_decision_required
    - path_outside_adaptive_scope
    - destructive_git_protected_branch_secret_or_real_data_risk
    - unfixable_security_or_integrity_issue
    - declared_iteration_budget_exhausted
```

Номер sequence: 0169
Время начала выполнения (execution_started_at) [measured/engine]: 2026-07-30T07:35:38.6341809+02:00
actor_type: agent
role: dev-implementer-01
time_source: measured_engine_clock
time_report_confidence: high
raw_chain_of_thought_stored: no

## Цель

Внедрить единый канон автономного terminal execution: каждая substantive
задача завершается готовым к human review PR с evidence либо доказанным STOP,
а отдельный failed check сначала рассматривается как recoverable failure.

## Definition of Ready

- Repository root, origin и clean tree проверены до создания work branch.
- Branch создана от актуального `origin/developer`
  `969364e88dca6a009adf2afe29b37a70c43ac324`.
- Adaptive scope включает source canon, registry/order, manifest capacity,
  generated mirrors, journal и checks dependency closure.

## Acceptance criteria

- Новый canon определяет два terminal outcome, closed STOP taxonomy, decision
  fallback, statuses findings и terminal report evidence.
- Contracts/templates требуют adaptive scope envelope и отдельные budgets.
- Existing continuation safeguards остаются действующими и не конфликтуют с
  новым terminal-outcome canon.
- Manifest, canonical order, capacity и generated artifacts синхронизированы.
- Все обязательные Docker-first checks и readiness возвращают success/ready;
  создаётся один PR только в `developer`.

## Autonomous terminal execution

Terminal outcomes: `ready_for_human_review` или `stopped_human_required`.
Recoverable scoped failure исправляется в этой branch; STOP допускается только
по taxonomy task_contract и протоколу.

Adaptive scope envelope:

```text
source -> registry/order -> manifest -> capacity/limit -> generated mirrors -> checks
```

Iteration budgets:

- targeted check reruns: 3;
- full readiness runs: 3;
- CI fix-pass: 2;
- integration-stack attempts: 1.

## Ограничения

Не изменять `main` или `developer` напрямую, CI/runtime/Docker/release policy,
права, product scope или agent token requirements. Не выполнять merge, rebase,
reset, stash, clean, force-push, push branch вне task branch, не читать `.env`
и не использовать private/client data.

## Ожидаемый terminal report

RESULT и final report фиксируют branch/HEAD/PR, prerequisites, классификацию
changed files, decisions, checks/CI и source verdict, фактические budgets,
residual risks, unresolved review threads, отсутствие merge и точный next
action.
