import logging
import config
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

handler = RotatingFileHandler(
    config.LOG_FILE,
    maxBytes=5*1024*1024,
    backupCount=3
)
handler.setFormatter(formatter)

logger = logging.getLogger("cyberguard")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)