# CHATGPT_RESPONSE_STANDARD

## Назначение

Этот стандарт описывает, как ChatGPT должен формировать ответы, если из ответа рождается задача для `engine`.

Цель стандарта - сделать так, чтобы пользователь мог скопировать один полный prompt для `engine` одним действием и вставить его без ручного сбора цели, команд, ограничений, проверок и формата отчета из разных частей ответа.

В новом project chat ChatGPT сначала применяет короткий operating contract:

```text
docs/agent-system/CHATGPT_OPERATING_CONTRACT.md
```

Если задача является только status/check/cleanup, применяется Operational Fast Lane. Если задача меняет файлы, создает PR или требует воспроизводимого scope, ChatGPT готовит self-contained Engine-блок по этому стандарту. Если Engine block становится слишком длинным, ChatGPT использует Task File Handoff Mode по `docs/agent-system/TASK_FILE_HANDOFF_CONTRACT.md`.

Во всех Engine-блоках действует `docs/agent-system/LANGUAGE_POLICY.md`: `engine` должен писать final report, TASK/RESULT/INDEX fields и descriptions на русском языке, кроме технических identifiers, commands, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.

## Когда применяется стандарт

Стандарт применяется, когда ChatGPT:

- готовит задачу для `engine`;
- формирует adoption task для target repository;
- предлагает отдельную задачу для доработки methodology repository;
- выводит ручные terminal-команды рядом с engine prompt;
- описывает audit, docs-only adoption, runtime adoption или methodology feedback.

Если ответ не содержит задачи для `engine`, стандарт используется как ориентир для ясности ответа, но сам Engine-блок не обязателен.

## Главное правило

Одна engine-задача = один самодостаточный copy/paste-блок.

Если ChatGPT дает задачу для `engine`, все входные данные для выполнения этой engine-задачи должны быть внутри одного fenced code block с заголовком `Блок для Engine — копировать целиком`.

Все данные engine, которые нужны для выполнения задачи, должны оставаться внутри этого блока.

Пользователь не должен искать недостающие команды, ограничения, ветки, allowed files, forbidden files, проверки, STOP-условия или требования к отчету в других разделах ответа.

## Что считается данными для engine

Данными для `engine` считаются:

- цель задачи;
- контекст;
- engine task file path;
- expected engine result file path;
- repository URL;
- local path, если применимо;
- base branch;
- working branch;
- роль агента;
- режим запуска;
- Recommended Engine Mode:
  - launch mode / запуск;
  - model / модель;
  - reasoning;
  - execution mode / режим;
  - why this mode is required / почему;
- Verified execution baseline:
  - repository full name;
  - local path, если применимо;
  - base branch;
  - working branch;
  - checked branch state;
  - latest relevant PR numbers/statuses, если применимо;
  - release PR status, если применимо;
  - sync PR status, если применимо;
  - latest known merge commit SHA, если доступен;
  - open PR state, если relevant;
  - verification source: GitHub connector / local git / user-provided;
  - verification date/time;
- preflight-команды;
- allowed files;
- forbidden files;
- конкретные изменения;
- проверки;
- STOP-условия;
- Russian-first policy и допустимые исключения для технических identifiers;
- Journal finalization policy;
- task source mode, если используется Task File Handoff Mode;
- commit, push и PR policy;
- требования к final report;
- дополнительные ограничения безопасности.

Все эти данные должны быть внутри Engine-блока, если без них `engine` не сможет корректно выполнить задачу.

Если ChatGPT перед Engine-блоком пишет GitHub/local baseline, summary, current state, recommended mode, branch state, PR state, release/sync state или safety assumptions, и эти данные нужны `engine` для выполнения задачи, они должны быть продублированы внутри Engine-блока.

Нельзя оставлять уникальный execution context только в обычном тексте перед Engine-блоком. В обычном тексте перед блоком допускаются пояснения для пользователя, но не обязательные execution data.

## Что запрещено выносить за пределы Engine-блока

За пределами Engine-блока нельзя оставлять:

