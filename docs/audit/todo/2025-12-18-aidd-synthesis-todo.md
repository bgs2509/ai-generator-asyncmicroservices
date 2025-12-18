# TODO: AIDD + Framework Synthesis

> **Purpose**: Synthesize AIDD role-based approach with existing 7-stage workflow
>
> **Created**: 2025-12-18
> **Priority**: P1 - Strategic Enhancement
> **Status**: 🔄 In Progress

---

## Executive Summary

### Problem Statement

Current 7-stage workflow conflates multiple AIDD roles into single stages:
- Stage 3 combines Researcher + Architect (different cognitive modes)
- Stage 5 combines Reviewer + QA + Validator (different verification types)
- Tech Writer role is underutilized in Stage 6

### Proposed Solution

Evolve from **7-stage process** to **10-stage role-aligned workflow** that preserves existing strengths while adding AIDD's role-based clarity.

---

## Part 1: Conceptual Decision

### 1.1 Synthesis Philosophy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SYNTHESIS PHILOSOPHY                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  AIDD Contribution:           Framework Contribution:                   │
│  ──────────────────           ───────────────────────                   │
│  • Role-based thinking        • Atomic documentation (170+ docs)        │
│  • Explicit contracts         • Maturity levels (1-4)                   │
│  • Quality gates              • Requirements traceability (100%)        │
│  • Gradual adoption           • Pre-action verification (CLAUDE.md)    │
│                               • Automated checks (CI/CD)                │
│                               • Architecture constraints                │
│                                                                         │
│  SYNTHESIS = Role-Based Stages + Atomic Knowledge + Quality Gates      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Key Design Decision

**Decision**: Each stage SHALL have a PRIMARY ROLE assignment.

**Rationale**:
- Clear cognitive mode per stage
- Better prompt engineering (role-specific system prompts)
- Easier to identify gaps and responsibilities
- Matches AIDD's proven "virtual team" metaphor

### 1.3 Role-to-Stage Mapping (Proposed)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              PROPOSED 10-STAGE ROLE-ALIGNED WORKFLOW                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Stage    Role           Primary Responsibility                         │
│  ─────    ────           ──────────────────────                         │
│                                                                         │
│  0        [System]       Context loading (not a role)                   │
│                                                                         │
│  1        Analyst        Prompt validation, completeness check          │
│  2        Analyst        Requirements intake, Req ID assignment         │
│                                                                         │
│  3        Researcher     Codebase exploration, constraints mapping      │
│  4        Architect      Solution design, ADR creation, RTM             │
│                                                                         │
│  5        Implementer    Code generation (phases 1-6)                   │
│                                                                         │
│  6        Reviewer       Code review, architecture compliance           │
│  7        QA             Testing (unit, integration, e2e)               │
│  8        Validator      Quality gates (ruff, mypy, bandit, coverage)   │
│                                                                         │
│  9        Tech Writer    Documentation, README, API docs                │
│  10       [Handoff]      QA Report, deliverables summary                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Part 2: Detailed Stage Changes

### 2.1 Stages to KEEP (no changes)

- [ ] **Stage 0: Init** — System preparation, context loading
  - No role assignment (system function)
  - Keep as-is

- [ ] **Stage 1: Prompt Validation** — Analyst role
  - Already well-defined
  - Maps cleanly to Analyst

- [ ] **Stage 2: Requirements Intake** — Analyst role
  - Already well-defined
  - Maps cleanly to Analyst

### 2.2 Stages to SPLIT

#### Stage 3: Planning → Stage 3 (Research) + Stage 4 (Architecture)

- [ ] **NEW Stage 3: Research** — Researcher role
  - **Purpose**: Explore existing codebase, identify constraints
  - **Inputs**: Requirements Intake from Stage 2
  - **Activities**:
    - Scan project structure
    - Identify existing patterns
    - Map technology constraints
    - Document integration points
  - **Outputs**: Research Report (constraints, patterns, risks)
  - **Documents to read**: `atomic/architecture/*`, `tech_stack.md`

