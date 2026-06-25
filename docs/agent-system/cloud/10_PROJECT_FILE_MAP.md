# PROJECT_FILE_MAP

AUTO-GENERATED — не править руками; регенерировать через `python docs/agent-system/tools/gen_file_map.py`.

## Контракт

- Источник истины: `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`.
- Карта является производной repo-local view и не заменяет manifest.
- Parity-check: `python docs/agent-system/tools/gen_file_map.py --check`.
- `--check` сравнивает закоммиченную карту с регенерированной и проверяет наличие concrete source/template/generated files.

## source

Authoritative methodology source files: живые reusable/canonical/operational документы methodology repository. Все пути в этой категории должны существовать в source checkout.

| path | description from manifest |
| --- | --- |
| `AGENTS.md` |  |
| `README.md` |  |
| `docs/agent-system/ADOPTION_GUIDE.md` |  |
| `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` |  |
| `docs/agent-system/BRANCH_POLICY.md` |  |
| `docs/agent-system/CI_POLICY.md` |  |
| `docs/agent-system/CODE_REVIEW_WORKFLOW.md` |  |
| `docs/agent-system/CROSS_PROJECT_CONSOLIDATION_CONTRACT.md` |  |
| `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md` |  |
| `docs/agent-system/ENGINE_ENTRYPOINT.md` |  |
| `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` |  |
| `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md` |  |
| `docs/agent-system/FILE_COMMENTING_STANDARD.md` |  |
| `docs/agent-system/tools/check_task_ready.py` |  |
| `docs/agent-system/tools/gen_cloud_bundle.py` |  |
| `docs/agent-system/tools/gen_file_map.py` |  |
| `docs/agent-system/tools/generated_eol_guard.py` |  |
| `docs/agent-system/tools/validate_task_contract.py` |  |
| `docs/agent-system/GITHUB_RULESETS.md` |  |
| `docs/agent-system/GITHUB_TOKEN_POLICY.md` |  |
| `docs/agent-system/LANGUAGE_POLICY.md` |  |
| `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md` |  |
| `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md` |  |
| `docs/agent-system/NEW_PROJECT_ONBOARDING_GUIDE.md` |  |
| `docs/agent-system/OPERATIONAL_FAST_LANE.md` |  |
| `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` |  |
| `docs/agent-system/ORCHESTRATOR_PROJECT_OPERATING_LAYER.md` |  |
| `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md` |  |
| `docs/agent-system/PR_WORKFLOW.md` |  |
| `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md` |  |
| `docs/agent-system/PUBLICATION_POLICY.md` |  |
| `docs/agent-system/README.md` |  |
| `docs/agent-system/REVIEW_AUTOLOOP.md` |  |
| `docs/agent-system/ROLE_MODEL.md` |  |
| `docs/agent-system/SECURITY_POLICY.md` |  |
| `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md` |  |
| `docs/agent-system/TASK_CONTRACT.md` |  |
| `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md` |  |
| `docs/agent-system/WORKFLOW.md` |  |
| `docs/agent-system/WORKTREE_GUIDE.md` |  |

## template

Reusable source templates from methodology repository. Шаблоны существуют в source checkout и могут использоваться для materialization/adaptation target files.

| path | description from manifest |
| --- | --- |
| `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/ADOPTION_PROMPT.md` |  |
| `docs/agent-system/templates/AGENT_REPORT_TEMPLATE.md` |  |
| `docs/agent-system/templates/AGENT_RESEARCH_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/BACKLOG_TEMPLATE.md` |  |
| `docs/agent-system/templates/BATCH_CLOSURE_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/CLOSURE_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md` |  |
| `docs/agent-system/templates/CODE_REVIEW_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/DECISION_TEMPLATE.md` |  |
| `docs/agent-system/templates/DEVELOPMENT_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md` |  |
| `docs/agent-system/templates/NEW_PROJECT_CHECKLIST.md` |  |
| `docs/agent-system/templates/NEW_PROJECT_HANDOFF_TEMPLATE.md` |  |
| `docs/agent-system/templates/NEW_PROJECT_PROMPT.md` |  |
| `docs/agent-system/templates/NEW_REPOSITORY_STRUCTURE_TEMPLATE.md` |  |
| `docs/agent-system/templates/ORCHESTRATOR_RESPONSE_TEMPLATE.md` |  |
| `docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md` |  |
| `docs/agent-system/templates/PROJECT_DASHBOARD_TEMPLATE.md` |  |
| `docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md` |  |
| `docs/agent-system/templates/PROJECT_PROFILE_TEMPLATE.md` |  |
| `docs/agent-system/templates/REVIEW_AUTOLOOP_ENGINE_FIX_PASS_TEMPLATE.md` |  |
| `docs/agent-system/templates/REVIEW_AUTOLOOP_REVIEWER_PASS_TEMPLATE.md` |  |
| `docs/agent-system/templates/ROADMAP_TEMPLATE.md` |  |
| `docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md` |  |
| `docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` |  |
| `docs/agent-system/templates/TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE.md` |  |
| `docs/agent-system/templates/TASK_HEADER_COMMON.md` |  |

