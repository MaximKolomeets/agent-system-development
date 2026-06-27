# NEW_PROJECT_ONBOARDING_GUIDE

## Stable methodology reference

Новый target/downstream project читает methodology repository из stable reference: `origin/main` / `main`, явно заданный release tag или published Source/cloud snapshot. `developer`, `work/*`, dirty local methodology tree и open methodology PR branch не являются source of truth для onboarding.

Dirty рабочая ветка в `agent-system-development` не блокирует onboarding, если stable reference доступен. Для чтения методологии не выполнять `git switch`, `git checkout`, `git pull`, `git reset`, `git clean` или `git stash` в рабочем methodology repository.

Все onboarding TASK/RESULT/INDEX, final report, PR title/body, commit message и target-local docs/templates пишутся по Russian-first policy.

## Назначение

Этот документ помогает пользователю запустить новый проект через lifecycle и templates из `agent-system-development`.

GitHub является source of truth: в репозитории фиксируются файлы, история изменений, ветки, pull request, отчеты, решения и текущее состояние. Чат помогает формулировать задачи и проверять отчеты, но не заменяет GitHub. Пользователь принимает финальные решения по scope, visibility, merge, release и изменению правил. Исполнители (engine) запускаются пользователем вручную.

`agent-system-development` используется как reusable methodology/template repository. Он не становится центральным репозиторием управления новым проектом: после adoption все рабочие ветки, worktree, отчеты, Pull Request и project-specific state ведутся в repository нового проекта.

Для запуска adoption в уже существующем target repository используйте canonical copy/paste prompt:

```text
docs/agent-system/templates/ADOPTION_PROMPT.md
```

Для нового пустого repository — раздел «Полный bootstrap prompt нового проекта» там же. Пошаговый перенос в существующий repository описан в `docs/agent-system/ADOPTION_GUIDE.md` → раздел «Пошаговый existing-repo adoption».

## Жизненный цикл (стадии 1–11)

Перед практическими шагами ниже полезно держать в голове концептуальный жизненный цикл нового проекта (обзорная стадийная модель; ранее жила в отдельном `PROJECT_LIFECYCLE.md`):

1. **Idea** — цель, ожидаемый результат, ограничения, публичность, запрещённые данные, минимальный первый milestone; отделить цель от non-goals.
2. **Project profile** — нейтральный профиль: название, repository name, visibility, роли, engines, security constraints, forbidden data, первый milestone, первый PR, acceptance criteria.
3. **Repository bootstrap** — новый пустой GitHub repository + минимальная структура (`README.md`, `AGENTS.md`, `.gitignore`, `docs/agent-system/`, базовые state/policy/workflow docs), достаточно малая для проверки одним PR.
4. **Branch policy setup** — `main` (стабильная), `developer` (интеграционная), `work/<role>/<task>` (основная task branch), `work/<role>/<task>/*` (внутренние sub-branches при необходимости); после bootstrap прямые изменения в `main`/`developer` запрещены процессом или rulesets/branch protection.
5. **Role/worktree setup** — роли по ответственности (без vendor/tool names), исполнитель отдельно как `engine`; каждая substantive task — в основной `work/<role>/<task>`.
6. **First documentation PR** — базовая методология проекта (current state, next steps, decision log, branch/PR workflow, publication/security policy, templates), чтобы дальнейшая работа была проверяемой.
7. **First implementation PR** — минимальный полезный результат, связанный с первым milestone; если рано — технический guardrail (CI, checks, scaffolding, безопасный skeleton).
8. **Review cycle** — для каждого PR: changed files, соответствие scope, отсутствие forbidden data, прохождение CI guardrails, обновление отчётов и state/decision docs; исправления в той же рабочей ветке.
9. **Developer stabilization** — после merge рабочих PR `developer` проверяется как единое состояние: сверить документацию, guardrails, подтвердить следующий milestone, подготовить перенос в `main`.
10. **Main release** — после проверки `developer` переносится в `main` (стабильное состояние и точка handoff); обновить state docs, если изменились current stage, next steps или решения.
11. **Handoff to next chat/session** — зафиксировать repository, visibility, current `main`/`developer`, active branch, current/completed PR, active rules, forbidden files, important docs, current goal, next PR, risks и exact prompt for continuation.

