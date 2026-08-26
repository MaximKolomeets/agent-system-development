#!/bin/sh
set -eu

if [ "$#" -ne 1 ] || [ "$1" != "/out/id_ed25519" ]; then
    printf '%s\n' 'usage: generate-key.sh /out/id_ed25519' >&2
    exit 64
fi
if [ -e "$1" ] || [ -e "$1.pub" ]; then
    printf '%s\n' 'refusing to overwrite an existing key pair' >&2
    exit 73
fi

umask 077
ssh-keygen -q -t ed25519 -N '' -C project-ops-relay -f "$1"
test -s "$1"
test -s "$1.pub"
