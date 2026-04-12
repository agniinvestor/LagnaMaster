# v11 Execution Plan — Session Contracts, Tool Specs, Testing Strategy

**Companion to:** `2026-04-07-canonical-architecture-v11.md`
**Purpose:** Operational detail that makes the architecture spec executable by AI sessions

---

## Status (2026-04-12 S323 audit)

| Stage | Description | Status | Notes |
|-------|-------------|--------|-------|
| 1 | Fix wrong formulas (42 bugs) | **~75% done** | C01,C02,C04,C05,C06,C07,C08,C09 fixed. C03 (D9 lagna), C13-C15 (div charts) remain. scoring_v2.py + avastha.py deleted (eliminated their bugs). |
| 2 | Tag verification levels | **Not started** | |
| 3 | Module registry + enforcer | **Partial** | `tools/validate_constants.py` built in S323. Full `MODULE_REGISTRY.py` not created. |
| 4 | Silent exception handlers | **Not started** | 143 handlers identified in S318. |
| 5 | Consolidate to canonical primitives | **DONE** | S323: constants.py golden source, 79 files refactored, ~1,830 net lines removed. |
| 6 | Delete dead code (~22,692 lines) | **~6% done** | S323 deleted 5 dead modules (1,392 lines). ~21K lines remain. |
| 7 | Wire missing connections | **Not started** | Dignity not wired into scoring. score_all_axes not deprecated. |
| 8 | Runtime invariant checker | **Not started** | |

**Execution was out of order:** S323 did Stage 5 first (highest encoding-impact). Stages 1-4 partially done through S317-S322 bug fix sessions. Plan should be re-evaluated — remaining stages 2, 4, 6, 8 are quality improvements that don't block encoding.

---

## Stage Reordering (from v11 original)

The original v11 spec had MODULE_REGISTRY as Stage 7. This is needed by Stage 5 (consolidation). The AST lint rule was implicit in Stage 3. Corrected ordering:

| Original | Corrected | Rationale |
|----------|-----------|-----------|
| Stage 1: Fix formulas | Stage 1: Fix formulas | No change |
| Stage 2: Tag verification | Stage 2: Tag verification | No change |
| Stage 7: Module registry + enforcer | **Stage 3: Module registry + enforcer** | Needed before consolidation (Stage 5) |
| Stage 3: Silent exceptions | **Stage 4: Silent exceptions** | AST lint rule built first, then cleanup |
| Stage 4: Consolidate | **Stage 5: Consolidate** | Requires Stage 3 registry |
| Stage 5: Delete dead code | **Stage 6: Delete dead code** | After consolidation identifies what's truly dead |
| Stage 6: Wire connections | **Stage 7: Wire connections** | After consolidation ensures single sources |
| Stage 8: Invariant checker | **Stage 8: Invariant checker** | No change |

---

## Session Contracts

Each contract specifies exactly what an AI session (with no memory between sessions) reads, does, validates, commits, and hands off.

### Stage 1: Fix Wrong Formulas (3-5 sessions)

**Pre-read:** CLAUDE.md, docs/s318_deep_audit.md (bug list C01-C20, H01-H12), docs/s317_full_audit.md

**Scope:** Fix 42 objectively wrong formulas. No new files. No architecture changes. 1-10 lines each.

**Execution order (primitives first, consumers second):**
1. Cancer yogakaraka scoring.py:115 — Venus to Mars
2. Mars aspects multi_axis_scoring.py:173, feature_decomp.py:352, scoring_v2.py:168 — {3,9} to {3,7}
3. Jupiter aspects scoring_v2.py:169 — {4,6,9} to {4,8}
4. Sunapha/Anapha swap yogas_extended.py:207-226
5. Vesi/Vasi swap yogas_extended.py:309-331
6. Rajju/Musala/Nala yogas_extended.py:85-101 — sign modality not house
7. Baladi even-sign reversal avastha.py:75-89
8. Shadbala Tribhaga day lords shadbala.py:353 — Jupiter to Mercury
9. Shadbala Tribhaga night shadbala.py:357 — Moon/Venus swap
10. Drekkana Bala shadbala.py:722 — female to 2nd, neutral to 3rd
11. 9 divisional chart formulas in divisional_charts.py (D3, D4, D7, D10, D16, D20, D24, D45)
12. rule_firing.py:585-586, 601-602 — list-dropping
13. rule_firing.py:268-316 — MT degree ranges
14. Bhakut 5/9 kundali_milan.py:317
15. Tara Janma kundali_milan.py:73
16. Yoni Mrigashira/Ardra kundali_milan.py:78-79
17. 6 friendship errors kundali_milan.py:140-178
18. varshaphala hardcoded 1947
19. av_transit.py:76 AV lookup
20. data_minimisation.py:83 last_accessed column

