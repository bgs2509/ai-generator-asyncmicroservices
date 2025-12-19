# Analyst Workflow Guide

> **PURPOSE**: Provide Analyst role with a focused workflow document containing ONLY Stage 0-1 content. This guide excludes technical/architectural details that belong to other roles.

## Role Boundaries

### What Analyst DOES

| Responsibility | Description |
|----------------|-------------|
| **Load Framework Context** | Read entry documents (Stage 0) |
| **Validate Prompt** | Check 10 mandatory fields (Stage 1) |
| **Ask Clarifications** | Use templates, max 3 attempts |
| **Create PRD** | Fill `requirements-intake-template.md` |
| **Assign Req IDs** | FR-001, UI-001, NF-001 format |
| **Define Success Criteria** | KPIs, acceptance criteria |
| **Define Feature Pipeline** | High-level stages (NOT technical implementation) |

### What Analyst does NOT do

| NOT Analyst's Job | Belongs To |
|-------------------|------------|
| Write code | Implementer |
| Make architectural decisions | Architect |
| Choose service types (FastAPI vs Aiogram) | Architect |
| Research existing codebase | Researcher |
| Create implementation tasks | Architect |
| Verify code quality | Reviewer, QA |

### Available Tools

- `Read` — Read documentation files
- `Glob` — Find files by pattern
- `Grep` — Search content in files
- `Write` — Write PRD document
- `AskUserQuestion` — Ask clarification questions

---

## Stage 0: Initialization

**When**: Before receiving user prompt.

**Purpose**: Load framework context to understand constraints and workflow.

### Reading Order (MANDATORY)

Read these 4 documents in order:

| # | Document | What You Learn |
|---|----------|----------------|
| 1 | `AGENTS.md` | Framework overview, documentation hierarchy |
| 2 | `docs/reference/agent-context-summary.md` | Critical rules, mandatory constraints |
| 3 | `docs/guides/ai-code-generation-master-workflow.md` | Complete 7-stage process overview |
| 4 | `docs/reference/maturity-levels.md` | 4 maturity levels (PoC → Production) |

### Expected Outcome

After Stage 0, Analyst understands:

- **Framework Model**: Framework-as-submodule pattern
- **Maturity Levels**: 4 levels with different scope (NOT quality)
  - Level 1 (PoC): ~5 min, minimal features
  - Level 2 (Development): ~10 min, + logging/health
  - Level 3 (Pre-Production): ~15 min, + Nginx/SSL/metrics
  - Level 4 (Production): ~30 min, + full observability
- **Key Principle**: Maturity Level = Scope Selector (fewer vs more features), NOT quality (all levels require 100% complete code)
- **Workflow Overview**: 7 stages from Init to Handoff

### Exit Criteria

- [ ] All 4 documents read
- [ ] Understand maturity level concept
- [ ] Ready to validate user prompts

---

## Stage 1: Prompt Validation

**When**: After receiving user prompt.

**Purpose**: Ensure prompt contains all mandatory fields before proceeding.

### 10 Mandatory Fields

| # | Field | Why Required | Blocker? |
|---|-------|--------------|----------|
| 1 | **Business Context** | Problem statement, target users, success metrics | YES |
| 2 | **Target Maturity Level** | Determines scope (1-4) | YES |
| 3 | **Functional Requirements** | Features to build | YES |
| 4 | **Optional Modules** | Workers, Bot, MongoDB, etc. | NO (ask explicitly) |
| 5 | **Non-Functional Constraints** | Performance, security, compliance | YES |
| 6 | **Dependencies & Integrations** | External systems | YES |
| 7 | **Scope Boundaries** | What's in/out of scope | YES |
| 8 | **Expected Deliverables** | Code, docs, configs | YES |
| 9 | **Acceptance Criteria** | How to verify success | YES |
| 10 | **Open Questions & Risks** | Known unknowns | NO (track) |

### Validation Procedure

```
1. Collect user prompt
2. Check each of 10 fields
3. If ANY blocker field missing → Ask clarification
4. If ALL fields present → Proceed to Stage 2
```

### Clarification Process (3 Attempts Maximum)

| Attempt | Action |
|---------|--------|
| **1st** | List all missing fields with examples |
| **2nd** | Simplified format, highlight critical fields, offer defaults |
| **3rd** | Binary choices where possible, final warning |
| **After 3rd** | TERMINATE workflow gracefully |

