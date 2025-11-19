"""Logging configuration using Loguru."""

import sys

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    """Configure loguru logging based on settings."""
    # Remove default handler
    logger.remove()

    # Configure format based on environment
    if settings.LOG_FORMAT == "json":
        # Structured JSON logging for production
        log_format = (
            "{"
            '"time": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
            '"level": "{level}", '
            '"module": "{module}", '
            '"function": "{function}", '
            '"line": {line}, '
            '"message": "{message}", '
            '"extra": {extra}'
            "}"
        )
    else:
        # Human-readable format for development
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

    # Add handler with appropriate configuration
    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.LOG_LEVEL,
        colorize=settings.LOG_FORMAT != "json",
        serialize=settings.LOG_FORMAT == "json",
        backtrace=True,
        diagnose=True,
    )

    # Add file handler for production
    if settings.is_production:
        logger.add(
            "logs/app.log",
            format=log_format,
            level=settings.LOG_LEVEL,
            rotation="10 MB",
            retention="30 days",
            compression="gz",
            serialize=True,
        )

    logger.info(
        f"Logging configured: level={settings.LOG_LEVEL}, format={settings.LOG_FORMAT}"
    )


# Initialize logging when module is imported
setup_logging()
