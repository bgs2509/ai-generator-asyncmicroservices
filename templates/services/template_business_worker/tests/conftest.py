"""Test fixtures - imports from shared.

Import shared fixtures for consistent testing across all services.
"""
import pytest

# Import shared fixtures - NO DUPLICATION
from shared.testing.base_fixtures import (
    mock_data_client,
    mock_rabbitmq_consumer,
)

# Re-export for pytest discovery
__all__ = ["mock_data_client", "mock_rabbitmq_consumer"]


# Worker-specific fixtures only
@pytest.fixture
def sample_message():
    """Sample RabbitMQ message for testing."""
    return {
        "event_type": "example.created",
        "entity_id": "123",
        "correlation_id": "test-correlation-id",
        "timestamp": "2025-01-01T00:00:00Z",
    }


@pytest.fixture
def task_processor(mock_data_client):
    """Create TaskProcessor with mocked dependencies."""
    from src.worker.task_processor import TaskProcessor
    return TaskProcessor(data_client=mock_data_client)
