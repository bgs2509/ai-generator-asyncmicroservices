# Error Handling

Return consistent, debuggable error responses using RFC 7807 Problem Details.

## Problem Details Structure

```json
{
  "type": "https://docs.example.com/errors/resource-not-found",
  "title": "Resource not found",
  "status": 404,
  "detail": "User 42 not found",
  "instance": "urn:request:123e4567-e89b-12d3-a456-426614174000",
  "code": "USER_NOT_FOUND",
  "context": {
    "resource": "user",
    "id": "42"
  }
}
```

## Implementation Pattern

```python
from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from src.core.errors import DomainError, NotFoundError


async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    problem = {
        "type": exc.problem_type,
        "title": exc.title,
        "status": exc.status_code,
        "detail": exc.message,
        "instance": str(request.state.request_id),
        "code": exc.code,
        "context": exc.context,
    }
    return JSONResponse(problem, status_code=exc.status_code)
```

Register handlers inside `create_app()`.

```python
app.add_exception_handler(DomainError, domain_error_handler)
app.add_exception_handler(NotFoundError, not_found_handler)
```

## Guidelines

- Convert Pydantic validation errors (`RequestValidationError`) into Problem Details with field paths (`data.attributes.name`).
- Avoid `raise HTTPException(...)` in routers; instead raise domain/application exceptions.
- Include request IDs and correlation IDs in responses for traceability.
- Hide sensitive details; log full error context but redact secrets before returning to clients.

## Anti-Patterns

### ❌ Silent Exception Swallowing

**Problem**: Using bare `except:` or `except Exception:` with `pass` silently swallows all errors, making debugging impossible

**Symptom**: Application appears to work but silently drops errors, no logs, no alerts, failed operations return success

**Impact**: Silent data loss, impossible debugging, no observability, corrupted state, user confusion

**Example (WRONG)**:
```python
# ❌ ANTI-PATTERN: Bare except with pass
from fastapi import APIRouter

router = APIRouter()

@router.post("/payments")
async def process_payment(payment_data: PaymentDTO) -> dict:
    """Process payment."""
    try:
        result = await payment_service.process(payment_data)
        await notification_service.send_confirmation(result.id)
        return {"status": "success", "payment_id": result.id}
    except:  # ❌ Catches EVERYTHING including KeyboardInterrupt, SystemExit!
        pass  # ❌ Silent failure - no logging, no retry, no user feedback!

    # ⚠️ Execution continues, returns None → crashes later or returns 200 OK with null!
    return {"status": "success"}  # ❌ LIE: Payment actually failed!
```

**Why This Matters**:
- Bare `except:` catches ALL exceptions including system signals (`KeyboardInterrupt`, `SystemExit`)
- `pass` discards exception → no logging → impossible to debug production failures
- Failed payments appear successful → financial discrepancies
- No observability: Monitoring shows 100% success rate while operations fail silently
- Corrupted state: Partial operations complete without rollback
- Violates fail-fast principle: Errors should bubble up, not disappear

**Solution (CORRECT)**:
```python
# ✅ CORRECT: Specific exception handling with logging and proper error responses
from fastapi import APIRouter, HTTPException, Request
from src.core.errors import DomainError, PaymentProviderError
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.post("/payments")
async def process_payment(
    payment_data: PaymentDTO,
    request: Request
) -> dict:
    """
    Process payment with proper error handling.

    Args:
        payment_data: Payment information
        request: FastAPI request (for request_id)

    Returns:
        Payment result with status

    Raises:
        DomainError: If payment validation fails
        HTTPException: If payment provider is unavailable
    """
    try:
        result = await payment_service.process(payment_data)
        await notification_service.send_confirmation(result.id)

        logger.info(
            "payment_processed",
            payment_id=result.id,
            amount=payment_data.amount,
            request_id=str(request.state.request_id)
        )

        return {"status": "success", "payment_id": result.id}

    except PaymentProviderError as e:
        # ✅ Specific exception: Payment provider is down
        logger.error(
            "payment_provider_error",
            error=str(e),
            payment_data=payment_data.dict(exclude={"card_number"}),
            request_id=str(request.state.request_id)
        )
        raise DomainError(
            code="PAYMENT_PROVIDER_UNAVAILABLE",
            message="Payment provider temporarily unavailable",
            context={"retry_after": 60}
        ) from e

    except ValidationError as e:
        # ✅ Specific exception: Invalid payment data
        logger.warning(
            "payment_validation_failed",
            error=str(e),
            request_id=str(request.state.request_id)
        )
        raise DomainError(
            code="PAYMENT_VALIDATION_FAILED",
            message="Invalid payment data",
            context={"errors": e.errors()}
        ) from e

    except Exception as e:
        # ✅ Last resort: Log unexpected errors and raise
        logger.exception(
            "payment_unexpected_error",
            error_type=type(e).__name__,
            error=str(e),
            request_id=str(request.state.request_id)
        )
        # ✅ Re-raise to trigger 500 error handler
        raise
```

**Architecture Rule**:
> Never use bare `except:` or `except Exception: pass`. Always catch specific exceptions, log errors with context, and re-raise or convert to domain errors. Silent failures are unacceptable in production systems.

**Best Practices**:
- Catch specific exceptions (`PaymentProviderError`, `ValidationError`) not `Exception`
- Always log errors with request IDs and relevant context
- Re-raise exceptions or convert to domain-specific errors with clear error codes
- Use `logger.exception()` to capture full stack trace
- Include `from e` to preserve exception chain for debugging
- Fail fast: Let unexpected errors bubble up to global error handler

**Related Anti-Patterns**:
- No Graceful Shutdown → `docs/atomic/integrations/cross-service/graceful-shutdown.md#no-graceful-shutdown`

## Testing

- Unit-test exception handlers to ensure correct payload shape.
- Integration tests should assert status codes and `code` values for each error scenario.

## Related Documents

- `docs/atomic/observability/logging/structured-logging.md`
- `docs/atomic/services/fastapi/security-patterns.md`
- `docs/atomic/observability/error-tracking/sentry-integration.md`
