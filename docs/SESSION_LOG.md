# LagnaMaster — Session Log

> Auto-generated: 2026-03-19
> Covers Sessions 1–15

This file records what was built in each session, key decisions, bugs found/fixed, and the state left for the next session. It serves as persistent memory across AI-assisted development sessions.

---

## Session 1 — `src/ephemeris.py`

**Date**: Early March 2026
**Tests added**: 14 (total: 14)
**Status**: ✅ Complete

### Deliverables
- `src/ephemeris.py` — pyswisseph wrapper
- `tests/test_ephemeris.py`
- `tests/fixtures.py` (INDIA_1947 dict)

### Key decisions
- Lahiri ayanamsha as default; Raman/Krishnamurti as options
- Moshier ephemeris (built-in) used if `ephe/` data files absent
- Ketu derived as `Rahu.longitude + 180° mod 360`
- `FLG_SIDEREAL | FLG_SPEED` passed to `swe.calc_ut`
- **P-1 fix**: `hour=None` treated as 0.0 (midnight birth)
- **P-4 fix**: unknown ayanamsha raises ValueError immediately

### 1947 fixture validation
- Lagna: 7.7286° Taurus ✅
- Sun: 27.989° Cancer ✅

---

## Session 2 — 7 Calculation Modules

**Date**: Early March 2026
**Tests added**: 36 (total: 50)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/dignity.py` — exaltation through debilitation, combustion, cazimi, Neecha Bhanga
- `src/calculations/nakshatra.py` — 27 nakshatras, 4 padas, D9 seed, Ganda Mool
- `src/calculations/friendship.py` — Naisargika + Tatkalik → Panchadha Maitri
- `src/calculations/house_lord.py` — whole-sign system, Kendra/Trikona/Dusthana helpers
- `src/calculations/chara_karak.py` — 7 Jaimini Chara Karakas (AK → GK)
- `src/calculations/narayana_dasa.py` — sign-based 81-year dasha; **N-1 fix** Taurus=7yr
- `src/calculations/shadbala.py` — 6 components in Virupas; **S-2 fix** Chesta Bala formula

### Key decisions
- Whole-sign house system throughout (not Placidus/Koch)
- Tatkalik friendship: signs 2/3/4/10/11/12 = Temp Friend; 1/5/6/7/8/9 = Temp Enemy
- 22 asymmetric pairs preserved in Naisargika matrix
- Rahu/Ketu excluded from Chara Karak ranking

---

## Session 3 — Scoring Engine + FastAPI + SQLite

**Date**: Early March 2026
**Tests added**: 20 (total: 70)
**Status**: ✅ Complete

### Deliverables
- `src/scoring.py` — 22 BPHS rules × 12 houses; scores clamped [-10, +10]
- `src/api/main.py` — 5 FastAPI endpoints (POST /charts, GET /charts, GET /charts/{id}, GET /charts/{id}/scores, GET /health)
- `src/api/models.py` — Pydantic v2 models
- `src/db.py` — SQLite, WAL mode, immutable inserts, `_SENTINEL` testability pattern

### Key decisions
- WC (Worth Considering) rules R03/R05/R07/R14 count at 0.5× weight
- Scores always recomputed from birth data (not cached) at `/charts/{id}/scores`
- `asynccontextmanager` lifespan (not deprecated `@app.on_event`)
- `_SENTINEL` allows tests to monkey-patch `DB_PATH` before import

---

## Session 4 — Streamlit UI

**Date**: Early March 2026
**Tests added**: 6 (total: 76)
**Status**: ✅ Complete

### Deliverables
- `src/ui/app.py` — 3-tab Streamlit UI: Chart / Domain Scores / Rule Detail
- `packages.txt` — apt packages for Streamlit Cloud (gcc, g++, python3-dev)

### Key decisions
- `fastapi` (not `fastapi[standard]`) to avoid Rust dependency from email-validator
- Session state: `chart`, `scores`, `chart_id`, `birth_date`, `show_history`
- Demo button pre-fills India 1947 chart

---

## Session 5 — Docker Compose + Integration Tests

**Date**: Early March 2026
**Tests added**: 17 (total: 93)
**Status**: ✅ Complete

### Deliverables
- `Dockerfile` — python:3.12-slim + gcc; runs api or ui
- `docker-compose.yml` — api (8000) + ui (8501) + shared SQLite named volume
- `Makefile` — up/down/logs/test targets
- `.streamlit/config.toml` — headless, indigo theme
- `tests/test_integration.py` — 17 end-to-end tests

### Key decisions
- Named volume `chart_data` for SQLite persistence
- `PYTHONPATH=/app` set in Dockerfile so `src.*` imports resolve
- All 3 ayanamshas tested in integration suite
- Rahu/Ketu 180° invariant checked

---

## Session 6 — Vimshottari Dasha + South Indian Chart SVG

**Date**: March 2026
**Tests added**: 20 (total: 113)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/vimshottari_dasa.py` — 120-year nakshatra dasha, 9 MDs × 9 ADs
- `src/ui/chart_visual.py` — South Indian SVG (520×520px, 4×4 grid)
- `src/ui/app.py` — expanded to 4 tabs (adds Vimshottari Dasha tab)
- `tests/test_vimshottari.py`

