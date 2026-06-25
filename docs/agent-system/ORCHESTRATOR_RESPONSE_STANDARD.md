# ORCHESTRATOR_RESPONSE_STANDARD

> Adapter layer: этот стандарт описывает применение роли `orchestrator` через любой chat-интерфейс по выбору архитектора. Canonical vendor-neutral правила находятся в `ROLE_MODEL.md`, `WORKFLOW.md`, `ENGINE_ENTRYPOINT.md` и `LANGUAGE_POLICY.md`. Не использовать имя продукта или инструмента как role name, branch namespace, task id или report filename.

## Назначение

Этот стандарт описывает, как оркестратор должен формировать ответы, если из ответа рождается задача для `engine`.

Цель стандарта - сделать так, чтобы пользователь мог скопировать один полный prompt для `engine` одним действием и вставить его без ручного сбора цели, команд, ограничений, проверок и формата отчета из разных частей ответа.

В новом project chat оркестратор сначала применяет короткий operating contract:

```text
docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md
```

Если задача является только status/check/cleanup, применяется Operational Fast Lane. Если задача меняет файлы, создает PR или требует воспроизводимого scope, оркестратор готовит self-contained блок для исполнителя (engine) по этому стандарту. Если блок для исполнителя (engine) становится слишком длинным, оркестратор использует Task File Handoff Mode по `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`.

Во всех блоках для исполнителя (engine) действует `docs/agent-system/LANGUAGE_POLICY.md`: `engine` должен писать final report, TASK/RESULT/INDEX fields и descriptions на русском языке, кроме технических identifiers, commands, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names. Commit subject/body и PR title/body тоже должны быть Russian-first: conventional prefix допустим, смысловой текст после него пишется по-русски.

## Когда применяется стандарт

Стандарт применяется, когда оркестратор:

- готовит задачу для `engine`;
- формирует adoption task для target repository;
- предлагает отдельную задачу для доработки methodology repository;
- выводит ручные terminal-команды рядом с engine prompt;
- описывает audit, docs-only adoption, runtime adoption или methodology feedback.

Если ответ не содержит задачи для `engine`, стандарт используется как ориентир для ясности ответа, но сам блок для исполнителя (engine) не обязателен.

## Главное правило

Одна engine-задача = один самодостаточный copy/paste-блок.

Если оркестратор дает задачу для `engine`, все входные данные для выполнения этой engine-задачи должны быть внутри одного fenced code block с заголовком `Блок для исполнителя (engine) — копировать целиком`.

Все данные engine, которые нужны для выполнения задачи, должны оставаться внутри этого блока.

Пользователь не должен искать недостающие команды, ограничения, ветки, разрешенные файлы, запрещенные файлы, проверки, STOP-условия или требования к отчету в других разделах ответа.

## Что считается данными для engine

Данными для `engine` считаются:

- цель задачи;
- контекст;
- путь к engine task file;
- путь к expected engine result file;
- URL repository;
- локальный путь, если применимо;
- базовая ветка;
- рабочая ветка;
- роль агента;
- режим запуска;
- рекомендуемый режим исполнения:
  - launch mode / запуск;
  - model / модель;
  - reasoning;
  - execution mode / режим;
  - why this mode is required / почему;
- проверенный execution baseline (Verified execution baseline):
  - полное имя repository;
  - локальный путь, если применимо;
  - базовая ветка;
  - рабочая ветка;
  - проверенное состояние ветки;
  - latest relevant PR numbers/statuses, если применимо;
  - release PR status, если применимо;
  - sync PR status, если применимо;
  - latest known merge commit SHA, если доступен;
  - open PR state, если relevant;
  - verification source: GitHub connector / local git / user-provided;
  - verification date/time;
- команды предварительной проверки;
- разрешенные файлы;
- запрещенные файлы;
- конкретные изменения;
- проверки;
- STOP-условия;
- Russian-first policy и допустимые исключения для технических identifiers;
- политика journal finalization;
- режим task source, если используется Task File Handoff Mode;
- политика commit, push и PR;
- требования к final report;
- дополнительные ограничения безопасности.

Все эти данные должны быть внутри блока для исполнителя (engine), если без них `engine` не сможет корректно выполнить задачу.

Если оркестратор перед блоком для исполнителя (engine) пишет GitHub/local baseline, summary, current state, recommended mode, branch state, PR state, release/sync state или safety assumptions, и эти данные нужны `engine` для выполнения задачи, они должны быть продублированы внутри блока для исполнителя (engine).

