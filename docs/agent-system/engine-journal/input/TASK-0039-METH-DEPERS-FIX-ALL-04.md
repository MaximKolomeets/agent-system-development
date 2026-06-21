# Задача для docs-maintainer-01: METH-DEPERS-FIX-ALL-04 (<agent-name> -> <роль> + README vendor)

## Режим

Роль: docs-maintainer.
Исполнитель: на усмотрение архитектора.
Reasoning effort: высокий.
branch-guard.

Batch-policy: открытые journal-записи не блокируют; closure не подмешивать.

## Цель

Убрать operational/source/template остатки `<agent-name>` и README vendor-actor literals,
не трогая history_state и append-only journal history.

## Scope

Discovery выполняется через:

```powershell
rg -l "<agent-name>" docs/agent-system README.md --glob '!engine-journal/**'
```

Исключены из scope как history_state/history:

- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/RELEASE_READINESS.md`
- `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md`
- `docs/agent-system/agents/**`
- `docs/agent-system/source/**`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/engine-journal/**`

## Allowed files

- `README.md`
- `docs/agent-system/ADOPTION_GUIDE.md`
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md`
- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`
- `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md`
- `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`
- `docs/agent-system/templates/ADOPTION_PROMPT.md`
- `docs/agent-system/templates/BACKLOG_TEMPLATE.md`
- `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md`
- `docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md`
- `docs/agent-system/templates/NEW_PROJECT_PROMPT.md`
- `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md`
- `docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md`
- `docs/agent-system/templates/ROADMAP_TEMPLATE.md`
- `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`
- `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` (inspection/possible alignment)
- `docs/agent-system/CODE_REVIEW_WORKFLOW.md` (judgment only if generic field)
- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/engine-journal/input/TASK-0039-METH-DEPERS-FIX-ALL-04.md`
- `docs/agent-system/engine-journal/output/RESULT-0039-METH-DEPERS-FIX-ALL-04.md`

## Проверки

- operational `rg -i "<agent-name>"` -> 0.
- operational `rg -i "chatgpt|codex|claude code"` -> 0.
- history_state не входит в diff.
- `python docs/agent-system/tools/gen_file_map.py --check` -> exit 0.
- `git diff --check` -> clean.
- branch guard: HEAD == `work/docs-maintainer-01/depers-fix-all-04`.

## Передача

Следующий: reviewer — review (operational `<agent-name>`/vendor -> 0; history не тронута; `--check` зелёный); затем архитектор — merge; затем engine — FIX-2 (orchestrator-context handoff); journal closure — batch перед release.
