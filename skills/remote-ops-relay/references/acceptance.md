# Acceptance matrix

| Gate | Ожидаемый результат |
|---|---|
| Local service health | healthy до и после tunnel |
| Tunnel container | non-root, read-only, cap-drop ALL, no-new-privileges |
| Host ports | 0 |
| Docker socket/backend secrets | отсутствуют |
| VPS remote listeners | только `127.0.0.1` |
| MCP anonymous | 401 |
| Admin anonymous | 401 или edge denial |
| Admin authorized | 200 |
| Observer list/read | только allowlisted tools/data |
| Observer operate | 403 + audit |
| Selected access profile | только заявленные capabilities |
| Adjacent denied capability | 403 + client-scoped audit |
| Credential isolation | отдельная identity на профиль и проект |
| Tunnel stop | local services продолжают работать |
| Tunnel restart | external endpoints восстанавливаются |
| Qdrant/database | runtime unchanged |
| Secret output | отсутствует |

Acceptance считается завершённым только при внешнем probe через публичный HTTPS
hostname. Внутренний curl на VPS или target доказывает лишь часть цепочки.

Для `bounded_operator` и `deployment_operator` добавь повтор одного request с
тем же idempotency key: side effect не должен выполняться второй раз. Для
`deployment_operator` также обязательны digest mismatch denial и rollback
только собственного сервиса.
