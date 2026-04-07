# S317 Full System Audit — 2026-04-07

**Scope:** Every directory, every module category, every document. Quantitative + content-verified where indicated.

## Summary of Critical Findings

### 🔴 ACTIVE BUGS (producing wrong results now)
1. **shadbala_patches.py had 4 wrong friendship values** — FIXED in this audit session
2. **11 modules have static malefic sets** that don't use chart-aware `is_natural_malefic()` — waning Moon and Mercury conjunction NOT considered in argala, arudha_perception, extended_yogas, functional_roles, longevity, multi_axis_scoring, multi_lagna, narayana_argala, yogas_extended, diagnostic_scorer, feature_decomp
3. **scoring_patches.py has stale ASPECT_STRENGTH** (0.75 fixed values) — not using BPHS speculum
4. **Only 23/7,412 rules (0.3%) marked "implemented"** — scoring engine can only evaluate 23 rules
5. **🔴🔴 MARS ASPECT BUG in multi_axis_scoring.py AND feature_decomp.py** — `Mars: {3, 9}` should be `Mars: {3, 7}`. Mars's 8th house aspect (diff=7) is coded as 10th house aspect (diff=9). This means Mars's 8th house aspect has been MISSING from the core scoring engine and a WRONG 10th house aspect applied instead. Affects R03, R07, R10, R14 for every chart. rule_firing.py, diagnostic_scorer.py, scoring_patches.py, sputa_drishti.py all have the CORRECT value {3, 7}. ONLY multi_axis_scoring and feature_decomp are wrong.
6. **107 `except Exception` clauses with ZERO logging** — errors silently swallowed across the calculation layer. Bugs produce wrong defaults instead of visible failures. NONE of the 107 clauses log the error.
7. **13 independent dignity computation functions** across different modules — each using own tables, own logic. Not guaranteed to produce same results for same input.
8. **21 independent aspect computation functions** across different modules — different implementations of the same concept.
9. **Tests importing from stale modules** — test_phase0.py and test_diverse_charts.py import from scoring_patches.py (stale ASPECT_STRENGTH). Tests for avasthas import from both avastha.py (old) and planet_avasthas.py (S138), not avasthas.py (S317 BPHS).

### 🟠 HIGH RISK (will cause issues under stress)
5. **multi_axis_scoring.py: 13 importers, 1 test file** — core scoring engine nearly untested
6. **functional_roles.py: 7 importers, 1 test** — functional classification widely used, barely tested
7. **diagnostic_scorer.py: 351 lines, 0 tests** — completely untested
8. **36/125 calculation modules have ZERO source citations** — including house_lord.py (38 importers), vimshottari_dasa.py (25 importers)
9. **74/143 corpus files lack verse_ref** — 52% of corpus lacks verse traceability
10. **111/125 modules untouched by S317** — 89% of calculation code not verified against text

### 🟡 STRUCTURAL DEBT
11. **11 hardcoded _NAT_MALEFIC sets** across separate files — should import from one source
12. **5 inline sign lord tables** — should import from one source
13. **8 avastha modules** — 3 confirmed unwired, rest untested for consistency
14. **4 friendship table copies** — dignity.py, panchadha_maitri.py, friendship.py, sayanadi_full.py (all now correct post-S317, but 4 copies = 4× future drift risk)
15. **0% concordance computed** across 7,412 rules — multi-text value proposition not operational
16. **Only 22/143 corpus files (15%) use V2 builder** — 85% old format
17. **13 rules still entity_target="general"** — L004 violation

## Duplication Index (EXHAUSTIVE — measured across entire repo)

