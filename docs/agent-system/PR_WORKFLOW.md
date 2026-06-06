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
11. Пользователь/ChatGPT проверяют diff.
12. Создается PR в `developer`.
13. После проверки PR merge в `developer`.
14. После накопления стабильных изменений `developer` merge в `main`.
15. После merge обновляются `CURRENT_STATE`, `DECISION_LOG`, `NEXT_STEPS`.

## Base branch warning

- Для рабочих веток base branch должен быть `developer`.
- Для переноса стабильного состояния base branch должен быть `main`, compare branch `developer`.
- Перед merge всегда проверять base/compare, чтобы не повторить ошибку merge рабочей ветки напрямую в `main`.
