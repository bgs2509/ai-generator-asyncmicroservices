# FastAPI Lifespan Management

Lifespan hooks manage startup and shutdown for databases, caches, message brokers, and background tasks. Always use the `lifespan` parameter of `FastAPI` to encapsulate resource ownership.

## Template

```python
from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.config import Settings
from src.infrastructure.db import Database
from src.infrastructure.redis import RedisClient
from src.infrastructure.messaging import RabbitMQClient


def build_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db = Database(settings.database_url)
        redis = RedisClient(settings.redis_url)
        rabbit = RabbitMQClient(settings.rabbitmq_url)

        await db.connect()
        await redis.connect()
        await rabbit.connect()

        app.state.db = db
        app.state.redis = redis
        app.state.rabbit = rabbit

        try:
            yield
        finally:
            await rabbit.close()
            await redis.close()
            await db.disconnect()

    return lifespan
```

## Guidelines

- Initialise resources once during startup; reuse through dependency injection.
- Set timeouts when connecting to external systems to avoid hanging deployments.
- Register health checks after connections succeed to prevent false positives.
- Remove state from `app.state` during shutdown to avoid memory leaks in reload mode.

## Monitoring

- Log startup and shutdown with request/trace IDs from `logging_rules` patterns.
- Emit Prometheus gauges for connection pool size and availability.
- Alert when connection retries exceed defined thresholds.

## Failure Handling

- Wrap connection attempts in retries (exponential backoff) but fail fast after a limited number of attempts.
- If a critical dependency fails to start, raise and let the orchestrator restart the container; do not swallow the exception.

## Anti-Patterns

### ❌ Deprecated Lifecycle APIs

**Problem**: Using deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")` decorators instead of modern `lifespan` context manager

**Symptom**: Deprecation warnings in logs, breaking changes on FastAPI upgrades, inconsistent startup/shutdown behavior

**Impact**: Code breaks on FastAPI 0.109+, difficult to track resource lifecycle, no exception handling guarantees

**Example (WRONG)**:
```python
# ❌ ANTI-PATTERN: Deprecated @app.on_event() decorators
from fastapi import FastAPI
from src.infrastructure.db import Database
from src.infrastructure.redis import RedisClient

app = FastAPI()

# ❌ DEPRECATED since FastAPI 0.93, removed in 0.109+
@app.on_event("startup")
async def startup():
    """Initialize resources on startup."""
    app.state.db = Database(settings.database_url)
    await app.state.db.connect()

    app.state.redis = RedisClient(settings.redis_url)
    await app.state.redis.connect()

# ❌ DEPRECATED
@app.on_event("shutdown")
async def shutdown():
    """Clean up resources on shutdown."""
    await app.state.redis.close()
    await app.state.db.disconnect()

# ⚠️ Issues:
# - No exception handling guarantee (startup may fail silently)
# - Shutdown may not run if startup fails
# - Multiple @on_event decorators have undefined order
# - No context management (resources may leak)
```

**Why This Matters**:
- `@app.on_event()` is DEPRECATED since FastAPI 0.93 (June 2023)
- Removed entirely in FastAPI 0.109+ (breaking change)
- No guaranteed exception handling: startup can fail without cleanup
- Shutdown handlers may not run if startup fails midway
- Difficult to test: decorators run at app creation, not in tests
- No context manager guarantees: resources may not be released

**Solution (CORRECT)**:
```python
# ✅ CORRECT: Modern @asynccontextmanager lifespan
from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.config import Settings
from src.infrastructure.db import Database
from src.infrastructure.redis import RedisClient
import structlog

logger = structlog.get_logger()

def build_lifespan(settings: Settings):
    """
    Build lifespan context manager for FastAPI application.

    Args:
        settings: Application settings

    Returns:
        Async context manager for application lifecycle
    """
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """
        Manage application lifecycle: startup and shutdown.

        Handles resource initialization on startup and guaranteed cleanup
        on shutdown, even if startup fails.
        """
        # Startup phase
        logger.info("application_startup_initiated")

        db = Database(settings.database_url)
        redis = RedisClient(settings.redis_url)

        try:
            # Initialize resources with retry logic
            await db.connect()
            logger.info("database_connected")

            await redis.connect()
            logger.info("redis_connected")

            # Store in app state for dependency injection
            app.state.db = db
            app.state.redis = redis

            logger.info("application_startup_complete")

            # ✅ Yield: Application runs here
            yield

        finally:
            # ✅ Shutdown phase: GUARANTEED to run, even if startup fails
            logger.info("application_shutdown_initiated")

            # Close in reverse order
            if hasattr(app.state, "redis"):
                await redis.close()
                logger.info("redis_closed")

            if hasattr(app.state, "db"):
                await db.disconnect()
                logger.info("database_closed")

            logger.info("application_shutdown_complete")

    return lifespan

# Create app with lifespan
settings = Settings()
app = FastAPI(lifespan=build_lifespan(settings))
```

**Architecture Rule**:
> Use `@asynccontextmanager` lifespan for all resource management. Never use deprecated `@app.on_event()`. Lifespan guarantees cleanup runs even if startup fails.

**Migration Guide**:
```python
# Before (DEPRECATED):
@app.on_event("startup")
async def startup():
    app.state.resource = init_resource()

@app.on_event("shutdown")
async def shutdown():
    await app.state.resource.close()

# After (CORRECT):
@asynccontextmanager
async def lifespan(app: FastAPI):
    resource = init_resource()
    app.state.resource = resource
    try:
        yield
    finally:
        await resource.close()

app = FastAPI(lifespan=lifespan)
```

**Benefits of Lifespan**:
- ✅ Guaranteed cleanup: `finally` block always runs
- ✅ Exception safety: Cleanup runs even if startup fails
- ✅ Clear context: All lifecycle code in one place
- ✅ Testable: Can test lifespan independently
- ✅ Future-proof: Won't break on FastAPI upgrades

**Related Anti-Patterns**:
- No Graceful Shutdown → `docs/atomic/integrations/cross-service/graceful-shutdown.md#no-graceful-shutdown`

## Related Documents

- `docs/atomic/services/fastapi/dependency-injection.md`
- `docs/atomic/architecture/event-loop-management.md`
- `docs/atomic/services/fastapi/basic-setup.md`
