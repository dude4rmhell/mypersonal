from __future__ import annotations

import logging

from config import settings


def get_logger(name: str = "helios.ai") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False
    settings.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(settings.LOG_PATH, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
    logger.addHandler(handler)
    return logger