- [ ] **NEW Stage 4: Architecture** — Architect role
  - **Purpose**: Design solution based on research
  - **Inputs**: Requirements Intake + Research Report
  - **Activities**:
    - Create Implementation Plan
    - Write ADRs (if needed)
    - Build Requirements Traceability Matrix
    - Select maturity level features
  - **Outputs**: Implementation Plan, ADR(s), RTM
  - **Documents to read**: `implementation-plan-template.md`, `maturity-levels.md`

#### Stage 5: Verification → Stage 6 (Review) + Stage 7 (QA) + Stage 8 (Validator)

- [ ] **NEW Stage 6: Code Review** — Reviewer role
  - **Purpose**: Verify code matches architecture decisions
  - **Inputs**: Generated code from Stage 5
  - **Activities**:
    - Check DDD/Hexagonal layer separation
    - Verify HTTP-only data access pattern
    - Check naming conventions
    - Review service boundaries
  - **Outputs**: Review Report (findings, recommendations)
  - **Gate**: All architectural violations resolved

- [ ] **NEW Stage 7: Testing** — QA role
  - **Purpose**: Verify functionality through tests
  - **Inputs**: Reviewed code from Stage 6
  - **Activities**:
    - Run unit tests
    - Run integration tests
    - Run e2e tests (if applicable)
    - Generate coverage report
  - **Outputs**: Test Report, Coverage Report
  - **Gate**: Tests pass, coverage ≥ threshold

- [ ] **NEW Stage 8: Quality Gates** — Validator role
  - **Purpose**: Automated quality enforcement
  - **Inputs**: Tested code from Stage 7
  - **Activities**:
    - Run ruff (linting)
    - Run mypy (type checking)
    - Run bandit (security)
    - Check complexity (radon)
    - Check duplication (jscpd)
  - **Outputs**: Validation Report
  - **Gate**: All checks pass

### 2.3 Stages to EXPAND

#### Stage 6: QA Report → Stage 9 (Documentation) + Stage 10 (Handoff)

- [ ] **NEW Stage 9: Documentation** — Tech Writer role
  - **Purpose**: Ensure complete, high-quality documentation
  - **Inputs**: Validated code from Stage 8
  - **Activities**:
    - Generate/update README.md
    - Generate API documentation (OpenAPI)
    - Update CHANGELOG
    - Create deployment guide
    - Verify all docstrings present
  - **Outputs**: Complete documentation package
  - **Gate**: All required docs present

- [ ] **NEW Stage 10: Handoff** — (Final stage, no specific role)
  - **Purpose**: Package and deliver
  - **Inputs**: All artifacts from Stages 1-9
  - **Activities**:
    - Compile QA Report
    - Update deliverables catalog
    - Create handoff package
  - **Outputs**: QA Report, Handoff Package

---

## Part 3: Implementation Tasks

### 3.1 Documentation Updates

- [ ] **P0** Create `docs/guides/role-based-workflow.md`
  - Document 10-stage process
  - Role descriptions and responsibilities
  - Stage entry/exit criteria

- [ ] **P0** Update `docs/guides/ai-code-generation-master-workflow.md`
  - Add role assignments to each stage
  - Split Stage 3, 5, 6 as described
  - Update Navigation Matrix

- [ ] **P1** Create role-specific prompt templates
  - `docs/reference/prompts/analyst-prompts.md`
  - `docs/reference/prompts/researcher-prompts.md`
  - `docs/reference/prompts/architect-prompts.md`
  - `docs/reference/prompts/implementer-prompts.md`
  - `docs/reference/prompts/reviewer-prompts.md`
  - `docs/reference/prompts/qa-prompts.md`
  - `docs/reference/prompts/validator-prompts.md`
  - `docs/reference/prompts/techwriter-prompts.md`

- [ ] **P1** Update `docs/reference/ai-navigation-matrix.md`
  - Expand to 10 stages
  - Add role column
  - Update document mappings

