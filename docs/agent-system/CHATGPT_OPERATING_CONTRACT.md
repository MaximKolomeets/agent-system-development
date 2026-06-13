# CHATGPT_OPERATING_CONTRACT

## Назначение

Этот короткий contract используется как стартовая инструкция для ChatGPT в новых проектных чатах, где нужно применять актуальную методологию `agent-system-development`.

Contract не заменяет Engine-блоки, engine journal или full adoption workflow. Он задает минимальные правила поведения ChatGPT до выбора: Operational Fast Lane, self-contained Engine-блок или отдельная methodology task.

## Copy/paste contract

```text
Используй актуальную методологию из:
https://github.com/MaximKolomeets/agent-system-development

Работай по Operational Fast Lane для проверок/cleanup.
Если Fast Lane/status review выявил необходимость менять файлы, PR body, journal или branch state через commit/push, остановить Fast Lane и дать полный self-contained Engine-блок.
GitHub состояние проверяй сам, если connector доступен.
Если пользователь сообщает, что merge/release/sync выполнены, проверь GitHub PR state и target journal state. Если RESULT/INDEX остались в pre-merge state, lifecycle не закрыт: дай полный self-contained Engine-блок на docs-only journal closure cleanup.
Engine-задачи оформляй через self-contained block и engine-journal.
Engine-блоки писать по Russian-first policy: русские заголовки и описания, английский только для технических identifiers, команд, путей, branch names, filenames, config keys, API names и literal names.
Для длинных задач не забивать context window: использовать Task File Handoff Mode через GitHub TASK file.
Не читать `.env`.
Не менять `main`/`developer` напрямую.
Для простых проверок/cleanup не создавать methodology PR.
Если локально всё чисто, пользователь пишет только `чисто`.
Если есть ошибка, пользователь присылает только ошибку и 5-10 строк контекста.
После methodology adoption переходить к target repository work, не расширять методологию без blocker.
```

## Как применять

В начале нового project chat ChatGPT должен:

1. Использовать этот operating contract как базовое правило работы.
2. Проверить актуальность methodology repository перед подготовкой задачи для target repository.
3. Для простых status/check/cleanup использовать `docs/agent-system/OPERATIONAL_FAST_LANE.md`.
4. Для задач, которые меняют файлы, создают Pull Request, выполняют adoption/bootstrap или требуют полного воспроизводимого scope, использовать self-contained Engine-блок по `docs/agent-system/CHATGPT_RESPONSE_STANDARD.md`.
5. Для длинных задач использовать Task File Handoff Mode по `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`, чтобы long task source of truth был TASK file в GitHub.
6. Не расширять methodology repository после adoption без blocker или отдельного решения пользователя.

## Safety

- Не читать `.env`.
- Не добавлять credentials, tokens, passwords, private keys или реальные секреты.
- Не добавлять private downstream project names, private repository URLs, client data или customer data.
- Не менять `main` или `developer` напрямую.
- Не создавать methodology PR для простой операционной проверки, status check или cleanup.
