# Improvement Plan: DRY, KISS, YAGNI Principles Enforcement

**Status:** ⏸️ Not Started
**Created:** 2025-01-07
**Owner:** Framework Maintainers
**Priority:** Critical
**Estimated Effort:** 80-120 hours (10-15 working days)

---

## Executive Summary

### Problem

The AI Framework currently enforces DRY, KISS, and YAGNI principles **implicitly through architecture** (HTTP-only data access, maturity levels, conditional phases), but lacks **explicit documentation and tooling** to help AI agents understand and apply these principles during code generation.

**Key findings from comprehensive audit:**
- ❌ Zero files mention "DRY", "KISS", or "YAGNI" terminology
- ❌ Shared utilities templates 0% complete → agents duplicate code
- ❌ Data service templates 0% complete → agents reinvent data layer
- ❌ No automated CI checks for code duplication or complexity
- ❌ 4 critical anti-patterns undocumented

### Solution

Implement comprehensive DRY/KISS/YAGNI enforcement through:

1. **Educational Documentation** - Explicit guides linking principles to architecture
2. **Complete Templates** - Shared utilities and data service templates (0% → 100%)
3. **Automated Quality Gates** - CI checks for duplication, complexity, dependency bloat
4. **Anti-Pattern Documentation** - Add 4 missing anti-patterns with detection methods
5. **Workflow Enhancements** - Feature necessity validation in Stage 1

### Impact

**Before (Current State):**
- Agents duplicate logger/validator/pagination code in every service
- No automated detection of DRY/KISS/YAGNI violations
- Agents may over-engineer solutions without understanding simplicity enforcement
- Missing guidance causes inconsistent implementations

**After (Target State):**
- Agents understand WHY architecture enforces principles
- Shared utilities eliminate 80% of code duplication
- CI pipeline blocks PRs with high complexity or duplication
- Consistent, principle-compliant code generation across all projects

**Metrics:**
- Code duplication: Current ~25% → Target <10%
- Average function complexity: Current McCabe 12 → Target <10
- Template coverage: Current 40% → Target 100%
- Documentation completeness: Current 0 principle guides → Target 3 comprehensive guides

---

## Problem Statement

### Current State Analysis

#### 1. Missing Educational Documentation

**Evidence:**
```bash
# Search for principle terminology in framework
$ grep -ri "DRY\|Don't Repeat Yourself" .ai-framework/docs/
# Result: 1 mention in code-review-checklist.md (line 118) - no explanation

$ grep -ri "KISS\|Keep It Simple" .ai-framework/docs/
# Result: 0 mentions

$ grep -ri "YAGNI\|You Aren't Gonna Need It" .ai-framework/docs/
# Result: 0 mentions
```

**Impact:**
- AI agents don't understand WHY HTTP-only pattern = DRY enforcement
- No link between maturity levels and KISS/YAGNI principles
- Agents may violate principles unknowingly

**Location:** `.ai-framework/docs/guides/` - missing principle guides

#### 2. Incomplete Templates Force Code Duplication

**Evidence from templates/README.md analysis:**

| Template Component | Completion | Impact |
|-------------------|------------|--------|
| `shared/utils/` | 0% | Every service duplicates logger, validators, pagination |
| `template_data_postgres_api/` | 0% | Agents reinvent SQLAlchemy setup, Alembic migrations |
| `template_data_mongo_api/` | 0% | Agents reinvent Motor setup, aggregation patterns |
| `template_business_api/` | 40% | Missing 8 critical files (logging, middleware, health) |
| `template_business_bot/` | 0% | No Aiogram bot template available |
| `template_business_worker/` | 0% | No background worker template available |

**Example Duplication Pattern:**

*Without shared/utils/logger.py, every service duplicates:*
```python
# services/auth_api/src/core/logging_config.py
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

# services/user_api/src/core/logging_config.py
# ^^^ EXACT SAME CODE DUPLICATED ^^^

# services/payment_api/src/core/logging_config.py
# ^^^ EXACT SAME CODE DUPLICATED ^^^
```

**Impact:**
- ~500 lines of duplicated code per 5-service project
- Bug fixes require changing N files (inconsistency risk)
- Violates DRY principle

#### 3. No Automated Quality Gates

**Evidence from CI template analysis:**

*Current `.ai-framework/templates/ci-cd/.github/workflows/ci.yml`:*
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Lint with Ruff
        run: ruff check .

      - name: Type check with Mypy
        run: mypy src/

      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
```

**Missing checks:**
- ❌ Code duplication detection (jscpd, cloc)
- ❌ Cyclomatic complexity limits (radon cc)
- ❌ Maintainability index (radon mi)
- ❌ Dependency count limits
- ❌ File size limits

**Impact:**
- KISS violations (complex functions) slip through
- DRY violations (duplicated code) not caught
- YAGNI violations (unused dependencies) accumulate

#### 4. Missing Anti-Patterns

**Current anti-pattern coverage:** 6 documented
**Missing critical anti-patterns:** 4

| Anti-Pattern | Principle | Priority | Current Status |
|-------------|-----------|----------|----------------|
| Copy-Paste Programming | DRY | 🟠 HIGH | ❌ Not documented |
| God Object | KISS | 🟠 HIGH | ❌ Not documented |
| Speculative Generality | YAGNI | 🟡 MEDIUM | ❌ Not documented |
| Premature Infrastructure | KISS + YAGNI | 🟠 HIGH | ❌ Not documented |

**Impact:** Agents repeat these mistakes without guidance on detection/prevention

---

## Goals and Success Criteria

### Primary Goals

1. **Make principles explicit and teachable**
   - ✅ Success: AI agents can explain WHY architecture enforces DRY/KISS/YAGNI
   - ✅ Measurement: Agent responses reference principle guides when making decisions

2. **Eliminate shared code duplication**
   - ✅ Success: Code duplication drops from ~25% to <10% in generated projects
   - ✅ Measurement: `jscpd` reports duplication <10% threshold

3. **Prevent complexity violations**
   - ✅ Success: 100% of functions have McCabe complexity <10
   - ✅ Measurement: `radon cc --min B` passes in CI

4. **Complete template coverage**
   - ✅ Success: All 6 service templates at 100% completion
   - ✅ Measurement: `templates/README.md` shows 100% for all components

5. **Automate principle enforcement**
   - ✅ Success: CI pipeline blocks PRs violating DRY/KISS/YAGNI
   - ✅ Measurement: CI config includes 5+ principle-specific checks

### Secondary Goals

6. **Document upgrade triggers for maturity levels**
   - ✅ Success: Developers know WHEN to upgrade (evidence-driven)
   - ✅ Measurement: maturity-levels.md includes "Upgrade Triggers" section

7. **Add feature necessity validation**
   - ✅ Success: Stage 1 challenges unnecessary features
   - ✅ Measurement: Workflow includes "Feature Necessity Challenge" step

8. **Expand anti-pattern library**
   - ✅ Success: 10 total anti-patterns documented (current 6 + new 4)
   - ✅ Measurement: INDEX.md lists all 10 with monitoring commands

---

## Detailed Implementation Plan

### Phase 1: Critical Improvements (P0)

**Estimated Effort:** 40-50 hours
**Target Completion:** Week 1-2

---

#### Task 1.1: Create DRY/KISS/YAGNI Principles Guide

**Status:** ⏸️ Not Started
**Priority:** 🔴 CRITICAL
**Estimated Time:** 8 hours
**Owner:** TBD

**Objective:**
Create comprehensive educational guide linking principles to framework architecture.

**Files to Create:**
- `.ai-framework/docs/guides/dry-kiss-yagni-principles.md`

**Acceptance Criteria:**
- [ ] Document explains DRY principle with 3+ examples (correct vs. wrong)
- [ ] Document explains KISS principle with maturity level examples
- [ ] Document explains YAGNI principle with feature justification template
- [ ] Links to architecture docs (HTTP-only pattern, maturity levels)
- [ ] Includes automated detection commands for each principle
- [ ] Cross-referenced from AGENTS.md and ARCHITECTURE.md
- [ ] Reviewed by 2+ maintainers

**Implementation Details:**

*File structure:*
```markdown
# DRY, KISS, YAGNI Principles

## Table of Contents
1. DRY (Don't Repeat Yourself)
2. KISS (Keep It Simple, Stupid)
3. YAGNI (You Aren't Gonna Need It)
4. How Framework Enforces Principles
5. Automated Detection Tools
6. Related Documents

## 1. DRY (Don't Repeat Yourself)

### Definition
Every piece of knowledge must have a single, unambiguous representation in the system.

### How Framework Enforces DRY

**Architectural Pattern: HTTP-Only Data Access**

The framework enforces DRY by requiring all business services to access data via HTTP:

✅ **CORRECT - Single Source of Truth:**
```python
# Business Service: auth_api/src/services/user_service.py
class UserService:
    def __init__(self, data_client: DataClient):
        self._data_client = data_client

    async def get_user(self, user_id: int) -> User:
        # HTTP call to data service (single source of truth)
        response = await self._data_client.get(f"/users/{user_id}")
        return User(**response.json())

# Data Service: data_postgres_api/src/repositories/user_repository.py
class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    async def get_by_id(self, user_id: int) -> UserModel:
        # Only place with direct database access
        return self._db.query(UserModel).filter(UserModel.id == user_id).first()
```

❌ **WRONG - Duplicated Database Logic:**
```python
# Business Service 1: auth_api/src/services/user_service.py
async def get_user(self, user_id: int) -> User:
    # Direct database access - VIOLATES ARCHITECTURE
    user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
    return User.from_orm(user)

# Business Service 2: profile_api/src/services/profile_service.py
async def get_user(self, user_id: int) -> User:
    # DUPLICATED: Same query in different service
    user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
    return User.from_orm(user)

# Business Service 3: payment_api/src/services/payment_service.py
async def get_user(self, user_id: int) -> User:
    # DUPLICATED AGAIN: Now bug fixes require changing 3 places
    user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
    return User.from_orm(user)
```

**Why This Matters:**
- Single source of truth for database operations
- Bug fix in UserRepository.get_by_id automatically fixes all consumers
- No possibility of inconsistent query logic across services
- Easier connection pool management (one pool, not N pools)

[... continue with more examples ...]

### Automated Detection

**Check code duplication percentage:**
```bash
# Install jscpd
npm install -g jscpd

# Scan for duplicates (fail if >10%)
jscpd src/ --threshold 10 --exitCode 1

# Detailed report
jscpd src/ --format html --output ./jscpd-report
```

**Find similar files:**
```bash
# Using cloc
cloc --by-file --csv src/ | awk -F',' '$5 > 80 {print $2, $5"%"}'
# Output shows files with >80% similarity
```

**Find duplicated functions:**
```bash
# Using PMD CPD
pmd cpd --minimum-tokens 50 --files src/ --language python
```

[... continue for KISS and YAGNI ...]
```

**Testing:**
```bash
# Validate Markdown syntax
markdownlint docs/guides/dry-kiss-yagni-principles.md

# Check links are valid
markdown-link-check docs/guides/dry-kiss-yagni-principles.md

# Preview in mkdocs
mkdocs serve
```

---

#### Task 1.2: Implement Shared Utilities Template

**Status:** ⏸️ Not Started
**Priority:** 🔴 CRITICAL
**Estimated Time:** 12 hours
**Owner:** TBD

**Objective:**
Create reusable shared utilities to eliminate duplication across all services.

**Files to Create:**
1. `.ai-framework/templates/shared/utils/__init__.py`
2. `.ai-framework/templates/shared/utils/logger.py`
3. `.ai-framework/templates/shared/utils/validators.py`
4. `.ai-framework/templates/shared/utils/exceptions.py`
5. `.ai-framework/templates/shared/utils/pagination.py`
6. `.ai-framework/templates/shared/utils/request_id.py`
7. `.ai-framework/templates/shared/utils/README.md`

**Files to Update:**
- `.ai-framework/templates/README.md` (update completion status to 100%)

**Acceptance Criteria:**
- [ ] logger.py provides structured JSON logging factory
- [ ] validators.py includes 10+ common validators (email, phone, UUID, etc.)
- [ ] exceptions.py defines base exception hierarchy
- [ ] pagination.py supports both offset and cursor pagination
- [ ] request_id.py manages correlation IDs across service boundaries
- [ ] All files have 100% type hint coverage
- [ ] All files have comprehensive docstrings (Google style)
- [ ] README.md documents usage patterns for each utility
- [ ] Unit tests achieve 100% coverage
- [ ] No business logic or project-specific code

**Implementation Details:**

*1. logger.py - Structured JSON Logging*

```python
"""Centralized logging configuration for all services.

This module provides a factory for creating structured JSON loggers
with consistent formatting across the microservices ecosystem.
"""

import logging
import sys
from typing import Optional

from pythonjsonlogger import jsonlogger


def create_logger(
    name: str,
    level: str = "INFO",
    include_request_id: bool = True,
) -> logging.Logger:
    """Create structured JSON logger.

    Args:
        name: Logger name (typically __name__ of calling module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        include_request_id: Whether to include request_id in log format

    Returns:
        Configured logger instance with JSON formatting

    Example:
        >>> from shared.utils.logger import create_logger
        >>> logger = create_logger(__name__)
        >>> logger.info("User authenticated", extra={"user_id": 123})
        # Output: {"asctime": "2025-01-07T10:30:00", "name": "auth_service",
        #          "levelname": "INFO", "message": "User authenticated",
        #          "user_id": 123, "request_id": "abc-123"}
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stdout)

    # Build format string
    format_fields = [
        "%(asctime)s",
        "%(name)s",
        "%(levelname)s",
        "%(message)s",
    ]

    if include_request_id:
        format_fields.append("%(request_id)s")

    formatter = jsonlogger.JsonFormatter(" ".join(format_fields))
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


class RequestIdFilter(logging.Filter):
    """Inject request_id into all log records.

    This filter should be added to loggers in API services
    to automatically include correlation IDs in logs.
    """

    def __init__(self, get_request_id_func) -> None:
        """Initialize filter with request ID getter function.

        Args:
            get_request_id_func: Callable that returns current request ID
        """
        super().__init__()
        self._get_request_id = get_request_id_func

    def filter(self, record: logging.LogRecord) -> bool:
        """Add request_id to log record.

        Args:
            record: Log record to modify

        Returns:
            True (always pass through)
        """
        record.request_id = self._get_request_id() or "no-request-id"
        return True


def configure_uvicorn_logging(level: str = "INFO") -> None:
    """Configure uvicorn access logs to use JSON format.

    Call this in FastAPI startup event to ensure consistent
    log formatting for HTTP access logs.

    Args:
        level: Logging level for uvicorn loggers

    Example:
        >>> from fastapi import FastAPI
        >>> app = FastAPI()
        >>> @app.on_event("startup")
        >>> async def startup():
        >>>     configure_uvicorn_logging()
    """
    uvicorn_loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]

    for logger_name in uvicorn_loggers:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()

        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(level.upper())
```

*2. validators.py - Reusable Validation Functions*

```python
"""Common validation functions used across services.

Provides reusable validators for email, phone, UUID, and other
common data types. Use these instead of duplicating validation logic.
"""

import re
from typing import Optional
from uuid import UUID


def is_valid_email(email: str) -> bool:
    """Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise

    Example:
        >>> is_valid_email("user@example.com")
        True
        >>> is_valid_email("invalid-email")
        False
    """
    if not email or len(email) > 254:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str, country_code: str = "US") -> bool:
    """Validate phone number format.

    Args:
        phone: Phone number to validate
        country_code: ISO 3166-1 alpha-2 country code

    Returns:
        True if phone format is valid for country, False otherwise

    Example:
        >>> is_valid_phone("+1-555-123-4567", "US")
        True
        >>> is_valid_phone("123", "US")
        False

    Note:
        For production, consider using phonenumbers library for
        comprehensive international phone validation.
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)

    if country_code == "US":
        # US: 10 digits, optional +1 prefix
        pattern = r'^(\+1)?[2-9]\d{9}$'
        return bool(re.match(pattern, cleaned))

    # Generic: 7-15 digits, optional + prefix
    pattern = r'^\+?\d{7,15}$'
    return bool(re.match(pattern, cleaned))


def is_valid_uuid(value: str) -> bool:
    """Validate UUID format.

    Args:
        value: String to validate as UUID

    Returns:
        True if valid UUID format, False otherwise

    Example:
        >>> is_valid_uuid("123e4567-e89b-12d3-a456-426614174000")
        True
        >>> is_valid_uuid("invalid-uuid")
        False
    """
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def is_valid_url(url: str, require_https: bool = False) -> bool:
    """Validate URL format.

    Args:
        url: URL string to validate
        require_https: If True, only accept HTTPS URLs

    Returns:
        True if valid URL format, False otherwise

    Example:
        >>> is_valid_url("https://example.com/path")
        True
        >>> is_valid_url("not-a-url")
        False
    """
    if require_https:
        pattern = r'^https://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    else:
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'

    return bool(re.match(pattern, url))


def validate_password_strength(
    password: str,
    min_length: int = 8,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digit: bool = True,
    require_special: bool = True,
) -> tuple[bool, Optional[str]]:
    """Validate password meets strength requirements.

    Args:
        password: Password to validate
        min_length: Minimum password length
        require_uppercase: Require at least one uppercase letter
        require_lowercase: Require at least one lowercase letter
        require_digit: Require at least one digit
        require_special: Require at least one special character

    Returns:
        Tuple of (is_valid, error_message)
        error_message is None if valid

    Example:
        >>> validate_password_strength("Weak123!")
        (True, None)
        >>> validate_password_strength("weak")
        (False, "Password must be at least 8 characters")
    """
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"

    if require_uppercase and not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if require_lowercase and not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if require_digit and not re.search(r'\d', password):
        return False, "Password must contain at least one digit"

    if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"

    return True, None


# Add more validators: is_valid_slug, is_valid_hex_color, etc.
```

*3. exceptions.py - Base Exception Hierarchy*

```python
"""Base exception classes for framework services.

Provides consistent exception hierarchy with proper HTTP status code
mapping for API services.
"""

from typing import Optional, Any


class BaseServiceException(Exception):
    """Base exception for all service errors.

    All custom exceptions should inherit from this class
    to enable consistent error handling.

    Attributes:
        message: Human-readable error message
        error_code: Machine-readable error code (e.g., "USER_NOT_FOUND")
        status_code: HTTP status code for API responses
        details: Additional error context
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize service exception.

        Args:
            message: Error message for users/logs
            error_code: Structured error code
            status_code: HTTP status code
            details: Optional additional context
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(BaseServiceException):
    """Resource not found (HTTP 404)."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: str = "NOT_FOUND",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404,
            details=details,
        )


class ValidationError(BaseServiceException):
    """Validation failed (HTTP 422)."""

    def __init__(
        self,
        message: str = "Validation failed",
        error_code: str = "VALIDATION_ERROR",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=422,
            details=details,
        )


class UnauthorizedError(BaseServiceException):
    """Authentication required (HTTP 401)."""

    def __init__(
        self,
        message: str = "Authentication required",
        error_code: str = "UNAUTHORIZED",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            details=details,
        )


class ForbiddenError(BaseServiceException):
    """Permission denied (HTTP 403)."""

    def __init__(
        self,
        message: str = "Permission denied",
        error_code: str = "FORBIDDEN",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=403,
            details=details,
        )


class ConflictError(BaseServiceException):
    """Resource conflict (HTTP 409).

    Example: Trying to create user with existing email.
    """

    def __init__(
        self,
        message: str = "Resource conflict",
        error_code: str = "CONFLICT",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=409,
            details=details,
        )


class ExternalServiceError(BaseServiceException):
    """External service call failed (HTTP 502/503)."""

    def __init__(
        self,
        message: str = "External service unavailable",
        error_code: str = "EXTERNAL_SERVICE_ERROR",
        status_code: int = 503,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=status_code,
            details=details,
        )


class RateLimitError(BaseServiceException):
    """Rate limit exceeded (HTTP 429)."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        error_code: str = "RATE_LIMIT_EXCEEDED",
        retry_after: Optional[int] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        details = details or {}
        if retry_after:
            details["retry_after"] = retry_after

        super().__init__(
            message=message,
            error_code=error_code,
            status_code=429,
            details=details,
        )
```

*4. pagination.py - Offset and Cursor Pagination*

```python
"""Pagination utilities for API responses.

Supports both offset-based and cursor-based pagination patterns.
"""

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field


T = TypeVar("T")


class OffsetPaginationParams(BaseModel):
    """Query parameters for offset-based pagination.

    Example:
        GET /users?limit=20&offset=40
    """

    limit: int = Field(default=20, ge=1, le=100, description="Items per page")
    offset: int = Field(default=0, ge=0, description="Items to skip")

    @property
    def skip(self) -> int:
        """Alias for offset (used in database queries)."""
        return self.offset


class OffsetPaginatedResponse(BaseModel, Generic[T]):
    """Response structure for offset-based pagination.

    Attributes:
        items: List of items for current page
        total: Total number of items across all pages
        limit: Items per page
        offset: Current offset
        has_next: Whether there are more pages
    """

    items: list[T]
    total: int
    limit: int
    offset: int

    @property
    def has_next(self) -> bool:
        """Check if there are more pages."""
        return self.offset + self.limit < self.total

    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page."""
        return self.offset > 0


class CursorPaginationParams(BaseModel):
    """Query parameters for cursor-based pagination.

    Cursor pagination is more efficient for large datasets
    and prevents issues with concurrent modifications.

    Example:
        GET /posts?limit=20&cursor=eyJpZCI6MTIzfQ
    """

    limit: int = Field(default=20, ge=1, le=100, description="Items per page")
    cursor: Optional[str] = Field(default=None, description="Pagination cursor")


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """Response structure for cursor-based pagination.

    Attributes:
        items: List of items for current page
        next_cursor: Cursor for next page (None if last page)
        has_next: Whether there are more pages
    """

    items: list[T]
    next_cursor: Optional[str] = None

    @property
    def has_next(self) -> bool:
        """Check if there are more pages."""
        return self.next_cursor is not None


def create_cursor(entity_id: int) -> str:
    """Create base64-encoded cursor from entity ID.

    Args:
        entity_id: ID of last entity in current page

    Returns:
        Base64-encoded cursor string

    Example:
        >>> create_cursor(123)
        'eyJpZCI6MTIzfQ=='
    """
    import base64
    import json

    cursor_data = {"id": entity_id}
    cursor_json = json.dumps(cursor_data)
    return base64.b64encode(cursor_json.encode()).decode()


def parse_cursor(cursor: str) -> dict:
    """Parse base64-encoded cursor to extract entity ID.

    Args:
        cursor: Base64-encoded cursor string

    Returns:
        Dictionary with cursor data (contains 'id' key)

    Raises:
        ValueError: If cursor format is invalid

    Example:
        >>> parse_cursor('eyJpZCI6MTIzfQ==')
        {'id': 123}
    """
    import base64
    import json

    try:
        cursor_json = base64.b64decode(cursor.encode()).decode()
        return json.loads(cursor_json)
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid cursor format: {e}")
```

*5. request_id.py - Correlation ID Management*

```python
"""Request ID (correlation ID) management for distributed tracing.

Provides context variables for propagating request IDs across
async function calls and service boundaries.
"""

import uuid
from contextvars import ContextVar
from typing import Optional


# Context variable for current request ID
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    "request_id", default=None
)


def generate_request_id() -> str:
    """Generate new UUID-based request ID.

    Returns:
        UUID string in format: req_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    Example:
        >>> generate_request_id()
        'req_123e4567-e89b-12d3-a456-426614174000'
    """
    return f"req_{uuid.uuid4()}"


def set_request_id(request_id: str) -> None:
    """Set request ID in context.

    This should be called at the start of request processing
    (e.g., in FastAPI middleware or Aiogram middleware).

    Args:
        request_id: Request ID to set

    Example:
        >>> set_request_id("req_123")
        >>> get_request_id()
        'req_123'
    """
    _request_id_ctx_var.set(request_id)


def get_request_id() -> Optional[str]:
    """Get current request ID from context.

    Returns:
        Current request ID, or None if not set

    Example:
        >>> set_request_id("req_123")
        >>> get_request_id()
        'req_123'
    """
    return _request_id_ctx_var.get()


def get_or_generate_request_id() -> str:
    """Get current request ID or generate new one.

    This is useful for background tasks that may not have
    a request ID set in context.

    Returns:
        Current request ID or newly generated one

    Example:
        >>> get_or_generate_request_id()  # No request ID set
        'req_abc-123...'
        >>> set_request_id("req_xyz")
        >>> get_or_generate_request_id()  # Request ID is set
        'req_xyz'
    """
    request_id = get_request_id()
    if request_id is None:
        request_id = generate_request_id()
        set_request_id(request_id)
    return request_id
```

*6. shared/utils/README.md - Usage Documentation*

```markdown
# Shared Utilities

Reusable utility functions and classes used across all framework services.

## Purpose

These utilities eliminate code duplication by providing:
- ✅ Structured JSON logging (no duplication of logging setup)
- ✅ Common validators (no duplication of email/phone/UUID validation)
- ✅ Base exception hierarchy (consistent error handling)
- ✅ Pagination helpers (no duplication of pagination logic)
- ✅ Request ID management (distributed tracing support)

## Design Principles

**100% Universal:**
- No business logic
- No project-specific code
- No database or external service dependencies

**Type-Safe:**
- 100% type hint coverage
- Passes mypy strict mode

**Well-Tested:**
- 100% test coverage
- Comprehensive docstrings with examples

## Usage Guide

### Logger

**Problem:** Every service duplicates logging configuration

**Solution:** Use `create_logger` factory

```python
# ❌ BEFORE - Duplicated in every service
import logging
import sys
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter("%(asctime)s %(name)s ...")
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)

# ✅ AFTER - One line, consistent across all services
from shared.utils.logger import create_logger

logger = create_logger(__name__)
logger.info("User authenticated", extra={"user_id": 123})
```

[... continue with usage examples for each utility ...]
```

**Testing Strategy:**

```python
# tests/unit/shared/utils/test_logger.py
import pytest
import logging
import json
from io import StringIO

from shared.utils.logger import create_logger, configure_uvicorn_logging


def test_create_logger_json_format(caplog):
    """Logger should output JSON formatted logs."""
    logger = create_logger("test_service", level="INFO")

    with caplog.at_level(logging.INFO):
        logger.info("Test message", extra={"user_id": 123})

    log_output = caplog.records[0]
    assert log_output.name == "test_service"
    assert log_output.levelname == "INFO"
    assert log_output.getMessage() == "Test message"
    # Verify JSON structure in formatter output


def test_create_logger_no_duplicate_handlers():
    """Creating logger twice should not add duplicate handlers."""
    logger1 = create_logger("test_service")
    initial_handlers = len(logger1.handlers)

    logger2 = create_logger("test_service")
    final_handlers = len(logger2.handlers)

    assert initial_handlers == final_handlers == 1


# ... more tests for validators, exceptions, pagination, request_id ...
```

---

#### Task 1.3: Implement Data Service Template (PostgreSQL)

**Status:** ⏸️ Not Started
**Priority:** 🔴 CRITICAL
**Estimated Time:** 16 hours
**Owner:** TBD

**Objective:**
Create complete PostgreSQL data service template to eliminate reinventing data layer.

**Files to Create:**
*Directory structure:*
```
templates/services/template_data_postgres_api/
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── .env.example
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── src/
│   ├── __init__.py
│   ├── main.py                        # FastAPI app
│   ├── core/
│   │   ├── config.py                  # Settings
│   │   ├── database.py                # SQLAlchemy setup
│   │   └── logging_config.py          # Uses shared/utils/logger
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py                    # SQLAlchemy Base + mixins
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base_repository.py         # Generic CRUD repository
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── base.py                    # Pydantic base schemas
│   └── api/
│       └── v1/
│           ├── __init__.py
│           ├── health.py              # Health check endpoint
│           └── router.py              # Main router
└── tests/
    ├── __init__.py
    ├── conftest.py                    # Shared fixtures
    ├── unit/
    │   └── repositories/
    │       └── test_base_repository.py
    └── integration/
        └── test_database_connection.py
```

**Acceptance Criteria:**
- [ ] SQLAlchemy 2.0+ with async support
- [ ] Base model with id, created_at, updated_at columns
- [ ] Generic repository with CRUD operations (create, get, list, update, delete)
- [ ] Alembic migrations configured
- [ ] Health check endpoint verifies database connectivity
- [ ] Integration tests use Testcontainers for PostgreSQL
- [ ] Connection pooling configured (min 5, max 20)
- [ ] All database operations use async/await
- [ ] 100% type hint coverage
- [ ] Comprehensive docstrings

**Implementation Details:**

*core/database.py - SQLAlchemy Async Setup*

```python
"""Database connection and session management.

Provides async SQLAlchemy engine and session factory with
connection pooling and health check support.
"""

from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool, QueuePool

from core.config import settings
from shared.utils.logger import create_logger


logger = create_logger(__name__)


def create_engine() -> AsyncEngine:
    """Create async SQLAlchemy engine with connection pooling.

    Returns:
        Configured async engine instance

    Configuration:
        - Pool size: 5-20 connections (min-max)
        - Pool pre-ping: True (verify connections before use)
        - Echo: True in development (log SQL queries)
        - Connect args: prepared statements disabled for better compatibility
    """
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        poolclass=QueuePool if not settings.TESTING else NullPool,
        pool_size=5,
        max_overflow=15,
        pool_pre_ping=True,
        connect_args={
            "prepared_statement_cache_size": 0,  # Disable for pgbouncer compatibility
        },
    )


# Global engine instance (created once at startup)
engine: AsyncEngine = create_engine()

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI endpoints to get database session.

    Yields:
        Async session instance

    Example:
        >>> from fastapi import Depends
        >>> @app.get("/users/{user_id}")
        >>> async def get_user(
        >>>     user_id: int,
        >>>     session: AsyncSession = Depends(get_session)
        >>> ):
        >>>     user = await session.get(UserModel, user_id)
        >>>     return user
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


async def check_database_connection() -> bool:
    """Check if database is accessible.

    Returns:
        True if database connection successful, False otherwise

    Used by health check endpoint to verify database status.
    """
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


@asynccontextmanager
async def get_session_context():
    """Context manager for manual session management.

    Use when you need explicit transaction control outside
    of FastAPI dependency injection.

    Example:
        >>> async with get_session_context() as session:
        >>>     user = await session.get(UserModel, 1)
        >>>     user.name = "Updated"
        >>>     # Committed automatically on context exit
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

*models/base.py - Base Model with Timestamp Mixins*

```python
"""Base SQLAlchemy model and mixins.

Provides base model class with common columns and utility methods.
"""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr


class CustomBase:
    """Base class with common columns and methods."""

    # Primary key (all tables have 'id')
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ from class name.

        Example:
            UserModel -> user_model
            PostComment -> post_comment
        """
        import re
        # Convert CamelCase to snake_case
        name = cls.__name__
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to dictionary.

        Returns:
            Dictionary with all column values

        Example:
            >>> user = UserModel(id=1, email="user@example.com")
            >>> user.to_dict()
            {'id': 1, 'email': 'user@example.com', 'created_at': '...'}
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


Base = declarative_base(cls=CustomBase)


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps.

    Usage:
        >>> class UserModel(Base, TimestampMixin):
        >>>     email = Column(String, unique=True)
        >>>
        >>> # Automatically has created_at and updated_at columns
    """

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="Timestamp when record was created",
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="Timestamp when record was last updated",
    )
```

*repositories/base_repository.py - Generic CRUD Repository*

```python
"""Base repository with generic CRUD operations.

