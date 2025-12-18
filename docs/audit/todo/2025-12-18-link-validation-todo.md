> **TODO FILE** — This document contains pending tasks that need to be completed.

# Documentation Audit Plan: Links & Facts Verification

> **Created**: 2025-12-18
> **Updated**: 2025-12-18
> **Status**: ✅ COMPLETED (2025-12-18)
> **Scope**: 236 markdown files across the entire project
> **Effort**: Medium-Large (AI-assisted)
> **Prerequisite**: ✅ `2025-12-18-documentation-issues-todo.md` — COMPLETED
> **Result**: 13 issues found, 12 fixed, 1 infra note logged

---

## Executive Summary

This plan outlines a comprehensive audit of all documentation files in the ai-generator-asyncmicroservices project to verify:
1. **Link integrity** — all internal/external links resolve correctly
2. **Fact accuracy** — claims, statistics, and technical statements match reality
3. **Cross-reference consistency** — documents reference each other correctly

---

## Scope Analysis

### File Distribution

| Location | Files | Priority |
|----------|-------|----------|
| Root (`*.md`) | 9 | 🔴 Critical |
| `docs/` (top-level) | 3 | 🔴 Critical |
| `docs/guides/` | 13 | 🔴 Critical |
| `docs/reference/` | 13 | 🔴 Critical |
| `docs/atomic/` | 172 | 🟡 Medium |
| `docs/checklists/` | 2 | 🟠 High |
| `docs/quality/` | 4 | 🟠 High |
| `docs/contributing/` | 5 | 🟢 Low |
| `docs/audit/` | 7 | 🟢 Low |
| `templates/` | 7 | 🟠 High |
| **Total** | **235** | — |

### Link Types to Verify

1. **Internal file links**: `[text](path/to/file.md)`
2. **Internal anchor links**: `[text](path/to/file.md#anchor)`
3. **Same-file anchors**: `[text](#anchor)`
4. **External URLs**: `[text](https://example.com)`
5. **Image links**: `![alt](path/to/image.png)`
6. **HTML anchor tags**: `<a id="anchor-name"></a>`

### Fact Categories to Verify

1. **Statistics**: file counts, percentages, coverage numbers
2. **Version numbers**: Python, library versions, tool versions
3. **Directory structures**: claimed vs actual layout
4. **Feature claims**: what framework provides
5. **Cross-document consistency**: same fact stated consistently across docs

---

## Phase 1: Critical Path Documents

**Priority**: 🔴 CRITICAL
**Estimated time**: 1-1.5 hours

### 1.1 Root Level Documents

| # | File | Verification Tasks |
|---|------|-------------------|
| 1.1.1 | `AGENTS.md` | ✅ COMPLETED (2025-12-18) |
| 1.1.2 | `README.md` | ✅ Links verified, external URL note logged |
| 1.1.3 | `ARCHITECTURE.md` | ✅ Links verified, diagrams accurate |
| 1.1.4 | `CHANGELOG.md` | ✅ Links verified, external URLs OK |
| 1.1.5 | `CONTRIBUTING.md` | ✅ Fixed CLAUDE.md→AGENTS.md, scripts/ issue logged |
| 1.1.6 | `EXAMPLES.md` | ✅ Fixed broken quick-start link |
| 1.1.7 | `ROADMAP.md` | ✅ Links verified |
| 1.1.8 | `SECURITY.md` | ✅ Links verified |
| 1.1.9 | `CODE_OF_CONDUCT.md` | ✅ Standard text OK, links verified |

### 1.2 Core Navigation Documents

| # | File | Verification Tasks |
|---|------|-------------------|
| 1.2.1 | `docs/INDEX.md` | ✅ Structure verified, anti-pattern links valid |
| 1.2.2 | `docs/LINKS_REFERENCE.md` | ✅ Anchor IDs present, paths verified |
| 1.2.3 | `docs/STYLE_GUIDE.md` | ✅ Examples valid, format correct |

---

## Phase 2: Guide Documents

**Priority**: 🔴 CRITICAL
**Estimated time**: 1.5-2 hours

### 2.1 AI Workflow Guides

| # | File | Verification Tasks |
|---|------|-------------------|
| 2.1.1 | `docs/guides/ai-code-generation-master-workflow.md` | [ ] Stage descriptions, navigation matrix accuracy |
| 2.1.2 | `docs/guides/prompt-validation-guide.md` | [ ] Checklist completeness, linked templates |
| 2.1.3 | `docs/guides/requirements-intake-template.md` | [ ] Template format, example validity |
| 2.1.4 | `docs/guides/implementation-plan-template.md` | [ ] Template sections, linked resources |
| 2.1.5 | `docs/guides/requirements-traceability-guide.md` | [ ] Methodology accuracy, example correctness |

