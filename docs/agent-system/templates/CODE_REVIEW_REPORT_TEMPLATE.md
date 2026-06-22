# <TASK-ID> - review report

Это шаблон **тела** review report. Путь сохранения файла определяется полем `Report delivery` в TASK (`chat` — не сохранять, `repository` / `chat+repository` — сохранить по `Report naming`). Путь `docs/agent-system/reviews/<task-id>-review.md` — target-local create-on-demand convention для потребляющего проекта, а не обязательный каталог methodology-source.

Journal RESULT создаётся отдельным файлом в `docs/agent-system/engine-journal/output/` всегда (`Journal trace: always`) по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` и не заменяется этим шаблоном.

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

## 9. Кандидаты на будущие задачи исполнителя (engine)

Для каждого candidate указать:

- role:
- branch:
- scope:
- reason:

Это только кандидаты. Reviewer не запускает исполнителя (engine), не меняет очередь исполнителя и не ставит себе implementation task.

## 10. Итоговый вывод

Кратко указать итог: `approve`, `changes required`, `hold` или другой явный вывод, соответствующий задаче.

Подтвердить scope boundaries: reviewer не менял production code, runtime, Docker, CI, scripts, dependencies и forbidden files, если задача не разрешала это отдельно.

## Облегчённый PR / comment review

Сокращённый формат для лёгкого PR review или комментарий-уровня review, когда полный 10-секционный шаблон выше не нужен. Используется по отдельному решению пользователя; журналирование TASK+RESULT остаётся обязательным (`Journal trace: always`).

### PR / branch

Указать PR или ветку.

### Scope

Описать границы review.

### Files reviewed

Перечислить просмотренные файлы.

### Checks run

Указать выполненные проверки.

### Findings

Описать найденные проблемы.

### Journal closure

Если PR уже merged, проверить `RESULT` и `INDEX`: PR status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes`, `No journal placeholders: yes`.

Блокирующие замечания:

- merged PR journal остается `PR open`;
- merged PR journal остается `ready for review`;
- merged PR journal остается `draft open`;
- merged PR journal содержит `pending at file materialization`;
- merged PR journal содержит `see Engine final report`;
- `RESULT` не фиксирует merge commit SHA после merge, когда SHA доступен.

### Required changes

Перечислить обязательные изменения.

### Recommendation

Дать рекомендацию: `approve`, `changes required` или `hold`.
