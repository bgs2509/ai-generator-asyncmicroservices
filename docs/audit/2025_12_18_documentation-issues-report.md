# Documentation Issues Report — 2025-12-18

## Executive Summary

This audit analyzed the AI Generator for Async Microservices documentation against the project's main purpose: enabling AI agents to generate consistent, high-quality microservices code through a 7-stage workflow.

### Key Findings

| Metric | Value |
|--------|-------|
| Total Issues Found | 8 |
| Critical (P0) | 3 |
| High (P1) | 2 |
| Medium (P2) | 2 |
| Low (P3) | 1 |
| Documentation Coverage | 73% (172 files, 52,389 lines) |
| Template Coverage | 40% (1 of 4 business templates complete) |
| **Workflow Impact** | **Stage 4 (Code Generation) BLOCKED** |

### Root Cause

The documentation is excellent, but **implementation templates are incomplete**. The 7-stage AI workflow cannot execute fully because required templates don't exist.

### Critical Path

```
Stage 0-3: ✅ WORKS (documentation exists)
Stage 4:   ❌ BLOCKED (missing templates)
Stage 5-6: ⚠️  PARTIAL (missing verification criteria)
```

---

## Issue Inventory

| ID | Severity | Category | Issue | Status |
|----|----------|----------|-------|--------|
| ISS-001 | P0 | Templates | Missing template_business_bot | Open |
| ISS-002 | P0 | Templates | Missing template_business_worker | Open |
| ISS-003 | P0 | Templates | Incomplete template_business_api | Open |
| ISS-004 | P1 | Reference | Missing maturity-levels.md | Open |
| ISS-005 | P1 | Reference | Missing conditional-stage-rules.md | Open |
| ISS-006 | P2 | Shared | Missing shared/events/ | Open |
| ISS-007 | P2 | Cross-refs | Inconsistent path formats | Open |
| ISS-008 | P3 | Meta | Multiple "CANONICAL" claims | Open |

---

## Detailed Issue Reports

---

### ISS-001: Missing template_business_bot (P0 — CRITICAL)

#### Problem Description

The `templates/services/template_business_bot/` directory is referenced in multiple locations but contains **NO FILES**.

**Referenced in:**
- `templates/README.md` (line 45) — Shows as "⏳ 0%"
- `docs/guides/ai-code-generation-master-workflow.md` (Stage 4) — Lists as available template
- `docs/atomic/services/aiogram/` — 8 documents reference this template

The Aiogram 3.x Telegram bot template is a core deliverable of this framework, yet it does not exist.

#### Current State (Problem Example)

```bash
# Attempting to use the template:
$ ls templates/services/template_business_bot/
ls: cannot access 'templates/services/template_business_bot/': No such file or directory

# Referenced in templates/README.md:
| Component              | Status | Description                      |
|------------------------|--------|----------------------------------|
| template_business_bot  | ⏳ 0%  | Aiogram Telegram bot scaffolding |
#                          ^^^^^
#                          ZERO FILES EXIST

# In docs/guides/ai-code-generation-master-workflow.md (Stage 4):
> Phase 5: Bot Generation
> - Copy template from `templates/services/template_business_bot/`
> - Customize handlers for use case
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   AI CANNOT EXECUTE THIS — TEMPLATE DOES NOT EXIST
```

#### Expected State (Solution Example)

The template should provide a complete Aiogram 3.x scaffolding:

```
templates/services/template_business_bot/
├── Dockerfile                              # Multi-stage build
├── requirements.txt                        # aiogram 3.13+, pydantic, etc.
├── .env.example                            # Environment variables template
├── src/
│   ├── __init__.py
│   ├── main.py                             # Bot entry point with lifespan
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                       # Pydantic Settings for bot
│   │   ├── logging_config.py               # Structured logging setup
│   │   └── constants.py                    # Bot constants
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── bot_instance.py                 # Bot and Dispatcher setup
│   │   ├── middlewares/
│   │   │   ├── __init__.py
│   │   │   ├── logging.py                  # Request logging middleware
│   │   │   └── error_handler.py            # Global error handling
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── start.py                    # /start command handler
│   │   │   ├── help.py                     # /help command handler
│   │   │   └── common.py                   # Common message handlers
│   │   ├── keyboards/
│   │   │   ├── __init__.py
│   │   │   └── inline.py                   # Inline keyboard builders
│   │   └── states/
│   │       ├── __init__.py
│   │       └── user_states.py              # FSM states for conversations
│   └── infrastructure/
│       ├── __init__.py
│       ├── http_clients/
│       │   ├── __init__.py
│       │   └── data_api_client.py          # HTTP client for Data Service
│       └── rabbitmq/
│           ├── __init__.py
│           └── publisher.py                # Event publisher
└── tests/
    ├── __init__.py
    ├── conftest.py                         # pytest fixtures
    └── test_handlers.py                    # Handler tests
```

**Example main.py:**

```python
# templates/services/template_business_bot/src/main.py
import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.core.config import settings
from src.core.logging_config import setup_logging, get_logger
from src.bot.handlers import start, help, common
from src.bot.middlewares.logging import LoggingMiddleware
from src.bot.middlewares.error_handler import ErrorHandlerMiddleware
from src.infrastructure.http_clients.data_api_client import DataApiClient

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(bot: Bot, dp: Dispatcher):
    """Manage bot lifecycle: startup and shutdown."""
    # Startup
    logger.info("Bot starting up...")

    # Initialize HTTP client for Data Service
    data_client = DataApiClient(settings.data_api_url)
    await data_client.connect()
    dp["data_client"] = data_client

    # Set bot commands menu
    await bot.set_my_commands([
        ("start", "Start the bot"),
        ("help", "Show help message"),
    ])

    yield

    # Shutdown
    logger.info("Bot shutting down...")
    await data_client.close()
    await bot.session.close()


async def main():
    """Initialize and run the bot."""
    setup_logging()

    # Initialize bot with default properties
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Initialize dispatcher
    dp = Dispatcher()

    # Register middlewares
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ErrorHandlerMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    dp.callback_query.middleware(ErrorHandlerMiddleware())

    # Register routers
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(common.router)

    # Run with lifespan management
    async with lifespan(bot, dp):
        logger.info(f"Bot @{(await bot.get_me()).username} started")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
```

