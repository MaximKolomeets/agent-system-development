# Профили прикладного доступа

Reverse SSH relay отвечает только за transport. Реальные права всегда задаёт
upstream-приложение отдельной identity и проверяет на каждом tool/API вызове.
Один token не переиспользуется между профилями или проектами.

## Выбор профиля

| Профиль | Разрешено | Запрещено по умолчанию | Когда применять |
|---|---|---|---|
| `observe` | health, inventory, allowlisted reports, audit чтение | mutation, rollout, deploy, secrets, RAW content | диагностика и независимая проверка |
| `bounded_operator` | `observe` плюс явно перечисленные идемпотентные бизнес-операции с лимитами и audit | shell, Docker API/socket, database/vector credentials, arbitrary URL/command, production alias | автономный bounded rollout или повторяемая операция |
| `deployment_operator` | проверенный deployment API для подписанного/digest-pinned release, status и rollback только данного сервиса | interactive shell, unrestricted Compose/Docker, host filesystem, secret readback | только когда у приложения существует узкий deploy control plane |
| `custom` | минимальный явный allowlist | всё, чего нет в allowlist | нестандартный проект после threat review |

`deployment_operator` нельзя имитировать передачей SSH shell или Docker socket.
Если узкого deployment API нет, deployment остаётся human gate до его реализации.

## Контракт identity

Для каждой identity зафиксируй без значений credentials:

```json
{
  "client_id": "automation-observer",
  "access_profile": "observe",
  "allowed_capabilities": ["inventory.read", "quality-report.read"],
  "denied_capabilities": ["rollout.start", "release.deploy"],
  "credential_reference": "restricted local secret file",
  "audit_actor": "automation-observer",
  "expires_or_rotates": "project policy"
}
```

Для `bounded_operator` каждая mutation должна иметь одновременно:

- точный resource/source boundary;
- bounded batch/rate/size;
- idempotency key или durable request identity;
- preflight и fail-closed quality gate;
- immutable audit с client ID и результатом;
- отдельный read tool для статуса/диагностики;
- запрет необратимого production promotion без отдельного human gate.

## Повышение и понижение прав

1. Создай новую identity; не меняй scope уже установленного observer token.
2. Проверь allowlisted positive operation на fixture/dry-run.
3. Проверь минимум одну соседнюю запрещённую capability: ожидается `403` и audit.
4. Проверь, что `tools/list` либо фильтруется, либо каждый лишний tool отклоняется сервером.
5. После завершения временной работы отзови/ротируй новую identity; observer остаётся независимым.

Никогда не проси пользователя вставлять token в Issue, chat, command history или
deployment package. Допускается hidden prompt или restricted secret file с
проверкой прав и выводом только boolean evidence.
