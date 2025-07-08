import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

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

#  database settings

# Read individual PostgreSQL connection parameters
# PGHOST = os.getenv("PGHOST", "localhost")
# PGDATABASE = os.getenv("PGDATABASE")
# PGUSER = os.getenv("PGUSER")
# PGPASSWORD = os.getenv("PGPASSWORD")
# PGPORT = os.getenv("PGPORT", "5432")
# PGSSLMODE = os.getenv("PGSSLMODE", "require")
# PGCHANNELBINDING = os.getenv("PGCHANNELBINDING", "require")

# Validate required parameters
# if not all([PGDATABASE, PGUSER, PGPASSWORD]):
#     raise ValueError(logger.error("Missing required PostgreSQL connection parameters in .env file"))
#
# DATABASE_URL = (
#     f"postgresql+asyncpg://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
#     f"?sslmode={PGSSLMODE}"
#     f"&sslrootcert={os.getenv('PGSSLROOTCERT', '')}"
#     f"&sslcert={os.getenv('PGSSLCERT', '')}"
#     f"&sslkey={os.getenv('PGSSLKEY', '')}"
#     f"&channel_binding={PGCHANNELBINDING}"
# )

DATABASE_URL = os.getenv("DATABASE_URL")

#FastAPI settings
DEBUG = os.getenv("DEBUG", False)
HOST = os.getenv("HOST", "127.0.0.1")
PORT = os.getenv("PORT", 8000)