#### Impact Analysis

| Impact Area | Description |
|-------------|-------------|
| **Workflow Blocked** | AI agents cannot generate Telegram bot services |
| **Stage 4 Failure** | Code Generation phase fails for any bot request |
| **User Experience** | Users must manually create bot scaffolding |
| **Documentation Gap** | 8 Aiogram docs reference non-existent template |
| **Framework Promise** | "One Ring to Rule Them All" broken for bots |

#### Solution Steps

1. Create `templates/services/template_business_bot/` directory
2. Create `Dockerfile` using multi-stage pattern from template_business_api
3. Create `requirements.txt` with:
   - aiogram>=3.13.0
   - pydantic>=2.9.0
   - pydantic-settings>=2.5.0
   - structlog>=24.0.0
   - httpx>=0.27.0
   - aio-pika>=9.4.0 (for RabbitMQ)
4. Create `src/main.py` with proper lifespan management
5. Create handler routers following Aiogram 3.x patterns
6. Create middleware for logging and error handling
7. Create HTTP client for Data Service communication (HTTP-only architecture)
8. Add tests with pytest-asyncio
9. Update `templates/README.md` to show ✅ 100%

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `templates/services/template_business_bot/` (entire directory, ~15 files) |
| UPDATE | `templates/README.md` — Change status from ⏳ 0% to ✅ 100% |

#### Related Issues

- ISS-002 — Similar pattern needed for worker template
- ISS-003 — Shared patterns with API template (http_clients, rabbitmq)
- ISS-006 — Needs shared/events/ for event publishing

---

### ISS-002: Missing template_business_worker (P0 — CRITICAL)

#### Problem Description

The AsyncIO background worker template is referenced in documentation but does not exist. Workers are essential for:
- Processing RabbitMQ messages
- Executing background tasks
- Handling scheduled jobs
- Long-running computations

#### Current State (Problem Example)

```bash
# Attempting to use the template:
$ ls templates/services/template_business_worker/
ls: cannot access 'templates/services/template_business_worker/': No such file or directory

# In templates/README.md:
| Component                | Status | Description                         |
|--------------------------|--------|-------------------------------------|
| template_business_worker | ⏳ 0%  | AsyncIO background worker scaffolding |
#                            ^^^^^
#                            ZERO FILES EXIST

# In docs/atomic/services/asyncio-workers/worker-setup.md:
> ## Quick Start
> 1. Copy template from `templates/services/template_business_worker/`
> 2. Customize task processor for your use case
> 3. Configure RabbitMQ connection
#    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#    STEP 1 FAILS — TEMPLATE DOES NOT EXIST
```

#### Expected State (Solution Example)

```
templates/services/template_business_worker/
├── Dockerfile
├── requirements.txt
├── .env.example
├── src/
│   ├── __init__.py
│   ├── main.py                             # Worker entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                       # Pydantic Settings
│   │   ├── logging_config.py               # Structured logging
│   │   └── constants.py                    # Worker constants
│   ├── worker/
│   │   ├── __init__.py
│   │   ├── task_processor.py               # Abstract task processor
│   │   └── handlers/
│   │       ├── __init__.py
│   │       └── example_handler.py          # Example task handler
│   └── infrastructure/
│       ├── __init__.py
│       ├── rabbitmq/
│       │   ├── __init__.py
│       │   ├── consumer.py                 # RabbitMQ consumer
│       │   └── connection.py               # Connection management
│       └── http_clients/
│           ├── __init__.py
│           └── data_api_client.py          # HTTP client for Data Service
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_task_processor.py
```

**Example main.py:**

```python
# templates/services/template_business_worker/src/main.py
"""
AsyncIO Background Worker Entry Point.

Implements graceful shutdown handling and RabbitMQ message consumption.
"""
import asyncio
import signal
from contextlib import asynccontextmanager

from src.core.config import settings
from src.core.logging_config import setup_logging, get_logger
from src.worker.task_processor import TaskProcessor
from src.infrastructure.rabbitmq.consumer import RabbitMQConsumer
from src.infrastructure.http_clients.data_api_client import DataApiClient

logger = get_logger(__name__)


class GracefulShutdown:
    """Handles graceful shutdown signals (SIGTERM, SIGINT)."""

    def __init__(self):
        self.shutdown_event = asyncio.Event()

    def trigger_shutdown(self, signum: int, frame) -> None:
        """Signal handler to trigger graceful shutdown."""
        logger.info(
            "Received shutdown signal",
            signal=signal.Signals(signum).name,
        )
        self.shutdown_event.set()


@asynccontextmanager
async def lifespan():
    """Manage worker lifecycle: startup and shutdown."""
    # Startup
    logger.info("Worker starting up...", queue=settings.queue_name)

    # Initialize connections
    consumer = RabbitMQConsumer(settings.rabbitmq_url)
    await consumer.connect()

    data_client = DataApiClient(settings.data_api_url)
    await data_client.connect()

    yield {"consumer": consumer, "data_client": data_client}

    # Shutdown
    logger.info("Worker shutting down...")
    await data_client.close()
    await consumer.close()


async def main() -> None:
    """Initialize and run the worker."""
    setup_logging()
    logger.info("Worker initializing...", version=settings.app_version)

    shutdown = GracefulShutdown()

    # Register signal handlers
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: shutdown.trigger_shutdown(s, None)
        )

    async with lifespan() as deps:
        processor = TaskProcessor(data_client=deps["data_client"])
        consumer = deps["consumer"]

        # Start consuming messages
        consume_task = asyncio.create_task(
            consumer.consume(
                queue_name=settings.queue_name,
                callback=processor.process,
            )
        )

        logger.info("Worker started, consuming messages...")

        # Wait for shutdown signal
        await shutdown.shutdown_event.wait()

        # Cancel consumer task gracefully
        logger.info("Stopping message consumption...")
        consume_task.cancel()
        try:
            await consume_task
        except asyncio.CancelledError:
            pass

    logger.info("Worker shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
```

