# Graceful Shutdown

Coordinate shutdown across services to avoid data loss and user-visible errors.

## Checklist

1. Signal receipt (`SIGTERM`, `SIGINT`).
2. Stop accepting new traffic (update readiness endpoints, drain load balancers).
3. Finish in-flight requests/messages or persist state for later recovery.
4. Close external connections (database, Redis, RabbitMQ) cleanly.
5. Log shutdown completion with request IDs for traceability.

## FastAPI

- Use lifespan shutdown hooks to close connection pools and flush background tasks.
- Return 503 from readiness checks while shutting down to reroute traffic.

## Aiogram & Workers

- Use `asyncio.Event` and signal handlers to cancel long-running tasks.
- Acknowledge or requeue messages before closing broker channels.

## Anti-Patterns

### ❌ No Graceful Shutdown Implementation

**Problem**: Service terminates abruptly without handling SIGTERM/SIGINT signals, causing data loss and user-visible errors

**Symptom**: 500 errors during deployment, messages lost on restart, partial data writes, "connection reset by peer" errors

**Impact**: User-facing failures, data inconsistency, broken user workflows, poor deployment experience

**Example (WRONG)**:
```python
# ❌ ANTI-PATTERN: No signal handling for graceful shutdown
import asyncio
from aiogram import Bot, Dispatcher

async def main() -> None:
    """Main bot entry point."""
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    # Register handlers
    dp.include_router(router)

    # ⚠️ Blocks forever, ignores SIGTERM from orchestrator!
    await dp.start_polling(bot)

    # ⚠️ Code below NEVER runs during normal shutdown
    await bot.session.close()
    await storage.close()

if __name__ == "__main__":
    asyncio.run(main())

# When Kubernetes/Docker sends SIGTERM:
# - Polling continues for grace period (30s default)
# - SIGKILL terminates process forcefully
# - In-flight messages lost
# - Connections not closed
# - No cleanup ran
```

**Why This Matters**:
- Orchestrators (Docker, Kubernetes) send SIGTERM on shutdown
- Without signal handling, service ignores SIGTERM for 30s grace period
- SIGKILL forcefully terminates → in-flight operations lost
- Database transactions not committed → data loss
- Connections not closed → resource leaks on server
- User sees 500 errors during rolling deployments
- Violates Twelve-Factor App principles (graceful termination)

**Solution (CORRECT)**:
```python
# ✅ CORRECT: Proper signal handling for graceful shutdown
from __future__ import annotations

import signal
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
import structlog

logger = structlog.get_logger()

# Global shutdown event
shutdown_event = asyncio.Event()

def handle_signal(signum: int, frame) -> None:
    """
    Handle shutdown signals (SIGTERM, SIGINT).

    Args:
        signum: Signal number
        frame: Stack frame
    """
    signal_name = signal.Signals(signum).name
    logger.info("shutdown_signal_received", signal=signal_name)
    shutdown_event.set()

async def main() -> None:
    """
    Main bot entry point with graceful shutdown.

    Handles SIGTERM/SIGINT signals and ensures clean shutdown:
    1. Stop accepting new messages
    2. Finish processing in-flight messages
    3. Close all connections
    4. Exit cleanly
    """
    # Register signal handlers BEFORE starting bot
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    bot = Bot(token=settings.bot_token)
    storage = RedisStorage.from_url(settings.redis_url)
    dp = Dispatcher(storage=storage)

    # Register handlers
    dp.include_router(router)

    logger.info("bot_startup_initiated")

    try:
        # Create polling task (doesn't block)
        polling_task = asyncio.create_task(dp.start_polling(bot))

        logger.info("bot_polling_started")

        # ✅ Wait for shutdown signal
        await shutdown_event.wait()

        logger.info("bot_shutdown_initiated", reason="signal")

        # ✅ Cancel polling gracefully
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            logger.info("polling_cancelled")

    except Exception as e:
        logger.exception("bot_error", error=str(e))
        raise

    finally:
        # ✅ GUARANTEED cleanup: Always runs
        logger.info("bot_cleanup_started")

        # Close in reverse order of initialization
        await storage.close()
        logger.info("storage_closed")

        await bot.session.close()
        logger.info("bot_session_closed")

        logger.info("bot_shutdown_complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("bot_interrupted_by_user")
```

**Architecture Rule**:
> All long-running services (bots, workers, APIs) MUST handle SIGTERM/SIGINT signals to enable graceful shutdown. Services MUST finish in-flight operations and close resources before exiting.

**Shutdown Sequence Best Practices**:
1. **Receive signal** → Set shutdown event, log signal received
2. **Stop accepting new work** → Cancel polling/listening tasks
3. **Finish in-flight work** → Wait for tasks with timeout (5-10s)
4. **Close connections** → Database, Redis, HTTP clients (reverse order)
5. **Log completion** → Final log message before exit
6. **Exit cleanly** → Return 0 exit code

**For FastAPI Services**:
```python
# FastAPI lifespan handles shutdown automatically
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # ✅ Shutdown runs on SIGTERM automatically
    await db.disconnect()
```

**Testing Graceful Shutdown**:
```python
import subprocess
import signal
import time

def test_graceful_shutdown():
    """Test bot shuts down gracefully on SIGTERM."""
    # Start bot in subprocess
    proc = subprocess.Popen(["python", "-m", "src.main"])

    time.sleep(2)  # Let bot start

    # Send SIGTERM (like orchestrator does)
    proc.send_signal(signal.SIGTERM)

    # Wait for clean exit
    return_code = proc.wait(timeout=10)

    # ✅ Should exit cleanly (code 0)
    assert return_code == 0
```

**Monitoring**:
```bash
# Check if service handles SIGTERM (should exit with code 0)
docker stop --time=10 service_name
echo $?  # Should be 0

# Monitor shutdown duration (should be < grace period)
time docker stop service_name
```

**Related Anti-Patterns**:
- Deprecated Lifecycle APIs → `docs/atomic/services/fastapi/lifespan-management.md#deprecated-lifecycle-apis`
- Global FSM Storage Never Closed → `docs/atomic/services/aiogram/state-management.md#global-fsm-storage-never-closed`

## Testing

- Simulate shutdown in integration tests (send `SIGTERM` to subprocess) and ensure no messages are lost.
- Measure shutdown duration and keep it below orchestrator grace periods (30s default).
- Verify all connections are closed (no FIN_WAIT/TIME_WAIT connection accumulation).

## Related Documents

- `docs/atomic/architecture/event-loop-management.md`
- `docs/atomic/services/asyncio-workers/signal-handling.md`
- `docs/atomic/services/fastapi/lifespan-management.md`
