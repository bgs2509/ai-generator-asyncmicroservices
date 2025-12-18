"""Base event classes for RabbitMQ messaging.

All domain events should inherit from BaseEvent.

Usage:
    from shared.events import BaseEvent, EventMetadata

    class UserCreatedEvent(BaseEvent):
        user_id: str
        email: str

    event = UserCreatedEvent(
        metadata=EventMetadata(event_type="user.created", source="user-api"),
        user_id="123",
        email="test@example.com",
    )
"""
from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class EventMetadata(BaseModel):
    """Standard event metadata."""

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_service: str = Field(alias="source")
    correlation_id: str | None = None
    version: str = "1.0"


class BaseEvent(BaseModel):
    """Base class for all domain events."""

    metadata: EventMetadata

    class Config:
        frozen = True

    def to_bytes(self) -> bytes:
        """Serialize for RabbitMQ."""
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def from_bytes(cls, body: bytes) -> "BaseEvent":
        """Deserialize from RabbitMQ."""
        return cls.model_validate_json(body)
