# Migration Guide: Phase 1 - DRY/KISS/YAGNI Enforcement

**Target Audience:** Existing projects using the AI Generator for Async Microservices framework
**Phase:** Phase 1 (DRY/KISS/YAGNI Principles Enforcement)
**Last Updated:** 2025-11-07

---

## Overview

This guide helps you migrate existing microservices projects to adopt Phase 1 improvements:

1. **Shared Utilities** - Eliminate code duplication
2. **PostgreSQL Data Service Template** - Standardize data access patterns
3. **Automated Quality Gates** - Enforce quality standards in CI

**Estimated Migration Time:** 4-8 hours for a typical 5-service project

---

## Prerequisites

Before starting migration:

- [ ] Existing project uses framework version 0.1.0 or later
- [ ] Git working directory is clean (commit or stash changes)
- [ ] All tests passing in current state
- [ ] CI/CD pipeline functional
- [ ] Backup or branch created (`git checkout -b migrate-phase1`)

---

## Phase 1: Migrate to Shared Utilities

**Goal:** Replace duplicated code with shared utilities

### Step 1.1: Copy Shared Utilities

```bash
# From framework root
cp -r templates/shared/utils/ your_project/shared/

# Verify files copied
ls -la your_project/shared/utils/
# Expected: __init__.py, logger.py, validators.py, exceptions.py,
#           pagination.py, request_id.py, README.md
```

### Step 1.2: Migrate Logging

**Before:** Duplicated logging setup in each service

```python
# services/user_api/src/core/logging_config.py (BEFORE)
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s"
    )
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(level)
```

**After:** Use shared logger

```python
# services/user_api/src/core/logging_config.py (AFTER)
from shared.utils.logger import create_logger

# Create service-specific logger
logger = create_logger("user_api", level="INFO", include_request_id=True)

# In your application code
from shared.utils.logger import create_logger

logger = create_logger(__name__)
logger.info("User created", extra={"user_id": user.id, "email": user.email})
```

**Files to migrate:**
- `services/*/src/core/logging_config.py` → Use `shared.utils.logger`
- `services/*/src/main.py` → Import from shared logger

### Step 1.3: Migrate Validators

**Before:** Duplicated validation in multiple services

```python
# services/user_api/src/utils/validators.py (BEFORE - DELETE THIS)
import re

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# services/profile_api/src/utils/validators.py (BEFORE - DELETE THIS)
# ^^^ SAME CODE DUPLICATED ^^^
```

**After:** Use shared validators

```python
# services/user_api/src/api/v1/users.py (AFTER)
from shared.utils.validators import is_valid_email, is_valid_phone
from shared.utils.exceptions import ValidationError

@router.post("/users")
async def create_user(data: UserCreate):
    if not is_valid_email(data.email):
        raise ValidationError("Invalid email format")

    if data.phone and not is_valid_phone(data.phone):
        raise ValidationError("Invalid phone format")

    # ... create user
```

**Files to migrate:**
- `services/*/src/utils/validators.py` → **DELETE** and use `shared.utils.validators`
- All imports → Change to `from shared.utils.validators import ...`

### Step 1.4: Migrate Exception Handling

**Before:** Inconsistent exception handling

```python
# services/user_api/src/exceptions.py (BEFORE)
class UserNotFound(Exception):
    pass

# services/payment_api/src/exceptions.py (BEFORE)
class PaymentNotFound(Exception):
    pass
```

**After:** Use shared exception hierarchy

```python
# services/user_api/src/exceptions.py (AFTER)
from shared.utils.exceptions import NotFoundError

class UserNotFound(NotFoundError):
    """User not found (404)."""

    def __init__(self, user_id: int):
        super().__init__(
            message=f"User {user_id} not found",
            error_code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )
```

**Benefits:**
- Automatic HTTP status code mapping (404, 422, 401, etc.)
- Consistent error response format
- Built-in error details support

### Step 1.5: Migrate Pagination

