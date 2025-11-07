"""FastAPI application for PostgreSQL Data Service.

This service provides HTTP-based access to PostgreSQL database,
implementing the data layer for the Improved Hybrid Approach.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import init_db, close_db
from src.api.v1 import health
from shared.utils.logger import create_logger


logger = create_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} ({settings.APP_ENV})")
    await init_db()
    logger.info(f"{settings.APP_NAME} started successfully")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")
    await close_db()
    logger.info(f"{settings.APP_NAME} stopped")


# Create FastAPI application
app = FastAPI(
    title=f"{settings.APP_NAME} API",
    description="PostgreSQL Data API Service - HTTP-based database access layer",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Register routers
app.include_router(health.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint.

    Returns:
        Service information

    Example:
        GET /

        Response:
        {
          "service": "data_postgres_api",
          "version": "1.0.0",
          "environment": "development"
        }
    """
    return {
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.APP_ENV,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
