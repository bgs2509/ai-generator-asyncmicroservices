# CLAUDE.md — Pre-Action Verification Protocol

> **Purpose**: Mandatory verification rules AI MUST execute BEFORE any action.
> This file prevents errors by requiring verification, not fixing them after.
>
> **Philosophy**: VERIFY BEFORE ACT — Never assume, always check.

---

## Quick Reference

| Action | Required Verification | Tool/Command |
|--------|----------------------|--------------|
| Create file | Verify NOT exists | `ls <path>` or Glob |
| Edit file | Read current content | Read tool |
| Delete file | Verify no dependencies | Grep for imports/references |
| Write code | Check DRY/KISS/SOLID | See §2 |
| Add documentation | Check canonical source | See §3 |
| Add/modify links | Verify link targets exist | See §4 |

---

## 1. File Operation Rules

### 1.1 Before Creating Files

**MANDATORY**: Verify file does NOT exist before creating.

```bash
# Required check
ls <path> 2>/dev/null && echo "⚠️ FILE EXISTS" || echo "✅ OK to create"
```

**WHY**: Prevents overwriting existing files, catches stale TODO-list entries.

**Anti-Pattern**:
```
❌ WRONG: TODO says "create file X" → create X
✅ RIGHT: TODO says "create file X" → check if X exists → then decide
```

### 1.2 Before Editing Files

**MANDATORY**: Read current content before ANY edit.

```bash
# Required: Use Read tool first
# Then verify the section you want to edit exists
```

**WHY**: Ensures understanding of context, prevents breaking existing logic.

### 1.3 Before Deleting Files

**MANDATORY**: Check for dependencies before deletion.

```bash
# Check Python imports
grep -r "from.*<module>" . --include="*.py"
grep -r "import.*<module>" . --include="*.py"

# Check documentation references
grep -r "<filename>" docs/ --include="*.md"

# Check configuration references
grep -r "<filename>" . --include="*.yml" --include="*.yaml" --include="*.toml"
```

**RULE**: If any references found → update them BEFORE deleting.

---

## 2. Code Quality Pre-Checks

> **REFERENCE**: Full principles in `docs/guides/dry-kiss-yagni-principles.md`

### 2.1 DRY Pre-Check (Don't Repeat Yourself)

**BEFORE writing any function/class**:

```bash
# Search for similar implementations
grep -r "<function_pattern>" . --include="*.py" | head -10

# Check shared utilities
ls templates/shared/utils/

# Check if similar logic exists in other services
grep -r "<logic_pattern>" templates/services/ --include="*.py"
```

**Checklist**:
- [ ] Searched for similar implementations?
- [ ] Checked `shared/utils/` for existing utilities?
- [ ] Checked `templates/` for existing patterns?
- [ ] If similar code exists → reuse or extract to shared

### 2.2 KISS Pre-Check (Keep It Simple)

**BEFORE writing complex logic**:

```bash
# Check complexity of existing file (if editing)
radon cc <file> --show-complexity

# Target: McCabe complexity < 10 for all functions
```

**Checklist**:
- [ ] Can this be simpler? (fewer branches, fewer lines)
- [ ] Is maturity level appropriate? (no Level 4 infra for PoC)
- [ ] Are there unnecessary abstractions?

### 2.3 SOLID Pre-Check

**BEFORE creating classes**:

| Principle | Question to Ask |
|-----------|-----------------|
| **S**ingle Responsibility | Does this class have ONE reason to change? |
| **O**pen/Closed | Can it be extended without modification? |
| **L**iskov Substitution | Can subtypes replace base types? |
| **I**nterface Segregation | Are interfaces focused and minimal? |
| **D**ependency Inversion | Does it depend on abstractions, not concretions? |

### 2.4 YAGNI Pre-Check (You Aren't Gonna Need It)

**BEFORE adding features/infrastructure**:

- [ ] Is this feature explicitly requested?
- [ ] Is there evidence this is needed NOW?
- [ ] Would simpler solution work for current requirements?

**Anti-Pattern**:
```
❌ WRONG: "We MIGHT need caching later" → add Redis
✅ RIGHT: "Users report slow responses" → add caching with evidence
```

---

## 3. Documentation Pre-Checks

> **REFERENCE**: Canonical sources in `docs/reference/canonical-references.md`

### 3.1 Before Adding Documentation

**MANDATORY**: Check if canonical source already exists.

```bash
# Check if topic already documented
grep -ri "<topic>" docs/ --include="*.md" | head -5

# Check canonical references
grep -i "<topic>" docs/reference/canonical-references.md
```

**RULE**: If canonical source exists → LINK to it, don't duplicate content.

### 3.2 Before Creating New Documentation Files

**Checklist**:
- [ ] Checked `docs/INDEX.md` for existing coverage?
- [ ] Checked `docs/reference/canonical-references.md`?
- [ ] If topic exists → update existing file, don't create new
- [ ] If new topic → add to `canonical-references.md` after creation

