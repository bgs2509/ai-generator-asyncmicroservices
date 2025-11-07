# Changelog

All notable changes to the AI Generator for Async Microservices framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

#### 🎯 Phase 1: DRY/KISS/YAGNI Principles Enforcement (2025-11-07)

- **📖 DRY/KISS/YAGNI Principles Guide** (`docs/guides/dry-kiss-yagni-principles.md`)
  - Comprehensive 915-line educational guide for AI agents and developers
  - 6 major sections covering DRY, KISS, YAGNI principles
  - Direct links to framework architecture (HTTP-only pattern, maturity levels)
  - Automated detection tools and commands
  - Before/after code examples for each principle
  - Cross-referenced from AGENTS.md and INDEX.md

- **🛠️ Shared Utilities Template** (`templates/shared/utils/`)
  - **logger.py** - Structured JSON logging factory with request ID support
  - **validators.py** - 10+ reusable validators (email, phone, UUID, password, slug, etc.)
  - **exceptions.py** - Base exception hierarchy with HTTP status code mapping
  - **pagination.py** - Offset and cursor pagination helpers with Pydantic models
  - **request_id.py** - Correlation ID management using context variables (async-safe)
  - **README.md** - 600+ line comprehensive usage guide with migration instructions
  - **Total**: 8 files, 1,769 lines eliminating code duplication

- **💾 PostgreSQL Data Service Template** (`templates/services/template_data_postgres_api/`)
  - Complete production-ready template with 27 files
  - **Async SQLAlchemy 2.0+** with asyncpg driver and full type safety
  - **Alembic migrations** for database schema versioning
  - **Generic CRUD repository** (BaseRepository) eliminating boilerplate
  - **Health check endpoints** (/health, /health/ready) for Kubernetes
  - **Testcontainers** integration for real database testing
  - **Multi-stage Dockerfile** (development + production)
  - Model mixins: TimestampMixin, SoftDeleteMixin
  - Connection pooling, graceful shutdown, comprehensive error handling
  - 100% type hints compatible with mypy strict mode

- **✅ Automated Quality Gates** (`templates/ci-cd/.github/workflows/ci.yml`)
  - **DRY Check** (jscpd): Fails if code duplication >10%
  - **KISS Check** (radon):
    - Cyclomatic complexity < 10 (McCabe)
    - Maintainability Index >= B (20+ score)
    - File size < 500 lines
  - **YAGNI Check**: Dependency count limits (30 for data, 50 for business services)
  - Comprehensive documentation (`docs/quality/automated-quality-gates.md`, 500+ lines)
  - Clear failure messages with remediation guidance
  - Local testing commands included

#### 📊 Quality Metrics

All Phase 1 deliverables passed automated quality gates:
- **Code Duplication**: 0% (target: <10%) ✅
- **Cyclomatic Complexity**: Average A (1.79) (target: <10) ✅
- **Maintainability Index**: All files Grade B or better ✅
- **File Size**: All files <500 lines (largest: ~400 lines) ✅
- **Dependencies**: 11-27 dependencies (thresholds: 30-50) ✅

#### 📈 Framework Improvements

- **Template Completion**: 58% → 68%
- **Documentation**: +3,500 lines across guides, templates, and quality documentation
- **Files Created**: 38 new files + 5 updated
- **Git Commits**: 4 detailed commits with comprehensive messages

- **📚 Anti-Pattern Documentation**: Integrated production-tested anti-patterns across atomic documents
  - **TEMPLATE.md**: Added Anti-Patterns section template with WRONG/CORRECT code example structure
  - **CONTRIBUTING.md**: Added comprehensive anti-pattern contribution guidelines with priority classification
  - **INDEX.md**: Added Anti-Pattern Quick Reference table with symptom-based lookup
  - **🔴 CRITICAL Anti-Patterns**:
    - Global FSM Storage Never Closed → `atomic/services/aiogram/state-management.md`
    - HTTP Client Proliferation → `atomic/integrations/http-communication/http-client-patterns.md`
    - Connection Pool Misuse → `atomic/integrations/redis/connection-management.md`
  - **🟠 HIGH Priority Anti-Patterns**:
    - Silent Exception Swallowing → `atomic/services/fastapi/error-handling.md`
    - Deprecated Lifecycle APIs → `atomic/services/fastapi/lifespan-management.md`
    - No Graceful Shutdown → `atomic/integrations/cross-service/graceful-shutdown.md`
  - All anti-patterns include monitoring commands (`docker stats`, `netstat`, `redis-cli CLIENT LIST`)
  - Source: Activity Tracker Bot ADR-20251107-001 (production lessons learned)

### Planned
- Example projects (Telemedicine, P2P Lending)
- Enhanced service templates with WebSocket support
- Complete observability setup with pre-configured dashboards
- CLI tool for project scaffolding

---

## [0.1.0] - 2025-01-05

### 🎉 Initial Release

This is the first public release of the AI Generator for Async Microservices framework.

### Added

#### Documentation
- **AGENTS.md** - Entry point for AI agents with complete framework overview
- **135+ atomic documentation modules** covering:
  - Architecture patterns and principles
  - Service implementation guides
  - Infrastructure setup and configuration
  - Observability and monitoring
  - Testing strategies
  - Security best practices
