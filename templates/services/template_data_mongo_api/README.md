# MongoDB Data Service Template

**Status**: ✅ 100% Complete
**Purpose**: HTTP-only data access service for MongoDB database

## Overview

This template provides a FastAPI-based HTTP data service that exposes MongoDB database operations following the framework's Improved Hybrid Approach architecture.

## Key Features

- HTTP-only data access (no direct DB access from business services)
- RESTful CRUD operations for documents
- Motor async MongoDB driver
- Schema validation with Pydantic
- Aggregation pipeline support
- ObjectId handling with Pydantic
- Health check endpoints

## Architecture Compliance

Following the mandatory Improved Hybrid Approach:
- Business services call this service via HTTP
- No direct database connections from business layer
- Stateless HTTP API design
- MongoDB for document storage

## Service Structure

```
template_data_mongo_api/
├── src/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Pydantic Settings for MongoDB
│   │   └── database.py             # Motor connection and pool
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py                 # Base Pydantic models with ObjectId
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base_repository.py      # Generic MongoDB CRUD repository
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── base.py                 # API response schemas
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── health.py           # Health check endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Shared fixtures
│   └── test_health.py              # Health endpoint tests
├── Dockerfile                      # Multi-stage build
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
├── .env.example                    # Environment template
├── pytest.ini                      # Pytest configuration
└── README.md                       # This file
```

## Usage

When using this template:

1. **Rename the service**: Replace `template_data_mongo_api` with your actual service name (e.g., `analytics_data_mongo_api`)
2. **Configure MongoDB**: Update connection settings in `.env`
3. **Define models**: Create Pydantic models for your documents in `src/models/`
4. **Implement repositories**: Add collection-specific repositories in `src/repositories/`
5. **Define API endpoints**: Create routers for your collections in `src/api/v1/`
6. **Setup indexes**: Configure MongoDB indexes for performance

## Example: Adding a New Collection

```python
# src/models/user.py
from src.models.base import TimestampedMongoModel

class UserDocument(TimestampedMongoModel):
    """User document model."""
    email: str
    name: str
    is_active: bool = True

# src/repositories/user_repository.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.repositories.base_repository import BaseMongoRepository
from src.models.user import UserDocument

class UserRepository(BaseMongoRepository[UserDocument]):
    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users", UserDocument)

    async def get_by_email(self, email: str) -> UserDocument | None:
        return await self.find_one({"email": email})

# src/api/v1/users.py
from fastapi import APIRouter, Depends
from src.core.database import get_database
from src.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: str, db=Depends(get_database)):
    repo = UserRepository(db)
    return await repo.get_by_id(user_id)
```

## API Endpoints

### Health Checks
- `GET /health/` - Liveness probe (is service running?)
- `GET /health/ready` - Readiness probe (is MongoDB connected?)

### Root
- `GET /` - Service information

### Business Endpoints (add your own)
- `POST /documents` - Create document
- `GET /documents/{id}` - Get document by ID
- `PUT /documents/{id}` - Update document
- `DELETE /documents/{id}` - Delete document
- `GET /documents` - List documents with pagination
- `POST /documents/aggregate` - Run aggregation pipeline

## Environment Variables

```env
# Application
APP_NAME=data_mongo_api
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Server
HOST=0.0.0.0
PORT=8002
WORKERS=4

# MongoDB
MONGODB_URL=mongodb://mongo:27017
DATABASE_NAME=app_db
MAX_POOL_SIZE=20
MIN_POOL_SIZE=5
CONNECT_TIMEOUT_MS=10000
SERVER_SELECTION_TIMEOUT_MS=10000

# Testing
TESTING=false
TEST_DATABASE_NAME=app_test_db

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Repository Methods

The `BaseMongoRepository` provides these methods:

| Method | Description |
|--------|-------------|
| `get_by_id(id)` | Get document by ObjectId |
| `get_all(skip, limit, sort_field, sort_order, filters)` | Get paginated documents |
| `create(model)` | Create document from model |
| `create_from_dict(data)` | Create document from dict |
| `update(id, update_data)` | Update document fields |
| `update_raw(id, update)` | Update with MongoDB operators |
| `delete(id)` | Delete document |
| `count(filters)` | Count documents |
| `exists(id)` | Check if document exists |
| `find_one(filters)` | Find single document |
| `find_many(filters, ...)` | Find multiple documents |
| `bulk_create(models)` | Bulk insert documents |
| `bulk_delete(ids)` | Bulk delete documents |
| `aggregate(pipeline)` | Run aggregation pipeline |

## Query Examples

```python
# Basic CRUD
user = await repo.create(UserDocument(email="john@example.com", name="John"))
user = await repo.get_by_id("507f1f77bcf86cd799439011")
user = await repo.update(user.id, {"name": "Jane"})
deleted = await repo.delete(user.id)

# Queries
users = await repo.find_many({"is_active": True}, limit=20)
count = await repo.count({"is_active": True})

# Aggregation
pipeline = [
    {"$match": {"is_active": True}},
    {"$group": {"_id": "$role", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = await repo.aggregate(pipeline)
```

## DRY Compliance

This template imports from `shared/`:

```python
from shared.utils.logger import create_logger
# from shared.middleware import RequestIdMiddleware  # Optional
```

## Running the Service

```bash
# Development (with hot reload)
uvicorn src.main:app --host 0.0.0.0 --port 8002 --reload

# Production (with Docker)
docker build -t data_mongo_api --target production .
docker run -p 8002:8002 data_mongo_api

# Testing
pytest tests/ -v
```

## Related Documentation

- [Data Access Architecture](../../../docs/atomic/architecture/data-access-architecture.md)
- [HTTP Communication Patterns](../../../docs/atomic/integrations/http-communication/)
- [MongoDB Infrastructure Setup](../../../docs/atomic/infrastructure/databases/mongodb-setup.md)

---

## Implementation Status

**Current completion: 100%**

### Completed
- [x] `src/main.py` — FastAPI app factory with lifespan
- [x] `src/core/config.py` — Pydantic Settings for MongoDB
- [x] `src/core/database.py` — Motor connection and pool
- [x] `src/models/base.py` — Base Pydantic models with ObjectId handling
- [x] `src/repositories/base_repository.py` — Generic MongoDB CRUD repository
- [x] `src/schemas/base.py` — API response schemas
- [x] `src/api/v1/health.py` — Health check endpoints
- [x] `Dockerfile` — Multi-stage build (dev + production)
- [x] `requirements.txt` — Production dependencies
- [x] `requirements-dev.txt` — Development dependencies
- [x] `.env.example` — Environment template
- [x] `pytest.ini` — Pytest configuration
- [x] `tests/conftest.py` — Shared fixtures
- [x] `tests/test_health.py` — Health endpoint tests
- [x] README.md with comprehensive documentation

---

**Note**: This is a production-ready template. Add your business-specific collections, models, and endpoints following the patterns shown above.
