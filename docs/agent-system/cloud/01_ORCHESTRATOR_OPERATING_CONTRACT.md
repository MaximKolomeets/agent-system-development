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
Commit messages и PR title/body тоже Russian-first; technical identifiers не переводятся, conventional prefix вроде `docs(agent-system):` допустим.
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

Этот раздел является human canon для handoff-поведения. Машиночитаемый состав context-load bundle находится в `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml` → `orchestrator_context_bundle`; остальные документы должны ссылаться на manifest и этот раздел, а не дублировать состав bundle прозой.

### Cloud staging

`docs/agent-system/cloud/` является generated staging folder для бандла оркестратора. Он создаётся командой:

```text
python docs/agent-system/tools/gen_cloud_bundle.py
```

Проверка drift:

```text
python docs/agent-system/tools/gen_cloud_bundle.py --check
```

`--check` является content-parity gate: каждый generated numbered `.md` файл должен совпадать с текущим source-файлом из bundle, а `cloud/00_README.md` должен сохранять priority map и upload how-to. Строки `asof` и `developer_head_sha` в `cloud/00_README.md` информационные и не входят в равенство gate; sync-merge, который меняет commit SHA без content-дрейфа bundle, не должен ломать `--check`.

### Проверки generated text artifacts: content-oriented / EOL-safe

Любой generated text artifact и связанный с ним режим `--check` должны сравнивать содержимое, а не байтовую форму checkout. Перед сравнением text-content нормализует `CRLF`, `CR` и `LF` к единому `LF`, чтобы Windows checkout и `core.autocrlf` не создавали false drift при отсутствии реального изменения content.

Новый генератор с режимом `--check` обязан иметь regression-проверку: EOL-only drift не должен давать ненулевой exit, но реальный content-drift в source или generated artifact обязан оставаться обнаруживаемым и приводить к ненулевому exit. Если generator emits generated-bundle paths, эти paths закрепляются в `.gitattributes` через `text eol=lf`, чтобы repository checkout был предсказуемым; это дополняет EOL-normalized compare, но не заменяет его.

Windows fallback: если wrapper, parallel runner или shell-композиция для generated `--check` зависает без живого полезного процесса, это не является parity failure. Для read-only generated checks нужно выполнить sequential fallback, предпочтительно `cmd /c python <generator> --check`, и считать gate-result по exit code этой последовательной команды. RESULT обязан записать, что применён fallback, указать команду и exit code. Это правило относится только к read-only generated text checks и не переносится на произвольные runtime/test jobs.

Zero-match/no-output scan fallback: на Windows read-only scans/checks не должны полагаться только на wrapper/parallel `rg`, если он зависает без вывода и без живого полезного процесса. Такой hang не является содержательной scan-находкой и не считается самостоятельным FAIL. Нужно повторить scan последовательным deterministic способом с явным exit code: `Select-String`, PowerShell script, Python script/one-liner или другая простая sequential command. RESULT обязан записать fallback-команду, exit code и смысл результата: zero matches подтверждены или matches найдены. Правило относится к read-only scans/checks вроде placeholder scan, sensitive filename-only/count-only scan, heading scan, wording scan и vendor scan; sensitive matches не печатать построчно, использовать filename-only или count-only.

Архитектор загружает `docs/agent-system/cloud/` целиком, если лимит интерфейса позволяет, или изменённое подмножество numbered-файлов по per-task handoff. `cloud/00_README.md` является авторитетной картой `source path -> cloud filename`, содержит priority map, freshness stamp и upload how-to.

### Per-task footer naming

Строка `Архитектору — загрузить в контекст оркестратора: ...` в final report и RESULT перечисляет только файлы, входящие в `orchestrator_context_bundle` и реально присутствующие в `docs/agent-system/cloud/`. Небандловые файлы, например tooling/generator sources, остаются в `Source Delta`, но не попадают в context-load строку.

Каждый файл в footer указывается cloud-именем из `docs/agent-system/cloud/00_README.md`, а исходный путь даётся в скобках для трассировки. Пример:

```text
Архитектору — загрузить в контекст оркестратора: 01_ORCHESTRATOR_OPERATING_CONTRACT.md (src: docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md), 11_ADOPTION_TRANSFER_MANIFEST_yml.md (src: docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml); asof: <ISO-8601 timestamp>; developer_head_sha: <sha>.
```

Drive-мост является architect-side операцией: архитектор один раз настраивает Google Drive for Desktop или `rclone` на своих credentials и синхронизирует generated `cloud/` folder. Исполнитель (engine) не авторизует Google Drive, не читает credentials и не создаёт token files.

### Что не грузить по умолчанию

Не загружать по умолчанию тела `history_state`, полную историю journal `RESULT-*` и `target_generated` файлы: они не нужны для обычного operate. Категории, назначение файлов и default bundle проверяются по `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`, производной карте `docs/agent-system/PROJECT_FILE_MAP.md` и generated staging folder `docs/agent-system/cloud/`.

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
