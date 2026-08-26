---
name: scoped-yandex-vault-mcp # Идентификатор skill.
description: Спроектировать, развернуть или проверить Docker MCP для канонического Markdown Vault, ограниченного одной папкой Яндекс.Диска через WebDAV. Использовать для нового project trust boundary, client scopes, optimistic writes, history и hardening; не использовать как RAW archive или массовое файловое зеркало.
---

# Scoped Yandex Vault MCP

Цель — один deployment на один project Vault root, с раздельными storage и MCP
credentials и без доступа клиента к соседним папкам через MCP.

## Сначала выбери реальную границу

Пароль приложения Яндекса ограничен сервисом Диск, но не отдельной папкой.

- Если достаточно application boundary, используй отдельный app password и жёсткий `WEBDAV_ROOT_PATH` в MCP.
- Если нужен provider-enforced boundary, создай отдельный Яндекс-аккаунт и дай ему доступ только к project folder. Это предпочтительный вариант для разных клиентов/trust boundaries.

Не утверждай, что app password сам ограничивает папку.

## Маршрутизация

- Для архитектуры и разделения RAW/Vault прочитай [references/architecture.md](references/architecture.md).
- Для развёртывания прочитай [references/runbook.md](references/runbook.md).
- Для диагностики WebDAV/ETag/history и acceptance прочитай [references/acceptance.md](references/acceptance.md).
- Перед mutation создай secret-free plan JSON и проверь его `scripts/validate_vault_plan.py`.

## Обязательный workflow

1. Зафиксируй project slug, точный WebDAV root и структуру Vault. Не принимай account root `/`.
2. Создай отдельный app password с нейтральным project label. Запроси exact account login, а не label пароля; значения сохраняются в restricted secret files и не печатаются.
3. Создай уникальный MCP token на каждого caller. Минимальные роли: writer и read-only/audit. Не переиспользуй tokens между проектами.
4. Запусти один generic image с project-specific env/secrets. Pin base/runtime image digest.
5. Раздели сети: internal Vault backend для клиентов и non-internal storage-egress только для Vault MCP. Не подключай обычных агентов к storage-egress.
6. Контейнер: non-root, read-only root, `cap_drop: ALL`, `no-new-privileges`, bounded tmpfs, no published port по умолчанию.
7. Нормализуй каждый относительный path. Запрещай absolute path, `..`, пустые segments, encoded traversal и внешний доступ к `_history`.
8. Запись существующего файла требует `expected_etag` или `modified_at`; create использует `If-None-Match: *`. После PUT выполняй read-after-write hash verification.
9. Перед replace/append/move сохраняй immutable history через GET + conditional PUT. Не полагайся на WebDAV COPY: провайдер может вернуть 409/unsupported.
10. Не регистрируй delete tool. Внешний MCP никогда не пишет непосредственно в `_history`.
11. Выполни offline tests, WebDAV 207 preflight, затем MCP E2E. Зафиксируй safe evidence без URL query, paths документов, tokens и содержимого.

Для нового deployment скопируй [assets/template](assets/template) в target
repository и меняй только generic configuration/secrets references. Не переписывай
server с нуля. Сначала запусти его offline tests; затем добавляй target-specific
Compose overlay и immutable image tag.

## Диск и производительность

- Полное зеркало выключено по умолчанию.
- Для обычного Vault читай файл по запросу; разрешён bounded metadata/content cache с TTL и жёстким byte limit только после измерения latency.
- Не используй Vault MCP для RAW. Ingestor складывает RAW в bounded local spool, объединяет мелкие файлы в архив/пакет, отправляет ограниченным числом WebDAV requests и сохраняет receipt/checksum.
- Qdrant и PostgreSQL не заменяют canonical Markdown; MCP не индексирует документы сам.

## Fail-closed условия

- WebDAV project-root `PROPFIND` не возвращает 207;
- exact login/app password не подтверждены;
- root пустой, `/`, содержит traversal или равен account root;
- secret file доступен непривилегированным principals;
- anonymous MCP не 401 или read-only caller может писать;
- history доступна извне;
- один request вызывает CPU spin или повторную выдачу ASGI body;
- тест предлагает отключить TLS verification, path check или auth.

При ошибке WebDAV не повторяй mutation бесконечно. Прекрати после bounded retry,
сохрани correlation id и safe upstream status.

## Результат

Верни image digest, container/network names, secret references, WebDAV root,
список MCP tools/scopes, hardening evidence, E2E markers, backup/restore status и
остаточный риск provider-level доступа app password. Никогда не возвращай сами
credentials или полный документ.