**After each fix:** `.venv/bin/pytest tests/ -q --tb=short -x`
**Commit format:** `fix(SNNN): BUG-XXX [description] — BPHS Ch.N v.M`
**Abort:** If a fix causes >5 unrelated failures, stop and investigate.

### Stage 2: Tag Verification Levels (1 session)

**Pre-read:** CLAUDE.md, architecture spec (canonical primitives table), s318 audit (which modules were PDF-verified)

**Scope:** Add `_VERIFICATION` dict to every module in src/calculations/. No logic changes.

**Format:**
```python
_VERIFICATION = {"level": "bphs_pdf", "reference": "Ch.3 v.47-48", "session": "S317"}
```

**Execution:** Tag 9 canonical sources as `bphs_pdf`. Tag formula-compared modules. Tag rest as `unverified`.
**Validation:** `grep -rL "_VERIFICATION" src/calculations/*.py` returns empty.
**Commit:** `chore(SNNN): tag verification levels on all src/calculations/ modules`

### Stage 3: Build Module Registry + Import Boundary Enforcer (2-3 sessions)

**Pre-read:** CLAUDE.md, architecture spec (canonical primitives table, anti-spaghetti criterion), s318 audit (duplication counts)

**Scope:** Create src/MODULE_REGISTRY.py and tools/import_boundary_check.py.

**MODULE_REGISTRY.py structure:**
```python
REGISTRY = {
    "house_lord": {"layer": 3, "tier": 2, "purpose": "Sign lords and house classification", "canonical_for": ["sign_lords", "house_classification"], "verification": "bphs_pdf"},
    # ... one entry per module
}
PROTECTED_CONSTANTS = {
    "sign_lords": "house_lord",
    "exaltation": "dignity",
    # ... one entry per concept
}
```

**import_boundary_check.py:** Regex scan for inline definitions of protected constants outside canonical sources. Also validates import direction (no layer N importing from layer N+1).

**Validation:** Run enforcer — MUST report violations (pre-consolidation). Verify it catches known duplicates (Mars aspects in multi_axis_scoring, sign lords in scoring.py).
**Commit:** `feat(SNNN): MODULE_REGISTRY + import boundary enforcer`

### Stage 4: Eliminate Silent Exception Handlers (2-3 sessions)

**Pre-read:** CLAUDE.md, s318 audit (silent exception handlers section)

**Scope:** Build tools/lint_silent_except.py FIRST, then fix 143 violations.

**Lint rule:** AST-based. Rejects except blocks without logger/raise/warnings.warn. Allows except SpecificError.
**Fix priority:** Programming errors (raise), expected failures (log + sentinel), UI errors (st.error already shown).
**Validation:** `python tools/lint_silent_except.py` exits 0.
**Commit:** `fix(SNNN): eliminate 143 silent exception handlers, add AST lint`

### Stage 5: Consolidate to Canonical Primitives (5-8 sessions)

**Pre-read:** CLAUDE.md, src/MODULE_REGISTRY.py (from Stage 3), architecture spec (consolidation map)

**Scope:** One concept at a time. Only consolidate to bphs_pdf or formula_compared modules.

**Order (least consumers to most):**
1. Yogakarakas (4 copies)
2. Exaltation/debilitation (8+ copies)
3. Natural malefic/benefic (14 sets)
4. Kendra/trikona/dusthana (20+ copies)
5. Aspects (21 functions)
6. Sign lords (17 copies)

**Per concept:** Verify canonical source verification tag → grep for copies → replace with import → test → commit.
**Validation:** `python tools/import_boundary_check.py` exits 0 after all concepts done.
**Abort:** If canonical source is tagged `unverified`, do NOT consolidate that concept.

### Stage 6: Delete Dead Code (2-3 sessions)

**Pre-read:** CLAUDE.md, s318 audit (dead code sections), MODULE_REGISTRY

