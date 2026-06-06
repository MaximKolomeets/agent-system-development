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

## Forbidden in public repository

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
- материалы `CORP_KNOWLEDGE_PLATFORM`, если они содержат внутреннюю архитектуру или данные.

## Private corporate repositories

`CORP_KNOWLEDGE_PLATFORM` должен оставаться private.

Для private repository на GitHub Free часть rulesets/branch protection может быть ограничена.

Возможные варианты:

1. Ручной workflow + review.
2. GitHub Pro.
3. GitHub Team/Organization.
4. Отдельный public шаблон без корпоративных данных.

## Before making any repository public

- Выполнить `git status --short`.
- Выполнить `git grep -n -i "token\|password\|secret\|api_key\|apikey\|credential\|пароль\|токен"`.
- Проверить, что найденные совпадения являются только документационными правилами, без реальных значений.
- Проверить отсутствие `.env`, `.venv`, `data/`, `runtime/`, `dist/`, `backups/`, `exports/`.
- Проверить историю commits, если ранее могли попадать секреты.
- Если секрет когда-либо был в истории, не просто удалить файл, а считать секрет скомпрометированным и ротировать его.
