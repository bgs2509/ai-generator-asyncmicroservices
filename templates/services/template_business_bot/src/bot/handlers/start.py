"""Start command handler.

Handles /start command and user onboarding flow.
"""
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from shared.utils.logger import create_logger

logger = create_logger(__name__)

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start command.

    This is the entry point for new users.
    Implement your onboarding logic here.
    """
    user = message.from_user
    logger.info(
        "Start command received",
        extra={
            "user_id": user.id if user else None,
            "username": user.username if user else None,
        },
    )

    await message.answer(
        f"Welcome, <b>{user.first_name if user else 'User'}</b>!\n\n"
        "This is a template bot. Customize this message for your business.\n\n"
        "Use /help to see available commands."
    )
