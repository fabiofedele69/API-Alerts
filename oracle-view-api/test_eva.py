#!/usr/bin/env python3

import requests
from pathlib import Path

PROPERTIES = "/app/M50/dyn/m50-tomcat/acm_repository.properties"


def read_properties(filename):
    props = {}

    with open(filename, "r") as f:
        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            props[key.strip()] = value.strip()

    return props


props = read_properties(PROPERTIES)

vault_address = props["vault.address"].rstrip("/")
vault_path = props["vault.path"].strip("/")

cert = props["vault.ssl.clientCertPem"]
key = props["vault.ssl.clientKeyPem"]

role = (
    props.get("vault.ssl.roleCert")
    or props.get("vault.ssl.role")
)

namespace = props["vault.namespace"]

ca_bundle = str(Path(cert).parent / "cacerts.pem")


print("==========================================")
print("EVA UAT connectivity test")
print("==========================================")

print("Vault address :", vault_address)
print("Vault path    :", vault_path)
print("Namespace     :", namespace)
print("Role          :", role)
print("Certificate   :", cert)
print("Private key   :", key)
print("CA bundle     :", ca_bundle)

print()
print("[1] Authenticating to EVA...")


login_url = f"{vault_address}/v1/auth/cert/login"

response = requests.post(
    login_url,
    headers={
        "X-Vault-Namespace": namespace
    },
    json={
        "name": role
    },
    cert=(cert, key),
    verify=ca_bundle,
    timeout=10
)

print("HTTP status:", response.status_code)

response.raise_for_status()

login_data = response.json()

token = login_data["auth"]["client_token"]

print("EVA authentication: SUCCESS")
print("Token received: YES (not displayed)")


print()
print("[2] Retrieving configured secret...")


secret_url = f"{vault_address}/v1/{vault_path}"

response = requests.get(
    secret_url,
    headers={
        "X-Vault-Namespace": namespace,
        "X-Vault-Token": token
    },
    cert=(cert, key),
    verify=ca_bundle,
    timeout=10
)

print("HTTP status:", response.status_code)

response.raise_for_status()

result = response.json()

secret = result.get("data", {})

# KV version 2
if (
    isinstance(secret, dict)
    and isinstance(secret.get("data"), dict)
):
    secret = secret["data"]


print("Secret retrieval: SUCCESS")

print()
print("Available secret fields:")

for field in secret.keys():

    # NEVER display secret values
    print("  -", field)


print()
print("==========================================")
print("TEST COMPLETED")
print("No secret/password values were displayed.")
print("==========================================")
