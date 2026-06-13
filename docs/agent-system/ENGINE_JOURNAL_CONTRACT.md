# ENGINE_JOURNAL_CONTRACT

## Назначение

Engine journal фиксирует воспроизводимый журнал задач для `engine` и ответов `engine`.

English alias: reproducible engine journal.

Цель журнала - сделать историю проекта восстановимой по GitHub files: кто сформулировал задачу, какой `engine` ее выполнил, какая ветка и Pull Request получились, какие проверки были выполнены и какой следующий шаг рекомендован.

Engine journal не заменяет Git history, Pull Request, commits или docs-maintainer reports. Он связывает их в одну читаемую цепочку:

```text
task file -> result file -> branch -> Pull Request -> commit/result
```

## Location

Canonical folder:

```text
docs/agent-system/engine-journal/
```

Required structure:

```text
docs/agent-system/engine-journal/
  README.md
  INDEX.md
  input/
  output/
  templates/
```

## Template Repository Scope

`agent-system-development` is a reusable methodology/template repository.

In this repository, `docs/agent-system/engine-journal/` contains only scaffold,
contract, index, README, and reusable templates. The `input/` and `output/`
folders are intentionally empty except `.gitkeep`.

Real task/result files are created in target repositories after adoption. Do not
store real methodology development TASK/RESULT history in this template
repository, and do not copy methodology operational history into target
repositories.

## Input And Output

`input/` содержит входные задачи для `engine`.

`output/` содержит ответы `engine` по этим задачам.

`templates/` содержит reusable templates для task/result files.

Task file и result file должны иметь одинаковый sequence number и task id, чтобы их можно было сопоставить без внешнего контекста.

## Russian-first journal policy

TASK/RESULT/INDEX files, user-facing labels, descriptions и final report должны быть на русском языке по `docs/agent-system/LANGUAGE_POLICY.md`.

Английский допустим только для technical identifiers, command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names.

Если target instructions конфликтуют с Russian-first policy, `engine` должен написать `STOP` и запросить решение пользователя, кроме случая явного разрешения пользователя на другой язык.

## Naming

Recommended naming:

```text
TASK-0001-PR-2r-engine-journal-contract.md
RESULT-0001-PR-2r-engine-journal-contract.md
```

Where:

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

## Append-Only Rule

Engine journal является append-only по умолчанию.

Task/result files нельзя удалять, перезаписывать или переиспользовать для другой задачи без отдельного решения пользователя.

Если задачу нужно уточнить, создается новый task file с новым sequence number или добавляется отдельный follow-up task. Старый task/result остается как historical record.

## Task File Handoff Mode

TASK file может быть создан до выполнения как отдельный task-file-only commit в target repository.

В этом режиме TASK file является source of truth, а short bootstrap prompt только указывает `engine`, какой repository, branch и task file path прочитать.

RESULT обязан ссылаться на:

- task file path;
- task source commit SHA;
- task file blob SHA, если доступен;
- execution branch;
- execution PR URL;
- final commit SHA.

Если TASK file, bootstrap prompt, branch или source SHA конфликтуют, `engine` должен написать `STOP` и не выполнять задачу.

## Safety

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

## Target Repository Adoption

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

Adoption transfers scaffold/templates only. The first target adoption/audit task
creates target-specific task/result files and target-specific `INDEX.md`
entries. Methodology repository operational history is not transferred.

## Required Links

Каждый result file должен ссылаться на:

- related task file;
- task source mode;
- task source commit SHA, если TASK file создан заранее;
- task file blob SHA, если доступен;
- task id;
- branch;
- commit SHA, если commit создан;
- PR URL, если PR создан;
- changed files;
- checks run;
- forbidden files result;
- sensitive/private marker result;
- risks;
- next recommended step.

## Post-PR Finalization Rule

`RESULT` и `INDEX` могут содержать временные placeholders только до создания PR.

После создания PR `engine` обязан обновить `RESULT` и `INDEX` фактическими значениями:

- final branch;
- final commit SHA;
- PR URL;
- PR status;
- checks run;
- blockers;
- next recommended step.

Если PR URL или final commit SHA стали известны только после materialization journal files, `engine` должен сделать follow-up commit в ту же рабочую ветку и push в тот же PR.

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

Если рабочий PR, release PR или sync PR был merged, `RESULT` и `INDEX` должны быть закрыты фактическими post-merge данными:

- PR status: `merged`;
- merge commit SHA;
- `merged_at` date/time, если доступно;
- release PR URL/status/merge commit SHA, если выполнялся release в `main`;
- sync PR URL/status/merge commit SHA, если выполнялся sync `main -> developer`;
- `RESULT closed after merge: yes`;
- `INDEX closed after merge: yes`;
- `No journal placeholders: yes`.

После merge следующие значения являются недопустимыми final states в `RESULT` или `INDEX`:

- `PR open`;
- `ready for review`;
- `draft open`;
- `pending at file materialization`;
- `see Engine final report`.

Если merge commit SHA доступен в GitHub или local git history, `RESULT` должен зафиксировать его. Отсутствие merge commit SHA после merge без явного объяснения считается blocker.

Post-merge closure не требует переписывать historical task/result content произвольно. Нужно добавить или обновить только closure-поля, final status и безопасный summary, сохранив append-only смысл journal entry.

## Review Rule

### Methodology Repository Review

For `agent-system-development`, reviewer must verify that:

- engine journal scaffold, templates, README, and contract are present;
- `input/` and `output/` are intentionally empty except `.gitkeep`;
- `INDEX.md` explains that entries are populated by target repositories;
- no real TASK/RESULT operational history is stored in the template repository;
- no private downstream data, credentials, tokens, or private repository URLs are added.

### Target Repository Review

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
