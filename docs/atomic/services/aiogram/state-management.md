# State Management

Aiogram's FSM helps track conversational state. Use it sparingly and persist state externally when resilience is required.

## Setup

```python
from __future__ import annotations

from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram import Dispatcher


class PhotoFlow(StatesGroup):
    waiting_for_caption = State()


def configure_state(dp: Dispatcher, redis_url: str) -> None:
    storage = RedisStorage.from_url(redis_url)
    dp.storage = storage
```

## Usage

```python
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from src.bot.states import PhotoFlow

router = Router()


@router.message(F.photo)
async def ask_for_caption(message: Message, state: FSMContext) -> None:
    await state.set_state(PhotoFlow.waiting_for_caption)
    await message.answer("Please provide a caption.")


@router.message(PhotoFlow.waiting_for_caption)
async def receive_caption(message: Message, state: FSMContext) -> None:
    caption = message.text or ""
    await state.clear()
    await message.answer(f"Received caption: {caption}")
```

## Guidelines

- Store minimal data in the FSM; large payloads belong in Redis or database services.
- Clean up state transitions (`await state.clear()`) to prevent stale sessions.
- Combine state with idempotency checks to avoid repeated processing after restarts.
- Persist FSM storage in Redis or database to survive restarts; in-memory storage is acceptable only for development.

## Anti-Patterns

### ❌ Global FSM Storage Never Closed

**Problem**: Memory leaks and connection pool exhaustion from unclosed Redis connections in FSM storage

**Symptom**: Bot crashes after 3-7 days uptime with "too many open files" error or memory exhaustion

**Impact**: Production crashes, requires frequent restarts, data loss on abrupt termination

**Example (WRONG)**:
```python
# ❌ ANTI-PATTERN: Global storage that is never closed
# src/api/handlers/poll.py
from aiogram.fsm.storage.redis import RedisStorage

_fsm_storage: RedisStorage | None = None

def get_fsm_storage() -> RedisStorage:
    """Get or create FSM storage instance for state checking."""
    global _fsm_storage
    if _fsm_storage is None:
        _fsm_storage = RedisStorage.from_url(settings.redis_url)
    return _fsm_storage  # ⚠️ NEVER CLOSED → Memory and connection leaks!

# Usage in handler
async def check_poll_handler(message: Message) -> None:
    storage = get_fsm_storage()  # Creates new connections indefinitely
    state_data = await storage.get_data(...)
```

**Why This Matters**:
- Redis connection pool is NEVER closed, accumulating over bot lifetime
- Each connection holds memory, file descriptors, and network sockets
- Over days/weeks → memory exhaustion → "too many open files" → crash
- No graceful shutdown means in-flight state updates may be lost

**Solution (CORRECT)**:
```python
# ✅ CORRECT: Proper lifecycle management with cleanup
from aiogram.fsm.storage.redis import RedisStorage

_fsm_storage: RedisStorage | None = None

def get_fsm_storage() -> RedisStorage:
    """
    Get shared FSM storage instance.

    Returns:
        Shared FSM storage instance for state management
    """
    global _fsm_storage
    if _fsm_storage is None:
        _fsm_storage = RedisStorage.from_url(settings.redis_url)
    return _fsm_storage

async def close_fsm_storage() -> None:
    """Close FSM storage and release resources."""
    global _fsm_storage
    if _fsm_storage is not None:
        await _fsm_storage.close()
        _fsm_storage = None
        logger.info("fsm_storage_closed", event="cleanup")

# In main bot entry point
async def main() -> None:
    """Main bot entry point with proper cleanup."""
    try:
        await dp.start_polling(bot)
    finally:
        # ✅ Proper cleanup on shutdown
        await close_fsm_storage()
        await bot.session.close()
        await storage.close()
```

**Architecture Rule**:
> All stateful resources (Redis clients, FSM storage, HTTP clients, database connections) MUST have explicit cleanup in application lifecycle hooks.

**Monitoring**:
```bash
# Monitor memory growth over time
docker stats --no-stream bot_service

# Check file descriptor leak (should be < 100 for healthy bot)
docker exec bot_service sh -c 'ls /proc/$$/fd | wc -l'

# Monitor Redis connections (should be stable, not growing)
docker exec redis redis-cli CLIENT LIST | wc -l
```

**Related Anti-Patterns**:
- HTTP Client Proliferation → `docs/atomic/integrations/http-communication/http-client-patterns.md#http-client-proliferation`
- Connection Pool Misuse → `docs/atomic/integrations/redis/connection-management.md#connection-pool-misuse`

## Related Documents

- `docs/atomic/services/aiogram/dependency-injection.md`
- `docs/atomic/integrations/redis/key-naming-conventions.md`
- `docs/atomic/integrations/cross-service/graceful-shutdown.md`
