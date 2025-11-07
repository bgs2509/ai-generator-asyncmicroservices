"""Centralized logging configuration for all services.

This module provides a factory for creating structured JSON loggers
with consistent formatting across the microservices ecosystem.

Usage:
    >>> from shared.utils.logger import create_logger
    >>> logger = create_logger(__name__)
    >>> logger.info("User authenticated", extra={"user_id": 123})
    # Output: {"asctime": "2025-01-07T10:30:00", "name": "auth_service",
    #          "levelname": "INFO", "message": "User authenticated",
    #          "user_id": 123, "request_id": "abc-123"}
"""

import logging
import sys
from typing import Callable, Optional

from pythonjsonlogger import jsonlogger


def create_logger(
    name: str,
    level: str = "INFO",
    include_request_id: bool = True,
) -> logging.Logger:
    """Create structured JSON logger.

    Args:
        name: Logger name (typically __name__ of calling module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        include_request_id: Whether to include request_id in log format

    Returns:
        Configured logger instance with JSON formatting

    Example:
        >>> logger = create_logger(__name__)
        >>> logger.info("User authenticated", extra={"user_id": 123})
        # Output: {"asctime": "2025-01-07T10:30:00", ...}
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stdout)

    # Build format string
    format_fields = [
        "%(asctime)s",
        "%(name)s",
        "%(levelname)s",
        "%(message)s",
    ]

    if include_request_id:
        format_fields.append("%(request_id)s")

    formatter = jsonlogger.JsonFormatter(" ".join(format_fields))
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


class RequestIdFilter(logging.Filter):
    """Inject request_id into all log records.

    This filter should be added to loggers in API services
    to automatically include correlation IDs in logs.

    Example:
        >>> from shared.utils.request_id import get_request_id
        >>> logger = create_logger(__name__)
        >>> logger.addFilter(RequestIdFilter(get_request_id))
    """

    def __init__(self, get_request_id_func: Callable[[], Optional[str]]) -> None:
        """Initialize filter with request ID getter function.

        Args:
            get_request_id_func: Callable that returns current request ID
        """
        super().__init__()
        self._get_request_id = get_request_id_func

    def filter(self, record: logging.LogRecord) -> bool:
        """Add request_id to log record.

        Args:
            record: Log record to modify

        Returns:
            True (always pass through)
        """
        record.request_id = self._get_request_id() or "no-request-id"
        return True


def configure_uvicorn_logging(level: str = "INFO") -> None:
    """Configure uvicorn access logs to use JSON format.

    Call this in FastAPI startup event to ensure consistent
    log formatting for HTTP access logs.

    Args:
        level: Logging level for uvicorn loggers

    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> @app.on_event("startup")
        >>> async def startup():
        >>>     configure_uvicorn_logging()
    """
    uvicorn_loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]

    for logger_name in uvicorn_loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()

        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(level.upper())