### Key decisions
- `_SEQUENCE`: Ketu→Venus→Sun→Moon→Mars→Rahu→Jupiter→Saturn→Mercury (9 planets)
- `_NAKSHATRA_LORDS = _SEQUENCE * 3` (27 entries)
- Antardasha = `maha_years × VIMSHOTTARI_YEARS[antar_lord] / 120`
- 1947 fixture: Moon in Pushya → Saturn birth dasha
- Benefics green (#1a7a1a), malefics red (#8b0000) in SVG

---

## Session 7 — Yogas

**Date**: March 2026
**Tests added**: 14 (total: 127)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/yogas.py` — 13 yoga types
- `src/ui/app.py` — adds Yogas tab
- `tests/test_yogas.py`

### Key decisions
- Rahu/Ketu excluded from planet counts (e.g. Pancha-Graha yoga: 7 main planets only)
- Kemadruma: Moon must have no planet in adjacent signs (excluding Rahu/Ketu)
- 1947 fixture: Pancha-Graha Yoga (5 planets in Cancer), Gajakesari, Budha-Aditya

---

## Session 8 — Ashtakavarga + E-1/A-2 Regression Guards

**Date**: March 2026
**Tests added**: 26 (total: 153)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/ashtakavarga.py` — 8-source bindu tables, 7 planets + Sarva
- `src/ui/app.py` — adds Ashtakavarga tab
- `tests/test_ashtakavarga.py` — includes E-1/A-2 regression guards

### Key decisions
- Fixed totals: Sun=50, Moon=48, Mars=42, Mercury=55, Jupiter=57, Venus=52, Saturn=40, Sarva=344
- Lagna is the 8th contributor (sign index = `chart.lagna_sign_index`)
- E-1 regression: asserts `|india_chart.jd_ut − 2432412.2708| < 0.001`
- A-2 regression: confirms Mercury `is_retrograde=True` on 2022-09-20

---

## Session 9 — Gochara (Transit Analysis)

**Date**: March 2026
**Tests added**: 29 (total: 182)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/gochara.py` — transit positions, Sade Sati, AV bindus
- `src/ui/app.py` — adds Transits tab
- `tests/test_gochara.py`

### Key decisions
- Transit positions at noon UTC: `swe.julday(y, m, d, 12.0, swe.GREG_CAL)`
- Sade Sati: Rising (sign-1), Peak (natal Moon sign), Setting (sign+1)
- Guru-Chandal transit: Jupiter and Rahu conjunct in transit sky
- AV bindus sourced from `compute_ashtakavarga(natal_chart)`

---

## Session 10 — Panchanga + Navamsha D9

**Date**: March 2026
**Tests added**: 40 (total: 222)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/panchanga.py` — 5-limb almanac + `compute_navamsha_chart()`
- `src/ui/chart_visual.py` — adds `navamsha_svg()`
- `src/ui/app.py` — Chart tab adds panchanga strip + D9 expander
- `tests/test_panchanga.py`

### Key decisions
- Karana sequence: 60 per month, 4 fixed + 7 movable cycling
- D9 formula: `_D9_START = {0:0, 1:9, 2:6, 3:3}` (Fire/Earth/Air/Water)
- 1947 known values: Tithi=28, Vara=Venus/Friday, Nakshatra=Pushya, Yoga=Siddhi
- NakshatraPosition: use `.dasha_lord` not `.lord`

---

## Session 11 — Pushkara Navamsha + Monte Carlo

**Date**: March 2026
**Tests added**: 30 (total: 252)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/pushkara.py` — Pushkara Navamsha detection (14 special navamsha points)
- `src/monte_carlo.py` — ±30-min birth time sampler, 100 samples, score stability report
- `tests/test_pushkara.py` + Monte Carlo tests

### Key decisions
- Pushkara Navamsha: 14 navamsha positions considered especially auspicious
- Monte Carlo returns score_mean, score_std, score_range per house
- Default: 100 samples, ±30 min range, tz_offset preserved
- 1947 fixture: Sun in Pushkara Navamsha (Cancer 3rd pada)

---

## Session 12 — Kundali Milan (Ashtakoot)

**Date**: March 2026
**Tests added**: 25 (total: 277)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/kundali_milan.py` — 8 Kuta compatibility scoring (max 36 points)
- `src/ui/app.py` — adds Kundali Milan tab (two-chart input)
- `tests/test_kundali_milan.py`

### Ashtakoot Kutas
1. Varna (1 pt) — caste/spiritual level
2. Vashya (2 pts) — dominance/control
3. Tara (3 pts) — birth star compatibility
4. Yoni (4 pts) — sexual compatibility (14 animal pairs)
5. Graha Maitri (5 pts) — planetary friendship (Moon sign lords)
6. Gana (6 pts) — temperament (Deva/Manushya/Rakshasa)
7. Bhakoot (7 pts) — moon sign compatibility (12 relationship patterns)
8. Nadi (8 pts) — health/constitution (Adi/Madhya/Antya)

### Key decisions
- Result: 36 = Perfect, ≥18 = Compatible, <18 = Caution
- Mangal Dosha check included as auxiliary flag
- Moon nakshatra lords used for Graha Maitri

---

## Session 13 — PDF Chart Report

**Date**: March 2026
**Tests added**: 15 (total: 292)
**Status**: ✅ Complete

### Deliverables
- `src/reports/pdf_report.py` — reportlab PDF export
- `src/ui/app.py` — download button in Chart tab
- `tests/test_pdf_report.py`

### PDF Content
- Cover: chart name, birth data, lagna, ayanamsha
- Page 1: South Indian D1 chart (SVG embedded as drawing)
- Page 2: 12-house domain scores table with ratings
- Page 3: Detected yogas list
- Page 4: Vimshottari Dasha current period + next 3 transitions

### Key decisions
- Uses `reportlab.graphics.renderPDF.draw()` for SVG-derived chart image
- Font: Helvetica (built-in, no TTF dependency)
- PDF bytes returned (no filesystem write) for Streamlit download_button

---

## Session 14 — Jaimini Chara Dasha

**Date**: March 2026
**Tests added**: 20 (total: 312)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/chara_dasha.py` — Jaimini sign-based dasha, 9 MDs × 9 ADs
- `src/ui/app.py` — Chara Dasha tab added
- `tests/test_chara_dasha.py`

### Key decisions
- Chara Dasha period = number of signs from Atmakaraka sign, forward or backward by lagna parity
- Direction: odd lagna → forward; even lagna → backward
- AntarDasha order: sub-dashas proceed through 12 signs from the MahaDasha sign
- Dasha periods range 1–12 years (one per sign)
- 1947 fixture: Taurus lagna (even) → backward starting from current sign

---

## Session 15 — Varga Divisional Charts

**Date**: 2026-03-19
**Tests added**: 25 (total: 337)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/varga.py` — D2/D3/D4/D7/D9/D10/D12/D60 divisional charts
- `tests/test_varga.py` — 25 tests
- Updated `PLAN.md` — reflects Sessions 11–15; defines Sessions 16–17
- Updated `DOCS.md` — adds Sessions 11–15 module reference
- `docs/SESSION_LOG.md` — this file

### Modules implemented
| Division | Name | Span | Formula |
|---|---|---|---|
| D2 | Hora | 15° | Odd: 0-15°→Leo, 15-30°→Cancer. Even: reversed |
| D3 | Drekkana | 10° | k=0→sign, k=1→sign+4, k=2→sign+8 |
| D4 | Chaturthamsha | 7°30' | k=0..3 → sign + k×3 |
| D7 | Saptamsha | 4°17' | Odd: sign+k. Even: sign+6+k |
| D9 | Navamsha | 3°20' | Fire→Aries, Earth→Capricorn, Air→Libra, Water→Cancer (cross-validates panchanga.py) |
| D10 | Dashamsha | 3° | Odd: sign+k. Even: sign+9+k |
| D12 | Dvadasamsha | 2°30' | (sign+k)%12, all signs same |
| D60 | Shashtyamsha | 0°30' | Odd: k%12. Even: (5+k)%12 |

### Key decisions
- D9 included for cross-validation with `panchanga.compute_navamsha_chart()` (must match)
- Rahu/Ketu follow the same positional formula as the 7 main planets
- `_is_odd_sign()`: Aries=0, Gemini=2, Leo=4, Libra=6, Sagittarius=8, Aquarius=10 are odd
- `VargaChart.d9()` shortcut; `VargaTable.planets_in_sign(si)` for sign occupancy queries
- All 9 planets present in every VargaTable (never raises KeyError)

### Tests passing
- Structure: 8 divisions, 9 planets each, correct labels ✅
- D2: odd/even sign, both halves, Sun in Cancer (1947 → Leo Hora) ✅
- D3: first/second/third decan trikona jumps ✅
- D4: quadrant assignments ✅
- D7: odd/even parity ✅
- D9: cross-validation vs panchanga (lagna + Moon) ✅
- D10: odd/even parity ✅
- D12: sequential rule, all signs ✅
- D60: odd=Aries, even=Virgo start, 13th division ✅
- Accessors: planet_sign, planet_sign_index, planets_in_sign ✅
- Determinism: same chart → same VargaChart ✅

### Next session (Session 16)
**Sapta Varga Dignity — Vimshopak Bala**
- Use D1/D2/D3/D7/D9/D10/D12 for 7-varga dignity scoring
- Vimshopak = weighted dignity score (max 20 points)
- Weight table: D1=3, D2=1.5, D3=1.5, D7=1.5, D9=5, D10=2.5, D12=2.5
- Integrates with existing `dignity.py` (dignity levels in each varga)
- ~20 tests expected

---

## Outstanding Work

### Session 16 (Next)
`src/calculations/sapta_varga.py` — Vimshopak Bala (20-pt varga dignity score)

### Session 17 (Planned)
`src/calculations/kp.py` — KP (Krishnamurti Paddhati) sub-lord system

### Sessions 18–25
Production hardening: PostgreSQL, Redis, JWT, K8s, Next.js

---

## Bug Tracker

| ID | Severity | Module | Description | Status |
|---|---|---|---|---|
| P-1 | Critical | ephemeris.py | Midnight birth: hour=0 treated as falsy | ✅ Fixed S1 |
| P-4 | Critical | ephemeris.py | Unknown ayanamsha silently uses default | ✅ Fixed S1 |
| N-1 | Critical | narayana_dasa.py | Taurus period = 4yr (should be 7yr) | ✅ Fixed S2 |
| S-2 | High | shadbala.py | Chesta Bala cell J14 = hardcoded 3851 | ✅ Fixed S2 |
| E-1 | Critical | ephemeris.py | JDN Gregorian +0.5 day correction | ✅ Not in Python code; regression test added S8 |
| A-2 | High | retrograde | Mercury direction: wrong row reference | ✅ Not in Python code; regression test added S8 |

---

## Test Count History

| After Session | Tests |
|---|---|
| 5 | 93 |
| 10 | 222 |
| 11 | 252 |
| 12 | 277 |
| 13 | 292 |
| 14 | 312 |
| 15 | 337 |

---

## Session 16 — Sapta Varga Vimshopak Bala

**Date**: 2026-03-19
**Tests added**: 20 (total: 357)
**Status**: ✅ Complete

### Deliverables
- `src/calculations/sapta_varga.py` — Vimshopak Bala (20-point weighted dignity)
- `tests/test_sapta_varga.py` — 20 tests

### Vimshopak Bala weights (sum = 20)
| Division | Weight |
|----------|--------|
| D1 Rasi | 3 |
| D2 Hora | 2 |
| D3 Drekkana | 2 |
| D7 Saptamsha | 1 |
| D9 Navamsha | 5 |
| D10 Dashamsha | 3 |
| D12 Dvadasamsha | 4 |

### Dignity fractions
Exaltation=1.0, Moolatrikona=0.75, OwnSign=0.5, Friend=0.375,
Neutral=0.25, Enemy=0.125, Debilitation=0.0

### Key decisions
- Rahu/Ketu always Neutral in every division (no classical exalt/debil in Parashari)
- Lagna treated as OwnSign in every varga (convention: ascendant is always in "own" dignity)
- Grade thresholds: Excellent≥15, Good≥10, Average≥6, Weak≥3, Very Weak<3
- `ranking()` returns 9 planets (not Lagna) sorted descending by Vimshopak score
- All dignity tables embedded directly (no import of dignity.py to avoid circular deps)

---

## Session 17 — KP Sub-lord System

**Date**: 2026-03-19
**Tests added**: 22 (total: 379)

> Note: test counts were recalibrated after Sessions 16-17; see README for canonical total.

**Status**: ✅ Complete

### Deliverables
- `src/calculations/kp.py` — KP Star Lord / Sub Lord / Sub-Sub Lord system
- `tests/test_kp.py` — 22 tests

### KP Sub-lord algorithm
Each nakshatra (13°20' = 800') is subdivided into 9 sub-lords proportional
to Vimshottari years (total 120). Within each sub, the same proportion gives
sub-sub lords. The sequence WITHIN a nakshatra starts from its own star lord
(not from Ketu), which correctly models BPHS KP sub-sequence.

### Pilot: whole-sign house cusps
KP traditionally uses Placidus/equal cusps. This pilot uses whole-sign
(0° of each house sign) as the cusp longitude. Full Placidus integration
is deferred to Phase 3 (when a robust swe.houses() wrapper is built).

### Significator ranking (per house)
1. Level 1: planets occupying the house
2. Level 2: planets whose KP star lord or sub lord is an occupant
3. Level 3: house lord (bhavesh)

### 1947 India known values
- Lagna at ~37.73° → Krittika nakshatra, Star Lord = Sun
- Moon at ~93.98° → Pushya nakshatra, Star Lord = Saturn

### Next: Session 18
Production hardening begins: PostgreSQL migration, Redis caching, JWT auth.
Or if staying in Python domain: Placidus house cusp integration for true KP.

---

## Test Count History (updated)

| After Session | Tests |
|---------------|-------|
| 5 | 93 |
| 10 | 222 |
| 14 | 312 |
| 15 | 337 |
| 16 | 357 |
| 17 | 379 |

---

## Session 19 — Streamlit 12-Tab UI Integration

**Date**: 2026-03-19 | **Tests added**: 20 | **Running total**: 421

### Deliverables
- `src/ui/app.py` — Complete rewrite: 12-tab Streamlit UI (942 lines)
- `tests/test_ui_s19.py` — 20 tests: import smoke tests + structural checks

### What changed in app.py

**Existing tabs (enhanced)**:
- Tab 1 📊 Chart: added Pushkara Navamsha indicators (✨) in planet table, Monte Carlo expander (S11), PDF download button (S13)
- Tab 5 ⏱ Dashas: added Chara Dasha section below Vimshottari (S14)

**New tabs (S12, S15-S18)**:

| Tab | Module | Key UI elements |
|-----|--------|----------------|
| 📐 Varga Charts | `varga.py` | Division selector, navamsha_svg() reused for any division, all-divisions summary table |
| ⚖️ Vimshopak | `sapta_varga.py` | Ranking bar chart, per-planet dignity breakdown, full table with abbreviated dignity names |
| 🔑 KP Analysis | `kp.py` | Lagna KP header, planet sub-lord table, house significators table |
| 🌟 Annual Chart | `varshaphala.py` | Year input, Solar return SVG, Muntha/Varsha Pati metrics, Tajika aspects table |
| 💑 Kundali Milan | `kundali_milan.py` | Person B form, 36-pt result, kuta breakdown, both charts SVG side-by-side |

### Design decisions
- **Graceful degradation**: every S11-S18 import wrapped in `try/except` with `_HAS_*` flag — if a module is unavailable, the tab shows an info message instead of crashing the whole app
- **navamsha_svg() reuse**: Varga tab reuses existing `navamsha_svg(d_data, lagna_si, label)` for all 8 divisional charts — no new SVG code needed
- **Session state for Annual Chart**: `_varsha_report` stored in `st.session_state` so result persists across tab switches without recomputing
- **Kundali Milan form**: uses `st.form()` to prevent partial submissions; Person B chart computed inline
- **Monte Carlo lazy**: runs only on button click, not on every chart compute

### Tab order rationale
Analytical tabs (Varga, Vimshopak, KP) grouped together after Transits. Annual Chart before Kundali Milan (single-chart vs two-chart). Rule Detail moved to end as a debugging/reference tool.

### Test strategy
- Import smoke tests: all 8 new module imports verified
- API surface tests: every attribute app.py accesses on return values checked
- Structural tests: 12 tab labels verified in source, all `_HAS_*` flags verified, all new module imports verified

---

## Test Count History

| After Session | Tests |
|---------------|-------|
| 5 | 93 |
| 10 | 222 |
| 14 | 312 |
| 15 | 337 |
| 16 | 357 |
| 17 | 379 |
| 18 | 401 |
| 19 | 421 |
