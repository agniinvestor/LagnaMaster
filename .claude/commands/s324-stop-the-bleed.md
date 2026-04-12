# S324-S328: Phase -1 — Stop the Bleed (Complete Remaining Work)

## Session type
**Governance** — fix bugs, wire connections, delete dead code, close gaps from plans/specs audit. No encoding.

## Context

S317-S323 partially executed the v11 canonical architecture Phase -1. This prompt completes everything remaining so encoding can resume from S329+ with a clean foundation.

**Reference docs (read before starting):**
- `docs/superpowers/specs/2026-04-07-v11-execution-plan.md` (status table at top)
- `docs/superpowers/specs/2026-04-07-canonical-architecture-v11.md`
- `docs/s318_deep_audit.md` (bug list C01-C16, silent exceptions, dead code)

**What's already done (S317-S323):**
- Stage 5 (consolidation): COMPLETE — `src/data/constants.py`, 79 files refactored
- Stage 1 (formula fixes): 12/16 critical bugs fixed, scoring_v2 + avastha deleted
- Condition primitives: taxonomy + builder + 2/4 in rule_firing
- Test diversification: 360-chart system operational
- Plans/specs audited with status markers

---

## Work Packages (execute in this order)

### WP1: Fix remaining critical bugs (Stage 1 completion)

**4 bugs remain from S318 audit:**

1. **C03: D9 lagna = D1 lagna in multi_axis_scoring.py**
   - `multi_axis_scoring.py:539` — `d9_lagna_si = chart.lagna_sign_index` (WRONG)
   - Must compute actual navamsha lagna from D1 lagna longitude
   - This affects 30% of composite score (D9 axis weight = 15%)
   - Fix: use the navamsha chart's lagna, not D1 lagna

2. **C13: D60 even-sign formula contradiction**
   - `varga.py:232` vs `divisional_charts.py:235` — different formulas
   - Verify against BPHS Ch.6 v.17-22, use correct one, fix the other

3. **C14: D7 zero-falsy bug in divisional_charts.py:265**
   - Python `and/or` idiom fails when `(si + div) % 12 == 0`
   - Fix: explicit conditional instead of truthy/falsy

4. **C15: D16 formula wrong for non-cardinal signs**
   - `divisional_charts.py:144-161` — `si % 4` produces 0-3 but dict maps 0-11
   - Verify against BPHS Ch.6, fix formula

**After each fix:** `.venv/bin/pytest tests/ -q --tb=short -x`
**Commit format:** `fix(S324): C0N [description] — BPHS Ch.N v.M`

### WP2: Add missing condition primitives to rule_firing.py

Two condition types are in taxonomy + builder but NOT evaluated by the engine:

1. **`planet_in_derived_house`** — used in 63 rules across Ch.29 + Ch.30
   - Needs: resolve derived house (Arudha Pada, Upa Pada, Karakamsa, etc.)
   - `src/calculations/derived_house.py` already has `resolve_house(base, offset)`
   - Add evaluation block to `_check_compound_conditions()` in rule_firing.py
   - Must handle: arudha_pada, upa_pada, karakamsa derivations
   - Can use existing `src/calculations/argala.py:compute_arudha_lagna` for arudha

2. **`planet_in_sign_type`** — used in 5 rules across Ch.12, 14, 16, 18
   - Needs: check if planet is in a sign matching a type (movable/fixed/dual, fire/earth/air/water, odd/even)
   - Use constants from `src/data/constants.py` (CARDINAL_SIGNS, FIXED_SIGNS, MUTABLE_SIGNS, FIRE_SIGNS, etc.)
   - Add evaluation block to `_check_compound_conditions()` in rule_firing.py

**Validate:** Run existing tests + add specific tests for each primitive.
**Commit:** `feat(S324): evaluate planet_in_derived_house + planet_in_sign_type in rule_firing`

### WP3: Wire dignity into scoring (Stage 7)

The most impactful single fix in the codebase. Dignity is computed but never used in scoring.

1. In `src/scoring.py:score_chart()` loop, after R22:
   ```python
   from src.calculations.dignity import compute_dignity, DIGNITY_SCORE
   r24_score = DIGNITY_SCORE.get(dignities[bhavesh].dignity, 0.0)
   rules.append(RuleResult("R24", f"Bhavesh dignity ({dignities[bhavesh].dignity.value})", r24_score, triggered=r24_score != 0.0))
   ```
2. Update W weights dict with R24 weight
3. India 1947 scores WILL change — update any snapshot tests with new expected values
4. Wire same logic into `multi_axis_scoring.py:_score_one_house()`

**Commit:** `feat(S324): wire dignity into scoring (R24) — Stage 7`

### WP4: Silent exception handlers (Stage 4)

163 broad `except Exception` handlers across src/. Priority order:

