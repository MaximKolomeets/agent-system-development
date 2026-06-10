# ADOPTION_AUDIT_TASK_TEMPLATE

## Mandatory header

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

Задача формулируется на русском языке. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Task

`<task title>`

## Target repository

`<owner/repository>`

## Adoption mode

`audit-only`

## Base branch

`<main or target base branch>`

## Working branch

`work/<role>/<task>`

## Role

`docs-maintainer-01`

## Goal

Выполнить repository self-discovery, проверить language consistency и создать только `docs/agent-system/ADOPTION_AUDIT.md`.

## Allowed files

- `docs/agent-system/ADOPTION_AUDIT.md`

## Forbidden changes

- `AGENTS.md`
- `README.md`
- `.github/workflows/**`
- Docker files
- runtime code
- architecture docs
- Source mirror
- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`

## Required preflight

- выполнить `ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- прочитать local `AGENTS.md`;
- прочитать local `README.md`;
- прочитать local architecture/status docs, если есть;
- проверить working tree;
- если working tree dirty - использовать clean worktree или STOP;
- sensitive grep только filename-only.

## Output

Создать audit file с разделами:

- repository self-discovery;
- current project state;
- template repository summary;
- fit analysis;
- language consistency audit;
- список файлов с нерусскими governance descriptions;
- рекомендация по унификации языка;
- проверка скриптов, workflow и templates на достаточные русские комментарии для нужных строк/блоков;
- adoption recommendation;
- risks;
- open questions;
- Methodology feedback;
- нейтральный `Methodology repository improvement request`, если audit показал, что methodology repository нужно улучшить.

Language consistency rule:

- English allowed only for code identifiers, paths, commands, config keys, vendor/tool names, upstream package names and API names;
- для русскоязычного target repository governance descriptions должны быть на русском языке;
- mixed-language sections должны быть либо оправданы, либо рекомендованы к нормализации.

Methodology feedback не должен включать private downstream data, private repository URLs, client data, customer data, internal code names или secrets.

## Checks

- git status --short
- git branch --show-current
- git diff --check
- git ls-files
- forbidden tracked paths check
- sensitive grep filename-only
- language consistency audit
- commenting consistency audit

## Final report

- working branch;
- created files;
- changed files;
- checks;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- language consistency result;
- commenting consistency result;
- risks;
- Methodology feedback;
- Methodology repository improvement request, если есть;
- commit SHA;
- push status;
- PR link/number.