Нельзя оставлять уникальный execution context только в обычном тексте перед блоком для исполнителя (engine). В обычном тексте перед блоком допускаются пояснения для пользователя, но не обязательные execution data.

## Что запрещено выносить за пределы блока для исполнителя (engine)

За пределами блока для исполнителя (engine) нельзя оставлять:

- обязательные команды;
- ограничения scope;
- разрешенные файлы;
- запрещенные файлы;
- проверки;
- STOP-условия;
- требования к отчету;
- branch policy;
- политика commit/push/PR;
- сведения, без которых `engine` не поймет задачу.

Вне блока для исполнителя (engine) можно давать только короткий вывод, контекст для пользователя, ссылки, цитаты и пояснения, которые не являются обязательными execution data.

## Защита перехода из Fast Lane в блок для исполнителя (engine)

Ответ оркестратора может использовать Operational Fast Lane только пока остается read-only/status/cleanup-only.

Если в ходе анализа оркестратор решает, что `engine` должен изменить repository files, обновить PR body, обновить journal artifacts, сделать commit, push, создать PR или исправить review findings через file edits, оркестратор обязан прекратить Fast Lane.

До отправки пользователю actionable часть должна быть переписана как один полный self-contained блок для исполнителя (engine) с заголовком `Блок для исполнителя (engine) — копировать целиком`.

Запрещен гибридный ответ, где Fast Lane text содержит implementation instructions, требующие write actions от `engine`.

Триггером является рекомендуемое действие, а не исходная формулировка пользователя. Даже если пользователь попросил только review/status, как только оркестратор рекомендует write changes, ответ становится задачей для исполнителя (engine).

Read-only review может завершиться фразой "нужна отдельная задача для исполнителя (engine)" только если:

- полный блок для исполнителя (engine) включен в ответ;
- или оркестратор явно запрашивает решение пользователя, потому что scope/approval недостаточны.

Если следующий шаг уже ясен, безопасен и не требует уточнения, оркестратор должен дать полный блок для исполнителя (engine), а не неформальное указание "пусть исполнитель (engine) поправит".

## Языковая граница блоков для исполнителя (engine)

Блоки для исполнителя (engine) являются user-facing task descriptions и должны соблюдать Russian-first policy.

Пользовательские заголовки и описания внутри блока для исполнителя (engine) должны быть на русском языке.

Английский допускается только для technical identifiers, command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names.

Запрещено использовать англоязычные служебные заголовки, если есть нормальная русская формулировка.

Примеры запрещенных пользовательских заголовков:

- `Required changes`;
- `Checks`;
- `Expected checks result`;
- `Commit/push policy`;
- `Final report requirements`;
- `STOP conditions`;
- `Allowed files`;
- `Forbidden files`.

Примеры правильных русских заголовков:

- `Требуемые изменения`;
- `Проверки`;
- `Ожидаемый результат проверок`;
- `Политика commit/push/PR`;
- `Требования к финальному отчету`;
- `STOP-условия`;
- `Разрешенные файлы`;
- `Запрещенные файлы`.

Термины `engine`, `PR`, `commit`, `push`, `branch`, `merge`, `SHA`, `Local only`, `Reasoning`, `Agent` допустимы как technical terms или literal values, но не должны заменять русские пользовательские описания там, где описание можно написать по-русски.

## Блок для исполнителя (engine) — копировать целиком

Блок для исполнителя (engine) должен быть одним fenced code block.

Внутри него должны быть:

- обязательная шапка задачи;
- путь к engine task file или ссылка на существующий task file;
- путь к expected engine result file;
- цель;
- контекст;
- URL repository;
- локальный путь;
- базовая ветка;
- рабочая ветка;
- разрешенные файлы;
- запрещенные файлы;
- точные изменения;
- предварительная проверка;
- проверки;
- STOP-условия;
- политика journal finalization;
- режим task source, если используется Task File Handoff Mode;
- рекомендуемый режим исполнения;
- проверенный execution baseline (Verified execution baseline) или явное `not applicable`;
- политика commit/push/PR;
- формат финального отчета.

Нельзя использовать вложенные fenced code blocks внутри блока для исполнителя (engine). Для внутренних команд используются маркеры `BEGIN POWERSHELL`, `END POWERSHELL`, `BEGIN BASH`, `END BASH`.

## Предотправочный checklist для блока исполнителя (engine)

Перед отправкой блока для исполнителя (engine) оркестратор проверяет:

