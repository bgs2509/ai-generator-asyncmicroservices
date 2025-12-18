"""Base repository with generic CRUD operations for MongoDB.

Provides reusable repository pattern for all collections, eliminating
code duplication for common database operations.
"""

from typing import Any, Generic, TypeVar, Type, Sequence

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from src.models.base import MongoModel
from shared.utils.logger import create_logger


logger = create_logger(__name__)

ModelType = TypeVar("ModelType", bound=MongoModel)


class BaseMongoRepository(Generic[ModelType]):
    """Generic repository with CRUD operations for MongoDB.

    This repository implements common database operations that work
    with any MongoDB collection. Inherit from this class for
    collection-specific repositories.

    Example:
        >>> class UserRepository(BaseMongoRepository[UserDocument]):
        >>>     def __init__(self, db: AsyncIOMotorDatabase):
        >>>         super().__init__(db, "users", UserDocument)
        >>>
        >>>     async def get_by_email(self, email: str) -> UserDocument | None:
        >>>         doc = await self._collection.find_one({"email": email})
        >>>         return UserDocument.from_mongo(doc) if doc else None
    """

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        collection_name: str,
        model_class: Type[ModelType],
    ) -> None:
        """Initialize repository.

        Args:
            db: Motor database instance
            collection_name: Name of the collection
            model_class: Pydantic model class for documents
        """
        self._db = db
        self._collection: AsyncIOMotorCollection = db[collection_name]
        self._model_class = model_class

    async def get_by_id(self, id: str | ObjectId) -> ModelType | None:
        """Get single document by ID.

        Args:
            id: Document ObjectId (as string or ObjectId)

        Returns:
            Model instance or None if not found

        Example:
            >>> user = await repo.get_by_id("507f1f77bcf86cd799439011")
            >>> if user:
            >>>     print(user.email)
        """
        if isinstance(id, str):
            id = ObjectId(id)

        doc = await self._collection.find_one({"_id": id})
        if doc is None:
            return None
        return self._model_class.from_mongo(doc)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_field: str = "_id",
        sort_order: int = -1,
        filters: dict[str, Any] | None = None,
    ) -> Sequence[ModelType]:
        """Get all documents with pagination.

        Args:
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            sort_field: Field to sort by (default: _id)
            sort_order: 1 for ascending, -1 for descending
            filters: Optional query filters

        Returns:
            List of model instances

        Example:
            >>> users = await repo.get_all(skip=0, limit=20)
            >>> for user in users:
            >>>     print(user.email)
        """
        query = filters or {}
        cursor = (
            self._collection.find(query)
            .sort(sort_field, sort_order)
            .skip(skip)
            .limit(limit)
        )

        results = []
        async for doc in cursor:
            results.append(self._model_class.from_mongo(doc))
        return results

    async def create(self, model: ModelType) -> ModelType:
        """Create new document.

        Args:
            model: Model instance to insert

        Returns:
            Created model instance with generated ID

        Example:
            >>> user = UserDocument(email="user@example.com", name="John")
            >>> created = await repo.create(user)
            >>> print(created.id)  # Auto-generated ObjectId
        """
        data = model.to_mongo()
        result = await self._collection.insert_one(data)

        # Fetch the created document
        created_doc = await self._collection.find_one({"_id": result.inserted_id})
        return self._model_class.from_mongo(created_doc)

    async def create_from_dict(self, data: dict[str, Any]) -> ModelType:
        """Create new document from dictionary.

        Args:
            data: Dictionary with document fields

        Returns:
            Created model instance with generated ID

        Example:
            >>> user = await repo.create_from_dict({
            >>>     "email": "user@example.com",
            >>>     "name": "John Doe"
            >>> })
        """
        result = await self._collection.insert_one(data)
        created_doc = await self._collection.find_one({"_id": result.inserted_id})
        return self._model_class.from_mongo(created_doc)

    async def update(
        self, id: str | ObjectId, update_data: dict[str, Any]
    ) -> ModelType | None:
        """Update existing document.

        Args:
            id: Document ObjectId
            update_data: Fields to update (without $set operator)

        Returns:
            Updated model instance or None if not found

        Example:
            >>> user = await repo.update(
            >>>     "507f1f77bcf86cd799439011",
            >>>     {"name": "Jane Doe", "email": "jane@example.com"}
            >>> )
        """
        if isinstance(id, str):
            id = ObjectId(id)

        result = await self._collection.update_one(
            {"_id": id},
            {"$set": update_data},
        )

        if result.matched_count == 0:
            return None

        return await self.get_by_id(id)

    async def update_raw(
        self, id: str | ObjectId, update: dict[str, Any]
    ) -> ModelType | None:
        """Update document with raw MongoDB update operators.

        Args:
            id: Document ObjectId
            update: MongoDB update document (with operators like $set, $inc, etc.)

        Returns:
            Updated model instance or None if not found

        Example:
            >>> user = await repo.update_raw(
            >>>     "507f1f77bcf86cd799439011",
            >>>     {"$inc": {"login_count": 1}, "$set": {"last_login": datetime.utcnow()}}
            >>> )
        """
        if isinstance(id, str):
            id = ObjectId(id)

        result = await self._collection.update_one({"_id": id}, update)

        if result.matched_count == 0:
            return None

        return await self.get_by_id(id)

    async def delete(self, id: str | ObjectId) -> bool:
        """Delete document by ID.

        Args:
            id: Document ObjectId

        Returns:
            True if document was deleted, False if not found

        Example:
            >>> deleted = await repo.delete("507f1f77bcf86cd799439011")
            >>> print(deleted)
            True
        """
        if isinstance(id, str):
            id = ObjectId(id)

        result = await self._collection.delete_one({"_id": id})
        return result.deleted_count > 0

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count total number of documents.

        Args:
            filters: Optional query filters

        Returns:
            Total document count

        Example:
            >>> total = await repo.count()
            >>> print(f"Total users: {total}")

            >>> active_count = await repo.count({"is_active": True})
        """
        query = filters or {}
        return await self._collection.count_documents(query)

    async def exists(self, id: str | ObjectId) -> bool:
        """Check if document exists.

        Args:
            id: Document ObjectId

        Returns:
            True if document exists, False otherwise

        Example:
            >>> if await repo.exists("507f1f77bcf86cd799439011"):
            >>>     print("User exists")
        """
        if isinstance(id, str):
            id = ObjectId(id)

        doc = await self._collection.find_one({"_id": id}, projection={"_id": 1})
        return doc is not None

    async def find_one(self, filters: dict[str, Any]) -> ModelType | None:
        """Find single document by filters.

        Args:
            filters: Query filters

        Returns:
            Model instance or None if not found

        Example:
            >>> user = await repo.find_one({"email": "test@example.com"})
        """
        doc = await self._collection.find_one(filters)
        if doc is None:
            return None
        return self._model_class.from_mongo(doc)

    async def find_many(
        self,
        filters: dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        sort_field: str = "_id",
        sort_order: int = -1,
    ) -> Sequence[ModelType]:
        """Find documents by filters with pagination.

        Args:
            filters: Query filters
            skip: Number of documents to skip
            limit: Maximum number of documents
            sort_field: Field to sort by
            sort_order: 1 for ascending, -1 for descending

        Returns:
            List of matching model instances
        """
        cursor = (
            self._collection.find(filters)
            .sort(sort_field, sort_order)
            .skip(skip)
            .limit(limit)
        )

        results = []
        async for doc in cursor:
            results.append(self._model_class.from_mongo(doc))
        return results

    async def bulk_create(self, models: list[ModelType]) -> Sequence[ModelType]:
        """Create multiple documents in bulk.

        Args:
            models: List of model instances

        Returns:
            List of created model instances

        Example:
            >>> users = await repo.bulk_create([
            >>>     UserDocument(email="user1@example.com", name="User 1"),
            >>>     UserDocument(email="user2@example.com", name="User 2"),
            >>> ])
        """
        documents = [model.to_mongo() for model in models]
        result = await self._collection.insert_many(documents)

        # Fetch created documents
        created_docs = await self._collection.find(
            {"_id": {"$in": result.inserted_ids}}
        ).to_list(length=len(result.inserted_ids))

        return [self._model_class.from_mongo(doc) for doc in created_docs]

    async def bulk_delete(self, ids: list[str | ObjectId]) -> int:
        """Delete multiple documents by IDs.

        Args:
            ids: List of document ObjectIds

        Returns:
            Number of documents deleted

        Example:
            >>> deleted_count = await repo.bulk_delete(["id1", "id2", "id3"])
        """
        object_ids = [ObjectId(id) if isinstance(id, str) else id for id in ids]
        result = await self._collection.delete_many({"_id": {"$in": object_ids}})
        return result.deleted_count

    async def aggregate(self, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Run aggregation pipeline.

        Args:
            pipeline: MongoDB aggregation pipeline

        Returns:
            List of result documents

        Example:
            >>> pipeline = [
            >>>     {"$match": {"status": "active"}},
            >>>     {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            >>>     {"$sort": {"count": -1}}
            >>> ]
            >>> results = await repo.aggregate(pipeline)
        """
        cursor = self._collection.aggregate(pipeline)
        return await cursor.to_list(length=None)
