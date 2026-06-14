# TARGET_REPOSITORY_ADOPTION_GUIDE

## Назначение

Этот guide нужен для переноса методологии `agent-system-development` в отдельный target implementation repository.

GitHub является source of truth: в target repository должны фиксироваться файлы, история изменений, ветки, pull request, отчеты, решения и текущее состояние. Public methodology repository не должен содержать приватные данные target repository. Target repository может быть public или private, и его visibility выбирается отдельно. Пользователь принимает финальные решения. `engine` запускается пользователем вручную.

`agent-system-development` используется как reusable methodology/template repository. Он не является центральным репозиторием управления агентами target repository. После adoption рабочие ветки, worktree, отчеты, Pull Request, project-specific state и рабочие артефакты создаются в самом target repository.

## Short prompt adoption mode

Canonical copy/paste prompt:

```text
docs/agent-system/templates/TARGET_REPOSITORY_ADOPTION_CHAT_PROMPT.md
```

Пользователь копирует этот prompt в новый чат в контексте target repository. ChatGPT изучает target repository и methodology repository, затем готовит первую задачу для engine в режиме `audit-only`. Engine не выполняет full adoption на первом шаге.

Пользователь может начать adoption коротким prompt со ссылкой на template repository:

```text
Интегрируй в текущий проект систему агентов. Шаблон возьми в репозитории https://github.com/MaximKolomeets/agent-system-development
```

В этом режиме `engine` обязан сам найти в template repository:

- `docs/agent-system/ENGINE_ENTRYPOINT.md`;
- `docs/agent-system/ENGINE_SELF_DISCOVERY_CONTRACT.md`;
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`;
- `docs/agent-system/templates/SHORT_TARGET_ADOPTION_PROMPT.md`.

До любых изменений `engine` выполняет repository self-discovery в текущем target repository, читает локальные инструкции и применяет safety gate. Первый результат должен быть adoption audit, а не полный перенос всех файлов template repository.

Если текущий repository не соответствует задаче, есть риск секретов, working tree не чистый без разрешения пользователя или локальные инструкции запрещают действие, `engine` пишет `STOP` и не меняет файлы.

## Adoption mode selection

Перед переносом файлов выбрать режим по документу:

```text
docs/agent-system/ADOPTION_GUIDE.md
```

Режимы:

- `audit-only` - первый безопасный dry run, результатом является только `docs/agent-system/ADOPTION_AUDIT.md`;
- `docs-only adoption` - адаптированная документационная система без runtime changes;
- `runtime adoption` - отдельный runtime scope только после архитектурного решения target repository.

Для проверки переносимых файлов использовать manifest:

```text
docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml
```

Файлы из category `template_state_do_not_copy_verbatim` нельзя копировать дословно. Файлы из category `requires_target_adaptation` нужно переписать под target repository.

## Methodology reference

Перед adoption/update `engine` должен синхронизировать methodology repository и зафиксировать точный commit SHA, который используется как reference.

Target audit, TASK/RESULT и optional target-local manifest должны содержать:

```yaml
methodology_reference:
  repository: MaximKolomeets/agent-system-development
  source_branch: developer
  source_commit: <commit-sha>
  checked_at: <ISO-8601 timestamp>
  reference_type: commit
  notes: <short Russian note>
