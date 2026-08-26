#!/usr/bin/env python3
"""Fail-closed validation of a secret-free outbound relay plan."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
from pathlib import Path


HOSTNAME = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")
FORBIDDEN_NAMES = {"docker", "docker-socket", "shell", "ssh", "postgres", "database", "qdrant", "vector-store"}
ACCESS_PROFILES = {"observe", "bounded_operator", "deployment_operator", "custom"}
FORBIDDEN_CAPABILITY_PARTS = {"shell", "docker", "socket", "database", "qdrant", "secret", "credential"}


def validate(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if set(payload) != {"vps_host", "relay_user", "access_profile", "allowed_capabilities", "mappings"}:
        raise ValueError(
            "plan must contain exactly vps_host, relay_user, access_profile, "
            "allowed_capabilities and mappings"
        )
    vps_host = str(payload["vps_host"])
    try:
        ipaddress.ip_address(vps_host)
    except ValueError:
        if not HOSTNAME.fullmatch(vps_host):
            raise ValueError("vps_host must be an IP address or DNS hostname") from None
    if not re.fullmatch(r"[a-z_][a-z0-9_-]{2,31}", str(payload["relay_user"])):
        raise ValueError("relay_user is invalid")
    access_profile = str(payload["access_profile"])
    if access_profile not in ACCESS_PROFILES:
        raise ValueError("access_profile is invalid")
    capabilities = payload["allowed_capabilities"]
    if not isinstance(capabilities, list) or not 1 <= len(capabilities) <= 32:
        raise ValueError("allowed_capabilities count must be in 1..32")
    if len(set(capabilities)) != len(capabilities):
        raise ValueError("allowed_capabilities must be unique")
    for capability in capabilities:
        if not isinstance(capability, str) or not re.fullmatch(r"[a-z][a-z0-9_.:-]{2,63}", capability):
            raise ValueError("capability name is invalid")
        parts = set(re.split(r"[-_.:]", capability.casefold()))
        if parts & FORBIDDEN_CAPABILITY_PARTS:
            raise ValueError("capability exposes a forbidden infrastructure primitive")
    if access_profile == "observe" and any(
        not capability.endswith((".read", ":read", ".list", ":list", ".status", ":status"))
        for capability in capabilities
    ):
        raise ValueError("observe profile accepts only read/list/status capabilities")
    if access_profile == "deployment_operator" and not any("deploy" in capability for capability in capabilities):
        raise ValueError("deployment_operator requires an explicit deploy capability")
    mappings = payload["mappings"]
    if not isinstance(mappings, list) or not 1 <= len(mappings) <= 4:
        raise ValueError("mappings count must be in 1..4")
    remote_ports: set[int] = set()
    hostnames: set[str] = set()
    for row in mappings:
        if not isinstance(row, dict) or set(row) != {
            "name",
            "local_host",
            "local_port",
            "vps_loopback_port",
            "public_hostname",
            "expected_anonymous_status",
        }:
            raise ValueError("mapping fields mismatch")
        name = str(row["name"]).casefold()
        local_host = str(row["local_host"])
        public_hostname = str(row["public_hostname"]).casefold()
        if name in FORBIDDEN_NAMES or any(part in FORBIDDEN_NAMES for part in re.split(r"[-_.]", name)):
            raise ValueError("mapping exposes a forbidden capability")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,31}", name):
            raise ValueError("mapping name is invalid")
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,62}", local_host):
            raise ValueError("local_host must be a Docker/service DNS name")
        local_port = row["local_port"]
        remote_port = row["vps_loopback_port"]
        if any(isinstance(value, bool) or not isinstance(value, int) or not 1024 <= value <= 65535 for value in (local_port, remote_port)):
            raise ValueError("ports must be integers in 1024..65535")
        if remote_port in remote_ports:
            raise ValueError("vps loopback ports must be unique")
        if not HOSTNAME.fullmatch(public_hostname) or public_hostname in hostnames:
            raise ValueError("public hostnames must be valid and unique")
        if row["expected_anonymous_status"] not in {401, 403, 404}:
            raise ValueError("anonymous status must fail closed")
        remote_ports.add(remote_port)
        hostnames.add(public_hostname)
    serialized = json.dumps(payload).casefold()
    if any(marker in serialized for marker in ("password", "private_key", "token", "authorization")):
        raise ValueError("plan must not contain secret fields")
    return {
        "valid": True,
        "access_profile": access_profile,
        "capabilities": len(capabilities),
        "mappings": len(mappings),
        "remote_ports": sorted(remote_ports),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.plan), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