### 2.2 Technical Guides

| # | File | Verification Tasks |
|---|------|-------------------|
| 2.2.1 | `docs/guides/architecture-guide.md` | [ ] Architecture principles match ARCHITECTURE.md |
| 2.2.2 | `docs/guides/development-commands.md` | [ ] Commands actually work, paths correct |
| 2.2.3 | `docs/guides/use-case-implementation-guide.md` | [ ] Step-by-step accuracy, code examples |
| 2.2.4 | `docs/guides/shared-components.md` | [ ] Component paths exist, usage examples |
| 2.2.5 | `docs/guides/template-naming-guide.md` | [ ] Naming examples match actual templates |
| 2.2.6 | `docs/guides/semantic-shortening-guide.md` | [ ] Decision tree accuracy |
| 2.2.7 | `docs/guides/dry-kiss-yagni-principles.md` | [ ] Principle examples, code samples |
| 2.2.8 | `docs/guides/migration-guide-phase1.md` | [ ] Migration steps accuracy |

---

## Phase 3: Reference Documents

**Priority**: 🟠 HIGH
**Estimated time**: 1 hour

### 3.1 Agent Reference Materials

| # | File | Verification Tasks |
|---|------|-------------------|
| 3.1.1 | `docs/reference/agent-context-summary.md` | [ ] Summary matches detailed docs |
| 3.1.2 | `docs/reference/maturity-levels.md` | [ ] Level descriptions, feature matrices |
| 3.1.3 | `docs/reference/ai-navigation-matrix.md` | [ ] Matrix completeness, stage mappings |
| 3.1.4 | `docs/reference/conditional-stage-rules.md` | [ ] Rules accuracy per level |
| 3.1.5 | `docs/reference/agent-toolbox.md` | [ ] Command accuracy, tool availability |
| 3.1.6 | `docs/reference/deliverables-catalog.md` | [ ] Artifact paths, format specs |
| 3.1.7 | `docs/reference/prompt-templates.md` | [ ] Template usability |
| 3.1.8 | `docs/reference/failure-scenarios.md` | [ ] Scenario accuracy, recovery steps |

### 3.2 Technical Reference

| # | File | Verification Tasks |
|---|------|-------------------|
| 3.2.1 | `docs/reference/tech_stack.md` | [ ] Version numbers current, tools exist |
| 3.2.2 | `docs/reference/project-structure.md` | [ ] Directory structure matches reality |
| 3.2.3 | `docs/reference/troubleshooting.md` | [ ] Solutions accuracy |
| 3.2.4 | `docs/reference/architecture-decision-log-template.md` | [ ] Template format validity |

---

## Phase 4: Quality & Checklists

**Priority**: 🟠 HIGH
**Estimated time**: 30 minutes

### 4.1 Quality Documents (4 files)

| # | File | Verification Tasks |
|---|------|-------------------|
| 4.1.1 | `docs/quality/agent-verification-checklist.md` | [ ] Checklist completeness, linked tools |
| 4.1.2 | `docs/quality/qa-report-template.md` | [ ] Template format, sections |
| 4.1.3 | `docs/quality/automated-quality-gates.md` | [ ] CI configuration accuracy |
| 4.1.4 | `docs/quality/README.md` | [ ] Index completeness |

### 4.2 Checklists (2 files)

| # | File | Verification Tasks |
|---|------|-------------------|
| 4.2.1 | `docs/checklists/service-naming-checklist.md` | [ ] Decision criteria accuracy |
| 4.2.2 | `docs/checklists/code-review-checklist.md` | [ ] Review points validity |

---

## Phase 5: Atomic Documentation

**Priority**: 🟡 MEDIUM
**Estimated time**: 2-3 hours

### 5.1 Architecture (17 files)

| # | Directory | Verification Tasks |
|---|-----------|-------------------|
| 5.1.1 | `docs/atomic/architecture/` | [ ] 9 core architecture docs |
| 5.1.2 | `docs/atomic/architecture/naming/` | [ ] 8 naming convention docs |

**Specific checks**:
- [ ] `improved-hybrid-overview.md` — diagram accuracy
- [ ] `service-separation-principles.md` — principle consistency
- [ ] `naming/README.md` — Quick Reference Table accuracy
- [ ] All Related Documents links valid

### 5.2 Services (32 files)

