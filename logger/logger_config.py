"""
logger_config.py

Конфигурация логгера для проекта. Логи пишутся в папку logs с ротацией по 500 КБ.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'app.log'

LOG_FORMAT = (
    '%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(funcName)s | %(filename)s:%(lineno)d | %(message)s'
)

# Максимальный размер файла лога — 500 КБ
MAX_LOG_SIZE = 500 * 1024  # 500 КБ
BACKUP_COUNT = 5


def setup_logger(name: str) -> logging.Logger:
    """
    Создаёт и возвращает настроенный логгер с ротацией файлов.

    Args:
        name: Имя логгера (обычно __name__).
    Returns:
        logging.Logger: Настроенный логгер.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT, encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger 