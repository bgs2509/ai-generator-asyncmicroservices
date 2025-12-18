# AsyncIO Worker Service Template

**Status**: ✅ Complete (100%)
**Purpose**: Background task processing with AsyncIO and RabbitMQ

## Overview

This template provides an AsyncIO-based background worker service for processing tasks asynchronously through RabbitMQ message queues.

## Key Features

- Pure AsyncIO implementation
- RabbitMQ consumer via shared/rabbitmq
- Task routing by event type
- Graceful shutdown handling
- HTTP calls to data services via shared/http_clients
- Structured logging with correlation IDs
- DRY-compliant: uses shared/ infrastructure

## Architecture Compliance

Following the mandatory service separation:
- Runs as separate container/process
- Consumes messages from RabbitMQ (RabbitMQConsumer)
- Calls data services via HTTP only (DataApiClient)
- No direct database access
- Stateless processing

## Service Structure

```
template_business_worker/
├── Dockerfile              # Multi-stage build
├── requirements.txt        # Dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── main.py            # Worker entry point with lifespan
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py      # Pydantic Settings
│   └── worker/
│       ├── __init__.py
│       ├── task_processor.py  # Routes messages to handlers
│       └── handlers/
│           ├── __init__.py
│           └── example_handler.py  # Example event handlers
└── tests/
    ├── __init__.py
    ├── conftest.py         # Imports shared.testing fixtures
    └── test_task_processor.py
```

## DRY Compliance

This template uses shared infrastructure:

```python
# In src/main.py - imports from shared/
from shared.utils.logger import create_logger
from shared.http_clients import DataApiClient
from shared.rabbitmq import RabbitMQConsumer

# In tests/conftest.py - imports shared fixtures
from shared.testing.base_fixtures import (
    mock_data_client,
    mock_rabbitmq_consumer,
)
```

## Usage

When using this template:

1. **Rename the service**: Replace `template_business_worker` with your actual service name (e.g., `finance_lending_worker`)
2. **Configure RabbitMQ**: Set RABBITMQ_URL and QUEUE_NAME in environment
3. **Define handlers**: Create event handlers in src/worker/handlers/
4. **Register handlers**: Add handlers to TaskProcessor._handlers dict
5. **Implement business logic**: Process events with DataApiClient

## Event Handler Pattern

```python
# src/worker/handlers/your_handler.py
async def handle_your_event(
    message: dict[str, Any],
    data_client: DataApiClient,
) -> None:
    entity_id = message.get("entity_id")
    # Fetch data from Data Service
    entity = await data_client.get(f"/entities/{entity_id}")
    # Perform business logic
    # ...
```

## Environment Variables

```env
# Application Settings
APP_NAME=template_business_worker
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=true

# Queue Configuration
QUEUE_NAME=default_queue

# Data Service URL (HTTP-only access)
DATA_API_URL=http://data-postgres-api:8000/api/v1

# RabbitMQ Configuration
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Worker Settings
PREFETCH_COUNT=10
MAX_RETRIES=3
RETRY_DELAY_SECONDS=5
```

## Graceful Shutdown

The worker handles SIGTERM and SIGINT signals for graceful shutdown:
- Stops consuming new messages
- Waits for current message processing to complete
- Closes connections cleanly

## Related Documentation

- [AsyncIO Workers](../../../docs/atomic/services/asyncio-workers/)
- [RabbitMQ Integration](../../../docs/atomic/integrations/rabbitmq/)
- [HTTP Communication](../../../docs/atomic/integrations/http-communication/)
- [Shared Components Guide](../../../docs/guides/shared-components.md)
