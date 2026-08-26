#!/bin/sh
set -eu

require_value() {
    name="$1"
    eval "value=\${$name:-}"
    if [ -z "$value" ]; then
        printf '%s\n' "required setting is missing: $name" >&2
        exit 64
    fi
}

require_port() {
    name="$1"
    minimum="$2"
    eval "value=\${$name:-}"
    case "$value" in ''|*[!0-9]*) printf '%s\n' "invalid port: $name" >&2; exit 64;; esac
    if [ "$value" -lt "$minimum" ] || [ "$value" -gt 65535 ]; then
        printf '%s\n' "port is outside the allowed range: $name" >&2
        exit 64
    fi
}

for name in RELAY_SSH_HOST RELAY_SSH_USER RELAY_LOCAL_HOST_A RELAY_LOCAL_HOST_B; do
    require_value "$name"
done
require_port RELAY_SSH_PORT 1
require_port RELAY_LOCAL_PORT_A 1
require_port RELAY_LOCAL_PORT_B 1
require_port RELAY_REMOTE_PORT_A 1024
require_port RELAY_REMOTE_PORT_B 1024
for value in "$RELAY_SSH_HOST" "$RELAY_LOCAL_HOST_A" "$RELAY_LOCAL_HOST_B"; do
    case "$value" in ''|*[!A-Za-z0-9.-]*|.*|*.) printf '%s\n' 'invalid host setting' >&2; exit 64;; esac
done
case "$RELAY_SSH_USER" in ''|*[!A-Za-z0-9_-]*) printf '%s\n' 'invalid relay user' >&2; exit 64;; esac
if [ "$RELAY_REMOTE_PORT_A" = "$RELAY_REMOTE_PORT_B" ]; then
    printf '%s\n' 'remote ports must differ' >&2
    exit 64
fi

key_source=/run/secrets/relay_ssh_key
known_hosts=/run/secrets/relay_known_hosts
key_runtime=/tmp/relay-identity
control_path=/tmp/relay-control
for path in "$key_source" "$known_hosts"; do
    test -s "$path" || { printf '%s\n' 'required relay secret is missing' >&2; exit 66; }
done

umask 077
cp "$key_source" "$key_runtime"
chmod 0600 "$key_runtime"

export AUTOSSH_GATETIME=0 AUTOSSH_POLL=30 AUTOSSH_LOGLEVEL=0
exec autossh -M 0 -NT \
    -o BatchMode=yes -o ConnectTimeout=10 \
    -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -o ExitOnForwardFailure=yes \
    -o ControlMaster=yes -o ControlPath="$control_path" -o ControlPersist=no \
    -o IdentitiesOnly=yes -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no \
    -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$known_hosts" -o LogLevel=ERROR \
    -i "$key_runtime" -p "$RELAY_SSH_PORT" \
    -R "127.0.0.1:${RELAY_REMOTE_PORT_A}:${RELAY_LOCAL_HOST_A}:${RELAY_LOCAL_PORT_A}" \
    -R "127.0.0.1:${RELAY_REMOTE_PORT_B}:${RELAY_LOCAL_HOST_B}:${RELAY_LOCAL_PORT_B}" \
    "${RELAY_SSH_USER}@${RELAY_SSH_HOST}"
