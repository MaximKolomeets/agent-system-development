# PROJECT_LIFECYCLE

Этот документ описывает универсальный жизненный цикл запуска нового проекта через `agent-system-development`.

GitHub является source of truth: в репозитории фиксируются файлы, история изменений, ветки, pull request, отчеты агентов, решения и текущее состояние. Чат помогает формулировать задачи и разбирать отчеты, но не заменяет GitHub.

Пользователь принимает финальные решения по scope, visibility, merge, release и изменениям правил. ChatGPT помогает структурировать описание проекта, формулировать задачи, проверять отчеты и готовить handoff. Engine-исполнители запускаются пользователем вручную и работают только в заданных ветках и каталогах.

## 1. Idea

Пользователь описывает новый проект: цель, ожидаемый результат, ограничения, публичность, риски и первый полезный milestone.

На этой стадии важно отделить:

- цель проекта;
- non-goals;
- данные, которые нельзя хранить в репозитории;
- ожидаемый уровень публичности;
- минимальный первый результат.

## 2. Project profile

На основе идеи создается нейтральный project profile. Он фиксирует название проекта, repository name, visibility, роли, engines, security constraints, forbidden data, первый milestone, первый PR и acceptance criteria.

Project profile не должен содержать реальные секреты, клиентские данные, персональные данные, внутренние кодовые имена или конкретные внешние проекты.

## 3. Repository bootstrap

Создается новый пустой GitHub repository. Затем добавляется минимальная структура:

- `README.md`;
- `AGENTS.md`;
- `.gitignore`;
- `docs/agent-system/`;
- базовые state/policy/workflow документы.

Repository bootstrap должен быть достаточно малым, чтобы его было легко проверить первым PR.

## 4. Branch policy setup

Определяются ветки:

- `main` как стабильная ветка;
- `developer` как интеграционная ветка;
- `work/<role>/*` как namespace рабочих веток.

После bootstrap прямые изменения в `main` и `developer` запрещаются процессом или rulesets/branch protection, если они доступны для выбранного repository visibility.

## 5. Role/worktree setup

Определяются роли агентов и локальные worktree-папки. Роли называются по ответственности, а не по vendor/tool name. Конкретный исполнитель указывается отдельно как `engine`.

Каждая задача выполняется в отдельной ветке:

```text
work/<role>/<task>
```

## 6. First documentation PR

Первый documentation PR фиксирует базовую методологию проекта:

- текущее состояние;
- следующие шаги;
- decision log;
- branch policy;
- workflow;
- PR workflow;
- publication/security policy;
- templates.

Цель этого PR - сделать дальнейшую работу проверяемой.

## 7. First implementation PR

Первый implementation PR добавляет минимальный полезный результат проекта. Он должен быть маленьким, проверяемым и связанным с первым milestone.

Если проект пока не готов к реализации, первым implementation PR может быть технический guardrail: CI, checks, scaffolding или безопасный skeleton.

## 8. Review cycle

Каждый PR проходит review:

- changed files;
- соответствие scope;
- отсутствие forbidden data;
- прохождение CI guardrails;
- обновление отчетов;
- обновление state/decision docs, если изменилось состояние или принято решение.

Если CI или review обнаружили нарушение, исправления выполняются в той же рабочей ветке.

## 9. Developer stabilization

После merge рабочих PR в `developer` интеграционная ветка проверяется как единое состояние. На этом этапе можно:

- сверить документацию;
- проверить guardrails;
- подтвердить следующий milestone;
- подготовить перенос в `main`.

## 10. Main release

После проверки `developer` переносится в `main`. `main` отражает стабильное состояние проекта и используется как точка handoff для следующего цикла.

После release нужно обновить state документы, если изменились current stage, next steps или важные решения.

## 11. Handoff to next chat/session

Для нового чата или новой рабочей сессии готовится handoff:

- repository;
- visibility;
- current main/developer;
- active branch;
- current PR;
- completed PRs;
- active rules;
- forbidden files;
- important docs to read;
- current goal;
- next PR;
- risks;
- exact prompt for continuation.

Handoff должен позволять продолжить работу без устных предположений и без переноса приватных данных в public repository.
