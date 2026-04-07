# LagnaMaster Canonical Architecture — v10

**Date:** 2026-04-07 (S318)
**Status:** Updated with S318 audit findings + migration sequence
**Supersedes:** v9 (S317) — pipeline and graph schema unchanged, migration plan rewritten
**Context:** S318 deep audit found 104 deduplicated bugs across 660 files / 178,072 lines

---

## What Changed from v9

v9 designed the target architecture (6-layer graph pipeline). v10 adds:
1. **Pre-graph migration sequence** informed by 104 audit bugs
2. **Verification discipline** — each module tagged with actual verification level
3. **Consolidation map** — which module is canonical for each concept
4. **Tech debt reduction targets** — every step deletes files/lines, codebase shrinks monotonically

v9's pipeline, graph schema, data contracts, multi-school model, and worked example are **unchanged**. This document focuses on HOW to get there safely.

---

## Why v9's Migration Plan Was Insufficient

v9 proposed:
```
Phase 1: Graph-as-Chart (adapters, feature flag, parity checks)
Phase 2: Rule IR (declarative DSL, physical restructuring)
```

S318 revealed this would build a graph on broken foundations:

| Problem | v9 Assumed | S318 Found |
|---------|-----------|------------|
| Core formulas | Correct | 42 wrong formulas (Shadbala Tribhaga, 9 wrong vargas, aspect bugs) |
| Single source of truth | Mostly there | 17 sign lord copies, 14 malefic sets, 20+ kendra defs |
| Scoring uses dignity | Yes | **No** — dignity computed but never affects score |
| One scoring engine | Yes | **Two** parallel engines with different bugs |
| Divisional charts | Correct | Scoring engine uses **wrong module** (9 of 16 vargas wrong) |
| Corpus rules fire | Most | **58.5% cannot fire**, only 23 of 7,412 wired |
| Rule engine sound | Yes | 5 HIGH bugs (list-dropping, MT ignores degrees, timing no-op) |

Building Graph-as-Chart on this foundation would produce: a perfectly consistent system that is consistently wrong.

---

## Revised Migration: 6 Steps

```
Step 1: Fix provably wrong formulas (no architecture change)
Step 2: Tag verification levels (discipline, no code change)
Step 3: Consolidate verified primitives (delete copies, reduce tech debt)
Step 4: Wire missing connections (minimal surgery)
Step 5: Delete dead code (22,692 lines across 151 files)
Step 6: Build graph on corrected, consolidated, slimmer codebase (v9 Phase 1+2)
```

Each step is independently valuable. Each reduces the codebase. No step requires a later step to be useful. The graph is the destination, not the prerequisite.

---

### Step 1: Fix Provably Wrong Formulas

**Scope:** Bugs where the formula itself is objectively incorrect per BPHS PDF verification. Not duplication fixes (Step 3), not wiring fixes (Step 4).

**What gets fixed:**

| Bug ID | File:Line | Fix | BPHS Reference |
|--------|----------|-----|----------------|
| BUG-001 | multi_axis_scoring.py:173 | Mars `{3,9}` → `{3,7}` | Ch.26 v.2-5 p.254 |
| BUG-001 | feature_decomp.py:352 | Mars `{3,9}` → `{3,7}` | Ch.26 v.2-5 p.254 |
| BUG-002 | scoring_v2.py:168 | Mars `{3,7,9}` → `{3,7}` | Ch.26 v.2-5 p.254 |
| BUG-003 | scoring_v2.py:169 | Jupiter `{4,6,9}` → `{4,8}` | Ch.26 v.2-5 p.254 |
| BUG-009 | avastha.py:75-89 | Add even-sign reversal for Baladi | Ch.45 v.3 p.449 |
| BUG-010 | avastha.py:70-71 | Vriddha 0.50→0.125, Mrita 0.10→0.0 | Ch.45 v.4 p.449 |
| BUG-011 | avastha.py:112 | Lajjitadi: apply to any planet, not just 5th lord | Ch.45 v.11-18 p.451 |
| BUG-024 | shadbala.py:353 | Tribhaga day: Jupiter→Mercury | Ch.27 v.12 p.269 |
| BUG-025 | shadbala.py:357 | Tribhaga night: Moon/Venus→Venus/Moon | Ch.27 v.12 p.269 |
| BUG-028 | shadbala.py:722 | Drekkana: female→2nd drk, neutral→3rd drk | Ch.27 v.6 p.266 |
| BUG-029 | divisional_charts.py:254 | D3: element-based→trikona | Ch.6 v.7-8 p.69 |
| BUG-030 | divisional_charts.py:137 | D4: consecutive→kendras | Ch.6 v.9 p.70 |
| BUG-031 | divisional_charts.py:245 | D10: si*10→si+k (odd), si+9+k (even) | Ch.6 v.13-14 p.73 |
| BUG-032 | divisional_charts.py:164 | D20: odd/even→modality | Ch.6 v.17-21 p.76 |
| BUG-033 | divisional_charts.py:176 | D24 even: Sag(8)→Cancer(3) | Ch.6 v.22-23 p.77 |
| BUG-034 | divisional_charts.py:221 | D45: si%3 wrong bases→modality | Ch.6 v.31-32 p.81 |
| BUG-016 | divisional_charts.py:265 | D7: fix zero-falsy and/or | Ch.6 v.10-11 p.71 |
| BUG-017 | divisional_charts.py:144 | D16: si%4→modality mapping | Ch.6 v.16 p.74 |
| BUG-035 | rule_firing.py:585-586 | planet_not_in_house: use full list | — |
| BUG-036 | rule_firing.py:601-602 | planet_not_aspecting: use full list | — |
| BUG-037 | rule_firing.py:268-316 | MT: add degree range checks | Ch.3 v.51-54 p.39 |
| BUG-050 | scoring.py:115 | Cancer yogakaraka: Venus→Mars | Ch.34 v.27 p.352 |
| BUG-006 | yogas_extended.py:213-240 | Sunapha/Anapha: swap assignments | Standard definition |
| BUG-007 | yogas_extended.py:315-331 | Vesi/Vasi: swap assignments | Standard definition |
| BUG-008 | yogas_extended.py:85-101 | Rajju/Musala/Nala: sign_index%3 not house | Standard definition |
| BUG-013 | kundali_milan.py:317 | Bhakut: remove 5,9 from penalty set | Standard Muhurta |
| BUG-057 | kundali_milan.py:73 | Tara: Janma group 1 → 0 points | Standard Muhurta |
| BUG-058 | kundali_milan.py:78-79 | Yoni: Mrigashira→serpent, Ardra→dog | Muhurta Chintamani |
| BUG-056 | kundali_milan.py:140-178 | 6 friendship errors in Graha Maitri | Ch.3 v.55 p.40 |
| BUG-039 | varshaphala.py | Solar return: remove hardcoded 1947 | — |
| BUG-040 | av_transit.py:76 | AV lookup: getattr→planet_av.get | — |
| BUG-066 | privacy/data_minimisation.py:83 | last_accessed column query | — |

**What does NOT get fixed here:** Duplication (Step 3), missing wiring (Step 4), dead code (Step 5), architecture flaws (Step 6). Each has its own step.

**Exit criteria:** All modified files pass `ruff check` + `pytest`. Each fix cites BPHS verse in commit message. No net new files.

**Estimated effort:** 3-5 sessions. Each fix is 1-10 lines.

---

### Step 2: Tag Verification Levels

**Purpose:** Prevent consolidation of unverified modules. Make confidence levels explicit in code, not just in the audit document.

**Implementation:** Each canonical-candidate module gets a module-level constant:

```python
# Verification levels (from S318 audit):
#   "bphs_pdf" — formula compared value-by-value against BPHS Santhanam PDF, verse cited
#   "formula_compared" — logic compared across multiple implementations, correctness inferred
#   "pattern_scanned" — checked for stale constants and exception patterns, formula not verified
#   "unverified" — read but no correctness assessment made
_VERIFICATION = "bphs_pdf"  # Ch.3 v.55 p.40, all 42 pairs
```

**Modules and their verified levels (from S318):**

