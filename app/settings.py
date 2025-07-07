from pathlib import Path
from loguru import logger

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