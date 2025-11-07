"""Base repository with generic CRUD operations.

Provides reusable repository pattern for all models, eliminating
code duplication for common database operations.
"""

from typing import Generic, TypeVar, Type, Optional, Sequence, Any

from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository with CRUD operations.

    This repository implements common database operations that work
    with any SQLAlchemy model. Inherit from this class for
    model-specific repositories.

    Example:
        >>> class UserRepository(BaseRepository[UserModel]):
        >>>     def __init__(self, session: AsyncSession):
        >>>         super().__init__(UserModel, session)
        >>>
        >>>     async def get_by_email(self, email: str) -> Optional[UserModel]:
        >>>         result = await self._session.execute(
        >>>             select(self._model).where(self._model.email == email)
        >>>         )
        >>>         return result.scalar_one_or_none()
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """Initialize repository.

        Args:
            model: SQLAlchemy model class
            session: Async database session
        """
        self._model = model
        self._session = session

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get single record by ID.

        Args:
            id: Primary key value

        Returns:
            Model instance or None if not found

        Example:
            >>> user = await repo.get_by_id(1)
            >>> if user:
            >>>     print(user.name)
        """
        result = await self._session.execute(
            select(self._model).where(self._model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
    ) -> Sequence[ModelType]:
        """Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Column name to order by (default: id DESC)

        Returns:
            List of model instances

        Example:
            >>> users = await repo.get_all(skip=0, limit=20)
            >>> for user in users:
            >>>     print(user.email)
        """
        query = select(self._model)

        # Apply ordering
        if order_by:
            query = query.order_by(getattr(self._model, order_by))
        else:
            query = query.order_by(self._model.id.desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self._session.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs: Any) -> ModelType:
        """Create new record.

        Args:
            **kwargs: Column values for new record

        Returns:
            Created model instance with generated ID

        Example:
            >>> user = await repo.create(
            >>>     email="user@example.com",
            >>>     name="John Doe"
            >>> )
            >>> print(user.id)  # Auto-generated ID
            1
        """
        instance = self._model(**kwargs)
        self._session.add(instance)
        await self._session.flush()  # Generate ID
        await self._session.refresh(instance)  # Load defaults
        return instance

    async def update(self, id: int, **kwargs: Any) -> Optional[ModelType]:
        """Update existing record.

        Args:
            id: Primary key of record to update
            **kwargs: Column values to update

        Returns:
            Updated model instance or None if not found

        Example:
            >>> user = await repo.update(
            >>>     1,
            >>>     name="Jane Doe",
            >>>     email="jane@example.com"
            >>> )
        """
        await self._session.execute(
            update(self._model)
            .where(self._model.id == id)
            .values(**kwargs)
        )
        await self._session.flush()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        """Delete record by ID.

        Args:
            id: Primary key of record to delete

        Returns:
            True if record was deleted, False if not found

        Example:
            >>> deleted = await repo.delete(1)
            >>> print(deleted)
            True
        """
        result = await self._session.execute(
            delete(self._model).where(self._model.id == id)
        )
        await self._session.flush()
        return result.rowcount > 0

    async def count(self, filters: Optional[dict[str, Any]] = None) -> int:
        """Count total number of records.

        Args:
            filters: Optional filters as dict (column_name: value)

        Returns:
            Total record count

        Example:
            >>> total = await repo.count()
            >>> print(f"Total users: {total}")
            Total users: 150

            >>> active_count = await repo.count({"is_active": True})
            >>> print(f"Active users: {active_count}")
            Active users: 120
        """
        query = select(func.count()).select_from(self._model)

        if filters:
            for column, value in filters.items():
                query = query.where(getattr(self._model, column) == value)

        result = await self._session.execute(query)
        return result.scalar()

    async def exists(self, id: int) -> bool:
        """Check if record exists.

        Args:
            id: Primary key to check

        Returns:
            True if record exists, False otherwise

        Example:
            >>> if await repo.exists(1):
            >>>     print("User exists")
        """
        result = await self._session.execute(
            select(self._model.id).where(self._model.id == id)
        )
        return result.scalar_one_or_none() is not None

    async def bulk_create(self, items: list[dict[str, Any]]) -> Sequence[ModelType]:
        """Create multiple records in bulk.

        Args:
            items: List of dictionaries with column values

        Returns:
            List of created model instances

        Example:
            >>> users = await repo.bulk_create([
            >>>     {"email": "user1@example.com", "name": "User 1"},
            >>>     {"email": "user2@example.com", "name": "User 2"},
            >>> ])
            >>> print(len(users))
            2
        """
        instances = [self._model(**item) for item in items]
        self._session.add_all(instances)
        await self._session.flush()

        # Refresh all instances to load generated IDs and defaults
        for instance in instances:
            await self._session.refresh(instance)

        return instances

    async def bulk_delete(self, ids: list[int]) -> int:
        """Delete multiple records by IDs.

        Args:
            ids: List of primary keys to delete

        Returns:
            Number of records deleted

        Example:
            >>> deleted_count = await repo.bulk_delete([1, 2, 3])
            >>> print(f"Deleted {deleted_count} users")
            Deleted 3 users
        """
        result = await self._session.execute(
            delete(self._model).where(self._model.id.in_(ids))
        )
        await self._session.flush()
        return result.rowcount