- обязательные команды;
- ограничения scope;
- allowed files;
- forbidden files;
- проверки;
- STOP-условия;
- требования к отчету;
- branch policy;
- commit/push/PR policy;
- сведения, без которых `engine` не поймет задачу.

Вне Engine-блока можно давать только короткий вывод, контекст для пользователя, ссылки, цитаты и пояснения, которые не являются обязательными execution data.

## Блок для Engine — копировать целиком

Engine-блок должен быть одним fenced code block.

Внутри него должны быть:

- обязательная шапка задачи;
- engine task file path или ссылка на существующий task file;
- expected engine result file path;
- цель;
- контекст;
- repository URL;
- local path;
- base branch;
- working branch;
- allowed files;
- forbidden files;
- точные изменения;
- preflight;
- checks;
- STOP-условия;
- Journal finalization policy;
- task source mode, если используется Task File Handoff Mode;
- Recommended Engine Mode;
- Verified execution baseline или явное `not applicable`;
- commit/push/PR policy;
- формат финального отчета.

Нельзя использовать вложенные fenced code blocks внутри Engine-блока. Для внутренних команд используются маркеры `BEGIN POWERSHELL`, `END POWERSHELL`, `BEGIN BASH`, `END BASH`.

## Pre-send checklist для Engine-блока

Перед отправкой Engine-блока ChatGPT проверяет:

- [ ] Можно ли выполнить задачу, скопировав только один fenced code block?
- [ ] Есть ли внутри блока Recommended Engine Mode?
- [ ] Есть ли внутри блока Verified execution baseline или явное `not applicable`?
- [ ] Есть ли repository/base branch/working branch?
- [ ] Есть ли allowed files?
- [ ] Есть ли forbidden files?
- [ ] Есть ли checks?
- [ ] Есть ли STOP conditions?
- [ ] Есть ли commit/push/PR policy, если задача создает изменения?
- [ ] Есть ли final report requirements?
- [ ] Нет ли обязательных execution data вне блока?
- [ ] Если что-то осталось вне блока, блок переписан до ответа пользователю.

## Engine journal

Каждая задача для `engine` должна иметь task file path или ссылку на уже существующий task file в `docs/agent-system/engine-journal/input/`.

Каждый ответ `engine` должен вернуть result file в `docs/agent-system/engine-journal/output/`.

Task/result files связываются единым sequence number и task id по contract:

```text
docs/agent-system/ENGINE_JOURNAL_CONTRACT.md
```

Task/result files являются append-only artifacts. Их нельзя удалять, перезаписывать или переиспользовать без отдельного решения пользователя.

Если задача создается до materialization task file, Engine-блок должен содержать `Engine task file` и `Expected engine result file`, чтобы `engine` создал оба artifacts в рамках разрешенного scope.

Engine-блок должен содержать обязательное поле `Journal finalization policy`: `engine` финализирует `RESULT` и `INDEX` после PR creation, заменяет journal placeholders фактическими значениями и делает follow-up commit/push, если PR URL или final commit SHA стали известны после materialization.

