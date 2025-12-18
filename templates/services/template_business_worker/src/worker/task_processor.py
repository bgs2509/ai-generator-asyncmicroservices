"""Task processor for handling RabbitMQ messages.

Routes messages to appropriate handlers based on event type.
"""
from typing import Any

from src.core.config import settings
from src.worker.handlers import example_handler

from shared.utils.logger import create_logger
from shared.http_clients import DataApiClient

logger = create_logger(__name__)


class TaskProcessor:
    """Processes incoming messages from RabbitMQ.

    Routes messages to handlers based on event_type field.
    """

    def __init__(self, data_client: DataApiClient):
        self.data_client = data_client
        self._handlers = {
            "example.created": example_handler.handle_example_created,
            "example.updated": example_handler.handle_example_updated,
            "example.deleted": example_handler.handle_example_deleted,
        }

    async def process(self, message: dict[str, Any]) -> None:
        """Process incoming message.

        Args:
            message: Decoded JSON message from RabbitMQ

        Raises:
            ValueError: If event_type is missing or unknown
        """
        event_type = message.get("event_type")

        if not event_type:
            logger.warning("Message missing event_type", extra={"message": message})
            raise ValueError("Message missing event_type")

        handler = self._handlers.get(event_type)

        if not handler:
            logger.warning(
                "Unknown event type",
                extra={"event_type": event_type, "known_types": list(self._handlers.keys())},
            )
            raise ValueError(f"Unknown event type: {event_type}")

        logger.info(
            "Processing event",
            extra={
                "event_type": event_type,
                "correlation_id": message.get("correlation_id"),
            },
        )

        await handler(message, self.data_client)

        logger.info(
            "Event processed successfully",
            extra={"event_type": event_type},
        )