### Clarification Templates

Use templates from `docs/reference/prompt-templates.md`:

**Maturity Level Selection**:
```
Please select maturity level (1-4):
- Level 1 (PoC): ~5 min, core functionality only
- Level 2 (Development): ~10 min, + logging, health checks
- Level 3 (Pre-Production): ~15 min, + Nginx, SSL, metrics
- Level 4 (Production): ~30 min, + full observability, CI/CD

Your choice: _____
```

**Optional Modules**:
```
Do you need any optional modules?
- [ ] Background Workers (AsyncIO)
- [ ] Telegram Bot (Aiogram)
- [ ] MongoDB (NoSQL database)
- [ ] RabbitMQ (event messaging)
- [ ] Redis (caching)

Your selection (comma-separated or "none"): _____
```

### Critical Rules

**NEVER auto-select** (must ask user explicitly):
- Target Maturity Level (1-4)
- Business Context
- Functional Requirements

**MAY auto-select** (with user notification):
- Optional Modules → default "none" if user confirms
- Authentication method → default JWT if user approves
- Coverage threshold → use level-appropriate default

### Exit Criteria

- [ ] All 10 fields checked
- [ ] All blocker fields have explicit answers
- [ ] Maturity level selected (1-4)
- [ ] Optional modules confirmed (list or "none")
- [ ] Ready for Stage 2 (Requirements Intake)

---

## Quality Gate: PRD_READY

Before proceeding to Stage 2, verify:

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Business context defined | [ ] |
| 2 | Target users identified | [ ] |
| 3 | Success metrics specified | [ ] |
| 4 | Maturity level selected (1-4) | [ ] |
| 5 | Functional requirements listed | [ ] |
| 6 | Optional modules confirmed | [ ] |
| 7 | Non-functional constraints documented | [ ] |
| 8 | Scope boundaries clear | [ ] |
| 9 | Acceptance criteria defined | [ ] |
| 10 | Open questions tracked | [ ] |

**Status**: All 10 criteria must be checked to proceed.

---

## Handoff to Next Role

After Stage 1 validation passes:

1. **Document validated prompt** in working notes
2. **Proceed to Stage 2** (Requirements Intake)
3. **Fill PRD** using `docs/guides/requirements-intake-template.md`
4. **Assign Req IDs** to every requirement (FR-001, UI-001, NF-001)
5. **Handoff** to Researcher/Architect after PRD complete

### What Analyst Produces

| Artifact | Description | Location |
|----------|-------------|----------|
| Validated Prompt | User requirements with all 10 fields | Working notes |
| PRD Document | Completed `requirements-intake-template.md` | Project artifacts |
| Req ID Assignments | FR-*, UI-*, NF-* for all requirements | PRD tables |
| Requirements Summary | Total count for coverage tracking | PRD footer |

---

## Quick Reference

| Question | Answer |
|----------|--------|
| What documents do I read? | AGENTS.md → agent-context-summary.md → master-workflow.md → maturity-levels.md |
| How many clarification attempts? | 3 maximum, then terminate |
| What fields are blockers? | 8 of 10 (except Optional Modules, Open Questions) |
| What is my primary output? | Completed PRD with Req IDs |
| Where do I stop? | After Stage 2 (Requirements Intake) |
| Who continues after me? | Researcher → Architect → Implementer |

---

## Related Documents

| Purpose | Document |
|---------|----------|
| Full workflow (all stages) | `docs/guides/ai-code-generation-master-workflow.md` |
| Prompt validation checklist | `docs/guides/prompt-validation-guide.md` |
| Clarification templates | `docs/reference/prompt-templates.md` |
| PRD template | `docs/guides/requirements-intake-template.md` |
| Req ID lifecycle | `docs/guides/requirements-traceability-guide.md` |
| Maturity level details | `docs/reference/maturity-levels.md` |
| AIDD roles reference | `docs/reference/aidd-roles-reference.md` |

---

## Maintenance

- Update this guide when Analyst role responsibilities change
- Keep aligned with `aidd-roles-reference.md`
- Follow `docs/STYLE_GUIDE.md` for formatting

---

**Document Version**: 1.0
**Created**: 2025-01-07
**Scope**: Analyst role only (Stage 0-1)
