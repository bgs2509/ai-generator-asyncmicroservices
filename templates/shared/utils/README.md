# Shared Utilities

Reusable utility functions and classes used across all framework services.

## Purpose

These utilities eliminate code duplication by providing:

- ✅ **Structured JSON logging** (no duplication of logging setup)
- ✅ **Common validators** (no duplication of email/phone/UUID validation)
- ✅ **Base exception hierarchy** (consistent error handling)
- ✅ **Pagination helpers** (no duplication of pagination logic)
- ✅ **Request ID management** (distributed tracing support)

## Design Principles

### 100% Universal

- ❌ No business logic
- ❌ No project-specific code
- ❌ No database or external service dependencies
- ✅ Pure, reusable utilities

### Type-Safe

- ✅ 100% type hint coverage
- ✅ Passes mypy strict mode
- ✅ Full IDE autocomplete support

### Well-Tested

- ✅ 100% test coverage requirement
- ✅ Comprehensive docstrings with examples
- ✅ Integration examples for each module

---

## Module Documentation

### 1. Logger (`logger.py`)

**Problem:** Every service duplicates logging configuration

**Solution:** Use `create_logger` factory

#### Before (WRONG - Duplicated Code)

```python
# services/auth_api/src/core/logging_config.py
import logging
import sys
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel("INFO")

# services/user_api/src/core/logging_config.py
# ^^^ EXACT SAME CODE DUPLICATED ^^^ (100+ lines)

# services/payment_api/src/core/logging_config.py
# ^^^ EXACT SAME CODE DUPLICATED ^^^ (100+ lines)
```

**Impact:** ~300 lines of duplicated code for 3 services

#### After (CORRECT - DRY)

```python
# All services use the same import
from shared.utils.logger import create_logger

logger = create_logger(__name__)
logger.info("User authenticated", extra={"user_id": 123})
# Output: {"asctime": "2025-01-07T10:30:00", "name": "auth_service",
#          "levelname": "INFO", "message": "User authenticated",
#          "user_id": 123, "request_id": "req_abc-123"}
```

**Impact:** 2 lines per service, consistent logging across all services

#### FastAPI Integration

```python
# src/main.py
from fastapi import FastAPI
from shared.utils.logger import create_logger, configure_uvicorn_logging

logger = create_logger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup():
    configure_uvicorn_logging()
    logger.info("Service started")
```

#### Request ID Integration

```python
from shared.utils.logger import create_logger, RequestIdFilter
from shared.utils.request_id import get_request_id

logger = create_logger(__name__)
logger.addFilter(RequestIdFilter(get_request_id))

# Now all logs automatically include request_id
logger.info("Processing payment")  # request_id included automatically
```

---

### 2. Validators (`validators.py`)

**Problem:** Validation logic duplicated across services

**Solution:** Reusable validation functions

#### Available Validators

```python
from shared.utils.validators import (
    is_valid_email,
    is_valid_phone,
    is_valid_uuid,
    is_valid_url,
    validate_password_strength,
    is_valid_slug,
    is_valid_hex_color,
    is_valid_username,
    is_valid_port,
)
```

#### Usage Examples

```python
# Email validation
if not is_valid_email("user@example.com"):
    raise ValidationError("Invalid email")

# Phone validation (US format)
if not is_valid_phone("+1-555-123-4567", "US"):
    raise ValidationError("Invalid phone number")

# Password strength
is_valid, error_msg = validate_password_strength("Weak123!")
if not is_valid:
    raise ValidationError(error_msg)

# UUID validation
if not is_valid_uuid("123e4567-e89b-12d3-a456-426614174000"):
    raise ValidationError("Invalid UUID")
```

#### FastAPI Integration

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from shared.utils.validators import is_valid_email

router = APIRouter()

class UserCreate(BaseModel):
    email: str

    @validator("email")
    def validate_email(cls, v):
        if not is_valid_email(v):
            raise ValueError("Invalid email format")
        return v

@router.post("/users")
async def create_user(data: UserCreate):
    # email already validated by Pydantic
    return {"email": data.email}
