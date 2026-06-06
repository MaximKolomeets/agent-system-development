# PR_WORKFLOW

1. Пользователь принимает решение о задаче.
2. ChatGPT формирует задачу.
3. Исполнитель создает `work/<role>/<task>`.
4. Исполнитель меняет только разрешенные файлы.
5. Исполнитель обновляет отчет.
6. Исполнитель делает commit и push.
7. Пользователь/ChatGPT проверяют diff.
8. Создается PR в `developer`.
9. После проверки PR merge в `developer`.
10. После накопления стабильных изменений `developer` merge в `main`.
11. После merge обновляются `CURRENT_STATE`, `DECISION_LOG`, `NEXT_STEPS`.

## Base branch warning

- Для рабочих веток base branch должен быть `developer`.
- Для переноса стабильного состояния base branch должен быть `main`, compare branch `developer`.
- Перед merge всегда проверять base/compare, чтобы не повторить ошибку merge рабочей ветки напрямую в `main`.