- [ ] Можно ли выполнить задачу, скопировав только один fenced code block?
- [ ] Есть ли внутри блока рекомендуемый режим исполнения?
- [ ] Есть ли внутри блока Verified execution baseline или явное `not applicable`?
- [ ] Есть ли repository/base branch/working branch?
- [ ] Есть ли разрешенные файлы?
- [ ] Есть ли запрещенные файлы?
- [ ] Есть ли checks?
- [ ] Есть ли STOP-условия?
- [ ] Есть ли commit/push/PR policy, если задача создает изменения?
- [ ] Указан ли язык commit/PR metadata: commit subject/body и PR title/body — Russian-first, technical identifiers не переводятся, conventional prefix допустим?
- [ ] Есть ли требования к финальному отчету?
- [ ] Нет ли обязательных execution data вне блока?
- [ ] Если ответ просит `engine` изменить файлы, есть ли ровно один полный блок для исполнителя (engine) для этой задачи?
- [ ] Остались ли write-action instructions вне блока для исполнителя (engine)?
- [ ] Если Fast Lane/status review выявил необходимость file changes, был ли Fast Lane остановлен и заменен полным блоком для исполнителя (engine)?
- [ ] Находятся ли PR body update, journal update, commit/push и review follow-up instructions внутри блока для исполнителя (engine)?
- [ ] Все ли пользовательские заголовки блока для исполнителя (engine) написаны на русском?
- [ ] Остался ли английский только в технических identifiers, commands, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names?
- [ ] Нет ли англоязычных служебных заголовков, если для них есть русская формулировка?
- [ ] Если пользователь сообщил о merge/release/sync, проверены ли GitHub state и journal state?
- [ ] Если PR merged, закрыты ли RESULT/INDEX после merge или это lifecycle-only `terminal-fold accepted`?
- [ ] Если release/sync выполнены, записаны ли release/sync факты?
- [ ] Если journal stale, отличён ли blocker `open/merged-but-unclosed substantive entry` от accepted terminal fold?
- [ ] Если найден только accepted terminal fold, не создаётся ли новая closure-задача только ради него?
- [ ] Если generated `--check` на Windows завис в wrapper/parallel runner, указан ли read-only sequential fallback (`cmd /c python <generator> --check`) и требование записать команду + exit code в RESULT?
- [ ] Если no-output `rg`/wrapper scan на Windows завис, указан ли deterministic fallback (`Select-String`/PowerShell/Python/sequential command) и требование записать команду + exit code в RESULT без печати sensitive matches?
- [ ] Если что-то осталось вне блока, блок переписан до ответа пользователю.

## Журнал исполнителя (engine)

Каждая задача для `engine` должна иметь task file path или ссылку на уже существующий task file в `docs/agent-system/engine-journal/input/`.

Каждый ответ `engine` должен вернуть result file в `docs/agent-system/engine-journal/output/`.

Task/result files связываются единым sequence number и task id по contract:

```text
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
```

Task/result files являются append-only artifacts. Их нельзя удалять, перезаписывать или переиспользовать без отдельного решения пользователя.

Если задача создается до materialization task file, блок для исполнителя (engine) должен содержать `Engine task file` и `Expected engine result file`, чтобы `engine` создал оба artifacts в рамках разрешенного scope.

Блок для исполнителя (engine) должен содержать обязательное поле `Journal finalization policy`: `engine` финализирует `RESULT` и `INDEX` после PR creation, заменяет journal placeholders фактическими значениями и делает follow-up commit/push, если PR URL или final commit SHA стали известны после materialization.

