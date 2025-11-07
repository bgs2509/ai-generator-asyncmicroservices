"""Health check endpoints for monitoring and orchestration.

Provides liveness and readiness probes for Kubernetes/Docker.
"""

from fastapi import APIRouter

from src.core.database import check_database_connection
from src.schemas.base import HealthResponse
from shared.utils.logger import create_logger


logger = create_logger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check (liveness probe).

    Returns 200 if service is running.
    Use this for Kubernetes liveness probe.

    Returns:
        Health status

    Example:
        GET /health

        Response:
        {
          "status": "healthy",
          "version": "1.0.0",
          "checks": {}
        }
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        checks={},
    )


@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    """Readiness check (readiness probe).

    Verifies connectivity to all dependencies:
    - PostgreSQL database connection

    Use this for Kubernetes readiness probe.

    Returns:
        Health status with dependency checks

    Raises:
        HTTPException: 503 if any dependency is unhealthy

    Example:
        GET /health/ready

        Response (healthy):
        {
          "status": "healthy",
          "version": "1.0.0",
          "checks": {
            "database": "healthy"
          }
        }

        Response (unhealthy):
        {
          "status": "unhealthy",
          "version": "1.0.0",
          "checks": {
            "database": "unhealthy"
          }
        }
    """
    checks = {}
    all_healthy = True

    # Check PostgreSQL database
    try:
        is_connected = await check_database_connection()
        checks["database"] = "healthy" if is_connected else "unhealthy"
        if not is_connected:
            all_healthy = False
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        checks["database"] = "unhealthy"
        all_healthy = False

    return HealthResponse(
        status="healthy" if all_healthy else "unhealthy",
        version="1.0.0",
        checks=checks,
    )