### 3.3 Documentation Style

> **REFERENCE**: Full style guide in `docs/STYLE_GUIDE.md`

**Quick rules**:
- Use links through `LINKS_REFERENCE.md` when possible
- Follow header hierarchy (# → ## → ### → ####)
- Include PURPOSE block at document start
- Add to INDEX.md after creating new docs

---

## 4. Link Integrity Verification

> **CRITICAL**: Broken links cause confusion and reduce trust in documentation.

### 4.1 Before Adding Links

**MANDATORY**: Verify link target exists BEFORE adding any link.

```bash
# For relative links in markdown
ls <target_path> 2>/dev/null && echo "✅ Target exists" || echo "❌ BROKEN"

# Example: Before adding [Guide](docs/guides/example.md)
ls docs/guides/example.md
```

### 4.2 Before Modifying/Moving Files

**MANDATORY**: Find all references to the file BEFORE moving/renaming.

```bash
# Find all markdown links to this file
grep -r "\[.*\].*(<filename>" docs/ --include="*.md"

# Find all references in any file
grep -r "<filename>" . --include="*.md" --include="*.py" --include="*.yml"
```

**RULE**: Update ALL references BEFORE or IMMEDIATELY AFTER moving/renaming.

### 4.3 Periodic Link Validation

**When to run full link check**:
- Before committing documentation changes
- After bulk file operations (move, rename, delete)
- During documentation audits

```bash
# Quick validation script for markdown links
for file in $(find docs/ -name "*.md"); do
  grep -oP '\[.*?\]\(\K[^)]+' "$file" 2>/dev/null | while read link; do
    # Skip external links and anchors
    if [[ ! "$link" =~ ^http && ! "$link" =~ ^# ]]; then
      # Resolve relative path
      dir=$(dirname "$file")
      target="$dir/$link"
      # Remove anchor if present
      target="${target%%#*}"
      if [[ ! -f "$target" && ! -d "$target" ]]; then
        echo "❌ BROKEN: $file → $link"
      fi
    fi
  done
done
```

### 4.4 Link Validation Checklist

**Before any PR with documentation changes**:
- [ ] All new links verified to exist?
- [ ] All modified file paths updated in referencing docs?
- [ ] No orphaned files created (files with no links to them)?
- [ ] INDEX.md and LINKS_REFERENCE.md updated if needed?

### 4.5 Common Link Issues

| Issue | Prevention |
|-------|------------|
| Typo in path | Copy-paste from `ls` output |
| Wrong relative path | Use paths relative to file location |
| Moved file, stale links | Search references BEFORE moving |
| Deleted file, broken links | Search references BEFORE deleting |
| Case sensitivity | Linux is case-sensitive, verify exact case |

---

## 5. Architecture Pre-Checks

> **REFERENCE**: Full architecture in `ARCHITECTURE.md`

### 5.1 Service Communication

**BEFORE implementing service calls**:

| Pattern | Rule |
|---------|------|
| Business → Data | HTTP only (NEVER direct DB access) |
| Service → Service | HTTP for sync, RabbitMQ for async |
| Event publishing | RabbitMQ only |

**Anti-Pattern**:
```python
# ❌ WRONG: Business service with direct DB
class UserService:
    def __init__(self, db_session: Session):  # Direct DB!
        self.db = db_session

# ✅ RIGHT: Business service with HTTP client
class UserService:
    def __init__(self, data_client: DataServiceClient):
        self.data_client = data_client
```

### 5.2 Naming Conventions

**BEFORE naming anything**:

```bash
# Check naming checklist
cat docs/checklists/service-naming-checklist.md
```

| Entity | Pattern | Example |
|--------|---------|---------|
| Services | `{context}_{domain}_{type}` | `finance_lending_api` |
| Templates | `template_{domain}_{type}` | `template_business_api` |

### 5.3 Event Loop Ownership

**RULE**: Each service owns ONE event loop.

**BEFORE adding async operations**:
- [ ] Does this service already have an event loop owner (FastAPI/Aiogram)?
- [ ] Am I accidentally creating a second event loop?
- [ ] Are all blocking operations properly wrapped?

---

## 6. Anti-Duplication Rules

### 6.1 Code Duplication Detection

```bash
# Pre-check: Find similar code (threshold 5%)
jscpd src/ --threshold 5 --silent

# If >5% duplication detected:
# → Extract to shared/utils/
# → Or create shared service method
```

### 6.2 File Duplication Detection

```bash
# Find files with identical content
find . -name "*.py" -type f -exec md5sum {} \; | sort | uniq -d -w32

# Find files with similar names (potential duplicates)
find . -name "*.py" | xargs -I{} basename {} | sort | uniq -d
```

### 6.3 Logic Duplication Prevention

**Before writing new logic, ask**:

1. Is this already in `templates/shared/utils/`?
2. Is this already in another service?
3. Should this be in data service (centralized)?
4. Can I import instead of copy-paste?

**Rule of Three**:
- First occurrence → write inline
- Second occurrence → note potential for extraction
- Third occurrence → MUST extract to shared

---

## 7. Conflict Prevention

### 7.1 Before Modifying Shared Code

```bash
# Check what depends on this code
grep -r "from.*<module>" . --include="*.py"
grep -r "import.*<module>" . --include="*.py"

# Check if tests exist
ls tests/*<module>* 2>/dev/null
```

**RULE**: If code is used by multiple services → extra careful review needed.

### 7.2 Before Changing API Contracts

**Checklist**:
- [ ] Is this a breaking change?
- [ ] Are all consumers identified?
- [ ] Is versioning needed (v1 → v2)?
- [ ] Are migration docs needed?

### 7.3 Before Modifying Database Schema

**MANDATORY**:
- [ ] Migration script created?
- [ ] Rollback possible?
- [ ] All services using this schema identified?
- [ ] Data service updated first?

---

## 8. Verification Commands Cheatsheet

### File Operations
```bash
# File exists?
ls <path> 2>/dev/null && echo "EXISTS" || echo "NOT EXISTS"

# Directory exists?
test -d <path> && echo "EXISTS" || echo "NOT EXISTS"

# Find file by name
find . -name "<filename>" -type f
```

### Code Quality
```bash
# Similar code search
grep -r "<pattern>" . --include="*.py" | head -10

# Code duplication %
jscpd src/ --threshold 10

# Complexity check
radon cc <file> --show-complexity

# Maintainability index
radon mi <file> --show
```

### Dependencies
```bash
# Python import check
grep -r "from <module>" . --include="*.py"
grep -r "import <module>" . --include="*.py"

# Documentation reference check
grep -r "<filename>" docs/ --include="*.md"
```

### Link Validation
```bash
# Find all markdown links in file
grep -oP '\[.*?\]\(\K[^)]+' <file>

# Check if link target exists
ls <target> 2>/dev/null

# Find broken links (quick scan)
grep -r "\](.*\.md)" docs/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  link=$(echo "$line" | grep -oP '\]\(\K[^)]+' | head -1)
  if [[ -n "$link" && ! "$link" =~ ^http ]]; then
    dir=$(dirname "$file")
    target="$dir/${link%%#*}"
    test -f "$target" || echo "BROKEN: $file → $link"
  fi
done
```

### Canonical Sources
```bash
# Check canonical source for topic
grep -i "<topic>" docs/reference/canonical-references.md

# List all canonical sources
grep "^\|" docs/reference/canonical-references.md | head -50
```

---

## 9. Quick Navigation

| Need | Document |
|------|----------|
| AI workflow & reading order | `AGENTS.md` |
| DRY/KISS/YAGNI details | `docs/guides/dry-kiss-yagni-principles.md` |
| Post-action verification | `docs/quality/agent-verification-checklist.md` |
| Code review standards | `docs/atomic/testing/quality-assurance/code-review-checklist.md` |
| Canonical sources | `docs/reference/canonical-references.md` |
| Architecture patterns | `ARCHITECTURE.md` |
| Documentation style | `docs/STYLE_GUIDE.md` |
| Naming conventions | `docs/checklists/service-naming-checklist.md` |
| Link reference table | `docs/LINKS_REFERENCE.md` |
| Documentation index | `docs/INDEX.md` |

---

## 10. Summary: The VERIFY BEFORE ACT Protocol

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE ANY ACTION, AI MUST:                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. FILE CREATE    → Verify file does NOT exist                 │
│  2. FILE EDIT      → Read current content first                 │
│  3. FILE DELETE    → Check all dependencies/references          │
│  4. ADD LINK       → Verify target exists                       │
│  5. WRITE CODE     → Check for existing similar code (DRY)      │
│  6. ADD FEATURE    → Verify it's needed NOW (YAGNI)             │
│  7. ADD DOCS       → Check canonical source exists              │
│  8. MODIFY SHARED  → Identify all dependents                    │
└─────────────────────────────────────────────────────────────────┘

NEVER ASSUME → ALWAYS VERIFY → THEN ACT
```

---

## Related Documents

- **Workflow**: `AGENTS.md` — Complete AI agent workflow
- **Principles**: `docs/guides/dry-kiss-yagni-principles.md` — Detailed principles
- **Verification**: `docs/quality/agent-verification-checklist.md` — Post-action checks
- **Style**: `docs/STYLE_GUIDE.md` — Documentation formatting
- **Architecture**: `ARCHITECTURE.md` — System design principles

---

**Document Version**: 1.0
**Created**: 2025-01-07
**Purpose**: Pre-action verification protocol for AI agents
**Scope**: Claude Code and compatible AI assistants
