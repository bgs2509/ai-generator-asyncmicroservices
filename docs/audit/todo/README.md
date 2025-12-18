# TODO Files

This directory contains pending tasks and work-in-progress items for the project.

## Current TODOs

| File | Description | Created | Status |
|------|-------------|---------|--------|
| [2025-12-18-documentation-issues-todo.md](./2025-12-18-documentation-issues-todo.md) | Documentation issues requiring fixes | 2025-12-18 | ✅ Completed |
| [2025-12-18-link-validation-todo.md](./2025-12-18-link-validation-todo.md) | Link and fact verification plan | 2025-12-18 | ✅ Completed |

---

## Style Guide for TODO Files

### File Naming Convention

```
YYYY-MM-DD-{descriptive-name}-todo.md
```

**Rules:**

- Use lowercase with hyphens (kebab-case)
- Date prefix ensures chronological sorting
- Suffix `-todo` distinguishes from other document types
- Name should be concise but descriptive (3-5 words max)

**Examples:**

- ✅ `2025-12-18-api-refactoring-todo.md`
- ✅ `2025-12-20-security-audit-todo.md`
- ❌ `todo.md` (no date, not descriptive)
- ❌ `2025-12-18-TODO-FOR-FIXING-ALL-THE-BUGS.md` (too long, uppercase)

### Priority Levels

| Priority | Label | Use Case |
|----------|-------|----------|
| 🔴 P0 | Critical | Blocking issues, security vulnerabilities |
| 🟠 P1 | High | Important features, significant bugs |
| 🟡 P2 | Medium | Standard tasks, improvements |
| 🟢 P3 | Low | Nice-to-have, minor enhancements |

### Status Labels

| Status | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Completed |
| `[!]` | Blocked |
| `[-]` | Cancelled/Won't fix |

---

## TODO File Templates

Choose the template based on your TODO type:

| Template | Use Case |
|----------|----------|
| **Basic** | Simple task lists, quick fixes |
| **Issue-Based** | Bug tracking, documentation issues, technical debt |
| **Audit-Based** | Verification tasks, link checks, compliance audits |

---

### Basic Template

For simple task tracking (< 10 items):

```markdown
> **TODO FILE** — This document contains pending tasks.

# {Title} TODO

> **Created:** YYYY-MM-DD
> **Author:** {name}
> **Priority:** 🟡 P2
> **Status:** 🟡 In Progress

## Overview

Brief description: what this TODO covers and why it exists.
One paragraph, 2-3 sentences maximum.

## Scope

**In Scope:**
- Item 1
- Item 2

**Out of Scope:**
- Item 1

## Tasks

### Category 1

- [ ] Task description — brief context
- [ ] Another task — why it matters

### Category 2

- [ ] Task with subtasks
  - [ ] Subtask A
  - [ ] Subtask B

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Notes

Additional context, decisions, or blockers.

## Related

- [Link to related doc](./path.md)
- Issue #123
```

---

### Issue-Based Template

For tracking bugs, documentation issues, or technical debt:

```markdown
> **TODO FILE** — This document contains pending tasks.

# {Title} — YYYY-MM-DD

## Executive Summary

Brief problem description and key metrics.

### Key Findings

| Metric | Value |
|--------|-------|
| Total Issues Found | X |
| Critical (P0) | X |
| High (P1) | X |
| Medium (P2) | X |
| Low (P3) | X |

### Root Cause

One-sentence root cause analysis.

### Critical Path

```
Step 1: ✅ WORKS
Step 2: ❌ BLOCKED
Step 3: ⚠️ PARTIAL
```

---

## Issue Inventory

| ID | Severity | Category | Issue | Status |
|----|----------|----------|-------|--------|
| ISS-001 | P0 | {category} | Brief description | Open |
| ISS-002 | P1 | {category} | Brief description | Open |

---

## Detailed Issue Reports

### ISS-001: {Title} (P0 — CRITICAL)

#### Problem Description

What is wrong and where it occurs.

#### Current State

```bash
# What happens now (error example)
```

#### Expected State

```bash
# What should happen (correct example)
```

#### Impact Analysis

| Impact Area | Description |
|-------------|-------------|
| **Area 1** | Impact description |
| **Area 2** | Impact description |

#### Solution Steps

1. Step one
2. Step two
3. Step three

#### Affected Files

| Action | File Path |
|--------|-----------|
| CREATE | `path/to/new/file.ext` |
| UPDATE | `path/to/existing/file.ext` |

#### Related Issues

- ISS-002 — Related problem
- ISS-003 — Dependency

---

## Implementation Roadmap

### Phase 1: {Name}

**Goal**: What this phase achieves.

| # | Task | Files | Priority |
|---|------|-------|----------|
| 1 | Task description | ~X files | P0 |
| 2 | Task description | X file | P1 |

### Phase 2: {Name}

| # | Task | Files | Priority |
|---|------|-------|----------|
| 3 | Task description | ~X files | P2 |

---

## Verification Checklist

After implementing fixes, verify:

- [ ] Verification item 1
- [ ] Verification item 2
- [ ] Verification item 3

---

## Related Documents

- `path/to/doc1.md` — Description
- `path/to/doc2.md` — Description
```

