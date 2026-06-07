# ENGINE_SELF_DISCOVERY_CONTRACT

## Назначение

Этот контракт описывает минимальный self-discovery, который `engine` обязан выполнить в target repository до любых изменений.

Цель self-discovery - подтвердить, что `engine` находится в правильном repository, понимает локальные инструкции, видит состояние working tree и не начинает bootstrap при риске повреждения данных или раскрытия секретов.

## Обязательные команды

В target repository выполнить:

```bash
git rev-parse --show-toplevel
```

```bash
git remote -v
```

```bash
git branch --show-current
```

```bash
git status --short
```

```bash
git ls-files
```

Команды должны использоваться для audit и safety gate. Они не дают разрешения автоматически менять файлы.

## Local instructions discovery

`engine` должен прочитать локальные документы target repository, если они существуют:

- `AGENTS.md`;
- `README.md`;
- `AI_SYSTEM_ARCHITECTURE.md`;
- `PROJECT_DASHBOARD.md`;
- `ROADMAP.md`;
- `DECISIONS.md`;
- `RUNBOOK.md`;
- `docs/agent-system/*`.

Если файл отсутствует, это фиксируется как observation, а не как ошибка.

## Forbidden tracked paths check

`engine` должен проверить tracked files на запрещенные пути. Минимальный список:

- `.env`;
- `.env.*`, кроме безопасного `.env.example`;
- `.venv/`;
- `data/`;
- `runtime/`;
- `dist/`;
- `backups/`;
- `exports/`;
- `*.log`;
- `*.tmp`;
- `*.bak`.

Если запрещенный путь уже tracked, `engine` должен остановиться до решения пользователя.

## Sensitive grep

Sensitive grep выполняется только в filename-only режиме:

```bash
git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" --
```

Matching lines нельзя печатать:

- в terminal output;
- в engine logs;
- в final report;
- в документации public methodology repository.

Если команда вернула файлы, `engine` должен сообщить только факт наличия filename-only matches и количество или список имен файлов, если это безопасно для контекста. Реальные значения секретов не печатать.

## Stop conditions

`engine` должен написать `STOP` и не менять файлы, если:

- working tree не чистый и нет явного разрешения работать с текущими изменениями;
- remote не соответствует задаче;
- текущий repository не является target repository;
- есть forbidden tracked paths;
- есть риск секретов;
- локальные инструкции запрещают требуемое действие;
- нет разрешения пользователя на изменение файлов;
- задача требует доступа к private data, которые нельзя переносить в public methodology repository.

## Результат self-discovery

Результат self-discovery должен быть кратким audit-блоком:

- repository root;
- remote summary;
- current branch;
- working tree status;
- local instructions found;
- template documents found;
- forbidden tracked paths result;
- sensitive grep result без matching lines;
- stop conditions, если есть;
- recommended next step.

Если stop conditions отсутствуют, следующим шагом все равно должен быть adoption audit, а не полный перенос файлов.
