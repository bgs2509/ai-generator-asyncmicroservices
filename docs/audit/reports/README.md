# Audit Reports

This directory contains completed documentation audit reports with findings and recommendations.

## Purpose

Audit reports document the results of systematic documentation reviews. They track issues found, prioritize fixes, and provide actionable remediation steps.

## Naming Convention

Reports follow the format: `YYYY-MM-{descriptive-name}.md`

**Examples:**
- `2025-12-documentation-issues.md`
- `2025-01-link-validation.md`
- `2024-10-architecture-review.md`

## Report Index

| Date | Report | Status | Issues | Resolution |
|------|--------|--------|--------|------------|
| 2025-12-18 | [documentation-issues TODO](../todo/2025-12-18-documentation-issues-todo.md) | ✅ Completed | 8 (resolved) | All issues fixed |
| 2025-12-18 | [link-validation TODO](../todo/2025-12-18-link-validation-todo.md) | ✅ Completed | 12 fixed | All verified |

## Report Structure

Each report follows a standard format:

```markdown
# Documentation Audit Report: {Title}

## Executive Summary
- Overall health score
- Issue count by severity
- Top critical findings

## Issue Inventory
| ID | Priority | Category | Status |
|----|----------|----------|--------|
| ISS-001 | P0 | Broken Link | Open |

## Detailed Issue Reports
### ISS-001: {Issue Title}
- Problem Description
- Current State
- Expected State
- Impact Analysis
- Solution Steps
- Affected Files

## Implementation Roadmap
- Phase 1: Critical fixes
- Phase 2: High priority
- Phase 3: Medium/Low priority
```

## Issue Severity Levels

| Level | Label | Description | Response Time |
|-------|-------|-------------|---------------|
| P0 | CRITICAL | Blocks core functionality | Immediate |
| P1 | HIGH | Significant impact on workflow | High priority |
| P2 | MEDIUM | Quality/consistency issues | Normal priority |
| P3 | LOW | Minor improvements | When convenient |

## Creating a New Report

1. Conduct audit using templates from `docs/audit/templates/`
2. Create new file: `YYYY-MM-{descriptive-name}.md`
3. Follow the standard report structure
4. Add entry to the Report Index table above
5. Submit PR with report

## Related Documents

- [Audit Templates](../templates/README.md) — How to conduct audits
- [Audit Directory](../README.md) — Audit process overview
- [Contributing Guide](../../contributing/README.md) — Contribution workflow
