# MANUAL_REVIEW_CHECKLIST

- Проверить base branch.
- Проверить head branch.
- Проверить, что одна задача = один PR.
- Проверить changed files.
- Проверить, что нет `.env`.
- Проверить, что нет `.venv/`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Проверить, что нет credentials/tokens/passwords.
- Проверить, что PR не добавляет реальные секреты.
- Проверить, что PR не добавляет внутренние данные `CORP_KNOWLEDGE_PLATFORM`.
- Проверить, что изменения подходят для public repository.
- Проверить, что base branch выбран правильно:
  - work branch -> developer;
  - developer -> main.
- Проверить, что нет vendor-specific agent names в именах папок.
- Проверить, что `CURRENT_STATE` обновлен, если изменилось состояние проекта.
- Проверить, что `DECISION_LOG` обновлен, если принято архитектурное решение.
- Проверить, что агентский отчет обновлен.
- Проверить итоговый отчет исполнителя.
