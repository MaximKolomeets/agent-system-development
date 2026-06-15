# WORKFLOW

1. Пользователь принимает решение.
2. ChatGPT помогает сформулировать задачу.
3. Задача оформляется по шаблону.
4. Исполнитель работает в своей ветке.
5. Исполнитель обновляет отчет.
6. Проверяющий агент делает review.
7. Пользователь принимает решение о merge.
8. После merge обновляются `CURRENT_STATE` и `DECISION_LOG`, если нужно.

## Шаблоны отчётов и решений

- Универсальный отчёт роли (не-PR работ, исследований, status-апдейтов): `docs/agent-system/templates/AGENT_REPORT_TEMPLATE.md` (Summary, Changed files, Checks, Risks, Open questions, Next step).
- Запись решения для `docs/agent-system/DECISION_LOG.md`: `docs/agent-system/templates/DECISION_TEMPLATE.md` (Date, Decision, Context, Options considered, Reason, Consequences, Follow-up actions).
- Review report: `docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md` (полный 10-секционный шаблон + раздел «Облегчённый PR/comment review»).

## Режимы применения

### Lightweight solo-operator mode

Этот режим используется, когда один оператор ведет задачу end-to-end. Он не требует искусственно запускать несколько агентов для маленькой docs-only или status-задачи.

Минимальные правила остаются обязательными:

- direct changes в `main`/`developer` запрещены без отдельного решения пользователя;
- file-changing task идет через `work/<role>/<task>` и PR;
- TASK/RESULT/INDEX создаются и финализируются, если задача меняет repository files или создает PR;
- Operational Fast Lane допускается только для read-only/status/cleanup без file edits;
- final report содержит проверки, риски и локальный sync block после PR/merge.

### Multi-agent governed mode

Этот режим используется для задач с высоким риском, несколькими исполнителями, review gate, runtime scope или target adoption.

Дополнительно требуется:

- явное разделение orchestrator, engine и reviewer responsibilities;
- review-only boundary для reviewer roles;
- отдельные implementation tasks для исправления findings;
- полный self-contained Engine-блок или Task File Handoff Mode;
- воспроизводимые journal artifacts и PR metadata.

## Anti-overengineering checkpoint

Перед добавлением нового документа, роли, workflow, template или gate нужно ответить:

- решает ли изменение повторяющуюся проблему, уже встреченную в работе;
- можно ли обойтись правкой существующего документа или checklist;
- не превращает ли изменение простой solo-operator workflow в обязательную multi-agent церемонию;
- есть ли явный trigger, когда правило обязательно, и когда оно не применяется;
- не добавляет ли изменение runtime/CI/Docker scope в docs-only задачу.

Если ответ неясен, изменение фиксируется как proposed follow-up, а не как обязательное правило.

## После bootstrap

- Прямые изменения в `developer` запрещены без отдельного разрешения пользователя.
- Рабочий поток идет через ветки `work/<role>/*`.
- Рабочая ветка создается от актуальной `developer`.
- `developer` принимает изменения через PR из рабочих веток.
- `developer` -> `main` выполняется только после проверки интеграционной ветки.

## Review-only workflow

Code review / external review / consulting review по умолчанию выполняется как review-only task:

```text
developer -> work/<reviewer-role>/<task-id> -> PR в developer
```

Review report по умолчанию возвращается в чат. Review-only PR создается только если пользователь явно разрешил docs-only сохранение отчета в repository.

Review-only PR содержит только review report files и journal/state updates, если они явно разрешены задачей.

Reviewer не исправляет production code, runtime, Docker, CI, scripts или dependencies. Findings превращаются в отдельные implementation PR только после решения пользователя.

Reviewer не запускает Codex/Engine, не меняет очередь исполнителя и не формулирует себе implementation task. Он может предложить кандидаты на будущие задачи, но решение принимает пользователь вместе с ChatGPT.

Review task должен явно указывать:

- режим: `review-only`, `docs-only` или `fix-allowed`;
- объект проверки: PR, branch, commit, diff или files;
- base branch;
- working branch, если нужна;
- allowed files;
- forbidden files;
- разрешенные и запрещенные команды;
- можно ли сохранять отчет в repository;
- можно ли создавать PR.

Для standard developer workflow review стартует от `developer`, конкретного PR/diff/branch/commit/files. `main` используется только если пользователь явно указал, что нужно проверить стабильную версию.

Подробный контракт:

```text
docs/agent-system/CODE_REVIEW_WORKFLOW.md
```

## Локальные действия после PR/merge

Если задача создала PR, была смержена, обновила remote `developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`, финальный отчет в чат должен содержать конкретный блок:

```text
## Локальные действия после PR/merge
```

Для PR в `developer` минимальный блок:

````text
## Локальные действия после PR/merge

Когда PR будет смержен в developer, выполнить локально:

```powershell
cd <repo-path>

git status --short
git fetch --all --prune

git switch developer
git pull --ff-only origin developer

git rev-parse developer
git rev-parse origin/developer
git status --short
```

Ожидаемый результат:

```text
developer == origin/developer
working tree clean
```
````

Если затронут `main`, добавить:

```powershell
git switch main
git pull --ff-only origin main

git switch developer
git pull --ff-only origin developer
```

Если локальная ветка устарела или расходится, вместо общих советов вывести диагностику:

```powershell
git status --short
git branch --show-current
git fetch --all --prune
git rev-parse developer
git rev-parse origin/developer
git log --oneline --decorate --left-right developer...origin/developer
git worktree list
```

Запрещено рекомендовать `git reset --hard`, если пользователь явно не подтвердил, что локальные изменения и локальные commits не нужны.
