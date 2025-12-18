# FastAPI Business Service Template

**Status**: ✅ Complete (100%)
**Purpose**: Business logic API service following the Improved Hybrid Approach

## Overview

This template provides a FastAPI-based business service that implements business logic, orchestrates data access via HTTP calls to data services, and publishes events to RabbitMQ.

## Key Features

- Business logic orchestration
- HTTP-only data access via shared/http_clients (DataApiClient)
- Event publishing to RabbitMQ via shared/rabbitmq (RabbitMQPublisher)
- Request ID middleware via shared/middleware (RequestIdMiddleware)
- Health check endpoints for Kubernetes probes
- RESTful API design with OpenAPI documentation
- DRY-compliant: uses shared/ infrastructure

## Architecture Compliance

Following the mandatory Improved Hybrid Approach:
- Business logic separated from data access
- HTTP calls to data services (no direct DB access)
- Event-driven communication via RabbitMQ
- Redis for cross-service state management
- Stateless API design

## Service Structure

```
template_business_api/
├── Dockerfile              # Multi-stage build
├── requirements.txt        # Dependencies
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── main.py            # FastAPI application with lifespan
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py      # Pydantic Settings (comprehensive)
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py  # Health endpoints
│   └── schemas/
│       ├── __init__.py
│       └── base.py        # Base response schemas
└── tests/
    ├── __init__.py
    ├── conftest.py         # Imports shared.testing fixtures
    └── test_health.py      # Health endpoint tests
```

## DRY Compliance

This template uses shared infrastructure:

```python
# In src/main.py - imports from shared/
from shared.utils.logger import create_logger
from shared.middleware import RequestIdMiddleware
from shared.http_clients import DataApiClient
from shared.rabbitmq import RabbitMQPublisher

# In tests/conftest.py - imports shared fixtures
from shared.testing.base_fixtures import (
    mock_data_client,
    mock_rabbitmq_publisher,
)
```

## Usage

When using this template:

1. **Rename the service**: Replace `template_business_api` with your actual service name (e.g., `finance_lending_api`)
2. **Configure integrations**: Update settings in .env for Redis, RabbitMQ, and data services
3. **Define business entities**: Create Pydantic schemas in src/schemas/
4. **Implement business logic**: Add service classes in src/services/ (create directory)
5. **Create API endpoints**: Define routers in src/api/v1/
6. **Set up event publishing**: Use app.state.publisher for event publishing

## Example Endpoint Pattern

```python
# src/api/v1/users.py
from fastapi import APIRouter, Request

from shared.utils.logger import create_logger
from src.schemas.user import UserCreate, UserResponse

logger = create_logger(__name__)
router = APIRouter(prefix="/users")


@router.post("/", response_model=UserResponse)
async def create_user(request: Request, user_in: UserCreate) -> UserResponse:
    data_client = request.app.state.data_client
    publisher = request.app.state.publisher

    # Create via Data Service
    result = await data_client.post("/users", user_in)

    # Publish event
    await publisher.publish(
        "users",
        "user.created",
        {"user_id": result["id"]},
    )

    return UserResponse(**result)
```

## Environment Variables

See `src/core/config.py` for full list. Key variables:

```env
PROJECT_NAME=MyApp
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=info

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Data service URLs (HTTP-only access)
POSTGRES_SERVICE_URL=http://data-postgres-api:8000

# Redis configuration
REDIS_URL=redis://redis:6379/0

# RabbitMQ configuration
RABBITMQ_URL=amqp://admin:admin@rabbitmq:5672/
```

## Health Endpoints

- `GET /api/v1/health/live` - Liveness probe (is process running?)
- `GET /api/v1/health/ready` - Readiness probe (can serve traffic?)

## Related Documentation

- [Architecture Guide](../../../docs/guides/architecture-guide.md)
- [Business Service Patterns](../../../docs/atomic/services/fastapi/)
- [HTTP Communication](../../../docs/atomic/integrations/http-communication/)
- [Event Publishing](../../../docs/atomic/integrations/rabbitmq/)
- [Shared Components Guide](../../../docs/guides/shared-components.md)