**Scope:** Delete ~22,692 lines across ~151 files. Move roadmap-relevant modules to src/archive/.

**Execution:** Build import graph → cross-reference with audit → verify each module truly unreachable → delete or archive → update MODULE_REGISTRY → fix broken test imports.
**Validation:** `find src/ -name "*.py" | xargs wc -l | tail -1` shows ~156,000 lines.

### Stage 7: Wire Missing Connections (2-3 sessions)

**Pre-read:** CLAUDE.md, src/scoring.py (full file), src/calculations/multi_axis_scoring.py, src/calculations/dignity.py, s318 audit (DD01, DD02)

**Scope:** Three changes:
1. Wire dignity into scoring (add R24, ~10 lines)
2. Deprecate score_all_axes() (add warnings.warn, migrate consumers)
3. Fix varga imports (all consumers use varga.py, not divisional_charts.py)

**R24 implementation:** After R22 in score_chart() loop:
```python
r24_score = DIGNITY_SCORE.get(dignities[bhavesh].dignity, 0.0)
rules.append(RuleResult("R24", f"Bhavesh dignity ({dignities[bhavesh].dignity.value})", r24_score, triggered=r24_score != 0.0))
```

**Snapshot update:** India 1947 scores will change. Update test expected values with pytest.approx.
**Deprecation:** Add DeprecationWarning to score_all_axes(). Do not delete yet.

### Stage 8: Build Runtime Invariant Checker (1-2 sessions)

**Pre-read:** CLAUDE.md, architecture spec (criterion 20), house_lord.py, dignity.py

**Scope:** Create src/invariants.py with 5 invariants. Wire into compute pipeline.

**Invariants:** Planet placement (sign 0-11, house 1-12), lordship uniqueness, aspect strength >= 0, dignity enum valid, house count = 12.
**Wiring:** Call check_chart_invariants() after Layer 3, before Layer 4 in score_chart().
**Validation:** India 1947 produces 0 violations.

---

## Enforcement Tool Specifications

### tools/import_boundary_check.py
- **Input:** src/MODULE_REGISTRY.py (canonical sources + protected constants)
- **Scans:** All .py in src/ for inline definitions matching protected patterns
- **Checks:** Layer direction (no N importing N+1), tier direction within Layer 3
- **Output:** Violations with file:line:concept:canonical_source. Exit 1 on violation.
- **Size:** ~150-200 lines. **Built in:** Stage 3.

### src/MODULE_REGISTRY.py
- **Structure:** Python dict. Fields: layer, tier, purpose (one sentence), canonical_for, verification, bphs_ref, max_lines.
- **Consumed by:** import_boundary_check.py, developers ("where is X?")
- **Size:** ~350 lines (80 structure + 5 per module x ~50 modules). **Built in:** Stage 3.

### tools/lint_silent_except.py
- **Rejects:** except blocks with no logger/raise/warnings.warn. except Exception: pass. Broad catch where exception variable is unused.
- **Allows:** except SpecificError. Blocks with logging. Blocks with raise.
- **Size:** ~60-80 lines. **Built in:** Stage 4 (first step).

### tools/lint_float_assert.py
- **Catches:** `assert x == 3.14` without pytest.approx in tests/ files
- **Size:** ~30-40 lines. **Built in:** Stage 4 (alongside silent except lint).

### tools/benchmark_chart.py
- **Measures:** Layer 1-5 time individually + end-to-end. 10 iterations, median + p95.
- **Thresholds:** End-to-end < 200ms median, < 500ms p95.
- **Size:** ~80-100 lines. **Built in:** Stage 3 (with other CI tooling).

### src/invariants.py
- **Invariants:** Planet placement, lordship uniqueness, aspect non-negative, dignity valid, house count.
- **Behavior:** Dev mode: raises. Prod mode: logs + continues.
- **Size:** ~80-120 lines. **Built in:** Stage 8.

---

## Stage 7 Expansion: Scoring Engine Resolution

### Both engines analyzed

**score_chart()** (scoring.py): 22 R-rules, D1 natal only, correct Mars aspects, per-rule RuleResult traceability, rho=0.31. Ignores dignity except for combustion (R19).

**score_all_axes()** (multi_axis_scoring.py): 23 R-rules, 5 axes (D1/CL/SL/D9/D10), WRONG Mars aspects {3,9}, 8 inline constant copies, no per-rule traceability, rho=0.13.

