# OPERATIONAL_FAST_LANE

## Назначение

Operational Fast Lane - это короткий режим для простых операционных проверок и cleanup. Он нужен, чтобы не превращать безопасные status checks, cleanup и post-engine result checks в длинные methodology/debug cycles.

Operational Fast Lane не заменяет engine task workflow и не применяется к задачам, которые меняют repository files или создают Pull Request.

## Когда применять

Operational Fast Lane применяется для:

- GitHub PR status check;
- local git status check;
- branch cleanup;
- post-engine result check;
- release readiness sanity check;
- remote branch cleanup;
- verify no open PRs;
- verify work branch is clean.

## Когда не применять

Operational Fast Lane не применяется для:

- изменения архитектуры;
- изменения runtime code;
- adoption bootstrap;
- docs-only governance pack;
- задач, где есть риск secrets/private data;
- задач, которые меняют файлы repository.

## Правила ответа ChatGPT

- Один ответ = один командный блок.
- Для пользователя это один блок команд без дополнительных длинных логов.
- GitHub состояние ChatGPT проверяет сам через connector, если доступно.
- Пользователь не должен присылать длинные логи, если все чисто.
- Если все чисто, пользователь пишет только `чисто`.
- Если есть ошибка, пользователь присылает только ошибку и 5-10 строк контекста.
- Не предлагать новый methodology PR для простой проверки/cleanup.
- Не предлагать sync `main -> developer` только из-за release merge commit.
- Не зеркалировать release merge commit обратно в `developer`, если содержательные изменения уже в `developer`.

## Стандартный формат

```text
Тип:
Что вижу:
Выполни один блок:
Ожидаемо:
Следующий шаг:
```

## Safety

Operational Fast Lane должен оставаться read-only или cleanup-only. Если в ходе проверки появляется необходимость менять файлы, создавать PR, работать с private data, читать `.env` или разбирать sensitive output, нужно остановиться и перейти к обычной задаче с явным scope, allowed files, forbidden files и checks.
