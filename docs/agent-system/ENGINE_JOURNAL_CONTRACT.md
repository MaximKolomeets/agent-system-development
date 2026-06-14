# ENGINE_JOURNAL_CONTRACT

## Назначение

Engine journal фиксирует воспроизводимый журнал задач для `engine` и ответов `engine`.

Английский alias: reproducible engine journal.

Цель журнала - сделать историю проекта восстановимой по GitHub files: кто сформулировал задачу, какой `engine` ее выполнил, какая ветка и Pull Request получились, какие проверки были выполнены и какой следующий шаг рекомендован.

Engine journal не заменяет Git history, Pull Request, commits или docs-maintainer reports. Он связывает их в одну читаемую цепочку:

```text
task file -> result file -> branch -> Pull Request -> commit/result
```

## Расположение

Каноническая папка:

```text
docs/agent-system/engine-journal/
```

Обязательная структура:

```text
docs/agent-system/engine-journal/
  README.md
  INDEX.md
  input/
  output/
  templates/
```

## Область template repository

`agent-system-development` is a reusable methodology/template repository.

In this repository, `docs/agent-system/engine-journal/` contains only scaffold,
contract, index, README, and reusable templates. The `input/` and `output/`
folders are intentionally empty except `.gitkeep`.

Real task/result files создаются в target repositories после adoption. Не
сохранять реальную TASK/RESULT history разработки methodology в этом template
repository и не копировать methodology operational history в target
repositories.

Исключение: если пользователь явно назначил methodology-hardening задачу для
самого `agent-system-development` и включил engine journal в allowed files/scope,
эта задача может создать собственные TASK/RESULT/INDEX entries в этом
repository. Такие entries не являются transferable template state и не должны
копироваться в target repositories. Ветка, PR, RESULT и INDEX все равно должны
быть Russian-first, append-only и финализированы после PR creation.

## Вход и выход

`input/` содержит входные задачи для `engine`.

`output/` содержит ответы `engine` по этим задачам.

`templates/` содержит reusable templates для task/result files.

Task file и result file должны иметь одинаковый sequence number и task id, чтобы их можно было сопоставить без внешнего контекста.

## Политика Russian-first journal

TASK/RESULT/INDEX files, user-facing labels, descriptions и final report должны быть на русском языке по `docs/agent-system/LANGUAGE_POLICY.md`.

Английский допустим только для technical identifiers, command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names.

Если target instructions конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая явного разрешения пользователя на другой язык.

## Именование

Рекомендуемое именование:

```text
TASK-0001-PR-2r-engine-journal-contract.md
RESULT-0001-PR-2r-engine-journal-contract.md
```

Где:

- `TASK` - входная задача для `engine`;
- `RESULT` - ответ `engine`;
- `0001` - сквозной номер в журнале;
- `PR-2r` - связанный task/PR id;
- `engine-journal-contract` - короткий slug.

## Index

`INDEX.md` содержит таблицу:

```text
| Seq | Task id | Input file | Output file | Branch | PR | Status | Notes |
```

Каждая journal entry должна быть добавлена в index отдельной строкой.

## Append-only правило

Engine journal является append-only по умолчанию.

Task/result files нельзя удалять, перезаписывать или переиспользовать для другой задачи без отдельного решения пользователя.

Если задачу нужно уточнить, создается новый task file с новым sequence number или добавляется отдельный follow-up task. Старый task/result остается как historical record.

## Режим Task File Handoff

TASK file может быть создан до выполнения как отдельный task-file-only commit в target repository.

В этом режиме TASK file является source of truth, а short bootstrap prompt только указывает `engine`, какой repository, branch и путь к task file прочитать.

RESULT обязан ссылаться на:

- путь к task file;
- commit SHA task source;
- blob SHA task file, если доступен;
- execution branch;
- execution PR URL;
- final commit SHA.

Если TASK file, bootstrap prompt, branch или source SHA конфликтуют, `engine` должен написать `STOP` и не выполнять задачу.

## Безопасность

Engine journal хранится в GitHub и считается публичным, если repository public.

Запрещено добавлять в journal:

- `.env`;
- credentials;
- tokens;
- private keys;
- real passwords;
- private repository URLs;
- private downstream project names;
- client/customer data;
- production/runtime data;
- secret values;
- logs with sensitive values.

Sensitive checks в journal result должны фиксировать только безопасный summary. Matching lines и secret values нельзя копировать в journal.

## Adoption target repository

При adoption target repository должен получить собственный `docs/agent-system/engine-journal/`.

Target repository journal хранит project-specific task/result history внутри target repository, а не в public methodology repository.

Первый adoption/audit PR должен создавать или обновлять:

- `docs/agent-system/engine-journal/README.md`;
- `docs/agent-system/engine-journal/INDEX.md`;
- `docs/agent-system/engine-journal/input/`;
- `docs/agent-system/engine-journal/output/`;
- `docs/agent-system/engine-journal/templates/`;
- task file для первой engine-задачи;
- result file для ответа engine.

Если первый шаг adoption остается `audit-only`, task/result files допускаются как journal artifacts рядом с `docs/agent-system/ADOPTION_AUDIT.md`, потому что они описывают выполнение audit, а не переносят full methodology state.

Adoption переносит только scaffold/templates. Первая target adoption/audit task
создает target-specific task/result files и target-specific записи `INDEX.md`.
Methodology repository operational history не переносится.

## Обязательные ссылки

Каждый result file должен ссылаться на:

