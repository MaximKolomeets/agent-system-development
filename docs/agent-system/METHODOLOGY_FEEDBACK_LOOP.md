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

В любом RESULT/final report `engine` должен добавить секцию:

```text
## Methodology feedback
```

Если feedback отсутствует, писать `нет`.

Поля:

- `what_was_unclear` - что было неясно в template repository;
- `missing_template_docs` - каких шаблонов или инструкций не хватило;
- `manual_steps_to_automate` - какие ручные шаги стоит автоматизировать;
- `safety_gaps` - какие safety rules нужно усилить;
- `target_repo_conflicts` - какие конфликты с локальными правилами target repository возникли;
- `suggested_methodology_prs` - какие PR стоит создать в `agent-system-development`;
- `do_not_publish` - что нельзя переносить в public methodology repository.

Если во время задачи появилось вне-scope предложение, `engine` дополнительно
заполняет обязательный раздел:

```text
## Unprompted Project Proposals
```

Этот раздел ведется по `AGENT_INITIATIVE_PROTOCOL.md`; если предложений нет,
писать `нет`.

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
6. `METHODOLOGY_IMPROVEMENT_LEDGER.md` обновляет lifecycle status: MIR, PR,
   release/snapshot и adoption category;
7. следующий target repository dry run использует обновленную методологию только
   после stable source: `main`, release tag или published snapshot.

Шапка задачи должна указывать рекомендуемый режим запуска, engine, модель, reasoning, режим работы и причину выбора режима. `<task-id>` должен быть связан с GitHub issue, Pull Request, task id или внутренним номером работы проекта.

## Closure policy feedback

Если после merge/release/sync target `RESULT` или `INDEX` не синхронизированы с GitHub PR state, проверять контекст по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` → «Closure policy». Для обычного work PR допустимо `merged; closure pending` до batch-closure перед release; нарушение возникает под release gate, audit/review consistency gate, adoption/source-update, завершением/паузой серии или явным closure-заданием.

Безопасный feedback pattern:

- описать проблему нейтрально: `target repository journal entry remains in pre-merge state after merge`;
- не переносить project-specific details, private repository URLs, branch names, PR numbers или SHA из target repository;
- создать docs-only journal closure cleanup task с фактическими merge данными внутри target repository, если сработало per-task исключение, release/audit/methodology boundary или противоречие journal facts;
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

## Sanitized downstream feedback loop

Новый reusable loop для downstream/project feedback описан в `docs/agent-system/DOWNSTREAM_FEEDBACK_LOOP.md`, а обязательный redaction gate - в `docs/agent-system/DOWNSTREAM_FEEDBACK_SANITIZATION_POLICY.md`.

Перед созданием methodology task feedback item проходит sanitization checkpoint, classification и backlog grouping. Target repository не является source of truth для reusable methodology, target-specific details не переносятся в active methodology docs, а target repositories получают изменения только после `main`, release tag или явно опубликованного Source/cloud snapshot.

Methodology task по sanitized feedback не читает target repository, если это прямо не разрешено task scope. Dirty/open target work branches не являются blocker для methodology repository work и не фиксируются как methodology fact.

Lifecycle после sanitized feedback ведется в `METHODOLOGY_IMPROVEMENT_LEDGER.md`.
Ledger хранит только public-safe MIR lifecycle facts и не заменяет private
consumer registry/adoption matrix в private control plane.

## Связь с инициативными предложениями

`Methodology feedback` описывает улучшения methodology repository, замеченные в
ходе задачи. `Unprompted Project Proposals` описывает вне-scope идеи или риски,
которые требуют triage до превращения в задачу.

Оба раздела обязательны в новых RESULT. Proposal не меняет текущий allowed scope
и не дает reviewer role права назначать implementation task напрямую.

## Acceptance criteria

Feedback loop считается соблюденным, если:

- final report содержит Methodology feedback;
- final report содержит Unprompted Project Proposals;
- feedback не раскрывает приватные данные;
- suggested methodology improvements сформулированы нейтрально;
- отдельные изменения в `agent-system-development` выполняются только отдельным PR.
