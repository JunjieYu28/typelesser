"""Logging configuration for the application."""

import logging
import sys

from src.constants import DATA_DIR, LOG_PATH, APP_NAME


def setup_logging(debug: bool = False) -> logging.Logger:
    """Initialise root logger with file + console handlers."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler
    fh = logging.FileHandler(LOG_PATH, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger
