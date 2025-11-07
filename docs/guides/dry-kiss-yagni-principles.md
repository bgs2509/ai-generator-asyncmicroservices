# DRY, KISS, YAGNI Principles

**Purpose:** Educational guide linking software engineering principles to framework architecture

**Audience:** AI code generation agents, developers, architects

**Last Updated:** 2025-01-07

---

## Table of Contents

1. [DRY (Don't Repeat Yourself)](#1-dry-dont-repeat-yourself)
2. [KISS (Keep It Simple, Stupid)](#2-kiss-keep-it-simple-stupid)
3. [YAGNI (You Aren't Gonna Need It)](#3-yagni-you-arent-gonna-need-it)
4. [How Framework Enforces Principles](#4-how-framework-enforces-principles)
5. [Automated Detection Tools](#5-automated-detection-tools)
6. [Related Documents](#6-related-documents)

---

## 1. DRY (Don't Repeat Yourself)

### Definition

**Every piece of knowledge must have a single, unambiguous representation in the system.**

The DRY principle states that duplication of code, logic, or data structures leads to maintenance nightmares. When the same knowledge exists in multiple places, changes must be synchronized across all copies, creating risk of inconsistency.

### How Framework Enforces DRY

#### Architectural Pattern: HTTP-Only Data Access

The framework enforces DRY by requiring all business services to access data via HTTP, creating a **single source of truth** for database operations.

**✅ CORRECT - Single Source of Truth:**

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

**❌ WRONG - Duplicated Database Logic:**

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

- ✅ Single source of truth for database operations
- ✅ Bug fix in `UserRepository.get_by_id` automatically fixes all consumers
- ✅ No possibility of inconsistent query logic across services
- ✅ Easier connection pool management (one pool, not N pools)
- ✅ Clear separation of concerns (data layer vs. business logic)

#### Shared Utilities Pattern

The framework provides `shared/utils/` for commonly duplicated code:

**✅ CORRECT - Use Shared Utilities:**

```python
# shared/utils/validators.py
def is_valid_email(email: str) -> bool:
    """Validate email address format."""
    if not email or len(email) > 254:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# services/auth_api/src/api/v1/users.py
from shared.utils.validators import is_valid_email

@router.post("/users")
async def create_user(data: UserCreate):
    if not is_valid_email(data.email):
        raise ValidationError("Invalid email")
    # ... continue
```

**❌ WRONG - Duplicated Validation:**

```python
# services/auth_api/src/api/v1/users.py
@router.post("/users")
async def create_user(data: UserCreate):
    # Duplicated validation logic
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.email):
        raise HTTPException(400, "Invalid email")
    # ...

# services/profile_api/src/api/v1/profiles.py
@router.put("/profiles")
async def update_profile(data: ProfileUpdate):
    # DUPLICATED: Same email validation
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.email):
        raise HTTPException(400, "Invalid email")
    # ...

# services/notification_api/src/api/v1/subscriptions.py
@router.post("/subscriptions")
async def subscribe(data: SubscriptionCreate):
    # DUPLICATED AGAIN: Third copy of same validation
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.email):
        raise HTTPException(400, "Invalid email")
    # ...
```

**Impact of Violation:**

- ❌ Bug in email regex requires fixing 3+ files
- ❌ Developer updates 2 files, forgets third → inconsistent behavior
- ❌ Must test same logic in 3+ test files
- ❌ ~500 lines of duplicated code per 5-service project

### Rule of Three

Extract shared code to `shared/utils/` when:

1. **Same logic appears in 2+ places** (Rule of Three)
2. **Logic is pure** (no business context, no external dependencies)
3. **Logic is stable** (won't change per service)

**Examples of what goes in shared/utils/:**

- ✅ Validators (email, phone, UUID, URL)
- ✅ Logging configuration
- ✅ Pagination helpers (offset, cursor)
- ✅ Exception base classes
- ✅ Request ID management

**Examples of what stays in services:**

- ❌ Business logic (user registration flow)
- ❌ Domain-specific validation (e.g., "premium users can have 10 profiles")
- ❌ Service-specific configuration

### Automated Detection

**Check code duplication percentage:**

```bash
# Install jscpd
npm install -g jscpd

# Scan for duplicates (fail if >10%)
jscpd src/ --threshold 10 --exitCode 1

# Detailed HTML report
jscpd src/ --format html --output ./jscpd-report
open jscpd-report/jscpd-report.html
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

---

## 2. KISS (Keep It Simple, Stupid)

### Definition

**Most systems work best if they are kept simple rather than made complicated.**

The KISS principle advocates for simplicity in design and implementation. Complex solutions are harder to understand, maintain, test, and debug. Simple solutions are easier to reason about and less prone to bugs.

### How Framework Enforces KISS

#### Maturity Levels - Incremental Complexity

The framework enforces KISS through **4 maturity levels** that add complexity only when needed:

**Level 1 (PoC):** Minimal infrastructure
- FastAPI app with basic routes
- No logging, no health checks, no middleware
- ~50 lines of code, 2-minute setup

**Level 2 (Development):** Essential development tools
- + Request ID tracking
- + Swagger documentation
- + Health checks
- + Basic tests

**Level 3 (Pre-Production):** Production readiness
- + HTTPS/TLS
- + Nginx load balancer
- + Prometheus metrics
- + Structured logging

**Level 4 (Production):** Enterprise scale
- + ELK stack (centralized logs)
- + Jaeger distributed tracing
- + Multi-environment CI/CD
- + Auto-scaling

**✅ CORRECT - Start Simple, Upgrade When Needed:**

```markdown
Scenario: New project, 1 developer, 0 users

Decision: Start at Level 1 ✅
- 50 lines of code
- 2-minute generation time
- Easy to understand and modify

After 2 weeks: Team grows to 4, need debugging tools
Decision: Upgrade to Level 2 ✅
- Add request ID tracking for debugging
- Add Swagger for team coordination
```

**❌ WRONG - Premature Complexity:**

```markdown
Scenario: New project, 1 developer, 0 users

Decision: Start at Level 4 ❌
- 2000+ lines of generated code
- Kubernetes, service mesh, distributed tracing
- 30-minute generation time
- Overwhelming for solo developer
- 95% of infrastructure unused

Result:
- Slow iteration (complex setup)
- Cognitive overload (too many moving parts)
- Time wasted on configuration instead of features
```

**Why Maturity Levels Enforce KISS:**

- ✅ Start simple, add complexity incrementally
- ✅ Only add infrastructure when evidence shows need
- ✅ Avoid premature optimization
- ✅ Reduce cognitive load for developers
- ✅ Faster time to market

See: [Maturity Levels Documentation](../reference/maturity-levels.md)

#### Cyclomatic Complexity Limits

The framework enforces KISS by limiting function complexity:

**Rule:** McCabe cyclomatic complexity < 10 for all functions

**✅ CORRECT - Simple Function:**

```python
async def get_user(self, user_id: int) -> User:
    """Get user by ID.

    Complexity: 2 (1 base + 1 if statement)
    """
    user = await self._repository.get_by_id(user_id)

    if not user:
        raise NotFoundError(f"User {user_id} not found")

    return user
```

**❌ WRONG - Complex Function:**

```python
async def process_payment(self, order_id: int, payment_data: dict) -> Payment:
    """Process payment with multiple conditional paths.

    Complexity: 15 (TOO HIGH - VIOLATES KISS)
    """
    order = await self._get_order(order_id)

    # Nested conditionals increase complexity
    if order.status == "pending":
        if payment_data["method"] == "credit_card":
            if payment_data["amount"] > 1000:
                if not payment_data.get("cvv"):
                    raise ValidationError("CVV required for large amounts")
                result = await self._charge_card(payment_data)
            else:
                result = await self._charge_card(payment_data)
        elif payment_data["method"] == "paypal":
            if payment_data["amount"] > 500:
                result = await self._charge_paypal_express(payment_data)
            else:
                result = await self._charge_paypal(payment_data)
        elif payment_data["method"] == "bank_transfer":
            if self._is_business_customer(order.customer_id):
                result = await self._initiate_wire_transfer(payment_data)
            else:
                raise ValidationError("Bank transfer only for business customers")
        else:
            raise ValidationError(f"Unsupported payment method: {payment_data['method']}")
    else:
        raise ValidationError(f"Order {order_id} is not pending")

    return result
```

**Refactoring Strategy - Extract Methods:**

```python
async def process_payment(self, order_id: int, payment_data: dict) -> Payment:
    """Process payment (refactored for simplicity).

    Complexity: 3 (simple and readable)
    """
    order = await self._validate_order(order_id)
    payment_handler = self._get_payment_handler(payment_data["method"])
    result = await payment_handler.charge(payment_data, order)
    return result

# Extracted methods (each with complexity < 10)
async def _validate_order(self, order_id: int) -> Order:
    """Validate order is ready for payment."""
    order = await self._get_order(order_id)
    if order.status != "pending":
        raise ValidationError(f"Order {order_id} is not pending")
    return order

def _get_payment_handler(self, method: str) -> PaymentHandler:
    """Get payment handler for method (Strategy Pattern)."""
    handlers = {
        "credit_card": CreditCardHandler(self._payment_gateway),
        "paypal": PayPalHandler(self._paypal_client),
        "bank_transfer": BankTransferHandler(self._bank_api),
    }

    if method not in handlers:
        raise ValidationError(f"Unsupported payment method: {method}")

    return handlers[method]
```

**Benefits of Refactoring:**

- ✅ Complexity reduced from 15 to 3
- ✅ Each method has single responsibility
- ✅ Easy to test (test each handler independently)
- ✅ Easy to add new payment methods (extend handlers dict)
- ✅ Readable and maintainable

### Automated Detection

**Check cyclomatic complexity:**

```bash
# Install radon
pip install radon

# Check complexity (fail if any function has complexity >= 10)
radon cc src/ --min B --total-average --show-complexity

# Output example:
# src/services/payment_service.py
#     M 156:4 PaymentService.process_payment - B (6)  ✅ PASS
#     M 180:4 PaymentService._validate_order - A (2)  ✅ PASS
```

**Check maintainability index:**

```bash
# MI (Maintainability Index) considers complexity, LOC, comments
radon mi src/ --min B --show

# Grading scale:
# A: 20-100 (excellent)
# B: 10-19 (good)
# C: 0-9 (needs refactoring)
```

**Check file sizes:**

```bash
# Files >500 lines violate KISS
find src/ -name "*.py" -type f -exec wc -l {} \; | awk '$1 > 500 {print $2, "("$1" lines)"}'

# Example output:
# src/services/god_object_service.py (842 lines)  ❌ VIOLATES KISS
```

---

## 3. YAGNI (You Aren't Gonna Need It)

### Definition

**Don't add functionality until it is necessary.**

The YAGNI principle states that developers should not add features, infrastructure, or abstraction layers based on speculation about future needs. Only implement what is required for current requirements.

### How Framework Enforces YAGNI

#### Evidence-Driven Maturity Upgrades

The framework enforces YAGNI by requiring **evidence** before upgrading complexity:

**✅ CORRECT - Evidence-Based Upgrade:**

```markdown
Current State: Level 2 app, 50 beta users, 2 weeks in production

Evidence for Level 3 upgrade:
1. ✅ Launching to production next week (HTTPS required)
2. ✅ CTO requires 99% uptime SLA (Prometheus monitoring needed)
3. ✅ Security audit mandated TLS encryption
4. ✅ Traffic projection: 500 req/sec (Nginx load balancing needed)

Decision: Upgrade to Level 3 ✅
Justification: All infrastructure has concrete business need
```

**❌ WRONG - Speculative Upgrade:**

```markdown
Current State: Level 1 PoC, 0 users, solo developer

Reasoning: "We MIGHT need monitoring later"
Decision: Generate Level 4 with full observability stack ❌

Result:
- 30-minute generation time
- Prometheus, Grafana, ELK, Jaeger configured
- 95% of infrastructure completely unused
- Time wasted: 4 hours configuring unused systems
- Complexity: Overwhelming for solo developer

Correct Decision: Stay at Level 1, upgrade when evidence shows need ✅
```

**When to Upgrade Maturity Levels:**

See: [Maturity Level Upgrade Triggers](../reference/maturity-levels.md#when-to-upgrade-levels)

Key evidence types:
- **Team size:** 1 developer → no coordination tools needed
- **User count:** 0 users → no monitoring needed
- **Deployment status:** Not in production → no HTTPS needed
- **Compliance:** No audit → no ELK needed

#### Feature Necessity Validation

The framework enforces YAGNI through **Stage 1: Feature Prioritization** in the AI workflow:

**✅ CORRECT - Challenge Unnecessary Features:**

```markdown
User Request: "Build authentication service with:
- Email/password login
- OAuth (Google, Facebook, GitHub, Apple, Twitter, LinkedIn)
- 2FA (SMS, TOTP, email, biometric)
- Password reset
- Account recovery via security questions
- Magic link login
- Passkey support
- Session management
- Remember me
- CAPTCHA
- Rate limiting
- Account lockout after failed attempts"

AI Agent (Stage 1 - Feature Necessity Challenge):
"I see 15 features requested. Let's prioritize using MoSCoW method:

MUST HAVE (MVP):
- Email/password login
- Password reset
- Session management

SHOULD HAVE (Phase 2):
- OAuth (Google only for MVP)
- 2FA (TOTP only for MVP)
- Rate limiting

COULD HAVE (Phase 3):
- OAuth (additional providers)
- Magic link login
- Remember me

WON'T HAVE (YAGNI - no evidence of need):
- Passkey support (bleeding edge, low adoption)
- Biometric 2FA (requires mobile app)
- Security questions (outdated, insecure)

Recommendation: Start with 3 MUST HAVE features, add others when evidence shows need."
```

**❌ WRONG - Implement Everything Upfront:**

```markdown
Developer: "Implements all 15 features in MVP"

Result:
- Development time: 6 weeks instead of 1 week
- Testing complexity: 3x more test cases
- Bugs: Security question feature has vulnerability (wasted time)
- Usage stats after 3 months:
  - Passkey: 0 users (wasted 40 hours)
  - LinkedIn OAuth: 2 users (wasted 20 hours)
  - Biometric 2FA: 0 users (requires mobile app that doesn't exist)

Total wasted effort: ~120 hours on unused features ❌
```

#### Dependency Minimalism

The framework enforces YAGNI through dependency count limits:

**Rule:**
- Level 1-2: Max 30 dependencies
- Level 3-4: Max 50 dependencies

**✅ CORRECT - Minimal Dependencies:**

```txt
# requirements.txt (Level 2 project - 12 dependencies)
fastapi==0.115.0
uvicorn==0.31.0
pydantic==2.9.2
httpx==0.27.2
python-multipart==0.0.12
python-jose[cryptography]==3.3.0

# Development
pytest==8.3.3
pytest-asyncio==0.24.0
pytest-cov==5.0.0
httpx==0.27.2
ruff==0.6.9
mypy==1.11.2
```

**❌ WRONG - Dependency Bloat:**

```txt
# requirements.txt (Level 1 PoC - 45 dependencies! YAGNI VIOLATION)
fastapi==0.115.0
uvicorn==0.31.0
pydantic==2.9.2

# "We MIGHT need these later" ❌
celery==5.4.0           # No background tasks in PoC
redis==5.1.1            # No caching requirement
prometheus-client==0.21.0  # No monitoring in PoC
opentelemetry-api==1.27.0  # No tracing in PoC
sentry-sdk==2.15.0      # No error tracking in PoC
elasticsearch==8.15.1   # No search feature in PoC
pillow==10.4.0          # No image processing in requirements
pandas==2.2.3           # No data analysis in requirements
numpy==2.1.2            # No numerical computation in requirements

# ... 36 more unused dependencies

Problems:
- Installation time: 5 minutes instead of 30 seconds
- Docker image size: 2GB instead of 200MB
- Security: 45 packages = 45 potential vulnerabilities
- Maintenance: Must update 45 packages
- Confusion: Developers don't know which are actually used
```

### Automated Detection

**Check dependency count:**

```bash
# Count non-comment, non-empty lines
grep -v '^#' requirements.txt | grep -v '^$' | wc -l

# Expected output:
# Level 1-2: <30 ✅
# Level 3-4: <50 ✅
```

**Find unused dependencies:**

```bash
# Install pip-check
pip install pip-check

# Check for unused dependencies
pip-check --verbose

# Remove unused dependencies
pip install pip-autoremove
pip-autoremove <package-name> -y
```

**Check for overengineered abstractions:**

```bash
# Find abstract base classes (potential over-abstraction)
grep -r "from abc import ABC" src/

# Find classes with only one implementation (YAGNI violation)
# If AbstractPaymentProvider has only CreditCardProvider → unnecessary abstraction
```

---

## 4. How Framework Enforces Principles

### Architectural Enforcement

| Principle | Architectural Mechanism | Enforcement Method |
|-----------|------------------------|-------------------|
| **DRY** | HTTP-only data access | Business services MUST call data service via HTTP (no direct DB access) |
| **DRY** | Shared utilities | Reusable validators, logger, pagination in `shared/utils/` |
| **KISS** | Maturity levels | Start simple (Level 1), add complexity incrementally based on evidence |
| **KISS** | Complexity limits | McCabe complexity <10, file size <500 lines |
| **YAGNI** | Evidence-based upgrades | Require metrics (team size, user count, deployment status) before upgrading |
| **YAGNI** | Feature prioritization | Stage 1 workflow challenges unnecessary features |

### Single Event Loop Ownership

The framework enforces **KISS** by preventing async/await conflicts:

**Rule:** Each service owns ONE event loop

**✅ CORRECT:**

```python
# Business Service: Uses HTTP clients (not direct async database)
async def get_user_profile(user_id: int) -> Profile:
    # HTTP call (no event loop conflict)
    user_data = await data_client.get(f"/users/{user_id}")
    return Profile(**user_data)
```

**❌ WRONG (Old Hybrid Approach):**

```python
# Business Service: Direct database access creates event loop conflicts
async def get_user_profile(user_id: int) -> Profile:
    # Service has Telegram Bot event loop
    # Database access tries to create second event loop
    # Result: RuntimeError: Event loop is already running
    user = await db.query(User).filter(User.id == user_id).first()  ❌
```

See: [Improved Hybrid Approach](../atomic/architecture/improved-hybrid-overview.md)

### Template Completeness

The framework enforces **DRY** through complete templates:

| Template Component | Status | DRY Enforcement |
|-------------------|--------|-----------------|
| `shared/utils/logger.py` | ✅ 100% | Eliminates logging setup duplication |
| `shared/utils/validators.py` | ✅ 100% | Eliminates validation duplication |
| `shared/utils/pagination.py` | ✅ 100% | Eliminates pagination logic duplication |
| `template_data_postgres_api/` | ✅ 100% | Single source of truth for PostgreSQL access |
| `template_business_api/` | ✅ 100% | HTTP client patterns, middleware |

---

## 5. Automated Detection Tools

### CI Pipeline Quality Gates

The framework enforces all three principles through **automated CI checks**:

#### DRY Enforcement

```yaml
# .github/workflows/ci.yml
check-duplication:
  runs-on: ubuntu-latest
  steps:
    - name: Check code duplication
      run: |
        npm install -g jscpd
        jscpd src/ --threshold 10 --exitCode 1 || {
          echo "❌ DRY VIOLATION: Code duplication >10%"
          echo "Extract shared code to shared/utils/"
          exit 1
        }
```

#### KISS Enforcement

```yaml
check-complexity:
  runs-on: ubuntu-latest
  steps:
    - name: Check cyclomatic complexity
      run: |
        pip install radon
        radon cc src/ --min B || {
          echo "❌ KISS VIOLATION: Function complexity >= 10"
          echo "Refactor complex functions into smaller ones"
          exit 1
        }

    - name: Check file sizes
      run: |
        large_files=$(find src/ -name "*.py" -exec wc -l {} \; | awk '$1>500')
        if [ -n "$large_files" ]; then
          echo "❌ KISS VIOLATION: Files >500 lines"
          echo "$large_files"
          exit 1
        fi
```

#### YAGNI Enforcement

```yaml
check-dependencies:
  runs-on: ubuntu-latest
  steps:
    - name: Check dependency count
      run: |
        dep_count=$(grep -v '^#' requirements.txt | grep -v '^$' | wc -l)
        threshold=30  # Level 1-2 threshold

        if [ $dep_count -gt $threshold ]; then
          echo "❌ YAGNI VIOLATION: Too many dependencies ($dep_count >$threshold)"
          echo "Remove unused dependencies or justify each one"
          exit 1
        fi
```

### Local Development Tools

**Pre-commit checks:**

```bash
# Install tools
npm install -g jscpd
pip install radon pip-check

# Create pre-commit script
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "Running quality gates..."

# DRY check
jscpd src/ --threshold 10 || exit 1

# KISS checks
radon cc src/ --min B || exit 1
radon mi src/ --min B || exit 1

# YAGNI check
dep_count=$(grep -v '^#' requirements.txt | grep -v '^$' | wc -l)
if [ $dep_count -gt 30 ]; then
  echo "❌ Too many dependencies: $dep_count"
  exit 1
fi

echo "✅ All quality gates passed"
EOF

chmod +x .git/hooks/pre-commit
```

### Monitoring Commands

**DRY Monitoring:**

```bash
# Code duplication report
jscpd src/ --reporters "console,html" --output ./report
open report/jscpd-report.html

# Find similar files
cloc --by-file --csv src/ | awk -F',' '$5 > 80 {print $2, "("$5"%)"}'

# Find duplicated imports (symptom of duplication)
grep -r "^from\|^import" src/ | sort | uniq -c | sort -rn | head -20
```

**KISS Monitoring:**

```bash
# Complexity metrics
radon cc src/ --show-complexity --total-average
radon mi src/ --show

# Largest files (potential god objects)
find src/ -name "*.py" -exec wc -l {} \; | sort -rn | head -10

# Most complex functions
radon cc src/ --json | jq '.[] | .[] | select(.complexity > 5) | {name, complexity}'
```

**YAGNI Monitoring:**

```bash
# Dependency analysis
pip list --format=freeze | wc -l  # Total installed
grep -v '^#' requirements.txt | grep -v '^$' | wc -l  # Required

# Find unused dependencies
pip install pipreqs
pipreqs . --print  # Shows actually imported packages
diff requirements.txt requirements_actual.txt  # Compare

# Vulnerability scan (more deps = more risk)
pip install safety
safety check
```

---

## 6. Related Documents

### Architecture Documentation

- [Improved Hybrid Approach](../atomic/architecture/improved-hybrid-overview.md) - How HTTP-only pattern enforces DRY
- [Architecture Overview](../atomic/architecture/architecture-overview.md) - Overall system design
- [Maturity Levels](../reference/maturity-levels.md) - Incremental complexity (KISS + YAGNI)
- [Quality Standards](../atomic/architecture/quality-standards.md) - Code quality requirements

### Anti-Patterns

- [Copy-Paste Programming](../atomic/architecture/anti-patterns/copy-paste-programming.md) - DRY violations
- [God Object](../atomic/architecture/anti-patterns/god-object.md) - KISS violations
- [Speculative Generality](../atomic/architecture/anti-patterns/speculative-generality.md) - YAGNI violations
- [Premature Infrastructure](../atomic/architecture/anti-patterns/premature-infrastructure.md) - KISS + YAGNI violations

### Implementation Guides

- [Shared Utilities README](../../templates/shared/utils/README.md) - Reusable components (DRY)
- [HTTP Client Patterns](../atomic/integrations/http/http-client-patterns.md) - HTTP-only data access (DRY)
- [AI Code Generation Workflow](./ai-code-generation-master-workflow.md) - Feature prioritization (YAGNI)

### Quality Assurance

- [Code Review Checklist](../atomic/testing/quality-assurance/code-review-checklist.md) - Includes DRY/KISS/YAGNI checks
- [Automated Quality Gates](../quality/automated-quality-gates.md) - CI enforcement
- [Testing Strategy](../atomic/testing/testing-strategy.md) - How to test simple code

---

## Quick Reference Card

### DRY Checklist

- [ ] No duplicated database queries across services (use data service via HTTP)
- [ ] No duplicated validators (use `shared/utils/validators.py`)
- [ ] No duplicated logging setup (use `shared/utils/logger.py`)
- [ ] No duplicated pagination logic (use `shared/utils/pagination.py`)
- [ ] Code duplication <10% (verified by `jscpd`)

### KISS Checklist

- [ ] All functions have McCabe complexity <10 (verified by `radon cc`)
- [ ] All files <500 lines (verified by `find` + `wc`)
- [ ] Maturity level matches project phase (PoC → Level 1, Production → Level 3-4)
- [ ] No premature optimization or over-engineering
- [ ] Clear, readable code with minimal nesting

### YAGNI Checklist

- [ ] All features have documented business justification
- [ ] Maturity level upgrade based on evidence (team size, users, deployment status)
- [ ] Dependency count appropriate for maturity level (<30 for Level 1-2)
- [ ] No unused dependencies (verified by `pip-check`)
- [ ] No speculative abstractions (no interfaces with single implementation)

---

**Document Version:** 1.0
**Last Updated:** 2025-01-07
**Status:** ✅ Complete
**Reviewed By:** Framework Maintainers
