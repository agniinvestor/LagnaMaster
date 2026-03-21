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

### Sessions 161–170 (Priority Queue)

| Session | Task | Effort | Impact |
|---------|------|--------|--------|
| 161 | Topocentric Moon — 2 lines in ephemeris.py | 30 min | HIGH — nakshatra accuracy |
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
| XIX. Output/API | 5 | 1 | 1 | 3 |
| OB. Architecture | 5 | 4 | 0 | 1 |

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
