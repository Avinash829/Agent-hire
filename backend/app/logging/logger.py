"""
Structured Logging Configuration Module.

Provides centralized logging configuration using loguru.
Ensures consistent log format across the application.
"""

import sys
from pathlib import Path
from loguru import logger
from app.config.settings import get_settings


def configure_logging() -> None:
    """Configure structured logging with loguru."""
    settings = get_settings()
    log_level = settings.log_level.upper()

    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stdout,
        format=log_format,
        level=log_level,
        colorize=True,
    )

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    logger.add(
        log_directory / "application.log",
        format=log_format,
        level=log_level,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )

    logger.add(
        log_directory / "errors.log",
        format=log_format,
        level="ERROR",
        rotation="10 MB",
        retention="90 days",
        compression="zip",
    )

    logger.info(f"Logging configured at {log_level} level")


def get_logger(module_name: str):
    """Return a logger instance bound to the specified module name."""
    return logger.bind(module=module_name)

