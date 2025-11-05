# Architecture

Detailed architectural documentation for the AI Generator for Async Microservices framework.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Improved Hybrid Approach](#improved-hybrid-approach)
3. [Core Architectural Principles](#core-architectural-principles)
4. [Service Types](#service-types)
5. [Data Access Pattern](#data-access-pattern)
6. [Communication Patterns](#communication-patterns)
7. [DDD & Hexagonal Architecture](#ddd--hexagonal-architecture)
8. [Technology Decisions](#technology-decisions)
9. [Quality Standards](#quality-standards)
10. [Deployment Architecture](#deployment-architecture)

---

## Overview

The AI Generator for Async Microservices framework implements a **battle-tested**, **production-ready** architecture that enforces consistency across all generated projects. The architecture is designed to be:

- **AI-Friendly**: Easy for AI to understand and replicate
- **Consistent**: Same patterns across all projects
- **Type-Safe**: Full type hints with mypy strict mode
- **Async-First**: All I/O operations use async/await
- **Observable**: Logging, metrics, and tracing built-in
- **Maintainable**: Clear separation of concerns

**Key Philosophy:** *"One Ring to Rule Them All"* — One architecture pattern for all your microservices projects.

---

## Improved Hybrid Approach

### The Core Concept

The **Improved Hybrid Approach** is our foundational architecture pattern. It combines:

1. **Centralized Data Services** — Dedicated services for database operations
2. **Distributed Business Logic** — Independent business services
3. **HTTP-Only Communication** — No direct database access from business services
4. **Event-Driven Messaging** — RabbitMQ for async communication

### Why This Approach?

**Problem with Traditional Microservices:**
- Each service has its own database connection
- Duplicate data access code across services
- Difficult to maintain consistency
- Database connection pool exhaustion

**Problem with Monolithic Data Layer:**
- Single point of failure
- Tight coupling
- Difficult to scale

**Our Solution:**
- **Two specialized data services** handle ALL database operations
- Business services focus on business logic only
- Clean separation of concerns
- Easy to scale and maintain

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Business API │  │ Business Bot │  │    Worker    │  │
│  │   (FastAPI)  │  │   (Aiogram)  │  │   (AsyncIO)  │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┴──────────────────┘          │
│                            │                             │
│                   HTTP ONLY (no direct DB)               │
│                            │                             │
└────────────────────────────┼─────────────────────────────┘
                             │
                     ┌───────┴───────┐
                     │               │
         ┌───────────▼─────┐  ┌──────▼───────────┐
         │  Data Service   │  │  Data Service    │
         │  PostgreSQL API │  │   MongoDB API    │
         │  (Port: 8001)   │  │   (Port: 8002)   │
         └─────────────────┘  └──────────────────┘
                 │                      │
         ┌───────▼─────────┐    ┌──────▼──────────┐
         │   PostgreSQL    │    │    MongoDB      │
         │    Database     │    │    Database     │
         └─────────────────┘    └─────────────────┘
```

---

## Core Architectural Principles

### 1. HTTP-Only Data Access ⚠️ MANDATORY

**Rule:** Business services NEVER access databases directly.

**Why:**
- ✅ Single source of truth for data access
- ✅ Easier to maintain and update
- ✅ Better connection pool management
- ✅ Clear separation of concerns
- ✅ Easy to add caching, validation, authorization at data layer

**Example:**

❌ **WRONG:**
```python
# Business service directly accessing database
from sqlalchemy import select

async def get_user(user_id: UUID) -> User:
    async with database.session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one()
```

✅ **CORRECT:**
```python
# Business service calling data API via HTTP
from httpx import AsyncClient

class UserDataClient:
    """Client for user data API."""

    def __init__(self, base_url: str):
        self.client = AsyncClient(base_url=base_url)

    async def get_user(self, user_id: UUID) -> User:
        """Get user from data API."""
        response = await self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        return User(**response.json())
```

### 2. Single Event Loop Ownership ⚠️ MANDATORY

**Rule:** Each service type runs in a separate process.

**Why:**
- ✅ No event loop conflicts
- ✅ Independent lifecycle management
- ✅ Easier debugging and monitoring
- ✅ Better resource isolation

**Service Types:**
- **FastAPI services** → Uvicorn process
- **Telegram bots** → Aiogram process
- **Background workers** → AsyncIO process

❌ **WRONG:**
```python
# Running FastAPI and Aiogram in same process
app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher()

# This will cause event loop conflicts!
```

✅ **CORRECT:**
```
services/
├── finance_lending_api/      # FastAPI in separate container
├── finance_notification_bot/  # Aiogram in separate container
└── finance_scoring_worker/    # AsyncIO in separate container
```

### 3. Async-First Design

**Rule:** All I/O operations must use async/await.

**Why:**
- ✅ Better performance under load
- ✅ Efficient resource utilization
- ✅ Natural backpressure handling
- ✅ Scales better

**Guidelines:**
- Use `async def` for all I/O operations
- Use `await` for all blocking calls
- Use async libraries (httpx, aiohttp, asyncpg)
- Never use blocking operations (`time.sleep`, `requests`, etc.)

### 4. Type Safety

**Rule:** Full type hints with mypy strict mode.

**Why:**
- ✅ Catch errors at development time
- ✅ Better IDE support
- ✅ Self-documenting code
- ✅ Easier refactoring

**Example:**
```python
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    """User entity with full type safety."""

    id: UUID
    email: str
    name: str
    is_active: bool


async def get_user(user_id: UUID) -> Optional[User]:
    """
    Get user by ID.

    Args:
        user_id: User unique identifier

    Returns:
        User entity or None if not found
    """
    # Implementation
    pass
```

### 5. Domain-Driven Design (DDD)

**Rule:** Clear domain boundaries and ubiquitous language.

**Structure:**
```
service/
├── domain/           # Pure business logic, no dependencies
│   ├── entities.py   # Domain entities
│   ├── value_objects.py
│   └── services.py   # Domain services
├── application/      # Use cases and application services
│   ├── services/
│   └── dtos/
├── infrastructure/   # External concerns (DB, HTTP, etc.)
│   ├── http/
│   ├── database/
│   └── messaging/
└── api/             # API layer (FastAPI routes)
    ├── routes/
    ├── dependencies.py
    └── schemas/
```

---

## Service Types

### 1. Business API (FastAPI)

**Purpose:** Handle HTTP requests, execute business logic.

**Characteristics:**
- FastAPI + Uvicorn
- RESTful API design
- No direct database access
- Calls data services via HTTP
- Port range: 8000-8099

**Example:**
```python
"""
Business API for user management.

Handles user registration, authentication, profile management.
"""

from fastapi import FastAPI, Depends
from uuid import UUID

app = FastAPI(title="Сервис управления пользователями")


@router.post("/users", summary="Регистрация пользователя")
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(),
) -> UserResponse:
    """
    Create new user.

    Args:
        request: User creation data
        user_service: User service dependency

    Returns:
        Created user data
    """
    user = await user_service.create_user(request)
    return UserResponse.from_entity(user)
```

### 2. Data API (FastAPI)

**Purpose:** Handle ALL database operations.

**Characteristics:**
- FastAPI + Uvicorn
- Direct database access (PostgreSQL, MongoDB)
- CRUD operations
- No business logic
- Port 8001 (PostgreSQL), 8002 (MongoDB)

**Example:**
```python
"""
Data API for user persistence.

Provides CRUD operations for user data in PostgreSQL.
"""

from fastapi import FastAPI, HTTPException
from sqlalchemy import select


@router.get("/users/{user_id}", summary="Получить пользователя")
async def get_user(user_id: UUID) -> UserResponse:
    """
    Get user by ID from database.

    Args:
        user_id: User identifier

    Returns:
        User data from database

    Raises:
        HTTPException: If user not found
    """
    async with database.session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404)
        return UserResponse.from_orm(user)
```

### 3. Worker (AsyncIO)

**Purpose:** Background task processing.

**Characteristics:**
- AsyncIO event loop
- Consumes from RabbitMQ
- Calls data services via HTTP
- No direct database access
- Long-running tasks

**Example:**
```python
"""
Worker for sending email notifications.

Consumes email tasks from RabbitMQ and sends emails.
"""

import asyncio
from aio_pika import connect_robust, IncomingMessage


async def process_email_task(message: IncomingMessage) -> None:
    """
    Process email task from queue.

    Args:
        message: RabbitMQ message with email data
    """
    async with message.process():
        data = json.loads(message.body)
        await send_email(
            to=data["to"],
            subject=data["subject"],
            body=data["body"],
        )
        logger.info("email_sent", to=data["to"])


async def main() -> None:
    """Main worker loop."""
    connection = await connect_robust("amqp://rabbitmq")
    channel = await connection.channel()
    queue = await channel.declare_queue("email_tasks")

    await queue.consume(process_email_task)
    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Bot (Aiogram)

**Purpose:** Telegram bot interface.

**Characteristics:**
- Aiogram 3.x
- Telegram Bot API
- Calls data services via HTTP
- No direct database access
- Event-driven handlers

**Example:**
```python
"""
Telegram bot for user notifications.

Handles user commands and sends notifications.
"""

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """
    Handle /start command.

    Args:
        message: Telegram message
    """
    await message.answer(
        "Добро пожаловать! Используйте /help для справки."
    )
    logger.info(
        "user_started_bot",
        user_id=message.from_user.id,
        username=message.from_user.username,
    )
```

---

## Data Access Pattern

### The Golden Rule

**Business services access data ONLY via HTTP calls to data services.**

### Why This Pattern?

1. **Single Source of Truth** — One place for all data access logic
2. **Better Connection Management** — Data services manage connection pools
3. **Easier to Optimize** — Add caching, batching at data layer
4. **Clear Boundaries** — Business logic vs data access
5. **Easy to Test** — Mock HTTP calls vs mocking database

### Implementation Example

**Data API Endpoint:**
```python
# services/finance_user_data_api/api/routes/users.py

@router.get("/users/{user_id}")
async def get_user(user_id: UUID) -> UserResponse:
    """Get user from PostgreSQL."""
    async with database.session() as session:
        user = await session.get(UserModel, user_id)
        if not user:
            raise HTTPException(status_code=404)
        return UserResponse.from_orm(user)
```

**Business API Client:**
```python
# services/finance_lending_api/infrastructure/http/user_client.py

class UserDataClient:
    """HTTP client for user data API."""

    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_user(self, user_id: UUID) -> User:
        """Get user via HTTP."""
        response = await self.client.get(f"/users/{user_id}")
        response.raise_for_status()
        return User(**response.json())
```

**Business Service Usage:**
```python
# services/finance_lending_api/application/services/loan_service.py

class LoanService:
    """Loan application business logic."""

    def __init__(self, user_client: UserDataClient):
        self.user_client = user_client

    async def apply_for_loan(
        self, user_id: UUID, amount: Decimal
    ) -> Loan:
        """
        Process loan application.

        Args:
            user_id: Applicant user ID
            amount: Loan amount

        Returns:
            Created loan application
        """
        # Get user via HTTP (not direct DB!)
        user = await self.user_client.get_user(user_id)

        # Business logic
        if not user.is_verified:
            raise UnverifiedUserError()

        # Create loan...
        return loan
```

---

## Communication Patterns

### 1. Synchronous: HTTP/REST

**When to use:**
- Request-response interactions
- Data retrieval
- CRUD operations

**Example:**
```python
# Business API → Data API
user = await user_data_client.get_user(user_id)
```

### 2. Asynchronous: RabbitMQ Events

**When to use:**
- Fire-and-forget operations
- Event notifications
- Background processing
- Cross-service communication

**Example:**
```python
# Publish event
await event_publisher.publish(
    "user.created",
    {"user_id": str(user.id), "email": user.email}
)

# Consume event (in worker)
async def handle_user_created(event: dict) -> None:
    """Send welcome email when user created."""
    await send_welcome_email(event["email"])
```

---

## DDD & Hexagonal Architecture

### Layer Responsibilities

**Domain Layer** (Pure business logic):
- Entities, Value Objects
- Domain Services
- Business Rules
- No external dependencies

**Application Layer** (Use cases):
- Application Services
- DTOs
- Orchestrates domain objects
- Calls infrastructure

**Infrastructure Layer** (External concerns):
- HTTP clients
- Database repositories
- Message brokers
- External APIs

**API Layer** (Entry point):
- FastAPI routes
- Request/Response schemas
- Dependency injection
- Input validation

---

## Technology Decisions

### Why FastAPI?
- ✅ Async-first
- ✅ Automatic OpenAPI docs
- ✅ Type hints native support
- ✅ High performance
- ✅ Easy dependency injection

### Why PostgreSQL?
- ✅ ACID transactions
- ✅ Rich query capabilities
- ✅ JSON support
- ✅ Proven reliability
- ✅ Great async support (asyncpg)

### Why MongoDB?
- ✅ Flexible schema
- ✅ Document storage
- ✅ Horizontal scalability
- ✅ Good for unstructured data

### Why RabbitMQ?
- ✅ Message persistence
- ✅ Flexible routing
- ✅ Dead letter queues
- ✅ Management UI
- ✅ Battle-tested

### Why Redis?
- ✅ Fast caching
- ✅ Session storage
- ✅ Rate limiting
- ✅ Pub/Sub support

---

## Quality Standards

### Type Checking
- mypy strict mode
- Full type hints
- No `Any` types without justification

### Testing
- >80% code coverage
- Unit tests for business logic
- Integration tests for API endpoints
- E2E tests for critical paths

### Linting
- Ruff for Python linting
- Consistent code style
- Pre-commit hooks

### Documentation
- Docstrings in English
- User messages in Russian
- Comprehensive guides
- Architecture decision records

---

## Deployment Architecture

### Development
```
docker-compose.dev.yml
├── All services in one compose file
├── Shared network
├── Volume mounts for hot reload
└── Debug logging enabled
```

### Production
```
Kubernetes Cluster
├── Service per deployment
├── Horizontal Pod Autoscaler
├── Ingress for routing
├── ConfigMaps and Secrets
└── Persistent volumes for databases
```

---

## Best Practices

1. **Never bypass the data API** — Always use HTTP to access data
2. **One service type per container** — No mixed responsibilities
3. **Use async/await consistently** — No blocking operations
4. **Type everything** — Full type hints
5. **Log structurally** — JSON logs with context
6. **Monitor everything** — Metrics, traces, logs
7. **Test thoroughly** — Unit, integration, E2E
8. **Document decisions** — ADRs for important choices

---

## Anti-Patterns to Avoid

❌ **Direct database access from business services**
❌ **Mixing FastAPI and Aiogram in one process**
❌ **Using blocking operations in async code**
❌ **Missing type hints**
❌ **Unstructured logging**
❌ **No health checks**
❌ **Tight coupling between services**

---

## Further Reading

- [Architecture Guide (Detailed)](docs/guides/architecture-guide.md)
- [Project Structure](docs/reference/project-structure.md)
- [Technology Stack](docs/reference/tech_stack.md)
- [Service Templates](templates/README.md)

---

**Last Updated:** 2025-01-05
**Version:** 0.1.0
