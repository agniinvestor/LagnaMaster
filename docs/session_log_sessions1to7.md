# LagnaMaster — Session Log: Sessions 1–7

> Date range: 2026-03-19
> Total tests at end: 127/127 passing

---

## Overview

Sessions 1–7 completed the full pilot build of LagnaMaster — transforming a 178-sheet Excel Jyotish workbook into a working FastAPI + Streamlit web platform.

**Strategy**: Pilot-first — translate Excel formulas to Python 1:1 (bugs preserved), ship a working end-to-end app, then fix accuracy iteratively in Sessions 8+.

---

## Session 1 — Ephemeris Wrapper
**Deliverable**: `src/ephemeris.py`
**Tests**: 14/14

pyswisseph wrapper that converts birth date/time/location to sidereal planet positions and ascendant.

- `FLG_SIDEREAL | FLG_SPEED` flags for sidereal positions with speed
- Lahiri, Raman, Krishnamurti ayanamshas supported
- Ketu = Rahu + 180° (not computed by pyswisseph)
- Moshier ephemeris fallback (no .se1 data files required)
- **Bugs fixed**: P-1 (midnight `hour=None`), P-4 (unknown ayanamsha ValueError)

**1947 India fixture**: Lagna 7.7286° Taurus, Sun 27.989° Cancer, Moon 3.9835° Cancer.

---

## Session 2 — 7 Calculation Modules
**Deliverable**: `src/calculations/` (7 modules)
**Tests**: 36/36

| Module | Purpose |
|--------|---------|
| `dignity.py` | DignityLevel enum, combustion, cazimi, Neecha Bhanga |
| `nakshatra.py` | 27 nakshatras, 4 padas, D9 navamsha, Ganda Mool |
| `friendship.py` | Naisargika + Tatkalik → Panchadha Maitri (5-fold) |
| `house_lord.py` | Whole-sign HouseMap, is_kendra/trikona/dusthana helpers |
| `chara_karak.py` | 7 Jaimini Chara Karakas (AK = highest degree in sign) |
| `narayana_dasa.py` | 81-year sign-based dasha (odd=forward, even=backward) |
| `shadbala.py` | 6-component planetary strength in Virupas |

**Bug fixed (N-1)**: Taurus Narayana Dasha was 4 years in Excel; corrected to 7 years.
**Bug fixed (S-2)**: Shadbala Chesta Bala cell J14 was hardcoded 3851; corrected to `min(60, mean_motion/|speed|×60)`.

---

## Session 3 — Scoring Engine + FastAPI + SQLite
**Deliverable**: `src/scoring.py`, `src/api/`, `src/db.py`
**Tests**: 20/20

- 22 BPHS scoring rules × 12 houses = 264 evaluations per chart
- WC rules (R03/R05/R07/R14) count at 0.5× weight
- Scores clamped to [-10, +10]; ratings: Excellent/Strong/Moderate/Weak/Very Weak
- FastAPI with lifespan pattern (not deprecated on_event)
- SQLite with _SENTINEL testability pattern; WAL mode; immutable inserts

---

## Session 4 — Streamlit UI (3 tabs)
**Deliverable**: `src/ui/app.py`
**Tests**: 6/6

Initial 3-tab Streamlit app:
1. **Chart** — planet positions table
2. **Domain Scores** — 12-house bar chart + ratings
3. **Rule Detail** — per-house rule breakdown

Sidebar: birth date, time, lat/lon, timezone, ayanamsha, Demo button (India 1947).

---

## Session 5 — Docker Compose + Integration Tests
**Deliverable**: `Dockerfile`, `docker-compose.yml`, `Makefile`, `tests/test_integration.py`
**Tests**: 17/17

- `python:3.12-slim` + gcc for pyswisseph compilation
- api service (port 8000) + ui service (port 8501) + shared `chart_data` volume for SQLite
- `packages.txt` for Streamlit Cloud: `gcc g++ python3-dev`
- Integration tests: end-to-end journey, history ordering, Rahu/Ketu 180° invariant, score determinism, all 3 ayanamshas

**Bug fix**: Rahu/Ketu 180° check: `abs(((rahu_lon - ketu_lon) % 360) - 180)` (not `+180` before mod).

**Streamlit Cloud fix**: `fastapi` not `fastapi[standard]` in requirements.txt (avoids Rust dependency from email-validator).

---

## Session 6 — Vimshottari Dasha + South Indian Chart
**Deliverable**: `src/calculations/vimshottari_dasa.py`, `src/ui/chart_visual.py`, updated `src/ui/app.py`
**Tests**: 20/20

