# CHATGPT_RESPONSE_TEMPLATE

## Назначение

Этот template задает copy/paste-ready структуру ответа ChatGPT, если ответ содержит задачу для `engine`.

## Короткий вывод

Кратко опишите, что обнаружено или что будет сделано. Не помещайте сюда execution data, без которых `engine` не сможет выполнить задачу.

## Блок для Engine — копировать целиком

```text
Задача для <agent-name>: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: <Local only | Cloud allowed | Hybrid>
Модель: <model recommendation>
Reasoning: <Low | Medium | High>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима>

Цель:

<одна конкретная цель задачи>

Target repository:

<owner/repository или URL>

Target repository local path:

<TARGET_REPOSITORY_LOCAL_PATH>

Methodology repository:

https://github.com/MaximKolomeets/agent-system-development

Methodology repository local path:

<METHODOLOGY_REPOSITORY_LOCAL_PATH>

Methodology base branch:

<METHODOLOGY_BASE_BRANCH, обычно developer>

Файл задачи Engine:

docs/agent-system/engine-journal/input/TASK-<SEQ>-<task-id>-<slug>.md

Ожидаемый файл результата Engine:

docs/agent-system/engine-journal/output/RESULT-<SEQ>-<task-id>-<slug>.md

Engine journal policy:

- task/result files сохраняются в `docs/agent-system/engine-journal/`;
- task/result files связываются одним `SEQ` и `<task-id>`;
- task/result files append-only и не удаляются/не перезаписываются без решения пользователя;
- result file обязателен как artifact final report;
- private data, secrets, credentials, tokens, private repository URLs и production/runtime data в journal запрещены.
- TASK/RESULT/INDEX labels and descriptions пишутся на русском языке, кроме technical identifiers и literal external names.
- после PR creation RESULT/INDEX финализируются фактическими PR URL, commit SHA, PR status и placeholder check.
- после merge/release/sync RESULT/INDEX закрываются по Post-merge Journal Closure: PR status `merged`, merge commit SHA, release/sync PR данные при наличии, `RESULT closed after merge: yes`, `INDEX closed after merge: yes`, `No journal placeholders: yes`.

Language policy:

Все ответы, final report, target-local docs/templates, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке. English допускается только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, code identifiers и literal external names.

Обязательная проверка актуального agent-system-development:

- перед применением методологии проверить актуальную версию methodology repository;
- если используется локальная копия, сначала проверить clean working tree;
- выполнить `git fetch --all --prune`;
- проверить наличие `origin/<METHODOLOGY_BASE_BRANCH>`;
- переключиться на `<METHODOLOGY_BASE_BRANCH>`;
- выполнить `git pull --ff-only origin <METHODOLOGY_BASE_BRANCH>`;
- проверить, что локальный `HEAD` строго равен `origin/<METHODOLOGY_BASE_BRANCH>`;
- только после успешного fast-forward pull и `HEAD == origin/<METHODOLOGY_BASE_BRANCH>` считать локальную methodology repository актуальной;
- после синхронизации methodology repository обязательно вернуться в target repository через `cd <TARGET_REPOSITORY_LOCAL_PATH>`;
- если выполнялся только fetch без pull, не писать, что локальная копия синхронизирована;
- если актуальность проверить невозможно, явно указать это в final report.

Base branch:

<base branch>

Working branch:

work/<role>/<task>

Разрешенные файлы:

- <allowed path>

Запрещенные файлы и изменения:

- `.env`
- `.venv/`
- `data/`
- `runtime/`
- `dist/`
- `backups/`
- `exports/`
- runtime code, если задача docs-only
- CI/Docker, если задача не разрешает такие изменения
- private data
- secrets

Preflight:

BEGIN POWERSHELL
# Перейти в локальную копию methodology repository, чтобы синхронизировать методологию перед подготовкой задачи.
cd <METHODOLOGY_REPOSITORY_LOCAL_PATH>

# Проверить рабочее дерево methodology repository до pull, чтобы не перетереть локальные изменения.
$methodologyStatus = git status --short
if ($methodologyStatus) {
  Write-Output "STOP: methodology repository working tree is not clean"
  $methodologyStatus
  exit 1
}

# Забрать актуальные remote refs methodology repository.
git fetch --all --prune

# Проверить наличие remote base branch methodology repository перед переключением.
$methodologyRemoteBranch = git branch -r --list origin/<METHODOLOGY_BASE_BRANCH>
if (-not $methodologyRemoteBranch) {
  Write-Output "STOP: methodology remote base branch not found"
  exit 1
}

# Переключиться на локальную methodology base branch для fast-forward синхронизации.
git switch <METHODOLOGY_BASE_BRANCH>

# Подтянуть локальную methodology branch строго fast-forward, чтобы не работать по устаревшим файлам.
git pull --ff-only origin <METHODOLOGY_BASE_BRANCH>

# Проверить, что локальная methodology branch строго совпадает с remote branch после pull.
$methodologyLocal = git rev-parse HEAD
$methodologyRemote = git rev-parse origin/<METHODOLOGY_BASE_BRANCH>
if ($methodologyLocal -ne $methodologyRemote) {
  Write-Output "STOP: methodology local HEAD does not match origin/<METHODOLOGY_BASE_BRANCH>"
  Write-Output "local: $methodologyLocal"
  Write-Output "remote: $methodologyRemote"
  exit 1
}

# Проверить, что working tree methodology repository остался clean после синхронизации.
$methodologyPostStatus = git status --short
if ($methodologyPostStatus) {
  Write-Output "STOP: methodology repository working tree changed during sync"
  $methodologyPostStatus
  exit 1
}

# Вернуться в target repository перед любыми target checks или изменениями.
cd <TARGET_REPOSITORY_LOCAL_PATH>

# Проверить корень repository, чтобы не выполнить задачу в неправильной папке.
git rev-parse --show-toplevel

# Проверить remote, чтобы подтвердить целевой repository.
git remote -v

# Проверить активную ветку до переключений.
git branch --show-current

# Проверить рабочее дерево, чтобы не перетереть локальные изменения.
git status --short

# Обновить remote refs для проверки актуальности base branch.
git fetch --all --prune
END POWERSHELL

Конкретные изменения:

- <изменение 1>
- <изменение 2>

Checks:

BEGIN POWERSHELL
# Проверить активную ветку после изменений.
git branch --show-current

# Проверить список измененных файлов.
git status --short

# Проверить whitespace/errors в diff.
git diff --check

# Проверить, что journal не содержит stale post-merge placeholders.
git grep -I -l -E "PR open|ready for review|draft open|pending at file materialization|see Engine final report" -- docs/agent-system/engine-journal

# Выполнить filename-only sensitive grep без вывода matching lines.
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --
END POWERSHELL

STOP-условия:

- current repository не соответствует задаче;
- remote не соответствует target repository;
- working tree dirty до старта и нет явного разрешения пользователя;
- base branch отсутствует;
- pull fast-forward невозможен;
- обнаружены private data или secrets;
- требуются изменения вне allowed files.

Commit/push/PR policy:

- коммитить только allowed files;
- не делать force push;
- Pull Request создавать в base branch;
- не делать auto-merge.
- после merge/release/sync выполнить или явно запланировать post-merge journal closure для RESULT/INDEX.

Финальный отчет:

- repository root;
- remote summary;
- base branch;
- working branch;
- created files;
- changed files;
- checks run;
- checks not run and why;
- sensitive grep result без matching lines;
- risks;
- STOP conditions encountered;
- language policy result;
- commit SHA;
- push status;
- PR link/number;
- статус PR после review (`PR status after review`);
- merge commit SHA после merge, если доступен;
- release PR URL/status/merge commit SHA, если release выполнялся;
- sync PR URL/status/merge commit SHA, если sync выполнялся;
- RESULT закрыт после merge;
- INDEX закрыт после merge;
- проверка Post-merge Journal Closure;
- engine result file;
- Methodology repository improvement request, если нужен.
```

