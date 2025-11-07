"""Repositories for database access.

Repositories implement the Repository Pattern, providing
a clean interface for database operations.

Import repositories here for easy access:

Example:
    from src.repositories.user_repository import UserRepository
    from src.repositories.product_repository import ProductRepository
"""

from src.repositories.base_repository import BaseRepository

__all__ = ["BaseRepository"]