- [ ] **P2** Create `docs/guides/role-switching-guide.md`
  - How to switch cognitive modes
  - Role-specific thinking patterns
  - Common mistakes per role

### 3.2 Template Updates

- [ ] **P1** Create Research Report template
  - `docs/guides/research-report-template.md`
  - Sections: Constraints, Patterns, Risks, Integration Points

- [ ] **P1** Create Code Review Report template
  - `docs/guides/code-review-report-template.md`
  - Architecture compliance checklist
  - DRY/KISS/YAGNI verification

- [ ] **P1** Create Test Report template
  - `docs/guides/test-report-template.md`
  - Unit/Integration/E2E breakdown
  - Coverage by module

- [ ] **P1** Create Validation Report template
  - `docs/guides/validation-report-template.md`
  - Gate-by-gate results
  - Pass/Fail summary

- [ ] **P2** Create Documentation Checklist
  - `docs/checklists/documentation-checklist.md`
  - Required docs per maturity level

### 3.3 Process Updates

- [ ] **P1** Define stage transitions (quality gates)
  - Stage 2 → 3: Requirements complete
  - Stage 3 → 4: Research complete
  - Stage 4 → 5: Plan approved
  - Stage 5 → 6: Code generated
  - Stage 6 → 7: Review passed
  - Stage 7 → 8: Tests passed
  - Stage 8 → 9: Validation passed
  - Stage 9 → 10: Docs complete

- [ ] **P2** Update `CLAUDE.md` with role-based pre-checks
  - Add role identification step
  - Role-specific verification rules

- [ ] **P2** Create `.claude/agents/` structure (AIDD-style)
  - `analyst.md` — Analyst role definition
  - `researcher.md` — Researcher role definition
  - `architect.md` — Architect role definition
  - `implementer.md` — Implementer role definition
  - `reviewer.md` — Reviewer role definition
  - `qa.md` — QA role definition
  - `validator.md` — Validator role definition
  - `techwriter.md` — Tech Writer role definition

### 3.4 Automation

- [ ] **P3** Create role-based hooks (AIDD Strict level)
  - Block Stage 5 if Stage 4 artifacts missing
  - Block Stage 7 if Stage 6 review not passed
  - Enforce quality gates in Stage 8

- [ ] **P3** Update CI workflow for 10-stage validation
  - Add role-specific checks
  - Stage transition validation

---

## Part 4: Migration Path

### 4.1 Gradual Adoption (AIDD-style levels)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ADOPTION LEVELS                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Level 1: MINIMAL (start here)                                          │
│  ─────────────────────────────                                          │
│  • Keep existing 7 stages                                               │
│  • Add role labels to each stage                                        │
│  • Use role-specific thinking (mental model)                            │
│  • Effort: ~2 hours                                                     │
│                                                                         │
│  Level 2: STANDARD                                                      │
│  ─────────────────                                                      │
│  • Split Stage 3 into Research + Architecture                           │
│  • Create Research Report template                                      │
│  • Effort: ~1 day                                                       │
│                                                                         │
│  Level 3: FULL                                                          │
│  ────────────                                                           │
│  • Split Stage 5 into Review + QA + Validator                           │
│  • Split Stage 6 into Documentation + Handoff                           │
│  • All templates created                                                │
│  • Effort: ~3 days                                                      │
│                                                                         │
│  Level 4: STRICT                                                        │
│  ─────────────                                                          │
│  • Role-based hooks                                                     │
│  • CI enforcement                                                       │
│  • Automated stage transitions                                          │
│  • Effort: ~1 week                                                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Recommended Sequence

1. **Week 1**: Level 1 (Minimal) — Add role labels, mental model
2. **Week 2**: Level 2 (Standard) — Split Stage 3
3. **Week 3**: Level 3 (Full) — Split Stages 5 and 6
4. **Week 4+**: Level 4 (Strict) — Automation and hooks

---

## Part 5: Success Criteria

