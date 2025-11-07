# Redis Connection Management

Use a single asynchronous Redis client per process, configured with connection pooling and constructed during service startup.

## Client Construction

```python
from redis.asyncio import Redis


def build_redis(url: str) -> Redis:
    return Redis.from_url(
        url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=100,
    )
```

- Instantiate the client inside FastAPI lifespan, Aiogram startup, or the worker `main()` coroutine.
- Store the client in application state (`app.state.redis`) or dispatcher startup context; never create clients per request.
- Close the client gracefully on shutdown to flush pending commands.

## Timeouts and Reliability

- Configure socket/connect timeouts to avoid hanging on network outages (`Redis.from_url(..., socket_timeout=5.0)`).
- Wrap initial connection attempts with retries (exponential backoff) but fail fast when the service cannot reach Redis.
- Use health checks that issue lightweight `PING` commands.

## Pool Sizing

- Size pools according to workload; start with `max_connections=100` for web services, lower for workers.
- Monitor pool usage via metrics to detect saturation and tune accordingly.

## Anti-Patterns

### ❌ Connection Pool Misuse

**Problem**: Creating new Redis connection pools per operation instead of reusing a single shared pool

**Symptom**: Redis connection leaks, "max clients reached" errors, degraded performance, memory growth

**Impact**: Redis server connection limit exhausted, service crashes, requires frequent restarts

**Example (WRONG)**:
```python
# ❌ ANTI-PATTERN: Creating new Redis client per operation
from redis.asyncio import Redis

async def cache_user_data(user_id: int, data: dict) -> None:
    """Cache user data in Redis."""
    # ⚠️ Creates NEW connection pool every call!
    redis = Redis.from_url(
        settings.redis_url,
        max_connections=100  # New pool with 100 connection slots!
    )
    await redis.setex(f"user:{user_id}", 3600, json.dumps(data))
    # ⚠️ NO .close() → connections never released!

# Called 50 times → 50 pools × 100 connections = 5000 potential connections!
```

**Why This Matters**:
- Each `Redis.from_url()` creates a NEW connection pool
- Pools are NOT garbage collected until explicitly closed
- Leaked pools accumulate → Redis `maxclients` limit reached
- Performance degradation: Connection handshakes on every operation
- Memory leak: Each pool holds internal buffers and state

**Solution (CORRECT)**:
```python
# ✅ CORRECT: Single shared Redis client with proper lifecycle
from redis.asyncio import Redis

# Shared client instance
_redis_client: Redis | None = None

def build_redis_client(url: str) -> Redis:
    """
    Build shared Redis client with connection pooling.

    Args:
        url: Redis connection URL

    Returns:
        Configured Redis client with connection pool
    """
    return Redis.from_url(
        url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=100,
        socket_timeout=5.0,
        socket_connect_timeout=1.0,
    )

async def close_redis_client() -> None:
    """Close Redis client and release all connections."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None
        logger.info("redis_client_closed", event="cleanup")

# In FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with Redis lifecycle."""
    global _redis_client
    _redis_client = build_redis_client(settings.redis_url)
    app.state.redis = _redis_client

    # Wait for connection to be ready
    await _redis_client.ping()
    logger.info("redis_connected", event="startup")

    try:
        yield
    finally:
        await close_redis_client()

# Usage: Inject client from app state
async def cache_user_data(
    user_id: int,
    data: dict,
    redis: Redis = Depends(get_redis)
) -> None:
    """
    Cache user data in Redis.

    Args:
        user_id: User identifier
        data: Data to cache
        redis: Shared Redis client (injected)
    """
    await redis.setex(
        f"user:{user_id}",
        3600,
        json.dumps(data)
    )
```

**Architecture Rule**:
> Redis clients MUST be instantiated once per process during startup, stored in app state, and closed during shutdown. Never create Redis clients per request or per operation.

**Monitoring**:
```bash
# Check Redis connection count (should be stable, < max_connections)
docker exec redis redis-cli CLIENT LIST | wc -l

# Monitor Redis memory usage
docker exec redis redis-cli INFO memory | grep used_memory_human

# Check for connection leaks (connections should not grow over time)
docker exec redis redis-cli INFO stats | grep total_connections_received
```

**Related Anti-Patterns**:
- HTTP Client Proliferation → `docs/atomic/integrations/http-communication/http-client-patterns.md#http-client-proliferation`
- Global FSM Storage Never Closed → `docs/atomic/services/aiogram/state-management.md#global-fsm-storage-never-closed`

## Observability

- Log connection lifecycle events (`redis_connected`, `redis_disconnected`) with request IDs from logging middleware.
- Emit metrics for command durations and error counts.

## Related Documents

- `docs/atomic/integrations/redis/key-naming-conventions.md`
- `docs/atomic/services/fastapi/dependency-injection.md`
- `docs/atomic/services/fastapi/lifespan-management.md`
