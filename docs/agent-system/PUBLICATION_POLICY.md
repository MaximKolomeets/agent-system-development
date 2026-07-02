# PUBLICATION_POLICY

## Public repository

`agent-system-development` может быть public repository.

Разрешено хранить:

- методологию;
- шаблоны;
- role model;
- branch workflow;
- review checklists;
- обезличенные инструкции;
- Source index/snapshot без секретов.

## Запрещено в public repository

Запрещено хранить:

- `.env`;
- реальные tokens;
- реальные passwords;
- реальные API keys;
- private credentials;
- клиентские данные;
- персональные данные;
- внутренние коммерческие данные;
- дампы баз;
- рабочие директории `data/`, `runtime/`, `dist/`, `backups/`, `exports/`;
- приватные логи;
- материалы private downstream repository, если они содержат внутреннюю архитектуру или данные.

## Private implementation repositories

Private downstream repository должен рассматриваться как отдельный private implementation repository.

Для private repository на GitHub Free часть rulesets/branch protection может быть ограничена.

Возможные варианты:

1. Ручной workflow + review.
2. GitHub Pro.
3. GitHub Team/Organization.
4. Отдельный public шаблон без корпоративных данных.

## Без названий внешних проектов

- Не упоминать конкретные внешние проекты.
- Не упоминать клиентские проекты.
- Не упоминать приватные downstream repositories по имени.
- Не упоминать внутренние кодовые имена.
- Для примеров использовать только нейтральные обозначения:
  - `target implementation repository`;
  - `private downstream repository`;
  - `private implementation repository`;
  - `example project`.

## Перед публикацией repository

- Выполнить `git status --short`.
- Выполнить filename-only scan:
  `git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" -- .`.
- Выполнить count-only scan:
  `git grep -I -l -i -E "token|password|secret|api_key|apikey|credential|пароль|токен" -- . | wc -l`.
- Проверить, что найденные filenames относятся только к документационным правилам,
  без реальных значений.
- Не печатать matching lines, values, headers, cookies или credentials в terminal,
  logs, journal, PR body или final report.
- Проверить отсутствие `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Проверить историю commits, если ранее могли попадать секреты.
- Если секрет когда-либо был в истории, не просто удалить файл, а считать секрет скомпрометированным и ротировать его.
