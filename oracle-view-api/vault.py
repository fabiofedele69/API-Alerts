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