## target_generated

Target files generated or written from source/templates. Эти пути НЕ являются source files methodology repository; source parity не должна ожидать их наличие в source checkout.

| path | description from manifest |
| --- | --- |
| `PROJECT_CONSTITUTION.md` |  |
| `PROJECT_DASHBOARD.md` |  |
| `ROADMAP.md` |  |
| `RUNBOOK.md` |  |
| `DECISIONS.md` |  |
| `docs/agent-system/PROJECT_GUARDRAILS.md` |  |
| `docs/agent-system/ENGINE_REGISTRY.md` |  |
| `docs/agent-system/ADOPTION_AUDIT.md` |  |

## history_state

История, состояние и производные snapshots methodology repository. Эти файлы не являются reusable source для target-copy и не входят в source parity.

| path | description from manifest |
| --- | --- |
| `docs/agent-system/agents/**` |  |
| `docs/agent-system/source/**` |  |
| `docs/agent-system/BACKLOG.md` |  |
| `docs/agent-system/CURRENT_STATE.md` |  |
| `docs/agent-system/DECISION_LOG.md` |  |
| `docs/agent-system/NEXT_STEPS.md` |  |
| `docs/agent-system/RELEASE_READINESS.md` |  |
| `docs/agent-system/STAGE_2_COMPLETION_CHECKLIST.md` |  |

## journal

Engine journal scaffold and operational history. Target repository получает структуру/шаблоны, но не копирует operational rows или TASK/RESULT history methodology repository.

| path | description from manifest |
| --- | --- |
| `docs/agent-system/engine-journal/**` |  |

## scaffold

Scaffold-only files that define format/registry placeholders and are not project-specific source content.

| path | description from manifest |
| --- | --- |
| `docs/agent-system/SOURCE_CONSUMERS.md` |  |

## generated

Repo-local derived artifacts generated from authoritative methodology source. Эти файлы не являются source-transferable; их нужно регенерировать, а не править руками.

| path | description from manifest |
| --- | --- |
| `docs/agent-system/PROJECT_FILE_MAP.md` |  |
| `docs/agent-system/cloud/00_README.md` |  |
| `docs/agent-system/cloud/01_ORCHESTRATOR_OPERATING_CONTRACT.md` |  |
| `docs/agent-system/cloud/02_ORCHESTRATOR_RESPONSE_STANDARD.md` |  |
| `docs/agent-system/cloud/03_TASK_HEADER_COMMON.md` |  |
| `docs/agent-system/cloud/04_BRANCH_POLICY.md` |  |
| `docs/agent-system/cloud/05_ENGINE_JOURNAL_CONTRACT.md` |  |
| `docs/agent-system/cloud/06_CURRENT_STATE.md` |  |
| `docs/agent-system/cloud/07_ENGINE_JOURNAL_INDEX.md` |  |
| `docs/agent-system/cloud/08_NEXT_STEPS.md` |  |
| `docs/agent-system/cloud/09_ENGINE_ENTRYPOINT.md` |  |
| `docs/agent-system/cloud/10_PROJECT_FILE_MAP.md` |  |
| `docs/agent-system/cloud/11_ADOPTION_TRANSFER_MANIFEST_yml.md` |  |
| `docs/agent-system/cloud/12_REVIEW_AUTOLOOP.md` |  |
