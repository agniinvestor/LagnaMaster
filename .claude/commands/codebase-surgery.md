# Codebase Surgery: Resolve Every Dead File, Silent Handler, and Ghost Test

## Session type
**Governance** — no encoding, no new features. Pure codebase health.

## Why this session exists

S324 revealed that 12.7% of src/ (79 files, 15,567 lines) has zero production importers. 77 silent exception handlers remain outside src/calculations/. 68 modules are imported only by tests — meaning thousands of "passing" tests validate code no user ever hits. The codebase cannot be trusted until every file is either reachable from a production entry point or explicitly deleted.

This is not a cleanup session. This is surgery. Every file gets a verdict. No deferrals.

---

## Ground rules

1. **No plans, no roadmaps, no execution specs.** The codebase is the only source of truth. Run diagnostics, read code, make decisions.
2. **No premature closure.** Do not propose "encoding can resume" until every diagnostic in the exit criteria section returns the target number.
3. **No rationalizing.** "Test-only" is not a status — it's a question. Either the test is valuable (wire the module in) or it's dead (delete both). Decide.
4. **Measure constantly.** After every batch of changes: `pytest`, `ruff check`, line count, zero-importer count. Numbers, not feelings.
5. **No "archive to future/" verdict.** Moving dead code to a new directory is renaming, not resolving. If a module has a concrete planned use, document it with the specific session/phase that will wire it in. Otherwise delete it.

---

## Phase 0: Map the actual import graph (BEFORE any deletions)

The simple "zero-importer" grep has blind spots. Build the real picture first.

### 0a. Identify the 3 production entry points

```bash
# These are the ONLY files that don't need an importer — they ARE the entry points
# Verify each one actually runs:
echo "=== Entry points ==="
echo "Streamlit UI: src/ui/app.py"
echo "FastAPI API:  src/api/main.py"  
echo "Celery worker: src/worker.py"
```

### 0b. Build the transitive reachability set

Don't just check direct importers. Trace the full import tree from each entry point.

```python
# Build a script (or use AST) that:
# 1. Starts from app.py, main.py, worker.py
# 2. Recursively follows every `from src.X import` and `import src.X`
# 3. Collects the full set of transitively reachable modules
# 4. Reports which src/ .py files are NOT in that set
```

This catches the case where Module A imports Module B imports Module C — but Module A itself is dead. The simple grep shows B and C as "having importers" when the whole chain is unreachable.

### 0c. Also check tools/ importers

```bash
grep -rn 'from src\.\|import src\.' tools/ --include='*.py' | grep -v __pycache__ | grep -v archive/
```

Modules imported ONLY by tools/ are infrastructure, not dead. But they should be documented as such.

### 0d. Check __init__.py re-exports

```bash
# Non-empty __init__.py files may re-export modules, making them appear imported
find src/ -name '__init__.py' -not -path '*__pycache__*' -not -empty -exec cat {} \;
```

### 0e. Record baseline

```bash
find src/ -name "*.py" -not -path "*__pycache__*" | xargs wc -l | tail -1
# Record this number — all reductions measured against it
```

---

## Phase 1: Classify every unreachable file

Using the reachability set from Phase 0, classify every file NOT in the set.

For EVERY unreachable file, assign exactly one verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **ENTRY_POINT** | Legitimate top-level entry (app.py, main.py, worker.py) | Already in reachability roots — no action needed |
| **TOOLS_INFRA** | Only imported by tools/ scripts (diff_engine, migration_audit, etc.) | Document in MODULE_REGISTRY. Verify the tool actually works. |
| **DEAD** | Not reachable from any entry point, not used by tools, no concrete plan to wire in | `git rm` the module AND update/delete any tests that import it |
| **WIRE** | Should be reachable but isn't — a wiring bug or missing integration | Fix the wiring. Add the import to the consumer that should use it. Verify it works. |

**There is no FUTURE/ARCHIVE verdict.** If you can name the specific session and consumer that will wire it in, it's WIRE (do it now or document the exact wiring needed). If you can't, it's DEAD.

**Commit strategy:** One commit per batch of ~10 related files (same directory or same verdict). Not one giant commit. Commit message: `refactor(S3XX): delete N dead modules in src/calculations/ (X lines)`

**After each commit:**
```bash
.venv/bin/pytest tests/ -q --tb=short -x
```

If tests break because they imported a deleted module, that's Phase 3 work — note the test file and continue.

**Verify after all Phase 1 work:**
```bash
# Re-run reachability analysis — every remaining file should be reachable
# OR documented as TOOLS_INFRA in MODULE_REGISTRY
```

---

## Phase 2: Fix every silent exception handler

S324 fixed src/calculations/ (100 → 16). The rest of src/ still has ~61 silent handlers.

### 2a. Find them ALL (improved grep)

```bash
# Pattern 1: except Exception with no logging/raise
grep -rn 'except.*Exception' src/ --include='*.py' | grep -v 'logger\|raise\|warnings\|log\.\|logging\|__pycache__'

# Pattern 2: catch-and-ignore (except ... as e where e is never used)
grep -rn 'except.*Exception.*as e' src/ --include='*.py' | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  lineno=$(echo "$line" | cut -d: -f2)
  # Check if 'e' is used in the next 5 lines
  used=$(sed -n "$((lineno+1)),$((lineno+5))p" "$file" | grep -c '\be\b')
  if [ "$used" -eq 0 ]; then echo "UNUSED_E: $line"; fi
done
```

