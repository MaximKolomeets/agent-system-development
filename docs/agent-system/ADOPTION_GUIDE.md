# ADOPTION_GUIDE

## Назначение

Документ описывает режимы применения methodology repository к target repository.

Цель:

- разделить audit-only, docs-only adoption и runtime adoption;
- не смешивать документационный bootstrap с runtime implementation;
- не переносить template repository state дословно;
- не раскрывать private data target repository.

## Роль methodology repository

`agent-system-development` является reusable methodology/template repository.

Он не является центральным репозиторием управления downstream-проектами. После adoption ветки, worktree, отчеты, Pull Request, project-specific state и рабочие артефакты ведутся в target repository.

В `agent-system-development` возвращаются только универсальные улучшения методологии через отдельные methodology PR без private data, client data, private repository URL, внутренних кодовых имен и project-specific state.

## Обязательная шапка task prompt

Каждая задача для `engine` должна быть на русском языке и начинаться с шапки:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

`<agent-name>` - role-based имя агента, которому назначена задача. `<task-id>` должен связывать задачу с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Adoption modes

### 1. audit-only

Назначение:
первый безопасный dry run.

Результат:
только `docs/agent-system/ADOPTION_AUDIT.md`.

Task template:

```text
docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md
```

Запрещено:

- менять код;
- менять Docker;
- менять CI;
- менять Source mirror;
- менять architecture docs;
- менять `AGENTS.md`/`README.md`, если это не отдельное решение пользователя;
- копировать весь template repository.

Acceptance criteria:

- repository self-discovery выполнен;
- локальные инструкции прочитаны;
- working tree clean или используется отдельный clean worktree;
- создан только adoption audit;
- final report содержит Methodology feedback.

### 2. docs-only adoption

Назначение:
добавить адаптированную документационную систему агентов.

Результат:
адаптированный `docs/agent-system/` в target repository.

Task template:

```text
docs/agent-system/templates/DOCS_ONLY_ADOPTION_TASK_TEMPLATE.md
```

Разрешено:

- generic docs;
- role model;
- target project governance pack;
- workflow docs;
- PR workflow;
- branch policy;
- manual review checklist;
- templates.

Запрещено:

- runtime agent code;
- Docker/service changes;
- CI changes, если не отдельный PR;
- production data;
- копировать `CURRENT_STATE`/`NEXT_STEPS`/`DECISION_LOG` дословно из template repository;
- переносить private data.

Acceptance criteria:

- project-specific state переписан под target repository;
- governance pack создан или адаптирован по фактам target repository;
- branch names адаптированы;
- local `AGENTS.md` имеет приоритет;
- Source mirror не менялся.

### 3. runtime adoption

Назначение:
добавить runtime agent services, orchestrator, workers или API.

Условие:
только после отдельного архитектурного решения в target repository.

Запрещено:

- начинать runtime adoption в audit-only или docs-only PR;
- добавлять services/Docker без отдельного scope;
- смешивать runtime changes с документационным bootstrap.

Acceptance criteria:

- есть архитектурное решение;
- есть отдельная ветка;
- есть отдельный PR;
- есть тесты/проверки;
- security constraints учтены.

## Transfer manifest

Машиночитаемый manifest переносимых файлов находится в:

```text
docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
```

Manifest делит файлы на categories:

- `generic` - можно использовать как методологическую основу;
- `requires_target_adaptation` - переносить только после адаптации под target repository;
- `template_state_do_not_copy_verbatim` - состояние самого methodology repository, не копировать дословно.

Если файл попадает в несколько categories, применяется самый строгий режим. Например, файл из `template_state_do_not_copy_verbatim` нельзя копировать как есть.

## Downstream adaptation checklist

Checklist downstream-адаптации находится в:

```text
docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
```

Checklist используется перед docs-only adoption и review, чтобы проверить repository identity, branch model, state documents, security, adoption mode и review criteria.

## Downstream checklist

Перед docs-only adoption заменить или подтвердить:

- repository name;
- repository visibility;
- branch model;
- наличие `developer` или `develop`;
- CI branch filters;
- worktree paths;
- current state;
- next steps;
- decision log;
- role names;
- forbidden data rules;
- publication policy;
- Source mirror policy.

`CURRENT_STATE.md`, `NEXT_STEPS.md` и `DECISION_LOG.md` из methodology repository нельзя копировать verbatim. Они описывают состояние template repository, а не target repository.

Governance pack описан в:

```text
docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
```

Шаблоны governance pack находятся в:

```text
docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
docs/agent-system/templates/PROJECT_DASHBOARD_TEMPLATE.md
docs/agent-system/templates/ROADMAP_TEMPLATE.md
docs/agent-system/templates/BACKLOG_TEMPLATE.md
docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md
docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md
```

## Developer vs develop

Template repository использует ветку `developer`.

Target repository может использовать `developer`, `develop`, `main`-only flow или другую модель. Перед переносом branch policy нужно:

- проверить фактические ветки target repository;
- адаптировать `BRANCH_POLICY.md`, `WORKFLOW.md`, `PR_WORKFLOW.md` и task templates;
- проверить GitHub Actions branch filters;
- убедиться, что CI запускается на реальных target branches;
- не переименовывать ветки без отдельного решения пользователя.

## PowerShell and UTF-8

Русские Markdown-файлы нужно читать в UTF-8, чтобы избежать mojibake.

Рекомендуемый PowerShell read-only пример:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Get-Content -Encoding UTF8 -Raw .\docs\agent-system\CURRENT_STATE.md
```

Если среда не разрешает менять `Console.OutputEncoding`, использовать `Get-Content -Encoding UTF8` и фиксировать проблему вывода как environment note, а не как ошибку документа.

## Minimal first PR

Minimal first PR должен создавать только:

```text
docs/agent-system/ADOPTION_AUDIT.md
```

Minimal first PR не должен:

- переносить весь `docs/agent-system/`;
- менять runtime code;
- менять Docker;
- менять CI;
- менять Source mirror;
- переписывать локальные инструкции target repository;
- копировать `CURRENT_STATE.md`, `NEXT_STEPS.md` или `DECISION_LOG.md` из methodology repository.

Цель minimal first PR - получить безопасный audit, зафиксировать Methodology feedback и только после этого планировать docs-only adoption.
