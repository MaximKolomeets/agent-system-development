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
| Tunnel stop | local services продолжают работать |
| Tunnel restart | external endpoints восстанавливаются |
| Qdrant/database | runtime unchanged |
| Secret output | отсутствует |

Acceptance считается завершённым только при внешнем probe через публичный HTTPS
hostname. Внутренний curl на VPS или target доказывает лишь часть цепочки.