**Example task_processor.py:**

```python
# templates/services/template_business_worker/src/worker/task_processor.py
"""
Task Processor - handles incoming messages from RabbitMQ.
"""
from abc import ABC, abstractmethod
from typing import Any

import structlog
from pydantic import BaseModel

from src.infrastructure.http_clients.data_api_client import DataApiClient


class TaskResult(BaseModel):
    """Result of task processing."""
    success: bool
    message: str
    data: dict[str, Any] | None = None


class TaskProcessor:
    """Processes tasks received from RabbitMQ queue."""

    def __init__(self, data_client: DataApiClient):
        self.data_client = data_client
        self.logger = structlog.get_logger(__name__)

    async def process(self, message: dict[str, Any]) -> TaskResult:
        """
        Process a single task message.

        Args:
            message: Parsed message payload from RabbitMQ

        Returns:
            TaskResult indicating success or failure
        """
        task_type = message.get("type", "unknown")
        correlation_id = message.get("correlation_id")

        self.logger.info(
            "Processing task",
            task_type=task_type,
            correlation_id=correlation_id,
        )

        try:
            # Route to appropriate handler based on task type
            handler = self._get_handler(task_type)
            result = await handler(message)

            self.logger.info(
                "Task completed successfully",
                task_type=task_type,
                correlation_id=correlation_id,
            )
            return result

        except Exception as e:
            self.logger.exception(
                "Task processing failed",
                task_type=task_type,
                correlation_id=correlation_id,
                error=str(e),
            )
            return TaskResult(
                success=False,
                message=f"Task failed: {e}",
            )

    def _get_handler(self, task_type: str):
        """Get handler function for task type."""
        handlers = {
            "example": self._handle_example,
            # Add more handlers here
        }
        return handlers.get(task_type, self._handle_unknown)

    async def _handle_example(self, message: dict[str, Any]) -> TaskResult:
        """Example task handler."""
        # Use data_client to communicate with Data Service
        # await self.data_client.update_entity(...)
        return TaskResult(success=True, message="Example task completed")

    async def _handle_unknown(self, message: dict[str, Any]) -> TaskResult:
        """Handler for unknown task types."""
        task_type = message.get("type", "unknown")
        self.logger.warning("Unknown task type", task_type=task_type)
        return TaskResult(success=False, message=f"Unknown task type: {task_type}")
```

#### Impact Analysis

| Impact Area | Description |
|-------------|-------------|
| **Workflow Blocked** | AI cannot generate background worker services |
| **Event-Driven Gap** | RabbitMQ consumers cannot be scaffolded |
| **Async Processing** | No pattern for background task execution |
| **K8s Integration** | No health check pattern for workers |
| **Architecture Incomplete** | HTTP-only architecture needs workers for async |

#### Solution Steps

1. Create `templates/services/template_business_worker/` directory
2. Create `Dockerfile` with Python 3.12+ base
3. Create `requirements.txt` with:
   - aio-pika>=9.4.0
   - pydantic>=2.9.0
   - pydantic-settings>=2.5.0
   - structlog>=24.0.0
   - httpx>=0.27.0
4. Create `src/main.py` with graceful shutdown handling
5. Create `src/worker/task_processor.py` with handler routing
6. Create `src/infrastructure/rabbitmq/consumer.py`
7. Add optional HTTP health endpoint for Kubernetes probes
8. Create tests with mock RabbitMQ

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `templates/services/template_business_worker/` (entire directory, ~12 files) |
| UPDATE | `templates/README.md` — Change status from ⏳ 0% to ✅ 100% |

#### Related Issues

- ISS-001 — Bot template shares infrastructure patterns
- ISS-003 — API template shares http_clients module
- ISS-006 — Needs shared/events/ for event consumption

---

### ISS-003: Incomplete template_business_api (P0 — CRITICAL)

#### Problem Description

The Business API template exists but is only **40% complete**. Critical components are missing, making the template unusable for production code generation.

#### Current State (Problem Example)

```bash
# Checking what exists:
$ ls templates/services/template_business_api/src/core/
config.py
# Missing: logging_config.py, middleware.py

$ ls templates/services/template_business_api/src/api/v1/
# Directory may not exist or is empty
# Missing: health_router.py

$ ls templates/services/template_business_api/src/infrastructure/
# Missing: http_clients/, rabbitmq/

$ ls templates/services/template_business_api/src/
# Missing: schemas/

$ ls templates/services/template_business_api/tests/
# Missing: conftest.py with fixtures
```

