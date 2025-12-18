# Feature Proposals

This directory contains proposals for new framework capabilities.

## Purpose

Feature proposals document requests for significant new functionality. They help coordinate discussion, design decisions, and implementation planning for major additions.

## When to Use Feature Proposals

**Use a feature proposal for:**

- New service types (e.g., gRPC services, GraphQL APIs)
- New integrations (e.g., Apache Kafka, Elasticsearch)
- New maturity levels or architectural patterns
- Major documentation additions
- New workflow stages or capabilities

**Skip feature proposal for:**

- Bug fixes — use GitHub Issues
- Small improvements — use direct PR
- Multi-phase changes — use [Improvement Plans](../improvement-plans/README.md)

## Proposal Template

Create a new file: `YYYY-MM-{feature-name}.md`

```markdown
# Feature Proposal: {Feature Name}

> **Status**: Draft | Under Review | Approved | Rejected | Implemented
> **Author**: {Name}
> **Created**: {Date}
> **Updated**: {Date}

## Summary

One paragraph describing the proposed feature.

## Motivation

Why is this feature needed? What problem does it solve?

## Proposed Solution

### High-Level Design

Describe the approach at a conceptual level.

### Technical Details

- Architecture changes
- New files/directories
- Dependencies added
- Impact on existing code

### Alternatives Considered

What other approaches were considered? Why was this approach chosen?

## Scope

### In Scope

- Feature A
- Feature B

### Out of Scope

- Feature C (defer to future proposal)

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Implementation Plan

1. Phase 1: {Description}
2. Phase 2: {Description}
3. Phase 3: {Description}

## Related Documents

- Link to related docs
- Link to related issues
```

## Workflow

1. **Draft** — Author creates proposal document
2. **Submit PR** — Proposal only (no implementation code)
3. **Review** — Maintainers and community provide feedback
4. **Revise** — Author updates based on feedback
5. **Approve/Reject** — Maintainer decision with rationale
6. **Implement** — If approved, follow normal contribution process

## Current Proposals

| Date | Proposal | Status | Author |
|------|----------|--------|--------|
| — | No active proposals | — | — |

## Related Documents

- [Contributing Guide](../README.md) — Contribution overview
- [Improvement Plans](../improvement-plans/README.md) — Multi-phase changes
- [Refactoring Plans](../refactoring-plans/README.md) — Architectural changes
