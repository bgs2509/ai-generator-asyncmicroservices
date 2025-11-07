"""Pydantic schemas for API request/response validation.

Schemas define the structure of data exchanged via API.
Separate from models (database) for clean layer separation.

Example:
    from src.schemas.user import UserCreate, UserResponse
    from src.schemas.product import ProductCreate, ProductResponse
"""

from src.schemas.base import BaseSchema

__all__ = ["BaseSchema"]
