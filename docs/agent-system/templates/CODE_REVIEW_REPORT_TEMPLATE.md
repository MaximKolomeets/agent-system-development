# <TASK-ID> - review report

## 1. Объект проверки

- Repository:
- Local path:
- Remote:
- Base branch:
- Head branch:
- Object type: `<PR | branch | commit | diff | files>`
- Object reference:
- Commit SHA:
- Working tree status:

## 2. Что было проверено

Кратко перечислить документы, файлы, diff, команды, workflows, entry points или PR sections, которые реально проверялись.

## 3. Запущенные команды

Перечислить команды и краткий результат.

## 4. Команды, которые не запускались, и почему

Перечислить tests/linters/checks, которые не запускались, и причину.

## 5. Найденные проблемы

### Критично

- Нет findings.

### Желательно

- Нет findings.

### Опционально

- Нет findings.

## 6. Security / forbidden files risks

Описать observations по forbidden paths, `.env` policy, credentials/tokens/passwords и sensitive grep filename-only result.

Matching lines и secret values не печатать.

## 7. Несоответствия документации и фактического состояния

Описать расхождения между docs/templates/workflow и фактическим состоянием repository.

## 8. Рекомендации

Перечислить рекомендации без внесения code fixes.

## 9. Кандидаты на будущие задачи Engine

Для каждого candidate указать:

- role:
- branch:
- scope:
- reason:

Это только кандидаты. Reviewer не запускает Codex/Engine, не меняет очередь исполнителя и не ставит себе implementation task.

## 10. Итоговый вывод

Кратко указать итог: `approve`, `changes required`, `hold` или другой явный вывод, соответствующий задаче.

Подтвердить scope boundaries: reviewer не менял production code, runtime, Docker, CI, scripts, dependencies и forbidden files, если задача не разрешала это отдельно.
