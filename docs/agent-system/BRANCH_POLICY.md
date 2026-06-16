# BRANCH_POLICY

## main

- стабильная ветка;
- изменения только через PR из `developer`;
- прямой push запрещен для агентов;
- force push запрещен.

### Обновление main (канон, правило 1)

- `main` обновляется ТОЛЬКО через release-PR `developer -> main`;
- release-PR мержит человек-архитектор (пользователь), а не агент;
- агент может ПОДГОТОВИТЬ release-PR (создать release-ветку/PR из `developer` в `main`), но НЕ мержит его и НЕ пушит в `main` напрямую;
- агент не делает merge release-PR даже при наличии прав; решение о переносе в `main` принимает человек.

## developer

- интеграционная ветка;
- изменения только через PR из `work/<role>/*`;
- прямой push запрещен после bootstrap, кроме отдельного решения пользователя;
- после merge в `main` должна быть синхронизирована с `main`.

## work/<role>/*

- рабочие ветки задач;
- одна задача = одна ветка;
- ветка создается от актуальной `developer`;
- после merge может быть удалена.

### Изоляция веток агентов (канон, правило 2)

- каждый агент действует ТОЛЬКО в своих ветках `work/<role>/<task>` своего role namespace;
- запрещено пушить, менять, force-пушить, переименовывать или удалять ветку другого агента (другого `work/<role>/*`);
- агент не строит свою работу поверх чужой непримёрженной рабочей ветки без отдельного решения пользователя;
- передача работы между агентами выполняется ТОЛЬКО через merged PR в `developer`, а не через правку чужих веток;
- если нужна работа поверх результата другого агента, сначала его PR мержится в `developer`, затем новая ветка создаётся от актуальной `developer`.

### Pre-commit branch guard (канон, правило 3)

- перед ЛЮБЫМ `git commit` агент проверяет текущую ветку: `git rev-parse --abbrev-ref HEAD`;
- если HEAD не его рабочая ветка задачи `work/<role>/<task>` (особенно если это `developer` или `main`) → `STOP`, переключиться на правильную work-ветку и только потом коммитить;
- прямой коммит в `developer` или `main` запрещён даже локально (не только push); локальный коммит в `developer`/`main` считается нарушением, даже если он ещё не запушен;
- обоснование: инцидент journal 0013 — resume сессии оставил HEAD на `developer`, и коммит сначала лёг туда; remote `developer` уцелел только потому, что пушилась work-ветка. Проверка ветки перед commit предотвращает это.

## work/dev-implementer-01/*

- задачи разработки.

## work/solution-architect-01/*

- архитектурные исследования и предложения.

## work/qa-reviewer-01/*

- проверки качества и тестов.

## work/code-reviewer-01/*

- code review, external review и consulting review;
- review-отчеты и findings;
- не используется для исправления production-кода без отдельной implementation task.

## work/security-reviewer-01/*

- проверки безопасности.

## work/docs-maintainer-01/*

- документация и Source summaries.

## Запрещено

- force push в `main`/`developer`;
- прямой push агентами в `main`;
- прямой push агентами в `developer` после bootstrap;
- смешивать несколько независимых задач в одной ветке.
- использовать model/vendor-specific ветки вроде `claude/*`, `gpt/*` или `gemini/*`.

## Review branch policy

Канонический namespace для review-задач в standard developer workflow:

```text
work/<reviewer-role>/<task-id>
```

Примеры:

```text
work/code-reviewer-01/<task-id>
work/qa-reviewer-01/<task-id>
work/security-reviewer-01/<task-id>
```

Namespace `review/*` не используется как канонический branch namespace этого repository без отдельного будущего решения пользователя и обновления branch policy.

Если review-отчет разрешено сохранить в repository, это остается docs-only работой в ветке `work/<reviewer-role>/<task-id>` с PR в `developer`.
