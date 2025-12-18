"""Example event handlers.

Demonstrates how to handle different event types.
Replace with your business-specific handlers.
"""
from typing import Any

from shared.utils.logger import create_logger
from shared.http_clients import DataApiClient

logger = create_logger(__name__)


async def handle_example_created(
    message: dict[str, Any],
    data_client: DataApiClient,
) -> None:
    """Handle example.created event.

    Args:
        message: Event payload with entity data
        data_client: HTTP client for Data Service
    """
    entity_id = message.get("entity_id")
    logger.info("Handling example.created", extra={"entity_id": entity_id})

    # Example: Fetch additional data from Data Service
    # entity = await data_client.get(f"/examples/{entity_id}")

    # Example: Perform business logic
    # await send_notification(entity)
    # await update_search_index(entity)

    logger.info("example.created processed", extra={"entity_id": entity_id})


async def handle_example_updated(
    message: dict[str, Any],
    data_client: DataApiClient,
) -> None:
    """Handle example.updated event.

    Args:
        message: Event payload with updated fields
        data_client: HTTP client for Data Service
    """
    entity_id = message.get("entity_id")
    changes = message.get("changes", {})
    logger.info(
        "Handling example.updated",
        extra={"entity_id": entity_id, "changed_fields": list(changes.keys())},
    )

    # Example: React to specific field changes
    # if "status" in changes:
    #     await notify_status_change(entity_id, changes["status"])

    logger.info("example.updated processed", extra={"entity_id": entity_id})


async def handle_example_deleted(
    message: dict[str, Any],
    data_client: DataApiClient,
) -> None:
    """Handle example.deleted event.

    Args:
        message: Event payload with deleted entity info
        data_client: HTTP client for Data Service
    """
    entity_id = message.get("entity_id")
    logger.info("Handling example.deleted", extra={"entity_id": entity_id})

    # Example: Cleanup related resources
    # await remove_from_search_index(entity_id)
    # await cleanup_files(entity_id)

    logger.info("example.deleted processed", extra={"entity_id": entity_id})
