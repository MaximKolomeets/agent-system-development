# CODE_REVIEW_WORKFLOW

## Назначение

Этот workflow описывает безопасный code review / external review / consulting review для methodology repository и target implementation repositories.

Цель workflow - подключать любой `engine` как reviewer-консультанта без vendor-specific имен в ролях, ветках, путях, filenames, task ids и отчетах.

`engine` указывается отдельно от роли:

```text
engine=<engine-name>
reviewer role=code-reviewer-01
```

Role name, branch namespace и report filename не должны зависеть от vendor/tool name.

## Роли reviewer

Рекомендуемые роли:

- `code-reviewer-01` - общий review архитектуры, структуры, кода, тестов, документации и рисков;
- `qa-reviewer-01` - review тестов, quality gates, регрессий и проверяемости;
- `security-reviewer-01` - review секретов, forbidden paths, auth/config risks и security guardrails.

Reviewer roles не исправляют найденные проблемы по умолчанию. Они возвращают **тело** review report в чат по умолчанию.

Одновременно reviewer roles **всегда** журналируют TASK + RESULT, обновляют INDEX по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md` и создают docs-only PR с journal artefacts в `developer`.

Если task дополнительно разрешает сохранять **тело** отчёта в repository (`Report delivery` включает `repository`), reviewer кладёт report-файл рядом с journal artefacts в том же PR.

Implementation выполняется отдельной задачей, отдельной веткой и отдельным PR, например:

```text
work/dev-implementer-01/<task-id>
```

## Review-only по умолчанию

Reviewer по умолчанию:

- изучает repository;
- запускает read-only или безопасные checks;
- пишет review report;
- возвращает **тело** review report в чат (`Report delivery: chat` — дефолт);
- **всегда** создаёт engine-journal TASK + RESULT + INDEX entry и делает docs-only PR с journal artefacts в `developer` (`Journal trace: always`);
- не меняет production code;
- не исправляет найденные проблемы;
- не делает refactor;
- не меняет runtime, Docker, CI, scripts или dependencies без отдельной задачи;
- не читает `.env`;
- не печатает matching lines sensitive grep.
- не запускает исполнителя (engine);
- не меняет очередь исполнителя;
- не формулирует себе implementation task.

Если пользователь просит исправить findings, нужно создать отдельную implementation task. Review report может предложить next PRs, но не должен сам превращаться в fix PR. Решение принимает пользователь вместе с оркестратором.

## Report delivery и Journal trace

Review-задачи различают два независимых понятия.

**Report delivery** — куда уходит **тело** отчёта (длинный markdown с findings/recommendations):

- `chat` (дефолт) — тело отчёта возвращается в чат и в repository не сохраняется;
- `repository` — тело отчёта сохраняется в repository по `Report naming`;
- `chat+repository` — тело отчёта дублируется в чат и в repository.

**Journal trace** — фиксация задачи в `docs/agent-system/engine-journal/`:

- `always` — обязательное правило. Любая review-задача (включая `review-only` с `Report delivery: chat`) создаёт TASK в `engine-journal/input/`, RESULT в `engine-journal/output/` и строку в `INDEX.md`, делает один docs-only commit, push рабочей ветки и PR в `developer`. Append-only, sequence, Russian-first, без placeholders — по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`.

`Report delivery: chat` сохраняет обязательный journal trace. «Chat-only» относится к телу отчёта, а journal-след всё равно создается.

`Journal trace: always` совместима с режимами `review-only`, `docs-only` и `fix-allowed`: в `review-only` PR содержит только journal artefacts; в `docs-only` дополнительно может содержать report-файл; в `fix-allowed` — также явно разрешённые правки.

## Режимы review task

Каждая review task должна явно указать один режим:

- `review-only` - reviewer проверяет PR/branch/commit/diff/files и возвращает тело отчёта согласно `Report delivery` (дефолт `chat`); `Journal trace: always` сохраняется — TASK/RESULT/INDEX создаются и идут в docs-only PR.
- `docs-only` - reviewer может сохранить review report или state docs в repository в дополнение к обязательному journal trace.
- `fix-allowed` - reviewer может менять только явно разрешенные файлы и только если пользователь отдельно разрешил исправления; этот режим требует отдельного scope, allowed files, forbidden files, checks и STOP-условий; `Journal trace: always` сохраняется.

