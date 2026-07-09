import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    ORACLE_USER = os.getenv("ORACLE_USER")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
    ORACLE_HOST = os.getenv("ORACLE_HOST")
    ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
    ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")

    API_HOST = "127.0.0.1"
    API_PORT = 8000


settings = Settings()
