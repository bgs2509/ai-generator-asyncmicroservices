# Automated Quality Gates

**Purpose:** Enforce DRY, KISS, and YAGNI principles through automated CI checks

**Last Updated:** 2025-01-07

---

## Overview

The CI pipeline includes automated quality gates that enforce software engineering principles. These checks run on every push and pull request, ensuring code quality and consistency across the framework.

## Quality Gate Jobs

### 1. check-duplication (DRY Enforcement)

**Tool:** jscpd (JavaScript Copy/Paste Detector)
**Threshold:** 10% duplication max
**Fails if:** Code duplication exceeds threshold

#### What it checks

- Duplicated code blocks across files
- Copy-paste patterns
- Similar code structures

#### How to fix violations

```bash
# Generate duplication report locally
npm install -g jscpd
jscpd services/ shared/ --reporters "console,html" --output "./report"
open report/jscpd-report.html
```

**Common fixes:**

1. **Extract to shared/utils/**
   ```python
   # Before: Duplicated in 3 files
   if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
       raise ValidationError("Invalid email")

   # After: Use shared validator
   from shared.utils.validators import is_valid_email
   if not is_valid_email(email):
       raise ValidationError("Invalid email")
   ```

2. **Create base classes**
   ```python
   # Before: Same CRUD methods in 5 repositories
   class UserRepository:
       async def get_by_id(self, id: int): ...
       async def create(self, **kwargs): ...

   # After: Inherit from BaseRepository
   class UserRepository(BaseRepository[User]):
       # Only add model-specific methods
       async def get_by_email(self, email: str): ...
   ```

3. **Use composition over duplication**
   ```python
   # Before: Same HTTP client setup in every service
   client = httpx.AsyncClient(timeout=30, ...)

   # After: Use shared client factory
   from shared.utils.http_client import create_client
   client = create_client(timeout=30)
   ```

---

### 2. check-complexity (KISS Enforcement)

**Tool:** radon
**Thresholds:**
- McCabe complexity < 10 per function
- Maintainability Index >= 20 (Grade B)
- File size < 500 lines

**Fails if:** Any function/file exceeds thresholds

#### What it checks

**Cyclomatic Complexity** - Number of independent code paths:
```python
# Complexity = 1 (simple)
def get_user(user_id: int) -> User:
    return repository.get(user_id)

# Complexity = 5 (moderate)
def validate_user(user: User) -> bool:
    if not user.email:  # +1
        return False
    if not user.name:  # +1
        return False
    if user.age < 0:  # +1
        return False
    if user.age > 150:  # +1
        return False
    return True

# Complexity = 15 (too high! ❌)
def process_payment(order, payment_data):
    if order.status == "pending":  # +1
        if payment_data["method"] == "card":  # +1
            if payment_data["amount"] > 1000:  # +1
                if not payment_data.get("cvv"):  # +1
                    # ... 11 more nested conditions
```

**Maintainability Index** - Composite metric (0-100):
- A (20-100): Excellent
- B (10-19): Good
- C (0-9): Needs refactoring

**File Size** - Lines of code per file

#### How to fix violations

```bash
# Check complexity locally
pip install radon
radon cc services/ shared/ --show-complexity
radon mi services/ shared/ --show

# Find large files
find services/ shared/ -name "*.py" -exec wc -l {} \; | sort -rn | head -10

# Most complex functions
radon cc services/ shared/ --json | jq '.[] | .[] | select(.complexity > 5) | {name, complexity}'
```

**Common fixes:**

1. **Extract methods (Replace Temp with Query)**
   ```python
   # Before: Complex function (McCabe = 15)
   def process_order(order_id):
       order = get_order(order_id)
       if order.status == "pending":
           if order.items:
               total = 0
               for item in order.items:
                   if item.price > 0:
                       total += item.price * item.quantity
               if total > order.discount:
                   final_total = total - order.discount
               else:
                   final_total = 0
               if final_total > 0:
                   charge_payment(order.payment_method, final_total)
           # ... more nested logic

   # After: Extracted methods (McCabe = 3)
   def process_order(order_id):
       order = get_order(order_id)
       if not can_process_order(order):
           return
       total = calculate_order_total(order)
       charge_payment(order.payment_method, total)

   def can_process_order(order):
       return order.status == "pending" and order.items

   def calculate_order_total(order):
       subtotal = sum(item.price * item.quantity for item in order.items)
       return max(subtotal - order.discount, 0)
   ```

2. **Use early returns (Guard Clauses)**
   ```python
   # Before: Nested conditions (McCabe = 8)
   def validate_user(user):
       if user:
           if user.email:
               if user.name:
                   if user.age >= 0:
                       if user.age <= 150:
                           return True
       return False

   # After: Early returns (McCabe = 4)
   def validate_user(user):
       if not user:
           return False
       if not user.email:
           return False
       if not user.name:
           return False
       if user.age < 0 or user.age > 150:
           return False
       return True
   ```

3. **Apply strategy pattern**
   ```python
   # Before: Large switch/case (McCabe = 12)
   def process_payment(method, data):
       if method == "card":
           if data["type"] == "visa":
               # ... visa logic
           elif data["type"] == "mastercard":
               # ... mastercard logic
       elif method == "paypal":
           # ... paypal logic
       elif method == "bank":
           # ... bank logic
       # ... 8 more payment methods

   # After: Strategy pattern (McCabe = 2)
   def process_payment(method, data):
       handler = get_payment_handler(method)
       return handler.charge(data)

   class VisaHandler:
       def charge(self, data): ...

   class PayPalHandler:
       def charge(self, data): ...
   ```

4. **Split large classes**
   ```python
   # Before: God class (842 lines)
   class UserService:
       # 50+ methods mixing concerns

   # After: Split by responsibility
   class UserAuthService:  # 150 lines
       # Only authentication methods

   class UserProfileService:  # 200 lines
       # Only profile management

   class UserNotificationService:  # 180 lines
       # Only notifications
   ```

---

### 3. check-dependencies (YAGNI Enforcement)

**Tool:** grep + pip-check
**Thresholds:**
- Level 1-2 (Data services): max 30 dependencies
- Level 3-4 (Business services): max 50 dependencies

**Fails if:** Dependency count exceeds threshold

#### What it checks

- Total number of dependencies per service
- Potentially unused dependencies (informational)

#### How to fix violations

```bash
# Check dependencies locally
wc -l < requirements.txt

# Find unused dependencies
pip install pip-check
pip-check --verbose

# Remove unused dependency
pip install pip-autoremove
pip-autoremove <package-name> -y
```

**Common fixes:**

1. **Remove dev dependencies from production**
   ```txt
   # Before: requirements.txt (45 dependencies)
   fastapi==0.115.0
   pytest==8.3.3          # ❌ Should be in requirements-dev.txt
   mypy==1.11.2           # ❌ Should be in requirements-dev.txt
   black==24.10.0         # ❌ Should be in requirements-dev.txt
   ...

   # After: requirements.txt (15 dependencies)
   fastapi==0.115.0
   uvicorn==0.31.0
   sqlalchemy==2.0.35
   ...

   # requirements-dev.txt
   pytest==8.3.3
   mypy==1.11.2
   black==24.10.0
   ```

2. **Use stdlib alternatives**
   ```python
   # Before: Install requests (heavy dependency)
   import requests
   response = requests.get(url)

   # After: Use stdlib urllib (no dependency)
   from urllib.request import urlopen
   response = urlopen(url)

   # Or: Use httpx (already required by framework)
   import httpx
   response = await httpx.get(url)
   ```

3. **Remove dependencies from earlier iterations**
   ```txt
   # Before: Leftover from prototype
   pandas==2.2.3          # ❌ Used in prototype, not production
   numpy==2.1.2           # ❌ Used in prototype, not production
   pillow==10.4.0         # ❌ Image processing not needed
   celery==5.4.0          # ❌ Replaced with AsyncIO workers
   ```

---

## Running Checks Locally

Before pushing, run all checks locally to catch issues early:

```bash
# Install tools
npm install -g jscpd
pip install radon pip-check

# DRY check
jscpd services/ shared/ --threshold 10

# KISS checks
radon cc services/ shared/ --min B
radon mi services/ shared/ --min B
find services/ shared/ -name "*.py" -exec wc -l {} \; | awk '$1>500 {print $0}'

# YAGNI check
for dir in services/*/; do
  echo "$(basename $dir): $(grep -v '^#' $dir/requirements.txt | grep -v '^$' | wc -l) dependencies"
