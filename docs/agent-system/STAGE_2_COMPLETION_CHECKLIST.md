# STAGE_2_COMPLETION_CHECKLIST

## Назначение

Этот checklist нужен для проверки готовности methodology stage перед первым target repository dry run.

## Required artifacts

- [x] `PROJECT_LIFECYCLE.md` exists (PR-C4: redirect-заглушка; канон жизненного цикла — `NEW_PROJECT_ONBOARDING_GUIDE.md`).
- [x] `NEW_PROJECT_ONBOARDING_GUIDE.md` exists.
- [x] `TARGET_REPOSITORY_ADOPTION_GUIDE.md` exists (PR-C4: redirect-заглушка; канон existing-repo adoption — `ADOPTION_GUIDE.md`).
- [x] `ADOPTION_GUIDE.md` exists.
- [x] `ADOPTION_TRANSFER_MANIFEST.yml` exists.
- [x] `DOWNSTREAM_ADAPTATION_CHECKLIST.md` exists.
- [x] `ENGINE_ENTRYPOINT.md` exists.
- [x] `ENGINE_SELF_DISCOVERY_CONTRACT.md` exists.
- [x] `METHODOLOGY_FEEDBACK_LOOP.md` exists.
- [x] `TARGET_PROJECT_GOVERNANCE_PACK.md` exists.
- [x] `PROJECT_CONSTITUTION_FRAMEWORK.md` exists.
- [x] `SHORT_TARGET_ADOPTION_PROMPT.md` exists.
- [x] reusable templates exist.
- [x] governance pack templates exist.
- [x] branch policy exists.
- [x] workflow exists.
- [x] PR workflow exists.
- [x] worktree guide exists.
- [x] publication policy exists.
- [x] CI policy exists.
- [x] forbidden files CI exists.
- [x] docs-maintainer reports exist.
- [x] handoff template exists.
- [x] target repository bootstrap task template exists.
- [x] `ADOPTION_AUDIT_TASK_TEMPLATE.md` exists.
- [x] `DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md` exists.
- [x] `CHATGPT_RESPONSE_STANDARD.md` exists.
- [x] `CHATGPT_RESPONSE_TEMPLATE.md` exists.
- [x] `FILE_COMMENTING_STANDARD.md` exists.
- [x] `TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md` exists.
- [x] `docs/agent-system/source/SOURCE_agent_system_index.md` exists and is updated after PR-2m.
- [x] `RELEASE_READINESS.md` exists and records a pre-PR-2o release readiness snapshot.
- [x] short prompt adoption mode documented.
- [x] audit-only, docs-only adoption and runtime adoption modes documented.
- [x] minimal first PR creates only `ADOPTION_AUDIT.md`.
- [x] downstream checklist includes repository name, branch model, worktree paths, current state and visibility.
- [x] developer vs develop and CI branch filters are documented.
- [x] PowerShell/UTF-8 note for Russian Markdown is documented.
- [x] `CURRENT_STATE.md` verbatim copy is forbidden.
- [x] target repository final report includes Methodology feedback.
- [x] feedback does not expose private data.
- [x] methodology repository role is documented as reusable template, not downstream control center.
- [x] mandatory engine task header is documented.
- [x] task id to issue/PR/task mapping is documented.
- [x] target project governance pack is documented.
- [x] project constitution framework is documented.
- [x] dashboard, roadmap, backlog, guardrails and engine registry templates exist.
- [x] project constitution template exists.
- [x] unified ChatGPT response standard is documented.
- [x] methodology freshness check is documented.
- [x] language consistency rule is documented.
- [x] file commenting standard is documented.

## Process readiness

- [x] one task = one branch = one PR;
- [x] work branches use `work/<role>/<task>`;
- [x] developer receives changes through PR;
- [x] main receives stable state from developer;
- [x] developer sync after main release is handled through PR if ruleset requires it;
- [x] user manually launches engine;
- [x] engine tasks start with `Задача для <agent-name>: <task-id>`;
- [x] ChatGPT reviews reports and prepares next tasks;
- [x] user makes final decisions.

## Security readiness

- [x] `.env` is forbidden;
- [x] `.venv/` is forbidden;
- [x] `data/`, `runtime/`, `dist/`, `backups/`, `exports/` are forbidden;
- [x] real credentials/tokens/passwords/API keys are forbidden;
- [x] sensitive grep is part of review;
- [x] public repository rules are documented;
- [x] target repository visibility is handled separately.

## Documentation readiness

- [x] `CURRENT_STATE.md` is current;
- [x] `NEXT_STEPS.md` is current;
- [x] `DECISION_LOG.md` has current decisions;
- [x] Source index is current;
- [x] docs-maintainer summary is current;
- [x] next chat prompt is current.
- [x] pre-release readiness snapshot is current.

## Known issues

- На момент PR-2c workflow был updated to Node.js 24 compatible checkout action.
- Если GitHub Actions снова покажет runtime warning, это должно идти отдельным PR.
- Source index существует как `docs/agent-system/source/SOURCE_agent_system_index.md` и обновлен в PR-2n follow-up commit.
- Release `developer` -> `main` еще не выполнен; PR-2o только фиксирует pre-release readiness snapshot и не создает release PR.
- Final release refresh требуется после merge PR-2o в `developer`.
- Unified response standard готов к применению в новых target repository adoption chats после release decision пользователя.

## Completion criteria

Этап считается готовым, если:

- PR-2m merged в `developer`;
- PR-2m standards присутствуют в `developer`;
- `CHATGPT_RESPONSE_STANDARD.md`, `CHATGPT_RESPONSE_TEMPLATE.md` и `FILE_COMMENTING_STANDARD.md` присутствуют;
- methodology freshness check закреплен в response template и engine-facing docs;
- one-engine-task-one-block rule закреплен в response standard/template;
- language consistency rule закреплен в adoption audit/docs-only adoption flow;
- stage checklist заполнен по фактически проверенным файлам;
- pre-release readiness snapshot для `developer` -> `main` зафиксирован;
- final release refresh после merge PR-2o обязателен перед release PR;
- release `developer` -> `main` выполняется только после решения пользователя;
- следующий шаг - release PR или target repository adoption dry run с обязательной task header.
