# PR_WORKFLOW

1. Пользователь принимает решение о задаче.
2. Оркестратор формирует задачу.
3. Проверяется, что задача выполняется из правильного worktree.
4. Проверяется `git branch --show-current`.
5. Проверяется `git status --short`.
6. Проверяется, что base для рабочей ветки - актуальная `developer`.
7. Исполнитель создает основную task branch `work/<role>/<task>`.
8. Если нужно, исполнитель создает внутренние sub-branches `work/<role>/<task>/*`, сливает их обратно в основную task branch и не открывает по ним отдельные PR в `developer`.
9. Исполнитель меняет только разрешенные файлы, запускает проверки и обновляет отчет.
10. Перед commit/push/PR исполнитель проверяет, что commit messages, PR title и PR body соблюдают Russian-first policy: conventional prefix вроде `docs(agent-system):` допустим, но смысловой текст после `:` пишется на русском; technical identifiers не переводятся.
11. Если commit еще не push, message можно безопасно исправить через `git commit --amend`.
12. Если commit уже push, force-push/rewrite history запрещён без явного решения архитектора; нарушение фиксируется в RESULT/PR body, а правило применяется со следующего commit.
13. Если PR заменяет документ, который остаётся в repository ради истории, внешних bookmarks или inbound links, в начало заменяемого файла добавляется баннер по `docs/agent-system/templates/SUPERSEDED_BANNER.md`: machine-readable comment `SUPERSEDED_BY` и видимая строка для читателя.
14. Исполнитель делает commit и push.
15. Дождаться GitHub Actions CI.
16. Если CI failed - не мержить PR.
17. Исправить нарушения и review feedback в той же основной task branch, если STOP-условия не требуют остановки.
18. Повторить push.
19. Review выполняется только после успешного CI или после осознанного решения пользователя.
20. Пользователь/оркестратор проверяют diff.
21. Создается один итоговый PR в `developer` по substantive task; внутренние sub-branches не являются самостоятельными delivery PR.
22. После проверки PR merge в `developer`.
23. После накопления стабильных изменений `developer` переносится в `main` только через human-merged release PR по `BRANCH_POLICY.md`.
24. После human merge release PR человек-архитектор ставит annotated tag на release merge commit в `main`; агент не создаёт tag и не публикует GitHub Release.
25. После merge обновляются `CURRENT_STATE`, `DECISION_LOG`, `NEXT_STEPS`.

## Review autoloop

Если reviewer оставил blockers/actionable feedback в active work PR:

1. Не создавать отдельный feedback PR.
2. Engine выполняет fix-pass в той же task branch.
3. Повторно запускает checks и generated checks.
4. Возвращает PR в `engine:ready-for-review`.
5. Reviewer делает re-review.
6. Цикл ограничен `max_review_cycles` по `docs/agent-system/REVIEW_AUTOLOOP.md`.
7. После approve-equivalent PR помечается `architect:ready-to-merge`; merge остаётся human-only.

## Base branch warning

- Для рабочих веток base branch должен быть `developer`.
- Для переноса стабильного состояния base branch должен быть `main`, compare branch `developer`.
- Перед merge всегда проверять base/compare, чтобы не повторить ошибку merge рабочей ветки напрямую в `main`.

## Review-only PR

Для code review / external review / consulting review используется ветка:

```text
developer -> work/code-reviewer-01/<task-id> -> PR в developer
```

Review-only PR может содержать только report files и journal/state updates, если они разрешены задачей.

Запрещено в review-only PR:

- исправлять production code;
- делать refactor;
- менять runtime, Docker, CI, scripts или dependencies;
- использовать vendor/tool names в branch names или report filenames.

Если findings требуют исправлений, создается отдельный implementation PR, например:

```text
work/dev-implementer-01/<task-id>
```