**Before:** Custom pagination in each service

```python
# services/user_api/src/api/v1/users.py (BEFORE)
@router.get("/users")
async def list_users(skip: int = 0, limit: int = 50):
    users = await user_service.get_users(skip=skip, limit=limit)
    total = await user_service.count_users()
    return {
        "items": users,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

**After:** Use shared pagination

```python
# services/user_api/src/api/v1/users.py (AFTER)
from shared.utils.pagination import (
    OffsetPaginationParams,
    OffsetPaginatedResponse,
    paginate_query
)

@router.get("/users", response_model=OffsetPaginatedResponse[UserOut])
async def list_users(
    pagination: OffsetPaginationParams = Depends()
):
    users, total = await user_service.get_users(
        skip=pagination.skip,
        limit=pagination.limit
    )
    return OffsetPaginatedResponse(
        items=users,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit
    )
```

**Benefits:**
- Type-safe pagination with Pydantic models
- Consistent pagination across all services
- Supports both offset and cursor pagination

### Step 1.6: Add Request ID Tracking

**New feature:** Correlation IDs for distributed tracing

```python
# services/user_api/src/core/middleware.py (NEW)
from fastapi import Request
from shared.utils.request_id import generate_request_id, set_request_id

async def request_id_middleware(request: Request, call_next):
    # Get request ID from header or generate new one
    request_id = request.headers.get("X-Request-ID", generate_request_id())
    set_request_id(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# In main.py
from src.core.middleware import request_id_middleware

app.middleware("http")(request_id_middleware)
```

**Usage in logging:**

```python
from shared.utils.logger import create_logger
from shared.utils.request_id import get_request_id

logger = create_logger(__name__, include_request_id=True)

# Request ID automatically included in logs
logger.info("Processing payment")
# Output: {"timestamp": "...", "request_id": "abc-123", "message": "Processing payment"}
```

### Step 1.7: Verify Migration

```bash
# 1. Check imports
grep -r "from shared.utils" services/*/src/ | wc -l
# Should show multiple imports

# 2. Remove old duplicate files
find services/ -name "validators.py" -path "*/utils/*" -delete
find services/ -name "logging_config.py" -path "*/core/*" -delete

# 3. Run tests
pytest services/*/tests/ -v

# 4. Run quality gates (see Phase 3)
jscpd services/ shared/ --threshold 10
```

---

## Phase 2: Adopt PostgreSQL Data Service Pattern

**Goal:** Standardize PostgreSQL data access using the template

### Step 2.1: Identify Data Services

```bash
# List services with direct database access
grep -r "create_engine\|AsyncEngine" services/*/src/ -l

# These services should be converted to data service pattern
```

### Step 2.2: Create New Data Service from Template

```bash
# Copy PostgreSQL data service template
cp -r templates/services/template_data_postgres_api/ services/data_postgres_api/

# Rename placeholders (if using sed)
cd services/data_postgres_api/
find . -type f -exec sed -i 's/{{PROJECT_NAME}}/your_project/g' {} +
find . -type f -exec sed -i 's/{{SERVICE_NAME}}/data_postgres_api/g' {} +
```

### Step 2.3: Migrate Database Models

**Before:** Models in business services

```python
# services/user_api/src/models/user.py (BEFORE - MOVE TO DATA SERVICE)
from sqlalchemy import Column, Integer, String
from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
```

**After:** Models in data service

```python
# services/data_postgres_api/src/models/user.py (AFTER)
from sqlalchemy import Column, Integer, String
from src.models.base import Base, TimestampMixin, SoftDeleteMixin

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)

    # TimestampMixin adds: created_at, updated_at
    # SoftDeleteMixin adds: deleted_at, soft_delete(), restore()
```

### Step 2.4: Create Repository

```python
# services/data_postgres_api/src/repositories/user_repository.py (NEW)
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.base_repository import BaseRepository
from src.models.user import User

class UserRepository(BaseRepository[User]):
    """User repository with CRUD operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email (custom query)."""
        from sqlalchemy import select

        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
```

**Benefits:**
- All CRUD operations inherited from BaseRepository
- Only implement custom queries (get_by_email)
- Type-safe with Generic[User]

### Step 2.5: Create API Endpoints

```python
# services/data_postgres_api/src/api/v1/users.py (NEW)
from fastapi import APIRouter, Depends, HTTPException
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserOut, UserCreate
from src.core.database import get_session

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    session = Depends(get_session)
):
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserOut, status_code=201)
async def create_user(
    data: UserCreate,
    session = Depends(get_session)
):
    repo = UserRepository(session)
    user = await repo.create(**data.model_dump())
    return user
```

### Step 2.6: Update Business Services to Use HTTP

**Before:** Business service with direct DB access

```python
# services/user_api/src/services/user_service.py (BEFORE - REMOVE DB ACCESS)
class UserService:
    def __init__(self, db: Session):
        self._db = db

    async def get_user(self, user_id: int) -> User:
        return self._db.query(UserModel).filter(UserModel.id == user_id).first()
```

**After:** Business service with HTTP access

```python
# services/user_api/src/services/user_service.py (AFTER - HTTP ONLY)
import httpx
from src.core.config import settings

class UserService:
    def __init__(self):
        self._data_api_url = settings.DATA_API_URL

    async def get_user(self, user_id: int) -> User:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._data_api_url}/users/{user_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return User(**response.json())
```

**Benefits:**
- Single source of truth for data access
- No duplicated database queries
- Data service handles connection pooling, transactions
- Business services focus on business logic only

### Step 2.7: Run Migrations

```bash
# In data service directory
cd services/data_postgres_api/

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Review migration file
cat alembic/versions/*_initial_schema.py

# Apply migration
alembic upgrade head

# Verify
alembic current
```

---

## Phase 3: Add Automated Quality Gates

**Goal:** Enforce quality standards in CI pipeline

### Step 3.1: Install Quality Tools

```bash
# Install jscpd (code duplication detector)
npm install -g jscpd

# Install radon (complexity analyzer)
pip install radon

# Verify installation
jscpd --version
radon --version
```

### Step 3.2: Copy CI Workflow

```bash
# Copy quality gates workflow
cp templates/ci-cd/.github/workflows/ci.yml .github/workflows/

# Review the new quality gate jobs
grep -A5 "check-duplication\|check-complexity\|check-dependencies" .github/workflows/ci.yml
```

### Step 3.3: Run Quality Gates Locally

**Test before pushing:**

```bash
# 1. DRY check (code duplication)
jscpd services/ shared/ --threshold 10 --format "python" --reporters "console"

# 2. KISS checks
# 2a. Cyclomatic complexity
radon cc services/ shared/ --min B --total-average --show-complexity

# 2b. Maintainability index
radon mi services/ shared/ --min B --show

# 2c. File sizes
find services/ shared/ -name "*.py" -type f -exec wc -l {} \; | awk '$1 > 500'

# 3. YAGNI check (dependencies)
for dir in services/*/; do
  echo "$(basename $dir): $(grep -cve '^#' -e '^$' $dir/requirements.txt 2>/dev/null || echo 0) deps"
done
```

### Step 3.4: Fix Violations

If quality gates fail, see remediation guide:
- [Automated Quality Gates Documentation](../quality/automated-quality-gates.md)

**Common fixes:**

1. **Code duplication >10%**
   - Extract to `shared/utils/`
   - Create base classes
   - Use composition

2. **Complexity >10**
   - Extract methods
   - Use early returns
   - Apply strategy pattern

3. **Too many dependencies**
   - Remove dev deps from production requirements.txt
   - Use stdlib alternatives
   - Remove unused dependencies

### Step 3.5: Commit and Push

```bash
# Stage all changes
git add .github/workflows/ci.yml shared/utils/ services/

# Commit
git commit -m "feat: Migrate to Phase 1 (DRY/KISS/YAGNI enforcement)

- Add shared utilities (logger, validators, exceptions, pagination)
- Migrate to PostgreSQL data service pattern
- Add automated quality gates in CI

Quality Metrics:
- Code duplication: <10%
- Cyclomatic complexity: <10
- All files <500 lines
- Dependencies within limits

🤖 Migrated using Phase 1 migration guide"

# Push and watch CI
git push origin migrate-phase1
```

---

## Verification Checklist

After migration, verify:

### Shared Utilities
- [ ] All services import from `shared.utils.*`
- [ ] Old duplicate files deleted
- [ ] Request IDs propagate across services
- [ ] Logging produces structured JSON
- [ ] Validators used consistently

### Data Service Pattern
- [ ] Data service has all database models
- [ ] Business services use HTTP only (no direct DB)
- [ ] Alembic migrations working
- [ ] Health checks responding (`/health`, `/health/ready`)
- [ ] BaseRepository used for CRUD operations

### Quality Gates
- [ ] CI workflow includes quality gate jobs
- [ ] Code duplication <10%
- [ ] Complexity <10 (McCabe)
- [ ] File sizes <500 lines
- [ ] Dependencies within limits (30/50)
- [ ] All tests passing

---

## Rollback Plan

If migration causes issues:

```bash
# 1. Rollback git changes
git reset --hard origin/main  # or origin/master

# 2. Remove shared utilities
rm -rf shared/utils/

# 3. Restore old CI workflow
git checkout origin/main -- .github/workflows/ci.yml

# 4. Restart services
docker-compose restart
```

---

## Troubleshooting

### Issue: Import errors after migration

**Symptom:**
```
ImportError: No module named 'shared.utils'
```

**Solution:**
```bash
# Ensure shared/ is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or in Dockerfile
ENV PYTHONPATH=/app
```

### Issue: Quality gates failing in CI

**Symptom:**
```
❌ DRY VIOLATION: Code duplication exceeds 10% threshold
```

**Solution:**
- See [automated-quality-gates.md](../quality/automated-quality-gates.md) for detailed remediation
- Run checks locally first: `jscpd services/ shared/ --threshold 10`
- Fix violations before pushing

### Issue: Business services can't connect to data service

**Symptom:**
```
httpx.ConnectError: Connection refused
```

**Solution:**
```bash
# 1. Verify data service is running
docker-compose ps data_postgres_api

# 2. Check DATA_API_URL in business service .env
echo $DATA_API_URL  # Should be http://data_postgres_api:8000

# 3. Test connectivity
curl http://data_postgres_api:8000/health
```

### Issue: Alembic migrations fail

**Symptom:**
```
alembic.util.exc.CommandError: Can't locate revision identified by 'xyz'
```

**Solution:**
```bash
# 1. Check migration history
alembic history

# 2. Stamp current database version
alembic stamp head

# 3. Generate new migration
alembic revision --autogenerate -m "Fix migration"
```

---

## Support

- **Documentation:** [docs/INDEX.md](../INDEX.md)
- **Quality Gates:** [docs/quality/automated-quality-gates.md](../quality/automated-quality-gates.md)
- **Shared Utils:** [templates/shared/utils/README.md](../../templates/shared/utils/README.md)
- **Data Service:** [templates/services/template_data_postgres_api/README.md](../../templates/services/template_data_postgres_api/README.md)
- **Issues:** https://github.com/anthropics/claude-code/issues

---

## Next Steps

After completing Phase 1 migration:

1. **Monitor Quality Metrics**
   - Track duplication trends
   - Monitor complexity growth
   - Review dependency changes

2. **Consider Phase 2** (when available)
   - Complete business API template
   - Add anti-patterns documentation
   - Maturity level upgrade triggers

3. **Share Feedback**
   - Report migration issues
   - Suggest improvements
   - Share success stories

---

**Migration Guide Version:** 1.0
**Last Updated:** 2025-11-07
**Status:** Active
