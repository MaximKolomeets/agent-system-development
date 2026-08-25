# Архитектура project-scoped Vault

```text
writer / read-only clients
  -> internal vault_backend
  -> scoped Vault MCP
  -> storage_egress
  -> Yandex WebDAV /<project-root>/vault
```

## Source of truth

| Слой | Назначение |
|---|---|
| Vault/Git | канонический долговечный non-RAW Markdown |
| RAW archive | исходные HTML/PDF/audio/events; отдельный lifecycle |
| PostgreSQL | structured state, ACL, provenance, audit |
| Qdrant | производный semantic index |
| Runtime copy/cache | ограниченная восстанавливаемая копия |

Vault содержит decisions, runbooks, skills, handoffs, role files и project
knowledge. Runtime containers хранят только рабочие копии.

## Folder boundary

Все WebDAV URL строятся как `base_url + encoded(root_segments + relative_segments)`.
Проверка выполняется до HTTP request. Нельзя использовать string-prefix check
после URL decoding; сначала нормализуй Unicode/path segments, отклони absolute,
dot segments и reserved `_history`.

Provider credential остаётся способным обращаться ко всему Диску аккаунта.
Отдельный аккаунт/shared folder нужен, если компрометация container process не
должна открывать соседние папки.

## API contract

Рекомендуемый минимальный набор:

- list/tree/stat/read/read_many;
- find/search_text/changed_since;
- write create/replace;
- append/mkdir/move;
- delete отсутствует.

Writer и reader получают разные bearer tokens. `tools/list` желательно
фильтровать по caller scope; в любом случае `tools/call` проверяется сервером.

## History

History размещается внутри project root в `_history/<logical-path>/<timestamp>-<name>`.
External path policy всегда запрещает `_history`; internal backup routine имеет
отдельный проверяемый флаг/call path. История на том же Диске не является
независимым backup.