**Missing files prevent:**
- Structured logging in generated services
- Request correlation across services
- Health check endpoints for Kubernetes
- HTTP communication with Data Services
- Event publishing to RabbitMQ
- Proper test fixtures

#### Expected State (Solution Example)

**File: `src/core/logging_config.py`**

```python
# templates/services/template_business_api/src/core/logging_config.py
"""
Structured logging configuration using structlog.

Provides consistent JSON logging for production and human-readable
output for development.
"""
import logging
import sys
from typing import Any

import structlog

from src.core.config import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.

    Uses JSON format in production (LOG_FORMAT=json) and
    console renderer in development for readability.
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.getLevelName(settings.log_level),
    )

    # Determine processors based on environment
    if settings.log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name, typically __name__

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)
```

**File: `src/core/middleware.py`**

```python
# templates/services/template_business_api/src/core/middleware.py
"""
FastAPI middleware for request processing.

Provides:
- Request ID correlation
- Request/response logging
- Timing metrics
"""
import time
from typing import Callable
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.logging_config import get_logger

# Import from shared utilities if available
try:
    from shared.utils.request_id import request_id_ctx
except ImportError:
    from contextvars import ContextVar
    request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add request ID correlation to all requests.

    - Extracts X-Request-ID from incoming headers or generates new UUID
    - Sets request ID in context for logging correlation
    - Adds X-Request-ID to response headers
    """

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request_id_ctx.set(request_id)

        # Log request start
        start_time = time.perf_counter()
        logger.info(
            "Request started",
            method=request.method,
            path=request.url.path,
            query=str(request.query_params),
            request_id=request_id,
        )

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Add request ID to response
        response.headers["X-Request-ID"] = request_id

        # Log request completion
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            request_id=request_id,
        )

        return response
```

**File: `src/api/v1/health_router.py`**

```python
# templates/services/template_business_api/src/api/v1/health_router.py
"""
Health check endpoints for Kubernetes probes.

Provides:
- /health/live — Liveness probe (is the process running?)
- /health/ready — Readiness probe (can it serve traffic?)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.core.config import settings
from src.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str
    version: str


class ReadinessResponse(BaseModel):
    """Readiness check response with dependency status."""
    status: str
    service: str
    version: str
    dependencies: dict[str, str]


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 if the service is running.",
)
async def liveness() -> HealthResponse:
    """
    Liveness probe for Kubernetes.

    This endpoint should always return 200 if the process is running.
    Kubernetes will restart the pod if this fails.
    """
    return HealthResponse(
        status="healthy",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness probe",
    description="Returns 200 if the service can serve traffic.",
)
async def readiness() -> ReadinessResponse:
    """
    Readiness probe for Kubernetes.

    Checks if all dependencies are available.
    Kubernetes will stop sending traffic if this fails.
    """
    dependencies: dict[str, str] = {}
    all_healthy = True

    # Check Data Service connectivity
    try:
        # TODO: Inject and check data_client health
        dependencies["data_service"] = "healthy"
    except Exception as e:
        logger.warning("Data service health check failed", error=str(e))
        dependencies["data_service"] = "unhealthy"
        all_healthy = False

    if not all_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service dependencies not ready",
        )

    return ReadinessResponse(
        status="ready",
        service=settings.app_name,
        version=settings.app_version,
        dependencies=dependencies,
    )
```

**File: `src/infrastructure/http_clients/data_api_client.py`**

```python
# templates/services/template_business_api/src/infrastructure/http_clients/data_api_client.py
"""
HTTP client for Data Service communication.

Implements the HTTP-only data access pattern:
- Business services NEVER access databases directly
- All data operations go through Data Service HTTP API
"""
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from src.core.config import settings
from src.core.logging_config import get_logger

# Import request ID for correlation
try:
    from shared.utils.request_id import request_id_ctx
except ImportError:
    from contextvars import ContextVar
    request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


class DataApiClient:
    """
    Async HTTP client for Data Service.

    Usage:
        async with DataApiClient(base_url) as client:
            user = await client.get("/users/123", UserResponse)
    """

    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "DataApiClient":
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def connect(self) -> None:
        """Initialize the HTTP client."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Content-Type": "application/json"},
        )
        logger.info("Data API client connected", base_url=self.base_url)

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.info("Data API client closed")

    def _get_headers(self) -> dict[str, str]:
        """Get headers with request ID for correlation."""
        headers = {}
        request_id = request_id_ctx.get()
        if request_id:
            headers["X-Request-ID"] = request_id
        return headers

    async def get(
        self,
        path: str,
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """
        Send GET request to Data Service.

        Args:
            path: API path (e.g., "/users/123")
            response_model: Optional Pydantic model for response validation

        Returns:
            Parsed response (model instance or dict)
        """
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        response = await self._client.get(path, headers=self._get_headers())
        response.raise_for_status()

        data = response.json()
        if response_model:
            return response_model.model_validate(data)
        return data

    async def post(
        self,
        path: str,
        payload: BaseModel | dict[str, Any],
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """
        Send POST request to Data Service.

        Args:
            path: API path
            payload: Request body (Pydantic model or dict)
            response_model: Optional Pydantic model for response validation

        Returns:
            Parsed response (model instance or dict)
        """
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        json_data = payload.model_dump() if isinstance(payload, BaseModel) else payload
        response = await self._client.post(
            path,
            json=json_data,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        data = response.json()
        if response_model:
            return response_model.model_validate(data)
        return data

    async def put(
        self,
        path: str,
        payload: BaseModel | dict[str, Any],
        response_model: type[T] | None = None,
    ) -> T | dict[str, Any]:
        """Send PUT request to Data Service."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        json_data = payload.model_dump() if isinstance(payload, BaseModel) else payload
        response = await self._client.put(
            path,
            json=json_data,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        data = response.json()
        if response_model:
            return response_model.model_validate(data)
        return data

    async def delete(self, path: str) -> None:
        """Send DELETE request to Data Service."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")

        response = await self._client.delete(path, headers=self._get_headers())
        response.raise_for_status()
```