| # | Directory | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 5.2.1 | `docs/atomic/services/fastapi/` | 11 | [ ] FastAPI patterns current |
| 5.2.2 | `docs/atomic/services/aiogram/` | 8 | [ ] Aiogram 3.x patterns |
| 5.2.3 | `docs/atomic/services/asyncio-workers/` | 7 | [ ] AsyncIO patterns |
| 5.2.4 | `docs/atomic/services/data-services/` | 6 | [ ] Data service patterns |

**Specific checks**:
- [ ] Code examples use Python 3.12+ syntax
- [ ] Library versions match tech_stack.md
- [ ] All CORRECT/INCORRECT patterns valid

### 5.3 Integrations (30 files)

| # | Directory | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 5.3.1 | `docs/atomic/integrations/redis/` | 9 | [ ] Redis 7+ patterns |
| 5.3.2 | `docs/atomic/integrations/rabbitmq/` | 11 | [ ] RabbitMQ patterns |
| 5.3.3 | `docs/atomic/integrations/http-communication/` | 6 | [ ] HTTP client patterns |
| 5.3.4 | `docs/atomic/integrations/cross-service/` | 4 | [ ] Cross-service patterns |

### 5.4 Infrastructure (24 files)

| # | Directory | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 5.4.1 | `docs/atomic/infrastructure/containerization/` | 5 | [ ] Docker configs valid |
| 5.4.2 | `docs/atomic/infrastructure/api-gateway/` | 5 | [ ] Nginx configs |
| 5.4.3 | `docs/atomic/infrastructure/databases/` | 6 | [ ] DB setup accuracy |
| 5.4.4 | `docs/atomic/infrastructure/configuration/` | 4 | [ ] Config patterns |
| 5.4.5 | `docs/atomic/infrastructure/deployment/` | 4 | [ ] Deployment patterns |

### 5.5 Observability (24 files)

| # | Directory | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 5.5.1 | `docs/atomic/observability/logging/` | 6 | [ ] Logging patterns |
| 5.5.2 | `docs/atomic/observability/metrics/` | 5 | [ ] Prometheus patterns |
| 5.5.3 | `docs/atomic/observability/tracing/` | 5 | [ ] OpenTelemetry patterns |
| 5.5.4 | `docs/atomic/observability/error-tracking/` | 3 | [ ] Sentry patterns |
| 5.5.5 | `docs/atomic/observability/elk-stack/` | 4 | [ ] ELK configs |

### 5.6 Testing (20 files)

| # | Directory | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 5.6.1 | `docs/atomic/testing/unit-testing/` | 5 | [ ] Pytest patterns |
| 5.6.2 | `docs/atomic/testing/integration-testing/` | 5 | [ ] Testcontainers |
| 5.6.3 | `docs/atomic/testing/service-testing/` | 4 | [ ] Service test patterns |
| 5.6.4 | `docs/atomic/testing/end-to-end-testing/` | 3 | [ ] E2E patterns |
| 5.6.5 | `docs/atomic/testing/quality-assurance/` | 3 | [ ] QA patterns |

### 5.7 Other Atomic Docs (25 files)

| # | Directory | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 5.7.1 | `docs/atomic/databases/` | 6 | [ ] DB patterns |
| 5.7.2 | `docs/atomic/security/` | 4 | [ ] Security patterns |
| 5.7.3 | `docs/atomic/real-time/` | 4 | [ ] WebSocket/SSE |
| 5.7.4 | `docs/atomic/file-storage/` | 5 | [ ] File handling |
| 5.7.5 | `docs/atomic/external-integrations/` | 4 | [ ] External APIs |
| 5.7.6 | `docs/atomic/README.md` | 1 | [ ] Status table accuracy |
| 5.7.7 | `docs/atomic/TEMPLATE.md` | 1 | [ ] Template validity |

---

## Phase 6: Template Documentation

**Priority**: 🟠 HIGH
**Estimated time**: 30 minutes

### 6.1 Template READMEs (7 files)

| # | File | Verification Tasks |
|---|------|-------------------|
| 6.1.1 | `templates/README.md` | [ ] Template list accuracy, status indicators |
| 6.1.2 | `templates/services/template_business_api/README.md` | [ ] Structure matches code |
| 6.1.3 | `templates/services/template_business_bot/README.md` | [ ] Bot setup accuracy |
| 6.1.4 | `templates/services/template_business_worker/README.md` | [ ] Worker patterns |
| 6.1.5 | `templates/services/template_data_postgres_api/README.md` | [ ] PostgreSQL patterns |
| 6.1.6 | `templates/services/template_data_mongo_api/README.md` | [ ] MongoDB patterns |
| 6.1.7 | `templates/shared/utils/README.md` | [ ] Shared utils docs |

### 6.2 Shared Infrastructure Verification

