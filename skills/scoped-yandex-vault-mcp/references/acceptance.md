# Acceptance

## Offline

- config rejects empty/root/traversal path;
- Unicode path round-trip;
- external `_history` denied;
- absolute and encoded traversal denied;
- клиентские tokens уникальны, имеют минимальную длину и allowlisted permissions;
- request/file/search bounds enforced;
- logs redact tokens and content;
- receive middleware завершается без CPU spin.

## WebDAV

1. Root `PROPFIND Depth: 0` = 207.
2. Создание тестового Markdown с `If-None-Match: *` успешно.
3. Stat/read возвращает ETag и тот же content hash.
4. Replace с верным ETag успешен; устаревший ETag возвращает conflict.
5. Операции append и move успешны.
6. Предыдущие версии существуют во внутренней history.
7. Внешние попытки traversal/absolute/other-root/`_history` отклонены.

## MCP/auth

| Проверка | Ожидается |
|---|---|
| no token | 401 |
| unknown token | 401 |
| writer create/replace/append/move | success |
| reader read/search/stat | success |
| reader write | 403 |
| delete tool | absent |
| published host ports | 0 по умолчанию |
| container hardening | all true |

Удаление тестовых файлов через недоступный delete tool запрещено. Используй
явно одобренную ручную cleanup-операцию в WebDAV UI либо оставь `_mcp_test` как
review evidence и задокументируй retention.
