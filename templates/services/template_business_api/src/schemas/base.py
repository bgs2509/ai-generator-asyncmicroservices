"""Base schemas for API responses.

Provides common response patterns for consistency.
"""
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(BaseModel):
    """Base response with metadata."""

    success: bool = True
    message: str = "OK"


class DataResponse(BaseResponse, Generic[T]):
    """Response containing data."""

    data: T


class ErrorResponse(BaseModel):
    """Error response format."""

    success: bool = False
    error: str
    detail: str | None = None
    request_id: str | None = None


class PaginatedResponse(BaseResponse, Generic[T]):
    """Paginated response format."""

    data: list[T]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total_pages: int = Field(ge=0)


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime
    updated_at: datetime | None = None
