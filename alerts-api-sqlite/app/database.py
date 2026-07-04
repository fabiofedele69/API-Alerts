import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()


def get_connection():
    """
    Returns a database connection based on the selected backend.
    """
    if DB_BACKEND == "oracle":
        return get_oracle_connection()

    return get_sqlite_connection()


def get_sqlite_connection():
    """
    SQLite connection used for local development.
    """
    db_path = os.getenv("SQLITE_DB_PATH", "alerts.db")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    return conn


def get_oracle_connection():
    """
    Oracle 19c connection.
    This function is NOT used until DB_BACKEND=oracle.
    """
    import oracledb

    use_thick = (
        os.getenv("ORACLE_USE_THICK_MODE", "false").lower() == "true"
    )

    if use_thick:
        client_lib_dir = os.getenv("ORACLE_CLIENT_LIB_DIR")

        if client_lib_dir:
            oracledb.init_oracle_client(lib_dir=client_lib_dir)
        else:
            oracledb.init_oracle_client()

    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    host = os.getenv("ORACLE_HOST")
    port = os.getenv("ORACLE_PORT", "1521")
    service_name = os.getenv("ORACLE_SERVICE_NAME")

    dsn = f"{host}:{port}/{service_name}"

    conn = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    )

    return conn