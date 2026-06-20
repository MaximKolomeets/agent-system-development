# TASK_FILE_HANDOFF_CONTRACT

## Назначение

Task File Handoff Mode - режим постановки больших задач для `engine`, в котором long task source of truth хранится в TASK file внутри target repository, а короткий bootstrap prompt для исполнителя (engine) только указывает, где этот TASK file прочитать.

Режим нужен, чтобы длинные audit/adoption/bootstrap задачи не забивали context window и оставались воспроизводимыми через Git history target repository.

## Когда использовать

Использовать Task File Handoff Mode, когда:

- задача длинная и может забить context window;
- задача меняет несколько документов;
- задача требует audit, adoption или bootstrap;
- задача должна быть воспроизводимой;
- task prompt больше примерно 1500-2000 слов;
- задача должна жить в Git history target repository.

## Когда не использовать

Не использовать Task File Handoff Mode, когда:

- это простой status check;
- это cleanup без изменения файлов;
- нужна одноразовая короткая команда;
- задача не должна попадать в Git history;
- есть риск записать secrets/private data.

Для простых status/cleanup задач используется `docs/agent-system/OPERATIONAL_FAST_LANE.md`.

## GitHub staging для TASK file

Если GitHub connector доступен и пользователь явно разрешил materialization TASK file, оркестратор или другой разрешенный интерфейс может создать в target repository только task-file-only branch/commit.

Task-file-only staging:

- branch: `work/<agent-role>/<task-id-description>`;
- file: `docs/agent-system/engine-journal/input/TASK-XXXX-<task-id>.md`;
- allowed change for оркестратора in this mode: только TASK file;
- Оркестратор не должен менять runtime, docs кроме TASK file, templates, RESULT, INDEX или governance files;
- `engine` затем продолжает работу в этой же branch.

Если GitHub connector недоступен:

- оркестратор дает путь и content для TASK file;
- пользователь или `engine` materializes этот файл в target repository;
- `engine` все равно должен читать TASK file как source of truth.

## Короткий bootstrap prompt для исполнителя (engine)

Bootstrap prompt должен быть коротким и указывать только repository, branch, TASK file path и обязательные safety/finalization reminders.

Bootstrap prompt не должен содержать уникальные execution data, которых нет в TASK file. Если baseline, режим запуска, branch state, PR state, safety assumptions или execution constraints указаны в bootstrap prompt, они должны быть также зафиксированы в TASK file.

Пример:

```text
Прочитай и выполни TASK file:

Repository: <owner/repo>
Branch: <work branch>
Task file: docs/agent-system/engine-journal/input/TASK-XXXX-<task-id>.md

Считай TASK file источником правды.
Не читать `.env`.
Не менять `main`/`developer` напрямую.
Все ответы, final report, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке; English допускается только для технических identifiers, команд, путей, branch names, filenames, config keys, API names, package names, vendor/tool names и literal external names.
Если target instructions конфликтуют с Russian-first policy, напиши STOP и запроси решение пользователя.
После PR creation финализируй RESULT и INDEX: PR URL, final commit SHA, status и placeholder check.
После merge/release/sync выполни Post-merge Journal Closure: сверить GitHub PR state и journal state, зафиксировать PR status `merged`, merge commit SHA, `merged_at`, release/sync PR URL/status/merge commit SHA/`merged_at` или `не применимо`, `RESULT closed after merge: yes`, `INDEX closed after merge: yes` и `No journal placeholders: yes`.
```

## Приоритет источника правды

- TASK file имеет более высокий приоритет, чем chat summary.
- Bootstrap prompt только указывает `engine`, где прочитать задачу.
- Если TASK file и chat prompt конфликтуют, `engine` должен написать `STOP` и сообщить о конфликте.
- Если bootstrap prompt и TASK file конфликтуют, `engine` должен написать `STOP` и не продолжать выполнение.
- `engine` должен записать task file path и task source commit SHA или blob SHA в RESULT.
- `engine` не должен молча выполнять TASK file из неожиданного repository или branch.

## Обязательные metadata TASK file

TASK file для handoff должен содержать:

- путь к TASK file;
- task id;
- sequence number;
- target repository;
- base branch;
- working branch;
- task source mode: `task-file-handoff`;
- task source commit SHA, если известен;
- task file blob SHA, если доступен;
- bootstrap prompt reference;
- recommended engine mode:
  - launch mode;
  - model;
  - reasoning;
  - execution mode;
  - why this mode is required;
