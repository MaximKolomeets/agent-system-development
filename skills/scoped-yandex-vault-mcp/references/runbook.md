# Runbook развёртывания

## Secret files

Создай вне repository:

```text
<secrets-root>/yandex-username.txt
<secrets-root>/yandex-app-password.txt
<secrets-root>/vault-mcp-clients.json
```

JSON содержит только client id, token и permissions. Генерируй tokens CSPRNG,
минимум 32 bytes entropy. Проверяй existence/non-empty/ACL без печати значений.

## Compose invariants

- один service на один Vault root;
- three Docker secrets, никаких secret values в environment;
- `expose`, не `ports`, если нет отдельного authenticated gateway;
- internal backend и egress network;
- запуск без root с read-only/cap-drop/no-new-privileges;
- bounded request/file/search limits;
- log rotation;
- health endpoint проверяет process/config, но не выполняет частый WebDAV write.

## WebDAV preflight

Из того же image/network выполни один authenticated `PROPFIND Depth: 0` точного
project root. Ожидается HTTP 207. HTTP 401 обычно означает неверный exact login
или app password; label пароля не является login. HTTP 404/409 означает неверный
root или отсутствующий parent.

Не выводи Authorization header и response body с document names.

## Известные provider/runtime ловушки

- WebDAV COPY для history может вернуть 409. Надёжнее GET source и conditional PUT history object.
- Internal history writer не должен проходить external `_history` deny path; используй отдельный internal method, не backdoor/tool.
- Streamable HTTP middleware, буферизующее ASGI request, должно отдать body ровно один раз, затем `http.disconnect`. Повторная выдача одного body вызывает CPU spin.
- Python/MCP dependency versions pin в requirements и image; предупреждения settings/forward references не маскируют failed acceptance.
- WebDAV latency не лечится безлимитным mirror. Сначала измерь, затем введи bounded cache.

## Update

Перед config/source change сохрани checksum-matched backup. Собери новый image
с новым immutable tag/digest, пройди offline tests, затем force-recreate только
Vault MCP. Не используй Docker commit как backup.

## Backup/restore

- canonical Vault уже remote, но нужен независимый export/snapshot;
- history на том же account не считается backup;
- храни compose/config/migrations/docs в Git;
- secrets backup отдельно в approved secret manager;
- выполняй restore drill в другую test folder и проверяй checksums/ETags.
