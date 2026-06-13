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
- рекомендуемый режим Engine (Recommended Engine Mode):
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

Все эти данные должны быть внутри Engine-блока, если без них `engine` не сможет корректно выполнить задачу.

Если ChatGPT перед Engine-блоком пишет GitHub/local baseline, summary, current state, recommended mode, branch state, PR state, release/sync state или safety assumptions, и эти данные нужны `engine` для выполнения задачи, они должны быть продублированы внутри Engine-блока.

Нельзя оставлять уникальный execution context только в обычном тексте перед Engine-блоком. В обычном тексте перед блоком допускаются пояснения для пользователя, но не обязательные execution data.

## Что запрещено выносить за пределы Engine-блока

За пределами Engine-блока нельзя оставлять:

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

Вне Engine-блока можно давать только короткий вывод, контекст для пользователя, ссылки, цитаты и пояснения, которые не являются обязательными execution data.

## Защита перехода из Fast Lane в Engine-блок

Ответ ChatGPT может использовать Operational Fast Lane только пока остается read-only/status/cleanup-only.

Если в ходе анализа ChatGPT решает, что `engine` должен изменить repository files, обновить PR body, обновить journal artifacts, сделать commit, push, создать PR или исправить review findings через file edits, ChatGPT обязан прекратить Fast Lane.

До отправки пользователю actionable часть должна быть переписана как один полный self-contained Engine-блок с заголовком `Блок для Engine — копировать целиком`.

Запрещен гибридный ответ, где Fast Lane text содержит implementation instructions, требующие write actions от `engine`.

Триггером является рекомендуемое действие, а не исходная формулировка пользователя. Даже если пользователь попросил только review/status, как только ChatGPT рекомендует write changes, ответ становится Engine task.

Read-only review может завершиться фразой "нужна отдельная Engine-задача" только если:

- полный Engine-блок включен в ответ;
- или ChatGPT явно запрашивает решение пользователя, потому что scope/approval недостаточны.

Если следующий шаг уже ясен, безопасен и не требует уточнения, ChatGPT должен дать полный Engine-блок, а не неформальное указание "пусть Engine поправит".

## Языковая граница Engine-блоков

Engine-блоки являются user-facing task descriptions и должны соблюдать Russian-first policy.

Пользовательские заголовки и описания внутри Engine-блока должны быть на русском языке.

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

Термины `Engine`, `PR`, `commit`, `push`, `branch`, `merge`, `SHA`, `Local only`, `Reasoning`, `Agent` допустимы как technical terms или literal values, но не должны заменять русские пользовательские описания там, где описание можно написать по-русски.

## Блок для Engine — копировать целиком

Engine-блок должен быть одним fenced code block.

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
- рекомендуемый режим Engine (Recommended Engine Mode);
- проверенный execution baseline (Verified execution baseline) или явное `not applicable`;
- политика commit/push/PR;
- формат финального отчета.

Нельзя использовать вложенные fenced code blocks внутри Engine-блока. Для внутренних команд используются маркеры `BEGIN POWERSHELL`, `END POWERSHELL`, `BEGIN BASH`, `END BASH`.

## Предотправочный checklist для Engine-блока

Перед отправкой Engine-блока ChatGPT проверяет:

- [ ] Можно ли выполнить задачу, скопировав только один fenced code block?
- [ ] Есть ли внутри блока Recommended Engine Mode?
- [ ] Есть ли внутри блока Verified execution baseline или явное `not applicable`?
- [ ] Есть ли repository/base branch/working branch?
- [ ] Есть ли разрешенные файлы?
- [ ] Есть ли запрещенные файлы?
- [ ] Есть ли checks?
- [ ] Есть ли STOP-условия?
- [ ] Есть ли commit/push/PR policy, если задача создает изменения?
- [ ] Есть ли требования к финальному отчету?
- [ ] Нет ли обязательных execution data вне блока?
- [ ] Если ответ просит `engine` изменить файлы, есть ли ровно один полный Engine-блок для этой задачи?
- [ ] Остались ли write-action instructions вне Engine-блока?
- [ ] Если Fast Lane/status review выявил необходимость file changes, был ли Fast Lane остановлен и заменен полным Engine-блоком?
- [ ] Находятся ли PR body update, journal update, commit/push и review follow-up instructions внутри Engine-блока?
- [ ] Все ли пользовательские заголовки Engine-блока написаны на русском?
- [ ] Остался ли английский только в технических identifiers, commands, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names?
- [ ] Нет ли англоязычных служебных заголовков, если для них есть русская формулировка?
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
- язык final report: русский.

## Ответ Task File Handoff

Ответ Task File Handoff используется, когда Engine-блок становится слишком длинным, задача может забить context window или long task source of truth должен жить в Git history target repository.

Ответ ChatGPT в этом режиме должен содержать:

- repository;
- branch;
- путь к task file;
- commit SHA или blob SHA task file, если известно;
- короткий Engine bootstrap prompt;
- напоминания по безопасности;
- указание, что TASK file является source of truth;
- указание финализировать RESULT/INDEX после PR creation;
- инструкция выполнить Post-merge Journal Closure после merge/release/sync;
- напоминание Russian-first для final report и journal artifacts.

Если GitHub connector доступен и пользователь явно разрешил, ChatGPT может создать только task-file-only branch/commit с TASK file. ChatGPT не должен менять runtime, templates, RESULT, INDEX, governance files или другие docs в этом staging commit.

Bootstrap prompt не заменяет TASK file. Если TASK file и bootstrap prompt конфликтуют, `engine` должен написать `STOP`.

## Ручная работа пользователя

Ручная работа выводится только для действий, которые должен выполнить пользователь, а не `engine`.

Ручные действия должны быть явно помечены как ручные. Они не должны содержать данных, без которых `engine` не сможет выполнить свою задачу.

Если ручные действия нужны до запуска `engine`, они должны быть либо внутри Engine-блока как preflight для `engine`, либо в отдельном разделе `Ручная работа до запуска engine`. Даже в этом случае Engine-блок должен оставаться самодостаточным.

## Режим Operational Fast Lane

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
- внутри одного fenced code block содержит цель, контекст, ветки, разрешенные файлы, запрещенные файлы, предварительную проверку, проверки, STOP-условия, политику commit/push/PR и final report;
- ручную работу выводит отдельным разделом только если она действительно нужна пользователю.

## Пример неправильного ответа

Неправильный ответ:

- часть цели оставляет до Engine-блока;
- часть команд оставляет после Engine-блока;
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
