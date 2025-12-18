"""Tests for task processor."""
import pytest

from src.worker.task_processor import TaskProcessor


@pytest.mark.asyncio
async def test_process_valid_message(task_processor, sample_message):
    """Test processing a valid message."""
    await task_processor.process(sample_message)
    # Should complete without raising


@pytest.mark.asyncio
async def test_process_missing_event_type(task_processor):
    """Test that missing event_type raises ValueError."""
    message = {"entity_id": "123"}

    with pytest.raises(ValueError, match="missing event_type"):
        await task_processor.process(message)


@pytest.mark.asyncio
async def test_process_unknown_event_type(task_processor):
    """Test that unknown event_type raises ValueError."""
    message = {
        "event_type": "unknown.event",
        "entity_id": "123",
    }

    with pytest.raises(ValueError, match="Unknown event type"):
        await task_processor.process(message)


@pytest.mark.asyncio
async def test_process_example_updated(task_processor):
    """Test processing example.updated event."""
    message = {
        "event_type": "example.updated",
        "entity_id": "123",
        "changes": {"name": "New Name"},
    }

    await task_processor.process(message)
    # Should complete without raising


@pytest.mark.asyncio
async def test_process_example_deleted(task_processor):
    """Test processing example.deleted event."""
    message = {
        "event_type": "example.deleted",
        "entity_id": "123",
    }

    await task_processor.process(message)
    # Should complete without raising
