# DOCS_ONLY_ADOPTION_TASK_TEMPLATE

## Mandatory header

```text
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: <свободное значение или пусто>
```

Задача формулируется на русском языке. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Рекомендуемый режим исполнения

Заполнить блок `Рекомендуемый режим исполнения` в mandatory header: роль / функция, исполнитель (на усмотрение архитектора), reasoning effort (низкий | средний | высокий), launch mode / запуск, execution mode / режим и why / почему.
Заполнить execution-время по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Execution timestamps»: measured `execution_started_at` обязательно для TASK; `orchestration_time_reported` опционально.

## Machine-readable task_contract

Docs-only adoption/source-update задачи должны включать fenced YAML block `task_contract` по `docs/agent-system/TASK_CONTRACT.md`, потому что они меняют repository files и требуют воспроизводимых allowed/forbidden files, checks и STOP conditions.

Если `task_contract` присутствует, он является источником истины для mode/scope/checks/STOP, а prose остаётся human explanation. Конфликт contract/prose означает `STOP`.

## Verified Baseline

- Repository:
- Local path, если применимо:
- Methodology repository:
- Methodology source branch:
- Methodology source commit:
- Methodology checked at:
- Base branch:
- Working branch:
- Checked branch state:
- Latest relevant PR numbers/statuses, если применимо:
- Release PR status, если применимо:
- Sync PR status, если применимо:
- Open PR state, если relevant:
- Verification source:
- Verification date/time:

## Проверка полноты copy/paste

- [ ] This TASK/Engine block can be executed without reading surrounding chat text.
- [ ] Блок «Рекомендуемый режим исполнения» включён.
- [ ] Verified baseline is included or explicitly marked as not applicable.
- [ ] Repository/base branch/working branch are included.
- [ ] Allowed files are included.
- [ ] Forbidden files are included.
- [ ] Checks are included.
- [ ] STOP conditions are included.
- [ ] Final report requirements are included.
- [ ] Source Delta requirement is included by reference to `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source Delta».
- [ ] No required execution context exists only in surrounding chat.

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Adoption mode

`docs-only adoption`

## Base branch

`<main/developer/develop according to target repository>`

## Working branch

`work/<role>/<task>`

## Role

`docs-maintainer-01`

## Goal

Добавить адаптированную документационную систему `docs/agent-system/` и, если входит в scope, target project governance pack в target repository без runtime changes.

Зафиксировать methodology reference, использованную для docs-only adoption:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: <developer или явно заданная branch>
  source_commit: <commit-sha>
  checked_at: <ISO-8601 timestamp>
  reference_type: commit
  notes: <short Russian note>
```

`source_commit` обязателен. Если commit SHA получить нельзя, docs-only adoption нельзя считать ready-for-review.

Governance docs target repository должны быть приведены к единому языку. Для русскоязычного target repository по умолчанию используется русский язык.

Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке. Английский допустим только для команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и code identifiers.

Target `AGENTS.md` или эквивалентные target instructions должны содержать Russian-first policy после adoption/update scope, если этот scope меняет такие инструкции.

Если target instructions конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая явного разрешения пользователя на другой язык.

Не переводить code identifiers, paths, commands, config keys, package names, API names, branch names, file names и vendor/tool names.

При переводе или унификации языка нельзя менять смысл архитектурных решений.

В создаваемые и изменяемые скрипты, workflow и технические файлы добавить русские комментарии для нужных строк/блоков. Если формат файла не поддерживает комментарии, пояснения добавить в соседнюю документацию или schema descriptions.

## Project constitution check

Project mission:
Current strategic goal:
Scope impact: <No scope expansion | Minor scope expansion | Major scope expansion>
Decision level: <Level 1 | Level 2 | Level 3 | Level 4>
Requires explicit user approval: <yes/no>

## Inputs

