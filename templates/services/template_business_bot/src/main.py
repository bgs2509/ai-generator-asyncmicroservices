"""Telegram Bot Entry Point.

Uses shared infrastructure - NO code duplication.
"""
import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.config import settings
from src.bot.handlers import start, help, common
from src.bot.middlewares.logging import LoggingMiddleware

# IMPORT FROM SHARED - NOT DUPLICATED
from shared.utils.logger import create_logger
from shared.http_clients import DataApiClient
from shared.rabbitmq import RabbitMQPublisher

logger = create_logger(__name__)


@asynccontextmanager
async def lifespan(bot: Bot, dp: Dispatcher):
    """Manage bot lifecycle."""
    logger.info("Bot starting up...")

    # Use shared HTTP client
    data_client = DataApiClient(settings.data_api_url)
    await data_client.connect()
    dp["data_client"] = data_client

    # Use shared RabbitMQ publisher
    publisher = RabbitMQPublisher(settings.rabbitmq_url)
    await publisher.connect()
    dp["publisher"] = publisher

    yield

    logger.info("Bot shutting down...")
    await publisher.close()
    await data_client.close()
    await bot.session.close()


async def main():
    """Initialize and run the bot."""
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.message.middleware(LoggingMiddleware())

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(common.router)

    async with lifespan(bot, dp):
        bot_info = await bot.get_me()
        logger.info(f"Bot @{bot_info.username} started")
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