Практические how-to шаги ниже разворачивают эти стадии в конкретные действия.

## 1. Описать идею проекта

Пользователь кратко описывает:

- цель;
- ожидаемый результат;
- ограничения;
- public/private visibility;
- запрещенные данные;
- первый полезный milestone.

На этом шаге важно отделить желаемый результат от non-goals и заранее указать, какие данные нельзя хранить в repository.

## 2. Заполнить профиль проекта (project profile)

Использовать шаблон:

```text
docs/agent-system/templates/PROJECT_PROFILE_TEMPLATE.md
```

Project profile должен быть нейтральным и не должен содержать:

- реальные credentials;
- tokens;
- passwords;
- API keys;
- `.env`;
- клиентские данные;
- персональные данные;
- внутренние кодовые имена;
- конкретные внешние проекты.

Project profile нужен, чтобы перед bootstrap было понятно, что создается, какие роли нужны, какие ограничения действуют и какой первый PR считается успешным.

## 3. Подготовить новый GitHub repository

Создать пустой repository и осознанно выбрать visibility:

- `public` - все содержимое считается публичным;
- `private` - доступ ограничен, но секреты и приватные данные все равно не должны попадать в Git без явного решения пользователя.

Для public repository нельзя переносить приватные данные, клиентские данные, персональные данные, рабочие файлы или внутренние кодовые имена.

## 4. Создать базовую структуру repository

Использовать шаблон:

```text
docs/agent-system/templates/NEW_REPOSITORY_STRUCTURE_TEMPLATE.md
```

Минимальная структура:

```text
README.md
AGENTS.md
.gitignore
docs/agent-system/
docs/agent-system/templates/
docs/agent-system/agents/
```

На bootstrap-этапе структура должна быть маленькой и проверяемой. Дополнительные папки и CI лучше добавлять отдельными PR, если они не нужны сразу.

## 4a. Подготовить governance pack

Новый проект должен получить governance pack до первых implementation PR. Это снижает риск, что engine уведет проект в сторону от цели или начнет работу без понятного roadmap, backlog, guardrails и state docs.

Минимальный набор:

