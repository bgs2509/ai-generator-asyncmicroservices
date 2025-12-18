# Documentation Audit Directory

This directory contains audit reports and quality assessments of the project documentation.

## Purpose

The audit process ensures:
- Documentation completeness and accuracy
- Cross-reference integrity
- Template availability for AI code generation
- Workflow execution capability

## Audit Report Format

Each audit report follows this structure:

| Section | Purpose |
|---------|---------|
| Executive Summary | Quick overview of findings |
| Issue Inventory | Tabular list of all issues |
| Detailed Issue Reports | Full analysis per issue |
| Implementation Roadmap | Prioritized fix plan |
| Appendix | File inventories, matrices |

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

## Audit Reports

| Date | Report | Status | Issues Found |
|------|--------|--------|--------------|
| 2025-12-18 | [Documentation Issues Report](./2025_12_18_documentation-issues-report.md) | Active | 8 (3 P0, 2 P1, 2 P2, 1 P3) |

## Running an Audit

To conduct a documentation audit:

1. Use the Explore agent to analyze all documentation
2. Cross-reference templates with documentation
3. Verify workflow stages have supporting files
4. Check cross-reference integrity
5. Document findings using the standard format
6. Prioritize by impact on AI code generation workflow

## Related Documents

- `docs/INDEX.md` — Master documentation index
- `docs/guides/ai-code-generation-master-workflow.md` — 7-stage workflow
- `templates/README.md` — Template status and inventory
