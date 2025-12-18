"""Logging middleware for Aiogram.

Logs all incoming updates with user information.
Uses shared logger for consistent JSON logging.
"""
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from shared.utils.logger import create_logger
from shared.utils.request_id import generate_request_id, set_request_id

logger = create_logger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware that logs all incoming updates.

    - Generates unique request ID for each update
    - Logs user information and update type
    - Measures processing time
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """Process update with logging."""
        # Generate and set request ID for this update
        request_id = generate_request_id()
        set_request_id(request_id)

        # Extract user info if available
        user_id = None
        username = None
        update_type = "unknown"

        if isinstance(event, Update):
            if event.message:
                update_type = "message"
                if event.message.from_user:
                    user_id = event.message.from_user.id
                    username = event.message.from_user.username
            elif event.callback_query:
                update_type = "callback_query"
                if event.callback_query.from_user:
                    user_id = event.callback_query.from_user.id
                    username = event.callback_query.from_user.username

        logger.info(
            "Update received",
            extra={
                "request_id": request_id,
                "update_type": update_type,
                "user_id": user_id,
                "username": username,
            },
        )

        # Process the update
        result = await handler(event, data)

        logger.info(
            "Update processed",
            extra={
                "request_id": request_id,
                "update_type": update_type,
            },
        )

        return result