> **Note**: Shared components created via `2025-12-18-documentation-issues-todo.md`

| # | Component | Files | Verification Tasks |
|---|-----------|-------|-------------------|
| 6.2.1 | `templates/shared/http_clients/` | 2 | [ ] DataApiClient imports work |
| 6.2.2 | `templates/shared/rabbitmq/` | 3 | [ ] Publisher/Consumer imports work |
| 6.2.3 | `templates/shared/middleware/` | 2 | [ ] RequestIdMiddleware imports work |
| 6.2.4 | `templates/shared/events/` | 2 | [ ] BaseEvent imports work |
| 6.2.5 | `templates/shared/testing/` | 2 | [ ] Fixtures imports work |
| 6.2.6 | `templates/shared/utils/` | 6 | [ ] All utils imports work |

---

## Phase 7: Audit Documentation

**Priority**: 🟢 LOW
**Estimated time**: 15 minutes

> **Self-referential**: This phase audits the audit documentation itself.

| # | File | Verification Tasks |
|---|------|-------------------|
| 7.1 | `docs/audit/README.md` | [ ] Index accuracy |
| 7.2 | `docs/audit/todo/README.md` | [ ] Style guide completeness |
| 7.3 | `docs/audit/todo/2025-12-18-documentation-issues-todo.md` | [ ] Cross-refs to this file |
| 7.4 | `docs/audit/templates/README.md` | [ ] Template list accuracy |
| 7.5 | `docs/audit/templates/comprehensive-audit.md` | [ ] Template usability |
| 7.6 | `docs/audit/reports/README.md` | [ ] Reports index |

---

## Verification Commands

### Link Verification Script

```bash
#!/bin/bash
# check-links.sh - Verify all markdown links

FILE="$1"
echo "Checking links in: $FILE"

# Extract all markdown links
grep -Eo '\]\([^)]+\)' "$FILE" | sed 's/](//' | sed 's/)$//' | while read link; do
    # Skip external URLs
    if [[ "$link" == http* ]]; then
        echo "  [EXT] $link"
        continue
    fi

    # Extract file path (before #)
    file_path=$(echo "$link" | cut -d'#' -f1)
    anchor=$(echo "$link" | grep -Eo '#.*' || echo "")

    # Get directory of current file for relative paths
    base_dir=$(dirname "$FILE")

    # Resolve path
    if [[ "$file_path" == /* ]]; then
        full_path="$file_path"
    else
        full_path="$base_dir/$file_path"
    fi

    # Normalize path
    full_path=$(realpath -m "$full_path" 2>/dev/null || echo "$full_path")

    if [ -f "$full_path" ]; then
        if [ -n "$anchor" ]; then
            anchor_name=$(echo "$anchor" | sed 's/#//')
            if grep -qiE "id=\"$anchor_name\"|^#+.*$anchor_name" "$full_path" 2>/dev/null; then
                echo "  [OK] $link"
            else
                echo "  [BROKEN ANCHOR] $link"
            fi
        else
            echo "  [OK] $link"
        fi
    else
        echo "  [MISSING] $link -> $full_path"
    fi
done
```

### Batch Verification

```bash
# Run on all docs
find docs -name "*.md" -type f -exec ./check-links.sh {} \; 2>&1 | tee link-audit.log

# Find broken links only
grep "MISSING\|BROKEN" link-audit.log
```

### Fact Verification Queries

```bash
# Check file counts match claims
echo "Atomic docs count:"
find docs/atomic -name "*.md" -type f | wc -l

# Check template services exist
ls -la templates/services/

# Check Python version in pyproject.toml files
find . -name "pyproject.toml" -exec grep -l "python" {} \;

# Verify tech stack versions
cat docs/reference/tech_stack.md | grep -E "^\|.*\|.*\|"
```

---

## Success Criteria

### Phase Completion Criteria

| Phase | Completion Criteria |
|-------|---------------------|
| Phase 1 | All root docs: 0 broken links, facts verified |
| Phase 2 | All guides: 0 broken links, code examples valid |
| Phase 3 | All references: 0 broken links, data current |
| Phase 4 | All quality docs: 0 broken links |
| Phase 5 | All atomic docs: 0 broken links, Related Documents valid |
| Phase 6 | All template docs: structure matches code, shared/ imports work |
| Phase 7 | All audit docs: self-consistent, cross-refs valid |

### Quality Gates

- [ ] **Zero broken internal links**
- [ ] **All anchors resolve correctly**
- [ ] **Statistics match reality** (file counts, percentages)
- [ ] **Version numbers current** (within 1 minor version)
- [ ] **Code examples syntactically valid**
- [ ] **Directory structures match claims**

