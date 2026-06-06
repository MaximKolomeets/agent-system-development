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

## work/security-reviewer-01/*

- проверки безопасности.

## work/docs-maintainer-01/*

- документация и Source summaries.

## Запрещено

- force push в `main`/`developer`;
- прямой push агентами в `main`;
- прямой push агентами в `developer` после bootstrap;
- смешивать несколько независимых задач в одной ветке.
