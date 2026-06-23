# PR_WORKFLOW

1. Пользователь принимает решение о задаче.
2. Оркестратор формирует задачу.
3. Проверяется, что задача выполняется из правильного worktree.
4. Проверяется `git branch --show-current`.
5. Проверяется `git status --short`.
6. Проверяется, что base для рабочей ветки - актуальная `developer`.
7. Исполнитель создает `work/<role>/<task>`.
8. Исполнитель меняет только разрешенные файлы.
9. Исполнитель обновляет отчет.
10. Исполнитель делает commit и push.
11. Дождаться GitHub Actions CI.
12. Если CI failed - не мержить PR.
13. Исправить нарушения в рабочей ветке.
14. Повторить push.
15. Review выполняется только после успешного CI или после осознанного решения пользователя.
16. Пользователь/оркестратор проверяют diff.
17. Создается PR в `developer`.
18. После проверки PR merge в `developer`.
19. После накопления стабильных изменений `developer` переносится в `main` только через human-merged release PR по `BRANCH_POLICY.md`.
20. После human merge release PR человек-архитектор ставит annotated tag на release merge commit в `main`; агент не создаёт tag и не публикует GitHub Release.
21. После merge обновляются `CURRENT_STATE`, `DECISION_LOG`, `NEXT_STEPS`.

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
