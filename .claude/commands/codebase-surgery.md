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
3. **No rationalizing.** "Test-only" is not a status — it's a question. Either the test is valuable (wire the module in or mark it as a future feature) or it's dead (delete both). Decide.
4. **Measure constantly.** After every batch of changes: `pytest`, `ruff check`, line count, zero-importer count. Numbers, not feelings.

---

## Phase 1: Classify every zero-importer file (DO THIS FIRST)

Run the zero-importer scan:
```bash
for f in $(find src/ -name '*.py' -not -name '__init__.py' -not -path '*__pycache__*'); do
  mod=$(echo $f | sed 's|/|.|g;s|\.py$||')
  src_count=$(grep -rn "from $mod import\|import $mod" src/ --include='*.py' 2>/dev/null | grep -v "$f" | grep -v __pycache__ | wc -l)
  test_count=$(grep -rn "from $mod import\|import $mod" tests/ --include='*.py' 2>/dev/null | grep -v __pycache__ | wc -l)
  if [ "$src_count" -eq 0 ]; then
    lines=$(wc -l < "$f")
    echo "src=$src_count test=$test_count lines=$lines $f"
  fi
done | sort -t= -k3 -rn
```

For EVERY file in the output, assign exactly one verdict:

| Verdict | Meaning | Action |
|---------|---------|--------|
| **ENTRY_POINT** | Legitimate top-level entry (app.py, main.py, worker.py) | Document in MODULE_REGISTRY as layer 6 entry point |
| **INFRA** | Build/validation tool (MODULE_REGISTRY, encoding_gate, corpus_audit) | Document as infrastructure, verify it's actually called by tools/ |
| **FUTURE** | Implements a real feature needed later (e.g., muhurtha for Phase A) | Move to `src/future/` with a one-line note of what it's for. Delete its tests from the main suite — they'll come back when the module is wired in |
| **DEAD** | Nobody needs this. No production path, no future plan. | `git rm` the module AND any test files that import it |
| **WIRE** | Should be reachable but isn't — a wiring bug | Fix the wiring (add import to the consumer that should use it) |

**Commit after Phase 1:** One commit with all deletions + moves + MODULE_REGISTRY updates. Message: `refactor(S3XX): classify and resolve N zero-importer files (X deleted, Y archived to src/future/)`

**Verify:**
```bash
# Re-run zero-importer scan — only ENTRY_POINT and INFRA verdicts should remain
# Every remaining zero-importer file must be documented in MODULE_REGISTRY
```

---

## Phase 2: Fix every silent exception handler outside src/calculations/

S324 fixed src/calculations/ (100 → 16). The rest of src/ still has ~61 silent handlers.

**Worst offenders (as of S324):**
- `src/ui/app.py` — 21 handlers. The Streamlit UI. Users see blank/stale screens instead of errors.
- `src/api/main.py` — 9 handlers. The FastAPI server. Clients get 200 OK with wrong data.
- `src/guidance/` — 9 handlers.
- `src/cache.py` — 6 handlers.
- `src/worker.py` — 5 handlers.
- `src/auth.py` — 4 handlers.

For each handler, apply the same classification as S324:
- **RAISE** — programming error being swallowed → remove try/except entirely
- **NARROW** — overly broad → change to specific exception type (ImportError, KeyError, etc.)
- **LOG** — legitimate broad catch but silent → add `logger.exception()` before the fallback
- **ACCEPT** — genuinely needs broad catch with silent fallback (rare)

**Priority order:** app.py first (most users hit it), then main.py, then the rest.

**Commit per file or per batch.** Run tests after each.

**Verify:**
```bash
grep -rn 'except.*Exception' src/ --include='*.py' | grep -v 'logger\|raise\|warnings\|log\.\|logging' | grep -v __pycache__ | wc -l
# Target: ≤ 20 (swisseph wrappers + genuinely unavoidable)
```

---

## Phase 3: Audit ghost tests

After Phase 1 deletes/moves dead modules, some tests will break (they import deleted modules). But there may be more ghost tests — tests that technically pass but test nothing meaningful.

Find them:
```bash
# Tests that import modules with 0 production importers
# (After Phase 1, this list should be empty or near-empty)
for f in $(find src/ -name '*.py' -not -name '__init__.py' -not -path '*__pycache__*' -not -path '*future*'); do
  mod=$(echo $f | sed 's|/|.|g;s|\.py$||')
  src_count=$(grep -rn "from $mod import\|import $mod" src/ --include='*.py' 2>/dev/null | grep -v "$f" | grep -v __pycache__ | wc -l)
  if [ "$src_count" -eq 0 ]; then
    grep -rn "from $mod import\|import $mod" tests/ --include='*.py' 2>/dev/null | grep -v __pycache__
  fi
done
```

For each test that imports a non-production module:
- If the module was moved to `src/future/` → move the test to `tests/future/` (excluded from default pytest)
- If the module was deleted → delete the test
- If the test validates something genuinely important (e.g., math correctness of shadbala) → wire the module into production

**Commit:** `refactor(S3XX): remove N ghost tests (tested dead code), archive M to tests/future/`

---

## Phase 4: Verify everything

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

# 5. Zero-importer count (should be only documented entry points + infra)
for f in $(find src/ -name '*.py' -not -name '__init__.py' -not -path '*__pycache__*' -not -path '*future*'); do
  mod=$(echo $f | sed 's|/|.|g;s|\.py$||')
  count=$(grep -rn "from $mod import\|import $mod" src/ --include='*.py' 2>/dev/null | grep -v "$f" | grep -v __pycache__ | wc -l)
  if [ "$count" -eq 0 ]; then echo "$f"; fi
done
# Target: only app.py, main.py, worker.py, MODULE_REGISTRY.py, invariants.py

# 6. Silent handler count
grep -rn 'except.*Exception' src/ --include='*.py' | grep -v 'logger\|raise\|warnings\|log\.\|logging' | grep -v __pycache__ | wc -l
# Target: ≤ 20

# 7. Line count
find src/ -name "*.py" -not -path "*__pycache__*" -not -path "*future*" | xargs wc -l | tail -1
# Record this as the "live code" baseline
```

---

## Exit criteria (ALL must be true)

1. Every .py file in src/ (excluding src/future/) is reachable from a production entry point OR documented as infrastructure in MODULE_REGISTRY
2. Zero-importer scan returns only documented entry points (≤ 10 files)
3. Silent exception handlers across all of src/: ≤ 20
4. No test imports a module from src/future/ (archived tests moved to tests/future/)
5. `pytest` green, `ruff` clean, `validate_constants` clean, `import_boundary_check` clean
6. Net line reduction from pre-session baseline recorded (expected: 10,000-15,000 lines)

## What this does NOT include

- No encoding
- No new features or condition primitives
- No scoring changes
- No BPHS chapter reading
- No modifier migration (that's encoding-session work)
