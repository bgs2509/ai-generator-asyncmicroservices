"""Test fixtures - imports from shared.

Import shared fixtures for consistent testing across all services.
"""
import pytest
from fastapi.testclient import TestClient

# Import shared fixtures - NO DUPLICATION
from shared.testing.base_fixtures import (
    mock_data_client,
    mock_rabbitmq_publisher,
)

# Re-export for pytest discovery
__all__ = ["mock_data_client", "mock_rabbitmq_publisher"]


@pytest.fixture
def client():
    """Create test client for FastAPI application."""
    from src.main import app
    return TestClient(app)


@pytest.fixture
def async_client():
    """Create async test client for FastAPI application.

    Usage:
        @pytest.mark.asyncio
        async def test_async_endpoint(async_client):
            async with async_client as client:
                response = await client.get("/api/v1/health/live")
    """
    from httpx import ASGITransport, AsyncClient
    from src.main import app

    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )
