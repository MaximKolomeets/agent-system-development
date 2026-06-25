# ORCHESTRATOR_RESPONSE_TEMPLATE

## Machine-readable task_contract

Если ответ содержит блок для исполнителя (engine), который меняет repository files, создаёт PR или описывает substantive/tooling/docs-only/review/fix-pass/release/adoption task, в начало блока нужно добавить fenced YAML `task_contract` по `docs/agent-system/TASK_CONTRACT.md`.

Fast Lane/status check без write-action, PR и journal trace может идти без `task_contract`. Если `task_contract` присутствует и конфликтует с prose, engine должен написать `STOP` и запросить решение архитектора.

## Назначение

Этот template задает copy/paste-ready структуру ответа оркестратора, если ответ содержит задачу для `engine`.

## Короткий вывод

Кратко опишите, что обнаружено или что будет сделано. Не помещайте сюда execution data, без которых `engine` не сможет выполнить задачу.

Если Fast Lane/status review выявил необходимость менять repository files, PR body, journal artifacts или branch state через commit/push, остановите Fast Lane и перепишите actionable часть в полный self-contained блок для исполнителя (engine).

Не оставляйте write-action instructions вне блока для исполнителя (engine).

## Блок для исполнителя (engine) — копировать целиком

```text
Задача для <роль>: <task-id>

Рекомендуемый режим исполнения:

Роль: <функция в методологии: docs-maintainer | reviewer | dev-implementer | infra | source-steward | ...>
Исполнитель: на усмотрение архитектора
Reasoning effort: <низкий | средний | высокий>
Запуск: <Local only | Cloud allowed | Hybrid>
Режим: <Agent | Ask | Manual review>
Почему: <краткое обоснование выбора режима и reasoning effort>

Цель:

<одна конкретная цель задачи>

Целевой репозиторий:

<owner/repository или URL>

Локальный путь целевого репозитория:

<TARGET_REPOSITORY_LOCAL_PATH>

Методологический репозиторий:

https://github.com/MaximKolomeets/agent-system-development

Локальный путь методологического репозитория:

<METHODOLOGY_REPOSITORY_LOCAL_PATH>

Базовая ветка методологии:

<METHODOLOGY_BASE_BRANCH, обычно developer>

Файл задачи исполнителя (engine):

docs/agent-system/engine-journal/input/TASK-<actual-next-seq>-<task-id>-<slug>.md

Ожидаемый файл результата исполнителя (engine):

docs/agent-system/engine-journal/output/RESULT-<actual-next-seq>-<task-id>-<slug>.md

`<actual-next-seq>` не предсказывается в блоке оркестратора. Исполнитель (engine) вычисляет его из `docs/agent-system/engine-journal/INDEX.md` на момент выполнения.

Политика engine journal:

- task/result files сохраняются в `docs/agent-system/engine-journal/`;
- task/result files связываются одним `<actual-next-seq>` и `<task-id>`;
- task/result files append-only и не удаляются/не перезаписываются без решения пользователя;
- result file обязателен как artifact final report;
- private data, secrets, credentials, tokens, private repository URLs и production/runtime data в journal запрещены.
- TASK/RESULT/INDEX labels и описания пишутся на русском языке, кроме technical identifiers и literal external names.
- после PR creation RESULT/INDEX финализируются фактическими PR URL, commit SHA, PR status и placeholder check.
- после merge/release/sync применяется Closure policy по `docs/agent-system/ENGINE_JOURNAL_CONTRACT.md`: обычные work PR закрываются batch-closure перед release; per-task closure используется только для release/state docs, audit/review consistency gate, adoption/source-update, завершения/паузы серии или явного closure-задания.

Языковая политика:

Все ответы, final report, target-local docs/templates, TASK/RESULT/INDEX и комментарии в файлах писать на русском языке. English допускается только для command names, flags, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, code identifiers и literal external names.

Пользовательские заголовки и описания внутри блока для исполнителя (engine) писать на русском языке. Не использовать англоязычные служебные заголовки вроде `Required changes`, `Checks`, `Expected checks result`, `Commit/push policy`, `Final report requirements`, `STOP conditions`, `Allowed files`, `Forbidden files`, если есть нормальная русская формулировка.

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

Базовая ветка:

<base branch>

Рабочая ветка:

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

Предварительная проверка:

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

Проверки:

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
- требуются изменения вне разрешенных файлов.
- implementation prompt просит изменить файлы, но не содержит repository, branch, разрешенные файлы, запрещенные файлы, проверки, STOP-условия и требования к финальному отчету, кроме случая действительного TASK file как source of truth.
- пользовательские заголовки и описания массово оформлены на английском языке без технической необходимости при действующей Russian-first policy.

Политика commit/push/PR:

- коммитить только разрешенные файлы;
- не делать force push;
- Pull Request создавать в base branch;
- не делать auto-merge.
- после merge/release/sync применить Closure policy для RESULT/INDEX: batch перед release по умолчанию, per-task только для исключений из канона.

Финальный отчет:

- корень repository;
- сводка remote;
- базовая ветка;
- рабочая ветка;
- созданные файлы;
- измененные файлы;
- запущенные проверки;
- не запущенные проверки и причина;
- результат sensitive grep без вывода matching lines;
- риски;
- сработавшие STOP-условия;
- результат language policy;
- commit SHA;
- статус push;
- ссылка/номер PR;
- статус PR после review (`PR status after review`);
- work PR status;
- work PR merge commit SHA;
- work PR `merged_at`;
- release PR status/merge commit SHA/`merged_at` или `не применимо`;
- sync PR status/merge commit SHA/`merged_at` или `не применимо`;
- RESULT закрыт после merge;
- INDEX закрыт после merge;
- No journal placeholders;
- результат stale pre-merge status check;
- проверка Closure policy;
- требуется per-task closure: yes/no; если no — указать batch-closure перед release.
- файл результата исполнителя (engine);
- запрос на улучшение methodology repository (`Methodology repository improvement request`), если нужен.
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

Рекомендуемый режим исполнения:

Роль: docs-maintainer
Исполнитель: на усмотрение архитектора
Reasoning effort: высокий
Запуск: Local only
Режим: Agent
Почему: задача меняет reusable methodology repository и должна быть выполнена отдельной веткой и Pull Request.

Цель:

<нейтрально описать улучшение methodology repository без private downstream data>

Repository:

https://github.com/MaximKolomeets/agent-system-development

Разрешенные файлы:

- <methodology files>

Запрещенные данные:

- private downstream names
- private repository URLs
- client data
- customer data
- internal code names
- credentials
- `.env`

Проверки:

BEGIN POWERSHELL
# Проверить diff на запрещенные private/downstream markers.
git grep -I -l -i -E "private repo url|client data|customer data|internal code name" -- docs/agent-system
END POWERSHELL

Финальный отчет:

- краткое описание;
- измененные файлы;
- проверки;
- результат проверки private data;
- результат language policy;
- ссылка/номер PR.
```

## Проверка результата

Укажите команды проверки и ожидаемые признаки успеха. Если команды нужны `engine`, они должны быть продублированы внутри блока для исполнителя (engine).

Проверьте перед отправкой:

- если ответ просит `engine` изменить файлы, есть ли ровно один полный блок для исполнителя (engine) для этой задачи;
- нет ли write-action instructions вне блока для исполнителя (engine);
- были ли PR body update, journal update, commit/push и review follow-up instructions помещены внутрь блока для исполнителя (engine);
- все ли пользовательские заголовки блока для исполнителя (engine) написаны на русском;
- остался ли английский только в технических identifiers, commands, paths, filenames, branch names, config keys, API names, package names, vendor/tool names, SHA values и literal external names.

## Риски и STOP-условия

Кратко перечислите главные риски для пользователя. Execution STOP-условия для `engine` должны оставаться внутри блока для исполнителя (engine).

## Следующий шаг

Укажите один конкретный следующий шаг.