- **Comprehensive guides**:
  - AI Code Generation Master Workflow (7 stages)
  - Architecture Guide
  - Development Commands Reference
  - Prompt Validation Guide
- **Reference documentation**:
  - Project Structure
  - Technology Stack
  - Maturity Levels (PoC → Production)
  - Service Naming Conventions
- **INDEX.md** - Complete documentation index

#### Service Templates
- **Business API Template** (FastAPI)
  - DDD/Hexagonal architecture
  - HTTP-only data access
  - Type-safe with mypy strict mode
  - Async-first design
  - Built-in observability
- **Data API Template - PostgreSQL**
  - SQLAlchemy 2.0 async integration
  - Alembic migrations
  - Connection pooling
  - Type-safe queries
- **Data API Template - MongoDB**
  - Motor async driver
  - Document modeling patterns
  - Index management
- **Worker Template** (AsyncIO)
  - Background task processing
  - RabbitMQ integration
  - Graceful shutdown
  - Error handling and retry logic
- **Bot Template** (Aiogram 3.x)
  - Telegram bot integration
  - State management
  - Command handling
  - Middleware patterns

#### Infrastructure
- **Docker configurations** for all service types
- **Docker Compose** examples for development
- **Nginx** configuration templates
- **Database** setup guides (PostgreSQL, MongoDB, Redis)
- **Message queue** setup guides (RabbitMQ)

#### Observability
- **Structured logging** patterns
- **Prometheus metrics** integration guides
- **Distributed tracing** with Jaeger setup
- **Health checks** implementation
- **Error tracking** with Sentry patterns

#### Testing
- **pytest** configuration and patterns
- **Testcontainers** integration examples
- **Unit testing** patterns with fixtures and mocking
- **Integration testing** for all service types
- **FastAPI testing** patterns
- **Aiogram testing** patterns

#### Quality Assurance
- **Type checking** with mypy strict mode
- **Linting standards** with Ruff
- **Code review checklist**
- **Coverage requirements**

#### Security
- **Authentication and authorization** patterns
- **Session management** best practices
- **Security testing guide**
- **SECURITY.md** - Security policy and vulnerability reporting

#### Community
- **CODE_OF_CONDUCT.md** - Community guidelines
- **CONTRIBUTING.md** - Contribution guidelines
- **LICENSE** - MIT License
- **README.md** - Comprehensive project overview

#### GitHub Integration
- **Issue templates** (Bug Report, Feature Request, Question)
- **Pull Request template**
- **GitHub Discussions** configuration

#### Documentation Site
- **MkDocs Material** configuration
- **Custom CSS** styling
- **Comprehensive navigation** structure
- **GitHub Pages** ready setup

### Project Philosophy
- **One Ring Architecture** - Single consistent pattern across all projects
- **HTTP-Only Data Access** - Business services never access databases directly
- **Async-First** - All I/O operations use async/await
- **Type Safety** - Full type hints and mypy strict mode
- **Observability by Design** - Logging, metrics, and tracing built-in
- **AI-Friendly** - Designed for AI code generation with atomic documentation

### Technology Stack
- **Python** 3.12+
- **FastAPI** 0.115+
- **Aiogram** 3.13+
- **PostgreSQL** 16+ with SQLAlchemy 2.0+
- **MongoDB** 7+ with Motor
- **Redis** 7+
- **RabbitMQ** 3.13+
- **Docker** 24.0+
- **Nginx** 1.27+
- **Prometheus**, **Grafana**, **Jaeger** for observability
- **pytest** 8.3+, **mypy** 1.11+, **Ruff** 0.6+ for quality

### Documentation Stats
- **Total files**: 150+ markdown documents
- **Lines of documentation**: 10,000+
- **Code examples**: 200+
- **Architecture diagrams**: 15+

---

## Release Notes

### Version Numbering
- **Major version** (x.0.0): Breaking changes, major feature additions
- **Minor version** (0.x.0): New features, backward compatible
- **Patch version** (0.0.x): Bug fixes, documentation updates

### Support Policy
- **Current version**: Full support with active development
- **Previous minor version**: Security fixes and critical bugs
- **Older versions**: Community support only

---

## How to Upgrade

### From Development to 0.1.0
This is the first release, no upgrade needed.

### Future Upgrades
Upgrade guides will be provided with each release that includes breaking changes.

---

## Links

- **Repository**: https://github.com/bgs2509/ai-generator-asyncmicroservices
- **Documentation**: https://bgs2509.github.io/ai-generator-asyncmicroservices
- **Issues**: https://github.com/bgs2509/ai-generator-asyncmicroservices/issues
- **Discussions**: https://github.com/bgs2509/ai-generator-asyncmicroservices/discussions

---

## Contributors

Thank you to all contributors who helped make this release possible!

- [@bgs2509](https://github.com/bgs2509) - Creator and maintainer

---

**Legend:**
- 🎉 Major milestone
- ✨ New feature
- 🐛 Bug fix
- 📚 Documentation
- 🔧 Configuration
- ⚡ Performance improvement
- 🔒 Security fix
- 💥 Breaking change
- 🗑️ Deprecation

---

[Unreleased]: https://github.com/bgs2509/ai-generator-asyncmicroservices/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/bgs2509/ai-generator-asyncmicroservices/releases/tag/v0.1.0
