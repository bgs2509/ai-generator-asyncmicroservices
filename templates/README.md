# Templates Directory

**Universal microservices templates for AI-assisted generation**

## 📁 Structure

```
templates/
├── infrastructure/          ✅ COMPLETE - 100% Universal
│   ├── docker-compose.yml           # Full-stack orchestration
│   ├── docker-compose.dev.yml       # Development overrides
│   ├── docker-compose.prod.yml      # Production overrides
│   ├── .env.example                 # Comprehensive env vars
│   └── Makefile                     # Development automation
│
├── nginx/                   ✅ COMPLETE - 100% Universal
│   ├── nginx.conf                   # Main config
│   ├── conf.d/
│   │   ├── upstream.conf            # Service definitions
│   │   ├── api-gateway.conf         # Main routing
│   │   └── ssl.conf                 # HTTPS/TLS config
│   └── Dockerfile                   # Nginx container
│
├── ci-cd/                   ✅ COMPLETE - 100% Universal
│   └── .github/workflows/
│       ├── ci.yml                   # Continuous Integration
│       └── cd.yml                   # Continuous Deployment
│
├── infrastructure/monitoring/  ✅ COMPLETE - 100% Universal
│   ├── prometheus/
│   │   └── prometheus.yml           # Metrics collection
│   └── grafana/provisioning/
│       └── datasources/
│           └── prometheus.yml       # Grafana datasource
│
├── services/                ✅ COMPLETE - 100% Universal (business templates)
│   ├── template_business_api/         ✅ 100% COMPLETE
│   │   ├── Dockerfile               # Multi-stage build
│   │   ├── requirements.txt         # Base dependencies
│   │   ├── src/
│   │   │   ├── main.py              # Application factory (uses shared/)
│   │   │   ├── core/config.py       # Pydantic Settings
│   │   │   ├── api/v1/health.py     # Health endpoints
│   │   │   └── schemas/base.py      # Base response schemas
│   │   └── tests/conftest.py        # Imports shared.testing
│   │
│   ├── template_business_bot/         ✅ 100% COMPLETE
│   │   ├── Dockerfile               # Multi-stage build
│   │   ├── requirements.txt         # Aiogram + dependencies
│   │   ├── src/
│   │   │   ├── main.py              # Bot entry point (uses shared/)
│   │   │   ├── core/config.py       # Bot settings
│   │   │   └── bot/                 # Handlers, keyboards, states
│   │   └── tests/conftest.py        # Imports shared.testing
│   │
│   ├── template_business_worker/      ✅ 100% COMPLETE
│   │   ├── Dockerfile               # Multi-stage build
│   │   ├── requirements.txt         # AsyncIO + dependencies
│   │   ├── src/
│   │   │   ├── main.py              # Worker entry point (uses shared/)
│   │   │   ├── core/config.py       # Worker settings
│   │   │   └── worker/              # Task processor, handlers
│   │   └── tests/conftest.py        # Imports shared.testing
│   │
│   ├── template_data_postgres_api/    ✅ 100% COMPLETE (existing)
│   └── template_data_mongo_api/       ⏳ TODO
│
└── shared/                  ✅ COMPLETE - 100% Universal utilities
    ├── utils/               ✅ 100%
    │   ├── __init__.py              # Exports all utilities
    │   ├── logger.py                # Structured JSON logging
    │   ├── request_id.py            # Correlation ID management
    │   ├── validators.py            # Email, phone, UUID, password validators
    │   ├── exceptions.py            # Base exception hierarchy with HTTP codes
    │   ├── pagination.py            # Offset and cursor pagination
    │   └── README.md                # Comprehensive usage guide
    ├── http_clients/        ✅ 100% - DRY-compliant
    │   ├── __init__.py              # Exports DataApiClient
    │   └── data_api_client.py       # HTTP client for Data Service
    ├── rabbitmq/            ✅ 100% - DRY-compliant
    │   ├── __init__.py              # Exports Publisher/Consumer
    │   ├── publisher.py             # Event publisher
    │   └── consumer.py              # Message consumer
    ├── middleware/          ✅ 100% - DRY-compliant
    │   ├── __init__.py              # Exports RequestIdMiddleware
    │   └── fastapi_request_id.py    # Request correlation middleware
    ├── events/              ✅ 100% - DRY-compliant
    │   ├── __init__.py              # Exports BaseEvent
    │   └── base_event.py            # Base event classes for RabbitMQ
    └── testing/             ✅ 100% - DRY-compliant
        ├── __init__.py              # Exports fixtures
        └── base_fixtures.py         # Shared pytest fixtures
```

## ✅ Completed (100% Universal)

### 1. Infrastructure Templates
- **docker-compose.yml**: Full production stack (all 5 services + infrastructure)
- **docker-compose.dev.yml**: Development overrides (hot reload, exposed ports, debug tools)
- **docker-compose.prod.yml**: Production optimizations (replicas, resource limits)
- **.env.example**: 150+ environment variables with descriptions
- **Makefile**: 30+ commands (dev, test, lint, db-migrate, monitoring, etc.)

### 2. Nginx API Gateway
- **nginx.conf**: Production-ready main configuration
- **upstream.conf**: Service definitions with health checks
- **api-gateway.conf**: Complete routing (API, auth, bot webhook, admin)
- **ssl.conf**: HTTPS/TLS configuration template
- **Dockerfile**: Nginx container with health checks

### 3. CI/CD Pipelines
- **ci.yml**: Complete CI pipeline (lint, test, build, security scan)
- **cd.yml**: CD pipeline (build/push images, deploy staging/production, rollback)

### 4. Observability
- **prometheus.yml**: Metrics collection for all services
- **grafana/datasources**: Prometheus datasource auto-provisioning

