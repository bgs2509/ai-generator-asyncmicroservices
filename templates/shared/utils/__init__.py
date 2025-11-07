"""Shared utility modules for all microservices.

This package provides reusable components to eliminate code duplication
across services. All utilities are:
- Pure (no business logic)
- Well-tested (100% coverage)
- Fully type-hinted
- Framework-agnostic

Available modules:
- logger: Structured JSON logging factory
- validators: Common validation functions (email, phone, UUID, etc.)
- exceptions: Base exception hierarchy with HTTP status codes
- pagination: Offset and cursor pagination helpers
- request_id: Correlation ID management for distributed tracing
"""

from shared.utils.logger import create_logger, configure_uvicorn_logging, RequestIdFilter
from shared.utils.validators import (
    is_valid_email,
    is_valid_phone,
    is_valid_uuid,
    is_valid_url,
    validate_password_strength,
)
from shared.utils.exceptions import (
    BaseServiceException,
    NotFoundError,
    ValidationError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    ExternalServiceError,
    RateLimitError,
)
from shared.utils.pagination import (
    OffsetPaginationParams,
    OffsetPaginatedResponse,
    CursorPaginationParams,
    CursorPaginatedResponse,
    create_cursor,
    parse_cursor,
)
from shared.utils.request_id import (
    generate_request_id,
    set_request_id,
    get_request_id,
    get_or_generate_request_id,
)

__all__ = [
    # Logger
    "create_logger",
    "configure_uvicorn_logging",
    "RequestIdFilter",
    # Validators
    "is_valid_email",
    "is_valid_phone",
    "is_valid_uuid",
    "is_valid_url",
    "validate_password_strength",
    # Exceptions
    "BaseServiceException",
    "NotFoundError",
    "ValidationError",
    "UnauthorizedError",
    "ForbiddenError",
    "ConflictError",
    "ExternalServiceError",
    "RateLimitError",
    # Pagination
    "OffsetPaginationParams",
    "OffsetPaginatedResponse",
    "CursorPaginationParams",
    "CursorPaginatedResponse",
    "create_cursor",
    "parse_cursor",
    # Request ID
    "generate_request_id",
    "set_request_id",
    "get_request_id",
    "get_or_generate_request_id",
]

__version__ = "1.0.0"
