---
name: remote-ops-relay # Идентификатор skill.
description: Развернуть или восстановить безопасный исходящий reverse SSH tunnel от Docker-сервиса за NAT к промежуточному VPS и опубликовать только allowlisted HTTP endpoints через HTTPS. Использовать для удалённого MCP/admin-доступа без inbound-портов, shell proxy, Docker socket или публикации backend-сервисов.
---

# Outbound VPS relay

Цель — дать внешнему клиенту доступ только к явно названным HTTP endpoints,
сохранив target host закрытым для входящих соединений.

## Выбор режима

- До проектирования transport выбери профиль прикладного доступа по
  [references/access-profiles.md](references/access-profiles.md). Relay не
  превращает read-only token в operator token и не заменяет авторизацию самого
  приложения.
- Для нового relay сначала прочитай [references/architecture.md](references/architecture.md), затем [references/runbook.md](references/runbook.md).
- Для диагностики существующего relay прочитай раздел recovery в [references/runbook.md](references/runbook.md); не переустанавливай контур до сбора evidence.
- Перед production acceptance прочитай [references/acceptance.md](references/acceptance.md).

## Обязательный workflow

1. Зафиксируй target repository, issue, владельца trust boundary, выбранный
   `access_profile`, разрешённые прикладные capabilities и список endpoint
   mappings. Не принимай произвольные URL/commands.
2. Создай plan JSON без секретов и проверь его `scripts/validate_relay_plan.py`.
3. На target host сгенерируй отдельную Ed25519 identity. Закрытая часть остаётся только на target host; на VPS передаётся только `.pub`.
4. Получи VPS host key через независимый канал и попроси человека подтвердить fingerprint до записи `known_hosts`.
5. Перед изменением VPS сохрани точечные backups sshd/Caddy. Нужна явная authority на root-изменения VPS.
6. Создай отдельного relay-user. Ограничь его одновременно в `authorized_keys` и `Match User`: только public-key auth, remote forwarding, точные `PermitListen`, без TTY/X11/agent forwarding.
7. Убедись, что глобальный `AllowUsers` не исключает relay-user. Не заменяй существующий список; добавляй с сохранением других principals.
8. Слушай reverse ports только на `127.0.0.1` VPS. Caddy публикует отдельные HTTPS hostnames и проксирует только эти loopback ports.
9. На target host запусти отдельный non-root/read-only transport container только в operator network. Не монтируй Docker socket, backend credentials и host ports.
10. Healthcheck должен доказывать живую SSH-сессию/control master, а не только наличие процесса.
11. Выполни полный acceptance, включая negative probe для каждой capability вне
    выбранного профиля, и зафиксируй image digest, fingerprints, mappings,
    application scopes, audit checks и rollback без secret values.

Для нового deployment скопируй [assets/template](assets/template) в target
repository. Шаблон воспроизводит проверенный двухканальный transport contour и
оставляет project-specific только hostnames, ports, service DNS names, network,
image digest и secret paths. Не переписывай tunnel entrypoint с нуля.

## Human gates

Остановись и запроси действие человека только для:

- независимого подтверждения VPS fingerprint;
- root/DNS/Caddy/sshd mutation;
- установки public key;
- выдачи или ротации client credentials;
- повышения профиля доступа или расширения allowlist capabilities;
- решения о публикации нового endpoint.

Не проси вставлять закрытую часть identity, access marker или пароль в чат/Issue/log.

## Fail-closed условия

- fingerprint не совпал;
- requested remote port не loopback или конфликтует;
- endpoint пытается открыть shell, Docker API, database, vector store или произвольный upstream;
- `sshd -t`, `sshd -T -C`, `caddy validate` или внешний auth probe не прошли;
- relay-user попал под `AllowUsers`/Fail2ban и причина не устранена;
- tunnel health не проверяет SSH-сессию;
- rollback не определён.

Не отключай host-key checking, TLS verification, Fail2ban или auth ради прохождения проверки.

## Результат

Верни:

- схему mappings без внутренних секретов;
- расположение private/public key и token references, но не значения;
- точные версии/digests;
- результат `401/403/200`, audit, reconnect и local independence;
- оставшиеся риски и следующий bounded step.