### 2b. Classify and fix

For each handler:
- **RAISE** — programming error being swallowed → remove try/except entirely
- **NARROW** — overly broad → change to specific exception type (ImportError, KeyError, etc.)
- **LOG** — legitimate broad catch but silent → add `logger.exception()` before the fallback
- **ACCEPT** — genuinely needs broad catch with silent fallback (document WHY in a comment)

**Priority order:** app.py (21 handlers, most users) → main.py (9, API clients) → worker.py (5, async jobs) → rest.

**Commit per file.** Run tests after each.

### 2c. Verify

```bash
grep -rn 'except.*Exception' src/ --include='*.py' | grep -v 'logger\|raise\|warnings\|log\.\|logging\|__pycache__' | wc -l
# Target: ≤ 20 (each one must have a comment explaining why it's ACCEPT)
```

---

## Phase 3: Audit ghost tests

### 3a. Fix tests broken by Phase 1 deletions

Some tests will fail because they import deleted modules. For each:
- If the test tested a dead module → delete the test
- If the test tested a concept that still exists elsewhere → rewrite the import

### 3b. Find tests that import unreachable modules

```bash
# After Phase 1, any test importing a non-reachable module is a ghost
for f in $(find src/ -name '*.py' -not -name '__init__.py' -not -path '*__pycache__*'); do
  mod=$(echo $f | sed 's|/|.|g;s|\.py$||')
  # Check if module is in reachability set — if not, find test importers
  src_count=$(grep -rn "from $mod import\|import $mod" src/ --include='*.py' 2>/dev/null | grep -v "$f" | grep -v __pycache__ | wc -l)
  if [ "$src_count" -eq 0 ]; then
    grep -rn "from $mod import\|import $mod" tests/ --include='*.py' 2>/dev/null | grep -v __pycache__
  fi
done
```

### 3c. Find tests that can never fail

```bash
# Trivial assertions
grep -rn 'assert True' tests/ --include='*.py'

# Catch-all passes inside test functions  
grep -rn 'except.*:' tests/ --include='*.py' -A1 | grep -B1 'pass$' | grep 'except'

# Empty test functions
grep -rn 'def test_' tests/ --include='*.py' -A2 | grep -A2 'def test_' | grep 'pass$'
```

For each: either add a real assertion or delete the test.

### 3d. Find duplicate test coverage

```bash
# Tests for the same module from different test files
# (indicates stale test files from prior sessions that were never cleaned up)
grep -rn 'from src\.calculations\.' tests/ --include='*.py' -h | sed 's/.*from \(src\.[^ ]*\) import.*/\1/' | sort | uniq -c | sort -rn | head -20
```

If 5 test files all import `src.calculations.dignity`, check whether they're testing different aspects or duplicating coverage.

**Commit:** `refactor(S3XX): remove N ghost tests, fix M broken imports`

---

## Phase 4: Check for duplicate functionality

The S318 audit found multiple implementations of the same concept. Constants were consolidated in S323, but duplicate FUNCTIONS may remain.

```bash
# Find functions with identical or near-identical names across different files
grep -rn 'def compute_\|def is_\|def get_' src/calculations/ --include='*.py' -h | \
  sed 's/.*def \([a-z_]*\)(.*/\1/' | sort | uniq -c | sort -rn | head -20
```

For each duplicate: read both implementations, determine which is canonical (usually the one with BPHS verse citations), delete or redirect the other.

---

## Phase 5: Verify everything

Run ALL diagnostics:

```bash
# 1. Tests
.venv/bin/pytest tests/ -q --tb=short

# 2. Ruff
.venv/bin/ruff check src/ tests/

# 3. Constants guard
.venv/bin/python tools/validate_constants.py

# 4. Import boundary check
.venv/bin/python tools/import_boundary_check.py

# 5. Reachability: every src/ file is reachable from entry points OR documented as TOOLS_INFRA
# (Re-run the Phase 0 reachability script)

# 6. Silent handler count
grep -rn 'except.*Exception' src/ --include='*.py' | grep -v 'logger\|raise\|warnings\|log\.\|logging\|__pycache__' | wc -l
# Target: ≤ 20

# 7. Ghost test count: tests importing unreachable modules
# Target: 0

# 8. Trivial assertion count
grep -rn 'assert True' tests/ --include='*.py' | wc -l
# Target: 0

# 9. Line count (compare to Phase 0 baseline)
find src/ -name "*.py" -not -path "*__pycache__*" | xargs wc -l | tail -1

# 10. File count
find src/ -name "*.py" -not -path "*__pycache__*" | wc -l
```

Report ALL 10 numbers. Do not interpret — just show them.

---

## Exit criteria (ALL must be true)

1. Every .py file in src/ is transitively reachable from an entry point (app.py, main.py, worker.py) OR documented as TOOLS_INFRA in MODULE_REGISTRY
2. Zero-importer scan (excluding documented entry points + tools infra): **0 files**
3. Silent exception handlers across all of src/: **≤ 20** (each with ACCEPT comment)
4. Tests importing unreachable modules: **0**
5. Trivial assertions (`assert True`, empty test bodies): **0**
6. `pytest` green, `ruff` clean, `validate_constants` clean, `import_boundary_check` clean
7. Before/after line counts and file counts recorded with exact numbers

## What this does NOT include

- No encoding
- No new features or condition primitives
- No scoring changes
- No BPHS chapter reading
- No modifier migration (that's encoding-session work)
- No "archive to future/" — every file is either reachable or deleted
