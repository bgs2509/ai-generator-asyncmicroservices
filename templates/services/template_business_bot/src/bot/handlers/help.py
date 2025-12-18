"""Help command handler.

Displays available commands and usage information.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from shared.utils.logger import create_logger

logger = create_logger(__name__)

router = Router(name="help")


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help command.

    Displays available commands and their descriptions.
    """
    logger.info("Help command received")

    help_text = (
        "<b>Available Commands:</b>\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "<i>Add your custom commands here.</i>"
    )

    await message.answer(help_text)
