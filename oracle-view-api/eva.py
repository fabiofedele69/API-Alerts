from pathlib import Path

EVA_CONFIG = Path("/app/M50/m50-batch-jobs/bin/env/eva.config")


def read_eva_config():
    """
    Reads the EVA configuration file and returns its values.
    """

    if not EVA_CONFIG.exists():
        raise FileNotFoundError(f"{EVA_CONFIG} not found")

    line = EVA_CONFIG.read_text().strip()

    fields = line.split("|")

    if len(fields) != 6:
        raise RuntimeError(
            f"Unexpected eva.config format ({len(fields)} fields)"
        )

    return {
        "cert": fields[0],
        "key": fields[1],
        "namespace": fields[2],
        "role": fields[3],
        "login_url": fields[4],
        "secret_url": fields[5],
    }
