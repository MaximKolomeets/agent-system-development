# WORKFLOW

1. Пользователь принимает решение.
2. ChatGPT помогает сформулировать задачу.
3. Задача оформляется по шаблону.
4. Исполнитель работает в своей ветке.
5. Исполнитель обновляет отчет.
6. Проверяющий агент делает review.
7. Пользователь принимает решение о merge.
8. После merge обновляются `CURRENT_STATE` и `DECISION_LOG`, если нужно.

## После bootstrap

- Прямые изменения в `developer` запрещены без отдельного разрешения пользователя.
- Рабочий поток идет через ветки `work/<role>/*`.
- Рабочая ветка создается от актуальной `developer`.
- `developer` принимает изменения через PR из рабочих веток.
- `developer` -> `main` выполняется только после проверки интеграционной ветки.

## Review-only workflow

Code review / external review / consulting review по умолчанию выполняется как review-only task:

```text
developer -> work/<reviewer-role>/<task-id> -> PR в developer
```

Review report по умолчанию возвращается в чат. Review-only PR создается только если пользователь явно разрешил docs-only сохранение отчета в repository.

Review-only PR содержит только review report files и journal/state updates, если они явно разрешены задачей.

Reviewer не исправляет production code, runtime, Docker, CI, scripts или dependencies. Findings превращаются в отдельные implementation PR только после решения пользователя.

Reviewer не запускает Codex/Engine, не меняет очередь исполнителя и не формулирует себе implementation task. Он может предложить кандидаты на будущие задачи, но решение принимает пользователь вместе с ChatGPT.

Review task должен явно указывать:

- режим: `review-only`, `docs-only` или `fix-allowed`;
- объект проверки: PR, branch, commit, diff или files;
- base branch;
- working branch, если нужна;
- allowed files;
- forbidden files;
- разрешенные и запрещенные команды;
- можно ли сохранять отчет в repository;
- можно ли создавать PR.

Для standard developer workflow review стартует от `developer`, конкретного PR/diff/branch/commit/files. `main` используется только если пользователь явно указал, что нужно проверить стабильную версию.

Подробный контракт:

```text
docs/agent-system/CODE_REVIEW_WORKFLOW.md
```

## Локальные действия после PR/merge

Если задача создала PR, была смержена, обновила remote `developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`, финальный отчет в чат должен содержать конкретный блок:

```text
## Локальные действия после PR/merge
```

Блок должен включать команды для текущего repository и затронутых веток. Запрещено рекомендовать `git reset --hard`, если пользователь явно не подтвердил, что локальные изменения и локальные commits не нужны.
