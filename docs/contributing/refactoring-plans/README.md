# Refactoring Plans

This directory contains coordination documents for significant architectural refactorings.

## Purpose

Refactoring plans help coordinate breaking changes, deprecations, and major restructuring that affects multiple parts of the framework.

## When to Use Refactoring Plans

**Use a refactoring plan for:**

- Breaking changes to templates or workflows
- Deprecating old patterns
- Major documentation restructuring
- Changing naming conventions
- Large-scale code reorganization

**Skip refactoring plan for:**

- Bug fixes — use GitHub Issues
- Small improvements — use direct PR
- New features — use [Feature Proposals](../feature-proposals/README.md)
- Non-breaking enhancements — use [Improvement Plans](../improvement-plans/README.md)

## Refactoring Plan Template

Create a new file: `YYYY-MM-{refactoring-name}.md`

```markdown
# Refactoring Plan: {Refactoring Name}

> **Status**: Draft | Under Review | Approved | In Progress | Completed
> **Author**: {Name}
> **Created**: {Date}
> **Target Completion**: {Date}

## Summary

One paragraph describing the refactoring and its impact.

## Motivation

Why is this refactoring needed? What technical debt or issues does it address?

## Breaking Changes

### Affected Components

| Component | Current State | New State | Migration Required |
|-----------|--------------|-----------|-------------------|
| {Name} | {Description} | {Description} | Yes/No |

### Migration Guide

Step-by-step instructions for users to migrate from old to new patterns.

## Implementation Phases

### Phase 1: Preparation

- [ ] Task 1
- [ ] Task 2

### Phase 2: Implementation

- [ ] Task 3
- [ ] Task 4

### Phase 3: Cleanup

- [ ] Remove deprecated code
- [ ] Update documentation
- [ ] Announce completion

## Rollback Plan

If critical issues are discovered:

1. Step 1
2. Step 2
3. Step 3

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk} | Low/Medium/High | Low/Medium/High | {Strategy} |

## Timeline

| Phase | Start | End | Status |
|-------|-------|-----|--------|
| Phase 1 | {Date} | {Date} | Pending |
| Phase 2 | {Date} | {Date} | Pending |
| Phase 3 | {Date} | {Date} | Pending |

## Related Documents

- Link to related docs
- Link to deprecation notices
```

## Workflow

1. **Draft** — Author creates refactoring plan
2. **Submit PR** — Plan document only
3. **Review** — Extended review period (breaking changes)
4. **Announce** — Notify community of planned changes
5. **Implement** — Execute phases per plan
6. **Validate** — Verify migration success
7. **Complete** — Remove deprecated code, update docs

## Current Plans

| Date | Plan | Status | Author |
|------|------|--------|--------|
| — | No active plans | — | — |

## Related Documents

- [Contributing Guide](../README.md) — Contribution overview
- [Improvement Plans](../improvement-plans/README.md) — Non-breaking enhancements
- [Feature Proposals](../feature-proposals/README.md) — New capabilities