- `docs/agent-system/ADOPTION_AUDIT.md` from target repository;
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` from template repository;
- `docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md` from template repository;
- `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md` from template repository;
- `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md` from template repository;
- local `AGENTS.md`;
- local `README.md`;
- local architecture/status docs.

## Allowed files

Разрешены только docs-only files, например:

- `docs/agent-system/README.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/SECURITY_POLICY.md`
- `docs/agent-system/MANUAL_REVIEW_CHECKLIST.md`
- `docs/agent-system/PROJECT_GUARDRAILS.md`
- `docs/agent-system/ENGINE_REGISTRY.md`
- `docs/agent-system/templates/**`
- `docs/agent-system/agents/docs-maintainer-01/**`
- `docs/agent-system/engine-journal/**`

Engine journal scope является target-specific: скопировать или создать scaffold/templates при необходимости, но не копировать methodology repository operational history. Target task/result entries являются append-only после создания.

Docs-only adoption/source-update является per-task closure exception по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure policy». После merge рабочего PR, release PR или sync PR target `RESULT` и `INDEX` закрываются по Closure policy; для обычных work PR вне adoption/source-update действует batch-closure перед release.

Governance pack files разрешены только как docs-only artifacts:

- `PROJECT_CONSTITUTION.md`
- `PROJECT_DASHBOARD.md`
- `ROADMAP.md`
- `RUNBOOK.md`
- `DECISIONS.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/PROJECT_GUARDRAILS.md`
- `docs/agent-system/ENGINE_REGISTRY.md`

## Requires adaptation

Нельзя копировать дословно:

- `PROJECT_DASHBOARD.md`
- `PROJECT_CONSTITUTION.md`
- `ROADMAP.md`
- `RUNBOOK.md`
- `DECISIONS.md`
- `CURRENT_STATE.md`
- `NEXT_STEPS.md`
- `BACKLOG.md`
- `DECISION_LOG.md`
- `PROJECT_GUARDRAILS.md`
- `ENGINE_REGISTRY.md`
- Source index
- docs-maintainer reports
- engine journal index entries and task/result files
- ruleset status
- branch status
- project-specific history

Эти файлы либо не добавляются в первом docs-only PR, либо переписываются под target repository.

## Forbidden changes

- runtime code
- Docker
- CI
- Source mirror
- architecture docs
- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`

## Branch adaptation

Перед изменениями проверить:

- default branch;
- integration branch;
- `developer` vs `develop`;
- CI branch filters;
- rulesets/branch protection status.

## Required preflight

- выполнить repository self-discovery;
- проверить clean worktree;
- прочитать local instructions;
- применить transfer manifest;
- применить downstream checklist;
- применить governance pack template, если он в scope;
- создать или адаптировать `PROJECT_CONSTITUTION.md`, если governance pack в scope;
- выбрать только docs-only adoption mode.

## Checks

- git status --short
- git branch --show-current
- git diff --check
- git ls-files
- forbidden tracked paths check
- sensitive grep filename-only
- проверить, что нет runtime/code/CI changes
- проверить, что governance state files переписаны по фактам target repository
- проверить, что reusable templates не смешаны с target-specific state files
- проверить, что engine journal structure создана и task/result files не содержат private data
- проверить, что шаг Closure policy есть для RESULT/INDEX (`adoption/source-update` — per-task closure exception)
- проверить, что materialized governance files адаптированы под target repository
- проверить Governance Review Checklist из `PROJECT_CONSTITUTION.md`
- проверить language consistency governance docs
- проверить Russian-first policy в target `AGENTS.md` или эквивалентных target instructions, если они входят в scope
- проверить, где добавлены русские комментарии для нужных строк/блоков
- проверить, где комментарии не применимы из-за формата файла
- проверить, что `methodology_reference` есть в audit/adoption artifacts и содержит source commit SHA
- проверить, что final report и RESULT содержат Source Delta по `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source Delta»

## Final report

- final report на русском языке;
- adoption mode;
- working branch;
- created files;
- changed files;
- adapted files;
- files intentionally not copied;
- checks;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- local instruction conflicts;
- language consistency changes;
- Russian-first policy result;
- commenting changes;
- methodology reference;
- engine journal files;
- Source Delta present: yes/no;
- проверка Closure policy (`adoption/source-update` — per-task closure exception);
- files where comments are not applicable and why;
- risks;
- Methodology feedback;
- next recommended PR;
- commit SHA;
- push status;
- PR link/number.
