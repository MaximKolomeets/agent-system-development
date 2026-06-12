# TASK_FILE_HANDOFF_CONTRACT

## Purpose

Task File Handoff Mode - режим постановки больших задач для `engine`, в котором long task source of truth хранится в TASK file внутри target repository, а short Engine bootstrap prompt только указывает, где этот TASK file прочитать.

Режим нужен, чтобы длинные audit/adoption/bootstrap задачи не забивали context window и оставались воспроизводимыми через Git history target repository.

## When To Use

Использовать Task File Handoff Mode, когда:

- задача длинная и может забить context window;
- задача меняет несколько документов;
- задача требует audit, adoption или bootstrap;
- задача должна быть воспроизводимой;
- task prompt больше примерно 1500-2000 слов;
- задача должна жить в Git history target repository.

## When Not To Use

Не использовать Task File Handoff Mode, когда:

- это простой status check;
- это cleanup без изменения файлов;
- нужна одноразовая короткая команда;
- задача не должна попадать в Git history;
- есть риск записать secrets/private data.

Для простых status/cleanup задач используется `docs/agent-system/OPERATIONAL_FAST_LANE.md`.

## GitHub Task-File Staging

Если GitHub connector доступен и пользователь явно разрешил materialization TASK file, ChatGPT или другой разрешенный интерфейс может создать в target repository только task-file-only branch/commit.

Task-file-only staging:

- branch: `work/<agent-role>/<task-id-description>`;
- file: `docs/agent-system/engine-journal/input/TASK-XXXX-<task-id>.md`;
- allowed change for ChatGPT in this mode: только TASK file;
- ChatGPT не должен менять runtime, docs кроме TASK file, templates, RESULT, INDEX или governance files;
- `engine` затем продолжает работу в этой же branch.

Если GitHub connector недоступен:

- ChatGPT дает путь и content для TASK file;
- пользователь или `engine` materializes этот файл в target repository;
- `engine` все равно должен читать TASK file как source of truth.

## Short Engine Bootstrap Prompt

Bootstrap prompt должен быть коротким и указывать только repository, branch, TASK file path и обязательные safety/finalization reminders.

Example:

```text
Read and execute the task file:

Repository: <owner/repo>
Branch: <work branch>
Task file: docs/agent-system/engine-journal/input/TASK-XXXX-<task-id>.md

Treat the task file as the source of truth.
Do not read .env.
Do not change main/developer directly.
After PR creation, finalize RESULT and INDEX with PR URL, final commit SHA, status and placeholder check.
```

## Source Of Truth Precedence

- TASK file has higher priority than chat summary.
- Bootstrap prompt only tells `engine` where to read the task.
- If TASK file and chat prompt conflict, `engine` must STOP and report conflict.
- `engine` must record task file path and task source commit SHA or blob SHA in RESULT.
- `engine` must not silently execute a task file from an unexpected repository or branch.

## Required TASK File Metadata

TASK file created for handoff must include:

- task file path;
- task id;
- sequence number;
- target repository;
- base branch;
- working branch;
- task source mode: `task-file-handoff`;
- task source commit SHA, if known;
- task file blob SHA, if available;
- bootstrap prompt reference;
- allowed files;
- forbidden files;
- STOP conditions;
- checks;
- Journal finalization policy;
- final report requirements.

## Engine Execution Requirements

Before execution, `engine` must verify:

- repository full name or remote matches the bootstrap prompt and TASK file;
- current branch matches the expected work branch or can be checked out safely;
- TASK file path exists at the expected branch/ref;
- task source commit SHA or blob SHA matches, if provided;
- working tree is clean before changes, unless the TASK file explicitly allows otherwise;
- TASK file does not require reading `.env` or using secrets/private data.

If repository, branch, path, commit SHA or blob SHA do not match, `engine` must STOP.

## Journal Finalization Requirements

`RESULT` must record:

- task source mode;
- task file path;
- task source commit SHA;
- task file blob SHA, if available;
- execution branch;
- execution PR URL;
- final commit SHA;
- RESULT finalized status;
- INDEX finalized status;
- no journal placeholders status;
- follow-up finalization commit SHA, if finalization required a second commit.

After PR creation, `engine` must finalize `RESULT` and `INDEX` with factual PR URL, final commit SHA, PR status, checks, blockers and next recommended step.

Ready-for-review PR must not contain unresolved journal placeholders.

## Safety Constraints

- Do not read `.env`.
- Do not add credentials, tokens, private keys, real passwords or secret values.
- Do not add private downstream project names, private repository URLs, client data, customer data or production/runtime data.
- Do not change `main` or `developer` directly.
- Do not use Task File Handoff Mode for runtime, CI or Docker changes unless a separate task explicitly allows that scope.
- Do not create real TASK/RESULT operational history in the public methodology repository.

## Review Blockers

Reviewer must block the PR if:

- TASK file source repository, branch or path is ambiguous;
- RESULT does not record task source commit SHA or blob SHA when available;
- `engine` executed a TASK file from an unexpected repository or branch;
- TASK file and bootstrap prompt conflict and execution continued without STOP;
- ready-for-review PR contains unresolved journal placeholders;
- RESULT or INDEX is not finalized after PR creation;
- private data, credentials, `.env`, private repository URLs or real target project names were added.
