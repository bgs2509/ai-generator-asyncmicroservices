"""Request ID middleware for FastAPI.

Provides request correlation across services.

Usage:
    from fastapi import FastAPI
    from shared.middleware import RequestIdMiddleware

    app = FastAPI()
    app.add_middleware(RequestIdMiddleware)
"""
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from shared.utils.logger import create_logger
from shared.utils.request_id import (
    generate_request_id,
    set_request_id,
    get_request_id,
)

logger = create_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware for request ID correlation and logging.

    - Extracts X-Request-ID from incoming headers or generates new UUID
    - Sets request ID in context for logging correlation
    - Adds X-Request-ID to response headers
    - Logs request start/end with timing
    """

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = generate_request_id()
        set_request_id(request_id)

        # Log request start
        start_time = time.perf_counter()
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query": str(request.query_params),
                "request_id": request_id,
            },
        )

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Add request ID to response
        response.headers["X-Request-ID"] = request_id

        # Log request completion
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "request_id": request_id,
            },
        )

        return response
