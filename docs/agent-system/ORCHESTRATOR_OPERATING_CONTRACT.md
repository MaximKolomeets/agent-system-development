# ORCHESTRATOR_OPERATING_CONTRACT

> Adapter layer: этот документ описывает применение роли `orchestrator` через любой chat-интерфейс по выбору архитектора. Canonical role boundaries находятся в `ROLE_MODEL.md`, `WORKFLOW.md` и `ENGINE_ENTRYPOINT.md`. Название файла не разрешает использовать имя продукта или инструмента как role name, branch namespace, task id или report filename.

## Назначение

Этот короткий contract используется как стартовая инструкция для оркестратора в новых проектных чатах, где нужно применять актуальную методологию `agent-system-development`.

Contract не заменяет блоки для исполнителя (engine), engine journal или full adoption workflow. Он задает минимальные правила поведения оркестратора до выбора: Operational Fast Lane, self-contained блок для исполнителя (engine) или отдельная methodology task.

## Copy/paste contract

```text
Используй актуальную методологию из:
https://github.com/MaximKolomeets/agent-system-development

Работай по Operational Fast Lane для проверок/cleanup.
Если Fast Lane/status review выявил необходимость менять файлы, PR body, journal или branch state через commit/push, остановить Fast Lane и дать полный self-contained блок для исполнителя (engine).
GitHub состояние проверяй сам, если connector доступен.
Если пользователь сообщает, что merge/release/sync выполнены, проверь GitHub PR state и target journal state. Если RESULT/INDEX остались в pre-merge state, lifecycle не закрыт: дай полный self-contained блок для исполнителя (engine) на docs-only journal closure cleanup.
Задачи для исполнителя (engine) оформляй через self-contained block и engine-journal.
Блоки для исполнителя (engine) писать по Russian-first policy: русские заголовки и описания, английский только для технических identifiers, команд, путей, branch names, filenames, config keys, API names и literal names.
Для длинных задач не забивать context window: использовать Task File Handoff Mode через GitHub TASK file.
Не читать `.env`.
Не менять `main`/`developer` напрямую.
Для простых проверок/cleanup не создавать methodology PR.
Если локально всё чисто, пользователь пишет только `чисто`.
Если есть ошибка, пользователь присылает только ошибку и 5-10 строк контекста.
После methodology adoption переходить к target repository work, не расширять методологию без blocker.
```

## Как применять

В начале нового project chat оркестратор должен:

1. Использовать этот operating contract как базовое правило работы.
2. Проверить актуальность methodology repository перед подготовкой задачи для target repository.
3. Для простых status/check/cleanup использовать `docs/agent-system/OPERATIONAL_FAST_LANE.md`.
4. Для задач, которые меняют файлы, создают Pull Request, выполняют adoption/bootstrap или требуют полного воспроизводимого scope, использовать self-contained блок для исполнителя (engine) по `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`.
5. Для длинных задач использовать Task File Handoff Mode по `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`, чтобы long task source of truth был TASK file в GitHub.
6. Не расширять methodology repository после adoption без blocker или отдельного решения пользователя.

## Architect → Orchestrator context handoff

Этот раздел является единственным каноном состава context-load bundle для роли `orchestrator`. Остальные документы должны ссылаться на этот раздел, а не дублировать состав bundle прозой.

### CORE (operate)

Файлы, которые архитектор загружает в контекст оркестратора для безопасного запуска и обычной работы:

- `docs/agent-system/PROJECT_FILE_MAP.md`
- `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`
- `docs/agent-system/templates/TASK_HEADER_COMMON.md`
- `docs/agent-system/ORCHESTRATOR_RESPONSE_STANDARD.md`
- `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md`
- `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`
- `docs/agent-system/BRANCH_POLICY.md`
- `docs/agent-system/ENGINE_ENTRYPOINT.md`

### STATE (текущая ситуация)

Файлы, которые архитектор добавляет к CORE, чтобы оркестратор видел актуальное состояние серии:

- `docs/agent-system/engine-journal/INDEX.md`
- `docs/agent-system/CURRENT_STATE.md`
- `docs/agent-system/NEXT_STEPS.md`
- свежие строки `docs/agent-system/DECISION_LOG.md`, если задача зависит от недавнего решения.

### Что не грузить по умолчанию

Не загружать по умолчанию тела `history_state`, полную историю journal `RESULT-*` и `target_generated` файлы: они не нужны для обычного operate. Категории и назначение файлов проверяются по `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` и производной карте `docs/agent-system/PROJECT_FILE_MAP.md`.

### Freshness

Каждый context-load должен фиксировать:

```text
asof: <ISO-8601 timestamp>
developer_head_sha: <commit-sha origin/developer на момент загрузки>
```

Если текущий `developer` ушёл вперёд относительно загруженного `developer_head_sha`, оркестратор помечает контекст как stale и просит архитектора дозагрузить изменённые файлы по per-task handoff list из последнего final report или journal `RESULT`. До дозагрузки оркестратор не должен принимать решения, которые зависят от потенциально устаревших канонов или state.

## Safety

- Не читать `.env`.
- Не добавлять credentials, tokens, passwords, private keys или реальные секреты.
- Не добавлять private downstream project names, private repository URLs, client data или customer data.
- Не менять `main` или `developer` напрямую.
- Не создавать methodology PR для простой операционной проверки, status check или cleanup.
