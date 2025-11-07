"""Base Pydantic schemas for API validation.

Provides base schema classes with common configuration.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base Pydantic schema with common configuration.

    All API schemas should inherit from this class.
    """

    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode (for SQLAlchemy models)
        populate_by_name=True,  # Allow both field names and aliases
        use_enum_values=True,  # Use enum values instead of enum objects
        validate_assignment=True,  # Validate on attribute assignment
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields.

    For responses that include created_at and updated_at.
    """

    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseSchema):
    """Health check response structure.

    Used by /health endpoints.
    """

    status: str
    version: str
    checks: dict[str, str] = {}


class ErrorResponse(BaseSchema):
    """Error response structure.

    Standard format for all API errors.
    """

    error: dict[str, any]
