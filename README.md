# AI Generator for Async Microservices

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://bgs2509.github.io/ai-generator-asyncmicroservices)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Introduction

### The Problem: Three Projects, Three Rings of Chaos 🌋

Ask AI to generate code for three projects. Get three different kingdoms:

- **Project A**: `user_service` + direct DB + `print()` debugging (it's 2025, not 2015!)
- **Project B**: `userService` + HTTP APIs + DB access (wait, both?!) + `OhNoSomethingWentWrongException`
- **Project C**: `user-svc_v2_FINAL` + mystery data layer + `try/except: pass` (courage of closing eyes)

You're not a developer. You're an archaeologist hunting "that RabbitMQ config."

**Different projects. Different planets. Different despair.**

### The Solution: One Ring to Rule Them All 💍

**AI Generator for Async Microservices** — your architectural One Ring. One pattern. One truth.

```
┌──────────────────────────────────────────┐
│  💍 One Ring — Every Project            │
├──────────────────────────────────────────┤
│  Structure:  Business API, Data API,     │
│              Workers, Bots               │
│                                          │
│  Naming:     {context}_{domain}_{type}   │
│              finance_lending_api ✅      │
│              No user-svc_v2_FINAL 🚫     │
│                                          │
│  Patterns:   HTTP-only data access       │
│              Async-first                 │
│              Type-safe (mypy strict)     │
│                                          │
│  Stack:      FastAPI, PostgreSQL, Redis  │
│              RabbitMQ, Docker, Nginx     │
│              Prometheus, Grafana, Jaeger │
└──────────────────────────────────────────┘
```

**The magic?** AI doesn't reinvent. AI **copies** battle-tested infrastructure, generates your unique business logic.

- Infrastructure (Docker, Nginx, CI/CD)? **Copy.** ✅
- Logging, health checks, graceful shutdown? **Copy.** ✅
- Your `LoanApplication`, `TelemedicineSession`? **AI generates.** 🤖

Open Project A Monday. Navigate blindfolded.
Switch to Project B Tuesday. Same structure. Same joy.
Deploy Project C Friday. You already know every file.

**One standard. Every project. Your sanity preserved.**

*"One architecture to rule them all, one pattern to bind them, one framework to bring them all, and in the structure unite them."* ⚔️

---

## Quick Start

### Prerequisites

- **Python** 3.12+
- **Docker** 24.0+
- **Docker Compose** 2.20+
- **Git** 2.40+

### Setup Framework as Knowledge Base

```bash
# Create your project and add framework
mkdir my_awesome_project && cd my_awesome_project && git init
git submodule add https://github.com/bgs2509/ai-generator-asyncmicroservices .ai-framework
git submodule update --init --recursive
```

**That's it!** 🎉

**Next:** Point your AI agent to `.ai-framework/AGENTS.md` — it will read the knowledge base and generate code in your project.

### How to Generate Code with AI

Open your AI assistant (Claude, ChatGPT) and copy-paste this prompt:

```
I have microservices framework in: .ai-framework/

INSTRUCTIONS FOR AI:
1. First, read .ai-framework/AGENTS.md to understand the framework
2. Then, validate my prompt using .ai-framework/docs/guides/prompt-validation-guide.md
3. Ask me for any missing information before generating code
4. Only after validation passes, generate code following framework rules

---

MY PROJECT:

What I'm building:
[Describe your project: e.g., "P2P lending platform" or "Telemedicine app"]

Problem it solves:
[What problem are you solving]

Key features:
- [Feature 1]
- [Feature 2]
- [Feature 3]

How complex should it be:
[Choose one: "Simple prototype" / "Development version" / "Production-ready"]

Additional services needed:
[e.g., "Background workers", "Telegram bot", "MongoDB" or just say "Not sure"]
```

**What happens next:**
- AI reads the framework documentation
- AI validates your prompt (asks questions if something is missing)
- AI generates complete, working code in your project

**Example:**
```
MY PROJECT:

What I'm building:
Telemedicine platform for remote doctor consultations

Problem it solves:
Patients can't easily access doctors remotely

Key features:
- Patient registration
- Doctor scheduling
- Video consultations
- Medical records

How complex should it be:
Simple prototype

Additional services needed:
Not sure
```

---

## Table of Contents

- [Key Features](#key-features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Key Features

- **📚 Atomic Documentation** — 135+ modular docs covering architecture, services, infrastructure, observability, testing, security
- **🎨 Service Templates** — FastAPI Business API, Telegram Bots, Workers, PostgreSQL/MongoDB Data APIs
- **🏗️ Production Infrastructure** — Docker, Nginx, CI/CD, Prometheus, Grafana, Jaeger, ELK
- **🤖 7-Stage AI Workflow** — Validation → Requirements → Planning → Generation → Verification → Handoff
- **🎯 Maturity Levels** — PoC (~5 min) to Production (~30 min) with incremental complexity
- **✅ Quality Built-in** — Type hints, tests, linting, mypy strict mode from day one

---

## Architecture

### Improved Hybrid Approach

The framework implements a **strict service separation model**:

```
┌─────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Business API │  │ Business Bot │  │    Worker    │      │
│  │   (FastAPI)  │  │   (Aiogram)  │  │   (AsyncIO)  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                   HTTP ONLY (no direct DB access)            │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                     ┌───────┴───────┐
                     │               │
         ┌───────────▼─────┐  ┌──────▼───────────┐
         │  Data Service   │  │  Data Service    │
         │  PostgreSQL API │  │   MongoDB API    │
         │  (FastAPI)      │  │   (FastAPI)      │
         └─────────────────┘  └──────────────────┘
                 │                      │
         ┌───────▼─────────┐    ┌──────▼──────────┐
         │   PostgreSQL    │    │    MongoDB      │
         │    Database     │    │    Database     │
         └─────────────────┘    └─────────────────┘
```

### Core Principles

1. **HTTP-Only Data Access** — Business services NEVER access databases directly
2. **Single Event Loop Ownership** — Each service owns its event loop (no sharing)
3. **DDD & Hexagonal Architecture** — Clear domain boundaries and ports/adapters
4. **Async-First** — All I/O operations use async/await
5. **Type Safety** — Full type hints, mypy strict mode compatible
6. **Observability by Design** — Structured logging, metrics, tracing built-in

**Service Naming:** `{context}_{domain}_{type}` (e.g., `finance_lending_api`, `healthcare_telemedicine_bot`) — See [Naming Checklist](docs/checklists/service-naming-checklist.md)

---

## Project Structure

### Framework Structure (when used as submodule)

```
your_project/
├── .ai-framework/                 # Git submodule — Knowledge Base (DO NOT MODIFY)
│   ├── docs/                      # Framework documentation
│   │   ├── atomic/               # Atomic knowledge modules
│   │   ├── guides/               # Implementation guides
│   │   └── reference/            # Reference materials
│   ├── templates/                # Universal templates (for AI reference)
│   └── AGENTS.md                 # AI agent entry point
│
├── services/                      # AI-generated application services
│   ├── finance_lending_api/      # Generated business service
│   ├── finance_user_api/         # Generated data service
│   └── ...
│
├── infrastructure/                # AI-generated infrastructure
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   ├── .env
│   └── Makefile
│
├── nginx/                         # AI-generated API Gateway configs
│   └── conf.d/
│
├── .github/                       # AI-generated CI/CD
│   └── workflows/
│
└── README.md                      # Your project README
```

**Service structure:** DDD/Hexagonal with `domain/`, `application/`, `infrastructure/`, `api/` layers — See [Project Structure](docs/reference/project-structure.md)

---

## Documentation

**For AI Agents:** Start with [AGENTS.md](AGENTS.md) → [AI Workflow](docs/guides/ai-code-generation-master-workflow.md) → [Maturity Levels](docs/reference/maturity-levels.md)

**For Developers:** [Architecture Guide](docs/guides/architecture-guide.md) • [Tech Stack](docs/reference/tech_stack.md) • [Development Commands](docs/guides/development-commands.md)

**Full Index:** [docs/INDEX.md](docs/INDEX.md) — 135+ atomic modules on architecture, services, infrastructure, observability, testing, security

---

## Technology Stack

| Category | Technologies |
|----------|-------------|
| **Core** | Python 3.12+, FastAPI 0.115+, Aiogram 3.13+, Pydantic, AsyncIO |
| **Data** | PostgreSQL 16+, MongoDB 7+, Redis 7+, SQLAlchemy 2.0+, Alembic |
| **Infrastructure** | Docker 24+, Nginx 1.27+, RabbitMQ 3.13+, Docker Compose 2.20+ |
| **Observability** | Prometheus, Grafana, Jaeger, ELK Stack, Sentry |
| **Quality** | pytest 8.3+, mypy 1.11+, Ruff 0.6+, Testcontainers |
| **CI/CD** | GitHub Actions, Makefile |

See [Technical Specifications](docs/reference/tech_stack.md) for versions and configuration details.

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Priority areas:** Service templates, documentation, infrastructure (K8s, Terraform), testing patterns

**Issues:** [GitHub Issues](https://github.com/bgs2509/ai-generator-asyncmicroservices/issues)

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🏷️ GitHub Topics

When setting up your repository, add these topics for better discoverability:

```
python fastapi microservices async docker ai code-generator framework postgresql rabbitmq redis mongodb hexagonal-architecture ddd asyncio api-gateway nginx aiogram pydantic sqlalchemy
```

**Copy-paste ready:**
```
python, fastapi, microservices, async, docker, ai, code-generator, framework, postgresql, rabbitmq, redis, mongodb, hexagonal-architecture, ddd, asyncio, api-gateway, nginx, aiogram, pydantic, sqlalchemy
```

---

**Made with ❤️ for developers who value consistency, quality, and automation.**

**Version**: 0.1.0 • **Status**: Active Development • **Updated**: 2025-01-05
