# METHODOLOGY_FEEDBACK_LOOP

## Назначение

Документ описывает feedback loop между target repository dry run и methodology repository.

Цель feedback loop:

- фиксировать, что оказалось неудобным при применении методологии;
- выявлять, какие инструкции не хватило автоматизировать;
- предлагать улучшения для `agent-system-development`;
- не переносить private data из target repository в public methodology repository.

## Когда используется

Feedback loop используется после:

- repository self-discovery;
- adoption audit;
- bootstrap PR;
- CI guardrail PR;
- role/worktree setup;
- любого target repository dry run.

## Что engine должен добавить в final report

В финальном отчете по target repository `engine` должен добавить секцию:

```text
## Methodology feedback
```

Поля:

- `what_was_unclear` - что было неясно в template repository;
- `missing_template_docs` - каких шаблонов или инструкций не хватило;
- `manual_steps_to_automate` - какие ручные шаги стоит автоматизировать;
- `safety_gaps` - какие safety rules нужно усилить;
- `target_repo_conflicts` - какие конфликты с локальными правилами target repository возникли;
- `suggested_methodology_prs` - какие PR стоит создать в `agent-system-development`;
- `do_not_publish` - что нельзя переносить в public methodology repository.

## Что запрещено переносить

- реальные credentials;
- tokens;
- passwords;
- API keys;
- `.env`;
- клиентские данные;
- персональные данные;
- внутренние кодовые имена;
- приватные URL;
- содержимое private downstream repository, если оно раскрывает приватный контекст.

## Sanitization checkpoint

Перед созданием methodology PR каждый feedback item нужно привести к нейтральному виду:

- заменить конкретное имя repository на `target implementation repository`;
- заменить private/local paths на обобщенные категории вроде `target docs path` или `runtime config path`;
- удалить target branch names, PR numbers, commit SHA, timestamps и private issue ids, если они не нужны для универсального правила;
- удалить имена клиентов, пользователей, команд, внутренних систем и code names;
- не цитировать private logs, prompts, source snippets, configs или file contents;
- описать problem pattern, reusable methodology change, affected docs/templates и acceptance criteria.

Если после sanitization item теряет смысл или все еще раскрывает private context, его нельзя переносить в public methodology repository. Такой feedback остается в target repository или private notes.

## Как превращать feedback в задачи

Feedback из target repository не должен автоматически менять methodology repository.

Правильный поток:

1. `engine` пишет Methodology feedback в final report target repository;
2. пользователь переносит только безопасную обобщенную часть оркестратору;
3. оркестратор формирует отдельную русскоязычную задачу для `agent-system-development` с обязательной шапкой `Задача для <роль>: <task-id>`;
4. изменения идут через отдельный PR в methodology repository;
5. после merge methodology repository обновляется;
6. следующий target repository dry run использует обновленную методологию.

Шапка задачи должна указывать рекомендуемый режим запуска, engine, модель, reasoning, режим работы и причину выбора режима. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Post-merge journal feedback

Если после merge/release/sync target `RESULT` или `INDEX` остаются в pre-merge status, это methodology compliance blocker.

Безопасный feedback pattern:

- описать проблему нейтрально: `target repository journal entry remains in pre-merge state after merge`;
- не переносить project-specific details, private repository URLs, branch names, PR numbers или SHA из target repository;
- создать docs-only journal closure cleanup task с фактическими merge данными внутри target repository;
- если проблема повторяется, создать отдельный methodology PR с обобщенным hardening proposal.

## Примеры безопасных feedback items

- "Нужен checklist для проверки, что engine запущен в правильном repository."
- "Нужен template для adoption audit."
- "Нужен автоматический preflight report."
- "Нужно явно запретить печатать matching lines sensitive grep."
- "Нужен шаблон для описания conflicts with local AGENTS.md."
- "Если review/status workflow обнаруживает, что repository files должны быть изменены, методология должна принудительно переводить режим из Operational Fast Lane в полный self-contained блок для исполнителя (engine)."
- "Если блок для исполнителя (engine) нарушает Russian-first policy пользовательскими англоязычными заголовками, это считается methodology compliance issue."

## Примеры небезопасных feedback items

- реальные имена клиентов;
- private repository URL;
- реальные внутренние названия;
- секреты;
- фрагменты `.env`;
- конкретные рабочие данные;
- приватные логи.

## Acceptance criteria

Feedback loop считается соблюденным, если:

- final report содержит Methodology feedback;
- feedback не раскрывает приватные данные;
- suggested methodology improvements сформулированы нейтрально;
- отдельные изменения в `agent-system-development` выполняются только отдельным PR.
