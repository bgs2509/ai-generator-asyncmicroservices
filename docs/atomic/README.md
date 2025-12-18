# Atomic Documentation Hub

The `docs/atomic` tree provides the canonical, domain-scoped knowledge base for the platform. Each Markdown file focuses on a single responsibility and serves as the definitive reference for its topic.

## 📝 Writing New Atomic Documents

**ALWAYS use the universal template when creating new documentation:**

👉 **[TEMPLATE.md](TEMPLATE.md)** — Universal template for all atomic documents

### Quick Start

```bash
# 1. Copy template to your category
cp docs/atomic/TEMPLATE.md docs/atomic/{category}/{your-topic}.md

# 2. Edit the file and replace placeholders:
#    - {Topic Title} → Your specific topic name
#    - {Category-Specific Sections} → Choose from template guide
#    - {Brief introduction} → Write 1-3 paragraphs
#    - Add code examples, related documents

# 3. Remove reference sections:
#    - Delete "Category-Specific Section Guide" (it's for reference only)
#    - Delete "Validation Checklist" (after checking)

# 4. Validate (optional, if script exists)
python scripts/validate_atomic_docs.py docs/atomic/{category}/{your-topic}.md
```

### Example Workflow

```bash
# Creating a new Redis caching patterns document

# Step 1: Copy template
cp docs/atomic/TEMPLATE.md docs/atomic/integrations/redis/caching-strategies.md

# Step 2: Edit file
# - Title: "Redis Caching Strategies"
# - Introduction: Explain caching patterns for Redis
# - Sections: Configuration, Best Practices, Examples
# - Code: Show cache-aside, write-through patterns
# - Related docs: connection-management.md, key-naming-conventions.md

# Step 3: Remove reference sections
# - Delete "Category-Specific Section Guide"
# - Delete "Validation Checklist"

# Done! Your document follows the standard.
```

---

## 📋 Document Standard

Each atomic document MUST include:

| Element | Required | Description |
|---------|----------|-------------|
| **H1 Title** | ✅ MANDATORY | Clear, specific topic name (no placeholders) |
| **Introduction** | ✅ MANDATORY | 1-3 paragraphs explaining what, why, when |
| **Category-Specific Sections** | ✅ MANDATORY | Choose appropriate sections from template |
| **Code Examples** | ⚠️ IF APPLICABLE | CORRECT/INCORRECT patterns for practical guidance |
| **Related Documents** | ✅ MANDATORY | Links to 2-3+ related atomic docs |

### Mandatory Structure

```markdown
# {Clear Specific Title}

{Introduction: 1-3 paragraphs}

## {Category-Specific Sections}
{Content with examples}

## Related Documents
- `docs/atomic/{category}/{file}.md`
- `docs/atomic/{category}/{file2}.md`
```

---

## 🎯 Core Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Single Responsibility** | One topic = one file | ✅ `redis-connection-management.md` <br> ❌ `redis-everything.md` |
| **Concise** | Keep focused, typically < 200 lines | Short, scannable documents |
| **Definitive** | Authoritative source for the topic | This is the SSOT |
| **Linked** | Reference related docs, don't duplicate | Use links instead of copying |
| **Practical** | Include working code examples | Real-world guidance |
| **Current** | Use latest versions (Python 3.12+, current libs) | No outdated patterns |

---

## 📂 Category Overview

