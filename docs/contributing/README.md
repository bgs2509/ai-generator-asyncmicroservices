# Contributing to AI Framework

Welcome! This directory contains resources for contributors to the AI Framework.

## 📁 Directory Structure

```
contributing/
├── README.md                      # This file - contribution overview
├── improvement-plans/             # Detailed plans for significant enhancements
│   ├── README.md                  # How to create and use improvement plans
│   └── 2025-01-*.md              # Active improvement plans
├── feature-proposals/             # Proposals for new framework capabilities (future)
└── refactoring-plans/             # Architectural refactoring plans (future)
```

## 🎯 Types of Contributions

### 1. Improvement Plans (`improvement-plans/`)

**Purpose:** Coordinate complex, multi-phase enhancements

**Use for:**
- Framework-wide improvements (affecting docs, templates, workflows)
- Multi-week efforts requiring coordination
- Architectural changes or pattern introductions
- Phased rollouts

**Examples:**
- Enforcing DRY/KISS/YAGNI principles across framework
- Completing template coverage (shared utils, data services)
- Adding automated quality gates
- Implementing new anti-pattern detection

**Process:**
1. Create plan document using template from `improvement-plans/README.md`
2. Submit PR for review (plan only, no code)
3. Iterate based on maintainer feedback
4. After approval, implement tasks from plan
5. Update plan progress regularly
6. Mark plan complete when all tasks validated

📖 [Learn more](improvement-plans/README.md)

### 2. Feature Proposals (`feature-proposals/`) - Coming Soon

**Purpose:** Propose new capabilities for the framework

**Use for:**
- New service types (e.g., gRPC services, GraphQL APIs)
- New integrations (e.g., Apache Kafka, Elasticsearch)
- New maturity levels or architectural patterns
- Major documentation additions

**Process:** TBD

### 3. Refactoring Plans (`refactoring-plans/`) - Coming Soon

**Purpose:** Plan significant architectural refactorings

**Use for:**
- Breaking changes to templates or workflows
- Deprecating old patterns
- Major documentation restructuring
- Changing naming conventions

**Process:** TBD

### 4. Direct Contributions

For smaller contributions, use standard GitHub workflow:

**Bug fixes:**
- Open issue describing bug
- Submit PR with fix
- Reference issue in PR description

**Documentation improvements:**
- Minor typo fixes: direct PR
- New atomic docs: follow template in `docs/atomic/TEMPLATE.md`
- Guide additions: discuss in issue first

**Template enhancements:**
- Small fixes: direct PR
- New templates: create improvement plan

## 🚀 Quick Start Guide

### For New Contributors

1. **Read framework documentation:**
   - [README](../../README.md) - Framework overview
   - [ARCHITECTURE](../../ARCHITECTURE.md) - Architectural principles
   - [Agent Workflow](../guides/ai-code-generation-master-workflow.md) - How AI uses framework

2. **Find contribution opportunities:**
   - Check [improvement-plans/](improvement-plans/) for active plans
   - Look for "good first issue" or "help wanted" labels
   - Review incomplete templates in `../../templates/README.md`

3. **Understand contribution workflow:**
   - Read main [CONTRIBUTING.md](../../CONTRIBUTING.md)
   - Review relevant plan document (if applicable)
   - Comment on issue/plan to claim task

4. **Set up development environment:**
   ```bash
   # Clone framework
   git clone <repo-url>
   cd .ai-framework

   # Install docs dependencies (if contributing to docs)
   pip install -r requirements-docs.txt

   # Preview docs locally
   mkdocs serve
   ```

5. **Make your contribution:**
   - Create feature branch: `git checkout -b feature/descriptive-name`
   - Make changes following style guides
   - Test thoroughly (see below)
   - Submit PR with clear description

### Testing Your Changes

**Documentation changes:**
```bash
# Check Markdown syntax
markdownlint docs/

# Build docs to check for errors
mkdocs build --strict

# Preview locally
mkdocs serve
# Visit http://127.0.0.1:8000
```

**Template changes:**
```bash
# Generate test project using your modified templates
python scripts/generate-project.py \
  --templates ./templates \
  --maturity-level 2 \
  --business-ideas "Test project for template validation" \
  --output /tmp/test-generated

# Validate generated project
cd /tmp/test-generated
make lint         # Should pass
make test         # Should pass
docker-compose up # Should start without errors
```

**Workflow changes:**
```bash
# Run workflow validation script
python scripts/validate-workflow.py

# Test with AI agent (if you have access)
# Follow instructions in docs/guides/testing-workflow-changes.md
```

## 📋 Contribution Checklist