```

Если commit SHA недоступен, нельзя выполнять docs-only adoption как ready-for-review. Нужно написать `STOP` или оставить audit blocker.

Tags/releases пока не являются обязательным versioning layer. Их можно добавить отдельной задачей после проверки real adoption flow.

Перед docs-only adoption и review использовать checklist:

```text
docs/agent-system/DOWNSTREAM_ADAPTATION_CHECKLIST.md
```

Governance pack для target repository описан в:

```text
docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
```

## Engine journal adoption

Target repository должен получить собственный journal:

```text
docs/agent-system/engine-journal/
```

Transfer only scaffold, templates, README, INDEX, and the contract. Do not copy
methodology repository operational history. The first target adoption/audit task
creates target-specific task/result files and the target-specific index entry.

Первый adoption/audit PR должен создать или проверить:

- `docs/agent-system/engine-journal/README.md`;
- `docs/agent-system/engine-journal/INDEX.md`;
- `docs/agent-system/engine-journal/input/`;
- `docs/agent-system/engine-journal/output/`;
- `docs/agent-system/engine-journal/templates/`;
- task file для первой engine-задачи;
- result file для ответа engine.

Journal files являются project-specific execution history target repository. Их нельзя переносить обратно в public methodology repository, кроме нейтральных улучшений methodology templates.

## Feedback to methodology repository

После target repository dry run `engine` должен собрать нейтральные предложения по улучшению methodology repository.

Feedback может включать:

- что было неясно в template repository;
- каких шаблонов или инструкций не хватило;
- какие ручные шаги стоит автоматизировать;
- какие safety rules нужно усилить;
- какие конфликты с локальными правилами target repository возникли;
- какие отдельные PR стоит создать в `agent-system-development`.

Private data из target repository не переносится в public methodology repository. Нельзя публиковать реальные credentials, tokens, passwords, API keys, `.env`, клиентские данные, персональные данные, внутренние кодовые имена, private repository URL или приватные логи.

Перед переносом feedback в methodology repository нужно выполнить sanitization:

- заменить concrete repository names на `target implementation repository`;
- заменить private paths на обобщенные path categories;
- убрать branch names, PR numbers, SHA и timestamps target repository, если они не нужны для универсального правила;
- убрать client/customer/person names и внутренние кодовые имена;
- не цитировать private logs, prompts или file contents;
- оставить только generalized problem, reusable rule, affected methodology docs/templates и proposed neutral acceptance criteria.

Если feedback нельзя безопасно обобщить, он остается в target/private notes и не переносится в public methodology repository.

Feedback не меняет methodology repository автоматически. Пользователь переносит только безопасную обобщенную часть в ChatGPT, после чего изменения оформляются отдельной задачей, отдельной веткой и отдельным PR в `agent-system-development`.

## 1. Подготовить target repository profile

Использовать шаблон:

```text
docs/agent-system/templates/PROJECT_PROFILE_TEMPLATE.md
```

Заполнить поля:

- project name;
- visibility;
- goal;
- non-goals;
- repository name;
- roles;
- branch policy;
- forbidden data;
- first milestone;
- first PR;
- acceptance criteria.

Profile должен быть нейтральным и не должен переносить приватные данные target repository обратно в public methodology repository.

## 2. Проверить visibility и публикационные ограничения

- Если target repository public, все материалы считаются публичными.
- Если target repository private, секреты все равно не должны попадать в Git.
- Public methodology repository и target implementation repository имеют разные уровни доступа.
- Нельзя переносить приватные данные target repository обратно в public methodology repository.

Visibility target repository не наследуется автоматически от public methodology repository. Решение о visibility принимает пользователь.

## 3. Создать базовую структуру target repository

Использовать шаблон:

```text
docs/agent-system/templates/NEW_REPOSITORY_STRUCTURE_TEMPLATE.md
```

Нейтральная структура:

```text
README.md
AGENTS.md
.gitignore
PROJECT_CONSTITUTION.md
docs/agent-system/
docs/agent-system/CURRENT_STATE.md
docs/agent-system/NEXT_STEPS.md
docs/agent-system/DECISION_LOG.md
docs/agent-system/BRANCH_POLICY.md
docs/agent-system/WORKFLOW.md
docs/agent-system/PR_WORKFLOW.md
docs/agent-system/ROLE_MODEL.md
docs/agent-system/PUBLICATION_POLICY.md
docs/agent-system/templates/
docs/agent-system/agents/
docs/agent-system/engine-journal/
```

Структура может адаптироваться под target repository, но bootstrap должен оставаться маленьким и проверяемым.

## 3a. Подготовить target project governance pack

До docs-only adoption нужно создать или адаптировать governance pack, чтобы проект не уходил от цели, roadmap и scope.

Использовать:

```text
docs/agent-system/TARGET_PROJECT_GOVERNANCE_PACK.md
docs/agent-system/PROJECT_CONSTITUTION_FRAMEWORK.md
docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md
```

Создать или адаптировать в target repository:

- `PROJECT_CONSTITUTION.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `RUNBOOK.md`;
- `DECISIONS.md` или `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`.

Эти файлы содержат target-specific state и не копируются verbatim из methodology repository. Они пишутся по фактам target repository. `PROJECT_CONSTITUTION.md` фиксирует mission, success criteria, out-of-scope, architectural principles, current strategic goal, decision authority и scope expansion control.

## 4. Адаптировать документы

Можно переносить как основу:

- `AGENTS.md`;
- README sections about workflow;
- branch policy;
- workflow;
- PR workflow;
- role model;
- publication policy;
- governance pack templates;
- templates.

