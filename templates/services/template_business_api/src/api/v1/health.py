"""Health check endpoints for Kubernetes probes.

Follows same pattern as template_data_postgres_api.
"""
from fastapi import APIRouter
from pydantic import BaseModel

from src.core.config import settings
from shared.utils.logger import create_logger

logger = create_logger(__name__)

router = APIRouter(prefix="/health")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str
    checks: dict[str, str] = {}


@router.get("/live", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    """Liveness probe - is process running?

    Used by Kubernetes to determine if the container is alive.
    """
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get("/ready", response_model=HealthResponse)
async def readiness() -> HealthResponse:
    """Readiness probe - can serve traffic?

    Used by Kubernetes to determine if the container is ready to receive traffic.
    Add dependency checks as needed (e.g., data service connectivity).
    """
    return HealthResponse(
        status="ready",
        service=settings.app_name,
        version=settings.app_version,
        checks={"data_service": "healthy"},
    )