Provides reusable repository pattern for all models, eliminating
code duplication for common database operations.
"""

from typing import Generic, TypeVar, Type, Optional, Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository with CRUD operations.

    This repository implements common database operations that work
    with any SQLAlchemy model. Inherit from this class for
    model-specific repositories.

    Example:
        >>> class UserRepository(BaseRepository[UserModel]):
        >>>     def __init__(self, session: AsyncSession):
        >>>         super().__init__(UserModel, session)
        >>>
        >>>     async def get_by_email(self, email: str) -> Optional[UserModel]:
        >>>         result = await self._session.execute(
        >>>             select(self._model).where(self._model.email == email)
        >>>         )
        >>>         return result.scalar_one_or_none()
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """Initialize repository.

        Args:
            model: SQLAlchemy model class
            session: Async database session
        """
        self._model = model
        self._session = session

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get single record by ID.

        Args:
            id: Primary key value

        Returns:
            Model instance or None if not found
        """
        result = await self._session.execute(
            select(self._model).where(self._model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        """Get all records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        result = await self._session.execute(
            select(self._model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, **kwargs) -> ModelType:
        """Create new record.

        Args:
            **kwargs: Column values for new record

        Returns:
            Created model instance with generated ID

        Example:
            >>> user = await repo.create(email="user@example.com", name="John")
            >>> print(user.id)  # Auto-generated ID
            1
        """
        instance = self._model(**kwargs)
        self._session.add(instance)
        await self._session.flush()  # Generate ID
        await self._session.refresh(instance)  # Load defaults
        return instance

    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update existing record.

        Args:
            id: Primary key of record to update
            **kwargs: Column values to update

        Returns:
            Updated model instance or None if not found

        Example:
            >>> user = await repo.update(1, name="Jane", email="jane@example.com")
        """
        await self._session.execute(
            update(self._model)
            .where(self._model.id == id)
            .values(**kwargs)
        )
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        """Delete record by ID.

        Args:
            id: Primary key of record to delete

        Returns:
            True if record was deleted, False if not found

        Example:
            >>> deleted = await repo.delete(1)
            >>> print(deleted)
            True
        """
        result = await self._session.execute(
            delete(self._model).where(self._model.id == id)
        )
        return result.rowcount > 0

    async def count(self) -> int:
        """Count total number of records.

        Returns:
            Total record count

        Example:
            >>> total = await repo.count()
            >>> print(f"Total users: {total}")
            Total users: 150
        """
        result = await self._session.execute(
            select(func.count()).select_from(self._model)
        )
        return result.scalar()
```

[... Continue with alembic setup, health check endpoint, tests ...]

**Testing Strategy:**

```python
# tests/integration/test_database_connection.py
import pytest
from testcontainers.postgres import PostgresContainer

from core.database import create_engine, check_database_connection


@pytest.fixture(scope="module")
def postgres_container():
    """Start PostgreSQL container for tests."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture
def database_url(postgres_container):
    """Get database URL from container."""
    return postgres_container.get_connection_url().replace(
        "psycopg2", "asyncpg"
    )


@pytest.mark.asyncio
async def test_database_connection(database_url, monkeypatch):
    """Database connection should succeed with valid credentials."""
    monkeypatch.setenv("DATABASE_URL", database_url)

    is_connected = await check_database_connection()

    assert is_connected is True


@pytest.mark.asyncio
async def test_database_connection_failure(monkeypatch):
    """Database connection should fail with invalid credentials."""
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://invalid:invalid@localhost:5432/invalid")

    is_connected = await check_database_connection()

    assert is_connected is False
```

---

#### Task 1.4: Add Automated Quality Gates to CI Pipeline

**Status:** ⏸️ Not Started
**Priority:** 🔴 CRITICAL
**Estimated Time:** 4 hours
**Owner:** TBD

**Objective:**
Add automated checks to CI pipeline to enforce DRY/KISS/YAGNI principles.

**Files to Update:**
- `.ai-framework/templates/ci-cd/.github/workflows/ci.yml`

**Acceptance Criteria:**
- [ ] CI checks code duplication with jscpd (fail if >10%)
- [ ] CI checks cyclomatic complexity with radon (fail if any function >10)
- [ ] CI checks maintainability index with radon (fail if any file <B grade)
- [ ] CI checks dependency count (fail if requirements.txt >30 for Level 1-2)
- [ ] CI checks file size (fail if any file >500 lines)
- [ ] All checks have clear error messages explaining violations
- [ ] Documentation updated with CI check descriptions

**Implementation Details:**

*Updated CI Workflow:*

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # Existing jobs
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ruff mypy
          pip install -r requirements.txt

      - name: Lint with Ruff
        run: ruff check .

      - name: Type check with Mypy
        run: mypy src/ --strict

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest pytest-cov pytest-asyncio
          pip install -r requirements.txt

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=xml \
            --cov-report=term-missing \
            --cov-fail-under=80

  # NEW: DRY/KISS/YAGNI Enforcement Jobs
  check-duplication:
    name: Check Code Duplication (DRY)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install jscpd
        run: npm install -g jscpd

      - name: Check for code duplication
        run: |
          echo "Checking code duplication (DRY principle)..."
          echo "Threshold: 10% (will fail if higher)"

          jscpd src/ \
            --threshold 10 \
            --format "python" \
            --reporters "console,html" \
            --output "./jscpd-report" \
            --exitCode 1 || {
              echo ""
              echo "❌ DRY VIOLATION: Code duplication exceeds 10% threshold"
              echo ""
              echo "Duplicated code violates the DRY (Don't Repeat Yourself) principle."
              echo "Consider extracting shared code to:"
              echo "  - shared/utils/ for reusable utilities"
              echo "  - infrastructure/ for HTTP clients, messaging, etc."
              echo "  - Base classes for common patterns"
              echo ""
              echo "See detailed report in jscpd-report/jscpd-report.html"
              echo ""
              echo "Learn more: docs/guides/dry-kiss-yagni-principles.md#dry"
              exit 1
            }

      - name: Upload duplication report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: jscpd-report
          path: ./jscpd-report

  check-complexity:
    name: Check Code Complexity (KISS)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install radon
        run: pip install radon

      - name: Check cyclomatic complexity
        run: |
          echo "Checking cyclomatic complexity (KISS principle)..."
          echo "Threshold: McCabe complexity < 10 for all functions"

          radon cc src/ --min B --total-average --show-complexity || {
            echo ""
            echo "❌ KISS VIOLATION: Functions with complexity >= 10 detected"
            echo ""
            echo "Complex functions violate the KISS (Keep It Simple) principle."
            echo "Consider refactoring by:"
            echo "  - Breaking large functions into smaller ones"
            echo "  - Extracting conditional logic into separate functions"
            echo "  - Using early returns to reduce nesting"
            echo "  - Applying strategy pattern for complex conditionals"
            echo ""
            echo "Learn more: docs/guides/dry-kiss-yagni-principles.md#kiss"
            exit 1
          }

      - name: Check maintainability index
        run: |
          echo "Checking maintainability index (KISS principle)..."
          echo "Threshold: Grade B or better (MI >= 20)"

          radon mi src/ --min B --show || {
            echo ""
            echo "❌ KISS VIOLATION: Low maintainability index detected"
            echo ""
            echo "Low maintainability indicates overly complex code."
            echo "Maintainability Index considers:"
            echo "  - Cyclomatic complexity"
            echo "  - Lines of code"
            echo "  - Halstead volume"
            echo "  - Comment density"
            echo ""
            echo "Learn more: docs/guides/dry-kiss-yagni-principles.md#kiss"
            exit 1
          }

      - name: Check file sizes
        run: |
          echo "Checking file sizes (KISS principle)..."
          echo "Threshold: No file > 500 lines"

          large_files=$(find src/ -name "*.py" -type f -exec wc -l {} \; | awk '$1 > 500 {print $2, "("$1" lines)"}')

          if [ -n "$large_files" ]; then
            echo ""
            echo "❌ KISS VIOLATION: Files exceeding 500 lines detected"
            echo ""
            echo "$large_files"
            echo ""
            echo "Large files are harder to understand and maintain."
            echo "Consider splitting into:"
            echo "  - Multiple focused modules"
            echo "  - Separate classes with single responsibilities"
            echo "  - Service layer + repository layer"
            echo ""
            echo "Learn more: docs/guides/dry-kiss-yagni-principles.md#kiss"
            exit 1
          fi

  check-dependencies:
    name: Check Dependency Bloat (YAGNI)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check dependency count
        run: |
          echo "Checking dependency count (YAGNI principle)..."

          # Count non-comment, non-empty lines in requirements.txt
          dep_count=$(grep -v '^#' requirements.txt | grep -v '^$' | wc -l)

          echo "Total dependencies: $dep_count"

          # Threshold varies by maturity level
          # Level 1-2: max 30, Level 3-4: max 50
          # For template validation, use Level 2 threshold
          threshold=30

          if [ $dep_count -gt $threshold ]; then
            echo ""
            echo "❌ YAGNI VIOLATION: Too many dependencies ($dep_count > $threshold)"
            echo ""
            echo "Excessive dependencies indicate:"
            echo "  - Features that aren't needed yet (YAGNI)"
            echo "  - Increased attack surface"
            echo "  - Slower installation and docker builds"
            echo ""
            echo "Review each dependency:"
            echo "  - Is it required for current maturity level?"
            echo "  - Can we use stdlib instead?"
            echo "  - Are there unused dependencies from earlier iterations?"
            echo ""
            echo "Learn more: docs/guides/dry-kiss-yagni-principles.md#yagni"
            exit 1
          fi

      - name: Check for unused dependencies
        run: |
          pip install pip-check || true

          echo "Checking for unused dependencies..."
          pip-check --verbose || {
            echo ""
            echo "⚠️  WARNING: Some dependencies may be unused"
            echo "Consider running: pip-autoremove to clean up"
          }

  # Summary job
  quality-gates:
    name: Quality Gates Summary
    runs-on: ubuntu-latest
    needs: [lint, test, check-duplication, check-complexity, check-dependencies]
    if: always()
    steps:
      - name: Check all gates passed
        run: |
          echo "Quality Gates Status:"
          echo "  - Linting: ${{ needs.lint.result }}"
          echo "  - Tests: ${{ needs.test.result }}"
          echo "  - DRY (Duplication): ${{ needs.check-duplication.result }}"
          echo "  - KISS (Complexity): ${{ needs.check-complexity.result }}"
          echo "  - YAGNI (Dependencies): ${{ needs.check-dependencies.result }}"

          if [[ "${{ needs.lint.result }}" != "success" ]] || \
             [[ "${{ needs.test.result }}" != "success" ]] || \
             [[ "${{ needs.check-duplication.result }}" != "success" ]] || \
             [[ "${{ needs.check-complexity.result }}" != "success" ]] || \
             [[ "${{ needs.check-dependencies.result }}" != "success" ]]; then
            echo ""
            echo "❌ Quality gates failed. See job details above."
            exit 1
          fi

          echo ""
          echo "✅ All quality gates passed!"
```

**Documentation Update:**

Create `.ai-framework/docs/quality/automated-quality-gates.md`:

```markdown
# Automated Quality Gates

## Overview

The CI pipeline enforces DRY, KISS, and YAGNI principles through automated checks.

## Quality Gate Jobs

### 1. check-duplication (DRY Enforcement)

**Tool:** jscpd (JavaScript Copy/Paste Detector)
**Threshold:** 10% duplication max
**Fails if:** Code duplication exceeds threshold

**What it checks:**
- Duplicated code blocks across files
- Copy-paste patterns
- Similar code structures

**How to fix:**
```bash
# Generate duplication report locally
npm install -g jscpd
jscpd src/ --reporters "console,html" --output "./report"
open report/jscpd-report.html

# Common fixes:
# 1. Extract to shared/utils/
# 2. Create base classes
# 3. Use composition over duplication
```

### 2. check-complexity (KISS Enforcement)

**Tool:** radon
**Thresholds:**
- McCabe complexity < 10 per function
- Maintainability Index >= 20 (Grade B)
- File size < 500 lines

**Fails if:** Any function/file exceeds thresholds

**What it checks:**
- Cyclomatic complexity (number of code paths)
- Maintainability index (composite metric)
- File sizes

**How to fix:**
```bash
# Check complexity locally
pip install radon
radon cc src/ --show-complexity
radon mi src/ --show

# Find large files
find src/ -name "*.py" -exec wc -l {} \; | sort -rn | head -10

# Common fixes:
# 1. Extract methods (Replace Temp with Query)
# 2. Use early returns (Guard Clauses)
# 3. Apply strategy pattern
# 4. Split large classes
```

### 3. check-dependencies (YAGNI Enforcement)

**Tool:** grep + pip-check
**Thresholds:**
- Level 1-2: max 30 dependencies
- Level 3-4: max 50 dependencies

**Fails if:** Dependency count exceeds threshold

**What it checks:**
- Total number of dependencies
- Unused dependencies

**How to fix:**
```bash
# Check dependencies locally
wc -l < requirements.txt

# Find unused dependencies
pip install pip-check
pip-check

# Remove unused
pip install pip-autoremove
pip-autoremove <package-name> -y

# Common fixes:
# 1. Remove dev dependencies from production requirements
# 2. Use stdlib alternatives
# 3. Remove dependencies from earlier iterations
```

## Running Checks Locally

Before pushing, run all checks:

```bash
# Install tools
npm install -g jscpd
pip install radon pip-check

# Run checks
make quality-check  # If Makefile configured

# Or manually:
jscpd src/ --threshold 10
radon cc src/ --min B
radon mi src/ --min B
find src/ -name "*.py" -exec wc -l {} \; | awk '$1>500'
wc -l < requirements.txt
```

## CI Badge

Add to README.md:

```markdown
![Quality Gates](https://github.com/your-org/your-repo/actions/workflows/ci.yml/badge.svg)
```

## Related Documents

- [DRY/KISS/YAGNI Principles](../guides/dry-kiss-yagni-principles.md)
- [Code Review Checklist](../atomic/testing/quality-assurance/code-review-checklist.md)
```

---

### Phase 2: High Priority Improvements (P1)

**Estimated Effort:** 24-30 hours
**Target Completion:** Week 3

---

#### Task 2.1: Complete Business API Template

**Status:** ⏸️ Not Started
**Priority:** 🟠 HIGH
**Estimated Time:** 8 hours
**Owner:** TBD

**Objective:**
Complete template_business_api/ from 40% to 100% completion.

**Files to Create:**
1. `src/core/logging_config.py` - Uses shared/utils/logger
2. `src/core/middleware.py` - Request ID, error handling, CORS
3. `src/api/v1/health_router.py` - Health check endpoints
4. `src/infrastructure/http_clients/data_client.py` - HTTP client for data service
5. `src/infrastructure/http_clients/base_client.py` - Reusable HTTP client base
6. `src/infrastructure/rabbitmq/publisher.py` - Event publishing
7. `src/infrastructure/rabbitmq/consumer.py` - Event consumption
8. `tests/conftest.py` - Shared test fixtures

**Files to Update:**
- `src/main.py` - Register middleware and routers
- `templates/README.md` - Update completion status

**Acceptance Criteria:**
- [ ] All 8 missing files created with comprehensive implementation
- [ ] Middleware injects request_id into all requests
- [ ] Middleware handles BaseServiceException with proper HTTP responses
- [ ] Health check verifies connectivity to data service and RabbitMQ
- [ ] HTTP client uses httpx with connection pooling
- [ ] RabbitMQ publisher/consumer use aio-pika
- [ ] All files fully type-hinted and documented
- [ ] Unit tests cover 100% of new code
- [ ] Integration tests verify end-to-end flows

**Implementation Details:**

*src/core/middleware.py*

```python
"""FastAPI middleware for request ID injection and error handling."""

from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from shared.utils.request_id import (
    generate_request_id,
    set_request_id,
    get_request_id,
)
from shared.utils.exceptions import BaseServiceException
from shared.utils.logger import create_logger


logger = create_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Inject correlation ID into requests and responses.

    This middleware:
    1. Extracts X-Request-ID header from incoming request (if present)
    2. Generates new request ID if not provided
    3. Sets request ID in context for logging
    4. Adds X-Request-ID header to response
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Process request with request ID injection.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler

        Returns:
            HTTP response with X-Request-ID header
        """
        # Extract or generate request ID
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = generate_request_id()

        # Set in context for logging
        set_request_id(request_id)

        # Log request
        logger.info(
            f"{request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
            },
        )

        # Process request
        response = await call_next(request)

        # Add request ID to response
        response.headers["X-Request-ID"] = request_id

        # Log response
        logger.info(
            f"Response {response.status_code}",
            extra={
                "status_code": response.status_code,
            },
        )

        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """Global exception handler for BaseServiceException.

    Converts service exceptions to proper HTTP JSON responses
    with consistent error structure.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Handle exceptions and convert to JSON responses.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/route handler

        Returns:
            HTTP response (success or error)
        """
        try:
            response = await call_next(request)
            return response

        except BaseServiceException as e:
            # Expected service exceptions
            logger.warning(
                f"Service exception: {e.message}",
                extra={
                    "error_code": e.error_code,
                    "status_code": e.status_code,
                    "details": e.details,
                },
            )

            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": {
                        "code": e.error_code,
                        "message": e.message,
                        "details": e.details,
                        "request_id": get_request_id(),
                    }
                },
                headers={"X-Request-ID": get_request_id()},
            )

        except Exception as e:
            # Unexpected exceptions
            logger.error(
                f"Unhandled exception: {str(e)}",
                exc_info=True,
                extra={"exception_type": type(e).__name__},
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred",
                        "request_id": get_request_id(),
                    }
                },
                headers={"X-Request-ID": get_request_id()},
            )