### 5. Shared Utilities
- **logger.py**: Structured JSON logging factory with request ID support
- **validators.py**: 10+ reusable validators (email, phone, UUID, password, slug, etc.)
- **exceptions.py**: Base exception hierarchy with HTTP status code mapping
- **pagination.py**: Offset and cursor pagination helpers with Pydantic models
- **request_id.py**: Correlation ID management using context variables
- **README.md**: Comprehensive usage guide with examples and migration guide

## 🚧 In Progress (95% Universal - Scaffolding Only)

### 5. API Service Scaffolding
**Completed:**
- ✅ Dockerfile (multi-stage: dev + production)
- ✅ requirements.txt (FastAPI, httpx, Redis, RabbitMQ, observability)
- ✅ src/main.py (application factory with lifespan)
- ✅ src/core/config.py (comprehensive Pydantic Settings)

**Remaining (critical for scaffolding):**
- ⏳ src/core/logging_config.py (structured JSON logging)
- ⏳ src/core/middleware.py (Request ID, logging, error handling)
- ⏳ src/api/v1/health_router.py (health check endpoint)
- ⏳ src/infrastructure/http_clients/postgres_client.py
- ⏳ src/infrastructure/http_clients/mongo_client.py
- ⏳ src/infrastructure/rabbitmq/publisher.py
- ⏳ src/schemas/health.py
- ⏳ tests/conftest.py (base fixtures)

### 6-9. Other Service Scaffolding
- ⏳ template_business_bot/ (Aiogram scaffolding)
- ⏳ template_business_worker/ (AsyncIO scaffolding)
- ⏳ template_data_postgres_api/ (SQLAlchemy scaffolding + Alembic)
- ⏳ template_data_mongo_api/ (Motor scaffolding)

### 10. Shared Utilities
- ⏳ shared/utils/ (logger, request_id, validators, exceptions)
- ⏳ shared/events/base_event.py

## 📋 Usage

### For AI Agents

When generating a new microservices project:

1. **Copy infrastructure/** → Ready to `docker-compose up`
2. **Copy nginx/** → Production-ready API Gateway
3. **Copy ci-cd/.github/workflows/** → CI/CD ready
4. **Copy services/{service}-scaffolding/** → Add business logic
5. **Copy shared/utils/** → Use utilities
6. Generate business-specific code:
   - Domain entities
   - Use cases
   - API endpoints
   - Database models
   - Bot handlers
   - Worker tasks

### For Developers

```bash
# Initialize new project
mkdir my_awesome_app && cd my_awesome_app

# Copy templates
cp -r /path/to/doc4microservices/templates/* .

# Configure environment
cp .env.example .env
# Edit .env with your values

# Start development
make dev

# Or use docker-compose directly
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## 🎯 Design Principles

### What Templates INCLUDE
✅ Infrastructure code (Docker, Nginx, CI/CD)
✅ Service scaffolding (folder structure, core utilities)
✅ Framework integration (FastAPI setup, SQLAlchemy config)
✅ Observability setup (Prometheus, logging)
✅ Development tools (Makefile, pytest setup)

### What Templates EXCLUDE
❌ Business entities (User, Product, Order)
❌ Business logic (use cases, domain rules)
❌ Business endpoints (/users, /orders)
❌ Business DTOs (UserCreate, ProductUpdate)
❌ Business events (user.created, order.completed)

### Substitution Variables

Templates use `{{variable}}` placeholders for AI substitution:
- `{{PROJECT_NAME}}` → User's project name
- `{{DOMAIN_NAME}}` → User's domain
- `{{entity}}` → Business entity name
- `{{feature}}` → Feature name

## 📊 Completion Status

| Component | Status | Universality | Priority |
|-----------|--------|--------------|----------|
| docker-compose | ✅ 100% | 100% | 🔴 P0 |
| nginx | ✅ 100% | 100% | 🔴 P0 |
| .env | ✅ 100% | 100% | 🔴 P0 |
| Makefile | ✅ 100% | 100% | 🔴 P0 |
| CI/CD | ✅ 100% | 100% | 🔴 P0 |
| Observability | ✅ 100% | 100% | 🔴 P0 |
| template_business_api | ✅ 100% | 100% | 🔴 P0 |
| template_business_bot | ✅ 100% | 100% | 🔴 P0 |
| template_business_worker | ✅ 100% | 100% | 🔴 P0 |
| template_data_postgres_api | ✅ 100% | 100% | 🔴 P0 |
| template_data_mongo_api | ⏳ 0% | 95% | 🟡 P1 |
| shared/utils | ✅ 100% | 100% | 🔴 P0 |
| shared/http_clients | ✅ 100% | 100% | 🔴 P0 |
| shared/rabbitmq | ✅ 100% | 100% | 🔴 P0 |
| shared/middleware | ✅ 100% | 100% | 🔴 P0 |
| shared/events | ✅ 100% | 100% | 🔴 P0 |
| shared/testing | ✅ 100% | 100% | 🔴 P0 |

**Overall Completion: ~94%**

## 🚀 Next Steps

### Phase 1: Complete MongoDB Data Service (Priority: 🟡 P1)
1. template_data_mongo_api scaffolding
2. Follow same DRY pattern as PostgreSQL service

### Phase 2: Documentation Polish (Priority: 🟢 P2)
1. Fix remaining relative path references in docs/atomic/
2. Verify all cross-references resolve correctly

## 📝 Notes

- All templates follow "Improved Hybrid Approach" architecture
- 100% type hints (mypy strict mode compatible)
- Production-ready (health checks, graceful shutdown, logging)
- Ready for 35 different business ideas analyzed
- AI copies templates, generates only business logic (80/20 rule)
