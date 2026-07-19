from pathlib import Path
from typing import Dict


RCM_PROPERTIES_FILE = Path(
    "/app/M50/dyn/m50-tomcat/acm_repository.properties"
)


class EvaConfigurationError(RuntimeError):
    """Raised when the EVA/RCM runtime configuration is invalid."""


def _read_properties_file(path: Path) -> Dict[str, str]:
    """
    Read a Java-style .properties file.

    Empty lines and lines beginning with # or ! are ignored.
    """

    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    properties: Dict[str, str] = {}

    with path.open("r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()

            if not line or line.startswith("#") or line.startswith("!"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            properties[key.strip()] = value.strip()

    return properties


def read_eva_config() -> Dict[str, str]:
    """
    Read the EVA configuration used by the running RCM application.

    No token or password is read or stored here.
    """

    properties = _read_properties_file(RCM_PROPERTIES_FILE)

    required_properties = {
        "vault.address": "Vault address",
        "vault.path": "Vault secret path",
        "vault.ssl.clientCertPem": "client certificate",
        "vault.ssl.clientKeyPem": "client private key",
        "vault.ssl.roleCert": "Vault certificate role",
        "vault.namespace": "Vault namespace",
    }

    missing = [
        property_name
        for property_name in required_properties
        if not properties.get(property_name)
    ]

    if missing:
        raise EvaConfigurationError(
            "Missing required properties in "
            f"{RCM_PROPERTIES_FILE}: {', '.join(missing)}"
        )

    vault_address = properties["vault.address"].rstrip("/")
    vault_path = properties["vault.path"].lstrip("/")

    return {
        "cert": properties["vault.ssl.clientCertPem"],
        "key": properties["vault.ssl.clientKeyPem"],
        "namespace": properties["vault.namespace"],
        "role": properties["vault.ssl.roleCert"],
        "login_url": f"{vault_address}/v1/auth/cert/login",
        "secret_url": f"{vault_address}/v1/{vault_path}",
    }
