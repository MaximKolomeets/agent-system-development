# CODE_REVIEW_TASK_TEMPLATE

Ниже расположен самодостаточный copy/paste-блок для `engine`. Перед использованием заменить placeholders в угловых скобках.

````text
Задача для <reviewer-role>: <task-id>

Рекомендуемый режим исполнения:

Роль: reviewer (<code-reviewer-01 | qa-reviewer-01 | security-reviewer-01>)
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: задача выполняет review-only audit/review без исправления кода; journal PR создается всегда, а тело отчета сохраняется в repository только при `Report delivery: repository` или `chat+repository`.
Время начала выполнения (execution_started_at) [measured/engine]: <ISO-8601 timestamp with timezone>
Время оркестрации, по факту (orchestration_time_reported) [reported/human, опционально]: <свободное значение или пусто>

## Repository

Repository:

```text
<repository-url>
```

Локальный путь:

```text
<local-path>
```

## Lifecycle and branch model

Lifecycle mode:

```text
<new empty bootstrap | existing adoption | existing implementation | methodology repository review>
```

Selected branch model:

```text
<standard developer workflow | main-only flow | other explicit model>
```

Base branch:

```text
<developer | main | other explicit base>
```

Working branch:

```text
work/<reviewer-role>/<task-id>
```

Reviewer role:

```text
<code-reviewer-01 | qa-reviewer-01 | security-reviewer-01>
```

Engine (опционально, исполнителя назначает архитектор; имя инструмента фиксируется постфактум, не как рекомендация):

```text
<engine-name | на усмотрение архитектора>
```

Review mode:

```text
<review-only | docs-only | fix-allowed>
```

Review object:

```text
<PR | branch | commit | diff | files>
```

Report delivery:

```text
<chat | repository | chat+repository>
```

Дефолт: `chat` (тело отчёта в чат, в repository не сохраняется).

Journal trace:

```text
always (required by docs/agent-system/ENGINE_JOURNAL_CONTRACT.md)
```

Любая review-задача создаёт TASK/RESULT/INDEX entries и делает docs-only PR в `developer` с journal artefacts, независимо от `Report delivery`.

PR creation allowed:

```text
yes (для journal artefacts всегда; для тела отчёта — если Report delivery включает repository)
```

## Russian-first policy

Final report, review report, TASK/RESULT/INDEX и target-local docs/templates писать на русском языке.

English допустим только для code identifiers, commands, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names и literal external names.

## Goal

Провести review repository и создать review report.

Reviewer должен:

- изучить repository;
- выполнить безопасные checks;
- описать findings;
- предложить кандидаты на будущие implementation PRs, если нужны fixes;
- вернуть **тело** review report согласно `Report delivery` (дефолт `chat`);
- **всегда** создать engine-journal TASK/RESULT/INDEX и открыть docs-only PR в `base` с journal artefacts (`Journal trace: always`);
- добавить report-файл в тот же PR, только если `Report delivery` включает `repository`.

Reviewer не должен исправлять production code в этой задаче.
Reviewer не должен запускать исполнителя (engine), менять очередь исполнителя или формулировать себе implementation task.
Если review object — активный work PR, reviewer оставляет comments/blockers как feedback к той же task branch. Исправления выполняет engine в исходной `work/<role>/<task-id>` branch; reviewer не создает отдельный PR для feedback без явного решения пользователя.

## Конвенция: review PR на GitHub по head SHA

Если `Review object` = `PR`, ревью выполняется по конкретному PR на GitHub и пиннится к head SHA для воспроизводимости — через `gh`:

```powershell
gh pr view <pr-number> --json number,headRefName,headRefOid,state,mergeable,baseRefName
gh pr diff <pr-number>
git fetch origin pull/<pr-number>/head
git checkout <headRefOid>   # head SHA из `gh pr view`
```

Review report и RESULT фиксируют reviewed head SHA. Если PR обновился после ревью (head SHA сменился), вердикт относится только к зафиксированному head SHA, что отмечается явно.

