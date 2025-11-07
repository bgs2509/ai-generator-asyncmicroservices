"""Pagination utilities for API responses.

Supports both offset-based and cursor-based pagination patterns.

Example (Offset):
    >>> from shared.utils.pagination import OffsetPaginationParams
    >>> params = OffsetPaginationParams(limit=20, offset=0)
    >>> # Use in database query: .limit(params.limit).offset(params.skip)

Example (Cursor):
    >>> from shared.utils.pagination import create_cursor, parse_cursor
    >>> cursor = create_cursor(entity_id=123)
    >>> # Return cursor in response
    >>> data = parse_cursor(cursor)  # {'id': 123}
"""

import base64
import json
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class OffsetPaginationParams(BaseModel):
    """Query parameters for offset-based pagination.

    Offset pagination is simple and works well for small to medium datasets.
    Use when:
    - Dataset is relatively small (<10,000 items)
    - Users need to jump to arbitrary pages
    - Concurrent data modifications are rare

    Example:
        GET /users?limit=20&offset=40
    """

    limit: int = Field(default=20, ge=1, le=100, description="Items per page")
    offset: int = Field(default=0, ge=0, description="Items to skip")

    @property
    def skip(self) -> int:
        """Alias for offset (used in database queries).

        Returns:
            Number of items to skip
        """
        return self.offset


class OffsetPaginatedResponse(BaseModel, Generic[T]):
    """Response structure for offset-based pagination.

    Attributes:
        items: List of items for current page
        total: Total number of items across all pages
        limit: Items per page
        offset: Current offset
        has_next: Whether there are more pages
        has_previous: Whether there is a previous page
    """

    items: list[T]
    total: int
    limit: int
    offset: int

    @property
    def has_next(self) -> bool:
        """Check if there are more pages.

        Returns:
            True if there are more items after current page
        """
        return self.offset + self.limit < self.total

    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page.

        Returns:
            True if offset > 0
        """
        return self.offset > 0

    @property
    def current_page(self) -> int:
        """Calculate current page number (1-indexed).

        Returns:
            Current page number
        """
        if self.limit == 0:
            return 1
        return (self.offset // self.limit) + 1

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages.

        Returns:
            Total number of pages
        """
        if self.limit == 0:
            return 1
        return (self.total + self.limit - 1) // self.limit


class CursorPaginationParams(BaseModel):
    """Query parameters for cursor-based pagination.

    Cursor pagination is more efficient for large datasets and prevents
    issues with concurrent modifications.

    Use when:
    - Dataset is large (>10,000 items)
    - Data changes frequently (concurrent modifications)
    - Users don't need to jump to arbitrary pages
    - Infinite scroll UI pattern

    Example:
        GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ
    """

    limit: int = Field(default=20, ge=1, le=100, description="Items per page")
    cursor: Optional[str] = Field(default=None, description="Pagination cursor")


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Response structure for cursor-based pagination.

    Attributes:
        items: List of items for current page
        next_cursor: Cursor for next page (None if last page)
        has_next: Whether there are more pages
    """

    items: list[T]
    next_cursor: Optional[str] = None

    @property
    def has_next(self) -> bool:
        """Check if there are more pages.

        Returns:
            True if next_cursor is not None
        """
        return self.next_cursor is not None


def create_cursor(entity_id: int) -> str:
    """Create base64-encoded cursor from entity ID.

    The cursor encodes the ID of the last item in the current page,
    allowing the next request to efficiently fetch items after this ID.

    Args:
        entity_id: ID of last entity in current page

    Returns:
        Base64-encoded cursor string

    Example:
        >>> cursor = create_cursor(123)
        >>> print(cursor)
        'eyJpZCI6MTIzfQ=='

    Note:
        For more complex cursors (multi-column sorting), encode a dict
        with multiple fields: {"id": 123, "created_at": "2025-01-07"}
    """
    cursor_data = {"id": entity_id}
    cursor_json = json.dumps(cursor_data)
    return base64.b64encode(cursor_json.encode()).decode()


def parse_cursor(cursor: str) -> dict:
    """Parse base64-encoded cursor to extract entity ID.

    Args:
        cursor: Base64-encoded cursor string

    Returns:
        Dictionary with cursor data (contains 'id' key)

    Raises:
        ValueError: If cursor format is invalid

    Example:
        >>> data = parse_cursor('eyJpZCI6MTIzfQ==')
        >>> print(data)
        {'id': 123}

    Note:
        For production, add cursor signature/encryption to prevent
        tampering: cursor = sign(base64(data)) + "." + base64(data)
    """
    try:
        cursor_json = base64.b64decode(cursor.encode()).decode()
        return json.loads(cursor_json)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid cursor format: {e}")


def create_multi_field_cursor(fields: dict[str, any]) -> str:
    """Create cursor with multiple fields for complex sorting.

    Use when pagination needs to handle multi-column sorting
    (e.g., ORDER BY created_at DESC, id DESC).

    Args:
        fields: Dictionary of field names and values

    Returns:
        Base64-encoded cursor string

    Example:
        >>> cursor = create_multi_field_cursor({
        >>>     "created_at": "2025-01-07T10:00:00Z",
        >>>     "id": 123
        >>> })
    """
    cursor_json = json.dumps(fields)
    return base64.b64encode(cursor_json.encode()).decode()


def parse_multi_field_cursor(cursor: str) -> dict[str, any]:
    """Parse multi-field cursor.

    Args:
        cursor: Base64-encoded cursor string

    Returns:
        Dictionary with all cursor fields

    Raises:
        ValueError: If cursor format is invalid

    Example:
        >>> data = parse_multi_field_cursor(cursor)
        >>> print(data)
        {'created_at': '2025-01-07T10:00:00Z', 'id': 123}
    """
    try:
        cursor_json = base64.b64decode(cursor.encode()).decode()
        return json.loads(cursor_json)
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid cursor format: {e}")
