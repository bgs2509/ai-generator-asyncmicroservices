"""Base Pydantic models for MongoDB documents.

Provides base model classes with ObjectId handling and common fields.
"""

from datetime import datetime
from typing import Annotated, Any

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.functional_validators import BeforeValidator


def validate_object_id(v: Any) -> ObjectId:
    """Validate and convert to ObjectId.

    Args:
        v: Value to convert (str or ObjectId)

    Returns:
        ObjectId instance

    Raises:
        ValueError: If value is not a valid ObjectId
    """
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError(f"Invalid ObjectId: {v}")


# Type annotation for ObjectId fields
PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]


class MongoModel(BaseModel):
    """Base model for MongoDB documents.

    All document models should inherit from this class.
    Provides automatic handling of MongoDB ObjectId.

    Example:
        >>> class UserDocument(MongoModel):
        >>>     email: str
        >>>     name: str
        >>>
        >>> user = UserDocument(id="507f1f77bcf86cd799439011", email="test@example.com", name="Test")
        >>> print(user.id)  # ObjectId('507f1f77bcf86cd799439011')
    """

    id: PyObjectId | None = Field(default=None, alias="_id")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        from_attributes=True,
    )

    def to_mongo(self) -> dict[str, Any]:
        """Convert model to MongoDB document format.

        Returns:
            Dictionary suitable for MongoDB insertion

        Example:
            >>> user = UserDocument(email="test@example.com", name="Test")
            >>> doc = user.to_mongo()
            >>> await collection.insert_one(doc)
        """
        data = self.model_dump(by_alias=True, exclude_none=True)
        # Remove _id if None (let MongoDB generate it)
        if "_id" not in data or data["_id"] is None:
            data.pop("_id", None)
        return data

    @classmethod
    def from_mongo(cls, data: dict[str, Any]) -> "MongoModel":
        """Create model from MongoDB document.

        Args:
            data: MongoDB document dictionary

        Returns:
            Model instance

        Example:
            >>> doc = await collection.find_one({"email": "test@example.com"})
            >>> user = UserDocument.from_mongo(doc)
        """
        if data is None:
            raise ValueError("Cannot create model from None")
        return cls.model_validate(data)


class TimestampedMongoModel(MongoModel):
    """Base model with automatic timestamps.

    Includes created_at and updated_at fields.
    """

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp.

        Call this before saving updates.
        """
        self.updated_at = datetime.utcnow()