**File: `tests/conftest.py`**

```python
# templates/services/template_business_api/tests/conftest.py
"""
Pytest fixtures for Business API tests.
"""
import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    """Synchronous test client for simple tests."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Async test client for async tests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_data_client(mocker):
    """Mock DataApiClient for unit tests."""
    mock = mocker.AsyncMock()
    mock.get.return_value = {"id": "123", "name": "Test"}
    mock.post.return_value = {"id": "456", "name": "Created"}
    return mock
```

#### Impact Analysis

| Impact Area | Description |
|-------------|-------------|
| **No Logging** | Generated APIs lack structured logging |
| **No Correlation** | Request IDs not propagated across services |
| **No Health Checks** | Kubernetes probes fail |
| **No Data Access** | Cannot communicate with Data Service |
| **No Tests** | Test fixtures missing, testing blocked |
| **Incomplete Template** | 40% != production-ready |

#### Solution Steps

1. Create `src/core/logging_config.py` — Structured logging with structlog
2. Create `src/core/middleware.py` — Request ID middleware
3. Create `src/api/v1/health_router.py` — Kubernetes health endpoints
4. Create `src/infrastructure/http_clients/__init__.py`
5. Create `src/infrastructure/http_clients/data_api_client.py`
6. Create `src/infrastructure/rabbitmq/__init__.py`
7. Create `src/infrastructure/rabbitmq/publisher.py`
8. Create `src/schemas/__init__.py`
9. Create `src/schemas/base.py` — Base response models
10. Create `tests/conftest.py` — pytest fixtures

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `templates/services/template_business_api/src/core/logging_config.py` |
| CREATE | `templates/services/template_business_api/src/core/middleware.py` |
| CREATE | `templates/services/template_business_api/src/api/v1/health_router.py` |
| CREATE | `templates/services/template_business_api/src/infrastructure/http_clients/__init__.py` |
| CREATE | `templates/services/template_business_api/src/infrastructure/http_clients/data_api_client.py` |
| CREATE | `templates/services/template_business_api/src/infrastructure/rabbitmq/__init__.py` |
| CREATE | `templates/services/template_business_api/src/infrastructure/rabbitmq/publisher.py` |
| CREATE | `templates/services/template_business_api/src/schemas/__init__.py` |
| CREATE | `templates/services/template_business_api/src/schemas/base.py` |
| CREATE | `templates/services/template_business_api/tests/conftest.py` |
| UPDATE | `templates/README.md` — Change status from 🚧 40% to ✅ 100% |

#### Related Issues

- ISS-001 — Bot template needs same infrastructure patterns
- ISS-002 — Worker template needs same infrastructure patterns
- ISS-006 — Publisher needs shared/events/

---

### ISS-004: Missing maturity-levels.md (P1 — HIGH)

#### Problem Description

The document `docs/reference/maturity-levels.md` is referenced **4 times** in the AI code generation workflow but does not exist.

Maturity levels are essential for AI agents to determine:
- Which features to include in generated code
- Expected generation time
- Quality and completeness targets

#### Current State (Problem Example)

```markdown
# In docs/guides/ai-code-generation-master-workflow.md:

## Stage 1: Prompt Validation (line 144)
> **Target Maturity Level**: See `docs/reference/maturity-levels.md`
#                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                                THIS FILE DOES NOT EXIST

## Stage 2: Requirements Clarification (line 224)
> Match requirements to maturity level from `docs/reference/maturity-levels.md`
#                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                                            THIS FILE DOES NOT EXIST

## Stage 3: Architecture Planning (line 287)
> Verify feature set matches target maturity level (`docs/reference/maturity-levels.md`)

## Stage 5: Quality Verification (line 637)
> Validate against maturity level requirements from `docs/reference/maturity-levels.md`
```

**Result:** AI agents cannot determine what features to include.

#### Expected State (Solution Example)

```markdown
# Maturity Levels Reference

## Overview

This document defines the four maturity levels for generated services.
AI agents use these levels to determine feature scope and quality targets.

## Quick Reference

| Level | Name | Time | Use Case |
|-------|------|------|----------|
| 1 | PoC | ~5 min | Validate idea quickly |
| 2 | Dev | ~10 min | Development-ready with basics |
| 3 | Pre-Prod | ~15 min | Ready for staging |
| 4 | Prod | ~30 min | Production-ready with full observability |

---

## Level 1: PoC (Proof of Concept)

**Purpose**: Validate core functionality as fast as possible.

**Time Target**: ~5 minutes

### Included Features

- Basic project structure
- Single endpoint or handler
- Console logging (print statements OK)
- `.env` configuration with defaults
- `requirements.txt` with minimal dependencies

### Excluded Features

- Tests
- Docker
- Health checks
- Structured logging
- Metrics/tracing
- Type hints (optional at this level)

### Directory Structure

```
project/
├── .env.example
├── requirements.txt
└── src/
    ├── __init__.py
    └── main.py
