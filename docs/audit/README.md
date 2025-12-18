# Documentation Audit Directory

This directory contains audit resources for maintaining documentation quality.

## Directory Structure

```
audit/
├── README.md              # This file - audit process overview
├── templates/             # Reusable audit templates
│   ├── README.md          # Template usage guide
│   └── comprehensive-audit.md    # Full 17-objective audit
├── reports/               # Completed audit findings
│   └── README.md          # Report index and format
└── todo/                  # Pending tasks and work-in-progress
    ├── README.md          # TODO index
    └── *.md               # Individual TODO files
```

> **Note**: TODO items are tracked in [todo/](./todo/README.md).

## Purpose

The audit process ensures:
- Documentation completeness and accuracy
- Cross-reference integrity
- Template availability for AI code generation
- Workflow execution capability

## Quick Start

| I want to... | Go to |
|--------------|-------|
| Conduct a full audit | [templates/comprehensive-audit.md](./templates/comprehensive-audit.md) |
| View past findings | [reports/](./reports/README.md) |
| View pending tasks | [todo/](./todo/README.md) |

## Issue Severity Levels

| Level | Label | Description | Response Time |
|-------|-------|-------------|---------------|
| P0 | CRITICAL | Blocks core functionality | Immediate |
| P1 | HIGH | Significant impact on workflow | High priority |
| P2 | MEDIUM | Quality/consistency issues | Normal priority |
| P3 | LOW | Minor improvements | When convenient |

## Issue Report Structure

Each issue (ISS-XXX) includes:

1. **Problem Description** — What is wrong
2. **Current State** — Example showing the problem
3. **Expected State** — Example showing the solution
4. **Impact Analysis** — Consequences of the issue
5. **Solution Steps** — How to fix it
6. **Affected Files** — Files to create/update
7. **Related Issues** — Connected problems

## Running an Audit

To conduct a documentation audit:

1. Choose appropriate template from `templates/`
2. Follow the Execution Protocol in the template
3. Run Smoke Tests first (5 minutes)
4. Execute validation commands sequentially
5. Document findings in `reports/` directory
6. Prioritize by impact on AI code generation workflow

## Related Documents

- [docs/INDEX.md](../INDEX.md) — Master documentation index
- [docs/guides/ai-code-generation-master-workflow.md](../guides/ai-code-generation-master-workflow.md) — 7-stage workflow
- [templates/README.md](../../templates/README.md) — Template status and inventory
- [docs/contributing/README.md](../contributing/README.md) — Contributing guide
