# Runbook и recovery

## Preflight

1. Подтверди, что target services healthy локально.
2. Зафиксируй их internal endpoints и operator network.
3. Проверь VPS TCP/22 и TCP/443 отдельно с host и из tunnel network.
4. Проверь свободные loopback ports на VPS.
5. Сохрани SHA-256 deployment package и image digest.

## VPS mutation

1. Создай restricted system user с отдельным home для `.ssh`.
2. Установи только public key; directory `0700`, `authorized_keys` `0600`.
3. Добавь отдельный sshd include и проверь `sshd -t`.
4. Проверь effective `AllowUsers`, `AllowTcpForwarding`, `PermitListen`, `PermitTTY`.
5. Добавь отдельный Caddy include. Файл должен быть читаем Caddy: caller `umask 077` не должен случайно оставить include `0600 root:root`.
6. Выполни `caddy validate`, затем graceful reload. При ошибке верни backup.

## Target deployment

- Windows Docker Desktop: PowerShell 7 предпочтителен; owner scripts должны также проходить Windows PowerShell 5.1.
- Не передавай пустой `ssh-keygen -N` через вложенный shell quoting. Используй native executable arguments или фиксированный container entrypoint.
- Native stderr в PowerShell 5.1 захватывай так, чтобы warning не обрывал сбор `$LASTEXITCODE` и diagnostics.
- Compose overlay должен подключать transport container только к существующей operator network.
- Не используй `--remove-orphans`, `down -v`, prune или Docker commit.

## Recovery decision tree

### TCP/22 недоступен

- Сначала проверь Fail2ban/nftables и наличие listener.
- Не отключай Fail2ban глобально. Сними только подтверждённый ban target IP и выясни причину повторных auth failures.

### `Permission denied (publickey)`

- Проверь exact relay-user, public key fingerprint, ownership/modes и effective `AllowUsers`.
- Не пробуй root key как tunnel key и не копируй private admin key в container.

### Tunnel process жив, endpoint недоступен

- Проверь реальную SSH session/control socket и VPS loopback listener.
- Health, основанный только на PID, является ложноположительным.

### Caddy validate успешен, reload неуспешен

- Проверь права include/certificate directories и journal Caddy.
- Восстанови предыдущий include; не перезапускай вслепую весь VPS.

## Rollback

Останови только tunnel container, удали только новый Caddy include и новый sshd
include/public key после validate/reload. Не удаляй общие users, certificates,
networks и firewall rules без отдельного подтверждения владельца.
