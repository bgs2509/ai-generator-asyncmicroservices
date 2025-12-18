"""FastAPI Business API Entry Point.

Uses shared infrastructure - NO code duplication.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.core.config import settings
from src.api.v1 import health

# IMPORT FROM SHARED - NOT DUPLICATED
from shared.utils.logger import create_logger
from shared.middleware import RequestIdMiddleware
from shared.http_clients import DataApiClient
from shared.rabbitmq import RabbitMQPublisher

logger = create_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    logger.info("API starting up...")

    # Use shared infrastructure
    data_client = DataApiClient(settings.data_api_url)
    await data_client.connect()
    app.state.data_client = data_client

    publisher = RabbitMQPublisher(settings.rabbitmq_url)
    await publisher.connect()
    app.state.publisher = publisher

    yield

    logger.info("API shutting down...")
    await publisher.close()
    await data_client.close()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        description="FastAPI Business API Service",
        version=settings.app_version,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url="/api/redoc" if settings.debug else None,
        openapi_url="/api/openapi.json" if settings.debug else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    # CORS Configuration
    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Use shared middleware - NOT DUPLICATED
    app.add_middleware(RequestIdMiddleware)

    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["Health"])

    # TODO: Add your business routers here
    # from src.api.v1 import users
    # app.include_router(users.router, prefix="/api/v1", tags=["Users"])

    logger.info("FastAPI application created")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_config=None,  # We use custom logging
    )