Если задача может завершиться merge/release/sync, Engine-блок должен требовать Post-merge Journal Closure по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: после merge journal фиксирует PR status `merged`, merge commit SHA, `merged_at` при доступности, release PR и sync PR status/merge commit SHA при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`.

Final report `engine` должен подтверждать:

- `RESULT finalized: yes`;
- `INDEX finalized: yes`;
- `No journal placeholders: yes`;
- final report language: Russian.

## Task File Handoff Response

Task File Handoff Response используется, когда Engine-блок становится слишком длинным, задача может забить context window или long task source of truth должен жить в Git history target repository.

Ответ ChatGPT в этом режиме должен содержать:

- repository;
- branch;
- task file path;
- task file commit SHA или blob SHA, если известно;
- short Engine bootstrap prompt;
- safety reminders;
- instruction that TASK file is source of truth;
- instruction to finalize RESULT/INDEX after PR creation;
- инструкция выполнить Post-merge Journal Closure после merge/release/sync;
- Russian-first reminder for final report and journal artifacts.

Если GitHub connector доступен и пользователь явно разрешил, ChatGPT может создать только task-file-only branch/commit с TASK file. ChatGPT не должен менять runtime, templates, RESULT, INDEX, governance files или другие docs в этом staging commit.

Bootstrap prompt не заменяет TASK file. Если TASK file и bootstrap prompt конфликтуют, `engine` должен написать `STOP`.

## Ручная работа пользователя

Ручная работа выводится только для действий, которые должен выполнить пользователь, а не `engine`.

Ручные действия должны быть явно помечены как ручные. Они не должны содержать данных, без которых `engine` не сможет выполнить свою задачу.

Если ручные действия нужны до запуска `engine`, они должны быть либо внутри Engine-блока как preflight для `engine`, либо в отдельном разделе `Ручная работа до запуска engine`. Даже в этом случае Engine-блок должен оставаться самодостаточным.

## Operational Fast Lane

Для manual checks/cleanup не нужен Engine-блок, если задача не меняет файлы repository, не создает PR и не затрагивает secrets/private data.

Operational Fast Lane используется для простых status checks, cleanup, post-engine result checks и release readiness sanity checks. Команды даются одним terminal block, а ответ не растягивается на много уточняющих сообщений.

Если GitHub connector доступен, ChatGPT сам проверяет PR/open/merged/branch state и не просит пользователя присылать длинные логи при чистом результате.

Post-merge checks в Operational Fast Lane должны включать journal closure state: рабочий PR merged, release PR merged при наличии, sync PR merged при наличии, stale work branches очищены или отмечены, `RESULT` и `INDEX` не остались в статусах `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report`.

Если пользователь пишет `готово` после merge, release или sync, ChatGPT должен проверить target journal entries. Если `RESULT` или `INDEX` stale, ChatGPT не должен считать цикл закрытым: нужно запросить у `engine` docs-only journal-closure cleanup task с фактическими merge данными.

Длинный Engine-блок нужен только для задач, которые меняют файлы, создают PR, выполняют adoption/bootstrap или требуют полного воспроизводимого scope.

## Разделение ручной работы

Одна ручная задача = один раздел = один terminal block.

Нельзя смешивать несколько независимых ручных операций в одном terminal block, если пользователь должен выполнять их в разное время, в разных repositories или с разными правами.

Нельзя помещать в один fenced code block и engine prompt, и manual terminal commands, если эти команды предназначены пользователю, а не `engine`.

## Несколько engine или repository в одном ответе

Если ответ содержит две независимые engine-задачи, каждая задача получает отдельный самодостаточный copy/paste-блок.

Например, задача для target repository и задача для methodology repository должны быть разными Engine-блоками. Нельзя делать один Engine-блок неполным из-за того, что часть данных находится в другом блоке.

## Проверка актуального methodology repository

Перед формированием задачи для target repository ChatGPT должен обратиться к актуальному `agent-system-development`, проверить изменения и использовать текущую версию методологии.

Если проверить актуальность невозможно, ChatGPT должен явно сказать это пользователю и включить в Engine-блок обязательный preflight для `git fetch --all --prune` и `git pull --ff-only` там, где это безопасно.

В новых проектных чатах проверка актуальности methodology repository выполняется после применения `docs/agent-system/CHATGPT_OPERATING_CONTRACT.md` и до постановки Engine-задачи для target repository.

## Синхронизация methodology repository перед выполнением

Любой `engine`, который применяет или изменяет methodology repository, должен перед изменениями синхронизировать локальную копию `agent-system-development` с GitHub.

Если working tree не чистый, `engine` должен написать `STOP` и не перетирать локальные изменения.

Если `origin/developer` отсутствует или pull fast-forward невозможен, `engine` должен написать `STOP` для methodology repository changes.

После `git pull --ff-only origin <METHODOLOGY_BASE_BRANCH>` локальный `HEAD` methodology repository должен строго совпадать с `origin/<METHODOLOGY_BASE_BRANCH>`. Если значения отличаются, `engine` должен написать `STOP`, потому что локальная methodology branch содержит состояние, которого нет в remote source of truth.

Если `engine` синхронизировал methodology repository в рамках задачи для target repository, он обязан вернуться в target repository через явный `cd <TARGET_REPOSITORY_LOCAL_PATH>` до проверки target remote, branch, working tree, файлов или выполнения изменений.

## Методологический feedback block

Если при работе с target repository выявлена необходимость доработки `agent-system-development`, ChatGPT должен вывести отдельный самодостаточный блок для engine-разработчика methodology repository.

Этот блок должен быть нейтральным и не должен раскрывать private downstream data, private repository URL, client data, customer data, credentials или internal code names.

В final report target repository такой вывод фиксируется как `Methodology repository improvement request`.

## Audit summary

Ответ с audit-задачей должен требовать от `engine` краткий audit summary:

- что проверено;
- что найдено;
- какие документы отсутствуют;
- какие риски есть;
- какой следующий PR рекомендуется;
- нужен ли отдельный methodology feedback.

Audit summary не заменяет полный audit artifact, если задача требует создать отдельный файл.

## Language consistency rule

ChatGPT и `engine` должны применять `docs/agent-system/LANGUAGE_POLICY.md` и проверять language consistency target docs.

Все user-facing answers, Engine final reports, TASK/RESULT/INDEX files, target-local methodology docs/templates и комментарии в файлах оформляются на русском языке.

Английский сохраняется только для code identifiers, команд, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, GitHub terms и literal external names, если перевод ухудшает точность.

Target project prompts должны включать Russian-first rule и требовать добавить его в target `AGENTS.md` или эквивалентные target instructions при adoption/update scope.

Engine-блок должен требовать от `engine` написать `STOP`, если target instructions конфликтуют с Russian-first policy и пользователь явно не разрешил другой язык для target repository.

## Русский язык документации target repository

После adoption audit и docs-only adoption целевые governance docs должны иметь один основной человеческий язык.

Если repository ведется на русском, смешанные англо-русские описания либо нормализуются, либо явно объясняются в audit/report.

## Запрет смешивания prompt, terminal commands и пояснений

Engine prompt, manual terminal commands и пояснения пользователю должны быть разделены.

Engine prompt помещается в Engine-блок. Ручные terminal-команды помещаются в отдельный раздел ручной работы. Пояснения остаются вне terminal blocks.

## Definition of Done для ответа

Ответ ChatGPT считается готовым, если:

- есть короткий вывод для пользователя;
- каждая engine-задача имеет отдельный самодостаточный Engine-блок;
- внутри Engine-блока есть все execution data;
- указан engine journal task/result path или причина, почему journal не применим;
- manual steps отделены от Engine-блока;
- проверки и STOP-условия не потеряны вне блока;
- methodology freshness check указан;
- language consistency rule указан, если задача связана с adoption;
- Russian-first policy указана для Engine final report и journal artifacts;
- methodology feedback нейтрален и не раскрывает private data;
- post-merge journal closure проверен или явно не применим;
- следующий шаг сформулирован явно.

## Пример правильного ответа

Правильный ответ:

- коротко объясняет пользователю, что будет сделано;
- выводит один раздел `Блок для Engine — копировать целиком`;
- внутри одного fenced code block содержит цель, контекст, ветки, allowed files, forbidden files, preflight, checks, STOP-условия, commit/push/PR policy и final report;
- ручную работу выводит отдельным разделом только если она действительно нужна пользователю.

## Пример неправильного ответа

Неправильный ответ:

- часть цели оставляет до Engine-блока;
- часть команд оставляет после Engine-блока;
- allowed files или forbidden files выносит в отдельный список вне блока;
- делает несколько разрозненных блоков для одной engine-задачи;
- смешивает manual terminal commands и engine prompt;
- не указывает, как проверялась актуальность methodology repository.

## Safety rules

- Не добавлять private downstream names.
- Не добавлять private repository URLs.
- Не добавлять client data или customer data.
- Не добавлять credentials, tokens, passwords, API keys или `.env`.
- Не печатать matching lines sensitive grep.
- Не читать `.env`.
- Не менять `main` или `developer` напрямую без отдельного разрешения.
- Не делать force push.
