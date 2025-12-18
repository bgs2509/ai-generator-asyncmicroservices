# Canonical Reference Guide

> **Purpose**: Single source of truth for canonical documentation locations.
>
> When multiple documents cover similar topics, this guide identifies which
> document is the authoritative source.

## Why This Matters

The project contains 170+ documentation files covering overlapping topics.
To avoid confusion and conflicting information, each topic should have
ONE canonical source that all other documents reference.

**Rule**: If a document is listed here as canonical, other documents should
link to it rather than duplicating the content.

---

## Canonical Sources by Topic

### Architecture

| Topic | Canonical Source | Purpose |
|-------|------------------|---------|
| Overall Architecture | `ARCHITECTURE.md` | High-level system design |
| Improved Hybrid Approach | `docs/atomic/architecture/improved-hybrid-overview.md` | HTTP-only data access pattern |
| Service Separation | `docs/atomic/architecture/service-separation-principles.md` | Business vs Data services |
| Naming Conventions | `docs/atomic/architecture/naming-conventions.md` | All naming standards |
| DDD/Hexagonal | `docs/atomic/architecture/ddd-hexagonal-principles.md` | Domain-driven design |
| Event Loop | `docs/atomic/architecture/event-loop-management.md` | Single ownership pattern |

### Services

| Topic | Canonical Source | Purpose |
|-------|------------------|---------|
| FastAPI Setup | `docs/atomic/services/fastapi/basic-setup.md` | Application factory pattern |
| Aiogram Setup | `docs/atomic/services/aiogram/basic-setup.md` | Bot initialization |
| AsyncIO Workers | `docs/atomic/services/asyncio-workers/basic-setup.md` | Background task setup |
| Data Services | `docs/atomic/services/data-services/postgres-service-setup.md` | Data API pattern |

### Infrastructure

| Topic | Canonical Source | Purpose |
|-------|------------------|---------|
| PostgreSQL | `docs/atomic/infrastructure/databases/postgresql-setup.md` | Database setup |
| RabbitMQ | `docs/atomic/integrations/rabbitmq/connection-management.md` | Message queue setup |
| Redis | `docs/atomic/integrations/redis/connection-management.md` | Cache setup |
| Docker Compose | `docs/atomic/infrastructure/containerization/docker-compose-setup.md` | Container orchestration |
| Nginx | `docs/atomic/infrastructure/api-gateway/nginx-setup.md` | API gateway config |

### Testing

| Topic | Canonical Source | Purpose |
|-------|------------------|---------|
| Pytest Setup | `docs/atomic/testing/unit-testing/pytest-setup.md` | Test configuration |
| Fixtures | `docs/atomic/testing/unit-testing/fixture-patterns.md` | Fixture patterns |
| Mocking | `docs/atomic/testing/unit-testing/mocking-strategies.md` | Mock patterns |
| Integration | `docs/atomic/testing/integration-testing/testcontainers-setup.md` | Container-based tests |

### AI Workflow

| Topic | Canonical Source | Purpose |
|-------|------------------|---------|
| 7-Stage Workflow | `docs/guides/ai-code-generation-master-workflow.md` | Complete AI workflow |
| Maturity Levels | `docs/reference/maturity-levels.md` | Level definitions |
| Conditional Rules | `docs/reference/conditional-stage-rules.md` | Stage entry conditions |
| Agent Context | `docs/reference/agent-context-summary.md` | Quick reference for AI |

### Templates

| Topic | Canonical Source | Purpose |
|-------|------------------|---------|
| Template Overview | `templates/README.md` | All templates status |
| Shared Utils | `templates/shared/utils/README.md` | Utility usage |
| Business API | `templates/services/template_business_api/README.md` | API template |
| Business Bot | `templates/services/template_business_bot/README.md` | Bot template |
| Business Worker | `templates/services/template_business_worker/README.md` | Worker template |

---

## How to Use This Guide

### For Documentation Writers

1. Check this guide before creating new documentation
2. If a canonical source exists, reference it instead of duplicating
3. If creating new content, update this guide with the new canonical location

### For AI Agents

1. When asked about a topic, check this guide first
2. Use the canonical source as the primary reference
3. Cross-reference with other documents only for additional context

### For Developers

1. Use canonical sources as authoritative
2. Report conflicts between documents to maintainers
3. Suggest updates to this guide when new patterns emerge

---

## Conflict Resolution

If you find conflicting information:

1. **Canonical source wins** — Always trust the canonical document
2. **Report the conflict** — Create an issue with both document paths
3. **Update non-canonical** — Align other documents with canonical source

---

## Related Documents

- `docs/INDEX.md` — Complete documentation catalog
- `docs/LINKS_REFERENCE.md` — Central link reference table
- `docs/STYLE_GUIDE.md` — Formatting standards
