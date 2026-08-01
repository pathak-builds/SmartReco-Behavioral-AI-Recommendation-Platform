"""
Logging configuration for SmartReco.

Provides centralized logging configuration for the application using
Python's built-in logging module.

Features:
- Console logging
- Rotating file logging
- Automatic log directory creation
- UTF-8 support
- Configurable log levels
- Reduced third-party log noise
"""

from pathlib import Path
import logging
import logging.config
from logging import Logger
from typing import Any


def setup_logging(log_level: str = "INFO") -> Logger:
    """
    Configure application logging.

    Parameters
    ----------
    log_level : str
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns
    -------
    Logger
        Root application logger.
    """

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging_config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": (
                    "[%(asctime)s] "
                    "%(levelname)-8s "
                    "%(name)s - "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": (
                    "[%(asctime)s] "
                    "%(levelname)-8s "
                    "%(name)s:%(lineno)d - "
                    "%(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": log_level,
                "formatter": "detailed",
                "filename": str(log_dir / "smartreco.log"),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": log_level,
            "handlers": [
                "console",
                "file",
            ],
        },
    }

    logging.config.dictConfig(logging_config)

    # Silence noisy third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)

    logger = logging.getLogger("smartreco")
    logger.info("=" * 70)
    logger.info("SmartReco logging initialized successfully.")
    logger.info("Log Level: %s", log_level)
    logger.info("=" * 70)

    return logger