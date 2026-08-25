# Архитектура outbound relay

```text
external client
  -> HTTPS hostname + edge auth
  -> Caddy on VPS
  -> 127.0.0.1:<remote-port>
  <- SSH -R over one outbound session
  <- hardened tunnel container on target host
  -> allowlisted service in operator network
```

## Trust boundaries

- Target host хранит private tunnel key и application client tokens.
- VPS хранит только public key, host key, Caddy routes и TLS material.
- Tunnel container получает закрытую часть tunnel identity read-only, но не получает backend secrets.
- Caddy не проксирует database, Docker socket, Qdrant/vector store или shell.
- Application auth остаётся вторым слоем после edge auth/TLS.

## Port model

Каждый mapping содержит:

```json
{
  "name": "mcp",
  "local_host": "service-name",
  "local_port": 8200,
  "vps_loopback_port": 28410,
  "public_hostname": "mcp.example.org",
  "expected_anonymous_status": 401
}
```

Remote bind всегда `127.0.0.1`. Порт выбирается заранее и проверяется на VPS
до mutation. Не используй `0.0.0.0`, `GatewayPorts clientspecified` или
динамический SOCKS proxy.

## SSH controls

Минимальный `Match User` профиль:

```text
Match User <relay-user>
    AuthenticationMethods publickey
    PasswordAuthentication no
    KbdInteractiveAuthentication no
    PermitTTY no
    X11Forwarding no
    AllowAgentForwarding no
    AllowTcpForwarding remote
    GatewayPorts no
    PermitListen 127.0.0.1:<port-a> 127.0.0.1:<port-b>
```

Добавь эквивалентные `restrict,port-forwarding,permitlisten="..."` options к
конкретному public key. Проверяй effective settings через:

```text
sshd -T -C user=<relay-user>,host=<vps-host>,addr=<target-public-ip>
```

## Client process

Используй `ssh`/`autossh` с:

- `BatchMode=yes`;
- `StrictHostKeyChecking=yes`;
- отдельным `UserKnownHostsFile`;
- `ExitOnForwardFailure=yes`;
- `ServerAliveInterval` и `ServerAliveCountMax`;
- только фиксированными `-R 127.0.0.1:remote:local:port`;
- `-N`, без remote command.

Закрытая часть identity никогда не передаётся на VPS и не попадает в image layer.
