"""Test fixtures - imports from shared.

Import shared fixtures for consistent testing across all services.
"""
import pytest

# Import shared fixtures - NO DUPLICATION
from shared.testing.base_fixtures import (
    mock_data_client,
    mock_rabbitmq_publisher,
)

# Re-export for pytest discovery
__all__ = ["mock_data_client", "mock_rabbitmq_publisher"]


# Bot-specific fixtures only
@pytest.fixture
def mock_bot(mocker):
    """Mock Aiogram Bot instance."""
    mock = mocker.AsyncMock()
    mock.get_me.return_value = mocker.MagicMock(username="test_bot")
    return mock


@pytest.fixture
def mock_dispatcher(mocker):
    """Mock Aiogram Dispatcher."""
    return mocker.MagicMock()


@pytest.fixture
def mock_message(mocker):
    """Mock Aiogram Message object."""
    message = mocker.AsyncMock()
    message.from_user = mocker.MagicMock(
        id=123456789,
        username="test_user",
        first_name="Test",
        last_name="User",
    )
    message.text = "/start"
    message.answer = mocker.AsyncMock()
    return message
