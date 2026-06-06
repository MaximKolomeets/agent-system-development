# BRANCH_POLICY

## main

- стабильная ветка;
- не менять напрямую агентами;
- перенос только после проверки `developer`.

## developer

- интеграционная ветка;
- первая рабочая ветка для bootstrap;
- после bootstrap прямые изменения в `developer` только по отдельному разрешению пользователя.

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
