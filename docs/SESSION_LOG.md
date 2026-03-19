# LagnaMaster Session Log
> 2026-03-19 | Sessions 1-14 complete | 312/312 tests

## Summary
| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1-10 | Pilot: ephemeris→panchanga | 222 |
| 11 | Pushkara Navamsha (R21) + Monte Carlo sensitivity | 30 |
| 12 | Kundali Milan — Ashtakoot 36-pt + Mangal Dosha | 25 |
| 13 | PDF Chart Report — reportlab A4 | 15 |
| 14 | Jaimini Chara Dasha — sign-based predictive cycle | 20 |

## Session 14 Details
- src/calculations/chara_dasha.py: compute_chara_dasha(), current_chara_dasha(), atmakaraka_sign()
- K.N.Rao/Iranganti method: years = planets_in_sign + sign_lord_distance, clamped [1,12]
- Odd lagna → forward; Even lagna → backward
- Birth balance from AK degree fraction (AK = highest-degree planet)
- 1947 India: Taurus lagna (even) → Taurus, Aries, Pisces... | AK = Sun (27.989° Cancer)
- tests/test_chara_dasha.py: 20 tests

## Open manual patches (apply to existing files)
- src/scoring.py R21: docs/session11_scoring_r21_patch.py
- src/ui/app.py tab 8 (Sensitivity): docs/session11_ui_sensitivity.py
- src/ui/app.py tab 9 (Kundali Milan): docs/session12_app_patch.py
- src/ui/app.py tab 10 (Chara Dasha): docs/session14_app_patch.py

## Session 15 — Next
- src/calculations/ashtakavarga.py: Kakshya (sub-sign) bindu calculation
- Gochara scoring weighted by AV bindus at transit sign
- tests/test_av_kakshya.py: 15 tests

---

## Session 15 — Varga Divisional Charts

**Date**: 2026-03-19 | **Tests added**: 25 | **Status**: ✅ Complete

### Deliverables
- `src/calculations/varga.py` — D2/D3/D4/D7/D9/D10/D12/D60 formulas + dataclasses
- `tests/test_varga.py` — 25 tests

### Divisions implemented
| Division | Name | Span | Formula |
|----------|------|------|---------|
| D2 | Hora | 15° | Odd: 0-15°→Leo, 15-30°→Cancer. Even: reversed |
| D3 | Drekkana | 10° | `(sign + k×4) % 12`, k=0/1/2 |
| D4 | Chaturthamsha | 7°30' | `(sign + k×3) % 12`, k=0..3 |
| D7 | Saptamsha | 4°17' | Odd: `(sign+k)%12`. Even: `(sign+6+k)%12` |
| D9 | Navamsha | 3°20' | Cross-validates panchanga.py |
| D10 | Dashamsha | 3° | Odd: `(sign+k)%12`. Even: `(sign+9+k)%12` |
| D12 | Dvadasamsha | 2°30' | `(sign+k)%12`, all signs |
| D60 | Shashtyamsha | 0°30' | Odd: `k%12`. Even: `(5+k)%12` |

### Key decisions
- D9 included for cross-validation with `panchanga.compute_navamsha_chart()` (must agree)
- Rahu/Ketu use same positional formula as 7 main planets
- `_is_odd_sign()`: Aries(0),Gemini(2),Leo(4),Libra(6),Sagittarius(8),Aquarius(10) are odd
- `VargaChart.d9()` shortcut; `VargaTable.planets_in_sign(si)` for occupancy queries

---

## Session 16 — Sapta Varga Vimshopak Bala

**Date**: 2026-03-19 | **Tests added**: 20 | **Status**: ✅ Complete

### Deliverables
- `src/calculations/sapta_varga.py` — 20-point weighted dignity score
- `tests/test_sapta_varga.py` — 20 tests

### Vimshopak weights (sum = 20)
D1=3, D2=2, D3=2, D7=1, D9=5, D10=3, D12=4

### Dignity fractions
Exaltation=1.0, Moolatrikona=0.75, OwnSign=0.5, Friend=0.375, Neutral=0.25, Enemy=0.125, Debilitation=0.0

### Key decisions
- Rahu/Ketu always Neutral (no classical exalt/debil in Parashari)
- Grade thresholds: Excellent≥15, Good≥10, Average≥6, Weak≥3, Very Weak<3
- `ranking()` returns 9 planets sorted descending by score

---

## Session 17 — KP Sub-lord System

**Date**: 2026-03-19 | **Tests added**: 22 | **Status**: ✅ Complete

### Deliverables
- `src/calculations/kp.py` — KP Star/Sub/Sub-Sub lords + house significators
- `tests/test_kp.py` — 22 tests

