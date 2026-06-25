# TARGET_REPOSITORY_BOOTSTRAP_TASK_TEMPLATE

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

Задача формулируется на русском языке. `<роль>` - vendor-neutral роль назначенного исполнителя. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

Все ответы, target-local docs, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке. Английский допустим только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и code identifiers.

Target `AGENTS.md` или эквивалентные target instructions должны содержать Russian-first policy после adoption/update scope, если этот scope меняет такие инструкции. Если target instructions конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая явного разрешения пользователя на другой язык.

## Рекомендуемый режим исполнения

Заполнить блок `Рекомендуемый режим исполнения` в mandatory header: роль / функция, исполнитель (на усмотрение архитектора), reasoning effort (низкий | средний | высокий), launch mode / запуск, execution mode / режим и why / почему.
Заполнить execution-время по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Execution timestamps»: measured `execution_started_at` обязательно для TASK; `orchestration_time_reported` опционально.

## Verified Baseline

- Repository:
- Local path, если применимо:
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
- [ ] No required execution context exists only in surrounding chat.

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Visibility

`public` или `private`.

## Base branch

`developer`

## Repository lifecycle mode

`new empty bootstrap` или `existing adoption`.

Для нового пустого repository со стандартной схемой `main -> developer -> work/<role>/<task>` ветка `developer` обязательна до первой рабочей ветки.

Если `developer` отсутствует, задача должна явно разрешить bootstrap creation of `developer` от актуального `main` или требовать `STOP`.

Рабочий PR в `main` запрещен для `standard developer workflow`.

## Selected branch model

`standard developer workflow`, `develop workflow`, `main-only flow` или custom flow.

`main-only flow` допустим только как осознанная фактическая модель existing repository adoption или как отдельное решение пользователя.

## Working branch

`work/<role>/<task>`

## Role

`<role-name>`

## engine

`engine=<manual or selected engine>`

## Mandatory preflight

Перед bootstrap `engine` обязан выполнить контракт:

```text
docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md
```

Self-discovery, adoption mode selection и adoption audit выполняются до любых изменений файлов.

Использовать:

```text
docs/agent-system/ADOPTION_GUIDE.md
docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
```

## Goal

Описать цель bootstrap.

## Project constitution check

Project mission:
Current strategic goal:
Scope impact: <No scope expansion | Minor scope expansion | Major scope expansion>
Decision level: <Level 1 | Level 2 | Level 3 | Level 4>
Requires explicit user approval: <yes/no>

## Adoption mode

`audit-only`, `docs-only adoption` или `runtime adoption`.

По умолчанию для первого dry run использовать `audit-only`.

## Allowed files

Пример:

- `README.md`
- `AGENTS.md`
- `.gitignore`
- `docs/agent-system/**`
- `.github/workflows/**`, если нужен CI

## Forbidden files and paths

- `.env`
- `.env.*`, кроме безопасного `.env.example`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- `*.log`
- `*.tmp`
- `*.bak`

## Required documents

Для `audit-only`:

- `docs/agent-system/ADOPTION_AUDIT.md`

Для `docs-only adoption`, после отдельного решения пользователя:

- `README.md`
- `AGENTS.md`
- `PROJECT_CONSTITUTION.md`
- `PROJECT_DASHBOARD.md`
- `ROADMAP.md`
- `RUNBOOK.md`
- `DECISIONS.md`, если нужен root-level decision log
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- `docs/agent-system/BACKLOG.md`
- `docs/agent-system/DECISION_LOG.md`
- `docs/agent-system/PROJECT_GUARDRAILS.md`
- `docs/agent-system/ENGINE_REGISTRY.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/WORKFLOW.md`
- `docs/agent-system/PR_WORKFLOW.md`
- `docs/agent-system/ROLE_MODEL.md`
- `docs/agent-system/PUBLICATION_POLICY.md`

Governance state files не копировать из template repository verbatim. `CURRENT_STATE.md`, `NEXT_STEPS.md`, `BACKLOG.md`, `DECISION_LOG.md`, `PROJECT_CONSTITUTION.md`, `PROJECT_DASHBOARD.md`, `ROADMAP.md`, `PROJECT_GUARDRAILS.md` и `ENGINE_REGISTRY.md` должны быть переписаны под target repository.

Target engine journal должен поддерживать Closure policy по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure policy». Bootstrap/adoption handoff является per-task closure exception; обычные work PR после bootstrap закрываются batch-closure перед release.

## Checks

- `git status --short`
- `git branch --show-current`
- `git diff --check`
- `git ls-files`
- branch model check: lifecycle mode, selected branch model, `developer` existence и `fallback-to-main allowed`;
- forbidden tracked paths check
- sensitive grep filename-only:

```bash
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --
```

Sensitive grep должен печатать только filenames. Не печатать matching lines в terminal output, engine logs или final reports.

- проверка Closure policy для RESULT/INDEX, если PR уже merged (`bootstrap/adoption` — per-task closure exception)

## Final report format

`engine` должен вернуть:

- final report на русском языке;
- working branch;
- created files;
- changed files;
- checks executed;
- repository lifecycle mode;
- selected branch model;
- developer branch existence;
- fallback-to-main allowed: yes/no with reason;
- checks not executed and why;
- risks;
- adoption mode;
- transfer manifest notes;
- methodology feedback;
- Russian-first policy result;
- suggested methodology improvements;
- automation opportunities;
- safety gaps;
- next step;
- commit SHA;
- push status;
- PR link/number;
- статус PR после review (`PR status after review`);
- merge commit SHA после merge, если доступен;
- release PR URL/status/merge commit SHA, если release выполнялся;
- sync PR URL/status/merge commit SHA, если sync выполнялся;
- RESULT закрыт после merge;
- INDEX закрыт после merge;
- проверка Closure policy (`bootstrap/adoption` — per-task closure exception).

## Rules

- Do not read `.env`.
- Do not commit forbidden files.
- Do not push directly to `main`.
- Do not push directly to `developer`.
- Do not expose secrets.
- Do not use real credentials in examples.
- User makes final decisions.
- Final report, TASK/RESULT/INDEX и target-local docs/templates пишутся на русском языке, кроме технических identifiers и literal external names.
