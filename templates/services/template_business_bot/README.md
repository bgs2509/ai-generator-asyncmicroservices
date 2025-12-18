# Telegram Bot Service Template

**Status**: ✅ Complete (100%)
**Purpose**: Aiogram-based Telegram bot for business logic

## Overview

This template provides an Aiogram 3.x based Telegram bot service following the framework's architecture principles for user interaction through messaging.

## Key Features

- Aiogram 3.x async bot framework
- Command and message handlers
- Inline keyboards and callbacks
- State management with FSM
- Middleware for logging and auth
- HTTP calls to data services via shared/http_clients
- Integration with RabbitMQ via shared/rabbitmq
- DRY-compliant: uses shared/ infrastructure

## Architecture Compliance

Following the mandatory service separation:
- Runs as separate container/process
- Calls data services via HTTP only (DataApiClient)
- Publishes events to RabbitMQ (RabbitMQPublisher)
- No direct database access
- Stateless design (state in Redis)

## Service Structure

```
template_business_bot/
├── Dockerfile              # Multi-stage build
├── requirements.txt        # Dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── main.py            # Bot entry point with lifespan
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py      # Pydantic Settings
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers/       # Command and message handlers
│   │   │   ├── __init__.py
│   │   │   ├── start.py   # /start command
│   │   │   ├── help.py    # /help command
│   │   │   └── common.py  # Unknown message handler
│   │   ├── middlewares/    # Custom middleware
│   │   │   ├── __init__.py
│   │   │   └── logging.py # Logging middleware
│   │   ├── keyboards/      # Keyboard layouts
│   │   │   ├── __init__.py
│   │   │   └── inline.py  # Inline keyboard builders
│   │   └── states/         # FSM states
│   │       ├── __init__.py
│   │       └── user_states.py
│   └── infrastructure/     # Re-exports from shared/
│       └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py         # Imports shared.testing fixtures
    └── test_handlers.py    # Handler tests
```

## DRY Compliance

This template uses shared infrastructure:

```python
# In src/main.py - imports from shared/
from shared.utils.logger import create_logger
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

1. **Rename the service**: Replace `template_business_bot` with your actual service name (e.g., `healthcare_appointment_bot`)
2. **Set bot token**: Configure BOT_TOKEN in environment
3. **Define handlers**: Create command and message handlers in src/bot/handlers/
4. **Setup keyboards**: Design user interaction flows in src/bot/keyboards/
5. **Define states**: Add FSM states for multi-step flows in src/bot/states/
6. **Configure data access**: Use DataApiClient from shared/http_clients

## Environment Variables

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
BOT_WEBHOOK_SECRET=your_webhook_secret_here

# Application Settings
APP_NAME=template_business_bot
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=true

# Data Service URL (HTTP-only access)
DATA_API_URL=http://data-postgres-api:8000/api/v1

# RabbitMQ Configuration
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/

# Redis Configuration (for FSM storage)
REDIS_URL=redis://redis:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Health Check Server
HEALTH_CHECK_PORT=8080
```

## Bot Commands

- `/start` - Initialize bot interaction
- `/help` - Show available commands

Add your custom commands by creating new handler files.

## Related Documentation

- [Aiogram Patterns](../../../docs/atomic/services/aiogram/)
- [Redis Integration](../../../docs/atomic/integrations/redis/)
- [RabbitMQ Events](../../../docs/atomic/integrations/rabbitmq/)
- [HTTP Communication](../../../docs/atomic/integrations/http-communication/)
- [Shared Components Guide](../../../docs/guides/shared-components.md)