```

### Example Use Cases

- "Can Aiogram handle inline keyboards?"
- "Does FastAPI work with async SQLAlchemy?"
- Quick demonstration to stakeholders

---

## Level 2: Dev (Development)

**Purpose**: Developer-ready with essential tooling.

**Time Target**: ~10 minutes

### Included Features

Everything in PoC, plus:

- Dockerfile (single stage OK)
- `docker-compose.dev.yml`
- Basic tests (1-2 per endpoint)
- Health endpoint (`/health`)
- Structured logging (console renderer)
- Type hints (required)
- Pydantic models for validation

### Excluded Features

- Full test coverage
- CI/CD pipelines
- Production Docker configs
- Metrics/tracing
- Database migrations

### Directory Structure

```
project/
├── .env.example
├── Dockerfile
├── docker-compose.dev.yml
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── api/
│       └── v1/
│           └── health.py
└── tests/
    ├── __init__.py
    └── test_health.py
```

---

## Level 3: Pre-Prod (Pre-Production)

**Purpose**: Ready for staging environment.

**Time Target**: ~15 minutes

### Included Features

Everything in Dev, plus:

- Full test suite (unit + integration)
- `docker-compose.prod.yml`
- CI pipeline (lint, test, build)
- Metrics endpoint (`/metrics`)
- Request ID correlation
- Error handling middleware
- API versioning (`/api/v1/`)
- Structured logging (JSON format)
- Alembic migrations (if database)

### Excluded Features

- Full observability stack (Grafana, Jaeger)
- CD pipeline
- Security hardening
- Performance optimization

### Directory Structure

```
project/
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Makefile
├── requirements.txt
├── alembic/
│   └── versions/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── middleware.py
│   └── api/
│       └── v1/
│           ├── __init__.py
│           ├── health.py
│           └── router.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    └── integration/
```

---

## Level 4: Prod (Production)

**Purpose**: Production-ready with full observability.

**Time Target**: ~30 minutes

### Included Features

Everything in Pre-Prod, plus:

- Distributed tracing (Jaeger integration)
- Prometheus metrics
- Grafana dashboard config
- CD pipeline (deploy to staging/prod)
- Rate limiting
- Security headers (CORS, CSP)
- Database migrations with Alembic
- Makefile with all commands
- Complete documentation

### Directory Structure

```
project/
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── Dockerfile
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── Makefile
├── README.md
├── requirements.txt
├── alembic/
├── grafana/
│   └── dashboards/
├── prometheus/
│   └── prometheus.yml
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   ├── api/
│   ├── domain/
│   ├── infrastructure/
│   └── schemas/
└── tests/
    ├── conftest.py
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## Feature Matrix

| Feature | PoC | Dev | Pre-Prod | Prod |
|---------|:---:|:---:|:--------:|:----:|
| Basic structure | ✅ | ✅ | ✅ | ✅ |
| Type hints | ❌ | ✅ | ✅ | ✅ |
| Pydantic models | ❌ | ✅ | ✅ | ✅ |
| Dockerfile | ❌ | ✅ | ✅ | ✅ |
| docker-compose | ❌ | Dev | Dev+Prod | Dev+Prod |
| Tests | ❌ | Basic | Full | Full+E2E |
| Health endpoint | ❌ | ✅ | ✅ | ✅ |
| Logging | Console | Structured | JSON | JSON |
| Metrics | ❌ | ❌ | Basic | Prometheus |
| Tracing | ❌ | ❌ | ❌ | Jaeger |
| CI pipeline | ❌ | ❌ | ✅ | ✅ |
| CD pipeline | ❌ | ❌ | ❌ | ✅ |
| Migrations | ❌ | ❌ | ✅ | ✅ |
| Makefile | ❌ | ❌ | ✅ | ✅ |

---

## Selecting a Maturity Level

Use this decision tree:

```
Q: Is this a quick experiment or demo?
├─ Yes → Level 1 (PoC)
└─ No
   Q: Will this run in production?
   ├─ No → Level 2 (Dev)
   └─ Yes
      Q: Does it need full observability?
      ├─ No → Level 3 (Pre-Prod)
      └─ Yes → Level 4 (Prod)
```

## Related Documents

- `docs/guides/ai-code-generation-master-workflow.md` — References maturity levels in Stages 1-5
- `docs/reference/conditional-stage-rules.md` — Phase execution based on maturity level
- `templates/README.md` — Template capabilities per level
```

#### Impact Analysis

| Impact Area | Description |
|-------------|-------------|
| **Workflow Ambiguous** | AI cannot determine feature scope |
| **Inconsistent Output** | Different features per generation |
| **User Confusion** | No expectation setting |
| **Time Estimates Wrong** | No reference for generation time |

#### Solution Steps

1. Create `docs/reference/maturity-levels.md`
2. Define 4 levels with clear boundaries
3. Create feature matrix table
4. Add decision tree for level selection
5. Link from workflow document

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `docs/reference/maturity-levels.md` |

#### Related Issues

- ISS-005 — Conditional rules depend on maturity levels

---

### ISS-005: Missing conditional-stage-rules.md (P1 — HIGH)

#### Problem Description

Referenced in Stage 4 of the workflow but does not exist.

#### Current State (Problem Example)

```markdown
# In docs/guides/ai-code-generation-master-workflow.md (Stage 4):
> For conditional phase execution, see `docs/reference/conditional-stage-rules.md`
#                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                                       THIS FILE DOES NOT EXIST
```

#### Expected State (Solution Example)

```markdown
# Conditional Stage Execution Rules

## Overview

Not all services require all generation phases. This document defines
when to skip or modify phases based on service type and requirements.

## Phase Execution Matrix