---

### Audit-Based Template

For verification tasks, link checks, and compliance audits:

```markdown
> **TODO FILE** — This document contains pending tasks.

# {Audit Name} — YYYY-MM-DD

> **Created**: YYYY-MM-DD
> **Status**: Pending
> **Scope**: X files across Y directories
> **Estimated effort**: X-Y hours

---

## Executive Summary

What this audit verifies and why it matters.

---

## Scope Analysis

### File Distribution

| Location | Files | Priority |
|----------|-------|----------|
| `path/` | X | 🔴 Critical |
| `path/` | X | 🟠 High |
| `path/` | X | 🟡 Medium |
| `path/` | X | 🟢 Low |
| **Total** | **X** | — |

### Verification Types

1. **Type 1**: Description
2. **Type 2**: Description
3. **Type 3**: Description

---

## Phase 1: {Name}

**Priority**: 🔴 CRITICAL
**Estimated time**: X hours

| # | File | Verification Tasks |
|---|------|-------------------|
| 1.1 | `path/file.md` | [ ] Task 1, [ ] Task 2 |
| 1.2 | `path/file.md` | [ ] Task 1, [ ] Task 2 |

---

## Phase 2: {Name}

**Priority**: 🟠 HIGH
**Estimated time**: X hours

| # | File | Verification Tasks |
|---|------|-------------------|
| 2.1 | `path/file.md` | [ ] Task 1 |
| 2.2 | `path/file.md` | [ ] Task 1 |

---

## Verification Commands

```bash
#!/bin/bash
# Command description

command --with --flags
```

---

## Success Criteria

### Quality Gates

- [ ] **Gate 1** — Description
- [ ] **Gate 2** — Description
- [ ] **Gate 3** — Description

---

## Issue Tracking

### Issue Template

```markdown
### [PHASE.TASK] Brief Description

**File**: `path/to/file.md`
**Line**: XX
**Type**: {Type}
**Severity**: {Severity}

**Current**:
What it says now

**Expected**:
What it should say

**Fix Applied**: [ ] Yes / [ ] No
```

### Issue Log

| ID | File | Type | Severity | Status |
|----|------|------|----------|--------|
| 1.1-001 | file.md | Type | Medium | ✅ Fixed |

---

## Execution Schedule

| Day | Phases | Focus |
|-----|--------|-------|
| Day 1 | 1 | Critical path |
| Day 2 | 2 | Secondary items |

---

## Post-Audit Actions

1. Update related documentation
2. Create summary report
3. Archive this TODO

---

## Related Documents

- `path/to/doc.md` — Description
```

---

## Template Sections Reference

### Basic Template Sections

| Section | Required | Description |
|---------|----------|-------------|
| **File Marker** | ✅ | `> **TODO FILE** — ...` identifies file type |
| **Title + Metadata** | ✅ | Date, author, priority, status at a glance |
| **Overview** | ✅ | Why this TODO exists; context for readers |
| **Scope** | ⚪ | Clarifies boundaries; prevents scope creep |
| **Tasks** | ✅ | Actionable items with checkboxes |
| **Acceptance Criteria** | ⚪ | Definition of "done" |
| **Notes** | ⚪ | Decisions, blockers, context |
| **Related** | ⚪ | Links to issues, PRs, docs |

### Issue-Based Template Sections

| Section | Required | Description |
|---------|----------|-------------|
| **Executive Summary** | ✅ | Key metrics, root cause, critical path |
| **Issue Inventory** | ✅ | Table: ID, Severity, Category, Status |
| **Detailed Reports** | ✅ | Per-issue: Problem, Current/Expected, Impact, Solution |
| **Affected Files** | ✅ | CREATE/UPDATE tables per issue |
| **Implementation Roadmap** | ⚪ | Phased approach for large fixes |
| **Verification Checklist** | ✅ | Post-fix validation items |

### Audit-Based Template Sections

| Section | Required | Description |
|---------|----------|-------------|
| **Scope Analysis** | ✅ | File counts, priority distribution |
| **Phased Tasks** | ✅ | Verification tasks grouped by priority |
| **Verification Commands** | ⚪ | Bash scripts for automated checks |
| **Success Criteria** | ✅ | Quality gates that must pass |
| **Issue Template** | ⚪ | Standard format for logging issues |
| **Issue Log** | ⚪ | Running table of found issues |
| **Execution Schedule** | ⚪ | Day-by-day plan |
| **Post-Audit Actions** | ⚪ | What to do after completion |

---

## Best Practices

1. **One TODO per concern** — Don't mix unrelated tasks in one file
2. **Atomic tasks** — Each checkbox should be completable independently
3. **Update status** — Mark items as you progress; don't let files go stale
4. **Archive completed TODOs** — Move to `../completed/` when done
5. **Link context** — Reference related files, issues, or discussions
6. **Time-box large tasks** — Break into smaller TODOs if > 20 items

---

## Related Documents

- [Audit Directory](../README.md) — Audit templates and completed reports
- [Contributing Guide](../../contributing/README.md) — Contribution guidelines
- [Style Guide](../../STYLE_GUIDE.md) — General documentation standards