1. **Core engine (100 handlers in src/calculations/)** — these hide bugs. Fix first.
   - For each: determine if it's a programming error (→ `raise`), expected failure (→ `logger.warning + return None`), or genuinely needs broad catch (→ `except SpecificError`)
   - Top files: planet_effectiveness.py (7), yoga_fructification.py (5), pressure_engine.py (5), jaimini_full.py (5), feature_decomp.py (5), chart_exceptions.py (5)

2. **Worker/infra (40 handlers)** — worker.py needs broad catches for job resilience, but should log

3. **UI (23 handlers in src/ui/)** — most are `st.error()` displays, acceptable. Review for any that silently swallow.

**Tool:** Use `ruff check --select BLE001` if available, or build `tools/lint_silent_except.py` (AST-based, ~60 lines).
**Commit per batch:** `fix(S32N): fix N silent exception handlers in [layer]`

### WP5: Delete dead code (Stage 6)

~21K lines of dead code remain (S318 identified ~22,692, S323 deleted 1,392).

1. **Build import graph** — find all .py files in src/ with 0 importers
2. **Cross-reference with S318 audit** — `docs/s318_deep_audit.md` lists dead modules
3. **For each dead module:**
   - Verify truly unreachable: `grep -rn 'from src.MODULE import\|import src.MODULE' src/ tests/`
   - If roadmap-relevant: `git mv` to `src/archive/` (create if needed)
   - If truly dead: `git rm`
   - Fix any test imports
4. **Target:** `find src/ -name "*.py" | xargs wc -l | tail -1` should drop significantly

**Commit per batch:** `refactor(S32N): delete N dead modules (X lines) — Stage 6`

### WP6: Module registry (Stage 3 completion)

Upgrade `tools/validate_constants.py` to full `src/MODULE_REGISTRY.py`:

```python
REGISTRY = {
    "house_lord": {"layer": 3, "tier": 2, "canonical_for": ["sign_lords", "house_classification"], "verification": "bphs_pdf"},
    "dignity": {"layer": 3, "tier": 1, "canonical_for": ["exaltation", "debilitation", "mooltrikona", "own_signs"], "verification": "bphs_pdf"},
    # ... one entry per module
}
```

Plus `tools/import_boundary_check.py` that validates:
- No protected constants defined outside canonical source
- No layer N importing from layer N+1

**Commit:** `feat(S32N): MODULE_REGISTRY + import boundary enforcer — Stage 3`

### WP7: Remaining governance gaps

1. **Modifier migration** — migrate 89 modifiers across 16 chapters to 5-effect taxonomy
   - Constants already in taxonomy.py, builder validates
   - Write migration script, apply, verify
   
2. **Legacy migration registry** — wire `migration_registry.py` to gate legacy exclusion
   - `migration_audit.py` exists (420 lines), `migration_tags.py` exists
   - Create registry, wire into `combined_corpus.py`

3. **Verification tags (Stage 2)** — add `_VERIFICATION` dict to every module in src/calculations/
   - Tag 9 canonical sources as `bphs_pdf`
   - Tag formula-compared modules
   - Tag rest as `unverified`

4. **Runtime invariant checker (Stage 8)** — create `src/invariants.py`
   - 5 invariants: planet placement, lordship uniqueness, aspect strength, dignity valid, house count
   - Wire into compute pipeline after Layer 3

**Commit per item:** separate commits

---

## Validation after ALL work packages

```bash
# Tests
.venv/bin/pytest tests/ -q --tb=short

# Ruff
.venv/bin/ruff check src/ tests/

# Constants guard
.venv/bin/python tools/validate_constants.py

# Import boundary check (after WP6)
.venv/bin/python tools/import_boundary_check.py

# Verify no silent exceptions in core
grep -rn 'except.*Exception.*:' src/calculations/ --include='*.py' | grep -v 'logger\|raise\|warnings\|log\.' | wc -l
# Target: 0

# Dead code reduction
find src/ -name "*.py" -not -path "*__pycache__*" | xargs wc -l | tail -1
```

## Exit criteria (ALL must be true before encoding resumes)

1. Zero critical bugs from S318 audit (C01-C16 all resolved)
2. All 4 condition primitives evaluated in rule_firing.py
3. Dignity wired into scoring (R24 fires for India 1947)
4. Silent exception handlers in src/calculations/: 0 bare `except Exception: pass`
5. Dead code: net line count reduction of ≥15,000 lines from pre-S324 baseline
6. MODULE_REGISTRY.py exists + import_boundary_check.py passes
7. All plans/specs status markers updated to reflect completion
8. `.venv/bin/pytest tests/` green, `.venv/bin/ruff check src/ tests/` clean

## What this does NOT include (deferred to encoding sessions)

- No new BPHS chapter encoding
- No new corpus rules
- No scoring recalibration
- No new condition primitives beyond the 4 already in taxonomy
- ENCODING_GRANULARITY.md update — do during first encoding session when the decision rule is needed in practice