Если задача может завершиться merge/release/sync, блок для исполнителя (engine) должен ссылаться на `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure policy». Для обычных work PR оркестратор планирует batch-closure перед release/audit/methodology boundary; per-task closure требует только для release/state docs, audit/review consistency gate, adoption/source-update, завершения/паузы серии, явного closure-задания или противоречивых journal facts.

Для substantive task блок должен явно указывать agent-owned task branch workflow: `work/<role>/<task-id>` как основная task branch, внутренние `work/<role>/<task-id>/*` только при необходимости, один итоговый PR в `developer`, review feedback исправляется в той же branch, engine не запрашивает подтверждение после каждого микрошага до STOP-условия.

Если задача предполагает review/fix/re-review, блок должен явно задавать review autoloop: `max_review_cycles`, reviewer feedback только в PR агента, engine fix-pass в той же task branch, `architect:ready-to-merge` после approve-equivalent и STOP при conflict/secrets-risk/forbidden paths/failed checks/scope drift/max cycles. Feedback должен требовать blocker IDs, class `machine-verifiable | semantic | mixed`, `verification_command`, `can_engine_fix_without_architect` и `re_review_policy`; machine-only blockers закрываются passed machine-check closure, semantic/mixed blockers идут на minimal re-review. Если formal own-PR review невозможен, использовать verdict comment fallback. Канон: `docs/agent-system/REVIEW_AUTOLOOP.md`.

Final report `engine` должен подтверждать:

- `RESULT finalized: yes`;
- `INDEX finalized: yes`;
- `Source Delta present: yes` по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source Delta»;
- `context-handoff present: yes` по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Orchestrator context handoff»;
- `No journal placeholders: yes`;
- язык final report: русский.

Оркестратор обязан ретранслировать Source Delta архитектору в своём ответе/передаче. Если final report или RESULT исполнителя (engine) не содержит «Source Delta», оркестратор запрашивает у исполнителя (engine) дополнение отчёта или journal-result, а не реконструирует таблицу молча.

Оркестратор обязан ретранслировать архитектору строку «Архитектору — загрузить в контекст оркестратора: …» и подтверждать `context-handoff present: yes`. Если final report или RESULT исполнителя (engine) не содержит per-task context handoff, оркестратор запрашивает дополнение отчёта или journal-result. Footer должен использовать numbered cloud-имена из `docs/agent-system/cloud/00_README.md` и перечислять только bundle-файлы; небандловые tooling/source-файлы остаются в «Source Delta» и не попадают в context-load строку. Базовый состав context-load bundle не дублируется здесь; авторитетный канон: `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` → «Architect → Orchestrator context handoff».

## Closure policy после merge/release/sync

Любой ответ оркестратора после сообщения пользователя о merge/release/sync должен разделять GitHub PR state и target journal RESULT/INDEX state.

GitHub merge сам по себе не закрывает substantive lifecycle задачи, если target journal stale. В batch-policy stale journal может быть допустимым промежуточным состоянием `merged; closure pending`, но release/audit boundary остаётся запрещён до closure всех substantive entries. Lifecycle-only `terminal-fold accepted` является финальным допустимым состоянием и не blocker.

Если задача находится под release gate, audit/review consistency gate, adoption/source-update, methodology boundary, завершением/паузой серии, явным closure-заданием или содержит противоречивые journal facts, оркестратор должен дать self-contained блок для per-task closure только для substantive stale entries. Не выдавать новую closure-задачу только ради accepted terminal fold. В обычной серии work PR оркестратор явно передаёт closure в batch перед release/audit boundary.

## Локальные действия после PR/merge

Если задача создала PR, была смержена, обновила remote `developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`, финальный ответ оркестратора или final report `engine` должен содержать конкретный блок:

```text
## Локальные действия после PR/merge
```

Полный формат блока, команды для sync `developer`/`main`, диагностика рассинхрона и запрет `git reset --hard` описаны в каноническом разделе `docs/agent-system/WORKFLOW.md`.

Closure-блок для исполнителя (engine) должен включать:

- target repository;
- work PR URL/status/merge commit SHA/`merged_at`;
- release PR URL/status/merge commit SHA/`merged_at` или `не применимо`;
- sync PR URL/status/merge commit SHA/`merged_at` или `не применимо`;
- разрешенные файлы только для `RESULT`, `INDEX` и безопасных state docs, если они нужны;
- запрет runtime, Docker, CI, secrets, private data и downstream-specific details;
- проверки stale placeholders и pre-merge statuses в `RESULT`/`INDEX`;
- финальный отчет на русском языке.

## Ответ Task File Handoff

Ответ Task File Handoff используется, когда блок для исполнителя (engine) становится слишком длинным, задача может забить context window или long task source of truth должен жить в Git history target repository.

Ответ оркестратора в этом режиме должен содержать:

- repository;
- branch;
- путь к task file;
- commit SHA или blob SHA task file, если известно;
- короткий bootstrap prompt для исполнителя (engine);
- напоминания по безопасности;
- указание, что TASK file является source of truth;
- указание финализировать RESULT/INDEX после PR creation;
- инструкция применить Closure policy после merge/release/sync: batch перед release по умолчанию, per-task только для исключений из канона;
- напоминание Russian-first для final report и journal artifacts.

Если GitHub connector доступен и пользователь явно разрешил, оркестратор может создать только task-file-only branch/commit с TASK file. Оркестратор не должен менять runtime, templates, RESULT, INDEX, governance files или другие docs в этом staging commit.

Bootstrap prompt не заменяет TASK file. Если TASK file и bootstrap prompt конфликтуют, `engine` должен написать `STOP`.

## Ручная работа пользователя

Ручная работа выводится только для действий, которые должен выполнить пользователь, а не `engine`.

Ручные действия должны быть явно помечены как ручные. Они не должны содержать данных, без которых `engine` не сможет выполнить свою задачу.

Если ручные действия нужны до запуска `engine`, они должны быть либо внутри блока для исполнителя (engine) как preflight для `engine`, либо в отдельном разделе `Ручная работа до запуска engine`. Даже в этом случае блок для исполнителя (engine) должен оставаться самодостаточным.

## Режим Operational Fast Lane

Для manual checks/cleanup не нужен блок для исполнителя (engine), если задача не меняет файлы repository, не создает PR и не затрагивает secrets/private data.

Operational Fast Lane используется для простых status checks, cleanup, post-engine result checks и release readiness sanity checks. Команды даются одним terminal block, а ответ не растягивается на много уточняющих сообщений.

Если GitHub connector доступен, оркестратор сам проверяет PR/open/merged/branch state и не просит пользователя присылать длинные логи при чистом результате.

Post-merge checks в Operational Fast Lane должны включать journal closure state: рабочий PR merged, release PR merged при наличии, sync PR merged при наличии, stale work branches очищены или отмечены. Для ordinary work PR в batch-серии pre-merge/closure-pending journal state допустим до boundary; для release/audit/adoption/source-update/explicit closure contexts `RESULT` и `INDEX` не должны оставаться в статусах `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report`, кроме lifecycle-only `terminal-fold accepted`.

Если пользователь пишет `готово` после merge, release или sync, оркестратор должен проверить target journal entries. Если это ordinary work PR в batch-серии, оркестратор фиксирует `closure pending` и не запускает отдельную closure-задачу. Если substantive `RESULT` или `INDEX` stale под release/audit/adoption/source-update/explicit closure context или противоречит GitHub, оркестратор не должен считать цикл закрытым: нужно запросить у `engine` docs-only journal-closure cleanup task с фактическими merge данными. Если остался только accepted terminal fold, не запускать новую closure-задачу только ради него.

Длинный блок для исполнителя (engine) нужен только для задач, которые меняют файлы, создают PR, выполняют adoption/bootstrap или требуют полного воспроизводимого scope.

## Разделение ручной работы

Одна ручная задача = один раздел = один terminal block.

Нельзя смешивать несколько независимых ручных операций в одном terminal block, если пользователь должен выполнять их в разное время, в разных repositories или с разными правами.

Нельзя помещать в один fenced code block и engine prompt, и manual terminal commands, если эти команды предназначены пользователю, а не `engine`.

## Несколько engine или repository в одном ответе

Если ответ содержит две независимые engine-задачи, каждая задача получает отдельный самодостаточный copy/paste-блок.

Например, задача для target repository и задача для methodology repository должны быть разными блоками для исполнителя (engine). Нельзя делать один блок для исполнителя (engine) неполным из-за того, что часть данных находится в другом блоке.

## Проверка актуального methodology repository

Перед формированием задачи для target repository оркестратор должен обратиться к актуальному `agent-system-development`, проверить изменения и использовать текущую версию методологии.

Если проверить актуальность невозможно, оркестратор должен явно сказать это пользователю и включить в блок для исполнителя (engine) обязательный preflight для `git fetch --all --prune` и `git pull --ff-only` там, где это безопасно.

В новых проектных чатах проверка актуальности methodology repository выполняется после применения `docs/agent-system/ORCHESTRATOR_OPERATING_CONTRACT.md` и до постановки задачи для исполнителя (engine) в target repository.

## Синхронизация methodology repository перед выполнением

Любой `engine`, который применяет или изменяет methodology repository, должен перед изменениями синхронизировать локальную копию `agent-system-development` с GitHub.

Если working tree не чистый, `engine` должен написать `STOP` и не перетирать локальные изменения.

Если `origin/developer` отсутствует или pull fast-forward невозможен, `engine` должен написать `STOP` для methodology repository changes.

После `git pull --ff-only origin <METHODOLOGY_BASE_BRANCH>` локальный `HEAD` methodology repository должен строго совпадать с `origin/<METHODOLOGY_BASE_BRANCH>`. Если значения отличаются, `engine` должен написать `STOP`, потому что локальная methodology branch содержит состояние, которого нет в remote source of truth.

Если `engine` синхронизировал methodology repository в рамках задачи для target repository, он обязан вернуться в target repository через явный `cd <TARGET_REPOSITORY_LOCAL_PATH>` до проверки target remote, branch, working tree, файлов или выполнения изменений.

## Методологический feedback block

Если при работе с target repository выявлена необходимость доработки `agent-system-development`, оркестратор должен вывести отдельный самодостаточный блок для engine-разработчика methodology repository.

Этот блок должен быть нейтральным и не должен раскрывать private downstream data, private repository URL, client data, customer data, credentials или internal code names.

В final report target repository такой вывод фиксируется как `Methodology repository improvement request`.

## Сводка audit

Ответ с audit-задачей должен требовать от `engine` краткий audit summary:

- что проверено;
- что найдено;
- какие документы отсутствуют;
- какие риски есть;
- какой следующий PR рекомендуется;
- нужен ли отдельный methodology feedback.

Audit summary не заменяет полный audit artifact, если задача требует создать отдельный файл.

## Правило language consistency

Оркестратор и `engine` должны применять `docs/agent-system/LANGUAGE_POLICY.md` и проверять language consistency target docs.

Все user-facing answers, final reports исполнителя (engine), TASK/RESULT/INDEX files, target-local methodology docs/templates и комментарии в файлах оформляются на русском языке.

Английский сохраняется только для code identifiers, команд, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, GitHub terms и literal external names, если перевод ухудшает точность.

Target project prompts должны включать Russian-first rule и требовать добавить его в target `AGENTS.md` или эквивалентные target instructions при adoption/update scope.

Блок для исполнителя (engine) должен требовать от `engine` написать `STOP`, если target instructions конфликтуют с Russian-first policy и пользователь явно не разрешил другой язык для target repository.

## Русский язык документации target repository

После adoption audit и docs-only adoption целевые governance docs должны иметь один основной человеческий язык.

Если repository ведется на русском, смешанные англо-русские описания либо нормализуются, либо явно объясняются в audit/report.

## Запрет смешивания prompt, terminal commands и пояснений

Prompt для исполнителя (engine), manual terminal commands и пояснения пользователю должны быть разделены.

Prompt для исполнителя (engine) помещается в блок для исполнителя (engine). Ручные terminal-команды помещаются в отдельный раздел ручной работы. Пояснения остаются вне terminal blocks.

## Definition of Done для ответа

Ответ оркестратора считается готовым, если:

- есть короткий вывод для пользователя;
- каждая engine-задача имеет отдельный самодостаточный блок для исполнителя (engine);
- внутри блока для исполнителя (engine) есть все execution data;
- указан engine journal task/result path или причина, почему journal не применим;
- manual steps отделены от блока для исполнителя (engine);
- проверки и STOP-условия не потеряны вне блока;
- methodology freshness check указан;
- language consistency rule указан, если задача связана с adoption;
- Russian-first policy указана для final report исполнителя (engine) и journal artifacts;
- methodology feedback нейтрален и не раскрывает private data;
- Closure policy проверена: batch перед release или per-task exception явно указаны;
- следующий шаг сформулирован явно.

## Пример правильного ответа

Правильный ответ:

- коротко объясняет пользователю, что будет сделано;
- выводит один раздел `Блок для исполнителя (engine) — копировать целиком`;
- внутри одного fenced code block содержит цель, контекст, ветки, разрешенные файлы, запрещенные файлы, предварительную проверку, проверки, STOP-условия, политику commit/push/PR и final report;
- ручную работу выводит отдельным разделом только если она действительно нужна пользователю.

## Пример неправильного ответа

Неправильный ответ:

- часть цели оставляет до блока для исполнителя (engine);
- часть команд оставляет после блока для исполнителя (engine);
- разрешенные файлы или запрещенные файлы выносит в отдельный список вне блока;
- делает несколько разрозненных блоков для одной engine-задачи;
- смешивает manual terminal commands и engine prompt;
- не указывает, как проверялась актуальность methodology repository.

## Правила безопасности

- Не добавлять private downstream names.
- Не добавлять private repository URLs.
- Не добавлять client data или customer data.
- Не добавлять credentials, tokens, passwords, API keys или `.env`.
- Не печатать matching lines sensitive grep.
- Не читать `.env`.
- Не менять `main` или `developer` напрямую без отдельного разрешения.
- Не делать force push.