| Module | Level | What Was Verified |
|--------|-------|-------------------|
| house_lord.py | bphs_pdf | Sign lords, is_kendra/trikona/dusthana |
| dignity.py (core tables) | bphs_pdf | EXALT_SIGN, DEBIL_SIGN, OWN_SIGNS, MT_RANGES, _NAISARGIKA (42 pairs), PARAMOTCHA_DEGREE |
| dignity.py (NB logic) | formula_compared | 6 conditions cross-checked across modules |
| functional_dignity.py (tables) | bphs_pdf | KNOWN_YOGAKARAKAS (12 lagnas), KNOWN_FUNCTIONAL_MALEFICS (12 lagnas) |
| functional_dignity.py (algorithm) | pattern_scanned | compute_functional_classifications() not verified against edge cases |
| varga.py | bphs_pdf | D1-D12, D60 formulas vs Ch.6 |
| avasthas.py | bphs_pdf | Baladi reversal, Jagradadi, Lajjitadi vs Ch.45 |
| sputa_drishti.py | bphs_pdf | Speculum + special aspects vs Ch.26 v.9-12 |
| panchadha_maitri.py | bphs_pdf | Friendship computation vs Ch.3 notes |
| shadbala.py (Kendradi, Naisargika, thresholds) | bphs_pdf | Ch.27 v.5, v.14, v.32-33 |
| shadbala.py (Tribhaga, Chesta, Hora, Drekkana) | bphs_pdf | **WRONG — fixed in Step 1** |
| ashtakavarga.py (BAV matrices) | bphs_pdf | Sun/Mercury/Jupiter/Venus rows vs Ch.66-72 |
| rule_firing.py | formula_compared | All 33 branches logic-checked |
| scoring.py | formula_compared | All 22 R-rules traced end-to-end |
| multi_axis_scoring.py | formula_compared | Full R-rule analysis, consumer tracing |
| kp.py | formula_compared | Sub-lord tables, significator logic |
| kundali_milan.py | formula_compared | All 8 kootas checked (bugs found, fixed in Step 1) |
| functional_roles.py | pattern_scanned | Algorithm checked, edge cases not verified |
| diagnostic_scorer.py | pattern_scanned | Own tables, 0 tests |
| All other src/calculations/ | pattern_scanned or unverified | See S318 audit for per-file status |

**Exit criteria:** Every module in `src/calculations/` has `_VERIFICATION` constant. No code behavior changes.

**Estimated effort:** 1 session.

---

### Step 3: Consolidate Verified Primitives

**Rule:** Only consolidate modules tagged `bphs_pdf` or `formula_compared`. Modules tagged `pattern_scanned` or `unverified` keep their local copies until independently verified.

**Consolidation map:**

| Concept | Canonical Source | Copies to Delete/Redirect | Safe? |
|---------|-----------------|--------------------------|-------|
| Sign lords | `house_lord.sign_lord()` | 17 inline `_SIGN_LORD` dicts | YES (bphs_pdf) |
| `is_kendra/trikona/dusthana` | `house_lord.py` functions | 20+ inline `_KENDRA` sets, 15+ `_DUSTHANA` sets | YES (bphs_pdf) |
| Exaltation signs | `dignity.EXALT_SIGN` | 8+ inline copies | YES (bphs_pdf) |
| Debilitation signs | `dignity.DEBIL_SIGN` | 8+ inline copies | YES (bphs_pdf) |
| Own signs | `dignity.OWN_SIGNS` | 7+ inline copies | YES (bphs_pdf) |
| MT ranges | `dignity.MOOLTRIKONA_RANGES` | rule_firing._MT_SIGNS (sign-only, no degrees) | YES (bphs_pdf) |
| Friendship table | `dignity._NAISARGIKA` | panchadha_maitri, friendship.py, sayanadi_full.py copies | YES (bphs_pdf, all 42 pairs) |
| Yogakarakas | `functional_dignity.KNOWN_YOGAKARAKAS` | scoring.py._YOGAKARAKA_MAP, multi_lagna._YOGAKARAKA | YES (bphs_pdf) |
| Functional malefics | `functional_dignity.KNOWN_FUNCTIONAL_MALEFICS` | — | YES (bphs_pdf) |
| Natural benefic/malefic | `rule_firing.is_natural_malefic()` (chart-aware) | 14 static `_NAT_MALEFIC` sets | PARTIAL — function is formula_compared but callers need case-by-case review |
| Aspect houses (Mars/Jup/Sat) | `sputa_drishti._SPECIAL_ASPECT_HOUSES` | 21 inline aspect dicts | YES (bphs_pdf) |
| Varga formulas | `varga.py` | `divisional_charts.py` (to be fixed in Step 1, then deprecated) | YES (bphs_pdf) |
| Avastha (Baladi/Jagradadi/Lajjitadi) | `avasthas.py` | `avastha.py`, `planet_avasthas.py` (both wrong/dead) | YES (bphs_pdf) |
| Avastha multipliers | **NOT SAFE TO CONSOLIDATE** | 3 conflicting sets, BPHS says "negligible"/"nil" not exact numbers | NO — keep avasthas.py values (closest to BPHS), document uncertainty |
| Sthir Karaka table | **NOT SAFE TO CONSOLIDATE** | 4 versions disagree on H4/H9/H10 | NO — needs BPHS Ch.32 verification |

**Implementation:** For each safe row: change inline constant to `from src.calculations.house_lord import sign_lord` (or equivalent). Delete the inline dict. Run tests.

**What gets deleted:**
- `friendship.py` (142 lines, dead, replaced by panchadha_maitri.py)
- `planet_avasthas.py` (271 lines, dead, replaced by avasthas.py)
- `sayanadi_full.py` (256 lines, dead, replaced by avasthas.py)
- ~200 lines of inline constants across 40+ files

**Exit criteria:** No two files define the same constant for any concept in the "Safe" column. All tests pass.

**Estimated effort:** 3-5 sessions. Mechanical search-and-replace per concept.

---

### Step 4: Wire Missing Connections

**Scope:** Make existing correct computations actually affect the output. Minimal surgery — not a rewrite.

**4A: Wire dignity into scoring**

BUG-081: `score_chart()` calls `compute_all_dignities()` but only uses the result for R19 (combustion). The `DIGNITY_SCORE` dict exists but is never read.

**Fix:** Add a new R-rule (or modify R04) that applies dignity_score to bhavesh:
```python
# R04 already checks bhavesh placement. Add dignity modifier:
dignity_bonus = DIGNITY_SCORE.get(dignities[bhavesh].level, 0)
```

This is a 5-10 line change in `scoring.py`. It makes exalted bhavesh score higher than debilitated bhavesh — the single most impactful correctness improvement possible.

**4B: Resolve scoring engine split**

BUG-082: `score_chart()` and `score_all_axes()` are parallel engines. The UI uses `score_chart()` (correct Mars aspects, no dignity). The v3 API uses `score_all_axes()` (wrong Mars aspects, wrong D9 lagna, uses functional_roles).

**Decision needed:** Which engine survives?

| Option | Pros | Cons |
|--------|------|------|
| Keep `score_chart()`, deprecate `score_all_axes()` | Known rho=0.31 (calibrated), correct aspects, simpler | No multi-axis (D9/D10/CL/SL), no functional roles |
| Keep `score_all_axes()`, fix its bugs | Multi-axis, richer signal, more extensible | rho=0.13 (uncalibrated), more bugs to fix |
| Merge: `score_chart()` absorbs multi-axis features | Best of both | Larger single function, needs careful integration |

**Recommendation:** Keep `score_chart()` as primary, add dignity wiring (4A). Deprecate `score_all_axes()` as a separate engine — its useful features (multi-axis D9/D10 weighting) get absorbed into `score_chart()` incrementally in the graph migration (Step 6). This follows L016: "don't replace working systems from scratch."

**4C: Fix scoring varga module**

BUG-083: `scoring_v3.py` imports from `divisional_charts.py` (9 wrong formulas). After Step 1 fixes those formulas, this is no longer a critical bug. But for long-term cleanliness, `scoring_v3.py` should import from `varga.py` (the correct, UI-used module). One import change.