**Vimshottari Dasha** (`vimshottari_dasa.py`):
- 120-year nakshatra-based cycle: 9 MahaDashas × 9 AntarDashas
- Birth dasha from Moon's nakshatra: `nak_idx = int(moon_lon / 13.333)`
- Balance = `VIMSHOTTARI_YEARS[birth_lord] × (1 - elapsed_fraction)`
- Antardasha = `maha_years × VIMSHOTTARI_YEARS[antar_lord] / 120`
- 1947 India: Moon at 93.98° → Pushya (index 7) → Saturn birth dasha

**South Indian chart** (`chart_visual.py`):
- 4×4 SVG grid (520×520px, CELL=130px)
- Fixed sign positions (Pisces top-left, Aries top-2, ...)
- Lagna highlighted indigo (#4B0082/#EDE7FF)
- Benefics green (#1a7a1a), malefics dark red (#8b0000)
- Center 4 cells: diagonal cross + chart label

**UI expanded to 4 tabs**: added Vimshottari Dasha tab.

**Bug fix**: `st.date_input(min_value=date(1915, 1, 1))` — without min_value, default range starts from recent years only.

---

## Session 7 — Yoga Detection + Enriched Planet Table
**Deliverable**: `src/calculations/yogas.py`, updated `src/ui/app.py`
**Tests**: 14/14

**13 Yoga types** in 7 categories:

| Category | Yogas |
|----------|-------|
| Pancha Mahapurusha | Ruchaka/Bhadra/Hamsa/Malavya/Shasha (planet in own/exalt AND kendra) |
| Raj | Kendra+Trikona lord conjunct (dusthana lords excluded) |
| Dhana | H1/2/5/9/11 lord pairs conjunct |
| Lunar | Gajakesari, Chandra-Mangala, Adhi, Kemadruma, Shakata |
| Solar | Budha-Aditya, Vesi, Vasi, Ubhayachari |
| Special | Pancha-Graha, Guru-Chandala, Neecha Bhanga Raj |

**Key fixes during development**:
- `sign_lord(debil_si)` used for Neecha Bhanga (not `_SIGN_LORDS[debil_si]` — private)
- Rahu/Ketu excluded from planet counts: iterate `chart.planets.items()` not `.values()`
- DignityResult field is `.dignity` (not `.level`)
- DignityLevel enum names: `EXALT`, `MOOLTRIKONA`, `OWN_SIGN`, `FRIEND_SIGN`, `NEUTRAL`, `ENEMY_SIGN`, `DEBIL`

**UI expanded to 5 tabs**: Yogas tab added between Domain Scores and Vimshottari Dasha. Planet table enriched with nakshatra+pada and dignity columns.

**1947 India results**:
- Pancha-Graha Yoga (5 planets in Cancer: Sun/Moon/Mercury/Venus/Saturn)
- Gajakesari (Jupiter in Libra = H4 from Moon in Cancer)
- Multiple Dhana Yogas (Cancer lord + other H lords conjunct)
- Budha-Aditya (Sun+Mercury conjunct in Cancer)
- Kemadruma absent (Mars in Gemini is adjacent to Moon in Cancer)

---

## Bugs Fixed Across All Sessions

| ID | Module | Bug | Fix |
|----|--------|-----|-----|
| P-1 | ephemeris.py | `hour=0` treated as falsy → midnight birth fails | `if hour is None` check |
| P-4 | ephemeris.py | Unknown ayanamsha silently defaults | `raise ValueError` |
| N-1 | narayana_dasa.py | Taurus = 4yr instead of 7yr | Corrected period table |
| S-2 | shadbala.py | Chesta Bala hardcoded 3851 | `min(60, mean_motion/|speed|×60)` |
| UI-1 | app.py | Date picker default range starts ~2016 | `min_value=date(1915, 1, 1)` |

## Bugs Deferred to Session 8

| ID | Module | Bug |
|----|--------|-----|
| E-1 | ephemeris.py | JDN Gregorian +0.5 day correction missing |
| A-2 | retrograde.py | Mercury direction uses wrong row reference |

---

## Architecture at End of Session 7

```
Birth Data (date, time, lat/lon)
        ↓
src/ephemeris.py             ← pyswisseph wrapper → BirthChart
        ↓
src/calculations/            ← 9 Jyotish modules
  dignity, nakshatra, friendship, house_lord,
  chara_karak, narayana_dasa, shadbala,
  vimshottari_dasa, yogas
        ↓
src/scoring.py               ← 22 BPHS rules × 12 houses
        ↓
src/api/main.py + src/db.py  ← FastAPI + SQLite
        ↓
src/ui/chart_visual.py       ← South Indian SVG
src/ui/app.py                ← Streamlit 5-tab UI
```

---

## Test Count by Session

| After Session | Tests |
|---------------|-------|
| 3 | 70 |
| 4 | 76 |
| 5 | 93 |
| 6 | 113 |
| 7 | **127** |