done
```

**Makefile shortcuts** (if available):

```bash
make quality-check      # Run all quality gates
make check-duplication  # DRY only
make check-complexity   # KISS only
make check-dependencies # YAGNI only
```

---

## CI Badge

Add to README.md to show quality gate status:

```markdown
![Quality Gates](https://github.com/your-org/your-repo/actions/workflows/ci.yml/badge.svg)
```

---

## Quality Gate Results

### Success ✅

All checks pass:

```
✅ All CI checks passed successfully!

📋 Quality Gates Summary:
   ✅ Linting & Type Checking
   ✅ Unit Tests
   ✅ Integration Tests
   ✅ Docker Build
   ✅ DRY Check (Code Duplication <10%)
   ✅ KISS Check (Complexity, Maintainability, File Size)
   ✅ YAGNI Check (Dependency Count)
   ✅ Security Scanning

🎉 Ready for deployment!
```

### Failure ❌

Example violation:

```
❌ DRY VIOLATION: Code duplication exceeds 10% threshold

📊 Duplicated code violates the DRY (Don't Repeat Yourself) principle.

💡 Consider extracting shared code to:
   • shared/utils/ for reusable utilities
   • Base classes for common patterns
   • Helper functions in appropriate modules

📖 Learn more: docs/guides/dry-kiss-yagni-principles.md#dry
📁 Detailed report: jscpd-report/jscpd-report.html
```

---

## Thresholds Summary

| Check | Threshold | Rationale |
|-------|-----------|-----------|
| Code Duplication | <10% | Industry standard for maintainable code |
| Cyclomatic Complexity | <10 (McCabe) | Recommended max for testable functions |
| Maintainability Index | >=20 (Grade B) | Good maintainability baseline |
| File Size | <500 lines | Single Responsibility Principle |
| Dependencies (Data) | <30 | Minimal attack surface |
| Dependencies (Business) | <50 | Allow integrations but limit bloat |

---

## Customizing Thresholds

To adjust thresholds for your project:

1. **Fork CI workflow**
   ```bash
   cp templates/ci-cd/.github/workflows/ci.yml .github/workflows/
   ```

2. **Edit thresholds**
   ```yaml
   # DRY threshold
   jscpd services/ shared/ --threshold 15  # Increase to 15%

   # KISS threshold
   radon cc services/ --min C  # Allow grade C (complexity 10-20)

   # YAGNI threshold
   threshold=50  # Increase dependency limit
   ```

3. **Document justification**
   ```markdown
   # CUSTOMIZATION.md
   ## Quality Gate Thresholds

   Modified thresholds:
   - Code duplication: 15% (legacy codebase, reducing gradually)
   - Complexity: Grade C allowed (complex domain logic)
   - Dependencies: 50 for data services (requires ML libraries)
   ```

---

## Related Documentation

- [DRY/KISS/YAGNI Principles](../guides/dry-kiss-yagni-principles.md) - Comprehensive principle guide
- [Code Review Checklist](../atomic/testing/quality-assurance/code-review-checklist.md) - Manual checks
- [Testing Strategy](../atomic/testing/testing-strategy.md) - How to test quality improvements

---

**Version:** 1.0.0
**Last Updated:** 2025-01-07
**Status:** ✅ Active in CI Pipeline
