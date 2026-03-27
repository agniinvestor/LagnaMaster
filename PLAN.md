# LagnaMaster — PLAN.md
## Sessions 1–160 Complete · Sessions 161+ Roadmap

### Completed Architecture (Sessions 1–160)

#### Calculation Engine
- 34 calculation modules in src/calculations/
- Parashari + Jaimini + Tajika + KP school declarations
- 1000+ tests, CI green, all sessions complete

#### What Is Done vs What Needs Wiring

**DONE AND WIRED into main pipeline:**
- dignity.py, shadbala.py, ashtakavarga.py (all wired to scoring)
- scoring_patches.py (ASPECT_STRENGTH + display_score in scoring_v3.py)
- nakshatra.py, bhava_and_transit.py, planetary_state.py
- varshaphala.py (25 tests, standalone module)
- All special lagnas, dasha systems, varga charts

**BUILT but NOT YET WIRED into main scoring pipeline:**
- functional_dignity.py — compute_functional_classifications() not in R02/R09
- dasha_scoring.py — apply_dasha_scoring() not called from score_chart()
- planet_avasthas.py — combined_modifier not applied to scoring
- shadbala_patches.py — war loser override not checked in compute_dignity()

**TOPOCENTRIC MOON — 2-line fix, NOT applied:**
```python
# In ephemeris.py, before Moon swe.calc_ut() call:
swe.set_topo(birth_lat, birth_lon, 0)
flags |= swe.FLG_TOPOCTR  # for Moon calculation only
```

### Sessions 161–188 (Complete)

| Session | Task | Effort | Impact |
|---------|------|--------|--------|
| 161 | Topocentric Moon — 2 lines in ephemeris.py | 30 min | HIGH — nakshatra accuracy | ✅ DONE | ✅ DONE |
| 162 | Wire functional dignity into R02/R09 | 2 hr | HIGH — systematic fix for all charts |
| 163 | Wire dasha_scoring into score_chart() | 3 hr | HIGH — temporal scoring |
| 164 | Wire war loser into compute_dignity() | 2 hr | MED — Graha Yuddha downstream |
| 165 | JHora reference fixtures (5 charts as JSON) | 4 hr | HIGH — external validation |
| 166 | Regression snapshot (J-2) | 3 hr | MED — prevents silent score changes |
| 167 | North Indian chart SVG | 6 hr | HIGH — commercial value |
| 168 | PDF export (weasyprint) | 4 hr | HIGH — client deliverables |
| 169 | KP cuspal sub-lord + promise/fructification | 8 hr | MED — KP completeness |
| 170 | Drekkana variant selection (Parasara/Jagannatha) | 2 hr | MED — D3 correctness |

### Classical Audit — Resolution Status

| Domain | Audit Issues | Done | Wired | Roadmap |
|--------|-------------|------|-------|---------|
| I. Scoring Engine | 5 | 4 | 1 (I-E) | 0 |
| II. Astronomical | 5 | 4 | 1 (F-1 topo) | 0 |
| III. Dignity | 14 | 13 | 1 (B-3 war) | 0 |
| IV. Aspects | 3 | 3 | 0 | 0 |
| V. House System | 3 | 2 | 1 (G-2) | 0 |
| VI. Vargas | 10 | 10 | 0 | 0 |
| VII. Shadbala | 8 | 8 | 0 | 0 |
| VIII. Yogas | 11 | 11 | 0 | 0 |
| IX. Dasha | 7 | 7 | 0 | 0 |
| X. AV | 4 | 4 | 0 | 0 |
| XI. Transit | 8 | 7 | 1 (XI-D) | 0 |
| XII. Panchanga | 4 | 4 | 0 | 0 |
| XIII. Jaimini | 6 | 6 | 0 | 0 |
| XIV. Special Lagnas | 2 | 2 | 0 | 0 |
| XVI. Varshaphala | 1 | 1 | 0 | 0 |
| XVIII. Validation | 3 | 1 | 1 | 1 |
| XIX. Output/API | 5 | 5 | 0 | 0 | ✅ S188 |
| OB. Architecture | 5 | 5 | 0 | 0 | ✅ S187/S188 |

### OB-3 (Empirical Calibration) — Long-Term Roadmap
Requires 500+ verified charts with documented life events.
ML pipeline: collect → verify → feature extract → gradient boost → feature importance.
Not feasible without chart corpus collection. Track as separate research project.

### Architecture Decisions (Permanent)

1. Scoring engine is a HEURISTIC — never present as classical verdict
2. School declaration (calc_config.py) gates which rules fire
3. CalcConfig.authority resolves inter-authority conflicts (PVRNR vs BV Raman)
4. All new rules must carry source: str docstring citing Text Author Ch.X v.Y
5. New yogas must have passing test with India 1947 OR a specific counter-example chart
6. Varshaphala is Tajika school — different aspects, separate pipeline
7. KP requires true node + KP ayanamsha + separate significator pipeline


## S187 — Scoring Wiring Gaps (March 2026) ✅
- War loser −1.5 penalty wired into `_score_one_house` (Saravali Ch.4 v.18-22)
- Dasha scoring wired into `score_chart_v3()` — D1 scores now dasha-sensitized
- `strict_school` param added to `score_axis()` / `score_all_axes()`
- `school_score_adjustment()` called in strict mode (live wire for R17/R18)

## S188 — XIX Output API + Postgres + Swiss Ephemeris (March 2026) ✅
- 5 new API endpoints: SVG, PDF, guidance, confidence, v3 scores
- Postgres routing live (`db_pg` — auto-falls back to SQLite if PG_DSN unset)
- Swiss Ephemeris real files installed — JPL DE431 precision
- API version: 3.0.0

## Sessions 189+ — Remaining Roadmap

## Living Documentation (docs/ folder — added S189)

All structured documentation now lives in `docs/`. See `docs/ROADMAP.md` for
the full session plan, `docs/ARCHITECTURE.md` for module reference, and
`docs/GUARDRAILS.md` for the 24 guardrails that govern all future sessions.

**Reading order for a new session:**
1. `git log --oneline -5` — verify actual state (GitHub UI shows stale data)
2. `docs/MEMORY.md` — current state + next session
3. `docs/ROADMAP.md` — find session entry
4. `docs/GUARDRAILS.md` — check applicable guardrails


| Priority | Item | Effort |
|----------|------|--------|
| 🟠 | C-18: 8 diverse stress-test fixtures (Neecha Bhanga, Graha Yuddha, nakshatra cusp, Parivartana, female, high-lat, year-boundary) | 1 day |
| 🟠 | Verify Shadbala Kala Bala all 8 sub-components complete | 2 hr |
| 🟠 | PostgreSQL live test (spin up PG_DSN, run 2 skipped tests) | 2 hr |
| 🟡 | Confidence model surfaced in Streamlit UI | 2 hr |
| 🟡 | Nehru Capricorn Lagna skip — investigate root cause | 1 hr |
| 🟡 | BC date charts: seplm_18.se1 + semom_18.se1 for pre-1800 | 30 min |
| 🔵 | OB-3: Empirical calibration ML pipeline (500+ charts required) | weeks |
| 🔵 | Mundane astrology consumer pipeline | 3–4 days |