- связанный task file;
- режим task source;
- commit SHA task source, если TASK file создан заранее;
- blob SHA task file, если доступен;
- task id;
- branch;
- commit SHA, если commit создан;
- PR URL, если PR создан;
- измененные файлы;
- запущенные проверки;
- результат проверки запрещенных файлов;
- результат sensitive/private marker;
- риски;
- следующий рекомендуемый шаг.

## Правило финализации после PR

`RESULT` и `INDEX` могут содержать временные placeholders только до создания PR.

После создания PR `engine` обязан обновить `RESULT` и `INDEX` фактическими значениями:

- финальная branch;
- final commit SHA;
- PR URL;
- PR status;
- запущенные проверки;
- blockers;
- следующий рекомендуемый шаг.

Если PR URL или final commit SHA стали известны только после materialization journal files, `engine` должен сделать follow-up commit в ту же рабочую ветку и push в тот же PR.

Финальный отчет задачи, которая создала PR, была смержена, обновила remote
`developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`,
должен содержать конкретный блок `Локальные действия после PR/merge` по
`docs/agent-system/WORKFLOW.md`.

Ready-for-review PR не должен содержать unresolved journal placeholders:

- `created after file materialization`;
- `pending at file materialization`;
- `see Engine final report`;
- `<commit SHA>`;
- `<PR URL>`;
- `<result>`;
- `<check command>`.

Reviewer должен считать такие placeholders blocker.

## Политика PR head SHA без self-reference

Commit не может честно содержать собственный SHA внутри файлов, включенных в этот же commit.

Journal artifacts могут фиксировать:

- `primary/materialization commit SHA`;
- `journal finalization commit SHA`;
- `follow-up materialization commit SHA`, если применимо;
- `latest known PR head SHA before follow-up`, если применимо;
- `actual/current PR head SHA after push`, если он проверен после push и может быть зафиксирован без self-referential loop.

Если запись `actual/current PR head SHA after final push` внутрь `RESULT` или `INDEX` требует бесконечного self-referential commit loop, `engine` не должен выдумывать false value.

В этом случае финальный отчет `engine` и PR body могут быть authoritative place для latest verified PR head SHA after final push.

`RESULT` и `INDEX` должны различать:

- commit SHA, зафиксированный в journal;
- actual/current PR head SHA, проверенный после final push.

Reviewer не должен требовать, чтобы commit содержал собственный SHA.

Unresolved placeholders остаются blockers, но явно отмеченное ограничение self-reference не считается placeholder.

## Post-merge Journal Closure

После merge рабочего PR target repository journal entry не должна оставаться в pre-merge статусе.

Task lifecycle закрыт только когда GitHub PR state и target journal RESULT/INDEX state согласованы.

Если рабочий PR, release PR или sync PR был merged, `RESULT` и `INDEX` должны быть закрыты фактическими post-merge данными:

- work PR status: `merged`;
- work PR merge commit SHA;
- work PR `merged_at`, если доступно;
- release PR URL/status/merge commit SHA/`merged_at`, если выполнялся release в `main`, иначе `не применимо`;
- sync PR URL/status/merge commit SHA/`merged_at`, если выполнялся sync `main -> developer`, иначе `не применимо`;
- `RESULT closed after merge: yes`;
- `INDEX closed after merge: yes`;
- `No journal placeholders: yes`;
- next step after closure;
- safe summary of checks.

После merge следующие значения являются недопустимыми final states в `RESULT` или `INDEX`:

- `PR open`;
- `ready for review`;
- `draft open`;
- `pending at file materialization`;
- `see Engine final report`.

Если merge commit SHA доступен в GitHub или local git history, `RESULT` должен зафиксировать его. Отсутствие merge commit SHA после merge без явного объяснения считается blocker.

Если final state в `RESULT`/`INDEX` противоречит GitHub PR state, reviewer должен считать это blocker.

Если PR body или GitHub state говорят, что PR merged/closed, но journal entry остается в состоянии `open`, `ready for review`, `not merged`, `submitted for review`, `PR open`, `draft open`, `pending at file materialization` или `see Engine final report`, reviewer должен считать это blocker.

Если release/sync PRs были merged, но journal не фиксирует release/sync facts, post-merge closure считается incomplete.

Post-merge closure не требует переписывать historical task/result content произвольно. Нужно добавить или обновить только closure-поля, final status и безопасный summary, сохранив append-only смысл journal entry.

## Правило review

### Проверка methodology repository

Для `agent-system-development` reviewer должен проверить, что:

- engine journal scaffold, templates, README и contract присутствуют;
- `input/` and `output/` are intentionally empty except `.gitkeep`;
- `INDEX.md` объясняет, что entries заполняются target repositories;
- real TASK/RESULT operational history не хранится в template repository;
- private downstream data, credentials, tokens или private repository URLs не добавлены.

### Проверка target repository

Перед merge PR reviewer должен проверить, что:

- task file и result file связаны одним sequence number;
- index обновлен;
- forbidden/private data не добавлены;
- task/result files не противоречат final report;
- branch, PR и commit references совпадают с фактическим GitHub state.
- ready-for-review PR не содержит unresolved journal placeholders в `RESULT` или `INDEX`;
- TASK/RESULT/INDEX являются Russian-first, кроме technical identifiers и literal external names.

Reviewer должен считать blocker, если merged PR journal:

- остается в статусе `PR open`;
- остается в статусе `ready for review`;
- остается в статусе `draft open`;
- содержит `pending at file materialization`;
- содержит `see Engine final report`;
- не фиксирует merge commit SHA после merge, когда SHA доступен;
- не фиксирует `RESULT closed after merge: yes`;
- не фиксирует `INDEX closed after merge: yes`.