**Exit criteria:** Dignity affects house scores. One scoring engine is primary. Varga imports are consistent. All tests pass (test values may change — that's expected).

**Estimated effort:** 2-3 sessions.

---

### Step 5: Delete Dead Code

S318 import graph analysis identified 22,692 lines across 151 files unreachable from production:

| Category | Files | Lines |
|----------|-------|-------|
| Dead calculations modules | 27 (after Step 3 deletions) | ~3,600 |
| Dead subsystems (interfaces, CI, research, ML, feedback, privacy) | 33 | 2,857 |
| Dead corpus infrastructure | 14 | 1,750 |
| Dead API routers (never mounted) | 4 | 352 |
| Dead guidance modules | 2 | 196 |
| Tools archive | 140 | 11,063 |
| **Total** | **~220** | **~19,818** |

**Approach:** Delete in batches by category. Each batch is one commit. Run full test suite after each batch — any test that breaks reveals a hidden import path the analysis missed.

**What to preserve:** Modules that are dead NOW but on the ROADMAP for future activation (e.g., `jaimini_full.py` for Phase 2 Jaimini school). Move to `src/archive/` with a note, don't delete.

**Exit criteria:** Only production-reachable code in `src/`. `tools/archive/` retained as-is (historical, already sequestered).

**Estimated effort:** 2-3 sessions.

---

### Step 6: Build Graph (v9 Phase 1 + Phase 2)

**Now the graph can be built safely because:**
- Core formulas are BPHS-verified and fixed (Step 1)
- Each module's verification level is explicit (Step 2)
- Each concept has exactly one canonical source (Step 3)
- Dignity flows into scoring (Step 4)
- Dead code is gone — smaller surface area to migrate (Step 5)

**v9's graph architecture is unchanged:**
- 6-layer pipeline (Astronomy → Conventions → Graph → Rules → Aggregation → Output)
- 4-tier graph (Structural → Derived → Interpretive → Evaluative/Lazy)
- Multi-school, multi-lagna, multi-varga
- Data contracts, query API, edge semantics as specified in v9

**Graph migration sequence:**
1. Create `src/graph/` with ChartGraph, builders, query API
2. Adapters: `score_chart(chart)` internally builds graph, delegates to graph queries
3. Feature flag: old path vs graph path, both run during migration, assert parity
4. Parity baseline: the corrected `score_chart()` output (from Steps 1-4) is the reference. Graph must match or explain divergences.
5. Incremental: migrate one concept at a time (lordships first, then aspects, then dignity, then shadbala)

**Exit criteria (same as v9):**
- 100% rules evaluate via graph
- Zero duplicated relationship logic
- Snapshot parity (zero deviation from corrected baseline)
- All tests passing
- Graph construction < 10ms (benchmarked)

**Estimated effort:** 30-50 sessions (as v9 estimated).

---

## Phase 2: Rule IR (Declarative Rule Language)

v9 had a 3-line stub for Phase 2. S318 audit data makes a real spec possible.

### Why a Rule IR

The current rule engine (`rule_firing.py`, 1,442 lines) is a procedural `if/elif` chain with 33 condition branches. S318 found:
- 5 HIGH bugs in the procedural logic (list-dropping, MT ignores degrees, timing no-op, dispositor inconsistency, unreachable lagna-scoped block)
- 33 condition types but only 12 used by V2 rules — 21 are speculative infrastructure
- Systematic corpus encoding errors that the procedural engine can't prevent (aspect-vs-occupation confusion, OR-vs-AND, relative-vs-absolute houses)
- `_is_activated` is a complete no-op — timing was designed but never implemented

A declarative Rule IR makes these bugs **structurally impossible** rather than relying on correct procedural code.

### What the Rule IR Is

A typed pattern language that expresses rule conditions as graph queries. Rules are data (not code), validated at encode-time, and executed by a single generic graph-pattern-matcher.

```python
# Current procedural (rule_firing.py):
if ctype == "lord_in_house":
    lord = _SIGN_LORDS[(chart.lagna_sign_index + int(cond["house"]) - 1) % 12]
    target_house = cond.get("target_house", [])
    # ... 20 lines of manual lookup, error handling, binding

# Rule IR (declarative):
RulePattern(
    bind={"P": lord_of(house=5)},
    match=[in_house("P", house=9)],
    require=[dignity("P", min="own_sign")],  # optional strength gate
)
```

### Condition Primitives (from audit data)

S318 traced which condition types are actually used by the 591 V2 rules and which produce correct results. The IR needs primitives for each, mapped to graph queries.

**Tier 1 — Core (12 types, used by V2 rules, graph-native):**

| IR Primitive | Graph Query | Current ctype | Used by V2 | S318 Status |
|-------------|-------------|---------------|-----------|-------------|
| `in_house(planet, house)` | `has_edge(IN_HOUSE, P, H)` | `planet_in_house` | YES | Correct |
| `in_sign(planet, sign)` | `has_edge(IN_SIGN, P, S)` | `planet_in_sign` | YES | Correct |
| `lord_of(house) → planet` | `follow(LORDS_HOUSE, H)` | `lord_in_house` | YES | Correct |
| `lord_in_sign(house, sign)` | `follow(LORDS_HOUSE, H)` then `has_edge(IN_SIGN, P, S)` | `lord_in_sign` | YES | Correct |
| `dignity(planet, level)` | `node(P).dignity.level` | `planet_dignity` | YES | Correct (but MT ignores degrees — BUG-037 fixed in Step 1) |
| `aspects(planet, target)` | `has_edge(ASPECTS_HOUSE, P, H)` or `has_edge(ASPECTS_PLANET, P, Q)` | `planet_aspecting` | YES | Correct |
| `conjunct(planet_a, planet_b)` | `has_edge(CONJUNCT, A, B)` | `planets_conjunct` | YES | Correct |
| `not_in_house(planet, houses)` | `NOT has_edge(IN_HOUSE, P, H) for H in houses` | `planet_not_in_house` | YES | **BUG-035: list-dropping. IR uses typed list, eliminates bug.** |
| `not_aspecting(planet, houses)` | `NOT has_edge(ASPECTS_HOUSE, P, H) for H in houses` | `planet_not_aspecting` | YES | **BUG-036: same list bug. Fixed by IR typing.** |
| `navamsa_sign(planet, sign)` | Query VargaGraphSet D9 | `planet_in_navamsa_sign` | YES | Correct |
| `house_sign_nature(house, nature)` | `follow(H, IN_SIGN).lord` then `is_natural_malefic` | `house_sign_nature` | YES | Correct |
| `parivartana(house_a, house_b)` | Mutual `lord_of(A) in B` and `lord_of(B) in A` | `parivartana` | YES | Correct |

**Tier 2 — Derived (8 types, used by V2 rules, require multi-hop):**

| IR Primitive | Graph Query | Current ctype |
|-------------|-------------|---------------|
| `in_house_from(planet, ref_planet, offset)` | Relative house computation | `planet_in_house_from` |
| `dispositor_of(planet) → planet` | `follow(IN_SIGN, P)` then `follow(LORDS, S)` | `dispositor_condition` |
| `or_group([pattern_a, pattern_b])` | Any sub-pattern matches | `or_group` |
| `count_with_state(state, min, max)` | Iterate planets, filter by dignity/sign | `count_planets_with_state` |
| `functional_role(planet, role)` | `node(P).functional_role` | `functional_benefic` |
| `derived_house(base, offset, target)` | `resolve_house(base + offset)` | `derived_points_relationship` |
| `argala(source, target, type)` | Argala edge query | `argala_condition` |
| `retrograde(planet)` | `node(P).is_retrograde` | `planet_retrograde` |

**Tier 3 — Evaluative (5 types, require Tier 4 lazy computation):**

| IR Primitive | Graph Query | Current ctype |
|-------------|-------------|---------------|
| `shadbala(planet, component, min)` | `graph.tier4(P).shadbala.component > min` | `shadbala_strength` |
| `moon_phase(phase)` | `(moon.lon - sun.lon) % 360` range check | `moon_phase` |
| `dynamic_karaka(planet, karaka)` | Chara Karaka lookup | `dynamic_karaka` |
| `lagna_sign_type(modality)` | Lagna sign % 3 | `lagna_sign_type` |
| `upagraha_in(upagraha, house)` | `has_edge(IN_HOUSE, U, H)` | `upagraha_in_house` |

**Dropped from current engine (8 types, zero V2 usage, speculative):**

| Current ctype | Why Dropped |
|---------------|-------------|
| `planets_conjunct_in_house` | Redundant: `conjunct(A, B)` + `in_house(A, H)` |
| `planet_nature` | Redundant: `functional_role` or `is_natural_malefic` |
| `planet_in_house_category` | Redundant: `in_house` + house classification function |
| `navamsa_lagna` | Fragile (`lagna_degree` ambiguity — BUG-007 in rule_firing). Replaced by `navamsa_sign(lagna, sign)` |
| `derived_house_sign` | Subsumable under `derived_house` + `in_sign` |
| `lord_of_derived_house` | Subsumable under `derived_house` + `lord_of` |
| `planet_from_derived_lord` | Subsumable under `derived_house` + `lord_of` + `in_house` |
| `planet_at_derived_point` | Subsumable under `derived_house` + `in_house` |

These 8 can be expressed as compositions of Tier 1-2 primitives. Keeping them as syntactic sugar is acceptable but they should NOT be separate branches in the evaluator — they should desugar to the composition before execution.

### How the IR Prevents Systematic Corpus Bugs

S318 found 5 systematic patterns in the V2 corpus. The IR addresses each:

**S1: Aspect vs Occupation Confusion**
Current: Encoder writes `planet_in_house` when verse says "conjunct OR aspected by."
IR fix: Separate primitives `in_house(P, H)` vs `aspects(P, H)` vs `in_house_or_aspects(P, H)`. The composite primitive makes the OR explicit. Encoder must choose — no default that silently picks one.

**S2: OR-vs-AND Logic Errors**
Current: Multiple conditions in a list are implicitly AND. Encoder puts OR alternatives into the same list.
IR fix: `or_group([pattern_a, pattern_b])` is an explicit primitive. AND is the default for a conditions list. The encoder MUST use `or_group` for alternatives — no way to accidentally AND them.

**S3: Relative-vs-Absolute House Positions**
Current: "trine FROM the 2nd lord" encoded as absolute houses `[1,5,9]`.
IR fix: `in_house_from(P, ref=lord_of(2), offset=[4,8])` expresses the relative position. The graph computes the actual house at evaluation time. The encoder writes the offset, not the resolved house.

**S4: Incomplete Multi-Condition Verses**
Current: Marriage timing rules encode only the first condition, silently drop the rest.
IR fix: IR validation requires `min_conditions` per verse complexity estimate. A verse with 3 stated conditions that encodes only 1 triggers a build-time warning (not a block — some conditions may be intentionally deferred as modifiers).

**S5: List-Valued Conditions Silently Truncated**
Current: `planet_not_in_house` drops all but first house from a list (BUG-035/036).
IR fix: `not_in_house(P, [6, 8, 12])` is a typed `list[int]`. The graph matcher iterates the full list. No `isinstance` check, no truncation — the type system enforces it.

### IR Validation Gates (encode-time)

The v2_builder currently has T1-14 through T1-18 gates but `mirror()` bypasses all of them (BUG-088). The IR builder replaces this:

| Gate | What It Checks | Current Status |
|------|---------------|----------------|
| IR-1 | Every primitive name is in the registered set | NEW (currently unchecked — unknown ctypes silently return False) |
| IR-2 | Every planet name is canonical (7 grahas + Rahu/Ketu + "lord_of_N" + "any_benefic/malefic") | Exists (T1-3) but has escape hatches |
| IR-3 | Every house reference is 1-12 or a typed list of 1-12 | NEW (currently no type check on house values) |
| IR-4 | `or_group` contains ≥ 2 alternatives | NEW |
| IR-5 | Relative references (`in_house_from`) have explicit `ref` — no absolute house fallback | NEW (prevents S3 pattern) |
| IR-6 | `not_in_house` and `not_aspecting` accept only `list[int]`, never single int | NEW (prevents BUG-035/036) |
| IR-7 | Mirror rules run through ALL validation gates (no bypass) | NEW (fixes BUG-088) |
| IR-8 | Entity target matches prediction entity (existing T1-17, kept) | Exists |
| IR-9 | Verse complexity estimate vs condition count (warning for S4 pattern) | NEW |

### IR Execution Model

```
1. Rule IR desugars composites into primitive graph queries
2. Each primitive maps to exactly one graph query method
3. Bindings propagate: bind={"P": lord_of(5)} makes P available to all subsequent patterns
4. All primitives in a rule's match list are AND'd (implicit conjunction)
5. or_group is the only way to express disjunction
6. Negation is explicit: not_in_house, not_aspecting (closed set, no generic NOT)
7. Evaluation order: bind → match → require (strength gates) → predict
8. Timing: require section can include temporal conditions (dasha period, age range)
   — replaces the current _is_activated no-op (BUG-048)
```

### Migration from Procedural to IR

Not a big-bang rewrite. Incremental:

1. **New V2 rules** (post-Phase 2 start) are encoded in IR syntax using the IR builder
2. **Existing V2 rules** (591) are auto-migrated: a script reads `primary_condition.conditions` and emits the equivalent IR pattern. Each auto-migrated rule is spot-checked.
3. **Existing V1 rules** with `placement_value` (~2,860 evaluable) are auto-migrated from `(planet, placement_type, placement_value)` to the equivalent IR primitive
4. **Phase 1A rules** (4,337 prose-only) are NOT migrated — they await V2 re-encoding per the corpus roadmap
5. **The 33-branch `if/elif` in rule_firing.py** is replaced by the generic graph pattern matcher. The old code is deleted once parity is confirmed.

### Timing Implementation (Replacing the No-Op)

BUG-048: `_is_activated` returns True always. The IR's `require` section supports temporal conditions:

```python
RulePattern(
    bind={"P": lord_of(5)},
    match=[in_house("P", house=9)],
    require=[
        timing(type="dasha", lord="P"),           # P must be running dasha lord
        timing(type="age", range=(32, 36)),        # native must be in age range
    ],
    predict=Prediction(domain="fortune", direction="positive"),
)
```

Timing conditions are optional. Rules without timing fire unconditionally (current behavior). Rules WITH timing fire only when the temporal context matches. This replaces the no-op with actual functionality without breaking existing rules.

### What Phase 2 Does NOT Include

- **Yoga detection as IR patterns.** Yogas (Raj Yoga, Gajakesari, etc.) are complex multi-step detections that don't fit cleanly into a single RulePattern. They remain as procedural functions (in `yogas.py`, which S318 confirmed is correct) that QUERY the graph. Future work may express simple yogas as IR templates, but this is not Phase 2 scope.
- **Scoring formula changes.** The IR is a rule evaluation mechanism, not a scoring mechanism. How rule results are weighted and aggregated into house scores is Layer 5 (Aggregation), unchanged from v9.
- **Multi-school aspect differences.** Parashari vs Jaimini aspects are already handled by the graph's school-tagged edges (v9 spec). The IR queries edges filtered by school — no IR-level school logic needed.

### Phase 2 Exit Criteria

- IR builder accepts all 25 primitives (12 core + 8 derived + 5 evaluative)
- All 9 IR validation gates (IR-1 through IR-9) enforced at encode-time
- All 591 V2 rules auto-migrated and spot-checked
- All ~2,860 evaluable V1 rules auto-migrated
- `rule_firing.py` 33-branch if/elif deleted
- Generic graph pattern matcher produces identical results to old engine on India 1947 fixture
- Timing conditions functional (at least dasha-period and age-range)
- Zero new condition types that aren't compositions of existing primitives

### Phase 2 Estimated Effort

- IR primitive definitions + graph query mappings: 3-5 sessions
- IR builder + validation gates: 2-3 sessions
- Auto-migration script + spot-checks: 3-5 sessions
- Graph pattern matcher: 5-8 sessions
- Timing implementation: 2-3 sessions
- Parity verification + old code deletion: 2-3 sessions
- **Total: 17-27 sessions** (within v9's S411-S470 allocation of 60 sessions)

---

## Corpus Repair (Parallel Track)

Not architecture work. Not blocked by Steps 1-6. Can run concurrently.

| Problem | Count | Fix |
|---------|-------|-----|
| Factual errors in V2 rules | 10 | Fix conditions per BPHS PDF (verse refs documented in S318) |
| Missing Ch.19 slokas | 9 of 15 | Encode from BPHS Vol 1 pp.169-172 |
| Systematic condition gaps (aspect vs occupation, OR→AND, relative→absolute) | ~40 rules | Re-encode per BPHS text |
| Marriage timing rules incomplete (Ch.18) | 9 of 11 | Add missing 2nd/3rd conditions |
| Phase 1A rules that can't fire (58.5%) | 4,337 | V2 re-encoding per BPHS encoding protocol |
| Fabricated claim (Ch.24a v.3) | 1 | Delete "no siblings lost" |
| Saravali SAV ID overrun (signs_5.py) | 1 | Fix header count |

**Estimated effort:** Corpus repair is the 1000-session roadmap. Each encoding session handles 1-2 chapters.

---

## Tech Debt Reduction Trajectory

| After Step | Files Deleted | Lines Removed | Codebase Size |
|------------|--------------|---------------|---------------|
| Start | 0 | 0 | 660 files, 178,072 lines |
| Step 1 | 0 | 0 (fixes in place) | 660 files, 178,072 lines |
| Step 2 | 0 | 0 (tags only) | 660 files, ~178,200 lines |
| Step 3 | ~3 dead modules + ~200 inline constants | ~870 | 657 files, ~177,200 lines |
| Step 4 | ~1-2 (deprecated engine) | ~600 | 655 files, ~176,600 lines |
| Step 5 | ~220 | ~19,818 | **435 files, ~156,800 lines** |
| Step 6 | ~50 (replaced by graph) | ~8,000 | **~385 files, ~148,800 lines** |

The codebase shrinks by ~17% through deletion alone (Steps 3+5), before the graph replaces any logic.

---

## Pipeline and Graph Schema

**Unchanged from v9.** The 6-layer pipeline, 4-tier graph schema, data contracts, multi-school model, query API, edge semantics, multi-lagna model, divisional chart handling, aggregation modes, enforcement rules, and worked example all remain as specified in v9.

See: `docs/superpowers/specs/2026-04-06-canonical-architecture-v9.md` for the complete graph specification.

---

## Audit-to-Architecture Traceability

Every step in the migration exists because the audit found a specific class of problem. Every architectural decision exists to prevent that class from recurring at scale.

### Step-to-Bug Mapping

| Step | Audit Bugs Addressed | Bug IDs | Why This Step, Not Another |
|------|---------------------|---------|---------------------------|
| Step 1 (Fix formulas) | Wrong formulas producing wrong answers NOW | BUG-001 to 042 (42 bugs) | These are objectively wrong per BPHS PDF. No architecture needed — just correct the value. |
| Step 2 (Tag verification) | False confidence in "correct" modules | — (discipline, not bugs) | S318 audited at 3 levels (bphs_pdf / formula_compared / pattern_scanned). Without tags, Step 3 could consolidate an unverified module. |
| Step 3 (Consolidate) | Duplication → drift → contradiction | BUG-051 (gentle signs), BUG-052-054 (Sthir Karak), BUG-055 (H1 yogakaraka), BUG-064 (Dig Bala), BUG-085 (weight discrepancies), BUG-087 (avastha chaos) | 17 sign lord copies can't be fixed one-by-one without drifting again. Single source + imports = structural prevention. |
| Step 4 (Wire connections) | Missing wiring → correct computation ignored | BUG-081 (dignity ignored), BUG-082 (parallel engines), BUG-083 (wrong varga module) | Architecture exists but isn't connected. 5-line fix has more impact than any 50-session rewrite. |
| Step 5 (Delete dead code) | Dead code → false surface area → maintenance drag | BUG-075-080 (22,692 dead lines) | Dead code confuses auditors, inflates test counts, and gets resurrected with its bugs intact. Delete it. |
| Step 6 (Graph) | Duplication at the conceptual level (21 aspect functions, 13 dignity functions) | BUG-086 (functional classification disagrees), all duplication clusters | Steps 1-5 fix the VALUES. The graph fixes the STRUCTURE — one computation per concept, queried everywhere. |
| Phase 2 (Rule IR) | Procedural engine bugs + encoding errors | BUG-035-038 (rule_firing bugs), BUG-048 (timing no-op), BUG-088 (mirror bypass), BUG-089-096 (corpus errors) | Declarative patterns can't have list-dropping bugs. Typed primitives can't have OR-vs-AND confusion. Validation gates can't be bypassed. |
| Corpus Repair | Data quality | BUG-089-096, all S1-S5 systematic patterns | Architecture can't fix wrong verse encodings. This is a separate data workstream. |

### How Each Architectural Layer Prevents Recurrence at Scale

The question isn't just "does this fix the 104 bugs?" It's "when we have 50,000 rules from 20 texts across 5 schools, do these bugs come back?"

**Problem 1: Duplication → Drift**

*How it happened (318 sessions):* Each new module needed sign lords, so each developer (session) copied the dict locally. 17 copies. One got Mars wrong. Nobody noticed because the others still worked.

*How the graph prevents it:* Sign lords are a Tier 1 edge (`LORDS`). There is exactly ONE code path that creates LORDS edges — the graph builder. Every consumer queries `graph.follow(sign, LORDS)`. There is no local dict to copy. Adding a new module means adding a new query, not a new dict.

*At 50,000 rules:* Each rule queries the graph. Zero rules contain their own sign lord table. A correction to the LORDS builder is a single-point fix that propagates to all 50,000.

**Problem 2: Parallel Implementations → Contradictions**

*How it happened:* `scoring.py` computes aspects one way. `multi_axis_scoring.py` computes them another way. `diagnostic_scorer.py` a third way. 21 aspect functions total. Mars gets `{3,7}` in some, `{3,9}` in others.

*How the graph prevents it:* Aspects are a Tier 2 edge (`ASPECTS_PLANET`, `ASPECTS_HOUSE`). The graph builder computes them ONCE using `sputa_drishti.py` (BPHS-verified). Every consumer — scoring, yoga detection, rule evaluation — queries the same edges. There is no second aspect computation.

*When adding Jaimini school:* Jaimini rasi drishti becomes a SEPARATE edge set tagged `school=jaimini`. It doesn't overwrite Parashari aspects. Both coexist in the graph. Rules declare their school and query only their school's edges. No contradiction possible — different schools, different edges.

*When adding KP school:* KP uses Placidus houses. The graph builder creates KP-specific `IN_HOUSE` edges tagged `school=kp`. Parashari whole-sign houses remain. KP rules query KP edges. Parashari rules query Parashari edges. House system differences are edges, not global state.

**Problem 3: Correct Computation Exists But Isn't Used**

*How it happened:* `dignity.py` computes exaltation/debilitation correctly. `scoring.py` calls `compute_all_dignities()`. Then ignores the result. For 318 sessions, every chart score treated exalted Jupiter the same as debilitated Jupiter.

*How the graph prevents it:* Dignity is a Tier 3 attribute on every planet node. It's ALWAYS there — not an optional import. When a rule queries `node(P).dignity`, it gets the value. There is no "forgetting to wire it." The graph doesn't have an opt-in model for correctness.

*At scale:* When Shadbala, Bhava Bala, and Avastha become Tier 4 lazy attributes, the same pattern applies. They're ON the graph. Any rule can query them. No wiring step needed. The question "does this computation affect the score?" becomes "does any rule query this attribute?" — which is a corpus decision, not an architecture decision.

**Problem 4: Wrong Module Used by Wrong Consumer**

*How it happened:* `scoring_v3.py` imports `divisional_charts.py` (9 wrong vargas). `app.py` imports `varga.py` (correct). Users see correct charts but get scores from wrong ones. Nobody noticed because the imports were in different files.

*How the graph prevents it:* Varga charts are computed ONCE by the graph builder as `VargaGraphSet`. There is no `divisional_charts.py` vs `varga.py` choice — there's one builder that produces one set of varga graphs. Every consumer (scoring, yoga fructification, Vimshopaka) queries the same `VargaGraphSet`.

*When adding new vargas (D40, D45):* Add the formula to the varga builder. All consumers automatically have access. No import to add. No second implementation to maintain.

**Problem 5: Procedural Engine Bugs**

*How it happened:* `rule_firing.py` has 33 `elif ctype ==` branches. Branch for `planet_not_in_house` silently truncates list arguments. Branch for `moolatrikona` ignores degree ranges. Branch for `_is_activated` is a no-op. Each branch is hand-coded, hand-maintained, and independently breakable.

*How the Rule IR prevents it:* There are no branches. There is one generic pattern matcher that resolves typed primitives against graph queries. `not_in_house(P, [6, 8, 12])` is a typed `list[int]`. The matcher iterates the full list. There is no `isinstance` check that could truncate it. The type system makes the bug structurally impossible.

*At 50,000 rules:* Every rule uses the same 25 primitives. Adding a new rule doesn't add a new code branch — it adds a new data pattern. The matcher is unchanged. The only code that grows is the corpus data, not the engine.

*When adding new condition types:* New primitives are compositions of existing ones. `planet_combust(P)` desugars to `conjunct(P, Sun) AND orb(P, Sun, max=14)`. No new `elif` branch. No new code path to break.

**Problem 6: Corpus Encoding Errors**

*How it happened:* Encoder writes `planet_in_house` when BPHS says "conjunct OR aspected by." Encoder puts OR alternatives into an AND list. Encoder writes absolute houses `[1,5,9]` when BPHS says "trine FROM the 2nd lord." The procedural engine can't distinguish correct from incorrect conditions — it just evaluates what's given.

*How the IR validation gates prevent it:* Gate IR-1 rejects unknown primitives (can't invent a condition type). Gate IR-5 requires relative references to have explicit `ref` (can't use absolute houses for relative positions). Gate IR-6 requires lists for negation conditions (can't silently truncate). Gate IR-9 warns when verse complexity doesn't match condition count.

*At 50,000 rules across 20 texts:* Every new rule passes through the same 9 gates. A Saravali encoder and a BPHS encoder face the same constraints. The gates prevent the 5 systematic patterns (S1-S5) structurally, regardless of which text is being encoded.

### What CANNOT Recur After Full Migration

| Current Problem | Structural Prevention | Recurrence Possible? |
|----------------|----------------------|---------------------|
| 17 sign lord copies | One graph LORDS builder | **NO** — no local dicts to copy |
| 21 aspect functions | One graph ASPECTS builder | **NO** — no per-module aspect code |
| Dignity ignored by scoring | Dignity is a graph node attribute | **NO** — always queryable, no wiring needed |
| Wrong module imported | One graph, one VargaGraphSet | **NO** — no module choice to get wrong |
| List-dropping in conditions | Typed IR primitives | **NO** — type system enforces full list |
| OR-vs-AND confusion | Explicit `or_group` primitive | **NO** — AND is default, OR is explicit |
| Relative→absolute house error | `in_house_from(ref=...)` with IR-5 gate | **NO** — gate rejects absolute fallback |
| Timing no-op | IR `require` section with temporal conditions | **NO** — timing is a typed primitive, not a stub |
| Mirror bypasses validation | IR-7 gate: all rules through all gates | **NO** — no bypass path exists |
| New school contradicts existing | School-tagged edges, auto-filtered queries | **NO** — schools are parallel edge sets, not overrides |

### What CAN Still Go Wrong

Honest about the limits:

| Risk | Why Architecture Doesn't Prevent It | Mitigation |
|------|-------------------------------------|------------|
| Wrong BPHS formula in the graph builder | Architecture ensures one source — but if that source is wrong, the error propagates everywhere | Verification tags (Step 2). Each builder function cites its BPHS verse. |
| Corpus rule encodes wrong prediction | IR validates structure, not semantic correctness | Maker-checker protocol per CLAUDE.md. Verse audit gate. |
| New school has fundamentally different concepts | Graph schema assumes planets/signs/houses. A school with different ontology (e.g., Chinese astrology) won't fit. | Out of scope. Graph is for Jyotish schools (Parashari/Jaimini/KP/Tajika). |
| Performance at 50,000 rules | Graph construction is O(planets × signs). Rule evaluation is O(rules × conditions). | Benchmark gate at Step 6 (<10ms graph construction). Rule indexing by house/planet for O(1) lookup. |
| Lazy Tier 4 computation explosion | If every rule queries Shadbala, it's computed 7×12 times (7 planets × 12 lagnas). | Memoization with key `(node, lagna, school)` as specified in v9. |

---

## Why 318 Sessions Produced This Mess

The 104 bugs are symptoms. The root cause is that nothing in the development process PREVENTS the patterns that create them. Every root cause maps to a missing enforcement mechanism.

### Root Cause 1: No Import Boundary Enforcement

**What happened:** Any module can import from any other module, or define any constant inline. There are no layer boundaries. `scoring.py` defines its own yogakaraka table. `multi_axis_scoring.py` defines its own sign lords. `feature_decomp.py` defines its own malefic set. Each is valid Python. Nothing stops it.

**Why the graph alone doesn't fix it:** After the graph is built, nothing stops session 500 from writing `from src.calculations.dignity import EXALT_SIGN` instead of `graph.node(planet).dignity`. The graph is one more import option, not a boundary.

**Structural enforcement needed:**

```python
# src/graph/__init__.py
# This module is the ONLY public API for chart data.
# All other src/calculations/ modules are internal implementation.

# Enforcement: pre-commit hook + ruff rule
# RULE: No file outside src/graph/ may import from src/calculations/ directly.
# RULE: No file outside src/graph/ may define sign lord, malefic, kendra, 
#       exaltation, or aspect constants.
# EXCEPTION: src/graph/builders/ imports from src/calculations/ (builder internals).
# EXCEPTION: tests/ may import from anywhere (testing internals is valid).
```

**Implementation:** A custom ruff rule or pre-commit hook that:
1. Scans every `.py` file outside `src/graph/builders/` and `tests/`
2. Rejects any `from src.calculations.` import
3. All external consumers use `from src.graph import compute_chart_graph` or `from src.graph.query import ...`

This makes the graph the ONLY way to access chart data. Not by convention — by enforcement. A developer who tries to import `dignity.py` directly gets a commit rejection with a message explaining why.

**When this activates:** After Step 6 (graph built). Before that, existing imports remain valid. The boundary is enforced only once the graph provides all the same data.

### Root Cause 2: No Concept Registry

**What happened:** A developer in session 200 needs sign lords. They don't know `house_lord.py` exists. They grep for "sign lord" but get 17 hits — which one is canonical? Easier to just define it locally. The 17 copies exist because there was no way to discover "this concept is already implemented, use this module."

**Why consolidation (Step 3) alone doesn't fix it:** Step 3 reduces 17 to 1. But it doesn't help the session-500 developer FIND the 1. They'll grep, get 1 hit, not know if it's canonical, and define their own anyway.

**Structural enforcement needed:**

```python
# src/graph/CONCEPT_REGISTRY.md (machine-readable, checked by CI)
#
# Every astrological concept has exactly one implementation.
# New concepts must be registered here before implementation.
# CI rejects new constants/functions that overlap with registered concepts.

concept: sign_lords
  canonical: src/calculations/house_lord.py::sign_lord()
  graph_edge: LORDS
  verification: bphs_pdf (Ch.3 v.18-19)
  constants_pattern: "_SIGN_LORD|SIGN_LORDS|sign_lord_map"  # grep pattern for duplicates

concept: natural_malefic
  canonical: src/calculations/rule_firing.py::is_natural_malefic()
  graph_attribute: PlanetNode.is_natural_malefic
  verification: bphs_pdf (Ch.3 v.8-10)
  constants_pattern: "_NAT_MALEFIC|_MALEFICS|NATURAL_MALEFICS"

concept: kendra_houses
  canonical: src/calculations/house_lord.py::is_kendra()
  graph_query: graph.edges_from(planet, IN_KENDRA_FROM)
  verification: bphs_pdf
  constants_pattern: "_KENDRA|KENDRA_HOUSES"

# ... one entry per concept
```

**Implementation:** A pre-commit hook that:
1. Reads `CONCEPT_REGISTRY.md`
2. For each concept, greps staged files for `constants_pattern`
3. If a match is found outside the `canonical` file → reject with message: "This concept is already implemented in {canonical}. Import from there."

This doesn't just prevent duplication — it makes the canonical source DISCOVERABLE. A developer who greps for `_SIGN_LORD` and hits the registry learns where the real one lives.

**When this activates:** After Step 3 (consolidation). The registry is built as part of Step 3, not after.

### Root Cause 3: No Build-Time Duplication Detection

**What happened:** Nobody noticed 17 sign lord copies because no tool checked. Each copy was in a different file, defined with a slightly different variable name (`_SIGN_LORD`, `_SIGN_LORDS`, `_SIGN_LORDS_BB`, `_SL`, `LORDS`). Human review can't catch this across 660 files.

**Why the concept registry alone doesn't fix it:** The registry catches exact pattern matches. But what about semantic duplicates? `{0: "Mars", 1: "Venus", ...}` and `["Mars", "Venus", ...]` are the same data in different structures. Pattern matching won't catch a list-based sign lord table.

**Structural enforcement needed:**

```python
# tools/duplication_detector.py
# Runs as pre-push hook step.
# Detects SEMANTIC duplication, not just string patterns.

CANONICAL_CONSTANTS = {
    "sign_lords": {
        "type": "dict[int, str]",
        "size": 12,
        "values_contain": ["Mars", "Venus", "Mercury", "Moon", "Sun", "Jupiter", "Saturn"],
        "canonical_file": "src/calculations/house_lord.py",
    },
    "exaltation_signs": {
        "type": "dict[str, int]",
        "size": 7,
        "values_contain": ["Sun", "Moon", "Mars"],
        "canonical_file": "src/calculations/dignity.py",
    },
    # ... one entry per concept with structural signature
}

def detect_duplicates(staged_files):
    """AST-parse each staged file. Find all module-level dict/list/set assignments.
    Compare against CANONICAL_CONSTANTS by structural signature (size + value overlap).
    Flag any that match >80% of a canonical constant's signature."""
```

This catches the case where a developer defines `PLANET_LORDS = ["Mars", "Venus", "Mercury", ...]` — it's not called `_SIGN_LORD` but the structural signature (list of 12 planet names mapped to positions) matches the sign lord concept.

**When this activates:** After Step 3. The detector is built as part of Step 3.

### Root Cause 4: No Architectural Compliance Tests

**What happened:** The graph will be built. Adapters will delegate to it. Tests will pass. Then session 500 adds a new feature and bypasses the graph because "it's faster to just compute aspects directly." No test catches this because no test checks HOW the computation happens — tests only check WHAT the output is.

**Why parity tests alone don't fix it:** Parity tests verify that old engine and graph produce the same outputs. They don't verify that all code USES the graph. A new module that computes aspects independently will produce correct outputs (if the formula is right) and pass all parity tests — but it's a new duplication that will drift.

**Structural enforcement needed:**

```python
# tests/test_architectural_compliance.py
# These tests verify HOW the system works, not WHAT it produces.
# They fail if anyone bypasses the graph.

import ast
import pathlib

GRAPH_CONSUMERS = pathlib.Path("src").rglob("*.py")
GRAPH_INTERNALS = {"src/graph/", "src/calculations/", "tests/"}

def test_no_direct_aspect_computation():
    """No file outside graph internals may compute aspects."""
    ASPECT_PATTERNS = [
        "SPECIAL_ASPECTS",
        "aspects_house",
        "_planet_aspects",
        "aspect_strength",
        "{3, 7}",  # Mars aspect offsets
        "{4, 8}",  # Jupiter aspect offsets
        "{2, 9}",  # Saturn aspect offsets
    ]
    for f in GRAPH_CONSUMERS:
        if any(f.is_relative_to(p) for p in GRAPH_INTERNALS):
            continue
        content = f.read_text()
        for pattern in ASPECT_PATTERNS:
            assert pattern not in content, (
                f"{f} computes aspects directly. "
                f"Use graph.edges_from(planet, ASPECTS_HOUSE) instead."
            )

def test_no_inline_sign_lords():
    """No file outside house_lord.py may define a sign lord mapping."""
    # ... similar pattern check

def test_no_inline_malefic_sets():
    """No file outside rule_firing.py may define a malefic set."""
    # ... similar pattern check

def test_scoring_uses_dignity():
    """score_chart() must query dignity from the graph, not ignore it."""
    content = pathlib.Path("src/scoring.py").read_text()
    assert "dignity" in content.lower(), "scoring.py does not reference dignity"
    # More specific: check that dignity affects the return value
    tree = ast.parse(content)
    # ... AST check that dignity variable is used in score computation

def test_single_scoring_engine():
    """Only one scoring entry point exists."""
    scoring_functions = []
    for f in pathlib.Path("src").rglob("*.py"):
        content = f.read_text()
        if "def score_chart" in content or "def score_all_axes" in content:
            scoring_functions.append(f)
    assert len(scoring_functions) == 1, (
        f"Multiple scoring engines: {scoring_functions}. "
        f"There must be exactly one."
    )

def test_varga_single_source():
    """Only one varga computation module is imported by non-test code."""
    varga_importers = set()
    for f in pathlib.Path("src").rglob("*.py"):
        if "test" in str(f):
            continue
        content = f.read_text()
        if "divisional_charts" in content:
            varga_importers.add(("divisional_charts", f))
        if "from src.calculations.varga" in content:
            varga_importers.add(("varga", f))
    sources = {name for name, _ in varga_importers}
    assert len(sources) <= 1, (
        f"Multiple varga modules in use: {varga_importers}. "
        f"Use only varga.py."
    )
```

These aren't unit tests. They're ARCHITECTURE tests. They verify structural invariants, not behavioral outputs. They run in CI alongside `pytest` and `ruff`. They make it physically impossible to bypass the graph without breaking the build.

**When this activates:** Incrementally. `test_no_inline_sign_lords` activates after Step 3. `test_scoring_uses_dignity` activates after Step 4. `test_single_scoring_engine` activates after Step 4. The full graph compliance tests activate after Step 6.

### Root Cause 5: No Session-Level Review for Parallel Implementations

**What happened:** Session 200 builds `avasthas.py`. Session 138 had already built `planet_avasthas.py`. Session 29 had already built `avastha.py`. Nobody checked "does this concept already exist?" because there was no session-level gate that asks that question.

**Why code review alone doesn't fix it:** Code review checks "is this code correct?" It doesn't check "should this code exist?" A reviewer sees well-written `avasthas.py` with correct BPHS formulas and approves it — without knowing two other avastha modules already exist.

**Structural enforcement needed:**

```python
# .claude/hooks/pre-session-start.sh
# Before ANY implementation work, this hook runs.
# It forces the session to check for existing implementations.

# 1. If the session creates a new .py file in src/calculations/:
#    - grep CONCEPT_REGISTRY.md for overlapping concepts
#    - list all existing modules in the same functional area
#    - require acknowledgment: "I checked and this is not a duplicate"

# 2. If the session modifies an existing module:
#    - check if the concept registry entry is still accurate
#    - check if the verification tag is still valid

# 3. At session END:
#    - run duplication_detector.py on all changed files
#    - run architectural compliance tests on all changed files
#    - if either fails, session cannot commit
```

This is L016 ("search before you build") enforced by the system, not by discipline. The hook makes it harder to create a parallel implementation than to find and extend the existing one.

**Implementation in CLAUDE.md session protocol:**

```markdown
**At session START (addition to existing protocol):**
4. Before creating ANY new function, constant, or file:
   a. Check CONCEPT_REGISTRY.md — does this concept exist?
   b. If yes: import from canonical source, do not reimplement
   c. If no: add entry to CONCEPT_REGISTRY.md BEFORE writing code
   d. Pre-commit hook enforces: new files in src/calculations/ must have
      a corresponding CONCEPT_REGISTRY.md entry

**At session END (addition to existing protocol):**
6. Run `tools/duplication_detector.py` on all modified files
7. Run `pytest tests/test_architectural_compliance.py`
8. Both must pass before commit
```

### How These 5 Enforcement Mechanisms Layer

```
Session starts
  ↓
[Hook] Check CONCEPT_REGISTRY.md — concept already exists? → import, don't reimplement
  ↓
Developer writes code
  ↓
[Pre-commit] Import boundary check — no direct src/calculations/ imports from outside graph
[Pre-commit] Concept registry pattern check — no new constants matching registered concepts
[Pre-commit] Duplication detector — no semantic duplicates of canonical constants
  ↓
[CI] Architectural compliance tests — graph is used, not bypassed
[CI] Ruff + pytest — code quality + behavioral correctness
  ↓
[Pre-push] Full test suite including architectural compliance
  ↓
Commit ships
```

At every stage, a different enforcement mechanism catches a different class of problem:

| Stage | Catches | Root Cause Addressed |
|-------|---------|---------------------|
| Session start hook | "This concept already exists" | RC5: No session-level review |
| Pre-commit import check | "Don't import from internal modules" | RC1: No import boundaries |
| Pre-commit pattern check | "This constant is registered elsewhere" | RC2: No concept registry |
| Pre-commit duplication detector | "This looks like an existing concept" | RC3: No duplication detection |
| CI architectural compliance | "This bypasses the graph" | RC4: No compliance tests |

### What This Changes About Session Estimates

Every session estimate in this document assumed "implement and test." It should be "implement, verify against BPHS, test, check duplication, check compliance." Adding enforcement infrastructure to every step:

| Step | Previous Estimate | With Enforcement Infrastructure | Honest Estimate |
|------|------------------|-------------------------------|-----------------|
| Step 1: Fix formulas | 2-3 | +0 (no new infra needed) | 2-3 |
| Step 2: Tag verification | 1 | +0 | 1 |
| Step 3: Consolidate | 4-6 | +3-4 (build concept registry + duplication detector) | 7-10 |
| Step 4: Wire connections | 3-4 | +1-2 (build initial compliance tests) | 4-6 |
| Step 5: Delete dead code | 2-3 | +0 | 2-3 |
| Step 6: Graph | 45-72 | +8-12 (import boundary enforcement + full compliance suite) | 53-84 |
| Phase 2: Rule IR | 28-45 | +5-8 (IR validation infrastructure) | 33-53 |
| **Total** | **85-134** | **+17-26** | **102-160** |

And honestly, this is still probably low. Each "verify against BPHS" step for Shadbala Chesta Bala (8-state motion system from scratch) or Yuddha Bala (planetary war detection) is not a 1-session task — it's a "read the BPHS chapter, understand the formula, implement, test against known charts, verify edge cases" cycle that takes 2-3 sessions per component. The Tier 4 lazy computation alone (Shadbala reimplementation) could be 15-25 sessions if done right.

**Honest total: 120-200 sessions for architecture + enforcement.**

### Structural Prevention vs Discipline Prevention — Final Honest Assessment

| Claim in This Spec | Structural or Discipline? | After Enforcement Layer |
|--------------------|--------------------------|-----------------------|
| "One graph LORDS builder" | Discipline (graph is optional) | **Structural** (import boundary rejects alternatives) |
| "Typed IR primitives" | Structural for corpus rules | Still discipline for procedural code (yogas.py, kundali_milan.py) |
| "School-tagged edges" | Structural within graph | **Structural** (compliance test verifies single builder per school+concept) |
| "Consolidation reduces copies" | Discipline (copy #18 possible) | **Structural** (duplication detector + concept registry block it) |
| "Verification tags" | Documentation (not enforced) | **Structural** (pre-commit checks tag before allowing canonical import) |
| "Delete dead code" | One-time action | **Structural** (compliance test detects new unreachable code each session) |
| "Session checks for existing implementations" | Discipline (L016) | **Structural** (session start hook enforces concept registry check) |

After the enforcement layer, 6 of 7 claims become genuinely structural. The one remaining discipline-dependent area is procedural computation code (yoga detection, kundali milan, varshaphala) that lives outside both the graph and the IR. These modules can still have bugs. The mitigation is architectural compliance tests that verify they QUERY the graph rather than computing independently — but the internal logic of "is this yoga correctly detected?" remains a correctness problem that only BPHS verification can address.

That's the honest limit. The enforcement layer prevents DUPLICATION and BYPASS. It does not prevent WRONG FORMULAS in procedural code. Wrong formulas are caught by verification tags + BPHS-verified tests, which are strong but not absolute.

---

## Honest Assessment: What This Spec Does and Does Not Achieve

### (1) Simplification — PARTIAL

Steps 1-5 simplify (fewer files, fewer copies, fewer engines). Step 6 adds layers: ephemeris → conventions → graph builders → graph → IR pattern matcher → aggregation → output. That's 7 layers where there used to be 2 (ephemeris → scoring). More organized, but not simpler.

**Spec commitment to actual simplification:** Post-graph, the standalone computation modules (`dignity.py`, `shadbala.py`, `house_lord.py`, `varga.py`, `avasthas.py`, `sputa_drishti.py`, `panchadha_maitri.py`, `functional_dignity.py`) become INTERNALS of `src/graph/builders/`. They are not public API. No code outside `src/graph/` may import them. This means the public surface area of the computation layer shrinks to ONE module (`src/graph/`), even though the internal complexity is preserved. The individual files may eventually be inlined into builders and deleted — that decision is made per-module when the builder is stable.

**Metric:** Public API surface (modules importable by scoring/UI/API) must be smaller post-graph than pre-graph. If it's not, the graph added complexity instead of removing it.

### (2) Stronger Controls — YES, but only if enforcement is in CI, not local hooks

The 5 enforcement mechanisms are only useful if they can't be skipped. Local pre-commit/pre-push hooks can be bypassed with `--no-verify`. 

**Spec commitment:** All 5 enforcement mechanisms run in CI (GitHub Actions), not only in local hooks. Local hooks are a convenience duplicate — CI is the authority. A PR that fails concept registry check, duplication detection, or architectural compliance cannot merge regardless of local hook state.

### (3) Robust Testing — NO, spec has a gap

The spec adds architectural compliance tests (verify HOW things work) but doesn't address the test quality problems S318 found: 107 exact float assertions, 3 fake tests, 5 critical coverage gaps. The compliance tests verify structure, not formula correctness.

**Spec commitment — Test Verification Standard:**

Every graph builder function and every computation module must have tests that meet ALL of:

| Requirement | What It Means | Why |
|-------------|--------------|-----|
| BPHS citation | Test docstring cites chapter, verse, page | Traces the test to source authority |
| Known-chart expected values | Uses a chart with hand-calculated expected output, not just "output is non-zero" | Catches wrong formulas, not just crashes |
| `pytest.approx` for floats | No exact float equality assertions | Prevents fragile tests that break on precision changes |
| Boundary conditions | Tests sign boundaries (29.99°/0.01°), house cusps, nakshatra transitions | Catches off-by-one and modulo errors |
| Negative cases | Tests what should NOT happen (debilitated planet should NOT get exaltation score) | Catches false positives |

**Exit criterion for Step 6:** Every graph builder has tests meeting this standard. Not "all existing tests pass" — "all builders have BPHS-cited, boundary-tested, approx-using tests."

**Exit criterion for Phase 2:** Every IR primitive has tests showing correct match AND correct non-match.

### (4) Better Astrological Insights — NO, spec has a gap

The spec is pure infrastructure. After 120-200 sessions of architecture work, a user gets: the same 22 R-rules (with corrected values), dignity now affecting scores, querying a graph. That's more correct but not more insightful.

Better insights require:
- More evaluable rules (corpus: 58.5% can't fire → goal: <10% can't fire)
- Multi-text concordance (v9 Layer 5: "this prediction is supported by 4 of 6 texts")
- Temporal predictions (dasha + transit activation of specific rules)
- Empirical calibration (do the predictions match real outcomes?)

**Spec commitment — Insight Delivery Milestones:**

The architecture is not done until it delivers measurable insight improvements, not just structural improvements.

| Milestone | What It Delivers | When | Metric |
|-----------|-----------------|------|--------|
| Step 1 complete | Correct answers (bugs fixed) | After Step 1 | 0 CRITICAL bugs |
| Step 4 complete | Dignity affects scores | After Step 4 | rho improvement on OB-3 calibration set (dignity-aware scores should correlate better than dignity-blind) |
| Step 6 + first 500 V2 rules migrated | Graph-based scoring with 500+ evaluable rules | After Step 6 + corpus work | Rules fired per chart: 22 → 200+ |
| Phase 2 + timing implementation | Time-dependent predictions | After Phase 2 | Predictions that differ based on query_date (currently impossible due to BUG-048 timing no-op) |
| Phase 2 + concordance aggregation | Multi-text agreement/disagreement visible to user | After Phase 2 + Layer 5 | Output shows "BPHS says X, Saravali says Y, agreement: 4/6 texts" |

If the architecture doesn't move these metrics, it's infrastructure for infrastructure's sake.

### (5) Prevention of Spaghetti — PARTIAL, needs growth controls

The enforcement mechanisms prevent DUPLICATION. They don't prevent COMPLEXITY GROWTH. At 50,000 rules and 20 texts, the graph itself could become the new spaghetti — not through duplication but through sheer size.

**Spec commitment — Growth Controls:**

| Rule | Trigger | Action |
|------|---------|--------|
| Module size limit | Any `.py` file exceeds 500 lines | Must be split into focused sub-modules |
| Builder decomposition | Any graph builder function exceeds 100 lines | Must be decomposed into helper functions with single responsibilities |
| Concept registry limit | Any category in CONCEPT_REGISTRY.md exceeds 30 entries | Category must be split into sub-categories with their own registry file |
| Test file limit | Any test file exceeds 150 test functions | Must be split by concept |
| IR primitive limit | Primitive count exceeds 40 | Review for compositions that should replace standalone primitives |
| Edge type limit | Graph edge types exceed 20 | Review for redundant or subsumable edges |
| Import depth limit | Any import chain exceeds 5 hops (A→B→C→D→E→F) | Intermediate modules must be consolidated or the dependency inverted |

These are mechanical rules. They don't require judgment — they trigger automatically when a threshold is crossed. They prevent the graph era from producing the same organic growth that the pre-graph era did.

**Enforcement:** CI checks file line counts, import depth, and concept registry size on every PR. Violations block merge with a message explaining the rule and the required action.

---

## Key Principles (from S318 audit lessons)

1. **Verify before consolidating.** Don't centralize unverified assumptions. Tag each module with its verification level. Only consolidate `bphs_pdf` or `formula_compared` modules.

2. **Delete before abstracting.** Remove dead code before building abstractions over it. A smaller codebase is easier to migrate.

3. **Fix before migrating.** Don't port broken formulas into the graph. Fix them in place first, verify, then port the correct version.

4. **Wire before rebuilding.** The dignity-into-scoring fix is 5 lines and improves every chart score. Don't wait for the graph to make this connection.

5. **One source, then zero copies.** For each concept: identify the canonical module → redirect all consumers → delete the copies. The graph is the eventual "one source" for all relationships.

6. **Corpus is data, not architecture.** Corpus quality is a separate workstream. Bad rules don't justify architecture changes. Architecture changes don't fix bad rules.

7. **Enforce in CI, not in hooks.** Local hooks are convenience. CI is authority. Any control that matters must be in CI, not only in local hooks.

8. **Test the HOW, not just the WHAT.** Architectural compliance tests verify structure. BPHS-cited tests verify correctness. Both are required. Neither alone is sufficient.

9. **Measure insights, not infrastructure.** The architecture succeeds when users get better astrological answers, not when the graph builds successfully. Track rules-fired-per-chart, rho correlation, and multi-text agreement as primary metrics.

10. **Bound growth mechanically.** Module size limits, import depth limits, concept registry limits, and edge type limits prevent organic complexity growth. These are CI-enforced, not discipline-dependent.