```

---

### 3. Exceptions (`exceptions.py`)

**Problem:** Inconsistent error handling across services

**Solution:** Base exception hierarchy with HTTP status codes

#### Available Exceptions

```python
from shared.utils.exceptions import (
    BaseServiceException,      # Base class
    NotFoundError,             # 404
    ValidationError,           # 422
    UnauthorizedError,         # 401
    ForbiddenError,            # 403
    ConflictError,             # 409
    ExternalServiceError,      # 502/503
    RateLimitError,            # 429
    BadRequestError,           # 400
    ServiceUnavailableError,   # 503
)
```

#### Usage Examples

```python
# Not found
user = await user_repository.get_by_id(user_id)
if not user:
    raise NotFoundError(
        message=f"User {user_id} not found",
        error_code="USER_NOT_FOUND",
        details={"user_id": user_id}
    )

# Validation error
if len(password) < 8:
    raise ValidationError(
        message="Password must be at least 8 characters",
        error_code="PASSWORD_TOO_SHORT",
        details={"min_length": 8, "actual_length": len(password)}
    )

# External service error
try:
    response = await payment_gateway.charge(amount)
except Exception as e:
    raise ExternalServiceError(
        message="Payment gateway unavailable",
        error_code="PAYMENT_GATEWAY_ERROR",
        status_code=503,
        details={"gateway": "stripe", "error": str(e)}
    )
```

#### FastAPI Integration

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from shared.utils.exceptions import BaseServiceException
from shared.utils.request_id import get_request_id

app = FastAPI()

@app.exception_handler(BaseServiceException)
async def service_exception_handler(request: Request, exc: BaseServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
                "request_id": get_request_id(),
            }
        },
        headers={"X-Request-ID": get_request_id() or "unknown"},
    )
```

---

### 4. Pagination (`pagination.py`)

**Problem:** Pagination logic duplicated across services

**Solution:** Reusable pagination patterns (offset and cursor)

#### Offset Pagination (Simple, for small datasets)

```python
from fastapi import APIRouter, Depends
from shared.utils.pagination import (
    OffsetPaginationParams,
    OffsetPaginatedResponse,
)

router = APIRouter()

@router.get("/users", response_model=OffsetPaginatedResponse[UserSchema])
async def list_users(
    pagination: OffsetPaginationParams = Depends(),
    repository: UserRepository = Depends(get_repository),
):
    users = await repository.get_all(
        skip=pagination.skip,
        limit=pagination.limit,
    )
    total = await repository.count()

    return OffsetPaginatedResponse(
        items=users,
        total=total,
        limit=pagination.limit,
        offset=pagination.offset,
    )

# Usage:
# GET /users?limit=20&offset=40
# Response:
# {
#   "items": [...],
#   "total": 1000,
#   "limit": 20,
#   "offset": 40,
#   "has_next": true,
#   "has_previous": true,
#   "current_page": 3,
#   "total_pages": 50
# }
```

#### Cursor Pagination (Efficient, for large datasets)

```python
from shared.utils.pagination import (
    CursorPaginationParams,
    CursorPaginatedResponse,
    create_cursor,
    parse_cursor,
)

@router.get("/posts", response_model=CursorPaginatedResponse[PostSchema])
async def list_posts(
    pagination: CursorPaginationParams = Depends(),
    repository: PostRepository = Depends(get_repository),
):
    # Parse cursor to get last ID
    last_id = 0
    if pagination.cursor:
        cursor_data = parse_cursor(pagination.cursor)
        last_id = cursor_data["id"]

    # Fetch items after cursor
    posts = await repository.get_after_id(
        after_id=last_id,
        limit=pagination.limit + 1,  # Fetch one extra to check has_next
    )

    has_next = len(posts) > pagination.limit
    if has_next:
        posts = posts[:pagination.limit]

    next_cursor = None
    if has_next and posts:
        next_cursor = create_cursor(posts[-1].id)

    return CursorPaginatedResponse(
        items=posts,
        next_cursor=next_cursor,
    )

# Usage:
# GET /posts?limit=20
# GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ
# Response:
# {
#   "items": [...],
#   "next_cursor": "eyJpZCI6MTQzfQ==",
#   "has_next": true
# }
```

---

### 5. Request ID (`request_id.py`)

**Problem:** No correlation IDs for distributed tracing

**Solution:** Context-based request ID management

#### FastAPI Middleware

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from shared.utils.request_id import generate_request_id, set_request_id, get_request_id

app = FastAPI()

class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-ID") or generate_request_id()
        set_request_id(request_id)

        # Process request
        response = await call_next(request)

        # Add request ID to response
        response.headers["X-Request-ID"] = request_id

        return response

app.add_middleware(RequestIdMiddleware)
```

#### Usage in Services

```python
from shared.utils.request_id import get_request_id
from shared.utils.logger import create_logger