## Ручная работа

Раздел нужен только для действий пользователя, а не `engine`.

### Ручная задача 1: <название>

```powershell
# Комментарий объясняет, что делает команда и зачем пользователь запускает ее вручную.
<manual command>
```

Каждая независимая ручная задача должна иметь отдельный раздел и отдельный terminal block.

## Блок для разработчика methodology repository

Этот раздел добавляется только если нужна доработка `agent-system-development`.

```text
Задача для methodology-maintainer-01: <task-id>

Рекомендуемый режим <engine-name>:

Запуск: Local only
Модель: <model recommendation>
Reasoning: High
Режим: Agent
Почему: задача меняет reusable methodology repository и должна быть выполнена отдельной веткой и Pull Request.

Цель:

<нейтрально описать улучшение methodology repository без private downstream data>

Repository:

https://github.com/MaximKolomeets/agent-system-development

Разрешенные файлы:

- <methodology files>

Forbidden data:

- private downstream names
- private repository URLs
- client data
- customer data
- internal code names
- credentials
- `.env`

Checks:

BEGIN POWERSHELL
# Проверить diff на запрещенные private/downstream markers.
git grep -I -l -i -E "private repo url|client data|customer data|internal code name" -- docs/agent-system
END POWERSHELL

Финальный отчет:

- summary;
- changed files;
- checks;
- private data check result;
- language policy result;
- PR link/number.
```

## Проверка результата

Укажите команды проверки и ожидаемые признаки успеха. Если команды нужны `engine`, они должны быть продублированы внутри Engine-блока.

## Риски и STOP-условия

Кратко перечислите главные риски для пользователя. Execution STOP-условия для `engine` должны оставаться внутри Engine-блока.

## Следующий шаг

Укажите один конкретный следующий шаг.
