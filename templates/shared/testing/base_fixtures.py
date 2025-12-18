"""Base pytest fixtures for all service templates.

Import and use in service-specific conftest.py:

    from shared.testing.base_fixtures import *
"""
import pytest


@pytest.fixture
def mock_data_client(mocker):
    """Mock DataApiClient for unit tests."""
    mock = mocker.AsyncMock()
    mock.get.return_value = {"id": "123", "name": "Test"}
    mock.post.return_value = {"id": "456", "name": "Created"}
    mock.put.return_value = {"id": "456", "name": "Updated"}
    mock.delete.return_value = None
    return mock


@pytest.fixture
def mock_rabbitmq_publisher(mocker):
    """Mock RabbitMQPublisher for unit tests."""
    mock = mocker.AsyncMock()
    mock.publish.return_value = None
    return mock


@pytest.fixture
def mock_rabbitmq_consumer(mocker):
    """Mock RabbitMQConsumer for unit tests."""
    mock = mocker.AsyncMock()
    return mock