### 5.1 Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Role clarity | 100% stages have role | Audit workflow doc |
| Stage separation | 0 stages with >1 role | Audit workflow doc |
| Template coverage | 1 template per role | Count templates |
| Gate coverage | 1 gate per transition | Audit transitions |

### 5.2 Validation

- [ ] Each stage has exactly ONE primary role
- [ ] Each role has dedicated prompt template
- [ ] Each stage has clear entry/exit criteria
- [ ] All 8 AIDD roles are represented
- [ ] Existing functionality preserved (no regression)

---

## Part 6: Open Questions

### 6.1 To Decide

- [ ] **Q1**: Should Analyst be split into two roles (Validator + Requirements)?
  - Current: One Analyst for Stages 1-2
  - Alternative: Separate validation from requirements gathering

- [ ] **Q2**: How to handle maturity levels with 10 stages?
  - Current: Some stages are conditional based on level
  - Question: Which of new stages are conditional?

- [ ] **Q3**: Should Researcher be mandatory or optional?
  - For greenfield projects: Maybe skip research
  - For existing codebases: Research is critical

### 6.2 Risks

| Risk | Mitigation |
|------|------------|
| Increased complexity (7 → 10 stages) | Gradual adoption levels |
| Longer generation time | Parallel stages where possible |
| Learning curve | Role-specific guides |
| Backward compatibility | Keep old workflow as "legacy mode" |

---

## Appendix A: Full Role Definitions (from AIDD)

### A.1 Analyst
- **Purpose**: Gather and validate requirements
- **Outputs**: PRD, Requirements Intake
- **Thinking mode**: "What does the user NEED?"

### A.2 Researcher
- **Purpose**: Explore codebase, identify constraints
- **Outputs**: Research Report
- **Thinking mode**: "What ALREADY EXISTS?"

### A.3 Architect
- **Purpose**: Design solution, make decisions
- **Outputs**: Implementation Plan, ADR
- **Thinking mode**: "How should we BUILD this?"

### A.4 Implementer
- **Purpose**: Write code
- **Outputs**: Source code
- **Thinking mode**: "How do I CODE this?"

### A.5 Reviewer
- **Purpose**: Verify architecture compliance
- **Outputs**: Review Report
- **Thinking mode**: "Does this MATCH the design?"

### A.6 QA
- **Purpose**: Test functionality
- **Outputs**: Test Report
- **Thinking mode**: "Does this WORK correctly?"

### A.7 Validator
- **Purpose**: Enforce quality gates
- **Outputs**: Validation Report
- **Thinking mode**: "Does this PASS all checks?"

### A.8 Tech Writer
- **Purpose**: Create documentation
- **Outputs**: README, API docs, guides
- **Thinking mode**: "How do I EXPLAIN this?"

---

## Appendix B: Visual Comparison

### B.1 Before (7 Stages)

```
Stage 0 ──► Stage 1 ──► Stage 2 ──► Stage 3 ──► Stage 4 ──► Stage 5 ──► Stage 6
[Init]     [Analyst]   [Analyst]   [Res+Arch]  [Impl]      [Rev+QA+Val] [TW+Hand]
                                   ❌ MIXED    ✅          ❌ MIXED     ❌ MIXED
```

### B.2 After (10 Stages)

```
Stage 0 ──► Stage 1 ──► Stage 2 ──► Stage 3 ──► Stage 4 ──► Stage 5
[Init]     [Analyst]   [Analyst]   [Researcher] [Architect] [Implementer]
                                   ✅ CLEAR     ✅ CLEAR    ✅ CLEAR

    ──► Stage 6 ──► Stage 7 ──► Stage 8 ──► Stage 9 ──► Stage 10
       [Reviewer]   [QA]        [Validator] [TechWriter] [Handoff]
       ✅ CLEAR     ✅ CLEAR    ✅ CLEAR    ✅ CLEAR     ✅ CLEAR
```

---

**Document Version**: 1.0
**Created**: 2025-12-18
**Author**: AI Synthesis Analysis
**Status**: Ready for Review
