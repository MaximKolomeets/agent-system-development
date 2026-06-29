# ORCHESTRATOR_OPERATING_CONTRACT

## Machine-readable task contract

Для write-action/substantive Engine-блоков оркестратор добавляет fenced YAML `task_contract` по `docs/agent-system/TASK_CONTRACT.md`. Contract является source of truth для mode/scope/checks/STOP, prose остаётся human explanation. Fast Lane без write-action, PR и journal trace может идти без `task_contract`.

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
Для target/downstream задач methodology reference всегда stable: `origin/main` / `main`, явно заданный release tag или published Source/cloud snapshot. Не использовать `developer`, `work/*`, dirty local methodology tree или open methodology PR branch как source of truth для downstream. Dirty `agent-system-development/developer` или `work/*` не является STOP, если stable reference доступен и читается. В рабочем methodology repository для downstream чтения не выполнять `git switch`, `git checkout`, `git pull`, `git reset`, `git clean` или `git stash`; `git fetch --all --prune` допустим только как read-refresh при разрешении задачи.
Если пользователь сообщает, что merge обычного PR выполнен, проверь GitHub PR state и локально синхронизируй `developer` по guard-правилам, если это входит в задачу. Не предлагай отдельный closure PR после ordinary PR: PR считается завершённым на `architect_ready` / `human_merge_allowed`, а GitHub PR metadata является source of truth для `merged_at`, merge commit SHA, PR state и PR URL. Boundary reconciliation откладывается до release/audit boundary или explicit architect request. Если сработал release/audit/explicit reconciliation context или journal facts противоречат GitHub внутри такого scope, дай полный self-contained блок для исполнителя (engine) на docs-only boundary reconciliation. Lifecycle-only `terminal-fold accepted` не считать blocker и не порождать новую closure-задачу только ради него.
Задачи для исполнителя (engine) оформляй через self-contained block и engine-journal.
Для substantive task указывай agent-owned branch model: основная branch `work/<role>/<task-id>`, при необходимости внутренние `work/<role>/<task-id>/*`, один итоговый PR в `developer`, feedback исправляется в той же branch, engine не ждёт подтверждения после каждого микрошага до STOP.

Для PR review/fix цикла используй `docs/agent-system/REVIEW_AUTOLOOP.md`: reviewer feedback остаётся в PR агента, engine делает fix-pass в той же branch, цикл ограничен `max_review_cycles`, а `architect:ready-to-merge` не означает auto-merge. Reviewer feedback должен иметь blocker IDs, class `machine-verifiable | semantic | mixed`, `verification_command` и `can_engine_fix_without_architect`; machine-only blockers можно закрыть passed machine-check closure, semantic/mixed blockers требуют minimal re-review. Если GitHub запрещает formal own-PR review, reviewer оставляет verdict comment в PR; это не blocker.
Перед ready-for-review PR для substantive/docs/tooling задач применяй semantic completeness gate по `docs/agent-system/SEMANTIC_COMPLETENESS_GATES.md`: RESULT, PR body, state docs, acceptance spec, blocker matrix, fixture plan и boundary docs должны согласовываться с фактическим diff и выполненными checks. Для acceptance/spec задач добавляй pattern `docs/agent-system/ACCEPTANCE_SPEC_COMPLETENESS_PATTERN.md`; finalized journal surface должен соблюдать `docs/agent-system/JOURNAL_FINALIZATION_POLICY.md`.
Блоки для исполнителя (engine) писать по Russian-first policy: русские заголовки и описания, английский только для технических identifiers, команд, путей, branch names, filenames, config keys, API names и literal names.
Commit messages, PR title/body, review summary, PR comments с verdict и final report тоже Russian-first; technical identifiers не переводятся, conventional prefix вроде `docs(agent-system):` допустим.
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
2. Проверить stable methodology reference перед подготовкой задачи для target repository: `origin/main` / `main`, release tag или явно заданный snapshot по `docs/agent-system/STABLE_METHODOLOGY_REFERENCE_POLICY.md`.
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

Если текущий `developer` ушёл вперёд относительно загруженного `developer_head_sha`, оркестратор помечает context-load bundle как stale для methodology-development решений. Для downstream/target задач source of truth остаётся stable reference `origin/main` / `main`; изменения, смерженные только в `developer`, не считаются доступными downstream до release PR `developer -> main` или явно указанного snapshot.

## Safety

- Downstream feedback перед methodology task проходит `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`; private/target-specific details, matching secret/header values и target branch/worktree state как methodology fact запрещены.
- Target repositories получают reusable methodology changes только после `main`, release tag или published Source/cloud snapshot; merge в `developer` сам по себе не является downstream adoption boundary.
- Не читать `.env`.
- Не добавлять credentials, tokens, passwords, private keys или реальные секреты.
- Не добавлять private downstream project names, private repository URLs, client data или customer data.
- Не менять `main` или `developer` напрямую.
- Не создавать methodology PR для простой операционной проверки, status check или cleanup.