| Concept | Inline Copies | Previous Estimate | Where They Are |
|---------|--------------|-------------------|---------------|
| Malefic set `{Sun,Mars,Saturn,Rahu,Ketu}` | **32** | 11 | 20 in src/calculations/, 2 in src/ui/, 1 in src/scoring.py, 1 in tools/, + corpus descriptions |
| Benefic set references | **102** | "a few" | Scattered across calculations, corpus descriptions, UI, guidance |
| Sign lord table | **7 inline dicts** | 5 | +rule_firing list form, +tools/diff_engine.py, +tests |
| Exalt sign dict | **4 inline** | "26 refs" | diagnostic_scorer, tools/diff_engine + dignity.py (authoritative), rule_firing (perf copy) |
| Dusthana `{6,8,12}` | **34** | "a few" | Nearly every scoring/yoga/dasha module defines its own |
| Kendra `{1,4,7,10}` | **45** | not measured | Worst duplication cluster — 45 separate definitions |
| Trikona `{1,5,9}` | **29** | not measured | Second worst — 29 separate definitions |
| Friendship table | **4 full copies** | 4 | dignity.py, panchadha_maitri.py, friendship.py, sayanadi_full.py |
| Avastha modules | **8 files** | 8 | avasthas.py, avastha_v2.py, avastha.py, planet_avasthas.py, sayanadi_full.py + 3 consumers |
| Scoring modules | **12 files** | 12 | scoring.py, scoring_v2.py, scoring_v3.py, scoring_patches.py, multi_axis_scoring.py, diagnostic_scorer.py + 6 others |
| ASPECT_STRENGTH | **2 copies** | 2 | scoring_patches.py (stale 0.75) + was in shadbala.py (removed S317) |

**Total inline concept duplications: ~275+ across the codebase.**
This is 3-5x worse than the original inventory estimated.

## Source Coverage

| Category | With Citations | Without | Citation Rate |
|----------|---------------|---------|---------------|
| Calculation modules | 89/125 | 36/125 | 71% |
| Corpus files (verse_ref) | 69/143 | 74/143 | 48% |
| Corpus files (V2 builder) | 22/143 | 121/143 | 15% |

## Test Coverage

| Module | Lines | Importers | Test Files | Risk |
|--------|-------|-----------|-----------|------|
| multi_axis_scoring.py | 588 | 13 | 1 | 🔴 CRITICAL |
| functional_roles.py | 206 | 7 | 1 | 🔴 HIGH |
| diagnostic_scorer.py | 351 | 1 | 0 | 🟠 UNTESTED |
| feature_expansion.py | 171 | 0 | 0 | 🟡 ORPHAN + UNTESTED |
| rule_firing.py | 1,442 | 13 | 9 | 🟡 Large, moderate coverage |

## Documentation Staleness (content-verified)

| Doc | Status | Key Issues |
|-----|--------|-----------|
| ARCHITECTURE.md | 🔴 STALE | Conflicts with graph spec. Wrong file paths. "12 modules" → 125. "22 rules" → 23. Missing PlanetPosition.latitude. Layer III references unreached sessions. |
| KPIS.md | 🟠 STALE NUMBERS, GOOD FRAMEWORK | Tests: 1338→14740. Rules: 23→7412. Framework is comprehensive and should be primary tracking instrument. |
| shadbala_audit_gaps.md | 🔴 FULLY STALE | Says 9 gaps open — all resolved in S317. |
| ROADMAP.md | 🟡 STRATEGIC CONTEXT | 1000-session plan. Graph architecture = Phase 2 (S411-S470). Must align. |
| GUARDRAILS.md | 🟠 ALL RED/ORANGE | 20 guardrails defined. Most not implemented. G02 (health/death) critical. |
| Makefile | 🔴 STALE | Says "76 tests" — actual 14,740. |
| BPHS_ENCODING_ROADMAP.md | 🟠 STALE | 6 chapter statuses not updated for S317. |

## API Layer

| Finding | Details |
|---------|---------|
| Two API versions | main.py (11 endpoints) + main_v2.py (5 endpoints). Both import from ephemeris + scoring. |
| Shared logic | Both call compute_chart → score_chart. main_v2.py is simpler subset. |
| DB routing | main.py uses db_pg (PostgreSQL). UI uses db (SQLite). Two DB paths. |

## Security

| Finding | Severity |
|---------|----------|
| JWT secret hardcoded fallback | 🔴 HIGH — "dev-secret-change-in-production" in auth.py:25 |
| Auth uses SQLite directly | 🟠 MEDIUM — Not using the db_pg routing layer |
| 0/21 dependencies pinned | 🟠 MEDIUM — All >= not == |
| No .env template | 🟡 LOW — Environment variables undocumented |

## Privacy & Guardrails

| Component | Status |
|-----------|--------|
| consent_engine.py | Exists (GDPR Art 7 + DPDP). Not audited for correctness. |
| data_minimisation.py | Exists (GDPR Art 5). Not audited. |
| family_consent.py | Exists. Not audited. |
| 20 G-series guardrails | Defined in GUARDRAILS.md. Most NOT implemented (🔴). |
| Health-sensitive handling | 772 references across codebase. Coverage unknown. |