Нужно адаптировать:

- project name;
- repository name;
- visibility;
- roles;
- first milestone;
- first PR;
- CI needs;
- branch model;
- worktree paths;
- forbidden data list;
- handoff text.

При адаптации не переносить реальные credentials, tokens, passwords, API keys, `.env`, клиентские данные, персональные данные или внутренние кодовые имена.

`CURRENT_STATE.md`, `NEXT_STEPS.md` и `DECISION_LOG.md` из methodology repository нельзя копировать verbatim. Они должны быть заново написаны по фактам target repository.

## 5. Создать ветки и worktree

Рекомендуемая схема веток:

- `main`;
- `developer`;
- `work/<role>/*`.

Нейтральный пример локальных путей:

```text
C:\Neural\repos\<target-repository-name>
C:\Neural\worktrees\<target-repository-name>\<role-name>
```

Каждая рабочая задача выполняется в отдельной ветке `work/<role>/<task>` от актуальной `developer`.

Если target repository использует `develop` вместо `developer` или другую branch model, нужно адаптировать branch policy, PR workflow, task templates и CI branch filters. Не переименовывать ветки без отдельного решения пользователя.

## 6. Подготовить первый bootstrap PR

Первый PR должен быть маленьким и проверяемым.

Пример первого PR:

- добавить `README.md`;
- добавить `AGENTS.md`;
- добавить `.gitignore`;
- добавить `docs/agent-system` минимальный набор;
- добавить templates;
- не добавлять рабочие данные.

Bootstrap PR не должен смешиваться с implementation PR.

Minimal first PR после короткого adoption prompt должен создавать только:

```text
docs/agent-system/ADOPTION_AUDIT.md
docs/agent-system/engine-journal/**
```

Полный docs-only bootstrap планируется только после audit, engine journal result и Methodology feedback.

## 6a. PowerShell/UTF-8 note

Русские Markdown-файлы читать как UTF-8:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
Get-Content -Encoding UTF8 -Raw .\docs\agent-system\CURRENT_STATE.md
```

Если среда выводит mojibake, это нужно фиксировать как environment note и перечитать файл с явным UTF-8 режимом.

## 7. Проверить forbidden files

Запрещенные пути:

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

Команды проверки:

```bash
git status --short
```

```bash
git ls-files
```

```bash
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --
```

Sensitive grep работает в filename-only режиме и должен печатать только имена файлов. Matching lines нельзя печатать в терминал, отчет или логи engine. Если найдено подозрение на реальный секрет, не печатать его дальше и остановиться для решения пользователя.

## 8. Запустить engine

- ChatGPT формирует задачу.
- Пользователь запускает engine вручную.
- `engine` работает только в рабочей ветке.
- `engine` не читает `.env`.
- `engine` не меняет `main`/`developer` напрямую.
- `engine` пишет отчет.

`engine` не должен расширять scope задачи без отдельного решения пользователя.

Задача для `engine` должна быть на русском языке и начинаться с обязательной шапки:

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>
```

`<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта. Это связывает задачу, ветку, отчет и Pull Request.

## 9. Проверить отчет engine

Отчет должен содержать:

- engine result file;
- рабочая ветка;
- что создано;
- что изменено;
- changed files;
- проверки;
- что не проверялось;
- риски;
- next step;
- commit SHA;
- PR link/number.

Если отчет не содержит result file, проверок, рисков или changed files, его нужно уточнить перед review/merge.

## 10. Провести review и merge

Стандартный поток:

```text
work/<role>/<task> -> developer -> main
```

PR из рабочей ветки идет в `developer`. После проверки стабильное состояние переносится из `developer` в `main`.

Если ruleset запрещает direct push, sync developer после release выполняется через PR.

## 11. Подготовить handoff

Использовать шаблон:

```text
docs/agent-system/templates/NEW_PROJECT_HANDOFF_TEMPLATE.md
```

Handoff нужен для нового чата или новой рабочей сессии. Он фиксирует repository, visibility, current branches, active PR, completed PRs, important docs, current goal, next PR, risks и exact prompt for continuation.

## 12. Что нельзя делать

- Не переносить приватные данные в public methodology repository.
- Не переносить `.env`.
- Не коммитить runtime/work data.
- Не давать engine прямой push в `main`/`developer`.
- Не смешивать bootstrap с implementation.
- Не использовать vendor/tool names в названиях ролей.
- Не считать public/private visibility одинаковыми для разных repositories.