- `PROJECT_CONSTITUTION.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `RUNBOOK.md`;
- `docs/agent-system/CURRENT_STATE.md`;
- `docs/agent-system/NEXT_STEPS.md`;
- `docs/agent-system/BACKLOG.md`;
- `docs/agent-system/DECISION_LOG.md`;
- `docs/agent-system/PROJECT_GUARDRAILS.md`;
- `docs/agent-system/ENGINE_REGISTRY.md`.

Использовать шаблоны:

```text
docs/agent-system/templates/TARGET_PROJECT_GOVERNANCE_PACK_TEMPLATE.md
docs/agent-system/templates/PROJECT_CONSTITUTION_TEMPLATE.md
docs/agent-system/templates/PROJECT_DASHBOARD_TEMPLATE.md
docs/agent-system/templates/ROADMAP_TEMPLATE.md
docs/agent-system/templates/BACKLOG_TEMPLATE.md
docs/agent-system/templates/PROJECT_GUARDRAILS_TEMPLATE.md
docs/agent-system/templates/ENGINE_REGISTRY_TEMPLATE.md
```

Governance pack пишется по фактам target repository и не должен копировать project-specific state из methodology repository.

`PROJECT_CONSTITUTION.md` должен быть подготовлен до первых implementation PR. В нем фиксируются mission, success criteria, out-of-scope, architectural principles, одна active strategic goal, Agent Authority, Decision Authority и Scope Expansion Control.

## 5. Создать ветки

Рекомендуемая схема:

- `main` - stable branch;
- `developer` - integration branch;
- `work/<role>/<task>` - основная task branch.
- `work/<role>/<task>/*` - внутренние sub-branches той же задачи, если они нужны.

После bootstrap прямые изменения в `main` и `developer` запрещаются процессом или rulesets/branch protection. Рабочие изменения идут через один итоговый PR из основной `work/<role>/<task>` в `developer`, затем стабильное состояние переносится из `developer` в `main`.

Для нового repository со стандартной схемой `main -> developer -> work/<role>/<task>` ветка `developer` должна быть создана до первой рабочей задачи `engine`.

Если `developer` отсутствует:

- создать `developer` от актуального `main` вручную или явно разрешенным bootstrap step;
- синхронизировать `origin/developer`;
- только потом создавать основную `work/<role>/<task>` от `developer`.

`engine` не должен открывать первый рабочий PR в `main`, если выбран стандартный workflow с `developer`.

## 6. Настроить worktree

Нейтральный пример локальной структуры:

```text
C:\Neural\repos\<repository-name>
C:\Neural\worktrees\<repository-name>\<role-name>
```

Каждая роль работает в своем worktree. Перед запуском engine-исполнителя пользователь проверяет текущую ветку и статус:

```powershell
git branch --show-current
git status --short
```

## 7. Определить роли и engines

Роли называются по ответственности. Названия ролей не должны содержать vendor/tool names. Конкретный исполнитель указывается отдельно как `engine`.

Примеры ролей:

- `docs-maintainer-01`;
- `dev-implementer-01`;
- `qa-reviewer-01`;
- `security-reviewer-01`;
- `solution-architect-01`.

Пример нейтральной записи:

```text
docs-maintainer-01: engine=<manual or selected engine>
```

## 8. Запланировать первые PR

Рекомендуемый порядок:

1. bootstrap PR;
2. documentation PR;
3. guardrail/CI PR;
4. first implementation PR;
5. review/stabilization PR, если нужен.

Каждый PR должен быть маленьким и проверяемым. Одна substantive task = одна основная task branch и один итоговый PR; внутренние sub-branches допустимы только внутри этой задачи.

## 9. Запустить engine-исполнителя вручную

Обычный порядок:

1. Оркестратор формирует задачу.
2. Пользователь запускает engine вручную.
3. Исполнитель (engine) работает только в своей рабочей ветке.
4. Исполнитель (engine) обновляет отчет.
5. Исполнитель (engine) не меняет `main` или `developer` напрямую.

Если задача требует новой ветки, она создается от актуальной `developer`.

Каждая задача для `engine` формулируется на русском языке и начинается с обязательной шапки:

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

`<роль>` - vendor-neutral роль или функция в методологии. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта, чтобы задачу, ветку, отчет и PR можно было сопоставить.

## 10. Проверить отчет engine

Отчет должен содержать:

- рабочая ветка;
- что сделано;
- какие файлы изменены;
- какие проверки выполнены;
- какие проверки не выполнены и почему;
- риски;
- next step;
- PR number/link.

Если отчет не содержит проверок, changed files или рисков, его нужно уточнить перед merge.

## 11. Провести review и merge

PR идет в `developer`. Перед merge проверяются:

- diff;
- scope;
- CI guardrails;
- forbidden files;
- отсутствие приватных данных;
- обновление state/report docs.

После проверки `developer` переносится в `main`. После release нужно синхронизировать `developer` с `main` через PR, если ruleset запрещает direct push.

## 12. Подготовить handoff

Использовать шаблон:

```text
docs/agent-system/templates/NEW_PROJECT_HANDOFF_TEMPLATE.md
```

Handoff нужен для продолжения в новом чате или новой рабочей сессии. Он должен фиксировать repository, visibility, current branches, active PR, completed PRs, important docs, current goal, next PR, risks и exact prompt for continuation.

## 13. Минимальный чеклист запуска

Полный чеклист:

```text
docs/agent-system/templates/NEW_PROJECT_CHECKLIST.md
```

Краткий checklist:

- [ ] Repository created.
- [ ] Visibility chosen.
- [ ] `.gitignore` created.
- [ ] Forbidden paths protected.
- [ ] `main`/`developer` policy chosen.
- [ ] Work branch namespace chosen.
- [ ] `docs/agent-system/` created.
- [ ] First state files created.
- [ ] First templates created.
- [ ] Rulesets/branch protection checked.
- [ ] First PR planned.
- [ ] CI guardrails planned.
- [ ] Source/index policy defined.

Если любой пункт не выполнен, его нужно либо закрыть до первого PR, либо явно зафиксировать как ограничение и риск.