Reviewer сверяет «Source Delta» из проверяемого PR с фактическим diff и `docs/agent-system/ADOPTION_TRANSFER_MANIFEST.yml`: все inventory-изменения отражены, категории соответствуют manifest, Source-рекомендации корректны, `manifest обновлён?` правдив. Для `added`/`deleted`/`renamed` inventory-файлов категории `source`, `template` или `target_generated` отсутствие manifest update является finding/blocker по канону `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Source Delta».

Reviewer сверяет, что новые TASK/RESULT записи содержат measured execution-поля по `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Execution timestamps»: `execution_started_at` в TASK/RESULT и `execution_finished_at` в RESULT. Отсутствие этих полей в finalized записи является minor finding, но не blocker; optional `reported/human` поля не проверяются как обязательные.

## Required preflight

```powershell
cd <local-path>
git rev-parse --show-toplevel
git remote -v
git fetch --all --prune
git branch --show-current
git status --short
```

Если working tree не clean и пользователь не разрешил работать с текущими изменениями, написать `STOP`.

Если selected branch model неясна, написать `STOP`.

Если selected branch model = `standard developer workflow`, рабочая ветка должна создаваться только от актуальной `developer`.

## Create branch

Для standard developer workflow:

```powershell
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status --short
```

Если `git status --short` не пустой — STOP. Не выполнять stash/reset/clean/checkout поверх локальных изменений без отдельного решения пользователя.

Затем:

```powershell
git fetch --all --prune
git switch <base>
git pull --ff-only origin <base>
git status --short
git switch -c work/<reviewer-role>/<task-id>
git rev-parse --abbrev-ref HEAD
```

Если HEAD не `work/<reviewer-role>/<task-id>` — STOP.

Для main-only flow использовать `main` только если это явно указано в selected branch model.

## Allowed files

Всегда обязательны (`Journal trace: always`):

```text
docs/agent-system/engine-journal/input/TASK-<actual-next-seq>-<task-id>-<slug>.md
docs/agent-system/engine-journal/output/RESULT-<actual-next-seq>-<task-id>-<slug>.md
docs/agent-system/engine-journal/INDEX.md
```

`<actual-next-seq>` engine вычисляет из `docs/agent-system/engine-journal/INDEX.md` на момент выполнения. Нельзя предсказывать, переиспользовать или пропускать sequence.

Дополнительно — только если task явно их разрешает:

```text
<review-report-path>          # только при Report delivery: repository или chat+repository
<state-docs-if-explicitly-allowed>
```

Если файл не указан в allowed files, не менять его.

При `Report delivery: chat` тело отчёта в repository не сохраняется.

Journal artefacts всё равно создаются, коммитятся, пушатся и идут в docs-only PR в `base`.

При `Report delivery: repository` или `chat+repository` разрешённые места для тела отчёта:

```text
docs/agent-system/reviews/                 # target-local create-on-demand convention; не methodology-source directory
docs/agent-system/agents/<review-agent-name>/
```

## Forbidden files and paths

Запрещено читать, создавать, изменять или коммитить:

```text
.env
.env.*
.venv/
data/
runtime/
dist/
backups/
exports/
*.log
*.tmp
*.bak
credentials
tokens
passwords
cookies
Authorization/session headers
private downstream data
client data
runtime code
Dockerfile
docker-compose.yml
.github/workflows/**
scripts/**
```

## Naming rules

Запрещено использовать vendor/tool names в:

- reviewer role name;
- branch name;
- report filename;
- docs path;
- task id, если task id описывает роль.

Engine name указывать только в отдельном поле `Engine`.

## Required checks

Выполнить минимум:

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

Sensitive grep выводить только filename-only. Matching lines не печатать.

Tests/linters запускать только если они описаны в repository docs, не требуют `.env`, не запускают production services, не обращаются к private data и не меняют рабочие данные.

