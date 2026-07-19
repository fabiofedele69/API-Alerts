import json
import ssl
import urllib.error
import urllib.request
from typing import Any, Dict

from app.eva import read_eva_config


class VaultAuthenticationError(RuntimeError):
    """Raised when authentication to EVA Vault fails."""


def _read_json_response(response: Any) -> Dict[str, Any]:
    raw_body = response.read().decode("utf-8")

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise VaultAuthenticationError(
            "EVA returned a response that is not valid JSON"
        ) from exc


def get_vault_token() -> str:
    """
    Authenticate to EVA Vault using the configured client certificate.

    The token is returned in memory and is not written to disk or logged.
    """

    config = read_eva_config()

    ssl_context = ssl.create_default_context()
    ssl_context.load_cert_chain(
        certfile=config["cert"],
        keyfile=config["key"],
    )

    request_body = json.dumps(
        {"name": config["role"]}
    ).encode("utf-8")

    request = urllib.request.Request(
        url=config["login_url"],
        data=request_body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Vault-Namespace": config["namespace"],
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            context=ssl_context,
            timeout=30,
        ) as response:
            response_data = _read_json_response(response)

    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")

        raise VaultAuthenticationError(
            f"EVA authentication failed with HTTP status {exc.code}: "
            f"{error_body[:300]}"
        ) from exc

    except urllib.error.URLError as exc:
        raise VaultAuthenticationError(
            f"Unable to connect to EVA: {exc.reason}"
        ) from exc

    except (ssl.SSLError, OSError) as exc:
        raise VaultAuthenticationError(
            f"EVA TLS/client-certificate error: {exc}"
        ) from exc

    token = (
        response_data.get("auth", {}).get("client_token")
        or response_data.get("client_token")
    )

    if not token:
        raise VaultAuthenticationError(
            "EVA authentication succeeded, but no client token "
            "was found in the JSON response"
        )

    return token

def get_oracle_password() -> str:
    """
    Retrieve the Oracle password from EVA Vault.

    The password is returned in memory and is never logged or written to disk.
    """

    config = read_eva_config()
    token = get_vault_token()

    ca_bundle = "/app/M50/dyn/npa/certs/FA23303/cacerts.pem"

    ssl_context = ssl.create_default_context(cafile=ca_bundle)
    ssl_context.load_cert_chain(
        certfile=config["cert"],
        keyfile=config["key"],
    )

    request = urllib.request.Request(
        url=config["secret_url"],
        method="GET",
        headers={
            "Accept": "application/json",
            "X-Vault-Token": token,
            "X-Vault-Namespace": config["namespace"],
        },
    )

    try:
        with urllib.request.urlopen(
            request,
            context=ssl_context,
            timeout=30,
        ) as response:
            response_data = _read_json_response(response)

    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")

        raise VaultAuthenticationError(
            f"EVA secret retrieval failed with HTTP status {exc.code}: "
            f"{error_body[:300]}"
        ) from exc

    except urllib.error.URLError as exc:
        raise VaultAuthenticationError(
            f"Unable to retrieve the EVA secret: {exc.reason}"
        ) from exc

    except (ssl.SSLError, OSError) as exc:
        raise VaultAuthenticationError(
            f"EVA secret TLS/client-certificate error: {exc}"
        ) from exc

    password = (
        response_data.get("data", {}).get("data", {}).get("password")
        or response_data.get("data", {}).get("password")
    )

    if not password:
        raise VaultAuthenticationError(
            "EVA returned the secret successfully, but no password field "
            "was found in the JSON response"
        )

    return str(password)