## Infrastructure

| Component | Status |
|-----------|--------|
| Docker | Dockerfile + docker-compose.yml. api + ui services. |
| Makefile | 15 targets. Test count stale (76 vs 14740). |
| Pre-push hook | 7 checks (pytest, ruff, docs, scorecard, rework, maturity, completeness). |
| Pre-commit hook | Deferral language detection + scorecard on staged corpus. |
| Redis | Referenced in ARCHITECTURE.md as planned. Not implemented. |
| Celery | In requirements.txt. Worker exists (src/worker.py). |

## Unwired Infrastructure (ready to use, not connected)

| Module | Lines | What It Does | Should Connect To |
|--------|-------|-------------|-------------------|
| config_additions.py | 141 | 36 ayanamshas, AstronomicalConfig | ephemeris.py (replaces 3-ayanamsha hardcoded map) |
| yogas_additions.py | 307 | PM Yoga, Lunar/Solar yogas | Yoga detection pipeline |
| feature_expansion.py | 171 | V2 corpus → continuous features | Phase 2 scoring (premature) |

## Additional Findings (deep sweep)

### Dig Bala — 4 SEPARATE IMPLEMENTATIONS
1. `dig_bala.py` — standalone module with `_DIG_BALA_PEAK` dict + `compute_dig_bala(chart)` → returns dict
2. `shadbala.py` — `DIG_BALA_PEAK_HOUSE` dict + `compute_dig_bala(planet, chart)` → returns float
3. `multi_axis_scoring.py` — `_DIG_BALA` dict (inline, used for R20)
4. `feature_decomp.py` — `_DIG_BALA` dict (inline, used for feature extraction)
Same concept, 4 implementations, 4 dictionaries. Any change to dig bala peak houses requires updating 4 files.

### Vimshottari Dasha Years — 2 COPIES
1. `vimshottari_dasa.py` — `MAHADASHA_YEARS`
2. `pratyantar_dasha.py` — `VIMSHOTTARI_YEARS`
Same data, two files. Change to dasha years requires updating both.

### Corpus Rule Duplication — 364 verse-level duplicates
Same (source, chapter, verse_ref) appearing in multiple rules. LaghuParashari Ch.1 v.3 appears 21 times. These may be legitimate (one verse encoding multiple claims) or true duplicates (same claim encoded twice). Needs manual audit.

### Magic Number Prevalence
| Constant | Occurrences | Named? |
|----------|------------|--------|
| 0.75 | 53 | Sometimes (ASPECT_STRENGTH) |
| 60.0 | 42 | Sometimes (VIRUPAS) |
| 30.0 | 35 | Rarely |
| 15.0 | 27 | Rarely |
| 23.45 | 1 | Yes (obliquity) |

### Tests Asserting Stale Values
- **5 tests assert aspect strength = 0.75** (test_phase0.py:330-350) — this is the old house-based value, not the BPHS speculum continuous function
- **37 test locations** hardcode malefic lists — any change to conditional Moon/Mercury won't be tested
- Tests assert specific house scores that may no longer be correct after S317 scoring changes

### Untested Modules (comprehensive)
| Layer | Module | Lines | Risk |
|-------|--------|-------|------|
| calculations/ | diagnostic_scorer.py | 351 | 🔴 1 importer, 0 tests |
| calculations/ | feature_expansion.py | 171 | 🟠 0 importers, 0 tests |
| api/ | mobile_router.py | 90 | 🟠 API endpoint, 0 tests |
| api/ | models.py | 199 | 🟠 Pydantic models, 0 tests |
| ui/ | chart_visual.py | 282 | 🟡 SVG generation, 0 tests |
| ui/ | confidence_tab.py | 236 | 🟡 UI component, 0 tests |
| ui/ | kundali_page.py | 300 | 🟡 UI page, 0 tests |
| guidance/ | guidance_api.py | 170 | 🟠 User-facing, 0 tests |

### 32 Condition Types in Rule Engine
rule_firing.py has 32 `elif ctype ==` branches. Each is a condition type that corpus rules can use. These must ALL be translatable to graph queries in Phase 1. Most complex: `or_group`, `count_planets_with_state`, `dispositor_condition`, `derived_points_relationship`.