---

## Issue Tracking

### Issue Template

```markdown
### [PHASE.TASK] Brief Description

**File**: `path/to/file.md`
**Line**: XX
**Type**: Broken Link | Invalid Fact | Outdated Info | Missing Content
**Severity**: Critical | High | Medium | Low

**Current**:
What the document currently says

**Expected**:
What it should say

**Fix Applied**: [ ] Yes / [ ] No
**Verified**: [ ] Yes / [ ] No
```

### Issue Log

| ID | File | Type | Severity | Status |
|----|------|------|----------|--------|
| 1.1.1-001 | AGENTS.md | Header mismatch | Medium | ✅ Fixed |
| 1.1.1-002 | AGENTS.md | Broken anchor | High | ✅ Fixed |
| 1.1.6-001 | EXAMPLES.md | Broken link `docs/getting-started/quick-start.md` | High | ✅ Fixed |
| 1.1.5-001 | CONTRIBUTING.md | Wrong file `CLAUDE.md` (should be AGENTS.md) | High | ✅ Fixed |
| 1.1.5-002 | CONTRIBUTING.md | Missing `scripts/audit_docs.sh` (9 refs) | Medium | ✅ Removed |
| 1.1.2-001 | README.md | External URL 404 `bgs2509.github.io` | Low | 📝 Note (infra) |
| 2.2.7-001 | dry-kiss-yagni-principles.md | 7 broken links (anti-patterns/, http/, etc.) | High | ✅ Fixed |
| 4.1.3-001 | automated-quality-gates.md | Broken link `testing-strategy.md` | Medium | ✅ Fixed |
| 5.1.1-001 | sqlalchemy-integration.md | Outdated `pydantic==2.5.0` → `>=2.6.3` | Low | ✅ Fixed |
| 5.1.2-001 | aiogram/basic-setup.md | Outdated `aiogram>=3.4` → `>=3.22.0` | Low | ✅ Fixed |
| 7.1.1-001 | audit/reports/README.md | Broken link `2025-12-documentation-issues.md` | High | ✅ Fixed |
| — | — | — | — | — |

---

## Execution Order

| Priority | Phases | Focus |
|----------|--------|-------|
| First | 1, 2 | Critical path (root + guides) |
| Second | 3, 4 | References + quality |
| Third | 5.1-5.3 | Atomic: architecture, services, integrations |
| Fourth | 5.4-5.7 | Atomic: infrastructure, observability, testing, others |
| Fifth | 6 | Templates + shared/ verification |
| Last | 7 + Review | Audit docs + final verification |

---

## Post-Audit Actions

1. **Update `docs/atomic/README.md`** — refresh completion statistics
2. **Update `docs/INDEX.md`** — add any missing document links
3. **Create audit report** — summarize findings in `docs/contributing/audit/`
4. **Update CHANGELOG.md** — document documentation fixes
5. **Consider automation** — implement pre-commit link checker

---

## Related Documents

- `AGENTS.md` — entry point documentation
- `docs/INDEX.md` — master documentation index
- `docs/LINKS_REFERENCE.md` — centralized link table
- `docs/STYLE_GUIDE.md` — documentation standards
- `docs/audit/todo/2025-12-18-documentation-issues-todo.md` — prerequisite (COMPLETED)
- `docs/audit/todo/README.md` — TODO file style guide

---

## Dependencies

### Completed Prerequisites

| Dependency | Status | Impact |
|------------|--------|--------|
| `2025-12-18-documentation-issues-todo.md` | ✅ COMPLETED | Shared infrastructure created |
| `templates/shared/http_clients/` | ✅ EXISTS | Phase 6.2 verification enabled |
| `templates/shared/rabbitmq/` | ✅ EXISTS | Phase 6.2 verification enabled |
| `templates/shared/middleware/` | ✅ EXISTS | Phase 6.2 verification enabled |
| `templates/shared/events/` | ✅ EXISTS | Phase 6.2 verification enabled |
| `templates/shared/testing/` | ✅ EXISTS | Phase 6.2 verification enabled |

### Created Templates

| Template | Status | Files |
|----------|--------|-------|
| `template_business_api` | ✅ COMPLETE | Full structure |
| `template_business_bot` | ✅ COMPLETE | Full structure |
| `template_business_worker` | ✅ COMPLETE | Full structure |
| `template_data_postgres_api` | ✅ EXISTS | Reference implementation |
| `template_data_mongo_api` | ✅ EXISTS | Reference implementation |

---

**Last Updated**: 2025-12-18
**Author**: AI Documentation Audit