Каждая review task должна явно указать объект проверки:

```text
PR / branch / commit / diff / files
```

## Именование веток

Для standard developer workflow используется модель:

```text
main -> developer -> work/<role>/* -> PR в developer
```

Reviewer branch создается от актуальной `developer`:

```text
work/code-reviewer-01/<task-id>
work/qa-reviewer-01/<task-id>
work/security-reviewer-01/<task-id>
```

Namespace `review/*` не является каноническим branch namespace этого repository. Review-задачи используют `work/<reviewer-role>/<task-id>` по `docs/agent-system/BRANCH_POLICY.md`.

Запрещено:

- создавать reviewer branch от `main` для standard developer workflow;
- открывать review PR напрямую в `main`;
- делать direct push в `main` или `developer`;
- использовать vendor/tool name в branch namespace.

По умолчанию review работает от `developer` или от конкретного PR/diff/branch/commit/files. `main` используется только если пользователь явно указал, что нужно проверить стабильную версию.

Если target implementation repository использует main-only flow, это должно быть явно зафиксировано в task как selected branch model. Если branch model неясна, reviewer пишет `STOP`.

## Vendor-neutral именование

Vendor/tool names запрещены в:

- role names;
- branch names;
- report filenames;
- docs paths;
- task ids, если task id описывает роль, а не внешний инструмент.

Bad examples:

```text
tool-name/initial-review
tool-review
docs/TOOL_REVIEW.md
```

Good examples:

```text
work/code-reviewer-01/initial-project-review
work/security-reviewer-01/dependency-risk-review
work/qa-reviewer-01/test-gap-review
docs/agent-system/templates/CODE_REVIEW_REPORT_TEMPLATE.md
docs/agent-system/agents/qa-reviewer-01/REPORTS.md
```

Depers-check: bare-слово «модель» само по себе не является vendor-marker, если рядом нет vendor/tool name и это не label вида `Модель: <имя исполнителя>`. Остаточная строка `Модель: <имя исполнителя>` в task/header scope заменяется на `Reasoning effort`.

## Именование report

Тело review report по умолчанию (`Report delivery: chat`) возвращается в чат и в repository не сохраняется.

Если task разрешает `Report delivery: repository` или `chat+repository`, тело отчёта сохраняется в repository рядом с journal artefacts.

Journal artefacts (TASK/RESULT/INDEX) создаются всегда независимо от `Report delivery`.

Для target implementation repository использовать:

```text
docs/reviews/<task-id>-review.md
```

Для methodology repository рекомендуемый путь:

```text
docs/agent-system/agents/<reviewer-role>/REPORTS.md
```

Для role-specific накопительных notes допустим путь:

```text
docs/agent-system/agents/<review-agent-name>/
```

Report filename не должен содержать vendor/tool name.

## Разрешённый scope

Review-only PR может содержать только files, явно разрешенные task.

Типичный scope:

- review report;
- engine journal TASK/RESULT/INDEX, если task включает engine journal;
- state docs, если task явно разрешает state update.

Запрещенный scope по умолчанию:

- production code fixes;
- refactor;
- runtime changes;
- Docker changes;
- CI changes;
- dependency changes;
- scripts changes;
- private downstream data;
- `.env` и `.env.*`;
- credentials, tokens, passwords, cookies, Authorization/session headers.

## Проверки безопасности (safety gates)

Перед review reviewer проверяет:

- repository соответствует task;
- remote соответствует expected repository;
- selected branch model указан;
- base branch определен;
- working tree clean или пользователь явно разрешил работать с текущими изменениями;
- forbidden tracked paths отсутствуют;
- sensitive grep выполняется filename-only;
- `.env` не читается.

Если gate не пройден, reviewer пишет:

```text
STOP
```

После `STOP` reviewer кратко указывает причину и не меняет файлы.

## Обязательные checks

Минимальный набор checks:

