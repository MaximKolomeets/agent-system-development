# PR_WORKFLOW

1. Пользователь принимает решение о задаче.
2. ChatGPT формирует задачу.
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
16. Пользователь/ChatGPT проверяют diff.
17. Создается PR в `developer`.
18. После проверки PR merge в `developer`.
19. После накопления стабильных изменений `developer` merge в `main`.
20. После merge обновляются `CURRENT_STATE`, `DECISION_LOG`, `NEXT_STEPS`.

## Base branch warning

- Для рабочих веток base branch должен быть `developer`.
- Для переноса стабильного состояния base branch должен быть `main`, compare branch `developer`.
- Перед merge всегда проверять base/compare, чтобы не повторить ошибку merge рабочей ветки напрямую в `main`.