Before submitting PR, verify:

- [ ] **Code/docs follow style guide**
  - Markdown: CommonMark format, wrap at 120 chars
  - Python templates: PEP 8, type hints, docstrings
  - YAML: 2-space indentation, alphabetized keys (where logical)

- [ ] **Changes are documented**
  - Update relevant atomic docs
  - Add inline comments for complex logic
  - Update CHANGELOG.md if applicable

- [ ] **Tests pass** (for template/code changes)
  - Linting: `make lint`
  - Type checking: `mypy`
  - Unit tests: `pytest`
  - Integration tests: `pytest tests/integration`

- [ ] **Backward compatibility maintained** (unless breaking change is approved)
  - Existing templates still work
  - Workflow stages remain compatible
  - Deprecated features have migration guide

- [ ] **PR description is clear**
  - References issue or improvement plan
  - Explains "why" not just "what"
  - Lists acceptance criteria satisfied
  - Includes screenshots (for UI/docs changes)

## 🎨 Style Guides

### Markdown Documentation

- Use ATX-style headers (`#`, `##`, `###`)
- Wrap lines at 120 characters (use soft wrap in editor)
- Use fenced code blocks with language specifier
- Link to other docs using relative paths
- Use emoji sparingly (only for status indicators)

**Example:**
```markdown
## Service Architecture

The framework uses a [hybrid approach](../atomic/architecture/improved-hybrid-overview.md) that combines:

- **Data Services:** Direct database access (PostgreSQL, MongoDB)
- **Business Services:** HTTP-only communication with data services

```python
# Example: Business service calling data service
async def get_user(user_id: int) -> User:
    response = await data_client.get(f"/users/{user_id}")
    return User(**response.json())
```

For more details, see [HTTP client patterns](../atomic/integrations/http/client-patterns.md).
```

### Template Code (Python)

Follow framework conventions:
- Type hints for all function signatures
- Docstrings in Google style
- Import order: standard lib → third party → local
- Max line length: 100 characters
- Use `async`/`await` for I/O operations

**Example:**
```python
"""User service module for managing user operations."""

from typing import Optional
import logging

from fastapi import HTTPException
from pydantic import BaseModel

from infrastructure.http_clients.data_client import DataClient


logger = logging.getLogger(__name__)


class UserService:
    """Service for user management operations.

    This service handles user CRUD operations by communicating
    with the data service via HTTP.
    """

    def __init__(self, data_client: DataClient) -> None:
        """Initialize user service.

        Args:
            data_client: HTTP client for data service communication
        """
        self._data_client = data_client

    async def get_user(self, user_id: int) -> Optional[UserDTO]:
        """Retrieve user by ID.

        Args:
            user_id: Unique identifier of the user

        Returns:
            User data transfer object, or None if not found

        Raises:
            HTTPException: If data service is unavailable
        """
        try:
            response = await self._data_client.get(f"/users/{user_id}")
            return UserDTO(**response.json())
        except HTTPException as e:
            logger.error(f"Failed to fetch user {user_id}: {e}")
            raise
```

### YAML Configuration

- 2-space indentation
- Alphabetize keys (unless order matters, e.g., Docker Compose depends_on)
- Use anchors for repeated configuration
- Comment non-obvious settings

**Example:**
```yaml
services:
  business_api:
    build:
      context: ./services/business_api
      dockerfile: Dockerfile
    container_name: business_api
    depends_on:
      - data_postgres_api
    environment:
      DATA_SERVICE_URL: http://data_postgres_api:8001
      LOG_LEVEL: ${LOG_LEVEL:-INFO}
    ports:
      - "${API_PORT:-8000}:8000"
    restart: unless-stopped
```

## 🤝 Code of Conduct

All contributors must follow the [Code of Conduct](../../CODE_OF_CONDUCT.md):

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the framework and community
- Accept responsibility for mistakes

## ❓ Questions or Need Help?

- **Documentation questions:** Check [docs/INDEX.md](../INDEX.md) for navigation
- **Contribution process:** Review this document and [CONTRIBUTING.md](../../CONTRIBUTING.md)
- **Technical questions:** Open GitHub Discussion or Issue
- **Security vulnerabilities:** See [SECURITY.md](../../SECURITY.md)

## 📊 Contribution Statistics

Want to see contribution history?

```bash
# Contributors by commit count
git shortlog -sn --no-merges

# Recent contributions
git log --pretty=format:"%h %an %ad %s" --date=short -n 20

# Files most frequently modified
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -20
```

---

**Thank you for contributing to the AI Framework!** Your efforts help improve code generation quality for all users. 🎉
