"""Tests for bot handlers."""
import pytest

from src.bot.handlers.start import cmd_start
from src.bot.handlers.help import cmd_help


@pytest.mark.asyncio
async def test_cmd_start(mock_message):
    """Test /start command handler."""
    await cmd_start(mock_message)

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    assert "Welcome" in call_args[0][0]
    assert mock_message.from_user.first_name in call_args[0][0]


@pytest.mark.asyncio
async def test_cmd_help(mock_message):
    """Test /help command handler."""
    await cmd_help(mock_message)

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args
    assert "Available Commands" in call_args[0][0]
    assert "/start" in call_args[0][0]
    assert "/help" in call_args[0][0]
