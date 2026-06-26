# TASK-0106 — METH-REVIEW-FEEDBACK-SCHEMA-01

execution_started_at: `2026-06-25T22:17:36.1440451+07:00`

## Режим

Роль: methodology-architect-01
Исполнитель: на усмотрение архитектора
Reasoning effort: средний
Режим: Agent, methodology docs/templates task
Branch: `work/methodology-architect-01/meth-review-feedback-schema-01`
Base: `developer`

## Цель

Снизить лишние review/fix-pass циклы в active work PR autoloop: закрепить структурированный reviewer feedback schema и engine fix-pass report, чтобы machine-verifiable blockers закрывались командами, а semantic/mixed blockers шли на минимальный re-review.

## Scope

Разрешённые изменения:

- `docs/agent-system/REVIEW_AUTOLOOP.md`
- `docs/agent-system/OPERATIONAL_FAST_LANE.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`
- `docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md`
- `docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/cloud/**` после regeneration
- journal artifacts `0106`

Запрещено:

- менять runtime/Docker/CI/branch protection;
- менять product/target repositories;
- читать `.env` или выводить secrets;
- реализовывать Python tooling/scripts;
- создавать release PR, merge или tag;
- переписывать append-only journal history.

## Требования

1. Ввести blocker IDs `B-01`, `B-02`, ...
2. Ввести blocker classes: `machine-verifiable`, `semantic`, `mixed`.
3. Требовать `verification_command` и `can_engine_fix_without_architect`.
4. Закрепить minimal re-review:
   - machine-only + passed checks + unchanged scope → machine-check closure без полного reviewer pass;
   - semantic/mixed → reviewer re-review по changed blocker scope;
   - full re-review только при scope drift/safety/failed checks/explicit request.
5. Закрепить own-PR verdict fallback: если GitHub не позволяет formal review, reviewer оставляет verdict comment в PR; это не blocker.
6. Обновить reviewer pass и engine fix-pass templates.
7. Обновить state/decision/backlog trace.
8. Регенерировать cloud bundle после изменения bundle-source и INDEX.

## Проверки

- `python docs/agent-system/tools/gen_file_map.py --check`
- `python docs/agent-system/tools/gen_cloud_bundle.py --check`
- `git diff --check origin/developer...HEAD`
- `git diff --name-only origin/developer...HEAD`
- `git diff --stat origin/developer...HEAD`
- `git status --short -uall`
- forbidden/sensitive scans без вывода secret values

## Передача

Следующий: reviewer — semantic scoped review PR; затем архитектор — human merge в `developer`.
