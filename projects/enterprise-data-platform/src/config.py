import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Enterprise Data Platform")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT = int(os.getenv("APP_PORT", "8001"))

    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "enterprise_data")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "platform_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", "8123"))
    CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "analytics")


settings = Settings()