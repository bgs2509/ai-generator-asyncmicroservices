"""SQLAlchemy models for PostgreSQL database.

Import all models here to ensure they're registered with Base.metadata
for Alembic autogenerate to detect them.

Example:
    from src.models.base import Base
    from src.models.user import User
    from src.models.product import Product

    # All models are now registered and will be detected by Alembic
"""

from src.models.base import Base

__all__ = ["Base"]
