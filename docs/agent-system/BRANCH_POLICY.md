# BRANCH_POLICY

## main

- стабильная ветка;
- изменения только через PR из `developer`;
- прямой push запрещен для агентов;
- force push запрещен.

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