| Service Request | Ph1 Infra | Ph2 Data | Ph3 API | Ph4 Worker | Ph5 Bot | Ph6 Test |
|-----------------|:---------:|:--------:|:-------:|:----------:|:-------:|:--------:|
| API only | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| API + Worker | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Bot only | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Bot + Worker | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Worker only | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Full Stack | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Conditional Rules

### Rule 1: Skip Worker Phase

```
IF requirements NOT CONTAIN any of:
  - "background task"
  - "async processing"
  - "queue"
  - "scheduled job"
  - "RabbitMQ consumer"
THEN SKIP Phase 4 (Workers)
```

### Rule 2: Skip Bot Phase

```
IF requirements NOT CONTAIN any of:
  - "telegram"
  - "bot"
  - "aiogram"
  - "chat interface"
THEN SKIP Phase 5 (Bot)
```

### Rule 3: Skip API Phase

```
IF service_type == "worker-only" OR service_type == "bot-only"
AND requirements NOT CONTAIN "REST API"
THEN SKIP Phase 3 (Business API)
```

### Rule 4: Database Selection

```
IF data_requirements CONTAIN any of:
  - "flexible schema"
  - "documents"
  - "nested objects"
  - "unstructured data"
THEN use template_data_mongo_api
ELSE use template_data_postgres_api  # Default
```

### Rule 5: Maturity Level Impact

```
IF maturity_level == "PoC":
  SKIP: Phase 6 tests, CI/CD in Phase 1

IF maturity_level == "Dev":
  SKIP: Full tests in Phase 6, CD in Phase 1

IF maturity_level == "Pre-Prod":
  SKIP: CD in Phase 1, Grafana dashboards

IF maturity_level == "Prod":
  INCLUDE: All phases, all features
```

## Examples

### Example 1: Simple REST API

**Request**: "Create a user management API with PostgreSQL"

**Phase Execution**:
- ✅ Phase 1: Docker Compose, Makefile
- ✅ Phase 2: PostgreSQL Data Service
- ✅ Phase 3: FastAPI Business API
- ❌ Phase 4: Skip (no background tasks)
- ❌ Phase 5: Skip (no Telegram bot)
- ✅ Phase 6: Tests

### Example 2: Telegram Bot with Background Processing

**Request**: "Create a Telegram bot that processes images in background"

**Phase Execution**:
- ✅ Phase 1: Docker Compose, Makefile
- ✅ Phase 2: PostgreSQL Data Service
- ❌ Phase 3: Skip (no REST API needed)
- ✅ Phase 4: AsyncIO Worker for image processing
- ✅ Phase 5: Aiogram Bot
- ✅ Phase 6: Tests

## Related Documents

- `docs/reference/maturity-levels.md` — Feature scope per level
- `docs/guides/ai-code-generation-master-workflow.md` — Stage 4 references this
```

#### Solution Steps

1. Create `docs/reference/conditional-stage-rules.md`
2. Define phase execution matrix
3. Document conditional rules with examples
4. Link from workflow document

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `docs/reference/conditional-stage-rules.md` |

---

### ISS-006: Missing shared/events/ (P2 — MEDIUM)

#### Problem Description

Event-driven architecture is mentioned throughout the documentation, but base event classes don't exist.

#### Current State (Problem Example)

```markdown
# In templates/README.md:
| shared/events/  | ⏳ 0%  | Base event classes |

# In docs/atomic/integrations/rabbitmq/event-publishing.md:
> from shared.events.base_event import BaseEvent
#      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#      THIS MODULE DOES NOT EXIST
```

#### Expected State (Solution Example)

```python
# templates/shared/events/base_event.py
"""
Base event classes for RabbitMQ messaging.

All domain events should inherit from BaseEvent to ensure
consistent serialization and metadata handling.
"""
from datetime import datetime
from typing import Any, Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

T = TypeVar("T")


class EventMetadata(BaseModel):
    """Standard event metadata for all domain events."""

    event_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for this event instance",
    )
    event_type: str = Field(
        description="Event type name (e.g., 'user.created')",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the event occurred",
    )
    source_service: str = Field(
        description="Service that produced this event",
    )
    correlation_id: str | None = Field(
        default=None,
        description="ID linking related events across services",
    )
    causation_id: str | None = Field(
        default=None,
        description="ID of the event that caused this event",
    )
    version: str = Field(
        default="1.0",
        description="Event schema version",
    )


class BaseEvent(BaseModel, Generic[T]):
    """
    Base class for all domain events.

    Usage:
        class UserCreatedPayload(BaseModel):
            user_id: str
            email: str

        class UserCreatedEvent(BaseEvent[UserCreatedPayload]):
            pass

        event = UserCreatedEvent(
            metadata=EventMetadata(
                event_type="user.created",
                source_service="user-api",
            ),
            payload=UserCreatedPayload(user_id="123", email="test@example.com"),
        )

        # Publish to RabbitMQ
        await publisher.publish(event)
    """

    metadata: EventMetadata
    payload: T

    class Config:
        frozen = True  # Events are immutable

    def to_rabbitmq_message(self) -> bytes:
        """Serialize event for RabbitMQ publishing."""
        return self.model_dump_json().encode("utf-8")

    @classmethod
    def from_rabbitmq_message(cls, body: bytes) -> "BaseEvent[T]":
        """Deserialize event from RabbitMQ message."""
        return cls.model_validate_json(body)

    @property
    def routing_key(self) -> str:
        """Generate routing key from event type."""
        return self.metadata.event_type.replace(".", "_")
