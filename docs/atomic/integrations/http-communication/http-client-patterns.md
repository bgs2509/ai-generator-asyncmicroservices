# HTTP Client Patterns

Use `httpx.AsyncClient` as the standard HTTP client for inter-service calls.

## Construction

```python
from httpx import AsyncClient, Limits, Timeout


def build_client(settings):
    return AsyncClient(
        timeout=Timeout(5.0, connect=1.0),
        limits=Limits(max_connections=200, max_keepalive_connections=100),
        headers={"User-Agent": settings.service_name},
    )
```

- Create the client once per process (FastAPI lifespan, worker bootstrap) and reuse it for all requests.
- Close the client during shutdown to release sockets.

## Middleware

- Add logging middleware to capture method, URL, status, and duration.
- Inject tracing headers (`traceparent`, `tracestate`) per request.

## Resilience

- Wrap calls with retries/backoff (see `timeout-retry-patterns.md`).
- Detect unhealthy dependencies using circuit breakers and fallback behaviour.

## Anti-Patterns

### ❌ HTTP Client Proliferation

**Problem**: Creating multiple `httpx.AsyncClient` instances instead of reusing a single shared client with connection pooling

**Symptom**: Connection pool exhaustion, "connection reset by peer" errors, high latency, resource leaks

**Impact**: Service degradation under load, connection limits reached, memory leaks from unclosed clients

**Example (WRONG)**:
```python
# ❌ ANTI-PATTERN: Creating new client per request
async def fetch_user_data(user_id: int) -> dict:
    """Fetch user data from data service."""
    # ⚠️ Creates NEW client with NEW connection pool every call!
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://finance_user_api:8000/users/{user_id}"
        )
        return response.json()

# Called 100 times → 100 separate connection pools → resource exhaustion!
```

**Why This Matters**:
- Each `AsyncClient()` creates its own connection pool (default 100 connections)
- Connection pools are NOT shared between client instances
- Creating clients per request → no connection reuse → TCP handshake overhead
- Unclosed clients leak file descriptors and memory
- Under load (1000s requests/sec) → system connection limit reached

**Solution (CORRECT)**:
```python
# ✅ CORRECT: Single shared client with connection pooling
from httpx import AsyncClient, Limits, Timeout
from contextlib import asynccontextmanager

# Shared client instance (created in lifespan)
_http_client: AsyncClient | None = None

def build_http_client(settings) -> AsyncClient:
    """
    Build shared HTTP client with connection pooling.

    Returns:
        Configured AsyncClient for inter-service communication
    """
    return AsyncClient(
        timeout=Timeout(5.0, connect=1.0),
        limits=Limits(
            max_connections=200,
            max_keepalive_connections=100
        ),
        headers={"User-Agent": settings.service_name},
    )

async def close_http_client() -> None:
    """Close HTTP client and release connections."""
    global _http_client
    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan with HTTP client lifecycle."""
    global _http_client
    _http_client = build_http_client(settings)
    app.state.http_client = _http_client
    try:
        yield
    finally:
        await close_http_client()

# Usage: Inject client from app state
async def fetch_user_data(
    user_id: int,
    client: AsyncClient = Depends(get_http_client)
) -> dict:
    """
    Fetch user data from data service.

    Args:
        user_id: User identifier
        client: Shared HTTP client (injected)

    Returns:
        User data dictionary
    """
    response = await client.get(
        f"http://finance_user_api:8000/users/{user_id}"
    )
    response.raise_for_status()
    return response.json()
```

**Architecture Rule**:
> HTTP clients MUST be instantiated once per process during startup and shared across all requests via dependency injection or app state.

**Monitoring**:
```bash
# Monitor active connections (should be stable, < max_connections)
netstat -an | grep ESTABLISHED | wc -l

# Check for connection leaks (TIME_WAIT should not grow indefinitely)
netstat -an | grep TIME_WAIT | wc -l

# Monitor file descriptors
docker exec service sh -c 'ls /proc/$$/fd | wc -l'
```

**Related Anti-Patterns**:
- Global FSM Storage Never Closed → `docs/atomic/services/aiogram/state-management.md#global-fsm-storage-never-closed`
- Connection Pool Misuse → `docs/atomic/integrations/redis/connection-management.md#connection-pool-misuse`

## Testing

- Mock responses with `respx` or `pytest-httpx` in unit tests.
- Use Testcontainers or staging data services for end-to-end contract validation.

## Related Documents

- `docs/atomic/integrations/http-communication/timeout-retry-patterns.md`
- `docs/atomic/integrations/http-communication/error-handling-strategies.md`
- `docs/atomic/services/fastapi/lifespan-management.md`
- `docs/atomic/services/fastapi/dependency-injection.md`
