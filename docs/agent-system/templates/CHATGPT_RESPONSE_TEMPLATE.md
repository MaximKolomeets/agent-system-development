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

Methodology repository:

https://github.com/MaximKolomeets/agent-system-development

Обязательная проверка актуального agent-system-development:

- перед применением методологии проверить актуальную версию methodology repository;
- если используется локальная копия, выполнить fetch/pull fast-forward при чистом working tree;
- если актуальность проверить невозможно, явно указать это в final report.

Base branch:

<base branch>

Working branch:

work/<role>/<task>

Allowed files:

- <allowed path>

Forbidden files and changes:

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
- commit SHA;
- push status;
- PR link/number;
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

Allowed files:

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
git grep -I -n -i -E "private repo url|client data|customer data|internal code name" -- docs/agent-system
END POWERSHELL

Final report:

- summary;
- changed files;
- checks;
- private data check result;
- PR link/number.
```

## Проверка результата

Укажите команды проверки и ожидаемые признаки успеха. Если команды нужны `engine`, они должны быть продублированы внутри Engine-блока.

## Риски и STOP-условия

Кратко перечислите главные риски для пользователя. Execution STOP-условия для `engine` должны оставаться внутри Engine-блока.

## Следующий шаг

Укажите один конкретный следующий шаг.
