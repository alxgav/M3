import os
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'

# Create log directory if it doesn't exist
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Loguru configuration
logger.remove()
logger.add(
    str(LOG_DIR / 'app.log'),
    format="{time:MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 week",
    compression="gz",
    retention="1 month",
)


class Config(BaseSettings):
    DATABASE_URL: str
    PGHOST: str
    PGDATABASE: str
    PGUSER: str
    PGPASSWORD: str
    PGSSLMODE: str = "require"
    PGCHANNELBINDING: str = "require"

    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()