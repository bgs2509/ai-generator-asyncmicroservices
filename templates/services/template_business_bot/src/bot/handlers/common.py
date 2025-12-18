"""Common message handlers.

Handles messages that don't match specific commands.
"""
from aiogram import Router
from aiogram.types import Message

from shared.utils.logger import create_logger

logger = create_logger(__name__)

router = Router(name="common")


@router.message()
async def handle_unknown(message: Message) -> None:
    """Handle unknown messages.

    This handler catches all messages that don't match other handlers.
    Place this router LAST in the dispatcher.
    """
    logger.debug(
        "Unknown message received",
        extra={
            "text": message.text[:100] if message.text else None,
            "content_type": message.content_type,
        },
    )

    await message.answer(
        "I don't understand this message.\n"
        "Use /help to see available commands."
    )
