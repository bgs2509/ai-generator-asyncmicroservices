"""AsyncIO Background Worker Entry Point.

Uses shared infrastructure - NO code duplication.
"""
import asyncio
import signal
from contextlib import asynccontextmanager

from src.core.config import settings
from src.worker.task_processor import TaskProcessor

# IMPORT FROM SHARED - NOT DUPLICATED
from shared.utils.logger import create_logger
from shared.http_clients import DataApiClient
from shared.rabbitmq import RabbitMQConsumer

logger = create_logger(__name__)


class GracefulShutdown:
    """Handles graceful shutdown signals."""

    def __init__(self):
        self.shutdown_event = asyncio.Event()

    def trigger_shutdown(self, signum: int, frame) -> None:
        logger.info("Received shutdown signal", extra={"signal": signum})
        self.shutdown_event.set()


@asynccontextmanager
async def lifespan():
    """Manage worker lifecycle."""
    logger.info("Worker starting up...", extra={"queue": settings.queue_name})

    # Use shared infrastructure
    consumer = RabbitMQConsumer(
        settings.rabbitmq_url,
        prefetch_count=settings.prefetch_count,
    )
    await consumer.connect()

    data_client = DataApiClient(settings.data_api_url)
    await data_client.connect()

    yield {"consumer": consumer, "data_client": data_client}

    logger.info("Worker shutting down...")
    await data_client.close()
    await consumer.close()


async def main() -> None:
    """Initialize and run the worker."""
    logger.info("Worker initializing...", extra={"version": settings.app_version})

    shutdown = GracefulShutdown()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: shutdown.trigger_shutdown(s, None)
        )

    async with lifespan() as deps:
        processor = TaskProcessor(data_client=deps["data_client"])
        consumer = deps["consumer"]

        consume_task = asyncio.create_task(
            consumer.consume(
                queue_name=settings.queue_name,
                callback=processor.process,
            )
        )

        logger.info("Worker started, consuming messages...")
        await shutdown.shutdown_event.wait()

        consume_task.cancel()
        try:
            await consume_task
        except asyncio.CancelledError:
            pass

    logger.info("Worker shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
