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
