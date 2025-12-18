# Audit Templates

This directory contains reusable templates and checklists for conducting documentation audits.

## Purpose

Templates help AI agents and human contributors conduct consistent, thorough audits of the framework documentation. Each template provides structured guidance for specific audit types.

## Available Templates

| Template | Purpose | Use When |
|----------|---------|----------|
| [comprehensive-audit.md](./comprehensive-audit.md) | Full 17-objective documentation audit | Major releases, quarterly reviews |
| [link-validation-checklist.md](./link-validation-checklist.md) | Link and facts verification | Quick validation, PR reviews |

## Template Selection Guide

```
                    ┌─────────────────────┐
                    │  What type of audit │
                    │     is needed?      │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │ Full Review │    │ Link Check  │    │ Custom Audit│
    │ (quarterly) │    │ (per PR)    │    │ (specific)  │
    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
           │                  │                   │
           ▼                  ▼                   ▼
    comprehensive-     link-validation-     Create new
    audit.md           checklist.md         template
```

## How to Use Templates

### For AI Agents

1. Read the template completely before starting
2. Follow the **Execution Protocol** section if present
3. Run **Smoke Tests** first (5 minutes) to assess scope
4. Execute validation commands sequentially
5. Document findings in `docs/audit/reports/` directory

### For Human Contributors

1. Copy template sections relevant to your audit scope
2. Execute commands manually or via scripts
3. Record results in the Evidence column
4. Submit findings as PR or issue

## Creating New Templates

When creating a new audit template:

1. Follow the structure of existing templates
2. Include:
   - Purpose and scope
   - Prerequisites
   - Step-by-step instructions
   - Validation commands with expected output
   - Reporting format
3. Add entry to the table above
4. Test template before committing

## Related Documents

- [Audit Reports](../reports/README.md) — Completed audit findings
- [Audit Directory](../README.md) — Audit process overview
- [docs/STYLE_GUIDE.md](../../STYLE_GUIDE.md) — Documentation standards