```

*src/api/v1/health_router.py*

```python
"""Health check endpoints for monitoring and orchestration."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from infrastructure.http_clients.data_client import DataClient, get_data_client
from infrastructure.rabbitmq.publisher import check_rabbitmq_connection
from shared.utils.logger import create_logger


logger = create_logger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


class HealthResponse(BaseModel):
    """Health check response structure."""

    status: str
    version: str
    checks: dict[str, str]


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check (liveness probe).

    Returns 200 if service is running.
    Use this for Kubernetes liveness probe.

    Returns:
        Health status
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",  # TODO: Get from config
        checks={},
    )


@router.get("/ready", response_model=HealthResponse)
async def readiness_check(
    data_client: DataClient = Depends(get_data_client),
):
    """Readiness check (readiness probe).

    Verifies connectivity to all dependencies:
    - Data service (PostgreSQL via HTTP)
    - RabbitMQ (message broker)

    Use this for Kubernetes readiness probe.

    Returns:
        Health status with dependency checks

    Raises:
        HTTPException: 503 if any dependency is unhealthy
    """
    checks = {}
    all_healthy = True

    # Check data service
    try:
        await data_client.health_check()
        checks["data_service"] = "healthy"
    except Exception as e:
        logger.error(f"Data service health check failed: {e}")
        checks["data_service"] = "unhealthy"
        all_healthy = False

    # Check RabbitMQ
    try:
        is_connected = await check_rabbitmq_connection()
        checks["rabbitmq"] = "healthy" if is_connected else "unhealthy"
        if not is_connected:
            all_healthy = False
    except Exception as e:
        logger.error(f"RabbitMQ health check failed: {e}")
        checks["rabbitmq"] = "unhealthy"
        all_healthy = False

    status_code = 200 if all_healthy else 503

    return HealthResponse(
        status="healthy" if all_healthy else "unhealthy",
        version="1.0.0",
        checks=checks,
    )
```

[... Continue with HTTP client, RabbitMQ publisher/consumer, tests ...]

---

#### Task 2.2: Add Anti-Patterns to Documentation

**Status:** ⏸️ Not Started
**Priority:** 🟠 HIGH
**Estimated Time:** 8 hours
**Owner:** TBD

**Objective:**
Document 4 missing anti-patterns related to DRY/KISS/YAGNI violations.

**Files to Create:**
1. `docs/atomic/architecture/anti-patterns/copy-paste-programming.md`
2. `docs/atomic/architecture/anti-patterns/god-object.md`
3. `docs/atomic/architecture/anti-patterns/speculative-generality.md`
4. `docs/atomic/architecture/anti-patterns/premature-infrastructure.md`

**Files to Update:**
- `docs/INDEX.md` - Add new anti-patterns to quick reference
- `docs/atomic/testing/quality-assurance/code-review-checklist.md` - Reference new anti-patterns

**Acceptance Criteria:**
- [ ] Each anti-pattern follows TEMPLATE.md structure
- [ ] Includes problem, symptom, impact, WRONG example, WHY section, CORRECT solution
- [ ] Includes monitoring commands (grep, radon, cloc, etc.)
- [ ] Links to related anti-patterns and architecture docs
- [ ] Added to INDEX.md with priority classification
- [ ] Reviewed by 2+ maintainers

**Implementation Details:**

*copy-paste-programming.md Structure:*

```markdown
# Anti-Pattern: Copy-Paste Programming

## Problem

Code is duplicated across multiple files instead of being extracted to shared utilities or base classes.

## Symptom

- Same validation logic appears in 5 different endpoints
- Multiple services have identical logger configuration code
- Bug fix requires changing N files (risk of inconsistency)
- Code duplication percentage > 10%

## Impact

**Technical:**
- Bug fixes require changing multiple files
- Inconsistent implementations (forgot to update one file)
- Higher maintenance burden
- Larger codebase

**Business:**
- Slower feature development (change N places)
- More bugs (missed updates)
- Higher technical debt

## Example (WRONG)

```python
# services/auth_api/src/api/v1/users.py
@router.post("/users")
async def create_user(data: UserCreate):
    # Duplicated validation
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.email):
        raise HTTPException(400, "Invalid email")
    ...

# services/profile_api/src/api/v1/profiles.py
@router.put("/profiles")
async def update_profile(data: ProfileUpdate):
    # DUPLICATED: Same email validation
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.email):
        raise HTTPException(400, "Invalid email")
    ...

# services/notification_api/src/api/v1/subscriptions.py
@router.post("/subscriptions")
async def subscribe(data: SubscriptionCreate):
    # DUPLICATED AGAIN: Third copy of same validation
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.email):
        raise HTTPException(400, "Invalid email")
    ...
```

## Why This Matters

- **Single Source of Truth:** DRY principle violated
- **Maintenance Nightmare:** Email regex bug requires fixing 3+ files
- **Inconsistency Risk:** Developer updates 2 files, forgets third → inconsistent behavior
- **Testing Burden:** Must test same logic in 3+ test files

## Solution (CORRECT)

**Extract to shared/utils/:**

```python
# shared/utils/validators.py
def is_valid_email(email: str) -> bool:
    """Validate email address format."""
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

# services/auth_api/src/api/v1/users.py
from shared.utils.validators import is_valid_email

@router.post("/users")
async def create_user(data: UserCreate):
    if not is_valid_email(data.email):
        raise ValidationError("Invalid email")
    ...

# services/profile_api/src/api/v1/profiles.py
from shared.utils.validators import is_valid_email

@router.put("/profiles")
async def update_profile(data: ProfileUpdate):
    if not is_valid_email(data.email):
        raise ValidationError("Invalid email")
    ...

# services/notification_api/src/api/v1/subscriptions.py
from shared.utils.validators import is_valid_email

@router.post("/subscriptions")
async def subscribe(data: SubscriptionCreate):
    if not is_valid_email(data.email):
        raise ValidationError("Invalid email")
    ...
```

**Benefits:**
- Single source of truth for email validation
- Bug fix in one place → automatic fix everywhere
- Consistent behavior guaranteed
- Test once in shared/utils/test_validators.py

## Architecture Rule

**Rule:** Extract shared code to `shared/utils/` when:
1. Same logic appears in 2+ places (Rule of Three)
2. Logic is pure (no business context)
3. Logic is stable (won't change per service)

**Examples of what goes in shared/utils/:**
- Validators (email, phone, UUID)
- Logging configuration
- Pagination helpers
- Exception classes
- Request ID management

**Examples of what stays in services:**
- Business logic (user registration flow)
- Domain-specific validation (e.g., "premium users can have 10 profiles")
- Service-specific configuration

## Monitoring

**Detect code duplication:**

```bash
# Install jscpd
npm install -g jscpd

# Scan for duplicates
jscpd src/ --threshold 10 --reporters "console,html" --output "./report"

# Open HTML report
open report/jscpd-report.html
```

**Detect similar files:**

```bash
# Using cloc
cloc --by-file --csv src/ | awk -F',' '$5 > 80 {print $2, "("$5"% similar)"}'
```

**Find duplicated imports (common symptom):**

```bash
# If 5 files import same things, might indicate duplication
grep -r "from shared.utils import" src/ | sort | uniq -c | sort -rn
```

## Related Anti-Patterns

- [Speculative Generality](speculative-generality.md) - Opposite extreme (over-abstraction)
- [HTTP Client Proliferation](../integrations/http/anti-patterns/client-proliferation.md) - Specific case of this pattern
- [Connection Pool Misuse](../integrations/redis/anti-patterns/connection-pool-misuse.md) - Specific case of this pattern

## Related Principles

- [DRY Principle](../../guides/dry-kiss-yagni-principles.md#dry) - Don't Repeat Yourself
- [HTTP-Only Data Access](../architecture/improved-hybrid-overview.md) - Architectural DRY enforcement
- [Shared Utilities](../../templates/shared/utils/README.md) - Where to put extracted code

---

**Classification:** 🟠 HIGH Priority
**Principle:** DRY (Don't Repeat Yourself)
**Detection:** Automated (jscpd in CI)
```

[... Similar structure for god-object.md, speculative-generality.md, premature-infrastructure.md ...]

---

#### Task 2.3: Add Upgrade Triggers to Maturity Levels

**Status:** ⏸️ Not Started
**Priority:** 🟠 HIGH
**Estimated Time:** 4 hours
**Owner:** TBD

**Objective:**
Document evidence-driven upgrade triggers for maturity levels.

**Files to Update:**
- `docs/reference/maturity-levels.md`

**Acceptance Criteria:**
- [ ] Section "When to Upgrade Levels" added with specific metrics
- [ ] Each upgrade (1→2, 2→3, 3→4) has 3-5 concrete triggers
- [ ] Triggers are measurable (team size, user count, deployment status)
- [ ] Anti-pattern "Premature Infrastructure" linked
- [ ] Examples show both correct and premature upgrades

**Implementation Details:**

*Add new section to maturity-levels.md:*

```markdown
## When to Upgrade Maturity Levels

**IMPORTANT:** Upgrade levels based on **evidence**, not speculation.

### Level 1 → Level 2 (PoC → Development)

Upgrade when you have **evidence** of at least 3 of these:

✅ **Team Growth:**
- Team grows to 3+ developers
- Need coordination across multiple contributors
- Code reviews becoming frequent

✅ **Debugging Complexity:**
- Debugging takes >2 hours due to lack of request IDs
- Need to trace requests across service boundaries
- Support team struggles to correlate logs

✅ **Stakeholder Requirements:**
- Stakeholders request API documentation (Swagger)
- Need to share API contract with frontend/mobile team
- QA team needs structured health checks

✅ **Development Velocity:**
- Developing new features without tests is becoming risky
- Need test coverage to enable refactoring
- Regression bugs appearing frequently

**Example (CORRECT):**
```markdown
Scenario: Started with Level 1 PoC, launched to 5 beta users
Evidence after 2 weeks:
- Team grew from 1 to 4 developers
- Spent 3 hours debugging issue without request IDs
- Frontend team requested Swagger docs

Decision: Upgrade to Level 2 ✅
```

**Example (PREMATURE):**
```markdown
Scenario: Just started project, solo developer
Reasoning: "We might need request IDs later"

Decision: Stay at Level 1 until evidence shows need ✅
Premature upgrade wastes time generating unused infrastructure ❌
```

### Level 2 → Level 3 (Development → Pre-Production)

Upgrade when you have **evidence** of at least 3 of these:

✅ **Production Deployment:**
- Preparing for production launch
- Need HTTPS/TLS for security
- Compliance requires encrypted connections

✅ **Monitoring Requirements:**
- Need to monitor uptime (SLA commitment)
- Business stakeholders request latency metrics
- On-call engineer needs Prometheus alerts

✅ **Load Requirements:**
- Traffic exceeds 100 requests/second
- Need Nginx load balancing across multiple instances
- Single instance hitting resource limits

✅ **Security Audit:**
- Security audit requires HTTPS
- PCI/HIPAA compliance requires TLS
- Penetration test findings require hardening

**Example (CORRECT):**
```markdown
Scenario: Level 2 app in development for 2 months
Evidence:
- Launching to production in 1 week
- CTO requires uptime monitoring (99% SLA)
- Security audit mandated HTTPS

Decision: Upgrade to Level 3 ✅
```

**Example (PREMATURE - Anti-Pattern):**
```markdown
Scenario: Still in PoC phase, 0 users
Reasoning: "Let's set up monitoring from the start"

Decision: Stay at Level 1 or 2 until production launch ✅
Level 3 infrastructure (Nginx, Prometheus, SSL) adds 10+ minutes
to generation time and complexity. Wait for evidence. ❌

See: [Premature Infrastructure anti-pattern](../atomic/architecture/anti-patterns/premature-infrastructure.md)
```

### Level 3 → Level 4 (Pre-Production → Production)

Upgrade when you have **evidence** of at least 4 of these:

✅ **Scale:**
- Daily active users > 1,000
- Request rate > 1,000 requests/second
- Multiple regions or availability zones needed

✅ **Compliance:**
- GDPR/HIPAA requires audit logging (ELK)
- Need to track "who did what when" for regulatory compliance
- Legal team requires log retention for N years

✅ **Team Maturity:**
- 10+ developers across multiple teams
- Need staging + production environments
- CI/CD required for frequent deployments

✅ **Observability:**
- Need distributed tracing (Jaeger) for debugging
- Request spans cross 5+ microservices
- Support team requires detailed trace analysis

✅ **Business Critical:**
- Downtime costs > $1,000/hour
- SLA commitment 99.9%+ uptime
- On-call rotation with PagerDuty

**Example (CORRECT):**
```markdown
Scenario: Level 3 app running in production for 6 months
Evidence:
- 5,000 DAU (daily active users)
- GDPR compliance audit requires ELK
- 15 developers, need CI/CD
- Request tracing across 6 microservices is difficult

Decision: Upgrade to Level 4 ✅
```

**Example (TOO EARLY):**
```markdown
Scenario: Level 3 app, launched 2 weeks ago, 50 users
Reasoning: "We plan to scale to 10,000 users"

Decision: Wait for actual scale ✅
Level 4 infrastructure (ELK, Jaeger, multi-env CI/CD) is complex.
Adds 15+ minutes to generation, significant operational overhead.
Upgrade when evidence shows need (actual scale, compliance requirement). ❌
```

---

## Anti-Pattern: Premature Infrastructure

**Problem:** Generating Level 4 infrastructure for Level 1 use case

**Symptom:**
- PoC project with Kubernetes, service mesh, distributed tracing
- Solo developer project with ELK stack, Prometheus, Grafana
- MVP with CI/CD for 5 environments
- 30-minute project generation time for 0 users

**Impact:**
- Slow iteration (long generation time)
- High operational complexity
- Wasted time configuring unused infrastructure
- Cognitive overload for developers

**Solution:**
- Start at Level 1 (PoC) unless evidence shows higher level needed
- Upgrade incrementally based on metrics
- See "When to Upgrade Levels" section above

See full anti-pattern: [Premature Infrastructure](../atomic/architecture/anti-patterns/premature-infrastructure.md)
```

---

### Phase 3: Medium Priority Improvements (P2)

**Estimated Effort:** 16-20 hours
**Target Completion:** Week 4

---

#### Task 3.1: Enhance Stage 1 with Feature Necessity Validation

**Status:** ⏸️ Not Started
**Priority:** 🟡 MEDIUM
**Estimated Time:** 4 hours
**Owner:** TBD

**Objective:**
Add feature prioritization and necessity challenge to Stage 1 (Prompt Validation).

**Files to Update:**
- `docs/guides/ai-code-generation-master-workflow.md`

**Acceptance Criteria:**
- [ ] Stage 1 includes "Feature Necessity Challenge" step
- [ ] AI must ask "Which features are absolutely required for MVP?"
- [ ] Applies MoSCoW prioritization (Must/Should/Could/Won't)
- [ ] Blocks Stage 2 until features prioritized
- [ ] Documents evidence/justification for each "Must Have" feature

**Implementation Details:**

[Continue with detailed implementation...]

---

#### Task 3.2: Create Consolidated DRY/KISS/YAGNI Checklist

[Continue with details...]

---

#### Task 3.3: Create Interactive Maturity Level Selector Script

[Continue with details...]

---

#### Task 3.4: Implement Anti-Pattern Detector Script

[Continue with details...]

---

## Testing and Validation

### Test Plan

**Phase 1 Testing:**
1. Generate project at Level 1 with new templates
2. Verify shared/utils/ are used (no duplication)
3. Run CI pipeline, verify quality gates pass
4. Measure code duplication (<10%)
5. Verify all functions McCabe < 10

**Phase 2 Testing:**
1. Generate business API project, verify all 8 files present
2. Test middleware: request ID injection, exception handling
3. Verify health checks work with mocked dependencies
4. Review anti-pattern docs with 3+ contributors

**Phase 3 Testing:**
1. Test Stage 1 feature prioritization with sample prompts
2. Validate consolidated checklist completeness
3. Run maturity level selector script with various inputs

### Success Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Code Duplication | ~25% | <10% | jscpd report |
| Avg Function Complexity | McCabe 12 | McCabe <10 | radon cc |
| Template Completion | 40% | 100% | templates/README.md |
| Principle Documentation | 0 guides | 3 guides | docs/guides/ |
| Anti-Patterns Documented | 6 | 10 | docs/INDEX.md |
| CI Quality Gates | 2 | 7 | .github/workflows/ci.yml |

---

## Rollout Strategy

### Phase 1: Critical Foundation (Week 1-2)

**Deliverables:**
- DRY/KISS/YAGNI principles guide
- Shared utilities template (100%)
- Data service template (100%)
- CI quality gates

**Rollout:**
1. Merge improvements to `develop` branch
2. Generate 2-3 test projects, validate templates
3. Update CHANGELOG.md with breaking changes (if any)
4. Merge to `main`
5. Tag release: `v0.2.0-principles-enforcement`

**Communication:**
- Announcement in framework repository README
- Migration guide for existing projects

### Phase 2: Enhanced Templates & Docs (Week 3)

**Deliverables:**
- Business API template (100%)
- 4 new anti-patterns
- Maturity level upgrade triggers

**Rollout:**
1. Merge to `develop`
2. Generate 5 test projects (different maturity levels)
3. Validate anti-pattern docs with code examples
4. Merge to `main`
5. Tag release: `v0.3.0-complete-templates`

### Phase 3: Workflow & Tooling (Week 4)

**Deliverables:**
- Enhanced Stage 1 workflow
- Consolidated checklist
- Helper scripts

**Rollout:**
1. Test new Stage 1 with 10+ sample prompts
2. Validate scripts work across platforms
3. Merge to `develop`, then `main`
4. Tag release: `v0.4.0-enhanced-workflow`

---

## Risks and Mitigations

### Risk 1: Breaking Changes to Existing Templates

**Probability:** MEDIUM
**Impact:** HIGH

**Mitigation:**
- Maintain backward compatibility where possible
- Provide migration guide for breaking changes
- Version templates (v1, v2) if necessary
- Test with existing projects before release

### Risk 2: CI Checks Too Strict

**Probability:** MEDIUM
**Impact:** MEDIUM

**Symptom:** Legitimate code fails CI (false positives)

**Mitigation:**
- Start with warning-only mode for first 2 weeks
- Collect feedback, adjust thresholds
- Allow configuration override in .ci-config.yml
- Document how to disable specific checks

### Risk 3: Incomplete Template Testing

**Probability:** LOW
**Impact:** HIGH

**Symptom:** Generated projects fail at runtime

**Mitigation:**
- Generate 10+ test projects per template
- Run full test suite on each generated project
- Deploy to test environment, verify functionality
- Automated template validation in CI

### Risk 4: Documentation Overload

**Probability:** LOW
**Impact:** MEDIUM

**Symptom:** Contributors overwhelmed by documentation volume

**Mitigation:**
- Create clear navigation in INDEX.md
- Add "Quick Start" sections to long docs
- Use examples liberally
- Create video walkthroughs (optional)

---

## Timeline

```
Week 1:
├── Task 1.1: DRY/KISS/YAGNI principles guide (8h)
├── Task 1.2: Shared utilities template (12h)
└── Task 1.3: Data service template - Part 1 (16h)

Week 2:
├── Task 1.3: Data service template - Part 2 (complete)
├── Task 1.4: CI quality gates (4h)
└── Phase 1 testing & rollout (8h)

Week 3:
├── Task 2.1: Complete business API template (8h)
├── Task 2.2: Add anti-patterns (8h)
├── Task 2.3: Maturity level upgrade triggers (4h)
└── Phase 2 testing & rollout (4h)

Week 4:
├── Task 3.1: Feature necessity validation (4h)
├── Task 3.2: Consolidated checklist (3h)
├── Task 3.3: Maturity level selector (4h)
├── Task 3.4: Anti-pattern detector (5h)
└── Phase 3 testing & rollout (4h)
```

**Total Estimated Effort:** 80-120 hours (2-3 weeks for 2-person team)

---

## Status Tracking

Use this section to track progress:

### Phase 1 Status ✅ COMPLETED (2025-11-07)

- [x] Task 1.1: DRY/KISS/YAGNI principles guide (commit: cb8bbcf)
- [x] Task 1.2: Shared utilities template (commit: 4ed25a5)
- [x] Task 1.3: Data service template (PostgreSQL) (commit: d7f017c)
- [x] Task 1.4: CI quality gates (commit: c474d19)

**Quality Gates Test Results:**
- Code Duplication: 0% (threshold: <10%) ✅
- Cyclomatic Complexity: Average A (1.79) ✅
- Maintainability Index: All files Grade B or better ✅
- File Size: All files <500 lines ✅
- Dependencies: 11-27 (thresholds: 30-50) ✅

**Deliverables:**
- 38 new files created
- 3,500+ lines of documentation and code
- CHANGELOG.md updated
- All tests passed

### Phase 2 Status

- [ ] Task 2.1: Complete business API template
- [ ] Task 2.2: Add anti-patterns
- [ ] Task 2.3: Maturity level upgrade triggers

### Phase 3 Status

- [ ] Task 3.1: Feature necessity validation
- [ ] Task 3.2: Consolidated checklist
- [ ] Task 3.3: Maturity level selector
- [ ] Task 3.4: Anti-pattern detector

---

## Contributors

| Name | Role | Tasks |
|------|------|-------|
| TBD | Lead | Overall coordination, Phase 1 |
| TBD | Developer | Templates (Phase 1-2) |
| TBD | Documentation | Docs (Phase 2) |
| TBD | DevOps | CI/CD (Phase 1) |

---

## References

- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - Framework architecture
- [Maturity Levels](../reference/maturity-levels.md) - Current maturity level documentation
- [Agent Workflow](../guides/ai-code-generation-master-workflow.md) - AI agent workflow
- [Quality Standards](../atomic/architecture/quality-standards.md) - Quality requirements

---

**Document Version:** 1.1
**Last Updated:** 2025-11-07
**Status:** Phase 1 Complete ✅ | Phase 2 & 3 Pending
