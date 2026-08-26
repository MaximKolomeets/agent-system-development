#!/bin/sh
set -eu

control_path=/tmp/relay-control
kill -0 1
test -S "$control_path"
ssh -S "$control_path" -O check -p "$RELAY_SSH_PORT" \
    "${RELAY_SSH_USER}@${RELAY_SSH_HOST}" >/dev/null 2>&1
nc -z -w 3 "$RELAY_LOCAL_HOST_A" "$RELAY_LOCAL_PORT_A"
nc -z -w 3 "$RELAY_LOCAL_HOST_B" "$RELAY_LOCAL_PORT_B"
