# NON_TECHNICAL_ARCHITECT_GUIDE

## Назначение

Этот guide помогает архитектору или владельцу проекта управлять разработкой без
обязанности быть программистом.

Главная роль архитектора — определить **что** должно быть сделано, зачем это
нужно, какие границы нельзя нарушать и когда человек должен принять решение.
Роль исполнителя — выбрать безопасный способ **как** это сделать внутри
утвержденного scope.

## Минимальный путь

Если вы не программист, начинайте так:

1. Прочитать этот guide.
2. Открыть `ARCHITECT_COCKPIT.md` и ответить на вопросы дня.
3. Заполнить или проверить `PROJECT_OPERATOR_DASHBOARD.md` по шаблону
   `docs/agent-system/templates/PROJECT_OPERATOR_DASHBOARD_TEMPLATE.md`.
4. Для передачи проекта другому человеку использовать
   `ARCHITECT_HANDOFF_PACK.md`.
5. Для merge/tag/publish/sync/rollback смотреть `HUMAN_GATE_POLICY.md` и
   `RELEASE_AUTHORITY_POLICY.md`: эти действия не делает агент сам.

## Глоссарий

| Термин | Простой смысл |
| --- | --- |
| Branch | Отдельная рабочая линия изменений, чтобы не менять стабильную версию напрямую. |
| Commit | Зафиксированный набор изменений с описанием. |
| Pull Request / PR | Запрос на проверку и merge изменений из branch. |
| Merge | Включение проверенных изменений в целевую branch. |
| Push | Отправка локальных commits в GitHub. |
| Fetch | Получение свежей информации из GitHub без изменения рабочей branch. |
| Pull | Получение и применение свежих изменений из GitHub. |
| Tag | Метка стабильного release commit. |
| Release | Опубликованная стабильная версия или release boundary. |
| Check | Автоматическая или ручная проверка. |
| Blocker | Проблема, из-за которой нельзя продолжать без исправления или решения человека. |
| Scope | Разрешенные границы задачи: файлы, действия и решения. |
| Journal | TASK/RESULT/INDEX trace: какая задача дала какой PR и какой итог. |
| Human Gate | Действие, которое должен выполнить или одобрить человек. |
| UAT | Ручная business acceptance проверка owner/PO перед release. |

## Human vs auto

| Действие | Кто делает | Почему |
| --- | --- | --- |
| Формулирует mission, priority, success criteria | Человек-архитектор/owner | Это решение о смысле проекта, не implementation detail. |
| Выбирает next safe task | Человек с помощью orchestrator | Нужна business/context judgement. |
| Пишет task scope, allowed files, checks и STOP | Orchestrator/architect | Это управленческая рамка для executor. |
| Делает file changes в task branch | Engine/executor | Это implementation внутри утвержденного scope. |
| Запускает проверки и готовит evidence | Engine/executor | Это воспроизводимая техническая работа. |
| Делает scoped review | Reviewer | Нужна независимая проверка качества. |
| Merge в `main`, tag, publish, rollback decision | Только человек | Это human-only release authority. |
| Branch protection/rulesets, CI/CD, prod-secrets | Только человек или явно уполномоченный owner | Высокий operational risk. |
| Финансовые решения и удаление данных | Только человек | Нельзя автоматизировать без explicit approval. |

## Как управлять PR без программирования

Перед тем как разрешить merge, попросить у engine или reviewer короткий отчет:

- какой task id и branch;
- какой PR URL;
- какие files изменены и почему;
- какие checks прошли;
- есть ли blockers или warnings;
- есть ли unresolved placeholders в RESULT/INDEX;
- есть ли human-only actions;
- есть ли private data, secrets или `.env` risk;
- что будет следующим безопасным шагом.

Не принимать PR, если:

- нет понятного task scope;
- нет финализированного RESULT/INDEX для file-changing task;
- checks не запускались без объяснения;
- есть blocker;
- изменены файлы вне allowed scope;
- PR просит человека выполнить merge/tag/publish/sync/rollback без evidence;
- непонятно, соответствует ли изменение mission/current goal.

## Что просить у engine

Можно не запускать команды самому. Достаточно попросить engine выполнить и
пересказать safe summary:

```text
Проверь baseline, branch, PR state, changed files, blockers, checks и journal finalization.
Не печатай secrets или matching lines; покажи только filenames/counts/status.
```

Для текущего repository стандартный ready-gate:

```text
python docs/agent-system/tools/check_task_ready.py --base origin/developer
```

Для language hygiene:

```text
python docs/agent-system/tools/russian_first_lint.py --base origin/developer
```

## STOP для не-программиста

Остановиться и запросить помощь, если:

- engine просит прямой push в `main` или `developer`;
- нужно менять branch protection, CI/CD, production secrets или finance settings;
- нужно удалить данные;
- нужно делать rollback/hotfix final decision;
- есть конфликт между mission/scope и предлагаемой задачей;
- отчет содержит реальные credentials, tokens, cookies или private repository URL;
- PR непонятен после короткого explanation.

## Передача

Следующий: architect/operator — использовать `ARCHITECT_COCKPIT.md` для
ежедневного управления и `ARCHITECT_HANDOFF_PACK.md` для передачи проекта другому
архитектору или в новую рабочую сессию.
