"""Request ID (correlation ID) management for distributed tracing.

Provides context variables for propagating request IDs across
async function calls and service boundaries.

Example:
    >>> from shared.utils.request_id import generate_request_id, set_request_id
    >>> # In middleware:
    >>> request_id = generate_request_id()
    >>> set_request_id(request_id)
    >>>
    >>> # Anywhere in request processing:
    >>> from shared.utils.request_id import get_request_id
    >>> logger.info("Processing request", extra={"request_id": get_request_id()})
"""

import uuid
from contextvars import ContextVar
from typing import Optional


# Context variable for current request ID
# Context variables are safe for async/await and maintain isolation
# between concurrent requests
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    "request_id", default=None
)


def generate_request_id() -> str:
    """Generate new UUID-based request ID.

    Returns:
        UUID string in format: req_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    Example:
        >>> request_id = generate_request_id()
        >>> print(request_id)
        'req_123e4567-e89b-12d3-a456-426614174000'

    Note:
        The "req_" prefix helps distinguish request IDs from other UUIDs
        in logs and makes them easily searchable.
    """
    return f"req_{uuid.uuid4()}"


def set_request_id(request_id: str) -> None:
    """Set request ID in context.

    This should be called at the start of request processing
    (e.g., in FastAPI middleware or Aiogram middleware).

    Args:
        request_id: Request ID to set

    Example:
        >>> # In FastAPI middleware:
        >>> request_id = request.headers.get("X-Request-ID") or generate_request_id()
        >>> set_request_id(request_id)
        >>>
        >>> # Later in request processing:
        >>> current_id = get_request_id()  # Returns the same ID
    """
    _request_id_ctx_var.set(request_id)


def get_request_id() -> Optional[str]:
    """Get current request ID from context.

    Returns:
        Current request ID, or None if not set

    Example:
        >>> request_id = get_request_id()
        >>> if request_id:
        >>>     logger.info("Processing", extra={"request_id": request_id})
    """
    return _request_id_ctx_var.get()


def get_or_generate_request_id() -> str:
    """Get current request ID or generate new one.

    This is useful for background tasks that may not have
    a request ID set in context.

    Returns:
        Current request ID or newly generated one

    Example:
        >>> # Background task without request context:
        >>> request_id = get_or_generate_request_id()
        >>> logger.info("Background task", extra={"request_id": request_id})
    """
    request_id = get_request_id()
    if request_id is None:
        request_id = generate_request_id()
        set_request_id(request_id)
    return request_id


def reset_request_id() -> None:
    """Reset request ID context.

    Useful for testing or cleanup in background tasks.

    Example:
        >>> # In test teardown:
        >>> reset_request_id()
    """
    _request_id_ctx_var.set(None)


# Alias for backward compatibility
clear_request_id = reset_request_id
