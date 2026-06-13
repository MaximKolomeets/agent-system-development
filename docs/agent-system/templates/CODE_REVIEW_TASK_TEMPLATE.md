# CODE_REVIEW_TASK_TEMPLATE

Ниже расположен самодостаточный copy/paste-блок для `engine`. Перед использованием заменить placeholders в угловых скобках.

````text
Задача для <reviewer-role>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: задача выполняет review-only audit/review и должна создать report PR без исправления кода.

## Repository

Repository:

```text
<repository-url>
```

Локальный путь:

```text
<local-path>
```

## Lifecycle and branch model

Lifecycle mode:

```text
<new empty bootstrap | existing adoption | existing implementation | methodology repository review>
```

Selected branch model:

```text
<standard developer workflow | main-only flow | other explicit model>
```

Base branch:

```text
<developer | main | other explicit base>
```

Working branch:

```text
work/<reviewer-role>/<task-id>
```

Reviewer role:

```text
<code-reviewer-01 | qa-reviewer-01 | security-reviewer-01>
```

Engine:

```text
<engine-name>
```

Review mode:

```text
review-only
```

## Russian-first policy

Final report, review report, TASK/RESULT/INDEX и target-local docs/templates писать на русском языке.

English допустим только для code identifiers, commands, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.

## Goal

Провести review repository и создать review report.

Reviewer должен:

- изучить repository;
- выполнить безопасные checks;
- описать findings;
- предложить next implementation PRs, если нужны fixes;
- создать report PR в base branch.

Reviewer не должен исправлять production code в этой задаче.

## Required preflight

```powershell
cd <local-path>
git rev-parse --show-toplevel
git remote -v
git fetch --all --prune
git branch --show-current
git status --short
```

Если working tree не clean и пользователь не разрешил работать с текущими изменениями, написать `STOP`.

Если selected branch model неясна, написать `STOP`.

Если selected branch model = `standard developer workflow`, рабочая ветка должна создаваться только от актуальной `developer`.

## Create branch

Для standard developer workflow:

```powershell
git checkout developer
git pull --ff-only origin developer
git checkout -b work/<reviewer-role>/<task-id>
```

Для main-only flow использовать `main` только если это явно указано в selected branch model.

## Allowed files

Разрешено создавать/изменять только:

```text
<review-report-path>
<engine-journal-task-path-if-in-scope>
<engine-journal-result-path-if-in-scope>
<engine-journal-index-path-if-in-scope>
<state-docs-if-explicitly-allowed>
```

Если файл не указан в allowed files, не менять его.

## Forbidden files and paths

Запрещено читать, создавать, изменять или коммитить:

```text
.env
.env.*
.venv/
data/
runtime/
dist/
backups/
exports/
*.log
*.tmp
*.bak
credentials
tokens
passwords
cookies
Authorization/session headers
private downstream data
client data
runtime code
Dockerfile
docker-compose.yml
.github/workflows/**
scripts/**
```

## Naming rules

Запрещено использовать vendor/tool names в:

- reviewer role name;
- branch name;
- report filename;
- docs path;
- task id, если task id описывает роль.

Engine name указывать только в отдельном поле `Engine`.

## Required checks

Выполнить минимум:

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

Sensitive grep выводить только filename-only. Matching lines не печатать.

Tests/linters запускать только если они описаны в repository docs, не требуют `.env`, не запускают production services, не обращаются к private data и не меняют рабочие данные.

Если tests/linters не запускались, объяснить почему.

## Report path

Использовать:

```text
docs/agent-system/reviews/<task-id>-review.md
```

Если `docs/agent-system/` отсутствует:

```text
docs/reviews/<task-id>-review.md
```

Report filename не должен содержать vendor/tool name.

## Report structure

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

## Commit, push and PR policy

Review-only task создает report PR.

Запрещено:

- direct push в `main` или `developer`;
- branch from `main` для standard developer workflow;
- vendor-specific branch names;
- vendor-specific report filenames;
- fixing code in review-only task;
- reading `.env`;
- printing sensitive grep matching lines.

После report:

```powershell
git status --short
git diff --check
git diff --name-only <base>...HEAD
git add <allowed-files>
git commit -m "<commit-message>"
git push -u origin work/<reviewer-role>/<task-id>
```

Создать PR:

```text
Base: <base>
Head: work/<reviewer-role>/<task-id>
Title: <review task title>
```

## Final report

Ответить на русском:

```text
- branch;
- PR URL;
- changed files;
- created files;
- checks run;
- forbidden paths result;
- sensitive grep filename-only result;
- vendor-specific naming check result;
- risks;
- next step.
```
````