Если tests/linters не запускались, объяснить почему.

## Report path

Использовать как target-local create-on-demand convention, только если `Report delivery` включает `repository`:

```text
docs/agent-system/reviews/<task-id>-review.md
```

Этот путь создаётся в потребляющем проекте при необходимости и не означает, что `docs/agent-system/reviews/` обязан существовать в methodology-source repository.

Если `docs/agent-system/` отсутствует:

```text
docs/reviews/<task-id>-review.md
```

Report filename не должен содержать vendor/tool name.

## Report structure

```text
# <TASK-ID> - review report

## 1. Объект проверки

## 2. Что было проверено

## 3. Запущенные команды

## 4. Команды, которые не запускались, и почему

## 5. Найденные проблемы

### Критично

### Желательно

### Опционально

## 6. Security / forbidden files risks

## 7. Несоответствия документации и фактического состояния

## 8. Рекомендации

## 9. Кандидаты на будущие задачи Engine

## 10. Итоговый вывод
```

## Шаги commit, push и PR

Любая review-задача выполняет один docs-only commit, push рабочей ветки и открывает PR в `base` — для journal artefacts (`Journal trace: always`). Дефолт `Report delivery: chat` НЕ отменяет этот PR; «chat-only» касается только тела отчёта.

В commit включаются:

- всегда: `engine-journal/input/TASK-<actual-next-seq>-*.md`, `engine-journal/output/RESULT-<actual-next-seq>-*.md`, `engine-journal/INDEX.md`;
- дополнительно (только при `Report delivery: repository` или `chat+repository`): файл тела отчёта по `Report naming`;
- иное — только если явно входит в allowed files (например, явно разрешённые state docs).

Запрещено:

- direct push в `main` или `developer`;
- branch from `main` для standard developer workflow;
- vendor-specific branch names;
- vendor-specific report filenames;
- fixing code в `review-only`-задаче;
- launching исполнителя (engine) or assigning implementation work to self;
- reading `.env`;
- printing sensitive grep matching lines.

Команды:

```powershell
git status --short
git diff --check
git diff --name-only <base>...HEAD
git add <allowed-files>
git commit -m "<commit-message>"
git push -u origin work/<reviewer-role>/<task-id>
```

Создать PR:

```text
Base: <base>
Head: work/<reviewer-role>/<task-id>
Title: <review task title>
```

Журнал финализируется после создания PR. После merge closure выполняется по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: default — batch перед release/audit/methodology boundary; per-task — только для explicit closure gate, release/audit consistency gate, финального PR перед release, adoption/source-update, противоречивых journal facts или другого явно указанного исключения. В closure-review reviewer сверяет merge-факты по `RESULT` closure-stamp и GitHub/local git; `INDEX` проверяется как status + PR URL и не обязан содержать полный merge commit SHA.

## Локальные действия после PR/merge

Если journal PR создан или обнаружен рассинхрон с `origin/*`, final report должен включать блок `Локальные действия после PR/merge` по каноническому разделу `docs/agent-system/WORKFLOW.md`.

## Final report

Ответить на русском:

```text
- branch;
- PR URL;
- changed files;
- created files;
- checks run;
- forbidden paths result;
- sensitive grep filename-only result;
- vendor-specific naming check result;
- reviewed head SHA, если Review object = PR;
- Source Delta review result: сверка с diff/manifest, findings по категориям, рекомендациям и manifest flag;
- risks;
- next step;
- Передача — блок `Следующий: <роль> — <что делает>` и batch-friendly формулировка, если применимо (канон `docs/agent-system/templates/TASK_HEADER_COMMON.md` → «Передача»);
- Source-reminder, если review менял методологию/каноны (`Обновить Source-снапшот у зарегистрированных потребителей: …` из `docs/agent-system/SOURCE_CONSUMERS.md`); иначе «не применимо»;
- локальные действия после PR/merge, если PR создан или обнаружен рассинхрон с `origin/*`.
```
````
