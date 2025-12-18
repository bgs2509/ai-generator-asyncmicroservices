"""Base Pydantic schemas for API validation.

Provides base schema classes with common configuration.
"""

from datetime import datetime
from typing import Any, Generic, TypeVar

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base Pydantic schema with common configuration.

    All API schemas should inherit from this class.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        use_enum_values=True,
        validate_assignment=True,
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
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

    error: dict[str, Any]


T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response structure.

    Used for list endpoints with pagination.

    Example:
        >>> @router.get("/items", response_model=PaginatedResponse[ItemResponse])
        >>> async def list_items(skip: int = 0, limit: int = 20):
        >>>     items = await repo.get_all(skip=skip, limit=limit)
        >>>     total = await repo.count()
        >>>     return PaginatedResponse(
        >>>         items=items,
        >>>         total=total,
        >>>         skip=skip,
        >>>         limit=limit,
        >>>     )
    """

    items: list[T]
    total: int
    skip: int = 0
    limit: int = 20
    has_more: bool = False

    def __init__(self, **data: Any):
        """Initialize and calculate has_more."""
        super().__init__(**data)
        # Calculate has_more based on pagination
        object.__setattr__(
            self, "has_more", (self.skip + len(self.items)) < self.total
        )
