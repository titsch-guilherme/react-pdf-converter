"""Logging configuration using Loguru."""

import sys

from loguru import logger

from app.core.config import settings


def setup_logging():
    """Configure loguru logging based on settings."""
    # Remove default handler
    logger.remove()

    # Configure format based on environment
    if settings.LOG_FORMAT == "json":
        log_format = (
            "{"
            '"time": "{time:YYYY-MM-DD HH:mm:ss.SSS}", '
            '"level": "{level}", '
            '"message": "{message}", '
            '"module": "{module}", '
            '"function": "{function}", '
            '"line": {line}'
            "}"
        )
    else:
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

    # Add handler with appropriate configuration
    logger.add(
        sys.stdout,
        format=log_format,
        level=settings.LOG_LEVEL,
        serialize=settings.LOG_FORMAT == "json",
        backtrace=settings.DEBUG,
        diagnose=settings.DEBUG,
    )

    # Add file handler for production
    if settings.is_production:
        logger.add(
            "logs/app.log",
            format=log_format,
            level=settings.LOG_LEVEL,
            serialize=True,
            rotation="100 MB",
            retention="30 days",
            compression="gz",
            backtrace=False,
            diagnose=False,
        )

    logger.info(
        f"Logging configured - Level: {settings.LOG_LEVEL}, Format: {settings.LOG_FORMAT}"
    )


# Configure logging on import
setup_logging()
