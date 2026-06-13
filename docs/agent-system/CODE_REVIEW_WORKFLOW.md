# CODE_REVIEW_WORKFLOW

## Назначение

Этот workflow описывает безопасный code review / external review / consulting review для methodology repository и target implementation repositories.

Цель workflow - подключать любой `engine` как reviewer-консультанта без vendor-specific имен в ролях, ветках, путях, filenames, task ids и отчетах.

`engine` указывается отдельно от роли:

```text
engine=<engine-name>
reviewer role=code-reviewer-01
```

Role name, branch namespace и report filename не должны зависеть от vendor/tool name.

## Reviewer roles

Рекомендуемые роли:

- `code-reviewer-01` - общий review архитектуры, структуры, кода, тестов, документации и рисков;
- `qa-reviewer-01` - review тестов, quality gates, регрессий и проверяемости;
- `security-reviewer-01` - review секретов, forbidden paths, auth/config risks и security guardrails.

Reviewer roles не исправляют найденные проблемы по умолчанию. Они создают report PR с findings и proposed next PRs.

Implementation выполняется отдельной задачей, отдельной веткой и отдельным PR, например:

```text
work/dev-implementer-01/<task-id>
```

## Review-only by default

Reviewer по умолчанию:

- изучает repository;
- запускает read-only или безопасные checks;
- пишет review report;
- не меняет production code;
- не исправляет найденные проблемы;
- не делает refactor;
- не меняет runtime, Docker, CI, scripts или dependencies без отдельной задачи;
- не читает `.env`;
- не печатает matching lines sensitive grep.

Если пользователь просит исправить findings, нужно создать отдельную implementation task. Review report может предложить next PRs, но не должен сам превращаться в fix PR.

## Branch naming

Для standard developer workflow используется модель:

```text
main -> developer -> work/<role>/* -> PR в developer
```

Reviewer branch создается от актуальной `developer`:

```text
work/code-reviewer-01/<task-id>
work/qa-reviewer-01/<task-id>
work/security-reviewer-01/<task-id>
```

Запрещено:

- создавать reviewer branch от `main` для standard developer workflow;
- открывать review PR напрямую в `main`;
- делать direct push в `main` или `developer`;
- использовать vendor/tool name в branch namespace.

Если target implementation repository использует main-only flow, это должно быть явно зафиксировано в task как selected branch model. Если branch model неясна, reviewer пишет `STOP`.

## Vendor-neutral naming

Vendor/tool names запрещены в:

- role names;
- branch names;
- report filenames;
- docs paths;
- task ids, если task id описывает роль, а не внешний инструмент.

Bad examples:

```text
claude/initial-review
codex-review
docs/CLAUDE_REVIEW.md
gemini-audit
copilot-fixes
```

Good examples:

```text
work/code-reviewer-01/initial-project-review
work/security-reviewer-01/dependency-risk-review
work/qa-reviewer-01/test-gap-review
docs/agent-system/reviews/initial-project-review.md
```

## Report naming

Для target implementation repository использовать:

```text
docs/agent-system/reviews/<task-id>-review.md
```

Если в target implementation repository нет `docs/agent-system/`, допустим fallback:

```text
docs/reviews/<task-id>-review.md
```

Для methodology repository рекомендуемый путь:

```text
docs/agent-system/reviews/
```

Report filename не должен содержать vendor/tool name.

## Allowed scope

Review-only PR может содержать только files, явно разрешенные task.

Типичный scope:

- review report;
- engine journal TASK/RESULT/INDEX, если task включает engine journal;
- state docs, если task явно разрешает state update.

Запрещенный scope по умолчанию:

- production code fixes;
- refactor;
- runtime changes;
- Docker changes;
- CI changes;
- dependency changes;
- scripts changes;
- private downstream data;
- `.env` и `.env.*`;
- credentials, tokens, passwords, cookies, Authorization/session headers.

## Safety gates

Перед review reviewer проверяет:

- repository соответствует task;
- remote соответствует expected repository;
- selected branch model указан;
- base branch определен;
- working tree clean или пользователь явно разрешил работать с текущими изменениями;
- forbidden tracked paths отсутствуют;
- sensitive grep выполняется filename-only;
- `.env` не читается.

Если gate не пройден, reviewer пишет:

```text
STOP
```

После `STOP` reviewer кратко указывает причину и не меняет файлы.

## Required checks

Минимальный набор checks:

```powershell
git rev-parse --show-toplevel
git remote -v
git fetch --all --prune
git branch --show-current
git status --short
git ls-files
git diff --check
git diff --name-only <base>...HEAD
git ls-files | Select-String -Pattern '(^|/)(\.env|\.venv|data|runtime|dist|backups|exports)(/|$)|\.(log|tmp|bak)$'
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" -- 2>$null
```

Sensitive grep result должен быть filename-only. Matching lines не печатать.

Reviewer может запускать tests/linters только если:

- они описаны в README/RUNBOOK/package scripts;
- они не требуют `.env`;
- они не запускают production services;
- они не обращаются к private data;
- они не меняют рабочие данные.

Если tests/linters не запускались, reviewer объясняет почему в review report.

## Report structure

Review report должен использовать структуру:

```text
# <task-id> - code review report

## Summary

## Repository snapshot

## Branch model

## Project description

## Architecture overview

## Entry points

## Dependency and tooling overview

## Tests and quality gates

## Security and secret-handling observations

## Findings

### Critical

### Important

### Optional

## Recommendations

## Proposed next PRs

## Checks executed

## Checks not executed and why

## Forbidden paths result

## Sensitive grep result

## Scope boundaries

## Reviewer notes
```

## Final report

Final report reviewer пишет на русском языке и включает:

- branch;
- PR URL, если PR создан;
- changed files;
- created files;
- checks run;
- forbidden paths result;
- sensitive grep filename-only result;
- vendor-specific naming check result;
- risks;
- next step.

## Findings to next PRs

Findings не исправляются внутри review-only task.

Для каждого finding reviewer может предложить next PR:

```text
role=<implementation-role>
branch=work/dev-implementer-01/<task-id>
scope=<короткое описание исправления>
base=<developer|explicit branch model>
```

Пользователь принимает отдельное решение, какие findings превращать в implementation PR.
