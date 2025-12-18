# Quality Assurance

This directory contains QA templates and verification checklists for the AI code generation workflow.

## Purpose

Quality assurance ensures generated code meets framework standards. These documents support **Stage 5 (Quality Verification)** and **Stage 6 (QA Report & Handoff)** of the [AI Code Generation Workflow](../guides/ai-code-generation-master-workflow.md).

## Contents

| Document | Purpose | Used In |
|----------|---------|---------|
| [agent-verification-checklist.md](./agent-verification-checklist.md) | Mandatory quality gates before delivery | Stage 5 |
| [qa-report-template.md](./qa-report-template.md) | Final QA report structure | Stage 6 |
| [automated-quality-gates.md](./automated-quality-gates.md) | CI/CD quality enforcement | All stages |

## Workflow Integration

```
Stage 4: Implementation
         │
         ▼
┌─────────────────────────────────────┐
│      Stage 5: Quality Verification   │
│  ┌─────────────────────────────────┐ │
│  │  agent-verification-checklist   │ │
│  │  • Static analysis (Ruff, Mypy) │ │
│  │  • Testing (pytest, coverage)   │ │
│  │  • Security scan (Bandit)       │ │
│  │  • Requirements traceability    │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│       Stage 6: QA Report & Handoff   │
│  ┌─────────────────────────────────┐ │
│  │     qa-report-template          │ │
│  │  • Summary of findings          │ │
│  │  • Coverage metrics             │ │
│  │  • Known issues & risks         │ │
│  │  • Deliverables list            │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
         │
         ▼
Stage 7: Documentation & Archive
```

## Quality Thresholds by Maturity Level

Coverage thresholds are defined in [maturity-levels.md](../reference/maturity-levels.md) (Single Source of Truth):

| Level | Name | Coverage Threshold |
|-------|------|-------------------|
| 1 | PoC/MVP | ≥ 60% |
| 2 | Development | ≥ 75% |
| 3 | Pre-Production | ≥ 80% |
| 4 | Production | ≥ 85% |

## CI/CD Integration

The [automated-quality-gates.md](./automated-quality-gates.md) document describes:

- **check-duplication** — DRY enforcement via jscpd (≤10% threshold)
- **check-complexity** — KISS enforcement via radon (Grade B or better)
- **check-dependencies** — YAGNI enforcement (30/50 dependency limit)

These gates run automatically on every PR.

## Related Documents

- [AI Code Generation Workflow](../guides/ai-code-generation-master-workflow.md) — 7-stage workflow
- [Maturity Levels](../reference/maturity-levels.md) — Quality thresholds per level
- [Development Commands](../guides/development-commands.md) — QA command reference
- [Troubleshooting](../reference/troubleshooting.md) — Fixing QA failures
