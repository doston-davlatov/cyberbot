# bot/utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE

def setup_logger():
    """
    Root logger ni bir marta to'g'ri sozlaydi:
    - console + rotating file
    - formatlar standart
    """
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Agar oldin handlerlar qo'shilgan bo'lsa, tozalash (duplicate oldini olish uchun)
    if root.hasHandlers():
        root.handlers.clear()

    # File handler (rotating)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    root.addHandler(console_handler)

    logging.info("Logging tizimi muvaffaqiyatli sozlandi")