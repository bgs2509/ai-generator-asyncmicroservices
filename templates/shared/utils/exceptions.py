"""Base exception classes for framework services.

Provides consistent exception hierarchy with proper HTTP status code
mapping for API services.

Example:
    >>> from shared.utils.exceptions import NotFoundError
    >>> raise NotFoundError(
    >>>     message="User not found",
    >>>     details={"user_id": 123}
    >>> )
"""

from typing import Any, Optional


class BaseServiceException(Exception):
    """Base exception for all service errors.

    All custom exceptions should inherit from this class
    to enable consistent error handling.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code (e.g., "USER_NOT_FOUND")
        status_code: HTTP status code for API responses
        details: Additional error context
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize service exception.

        Args:
            message: Error message for users/logs
            error_code: Structured error code
            status_code: HTTP status code
            details: Optional additional context
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(BaseServiceException):
    """Resource not found (HTTP 404).

    Example:
        >>> raise NotFoundError(
        >>>     message="User not found",
        >>>     error_code="USER_NOT_FOUND",
        >>>     details={"user_id": 123}
        >>> )
    """

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404,
            details=details,
        )


class ValidationError(BaseServiceException):
    """Validation failed (HTTP 422).

    Example:
        >>> raise ValidationError(
        >>>     message="Invalid email format",
        >>>     error_code="INVALID_EMAIL",
        >>>     details={"field": "email", "value": "invalid"}
        >>> )
    """

    def __init__(
        self,
        message: str = "Validation failed",
        error_code: str = "VALIDATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=422,
            details=details,
        )


class UnauthorizedError(BaseServiceException):
    """Authentication required (HTTP 401).

    Example:
        >>> raise UnauthorizedError(
        >>>     message="Invalid credentials",
        >>>     error_code="INVALID_CREDENTIALS"
        >>> )
    """

    def __init__(
        self,
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            details=details,
        )


class ForbiddenError(BaseServiceException):
    """Permission denied (HTTP 403).

    Example:
        >>> raise ForbiddenError(
        >>>     message="Insufficient permissions",
        >>>     error_code="INSUFFICIENT_PERMISSIONS",
        >>>     details={"required_role": "admin", "user_role": "user"}
        >>> )
    """

    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "FORBIDDEN",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=403,
            details=details,
        )


class ConflictError(BaseServiceException):
    """Resource conflict (HTTP 409).

    Use when trying to create a resource that already exists
    or when there's a state conflict.

    Example:
        >>> raise ConflictError(
        >>>     message="Email already registered",
        >>>     error_code="EMAIL_ALREADY_EXISTS",
        >>>     details={"email": "user@example.com"}
        >>> )
    """

    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str = "CONFLICT",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=409,
            details=details,
        )


class ExternalServiceError(BaseServiceException):
    """External service call failed (HTTP 502/503).

    Use when downstream service (data API, payment gateway, etc.)
    is unavailable or returns an error.

    Example:
        >>> raise ExternalServiceError(
        >>>     message="Payment gateway unavailable",
        >>>     error_code="PAYMENT_GATEWAY_ERROR",
        >>>     status_code=503,
        >>>     details={"service": "stripe", "timeout": 30}
        >>> )
    """

    def __init__(
        self,
        message: str = "External service unavailable",
        error_code: str = "EXTERNAL_SERVICE_ERROR",
        status_code: int = 503,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
            details=details,
        )


class RateLimitError(BaseServiceException):
    """Rate limit exceeded (HTTP 429).

    Example:
        >>> raise RateLimitError(
        >>>     message="Too many requests",
        >>>     retry_after=60,
        >>>     details={"limit": 100, "window": "1m"}
        >>> )
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        error_code: str = "RATE_LIMIT_EXCEEDED",
        retry_after: Optional[int] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if retry_after:
            details["retry_after"] = retry_after

        super().__init__(
            message=message,
            error_code=error_code,
            status_code=429,
            details=details,
        )


class BadRequestError(BaseServiceException):
    """Bad request (HTTP 400).

    Use for malformed requests or invalid parameters that don't
    fit other specific error types.

    Example:
        >>> raise BadRequestError(
        >>>     message="Missing required parameter",
        >>>     error_code="MISSING_PARAMETER",
        >>>     details={"parameter": "user_id"}
        >>> )
    """

    def __init__(
        self,
        message: str = "Bad request",
        error_code: str = "BAD_REQUEST",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=400,
            details=details,
        )


class ServiceUnavailableError(BaseServiceException):
    """Service temporarily unavailable (HTTP 503).

    Use during maintenance windows or when service is overloaded.

    Example:
        >>> raise ServiceUnavailableError(
        >>>     message="Service under maintenance",
        >>>     error_code="MAINTENANCE_MODE",
        >>>     details={"eta": "2025-01-07T12:00:00Z"}
        >>> )
    """

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        error_code: str = "SERVICE_UNAVAILABLE",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=503,
            details=details,
        )