### Decision: score_chart() survives

Rationale: Better empirical performance (rho 0.31 vs 0.13), correct aspects, per-rule traceability (needed for Phase A), imports from canonical sources. Its valuable features (multi-axis, functional roles) get absorbed incrementally post-Stage 7.

### R24 dignity wiring (~10 lines in scoring.py)
After R22 in the house loop, add DIGNITY_SCORE lookup for bhavesh. Exalted bhavesh: +1.5 to +2.0. Debilitated: -1.5. Own sign: +0.75. This is the single highest-impact correctness improvement.

### Deprecation timeline
- Stage 7: All consumers migrated to score_chart(). DeprecationWarning added to score_all_axes().
- Stage 8+: score_all_axes() deleted. multi_axis_scoring.py moved to src/archive/.

---

## Testing Strategy

### Current state
14,740 test invocations, 193 files, 3 fake tests, 107 exact float assertions, 5 critical coverage gaps (dignity in scoring, list conditions, Yoni mapping, KP Placidus, D9 cross-validation).

### Pyramid
- Level 1 (unit): Each canonical primitive function exhaustively tested. sign_lord() for all 12 signs. is_kendra() for all 12 houses. Dignity for all 7 planets x all levels.
- Level 2 (integration): Given a chart, verify Layer 3 derived facts are correct. Given a chart + rule, verify Layer 4 evaluation is correct.
- Level 3 (end-to-end): Full pipeline birth data to ChartScores. Minimum 3 chart fixtures with snapshots.

### Regression snapshot strategy
- `tests/snapshots/india_1947_scores.json`: All 12 house scores + rules fired.
- When a bug fix intentionally changes scores, commit updates the snapshot with explanation.
- Accidental changes caught by failing snapshot test.
- All snapshot assertions use pytest.approx(tolerance=0.01).

---

## Scoring Rubric

- **5/5** = Implemented, tested, enforced in CI. Exists in code today.
- **4/5** = Designed with implementation spec, dependencies identified. Partial implementation exists. < 3 sessions to complete.
- **3/5** = Problem identified, solution described with actionable detail. No implementation yet.
- **2/5** = Problem identified, solution direction proposed but underspecified.
- **1/5** = Problem mentioned but not substantively addressed.

### Honest re-score (v11 AS WRITTEN, not as planned)

| # | Criterion | Self-Scored | Honest | Gap |
|---|-----------|-----------|--------|-----|
| 1 | Simplicity | 5 | **4** | Model sound, enforcement unbuilt |
| 2 | Robustness | 5 | **3** | 143 handlers identified, lint rule unbuilt |
| 3 | Testability | 5 | **3** | Strategy described, infrastructure unbuilt |
| 4 | Modularity | 5 | **3** | Registry described, not created |
| 5 | Prediction Quality | 4 | **2** | Dignity wiring described, not done |
| 6 | Anti-Spaghetti | 5 | **3** | Enforcer described, not built |
| 7 | Domain Fidelity | 5 | **3** | Tags described, not added |
| 8 | Evolvability | 5 | **2** | Checklists described, not written |
| 9 | Explainability | 5 | **3** | Richer RuleResult described, not implemented |
| 10 | Developer Experience | 5 | **3** | Registry described, not created |
| 11 | Reproducibility | 5 | **3** | Snapshots described, not built |
| 12 | Observability | 5 | **2** | Logging described, not added |
| 13 | Data Sensitivity | 4 | **2** | Fixes identified, not done |
| 14 | Cost of Change | 5 | **3** | Depends on consolidation (Stage 5) |
| 15 | Knowledge Preservation | 5 | **4** | Verse audits exist, builder validates |
| 16 | Performance | 4 | **3** | Benchmark described, not built |
| 17 | Interoperability | 5 | **3** | JSON works in practice, no schema versions |
| 18 | Concurrency | 4 | **3** | Stateless in practice, no lint check |
| 19 | Versioning | 5 | **2** | Three axes designed, zero implemented |
| 20 | Runtime Correctness | 5 | **2** | Invariant checker designed, not built |
| | **Total** | **96** | **55** | Plan → Implementation gap |

The 55/100 is the spec's honest score as a PLAN. After Stages 1-4 complete, expect ~70. After all 8 stages, expect ~90. The remaining ~10 points require Phase A/B work.