### KP algorithm
Each nakshatra (13°20') subdivided proportional to Vimshottari years.
Sub sequence within a nakshatra starts from its own star lord (BPHS correct).
Pilot uses whole-sign house cusps; Placidus deferred to Phase 3.

### Significators (per house)
1. Planets occupying the house
2. Planets whose star/sub lord is an occupant
3. House lord (bhavesh)

### 1947 India known values
- Lagna at ~37.73° → Krittika, Star Lord = Sun
- Moon at ~93.98° → Pushya, Star Lord = Saturn

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

---

## Session 15 — Varga Divisional Charts

**Date**: 2026-03-19 | **Tests added**: 25 | **Running total**: 337

### Deliverables
- `src/calculations/varga.py` — D2/D3/D4/D7/D9/D10/D12/D60 divisional chart engine
- `tests/test_varga.py` — 25 tests

### Divisions
| Division | Name | Span | Formula summary |
|----------|------|------|-----------------|
| D2 | Hora | 15° | Odd sign: 0-15°→Leo, 15-30°→Cancer; Even: reversed |
| D3 | Drekkana | 10° | `(si + k×4) % 12`, k=0/1/2 per decan |
| D4 | Chaturthamsha | 7°30' | `(si + k×3) % 12`, k=0..3 |
| D7 | Saptamsha | 4°17' | Odd: `(si+k)%12`; Even: `(si+6+k)%12` |
| D9 | Navamsha | 3°20' | Cross-validates panchanga.compute_navamsha_chart() |
| D10 | Dashamsha | 3° | Odd: `(si+k)%12`; Even: `(si+9+k)%12` |
| D12 | Dvadasamsha | 2°30' | `(si+k)%12` for all signs |
| D60 | Shashtyamsha | 0°30' | Odd: `k%12`; Even: `(5+k)%12` |

### Key decisions
- D9 cross-validates panchanga.py (must agree or test fails)
- Rahu/Ketu use same positional formula as 7 main planets
- VargaChart.d9() shortcut; VargaTable.planets_in_sign(si) helper

---

## Session 16 — Sapta Varga Vimshopak Bala

**Date**: 2026-03-19 | **Tests added**: 20 | **Running total**: 357

### Deliverables
- `src/calculations/sapta_varga.py` — 20-point weighted dignity score
- `tests/test_sapta_varga.py` — 20 tests

### Weights (must sum to 20)
D1=3, D2=2, D3=2, D7=1, D9=5, D10=3, D12=4

### Dignity fractions
Exaltation=1.0 / Moolatrikona=0.75 / OwnSign=0.5 / Friend=0.375 /
Neutral=0.25 / Enemy=0.125 / Debilitation=0.0

### Key decisions
- Rahu/Ketu always Neutral (no classical exalt/debil in Parashari)
- Grade thresholds: Excellent≥15, Good≥10, Average≥6, Weak≥3, Very Weak<3
- ranking() returns 9 planets sorted descending, Lagna excluded

---

## Session 17 — KP Sub-lord System

**Date**: 2026-03-19 | **Tests added**: 22 | **Running total**: 379

### Deliverables
- `src/calculations/kp.py` — KP Star/Sub/Sub-Sub lords + house significators
- `tests/test_kp.py` — 22 tests

### Algorithm
Each nakshatra (13°20') subdivided into 9 sub-lords proportional to Vimshottari years.
Sub sequence within a nakshatra starts from the nakshatra's own star lord (BPHS correct).
Sub-sub: same proportional split applied recursively within each sub.

### House significators (3 levels)
1. Planets occupying the house (direct)
2. Planets whose star/sub lord is an occupant (indirect)
3. House lord (bhavesh)

### 1947 India known values
- Lagna ~37.73° → Krittika nakshatra, Star Lord = Sun
- Moon ~93.98° → Pushya nakshatra, Star Lord = Saturn

### Note
Pilot uses whole-sign house cusps (0° of each house sign).
Placidus cusp integration deferred to Phase 3.

---

## Session 18 — Varshaphala (Annual Solar Return)

**Date**: 2026-03-19 | **Tests added**: 22 | **Running total**: 401

### Deliverables
- `src/calculations/varshaphala.py` — Annual Solar Return engine
- `tests/test_varshaphala.py` — 22 tests

### Concepts implemented
| Concept | Description |
|---------|-------------|
| Solar Return | Binary-search for exact moment Sun returns to natal longitude |
| Varsha Lagna | Ascendant of the solar return chart |
| Muntha | Annual significator: `(natal_lagna_si + years_elapsed) % 12` |
| Varsha Pati | Year Lord = sign lord of Muntha sign |
| Tajika aspects | 5 aspects: Itthasala(60°), Ishrafa(120°), Nakta(90°), Kambool(180°), Dainya(30°) |

### Binary search precision
60 iterations → sub-arcsecond precision (~0.000001°).
Handles 359°→0° wrap correctly via signed angular difference.

### 1947 India: 1948 solar return
- solar_return_date: 1948-08-xx (Sun returns to ~117.99° Cancer)
- years_elapsed: 1
- Muntha: Taurus (si=1) + 1 = Gemini (si=2)

### 2026 solar return for 1947 chart
- years_elapsed: 79
- Muntha: (1 + 79) % 12 = 80 % 12 = 8 = **Sagittarius**
- Varsha Pati: Jupiter (lord of Sagittarius)

---

## Test Count History

| After Session | Tests |
|---------------|-------|
| 5 | 93 |
| 10 | 222 |
| 11 | 252 |
| 12 | 277 |
| 13 | 292 |
| 14 | 312 |
| 15 | 337 |
| 16 | 357 |
| 17 | 379 |
| 18 | 401 |
