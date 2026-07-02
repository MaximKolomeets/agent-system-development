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
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>
```

`<роль>` - vendor-neutral роль, которой назначена задача. `<task-id>` должен связывать задачу с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Журнал engine (Engine journal)

Каждая engine-задача и ответ engine должны сохраняться в target repository:

```text
docs/agent-system/engine-journal/input/
docs/agent-system/engine-journal/output/
```

Journal связывает task -> result -> branch -> PR -> commit/result. Task/result files являются append-only и не должны удаляться или перезаписываться без отдельного решения пользователя.

Contract:

```text
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
```

During adoption, transfer only the engine journal scaffold, templates, and
contract. Do not copy methodology repository operational history. The first
target adoption/audit task creates target-specific task/result files and the
target-specific `INDEX.md` entry.

## Режимы adoption (adoption modes)

Перед выбором режима выполнить `docs/agent-system/TARGET_ADOPTION_DETECTOR.md`: определить Variant A/B/C или STOP, подтвердить clean target tree, stable methodology source (`main`, release tag или published snapshot) и отсутствие риска overwrite target-specific journal/history/state. Detector не читает private data и не разрешает adoption от methodology `developer` или `work/*`.

## Методологическая ссылка (methodology_reference)

Каждая target adoption/update task должна фиксировать, какая версия methodology repository использована.

Канон спецификации `methodology_reference` (YAML-блок, обязательность commit SHA, STOP-условия, места включения): см. `docs/agent-system/ENGINE_ENTRYPOINT.md` → раздел «Methodology reference».

## Церемония и token budget

Методология не должна заставлять простую задачу проходить полный multi-agent ritual.

- Для read-only/status/cleanup использовать Operational Fast Lane.
- Для маленькой docs-only правки в solo-operator режиме достаточно одного role owner, одной ветки, одного PR и focused checks.
- Для target adoption, runtime, CI, security, branch model changes, journal closure или private-data risk использовать governed mode с полным блоком для исполнителя (engine).
- Если блок для исполнителя (engine) становится слишком длинным, использовать Task File Handoff Mode вместо расширения chat prompt.
- Нельзя добавлять новые templates/checklists только ради полноты, если существующий документ можно точечно расширить.

## Bootstrap нового пустого repository vs adoption существующего repository

`new empty repository bootstrap` используется для нового пустого repository.

Если выбран `standard developer workflow`:

- `developer` должен существовать до первой рабочей ветки;
- отсутствие `developer` не разрешает рабочий PR в `main`;
- допускается только явно разрешенный bootstrap-шаг создания `developer` от актуального `main`;
- после создания `developer` все рабочие ветки идут от `developer`;
- рабочие PR направляются в `developer`.

`existing repository adoption` используется для уже существующего target repository.

Для него действуют другие правила:

- фактическая branch model может быть `developer`, `develop`, `main-only flow` или custom;
- `engine` не переименовывает ветки без решения пользователя;
- если пользователь выбирает `standard developer workflow`, нужно создать или подтвердить `developer` до рабочих PR;
- если branch model неясна, `engine` пишет `STOP` и запрашивает решение пользователя.

## Канонический adoption chat prompt

Для нового target repository пользователь может скопировать полный prompt из канона:

```text
docs/agent-system/templates/ADOPTION_PROMPT.md
```

(раздел «Полный canonical copy/paste prompt»). Этот prompt просит оркестратора подготовить первую задачу для engine в режиме `audit-only`. Он не запускает full docs-only adoption и не переносит template repository state на первом шаге.

### 1. audit-only

Назначение:
первый безопасный dry run.

Результат:
только `docs/agent-system/ADOPTION_AUDIT.md` (target-local; канон-шаблон: `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`) и связанные engine journal artifacts.

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
- создана или обновлена journal entry для audit task/result;
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

- reusable source/template docs;
- role model;
- target project governance pack;
- project constitution;
- workflow docs;
- PR workflow;
- branch policy;
- manual review checklist;
- templates;
- engine journal templates and folders.

Engine journal transfer means scaffold/templates only. Existing methodology
repository task/result history, if any, is not copied into target repositories.

Запрещено:

- runtime agent code;
- Docker/service changes;
- CI changes, если не отдельный PR;
- production data;
- копировать `CURRENT_STATE`/`NEXT_STEPS`/`DECISION_LOG` дословно из template repository;
- переносить private data.

Acceptance criteria:

- project-specific state переписан под target repository;
- engine journal structure перенесена как process artifact;
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

## Манифест переноса (transfer manifest)

Машиночитаемый manifest переносимых файлов находится в:

```text
docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
```

Для discovery `engine` сначала читает manifest и его categories, а затем
подключает trigger-specific overlays по root `README.md` и
`docs/agent-system/METHODOLOGY_MAP.md` → `Mandatory overlays by trigger`.
Adoption docs не должны поддерживать отдельный полный inventory файлов рядом с
manifest: при изменении состава файлов обновляется manifest, а
`PROJECT_FILE_MAP.md` и `cloud/**` регенерируются.

Manifest делит файлы на текущие categories:

- `source` - reusable/canonical/operational methodology files; проверять наличие в source checkout и адаптировать target-facing policy по target facts;
- `template` - reusable templates; проверять наличие в source checkout и применять как основу materialization/adaptation;
- `target_generated` - файлы создаются в target repository из source/templates; не искать эти target paths в source checkout и не копировать verbatim;
- `history_state` - история, state и snapshots methodology repository; не копировать verbatim;
- `journal` - переносить только scaffold/templates, без operational rows и без истории TASK/RESULT methodology repository;
- `scaffold` - placeholder/scaffold files; заполнять в target только target-specific данными;
- `generated` - repo-local derived artifacts; регенерировать в target, а не копировать руками.

Если файл попадает в несколько categories или rules, применяется самый строгий режим. Например, `history_state` нельзя копировать как есть, а `target_generated` создаётся заново по target facts.

Manifest должен содержать `methodology_reference_required: true` для target adoption/update flows. Если target repository materializes собственный manifest или adoption audit, он фиксирует commit SHA methodology repository.

## Контроль Source и snapshot drift

Канон политики `source_snapshot` (YAML-header, GitHub как source of truth, drift handling, запрет менять repository state по устаревшему snapshot): см. `docs/agent-system/source/README.md` → «Source Snapshot Policy».

## Чеклист адаптации downstream (downstream adaptation checklist)

Checklist downstream-адаптации находится в:

```text
docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
```

Checklist используется перед docs-only adoption и review, чтобы проверить repository identity, branch model, state documents, security, adoption mode и review criteria.

## Чеклист downstream (downstream checklist)

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

Governance pack и Project Constitution Framework описаны в:

```text
docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
```

Шаблоны governance pack находятся в:

```text
docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md
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

`main-only flow` допустим только как осознанная фактическая модель existing repository adoption. Его нельзя молча применять к новому пустому repository, если пользователь выбрал `standard developer workflow` с `developer`.

Для нового пустого repository со стандартной схемой `main -> developer -> work/<role>/<task>` отсутствие `developer` является bootstrap blocker или trigger для явно разрешенного bootstrap creation step.

## PowerShell и UTF-8

Русские Markdown-файлы нужно читать в UTF-8, чтобы избежать mojibake.

Рекомендуемый PowerShell read-only пример:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Get-Content -Encoding UTF8 -Raw .\docs\agent-system\CURRENT_STATE.md
```

Если среда не разрешает менять `Console.OutputEncoding`, использовать `Get-Content -Encoding UTF8` и фиксировать проблему вывода как environment note, а не как ошибку документа.

## Минимальный первый PR

Minimal first PR должен создавать только:

```text
docs/agent-system/ADOPTION_AUDIT.md (target-local; канон-шаблон: docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md)
docs/agent-system/engine-journal/**
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

## Пошаговый existing-repo adoption

Этот раздел — канон пошагового переноса методологии в **уже существующий** target implementation repository (ранее жил в отдельном `TARGET_REPOSITORY_ADOPTION_GUIDE.md`).

GitHub является source of truth: в target repository фиксируются файлы, история, ветки, Pull Request, отчёты, решения и состояние. Public methodology repository не должен содержать приватные данные target repository. Visibility target repository выбирается отдельно и не наследуется от methodology repository. Пользователь принимает финальные решения; `engine` запускается вручную.

Старт adoption — через canonical prompt (`docs/agent-system/templates/ADOPTION_PROMPT.md`). Режимы (`audit-only` / `docs-only adoption` / `runtime adoption`), `methodology_reference`, transfer manifest, source snapshot drift, branch-flow канон (`developer` / `develop` / `main-only flow`), minimal first PR и PowerShell/UTF-8 — см. соответствующие разделы выше в этом документе. Feedback и его sanitization — канон в `docs/agent-system/METHODOLOGY_FEEDBACK_LOOP.md`.

### 1. Подготовить target repository profile

Шаблон: `docs/agent-system/templates/PROJECT_PROFILE_TEMPLATE.md`. Поля: project name, visibility, goal, non-goals, repository name, roles, branch policy, forbidden data, first milestone, first PR, acceptance criteria. Profile нейтральный, без приватных данных.

### 2. Проверить visibility и публикационные ограничения

- Public target repository — всё содержимое публично.
- Private target repository — секреты всё равно не попадают в Git.
- Methodology repository и target repository имеют разные уровни доступа; приватные данные target repository не переносятся обратно. Visibility решает пользователь.

### 3. Создать или подтвердить базовую структуру

Шаблон: `docs/agent-system/templates/NEW_REPOSITORY_STRUCTURE_TEMPLATE.md`. Нейтральная структура: `README.md`, `AGENTS.md`, `.gitignore`, `PROJECT_CONSTITUTION.md`, `docs/agent-system/` с `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md`, `BRANCH_POLICY.md`, `WORKFLOW.md`, `PR_WORKFLOW.md`, `ROLE_MODEL.md`, `PUBLICATION_POLICY.md`, `templates/`, `agents/`, `engine-journal/`. Bootstrap остаётся маленьким и проверяемым.

### 3a. Подготовить target project governance pack

До docs-only adoption создать или адаптировать governance pack по `docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md` и `docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md` (шаблоны `TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md`, `PROJECT_CONSTITUTION_TEMPLATE.md`): `PROJECT_CONSTITUTION.md`, `PROJECT_DASHBOARD.md`, `ROADMAP.md`, `RUNBOOK.md`, `DECISIONS.md` или `docs/agent-system/DECISION_LOG.md`, `CURRENT_STATE.md`, `NEXT_STEPS.md`, `BACKLOG.md`, `PROJECT_GUARDRAILS.md`, `ENGINE_REGISTRY.md`. Файлы пишутся по фактам target repository, не копируются verbatim. `PROJECT_CONSTITUTION.md` фиксирует mission, success criteria, out-of-scope, architectural principles, current strategic goal, decision authority и scope expansion control.

### 4. Адаптировать документы

Как основу можно переносить: `AGENTS.md`, README workflow-секции, branch policy, workflow, PR workflow, role model, publication policy, governance pack templates, templates. Адаптировать: project name, repository name, visibility, roles, first milestone, first PR, CI needs, branch model, worktree paths, forbidden data list, handoff text. Не переносить credentials, tokens, passwords, API keys, `.env`, клиентские/персональные данные, внутренние кодовые имена. `CURRENT_STATE.md`, `NEXT_STEPS.md`, `DECISION_LOG.md` пишутся заново по фактам target repository.

### 5. Создать ветки и worktree

Схема: `main`, `developer`, `work/<role>/<task>`; внутренние `work/<role>/<task>/*` допустимы только внутри той же substantive task. Нейтральный пример путей: `C:\Neural\repos\<target-repository-name>` и `C:\Neural\worktrees\<target-repository-name>\<role-name>`. Каждая задача — в основной ветке `work/<role>/<task>` от актуальной `developer`. Если target repository использует `develop` или другую модель — адаптировать branch policy, PR workflow, task templates, CI branch filters; не переименовывать ветки без решения пользователя (см. раздел «Developer vs develop» выше).

### 6. Подготовить первый bootstrap PR

Первый PR маленький и проверяемый (например: `README.md`, `AGENTS.md`, `.gitignore`, минимальный `docs/agent-system`, templates; без рабочих данных). Bootstrap PR не смешивается с implementation PR. Minimal first PR после короткого adoption prompt создаёт только `docs/agent-system/ADOPTION_AUDIT.md` (target-local; канон-шаблон: `docs/agent-system/templates/ADOPTION_AUDIT_TASK_TEMPLATE.md`) и `docs/agent-system/engine-journal/**` (см. «Minimal first PR» выше). Полный docs-only bootstrap — только после audit, engine journal result и Methodology feedback.

### 7. Проверить forbidden files

Запрещённые пути: `.env`, `.env.*` (кроме безопасного `.env.example`), `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`, `*.log`, `*.tmp`, `*.bak`. Проверки:

```bash
git status --short
git ls-files
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --
```

Sensitive grep — только filename-only; matching lines не печатать в терминал, отчёт или логи. При подозрении на реальный секрет — не печатать его и остановиться для решения пользователя.

### 8. Запустить engine

Оркестратор формирует задачу; пользователь запускает engine вручную; `engine` работает только в рабочей ветке, не читает `.env`, не меняет `main`/`developer` напрямую, пишет отчёт и не расширяет scope без решения пользователя. Задача на русском, начинается с обязательной шапки (`Задача для <роль>: <task-id>` + блок рекомендованного режима; канон шапки — `docs/agent-system/templates/TASK_HEADER_COMMON.md`). `<task-id>` связан с GitHub issue, Pull Request, task id или внутренним номером работы.

### 9. Проверить отчёт engine

Отчёт содержит: engine result file, рабочую ветку, что создано/изменено, changed files, проверки, что не проверялось, риски, next step, commit SHA, PR link/number. Без result file, проверок, рисков или changed files — уточнить перед review/merge.

### 10. Провести review и merge

Поток `work/<role>/<task> -> developer -> main`. PR из рабочей ветки идёт в `developer`; стабильное состояние переносится в `main`. Если ruleset запрещает direct push, sync `developer` после release выполняется через PR.

### 11. Подготовить handoff

Шаблон: `docs/agent-system/templates/NEW_PROJECT_HANDOFF_TEMPLATE.md`. Handoff фиксирует repository, visibility, current branches, active PR, completed PRs, important docs, current goal, next PR, risks и exact prompt for continuation.

### 12. Что нельзя делать

- Не переносить приватные данные в public methodology repository.
- Не переносить `.env`.
- Не коммитить runtime/work data.
- Не давать engine прямой push в `main`/`developer`.
- Не смешивать bootstrap с implementation.
- Не использовать vendor/tool names в названиях ролей.
- Не считать public/private visibility одинаковыми для разных repositories.