- verified baseline:
  - checked repository;
  - local path, если применимо;
  - checked base branch;
  - working branch;
  - latest relevant merged PR, если применимо;
  - release PR status, если применимо;
  - sync PR status, если применимо;
  - open PR state, если relevant;
  - baseline verification source;
  - baseline verification date/time;
- copy/paste completeness assertion:
  - TASK file is source of truth;
  - bootstrap prompt has no unique execution data not present in TASK file;
  - required execution context is not stored only in surrounding chat;
- allowed files;
- forbidden files;
- STOP conditions;
- checks;
- Russian-first policy;
- Journal finalization policy;
- policy Post-merge Journal Closure;
- final report requirements на русском языке.

## Требования к выполнению исполнителя (engine)

Перед выполнением `engine` должен проверить:

- repository full name или remote соответствует bootstrap prompt и TASK file;
- current branch соответствует expected work branch или может быть безопасно переключена;
- TASK file path существует на expected branch/ref;
- task source commit SHA или blob SHA совпадает, если указан;
- working tree чистый до изменений, если TASK file явно не разрешает иначе;
- TASK file не требует читать `.env` или использовать secrets/private data;
- TASK file требует русский язык для final report и journal artifacts;
- target instructions не конфликтуют с Russian-first policy или пользователь явно разрешил другой язык для target repository.

Если repository, branch, path, commit SHA или blob SHA не совпадают, `engine` должен написать `STOP`.

Если target instructions конфликтуют с Russian-first policy, `engine` должен написать `STOP` и сообщить о конфликте до изменений.

## Требования к финализации journal

`RESULT` должен фиксировать:

- task source mode;
- task file path;
- task source commit SHA;
- task file blob SHA, if available;
- execution branch;
- execution PR URL;
- final commit SHA;
- статус PR после review (`PR status after review`);
- merge commit SHA после merge, если доступен;
- `merged_at` date/time, если доступно;
- release PR URL/status/merge commit SHA/`merged_at`, если release выполнялся;
- sync PR URL/status/merge commit SHA/`merged_at`, если sync выполнялся;
- RESULT finalized status;
- INDEX finalized status;
- status `RESULT closed after merge`;
- status `INDEX closed after merge`;
- no journal placeholders status;
- language policy result;
- follow-up finalization commit SHA, if finalization required a second commit.

После PR creation `engine` должен финализировать `RESULT` и `INDEX` фактическими PR URL, final commit SHA, PR status, checks, blockers и next recommended step.

После merge рабочего PR, release PR или sync PR `engine` должен финализировать post-merge closure в `RESULT` и `INDEX`. Journal entry не может оставаться в статусах `PR open`, `ready for review`, `draft open`, `pending at file materialization` или `see Engine final report`. Если GitHub PR state и journal state расходятся, TASK file handoff не считается закрытым.

User-facing labels/descriptions в RESULT и INDEX должны быть Russian-first.

Ready-for-review PR не должен содержать unresolved journal placeholders.

## Safety constraints

- Do not read `.env`.
- Do not add credentials, tokens, private keys, real passwords or secret values.
- Do not add private downstream project names, private repository URLs, client data, customer data or production/runtime data.
- Do not change `main` or `developer` directly.
- Do not use Task File Handoff Mode for runtime, CI or Docker changes unless a separate task explicitly allows that scope.
- Do not create real TASK/RESULT operational history in the public methodology repository.
- Do not create mostly English user-facing TASK/RESULT/INDEX files when Russian-first policy applies.

## Review blockers

Reviewer must block the PR if:

- TASK file source repository, branch or path is ambiguous;
- RESULT does not record task source commit SHA or blob SHA when available;
- `engine` executed a TASK file from an unexpected repository or branch;
- TASK file and bootstrap prompt conflict and execution continued without STOP;
- bootstrap prompt contains unique execution data absent from TASK file;
- ready-for-review PR contains unresolved journal placeholders;
- RESULT or INDEX is not finalized after PR creation;
- merged PR journal remains `PR open`;
- merged PR journal remains `ready for review`;
- merged PR journal remains `draft open`;
- merged PR journal contains `pending at file materialization`;
- merged PR journal contains `see Engine final report`;
- RESULT lacks merge commit SHA after merge when available;
- RESULT or INDEX is not closed after merge;
- TASK/RESULT/INDEX, final report or target-local templates are mostly English without explicit user language decision;
- private data, credentials, `.env`, private repository URLs or real target project names were added.
