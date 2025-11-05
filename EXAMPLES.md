# Examples

Real-world examples and use cases demonstrating how to use the AI Generator for Async Microservices framework.

---

## 📚 Table of Contents

1. [Quick Examples](#quick-examples)
2. [Complete Project Examples](#complete-project-examples)
3. [Service Type Examples](#service-type-examples)
4. [Integration Patterns](#integration-patterns)
5. [Production Patterns](#production-patterns)

---

## Quick Examples

### Example 1: Simple E-commerce Platform

**Scenario:** Building a basic e-commerce platform with product catalog and orders.

```
MY PROJECT:

What I'm building:
Simple e-commerce platform for online store

Problem it solves:
Small business needs online presence for selling products

Key features:
- Product catalog management
- Shopping cart
- Order processing
- User accounts

How complex should it be:
Simple prototype

Additional services needed:
Not sure
```

**Generated Structure:**
```
my-ecommerce/
├── services/
│   ├── ecommerce_product_api/        # Business API for products
│   ├── ecommerce_order_api/          # Business API for orders
│   ├── ecommerce_user_data_api/      # Data API (PostgreSQL)
│   └── ecommerce_notification_worker/ # Worker for email notifications
├── infrastructure/
│   ├── docker-compose.yml
│   └── docker-compose.dev.yml
└── nginx/
    └── conf.d/
        └── ecommerce.conf
```

**Key Benefits:**
- ✅ Consistent naming: `ecommerce_{domain}_{type}`
- ✅ Clear separation: Business logic vs Data access
- ✅ Ready infrastructure: Docker + Nginx configured
- ✅ Production patterns: Health checks, logging, metrics

---

### Example 2: Telemedicine Platform

**Scenario:** Healthcare platform for remote doctor consultations.

```
MY PROJECT:

What I'm building:
Telemedicine platform for remote doctor consultations

Problem it solves:
Patients can't easily access doctors remotely, especially in rural areas

Key features:
- Patient registration and profiles
- Doctor scheduling and availability
- Video consultation sessions
- Medical records storage
- Prescription management
- Appointment reminders

How complex should it be:
Development version

Additional services needed:
- Telegram bot for appointment reminders
- Background workers for notifications
- File storage for medical documents
```

**Generated Structure:**
```
telemedicine-platform/
├── services/
│   ├── healthcare_patient_api/           # Business API for patients
│   ├── healthcare_doctor_api/            # Business API for doctors
│   ├── healthcare_appointment_api/       # Business API for appointments
│   ├── healthcare_consultation_api/      # Business API for consultations
│   ├── healthcare_prescription_api/      # Business API for prescriptions
│   ├── healthcare_user_data_api/         # Data API - User data (PostgreSQL)
│   ├── healthcare_medical_data_api/      # Data API - Medical records (MongoDB)
│   ├── healthcare_notification_worker/   # Worker for email/SMS notifications
│   └── healthcare_reminder_bot/          # Telegram bot for reminders
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── postgres/
│   ├── mongodb/
│   ├── redis/
│   └── rabbitmq/
└── nginx/
    └── conf.d/
        ├── patient-api.conf
        ├── doctor-api.conf
        └── appointment-api.conf
```

**Architecture Highlights:**
- **PostgreSQL** for user data (patients, doctors)
- **MongoDB** for medical records (flexible schema)
- **Redis** for session management and caching
- **RabbitMQ** for async communication
- **Telegram Bot** for appointment reminders
- **Worker** for email/SMS notifications

---

### Example 3: P2P Lending Platform

**Scenario:** Peer-to-peer lending marketplace.

```
MY PROJECT:

What I'm building:
P2P lending platform connecting borrowers with lenders

Problem it solves:
Traditional banks have high interest rates and strict requirements

Key features:
- Borrower and lender registration
- Loan application and approval
- Investment management
- Credit scoring
- Payment processing
- Transaction history

How complex should it be:
Production-ready

Additional services needed:
- Background scoring worker
- Payment processing integration
- Real-time notifications
```

**Generated Structure:**
```
p2p-lending/
├── services/
│   ├── finance_user_api/              # Business API for users
│   ├── finance_loan_api/              # Business API for loans
│   ├── finance_investment_api/        # Business API for investments
│   ├── finance_payment_api/           # Business API for payments
│   ├── finance_scoring_api/           # Business API for credit scoring
│   ├── finance_user_data_api/         # Data API - Users (PostgreSQL)
│   ├── finance_transaction_data_api/  # Data API - Transactions (PostgreSQL)
│   ├── finance_scoring_worker/        # Worker for credit scoring
│   ├── finance_payment_worker/        # Worker for payment processing
│   └── finance_notification_bot/      # Telegram bot for notifications
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── monitoring/
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   └── jaeger/
│   └── elk/
└── nginx/
    └── conf.d/
        ├── api-gateway.conf
        └── ssl/
```

**Production Features:**
- ✅ Complete observability (Prometheus + Grafana + Jaeger)
- ✅ Centralized logging (ELK stack)
- ✅ SSL/TLS configuration
- ✅ Rate limiting and security
- ✅ Database backups and replication
- ✅ CI/CD pipelines

---

## Complete Project Examples

### Full Example: Task Management System

**Requirements:**
```
MY PROJECT:

What I'm building:
Team task management and collaboration platform

Problem it solves:
Teams need to organize work, track progress, and collaborate

Key features:
- Projects and task management
- Team collaboration
- Real-time updates
- File attachments
- Comments and discussions
- Activity timeline

How complex should it be:
Development version

Additional services needed:
- WebSocket for real-time updates
- File storage
- Background workers for notifications
```

**Step 1: AI Generates Project Structure**

```bash
task-management/
├── .ai-framework/                    # Framework as submodule
├── services/
│   ├── task_project_api/            # Projects management
│   ├── task_task_api/               # Tasks CRUD
│   ├── task_comment_api/            # Comments and discussions
│   ├── task_file_api/               # File uploads
│   ├── task_realtime_api/           # WebSocket server
│   ├── task_project_data_api/       # Data API (PostgreSQL)
│   ├── task_notification_worker/    # Email notifications
│   └── task_activity_worker/        # Activity timeline
├── infrastructure/
├── nginx/
└── README.md
```

**Step 2: Domain Models Generated**

`services/task_project_api/domain/entities.py`:
```python
"""
Domain entities for project management.

This module defines core business entities.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class Project:
    """
    Project entity representing a work project.

    Attributes:
        id: Unique project identifier
        name: Project name
        description: Project description
        owner_id: User who owns the project
        created_at: Project creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


@dataclass(frozen=True)
class Task:
    """
    Task entity representing a work item.

    Attributes:
        id: Unique task identifier
        project_id: Parent project identifier
        title: Task title
        description: Task description
        assignee_id: User assigned to task
        status: Task status (TODO, IN_PROGRESS, DONE)
        priority: Task priority (LOW, MEDIUM, HIGH)
        due_date: Task deadline
        created_at: Task creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    project_id: UUID
    title: str
    description: str
    assignee_id: Optional[UUID]
    status: str  # TODO, IN_PROGRESS, DONE
    priority: str  # LOW, MEDIUM, HIGH
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

**Step 3: API Endpoints Generated**

`services/task_project_api/api/routes/projects.py`:
```python
"""
API routes for project management.

This module defines REST API endpoints for projects.
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_project_service
from ..schemas.requests import CreateProjectRequest, UpdateProjectRequest
from ..schemas.responses import ProjectResponse
from ...application.services.project_service import ProjectService


router = APIRouter(prefix="/projects", tags=["Проекты"])


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать проект",
    description="Создание нового проекта для организации задач",
)
async def create_project(
    request: CreateProjectRequest,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """
    Create new project.

    Args:
        request: Project creation data
        service: Project service dependency

    Returns:
        Created project data
    """
    project = await service.create_project(
        name=request.name,
        description=request.description,
        owner_id=request.owner_id,
    )
    return ProjectResponse.from_entity(project)


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Получить проект",
    description="Получение информации о проекте по ID",
)
async def get_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    """
    Get project by ID.

    Args:
        project_id: Project unique identifier
        service: Project service dependency

    Returns:
        Project data

    Raises:
        HTTPException: If project not found
    """
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Проект {project_id} не найден",
        )
    return ProjectResponse.from_entity(project)


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Список проектов",
    description="Получение списка всех проектов пользователя",
)
async def list_projects(
    owner_id: UUID,
    service: ProjectService = Depends(get_project_service),
) -> List[ProjectResponse]:
    """
    List all projects for user.

    Args:
        owner_id: User identifier
        service: Project service dependency

    Returns:
        List of projects
    """
    projects = await service.list_projects(owner_id)
    return [ProjectResponse.from_entity(p) for p in projects]
```

**Note:** All documentation, comments, and docstrings are in **English**, while user-facing messages (API responses, error messages) are in **Russian**.

---

## Service Type Examples

### Business API Example

**Use Case:** User authentication service

```python
# services/auth_user_api/api/routes/auth.py
"""
Authentication API routes.

Handles user login, logout, and token refresh.
"""

@router.post("/login", summary="Вход в систему")
async def login(credentials: LoginRequest) -> TokenResponse:
    """User login endpoint."""
    # Business logic here
    pass
```

### Data API Example

**Use Case:** User data persistence

```python
# services/auth_user_data_api/api/routes/users.py
"""
User data API routes.

Provides CRUD operations for user data.
"""

@router.get("/users/{user_id}", summary="Получить пользователя")
async def get_user(user_id: UUID) -> UserResponse:
    """Get user by ID from database."""
    # Data access here
    pass
```

### Worker Example

**Use Case:** Email notification sender

```python
# services/notification_email_worker/worker.py
"""
Email notification worker.

Consumes email tasks from RabbitMQ and sends emails.
"""

async def process_email_task(task: EmailTask) -> None:
    """Process and send email."""
    # Worker logic here
    pass
```

### Bot Example

**Use Case:** Telegram notification bot

```python
# services/notification_telegram_bot/handlers/notifications.py
"""
Notification handlers for Telegram bot.

Sends notifications to users via Telegram.
"""

@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    """Handle /start command."""
    await message.answer("Добро пожаловать!")
```

---

## Integration Patterns

### HTTP Communication

**Business API → Data API:**

```python
"""
HTTP client for data API communication.

All business services communicate with data services via HTTP only.
"""

from typing import Optional
import httpx

from ..domain.entities import User


class UserDataClient:
    """Client for user data API."""

    def __init__(self, base_url: str):
        """
        Initialize client.

        Args:
            base_url: Data API base URL
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        """
        Get user by ID from data API.

        Args:
            user_id: User identifier

        Returns:
            User entity or None if not found
        """
        response = await self.client.get(
            f"{self.base_url}/users/{user_id}"
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        return User(**data)
```

### RabbitMQ Integration

**Publishing events:**

```python
"""
Event publisher for RabbitMQ.

Publishes domain events to message broker.
"""

from aio_pika import Message, connect_robust


class EventPublisher:
    """RabbitMQ event publisher."""

    async def publish_user_created(self, user_id: UUID) -> None:
        """
        Publish user created event.

        Args:
            user_id: Created user identifier
        """
        connection = await connect_robust("amqp://rabbitmq")
        channel = await connection.channel()

        message = Message(
            body=json.dumps({"user_id": str(user_id)}).encode()
        )
        await channel.default_exchange.publish(
            message,
            routing_key="user.created"
        )
```

---

## Production Patterns

### Health Checks

```python
"""
Health check endpoints.

Provides liveness and readiness probes for Kubernetes.
"""

@router.get("/health/live", summary="Проверка работоспособности")
async def liveness() -> dict:
    """Liveness probe."""
    return {"status": "alive"}


@router.get("/health/ready", summary="Проверка готовности")
async def readiness(
    db: Database = Depends(get_database),
) -> dict:
    """Readiness probe with database check."""
    await db.execute("SELECT 1")
    return {"status": "ready"}
```

### Structured Logging

```python
"""
Structured logging configuration.

All logs are JSON-formatted for easy parsing.
"""

import structlog

logger = structlog.get_logger()

await logger.ainfo(
    "user_created",
    user_id=str(user.id),
    email=user.email,
    request_id=request_id,
)
```

### Metrics

```python
"""
Prometheus metrics.

Exposes business and technical metrics.
"""

from prometheus_client import Counter, Histogram

user_created = Counter(
    "user_created_total",
    "Total users created"
)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration"
)
```

---

## Next Steps

1. **Try the Quick Start**: Follow the [Quick Start Guide](docs/getting-started/quick-start.md)
2. **Read the Guides**: Check [AI Code Generation Workflow](docs/guides/ai-code-generation-master-workflow.md)
3. **Explore Templates**: See [Service Templates](templates/README.md)
4. **Join Community**: Ask questions in [GitHub Discussions](https://github.com/bgs2509/ai-generator-asyncmicroservices/discussions)

---

**More examples coming soon!** We're working on:
- Complete telemedicine platform example
- P2P lending platform example
- IoT data collection system
- Real-time chat application

---

**Last Updated:** 2025-01-05
