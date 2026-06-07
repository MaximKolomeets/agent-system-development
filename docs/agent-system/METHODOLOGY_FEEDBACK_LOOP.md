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

## Как превращать feedback в задачи

Feedback из target repository не должен автоматически менять methodology repository.

Правильный поток:

1. `engine` пишет Methodology feedback в final report target repository;
2. пользователь переносит только безопасную обобщенную часть в ChatGPT;
3. ChatGPT формирует отдельную задачу для `agent-system-development`;
4. изменения идут через отдельный PR в methodology repository;
5. после merge methodology repository обновляется;
6. следующий target repository dry run использует обновленную методологию.

## Примеры безопасных feedback items

- "Нужен checklist для проверки, что engine запущен в правильном repository."
- "Нужен template для adoption audit."
- "Нужен автоматический preflight report."
- "Нужно явно запретить печатать matching lines sensitive grep."
- "Нужен шаблон для описания conflicts with local AGENTS.md."

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