| Category | Focus | Document Count | Status |
|----------|-------|----------------|--------|
| **architecture/** | Architectural principles, patterns, constraints | 10 | ✅ Complete |
| **services/** | Service-specific setup and patterns | 28 | ✅ Complete |
| - `services/fastapi/` | FastAPI setup, routing, security, testing | 11 | ✅ Complete |
| - `services/aiogram/` | Aiogram bot setup, handlers, middleware | 8 | ✅ Complete |
| - `services/asyncio-workers/` | AsyncIO workers, task management | 7 | ✅ Complete |
| - `services/data-services/` | Data service patterns for PostgreSQL/MongoDB | 6 | ✅ Complete |
| **integrations/** | Integration patterns for external systems | 36 | ✅ Complete |
| - `integrations/redis/` | Redis connection, caching, idempotency | 9 | ✅ Complete |
| - `integrations/rabbitmq/` | RabbitMQ messaging, queues, consumers | 11 | ✅ Complete |
| - `integrations/http-communication/` | HTTP clients, retries, tracing | 6 | ✅ Complete |
| - `integrations/cross-service/` | Service discovery, health checks | 4 | ✅ Complete |
| **infrastructure/** | Infrastructure setup and deployment | 24 | ✅ Complete |
| - `infrastructure/containerization/` | Docker, Docker Compose patterns | 5 | ✅ Complete |
| - `infrastructure/api-gateway/` | Nginx, load balancing, SSL | 5 | ✅ Complete |
| - `infrastructure/databases/` | Database setup, migrations | 5 | ✅ Complete |
| - `infrastructure/configuration/` | Config management, secrets | 4 | ✅ Complete |
| - `infrastructure/deployment/` | CI/CD, production deployment | 4 | ✅ Complete |
| **observability/** | Logging, metrics, tracing, error tracking | 24 | ✅ Complete |
| - `observability/logging/` | Structured logging, correlation | 6 | ✅ Complete |
| - `observability/metrics/` | Prometheus, custom metrics | 5 | ✅ Complete |
| - `observability/tracing/` | OpenTelemetry, Jaeger | 5 | ✅ Complete |
| - `observability/error-tracking/` | Sentry integration, alerting | 3 | ✅ Complete |
| - `observability/elk-stack/` | Elasticsearch, Logstash, Kibana | 4 | ✅ Complete |
| **testing/** | Unit, integration, E2E, service testing | 20 | ✅ Complete |
| - `testing/unit-testing/` | Pytest, fixtures, mocking | 5 | ✅ Complete |
| - `testing/integration-testing/` | Testcontainers, database testing | 5 | ✅ Complete |
| - `testing/service-testing/` | FastAPI, Aiogram, Worker testing | 4 | ✅ Complete |
| - `testing/end-to-end-testing/` | User journey, performance testing | 3 | ✅ Complete |
| - `testing/quality-assurance/` | Linting, type checking, code review | 3 | ✅ Complete |
| **databases/** | Database setup and patterns | 6 | ✅ Complete |
| **security/** | Security patterns and implementations | 4 | ✅ Complete |
| **real-time/** | WebSocket, SSE, real-time patterns | 4 | ✅ Complete |
| **file-storage/** | File storage patterns (S3, local) | 5 | ✅ Complete |
| **external-integrations/** | Third-party API integrations | 4 | ✅ Complete |

**Total:** 162 documents | **Completed:** 162 (100%) | **TODO:** 0 (0%)

---

## 🚀 Contributing

### Adding New Documents

1. **Use Template**: Copy `TEMPLATE.md` as starting point
2. **Follow Section Guide**: Choose appropriate sections from template's category guide
3. **Write Content**: Fill in introduction, sections, code examples, related links
4. **Remove Reference Sections**: Delete "Category-Specific Section Guide" and "Validation Checklist"
5. **Validate**: Check against template's validation checklist
6. **Update Indexes**: Add entry to this README and `docs/INDEX.md`

### Updating Existing Documents

1. **Read Current Version**: Understand existing content
2. **Check Template Compliance**: Verify structure matches `TEMPLATE.md`
3. **Update Content**: Improve clarity, add examples, update versions
4. **Verify Links**: Ensure all related documents links work
5. **Update Metadata**: Change "Last Updated" date if document has metadata section

### Quality Standards

Before submitting new/updated atomic documents:

- [ ] Structure follows `TEMPLATE.md`
- [ ] H1 title is clear and specific
- [ ] Introduction has 1-3 paragraphs minimum
- [ ] Code examples use Python 3.12+ with type hints
- [ ] Code examples follow CORRECT/INCORRECT pattern (when applicable)
- [ ] "Related Documents" section has 2-3+ links
- [ ] No TODO placeholders
- [ ] No sensitive data (passwords, tokens, real IPs)
- [ ] Follows naming conventions (snake_case for code, kebab-case for Kubernetes)
- [ ] Links use relative paths (`docs/atomic/...`)
- [ ] No grammar/spelling errors

---

## 🔧 Maintenance

### Updating Technology Versions

When underlying technologies change (Python version, library versions, etc.):

1. Update relevant atomic documents
2. Update code examples with new syntax/APIs
3. Test updated examples
4. Update "Prerequisites" or "Dependencies" sections
5. Note version changes in commit message

### Archiving Obsolete Documents

If a pattern becomes obsolete:

1. Add "DEPRECATED" notice at top of document
2. Update links in related documents
3. Remove from this README's category list
4. Mark in `docs/INDEX.md` with ⚠️ DEPRECATED marker
5. Consider removal after 6 months if no usage

### Regular Maintenance Tasks

- **Monthly**: Review TODO documents, prioritize filling gaps
- **Quarterly**: Check for broken links, outdated examples
- **Per major version**: Update all code examples, dependency versions
- **As needed**: Add new categories when introducing new technologies

---

## 📊 Documentation Coverage

### Current Status

```
Total Documents:     162
Completed:           162 (100%)
TODO (Need Work):      0 (0%)

All documentation categories are complete:
✅ architecture/         10 docs
✅ services/             28 docs
✅ integrations/         36 docs
✅ infrastructure/       24 docs
✅ observability/        24 docs
✅ testing/              20 docs
✅ databases/             6 docs
✅ security/              4 docs
✅ real-time/             4 docs
✅ file-storage/          5 docs
✅ external-integrations/ 4 docs
```

### Documentation Quality

All atomic documents include:
- Clear introduction (1-3 paragraphs)
- Configuration examples with code
- Best practices (DO/DON'T patterns)
- Working code examples (Python 3.12+)
- Checklists for verification
- Related documents links

---

## 🔍 Finding Documents

### By Task

| I want to... | See Category |
|-------------|--------------|
| Understand architecture principles | `architecture/` |
| Set up a FastAPI service | `services/fastapi/` |
| Set up an Aiogram bot | `services/aiogram/` |
| Set up an AsyncIO worker | `services/asyncio-workers/` |
| Integrate with Redis | `integrations/redis/` |
| Integrate with RabbitMQ | `integrations/rabbitmq/` |
| Make HTTP calls between services | `integrations/http-communication/` |
| Set up Docker Compose | `infrastructure/containerization/` |
| Configure Nginx | `infrastructure/api-gateway/` |
| Deploy to production | `infrastructure/deployment/` |
| Add logging | `observability/logging/` |
| Add metrics | `observability/metrics/` |
| Add tracing | `observability/tracing/` |
| Write tests | `testing/` (specific subdirectory by test type) |
| Set up PostgreSQL | `databases/postgresql/` |
| Implement security | `security/` |
| Add WebSocket support | `real-time/` |
| Upload/download files | `file-storage/` |
| Integrate third-party API | `external-integrations/` |

### By Document Name

See `docs/INDEX.md` for complete alphabetical index of all atomic documents.

---

## 📚 Related Documentation

- **[TEMPLATE.md](TEMPLATE.md)** — Universal template for atomic documents
- **[../INDEX.md](../INDEX.md)** — Complete documentation catalog
- **[../LINKS_REFERENCE.md](../LINKS_REFERENCE.md)** — Central link reference table
- **[../STYLE_GUIDE.md](../STYLE_GUIDE.md)** — Formatting standards
- **[../guides/architecture-guide.md](../guides/architecture-guide.md)** — Architecture overview

---

## 💡 Tips for Document Authors

### Writing Effective Code Examples

```python
# ✅ GOOD: Clear, runnable, with context
async def create_user(user_data: UserCreateDTO) -> User:
    """Create a new user with validation.

    Args:
        user_data: User creation data

    Returns:
        Created user instance

    Raises:
        ValidationError: If user_data is invalid
    """
    # Validate email format
    if not is_valid_email(user_data.email):
        raise ValidationError("Invalid email format")

    # Create user via data service HTTP call
    user = await postgres_client.create_user(user_data.dict())
    return User(**user)

# ❌ BAD: No context, unclear purpose
def create(data):
    return db.insert(data)
```

### Linking to Related Documents

```markdown
✅ GOOD:
- `docs/atomic/services/fastapi/basic-setup.md` — FastAPI service scaffolding
- `docs/atomic/integrations/redis/connection-management.md` — Redis client setup

❌ BAD:
- See FastAPI docs
- Check Redis integration
```

### Structuring Sections

```markdown
✅ GOOD: Clear hierarchy
## Configuration
### Client Setup
### Connection Pooling
### Timeouts

❌ BAD: Flat structure
## Configuration
## Client Setup
## Connection Pooling
## Timeouts
```

---

## ⚠️ Common Mistakes to Avoid

1. **Creating documents without using TEMPLATE.md**
   - Result: Inconsistent structure, missing sections
   - Fix: Always start with `cp docs/atomic/TEMPLATE.md ...`

2. **Duplicating content from other documents**
   - Result: Maintenance nightmare, conflicting info
   - Fix: Link to other docs instead of copying

3. **Writing generic documents that cover multiple topics**
   - Result: Violates single responsibility principle
   - Fix: Split into multiple focused documents

4. **Using outdated code examples**
   - Result: Users copy old patterns
   - Fix: Always use Python 3.12+, latest library versions

5. **Not removing reference sections from TEMPLATE.md**
   - Result: Published docs contain meta-instructions
   - Fix: Delete "Category-Specific Section Guide" and "Validation Checklist"

6. **Missing Related Documents section**
   - Result: Users can't navigate to related content
   - Fix: Always include 2-3+ related document links

7. **Using hyphens in Python code examples**
   - Result: SyntaxError when users copy code
   - Fix: Use snake_case (`finance_lending_api`, not `finance-lending-api`)

---

## 📞 Getting Help

- **Questions about template usage**: See `TEMPLATE.md` instructions and examples
- **Questions about specific categories**: See existing documents in that category
- **Questions about architecture**: See `docs/guides/architecture-guide.md`
- **Questions about framework**: See `README.md` at project root

---

**Last Updated:** 2025-12-18
**Maintainers:** Documentation Team
