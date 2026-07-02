# ARCHITECT_COCKPIT

## Назначение

Architect cockpit — человеко-читаемый слой поверх строгих policy. Он помогает
архитектору управлять проектом вопросами, а не чтением всех канонов каждый день.

Cockpit не заменяет `WORKFLOW.md`, `BRANCH_POLICY.md`, `HUMAN_GATE_POLICY.md`,
`RELEASE_AUTHORITY_POLICY.md` или `PROJECT_CONSTITUTION_FRAMEWORK.md`. Если
cockpit и policy расходятся, действует профильный policy.

## Ежедневные вопросы

- Какой один next safe step сегодня?
- Есть ли active PR, который ждет review, fix-pass или human merge?
- Есть ли blocker, warning или missing evidence?
- Не устарели ли `CURRENT_STATE.md`, `NEXT_STEPS.md` или project dashboard?
- Есть ли human-only action, который агент не должен выполнять?
- Не появился ли scope creep: новая platform, service, runtime, finance или
  strategy change?
- Есть ли риск private data/secrets в public repository?

## Еженедельные вопросы

- Текущая strategic goal все еще актуальна?
- Есть ли stale PRs, stale branches или незакрытые journal entries?
- Какие decisions были приняты за неделю и отражены ли они в decision log?
- Какие target repositories или source consumers нужно обновить после release?
- Есть ли накопленные missing time/cost reports?
- Нужен ли handoff pack перед отпуском, паузой или сменой owner?

## Перед обычным PR merge

Спросить у engine/reviewer:

- task id, branch и PR URL;
- финализированы ли TASK/RESULT/INDEX;
- прошел ли `check_task_ready.py --base origin/developer`;
- есть ли `russian_first_lint_result: passed`;
- есть ли unresolved placeholders;
- есть ли files вне allowed scope;
- есть ли private data, secrets или `.env` risk;
- что изменится для пользователя или проекта;
- какой next safe step после merge.

Не принимать PR, если ответ непонятен или содержит blocker.

## Перед release

Проверить:

- release authority actor определен;
- Business Acceptance Gate пройден или явно `not_applicable` с причиной;
- UAT evidence есть;
- release PR `developer -> main` готов, но merge выполняет человек;
- tag/publish/sync decision выполняет человек;
- rollback plan известен;
- `RELEASE_READINESS.md` и `NEXT_STEPS.md` актуальны.

## Перед adoption/source-update

Проверить:

- stable methodology reference не указывает на `developer` или `work/*`;
- manifest categories применены;
- target-local docs адаптируются по target facts;
- private target data не переносится в public methodology;
- Russian-first policy добавлена в target instructions;
- handoff pack или dashboard показывает next safe step.

## Красные флаги

- "Можно быстро смержить без review".
- "Нужно просто push в main".
- "Секреты в истории не страшно, мы удалили файл".
- "RESULT/INDEX допишем потом".
- "Это маленькое изменение CI/CD/branch protection".
- "Новая architecture direction без отдельного решения".
- "Target private details можно записать в public methodology".
- "Reviewer сам исправит production files".

Любой красный флаг означает STOP или отдельное explicit human decision.

## Что попросить у engine

Безопасный запрос:

```text
Собери management summary: branch, PR URL, changed files, checks, blockers,
human-only actions, journal status, next safe step. Secrets не печатать.
```

Для handoff:

```text
Заполни ARCHITECT_HANDOFF_PACK safe summary без private data и secret values.
```

Для dashboard:

```text
Обнови PROJECT_OPERATOR_DASHBOARD по template: yes/no поля, blockers, next safe step.
```

## Связанные документы

- `NON_TECHNICAL_ARCHITECT_GUIDE.md`;
- `ARCHITECT_HANDOFF_PACK.md`;
- `docs/agent-system/templates/PROJECT_OPERATOR_DASHBOARD_TEMPLATE.md`;
- `ROLE_MODEL.md`;
- `PROJECT_CONSTITUTION_FRAMEWORK.md`;
- `HUMAN_GATE_POLICY.md`;
- `RELEASE_AUTHORITY_POLICY.md`;
- `UAT_WORKFLOW.md`;
- `HOTFIX_AND_ROLLBACK_POLICY.md`.

## Передача

Следующий: architect/operator — заполнить operator dashboard и выбрать один
next safe step; если есть красный флаг, вернуть STOP.
