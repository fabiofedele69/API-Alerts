import json
import ssl
import urllib.error
import urllib.request
from typing import Any, Dict

from app.eva import read_eva_config


CA_BUNDLE = "/app/M50/dyn/npa/certs/FA23303/cacerts.pem"
HTTP_TIMEOUT_SECONDS = 30


class VaultAuthenticationError(RuntimeError):
    """Raised when communication with EVA Vault fails."""


def _read_json_response(response: Any) -> Dict[str, Any]:
    """
    Read an HTTP response and decode its JSON body.
    """

    raw_body = response.read().decode("utf-8")

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as exc:
        raise VaultAuthenticationError(
            "EVA returned a response that is not valid JSON"
        ) from exc


def _create_ssl_context(config: Dict[str, str]) -> ssl.SSLContext:
    """
    Create the SSL context used for EVA authentication
    and secret retrieval.

    The context:
    - trusts the UBS CA bundle;
    - presents the configured client certificate;
    - presents the configured private key;
    - verifies the EVA server certificate.
    """

    ssl_context = ssl.create_default_context(cafile=CA_BUNDLE)

    ssl_context.load_cert_chain(
        certfile=config["cert"],
        keyfile=config["key"],
    )

    return ssl_context


def get_vault_token() -> str:
    """
    Authenticate to EVA Vault using the configured client certificate.

    The token is returned only in memory. It is not logged
    and is not written to disk.
    """

    config = read_eva_config()
    ssl_context = _create_ssl_context(config)

    request_body = json.dumps(
        {
            "name": config["role"],
        }
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
            timeout=HTTP_TIMEOUT_SECONDS,
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

    return str(token)


def get_oracle_password() -> str:
    """
    Retrieve the Oracle password from EVA Vault.

    The password is returned only in memory. It is not logged
    and is not written to disk.
    """

    config = read_eva_config()
    token = get_vault_token()
    ssl_context = _create_ssl_context(config)

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
            timeout=HTTP_TIMEOUT_SECONDS,
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
            "EVA returned the secret successfully, but no password "
            "field was found in the JSON response"
        )

    return str(password)