### 61 Yoga Detection Functions
Across 12 files. No inventory of which yogas are detected vs which are missing from the ~300 classical yogas.

## Deep Logic Sweep Findings

### Parallel Scoring Engines
`src/scoring.py` (619 lines) has its OWN R01-R23 weight table (87 R-rule references) completely separate from `src/calculations/multi_axis_scoring.py` (588 lines). Two independent scoring engines scoring the same chart. Which one produces the API output? Both exist, both are imported by different consumers.

### Yogakaraka — 3 Independent Sources
1. `functional_dignity.py:KNOWN_YOGAKARAKAS` — static table (S317 verified against BPHS)
2. `functional_roles.py:compute_functional_roles()` — dynamic computation from lordships (does NOT use KNOWN_YOGAKARAKAS)
3. `multi_lagna.py:_YOGAKARAKA` — separate static dict

These may produce DIFFERENT yogakarakas for the same lagna. No test verifies they agree.

### Configuration Class Collision
`calc_config.py:CalcConfig` AND `config_toggles.py:CalcConfig` — same class name, different modules. Importing `CalcConfig` gives different behavior depending on which module you import from.

### Error Swallowing
107 `except Exception` clauses across calculations/ with ZERO logging. Bugs produce silent wrong defaults.

### Test Fragility
- 241 exact float equality assertions (`assert x == 0.75`)
- Only 19 using `pytest.approx` (robust)
- 1 test file with zero assertions (`test_panchanga_legacy.py`)
- Tests import from stale modules (scoring_patches ASPECT_STRENGTH, old avastha modules)

### Nakshatra Index — 3 Formulas
1. `int(lon * 27 / 360)` — used in ashtottari_dasha, kalachakra_dasha
2. `int(lon / 13.333)` — documented as WRONG in nakshatra.py itself
3. `int(lon / (360/27))` — used in avasthas.py

Boundary behavior differs between formulas. Charts near nakshatra boundaries may get different nakshatras depending on which module computes it.

### House Computation — Mixed Conventions
360 occurrences of `% 12` in house calculations. Most use `(si - lagna) % 12 + 1` (1-indexed). Some use `(si - lagna) % 12` (0-indexed). Mixed conventions in same codebase = off-by-one risk at every house computation.

## Scoring Path Analysis

**TWO parallel scoring engines serve different consumers:**

| Engine | File | Consumers | Call Count |
|--------|------|-----------|-----------|
| `score_chart()` | src/scoring.py (619 lines) | API main.py, API main_v2.py, UI app.py, worker.py, montecarlo, pushkara | 11 |
| `score_all_axes()` | src/calculations/multi_axis_scoring.py (588 lines) | scoring_v3, domain_weighting, lpi, house_score, dominance_engine, varga_agreement, chart_exceptions, interfaces/scoring_engine | 10 |

Same chart, two engines, potentially different scores. The API serves `score_chart`. Internal analysis uses `score_all_axes`. These are NOT the same computation.

## Corpus Data Quality

| Metric | Value | Implication |
|--------|-------|------------|
| Empty outcome_direction | 2,634 (35.5%) | Can't contribute to directional scoring |
| Missing signal_group | 6,812 (91.9%) | Can't be grouped for pattern analysis |
| Health-sensitive rules | 110 | G02 guardrail NOT implemented — unprotected |
| entity_target = "general" | 13 | L004 violation (cop-out) |
| Verse-level duplicates | 364 | Potential double-counting |

## Deployment Inconsistency

| Setting | CLAUDE.md | Dockerfile | Reality |
|---------|-----------|-----------|---------|
| Python | 3.14 | 3.12-slim | Mismatch — Docker builds different Python |
| Makefile test count | — | "76 tests" | Actual: 14,740 |

## What This Audit Did NOT Cover

- Line-by-line CODE LOGIC correctness of 111 untouched calculation modules (swept for stale VALUES, not logic bugs)
- API endpoint BEHAVIOR testing (counted endpoints, not tested responses)
- UI VISUAL correctness
- Privacy module LEGAL compliance verification
- DB schema validation
- Docker build verification
- Celery worker functionality
- Performance profiling
- Security penetration testing
- Corpus rule CONTENT quality (checked metadata, not whether each rule correctly encodes its verse)