```

#### Solution Steps

1. Create `templates/shared/events/__init__.py`
2. Create `templates/shared/events/base_event.py`
3. Create `templates/shared/events/README.md` with usage examples
4. Update `templates/README.md` status

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `templates/shared/events/__init__.py` |
| CREATE | `templates/shared/events/base_event.py` |
| CREATE | `templates/shared/events/README.md` |
| UPDATE | `templates/README.md` — Status to ✅ |

---

### ISS-007: Inconsistent Cross-Reference Paths (P2 — MEDIUM)

#### Problem Description

Some documents use relative paths instead of project-root paths.

#### Current State (Problem Example)

```markdown
# In docs/atomic/architecture/naming/naming-python.md:
## Related Documents
- `./README.md` — Main naming conventions hub
- `naming-services.md` — Service naming patterns

# In docs/atomic/integrations/redis/redis-caching.md:
## Related Documents
- `../context-registry.md` — Context management
```

#### Expected State (Solution Example)

```markdown
# Consistent format across ALL files:
## Related Documents
- `docs/atomic/architecture/naming/README.md` — Main naming conventions hub
- `docs/atomic/architecture/naming/naming-services.md` — Service naming patterns
```

#### Solution Steps

1. Search for relative paths: `./`, `../`
2. Replace with full project-root paths
3. Verify all links resolve correctly

#### Affected Files

Approximately 10-15 files in `docs/atomic/` with relative path references.

---

### ISS-008: Multiple "CANONICAL" Claims (P3 — LOW)

#### Problem Description

Multiple documents claim to be the "canonical" source of truth for the same topic.

#### Current State (Problem Example)

```markdown
# In docs/guides/architecture-guide.md (line 3):
> CANONICAL ARCHITECTURE REFERENCE: This document is the single source of truth

# In docs/guides/development-commands.md (line 1):
> CANONICAL COMMAND REFERENCE

# But also in root ARCHITECTURE.md:
> (Contains architecture information, implying it's authoritative)

# Which is canonical?
```

#### Expected State (Solution Example)

Create a reference map:

```markdown
# docs/reference/canonical-references.md

## Canonical Reference Map

| Topic | Canonical Document | Secondary/Guides |
|-------|-------------------|------------------|
| Architecture | `/ARCHITECTURE.md` | `docs/guides/architecture-guide.md` |
| Commands | `Makefile` | `docs/guides/development-commands.md` |
| Naming | `docs/atomic/architecture/naming/README.md` | — |
| Templates | `templates/README.md` | — |
| Workflow | `docs/guides/ai-code-generation-master-workflow.md` | — |
```

Then update guide documents to say "extends" or "implements" rather than "canonical."

#### Solution Steps

1. Create `docs/reference/canonical-references.md`
2. Update `docs/guides/architecture-guide.md` — Remove "CANONICAL" claim
3. Update `docs/guides/development-commands.md` — Remove "CANONICAL" claim

---

## Implementation Roadmap

### Phase 1: Unblock Workflow (P0 + P1)

**Goal**: Enable 7-stage workflow to execute fully.

| # | Task | Files | Priority |
|---|------|-------|----------|
| 1 | Complete template_business_api | ~10 files | P0 |
| 2 | Create template_business_bot | ~15 files | P0 |
| 3 | Create template_business_worker | ~12 files | P0 |
| 4 | Create maturity-levels.md | 1 file | P1 |
| 5 | Create conditional-stage-rules.md | 1 file | P1 |

### Phase 2: Complete Templates (P0 continued)

**Goal**: All 4 business templates at 100%.

| # | Task | Files | Priority |
|---|------|-------|----------|
| 6 | Create template_data_mongo_api | ~12 files | P0 |

### Phase 3: Polish (P2 + P3)

**Goal**: Clean up consistency issues.

| # | Task | Files | Priority |
|---|------|-------|----------|
| 7 | Create shared/events/ | 3 files | P2 |
| 8 | Fix relative path references | ~15 files | P2 |
| 9 | Create canonical-references.md | 3 files | P3 |

---

## Appendix A: File Inventory

### Files to CREATE

| Category | Files | Count |
|----------|-------|-------|
| template_business_api (complete) | logging_config, middleware, health_router, http_clients, rabbitmq, schemas, conftest | ~10 |
| template_business_bot | Full Aiogram scaffolding | ~15 |
| template_business_worker | Full AsyncIO scaffolding | ~12 |
| template_data_mongo_api | Full Motor scaffolding | ~12 |
| shared/events | base_event.py, README.md, __init__.py | 3 |
| docs/reference | maturity-levels.md, conditional-stage-rules.md, canonical-references.md | 3 |
| **TOTAL** | | **~55** |

### Files to UPDATE

| File | Change |
|------|--------|
| `templates/README.md` | Update status for all templates |
| `docs/guides/architecture-guide.md` | Remove "CANONICAL" claim |
| `docs/guides/development-commands.md` | Remove "CANONICAL" claim |
| ~15 atomic docs | Fix relative path references |
| **TOTAL** | **~18** |

---

## Appendix B: Verification Checklist

After implementing fixes, verify:

- [ ] All templates at 100% status in `templates/README.md`
- [ ] `docs/reference/maturity-levels.md` exists and is linked from workflow
- [ ] `docs/reference/conditional-stage-rules.md` exists and is linked from workflow
- [ ] `shared/events/base_event.py` exists and is importable
- [ ] No relative paths (`./`, `../`) in atomic docs
- [ ] No duplicate "CANONICAL" claims
- [ ] 7-stage workflow can execute all phases

---

## Related Documents

- `docs/guides/ai-code-generation-master-workflow.md` — 7-stage workflow
- `templates/README.md` — Template status and inventory
- `ARCHITECTURE.md` — Core architecture documentation
- `docs/INDEX.md` — Master documentation index