```powershell
git rev-parse --show-toplevel
git remote -v
git fetch --all --prune
git branch --show-current
git status --short
git ls-files
git diff --check
git diff --name-only <base>...HEAD
git ls-files | Select-String -Pattern '(^|/)(\.env|\.venv|data|runtime|dist|backups|exports)(/|$)|\.(log|tmp|bak)$'
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" -- 2>$null
```

Sensitive grep result должен быть filename-only. Matching lines не печатать.

Reviewer может запускать tests/linters только если:

- они описаны в README/RUNBOOK/package scripts;
- они не требуют `.env`;
- они не запускают production services;
- они не обращаются к private data;
- они не меняют рабочие данные.

Если tests/linters не запускались, reviewer объясняет почему в review report.

## Структура report

Review report должен использовать структуру:

```text
# <TASK-ID> - отчёт review

## 1. Объект проверки

## 2. Что было проверено

## 3. Запущенные команды

## 4. Команды, которые не запускались, и почему

## 5. Найденные проблемы

### Критично

### Желательно

### Опционально

## 6. Риски security / forbidden files

## 7. Несоответствия документации и фактического состояния

## 8. Рекомендации

## 9. Кандидаты на будущие задачи исполнителя (engine)

## 10. Итоговый вывод
```

Раздел `Кандидаты на будущие задачи исполнителя (engine)` содержит только предложения. Reviewer не запускает исполнителя (engine) и не ставит задачи исполнителю напрямую.

## Финальный отчёт

Final report reviewer пишет на русском языке и включает:

- branch;
- PR URL, если PR создан;
- changed files;
- created files;
- checks run;
- forbidden paths result;
- sensitive grep filename-only result;
- vendor-specific naming check result;
- risks;
- next step.

## Передача findings в следующие PR

Findings не исправляются внутри review-only task.

Для каждого finding reviewer может предложить next PR:

```text
role=<implementation-role>
branch=work/dev-implementer-01/<task-id>
scope=<короткое описание исправления>
base=<developer|explicit branch model>
```

Пользователь принимает отдельное решение, какие findings превращать в implementation PR.

## Анти-паттерн (anti-pattern)

Запрещенный prompt:

```text
Создай ветку tool-name/initial-review от main, сделай review, запиши docs/TOOL_REVIEW.md, закоммить.
```

Почему запрещено:

- model/vendor-specific branch name;
- старт от `main` без явного решения;
- review-агент сам превращается в исполнителя;
- отчет сохраняется без отдельного разрешения;
- файл назван по модели, а не по роли;
- нет allowed/forbidden files;
- нет режима `review-only` / `docs-only` / `fix-allowed`;
- нет объекта проверки PR/branch/commit/diff/files.

## Безопасный пример: REVIEW-INITIAL-01

```text
Задача для qa-reviewer-01: REVIEW-INITIAL-01

Режим: review-only.
Объект проверки: проект agent-system-development на базе developer.
Код не менять.
Production-файлы не менять.
Report delivery: chat (тело отчёта в чат).
Journal trace: always (TASK/RESULT/INDEX обязательно, docs-only PR в developer).
Сохранять тело отчёта в repository только после отдельного разрешения пользователя (Report delivery: repository или chat+repository).

Проверить:
- структуру проекта;
- AGENTS.md;
- README.md;
- docs/agent-system/*;
- branch policy;
- role model;
- workflow;
- templates;
- соответствие методологии фактическим правилам.

Не читать:
- .env
- .env.*

Не коммитить:
- .env
- .venv/
- data/
- runtime/
- dist/
- backups/
- exports/

Если отчет разрешено сохранить:
- ветка: work/qa-reviewer-01/review-initial-01
- файл: docs/agent-system/agents/qa-reviewer-01/REPORTS.md
- только docs-only commit.
```

## Локальные действия после PR/merge

Если review-задача создала PR, была смержена, обновила remote `developer`/`main` или обнаружила рассинхрон локальной ветки с `origin/*`, final report должен содержать конкретный блок `Локальные действия после PR/merge` по `docs/agent-system/WORKFLOW.md`.
