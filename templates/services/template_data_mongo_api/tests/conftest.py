"""Shared pytest fixtures for MongoDB Data Service tests.

Imports from shared testing utilities where applicable.
"""

import pytest
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

# Import shared fixtures if available
# from shared.testing.base_fixtures import mock_data_client


@pytest.fixture
def mock_mongo_collection() -> MagicMock:
    """Mock MongoDB collection for unit tests.

    Returns:
        Mocked collection with common operations
    """
    collection = MagicMock()

    # Mock find_one
    collection.find_one = AsyncMock(return_value={
        "_id": "507f1f77bcf86cd799439011",
        "name": "Test Document",
        "created_at": "2025-01-01T00:00:00Z",
    })

    # Mock insert_one
    mock_result = MagicMock()
    mock_result.inserted_id = "507f1f77bcf86cd799439011"
    collection.insert_one = AsyncMock(return_value=mock_result)

    # Mock update_one
    update_result = MagicMock()
    update_result.matched_count = 1
    update_result.modified_count = 1
    collection.update_one = AsyncMock(return_value=update_result)

    # Mock delete_one
    delete_result = MagicMock()
    delete_result.deleted_count = 1
    collection.delete_one = AsyncMock(return_value=delete_result)

    # Mock count_documents
    collection.count_documents = AsyncMock(return_value=10)

    # Mock find with cursor
    mock_cursor = MagicMock()
    mock_cursor.sort = MagicMock(return_value=mock_cursor)
    mock_cursor.skip = MagicMock(return_value=mock_cursor)
    mock_cursor.limit = MagicMock(return_value=mock_cursor)
    mock_cursor.__aiter__ = MagicMock(return_value=iter([
        {"_id": "id1", "name": "Doc 1"},
        {"_id": "id2", "name": "Doc 2"},
    ]))
    collection.find = MagicMock(return_value=mock_cursor)

    return collection


@pytest.fixture
def mock_mongo_database(mock_mongo_collection: MagicMock) -> MagicMock:
    """Mock MongoDB database for unit tests.

    Args:
        mock_mongo_collection: Mocked collection fixture

    Returns:
        Mocked database that returns the mock collection
    """
    database = MagicMock()
    database.__getitem__ = MagicMock(return_value=mock_mongo_collection)
    return database


@pytest.fixture
def test_client() -> TestClient:
    """Create test client for synchronous tests.

    Note: For async tests, use async_client instead.

    Returns:
        FastAPI TestClient instance
    """
    from src.main import app
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async test client for async tests.

    Yields:
        Async HTTP client for testing

    Example:
        >>> async def test_health(async_client):
        >>>     response = await async_client.get("/health")
        >>>     assert response.status_code == 200
    """
    from src.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def sample_document() -> dict:
    """Sample document data for testing.

    Returns:
        Dictionary with sample document fields
    """
    return {
        "name": "Test Document",
        "description": "A test document for unit tests",
        "status": "active",
        "tags": ["test", "sample"],
        "metadata": {
            "created_by": "test_user",
            "version": 1,
        },
    }