logger = create_logger(__name__)

async def process_order(order_id: int):
    # Request ID is automatically available in context
    logger.info(
        f"Processing order {order_id}",
        extra={"order_id": order_id, "request_id": get_request_id()}
    )

    # When calling another service, propagate request ID
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://data-api/orders/{order_id}",
            headers={"X-Request-ID": get_request_id()}
        )
```

#### Aiogram Bot Integration

```python
from aiogram import BaseMiddleware
from aiogram.types import Message
from shared.utils.request_id import generate_request_id, set_request_id

class RequestIdMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        request_id = generate_request_id()
        set_request_id(request_id)

        # All handlers in this request will have access to request_id
        return await handler(event, data)
```

---

## Testing Examples

### Testing with Validators

```python
# tests/unit/test_validators.py
import pytest
from shared.utils.validators import is_valid_email

def test_valid_email():
    assert is_valid_email("user@example.com") is True
    assert is_valid_email("test+tag@domain.co.uk") is True

def test_invalid_email():
    assert is_valid_email("invalid") is False
    assert is_valid_email("@example.com") is False
    assert is_valid_email("user@") is False
```

### Testing with Exceptions

```python
# tests/unit/test_service.py
import pytest
from shared.utils.exceptions import NotFoundError

async def test_get_user_not_found():
    with pytest.raises(NotFoundError) as exc_info:
        await user_service.get_user(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.error_code == "USER_NOT_FOUND"
    assert exc_info.value.details["user_id"] == 999
```

### Testing with Request ID

```python
# tests/unit/test_request_id.py
from shared.utils.request_id import set_request_id, get_request_id, reset_request_id

def test_request_id_context():
    # Setup
    reset_request_id()

    # Test
    set_request_id("test-123")
    assert get_request_id() == "test-123"

    # Cleanup
    reset_request_id()
    assert get_request_id() is None
```

---

## Migration Guide

### Migrating Existing Services

If you have existing services with duplicated code, follow this migration path:

#### Step 1: Replace Logger

```bash
# Find all logging setup
grep -r "jsonlogger" services/*/src/

# Replace with:
from shared.utils.logger import create_logger
logger = create_logger(__name__)
```

#### Step 2: Replace Validators

```bash
# Find email validation patterns
grep -r "re.match.*@" services/*/src/

# Replace with:
from shared.utils.validators import is_valid_email
if not is_valid_email(email):
    raise ValidationError("Invalid email")
```

#### Step 3: Replace Exception Classes

```bash
# Find custom exception definitions
grep -r "class.*Exception" services/*/src/

# Replace with imports:
from shared.utils.exceptions import NotFoundError, ValidationError
```

#### Step 4: Add Pagination

```bash
# Find manual pagination code
grep -r "offset.*limit" services/*/src/

# Replace with:
from shared.utils.pagination import OffsetPaginationParams
```

---

## Best Practices

### DO ✅

- **Import from shared.utils** for all common utilities
- **Add new validators** when you find duplication
- **Use type hints** for all function parameters
- **Write docstrings** with usage examples
- **Test thoroughly** (100% coverage requirement)

### DON'T ❌

- **Don't add business logic** to shared utilities
- **Don't add project-specific code** (must be universal)
- **Don't add external dependencies** without discussion
- **Don't break backward compatibility** without major version bump
- **Don't skip testing** (all utilities must have tests)

---

## Adding New Utilities

If you need to add a new shared utility:

1. **Check for duplication**: Is this logic duplicated in 2+ services?
2. **Ensure universality**: Will this work for ANY microservice?
3. **Write the utility**: Add to appropriate module or create new one
4. **Add type hints**: 100% type coverage required
5. **Write tests**: 100% test coverage required
6. **Document usage**: Add examples to this README
7. **Submit PR**: Include migration guide for existing services

---

## Related Documentation

- [DRY Principle Guide](../../../docs/guides/dry-kiss-yagni-principles.md#dry) — Why we eliminate duplication
- [Code Review Checklist](../../../docs/atomic/testing/quality-assurance/code-review-checklist.md) — Includes DRY checks
- [HTTP-Only Data Access](../../../docs/atomic/architecture/improved-hybrid-overview.md) — Architecture enforcing DRY

---

**Version:** 1.0.0
**Status:** ✅ Complete
**Coverage:** 100% type hints, 100% tests required
**Maintained By:** Framework Maintainers
