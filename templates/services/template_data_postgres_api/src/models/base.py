"""Base SQLAlchemy model and mixins.

Provides base model class with common columns and utility methods.
"""

import re
from datetime import datetime
from typing import Any

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    Automatically generates table names from class names.
    Provides common columns and utility methods.
    """

    # Primary key (all tables have 'id')
    id: int = Column(Integer, primary_key=True, index=True)

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """Generate __tablename__ from class name.

        Converts CamelCase to snake_case.

        Example:
            UserModel -> user_model
            PostComment -> post_comment
        """
        # Convert CamelCase to snake_case
        name = cls.__name__
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary.

        Returns:
            Dictionary with all column values

        Example:
            >>> user = UserModel(id=1, email="user@example.com")
            >>> user.to_dict()
            {'id': 1, 'email': 'user@example.com', 'created_at': '...'}
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps.

    Usage:
        >>> class UserModel(Base, TimestampMixin):
        >>>     email = Column(String, unique=True)
        >>>
        >>> # Automatically has created_at and updated_at columns
    """

    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        doc="Timestamp when record was created",
    )

    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        doc="Timestamp when record was last updated",
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality.

    Instead of deleting records, mark them as deleted.

    Usage:
        >>> class UserModel(Base, SoftDeleteMixin):
        >>>     email = Column(String, unique=True)
        >>>
        >>> # Has deleted_at column
        >>> # Query only non-deleted: session.query(User).filter(User.deleted_at.is_(None))
    """

    deleted_at: datetime | None = Column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
        doc="Timestamp when record was soft deleted (NULL if not deleted)",
    )

    @property
    def is_deleted(self) -> bool:
        """Check if record is soft deleted.

        Returns:
            True if deleted_at is set, False otherwise
        """
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        """Mark record as deleted.

        Sets deleted_at to current timestamp.
        """
        self.deleted_at = datetime.utcnow()

    def restore(self) -> None:
        """Restore soft-deleted record.

        Sets deleted_at back to None.
        """
        self.deleted_at = None
