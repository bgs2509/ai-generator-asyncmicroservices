# PostgreSQL Data API Service Template

**Status:** ✅ Complete (100%)
**Purpose:** HTTP-based PostgreSQL data access layer

Part of the Improved Hybrid Approach architecture - provides centralized database access via HTTP endpoints.

## 🎯 Purpose

This template implements the **Data Service** pattern where:
- ✅ **Single source of truth** for PostgreSQL database operations
- ✅ All business services access data via HTTP (no direct DB connections)
- ✅ Enforces DRY principle (no duplicated database queries)
- ✅ Async SQLAlchemy 2.0+ with full type safety
- ✅ Alembic migrations for schema management

## 📦 What's Included

### Core Features

- **Async SQLAlchemy 2.0+** with asyncpg driver
- **Alembic migrations** for database schema versioning
- **Generic CRUD repository** eliminates boilerplate
- **Health check endpoints** (/health, /health/ready)
- **Type-safe** with 100% type hints (mypy strict mode)
- **Production-ready** with connection pooling, error handling

### File Structure (27 files)

```
template_data_postgres_api/
├── Dockerfile                   # Multi-stage (dev + production)
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development/testing dependencies
├── pytest.ini                   # Pytest configuration
├── .env.example                 # Environment variables template
├── alembic.ini                  # Alembic configuration
├── alembic/
│   ├── env.py                   # Alembic environment (async support)
│   ├── script.py.mako           # Migration template
│   └── versions/                # Migration files go here
├── src/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application
│   ├── core/
│   │   ├── config.py            # Pydantic Settings
│   │   └── database.py          # SQLAlchemy async setup
│   ├── models/
│   │   └── base.py              # Base model + mixins
│   ├── repositories/
│   │   └── base_repository.py  # Generic CRUD repository
│   ├── schemas/
│   │   └── base.py              # Pydantic base schemas
│   └── api/v1/
│       └── health.py            # Health check endpoints
└── tests/
    ├── conftest.py              # Test fixtures (Testcontainers)
    ├── unit/                    # Unit tests
    └── integration/             # Integration tests
```

## 🚀 Quick Start

### 1. Copy Template

```bash
cp -r templates/services/template_data_postgres_api services/{{service_name}}
cd services/{{service_name}}
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### 4. Run Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 5. Start Service

```bash
# Development (with hot reload)
uvicorn src.main:app --reload

# Production
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 6. Verify

```bash
# Health check
curl http://localhost:8000/health

# Readiness check (includes database connectivity)
curl http://localhost:8000/health/ready

# API docs
open http://localhost:8000/docs
```

## 📝 Adding a New Model

See detailed usage guide with code examples:
- Adding models
- Creating repositories
- Defining schemas
- Creating API endpoints
- Writing migrations

Full examples in template documentation.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run only unit tests
pytest tests/unit/ -m unit

# Run only integration tests (uses Testcontainers)
pytest tests/integration/ -m integration

# With coverage
pytest --cov=src --cov-report=html
```

## 📚 Related Documentation

- [DRY Principles](../../../docs/guides/dry-kiss-yagni-principles.md) - Why HTTP-only data access enforces DRY
- [Improved Hybrid Approach](../../../docs/atomic/architecture/improved-hybrid-overview.md) - Architecture overview
- [Shared Utilities](../../shared/utils/README.md) - Reusable components used by this service

---

**Version:** 1.0.0
**Completeness:** 100% (27 files)
**Production Ready:** ✅ Yes
