# LagnaMaster — Session Log: Sessions 8–10

> Date: 2026-03-19
> Sessions: 8 (Ashtakavarga), 9 (Gochara + Shadbala UI), 10 (Panchanga + Navamsha D9)
> Tests added: 95 (26 + 29 + 40); cumulative total: 222/222
> Commits: Session 8 → 49b615f · Session 9 → 8661536 · Session 10 → dc76852

---

## Session 8 — Ashtakavarga + Accuracy Regression Guards

### Deliverables

- **`src/calculations/ashtakavarga.py`** — Parashari Ashtakavarga (8-source bindu tables)
- **`src/ui/app.py`** — Ashtakavarga tab added (4th tab, expanding UI from 5 → 6 tabs)
- **`tests/test_ashtakavarga.py`** — 26 tests

### What Was Built

Classical Parashari Ashtakavarga computes, for each of 7 planets, how many "bindus" (dots) each of the 12 signs receives from 8 contributors (the 7 planets + the Lagna). The specific houses from each contributor that donate a bindu are encoded in fixed BPHS tables (`_BENEFIC_HOUSES` dict).

**Key data structures**:
```python
@dataclass
class AshtakavargaTable:
    planet: str
    bindus: list[int]   # 12 values; index 0 = Aries
    total: int
    def strength(self, sign_index: int) -> str  # Strong/Average/Weak

@dataclass
class AshtakavargaChart:
    planet_av: dict[str, AshtakavargaTable]  # 7 planets
    sarva: AshtakavargaTable                  # sum of all 7
```

**Fixed totals** (chart-independent):
| Planet | Sun | Moon | Mars | Mercury | Jupiter | Venus | Saturn | Sarva |
|--------|-----|------|------|---------|---------|-------|--------|-------|
| Total  | 50  | 48   | 42   | 55      | 57      | 52    | 40     | 344   |

**UI additions** (Ashtakavarga tab):
- Sarvashtakavarga 12-sign bar chart (colour-coded by strength)
- Per-planet bindu grids (lagna cell highlighted, own-sign marked with ◉)
- Full data table with per-planet columns

### Accuracy Audit — E-1 and A-2

Both bugs were in the original Excel workbook only; the Python code was already correct:

- **E-1 (JDN +0.5 correction)**: `swe.julday` handles negative UT hours correctly. `swe.julday(1947, 8, 15, -5.5, GREG_CAL)` = 2432412.2708, matching expected value. Regression test: `|india_chart.jd_ut − 2432412.2708| < 0.001`.
- **A-2 (Mercury direction row ref)**: Python uses `speed < 0` to determine retrograde — no lookup table involved. Regression tests confirm: `compute_chart(2022, 9, 20, ...)` → `is_retrograde=True`; `compute_chart(2022, 10, 15, ...)` → `is_retrograde=False`.

### Tests — 26/26

- **Structure**: 7 planet tables + Sarva; 12 bindus each; all values 0–8
- **Fixed totals**: chart-independent (assert `FIXED_TOTALS` values match)
- **Sarva**: equals element-wise sum of 7 planet arrays
- **Strength ratings**: Strong ≥5, Average 3–4, Weak ≤2
- **E-1 regression**: JD accuracy ±0.001
- **A-2 regression**: Mercury Rx direction
- **Determinism**: same input → same output

---

## Session 9 — Gochara (Transits) + Shadbala UI

### Deliverables

- **`src/calculations/gochara.py`** — Transit analysis with Sade Sati and AV bindus
- **`src/ui/app.py`** — Transits tab added + Shadbala expander in Chart tab (6 → 7 tabs)
- **`tests/test_gochara.py`** — 29 tests

### What Was Built

Gochara computes where the 9 planets are today (or on a specified date) and maps them against the natal chart to produce:
- Transit sign and house (whole-sign from natal lagna)
- Ashtakavarga bindu quality at the transit sign
- Sade Sati detection (Saturn within ±1 sign of natal Moon)
- Guru-Chandal transit (Jupiter conjunct Rahu in transit sky)

**Transit position computation**: noon UTC (`swe.julday(y, m, d, 12.0, swe.GREG_CAL)`) — location-independent for daily transit analysis.

**House formula**:
```python
def _whole_sign_house(planet_si: int, lagna_si: int) -> int:
    return (planet_si - lagna_si) % 12 + 1
```

**Sade Sati phases**:
- Rising: Saturn in sign preceding natal Moon
- Peak: Saturn in natal Moon sign
- Setting: Saturn in sign following natal Moon

**Key data structure**:
```python
@dataclass
class GocharaReport:
    transit_date: date
    natal_lagna_sign: str
    natal_moon_sign: str; natal_moon_sign_index: int
    planets: dict[str, TransitPlanet]     # 9 planets
    sade_sati: bool; sade_sati_phase: str
    guru_transit_house: int; guru_chandal_transit: bool
```

**Shadbala surface in UI** (Chart tab → expander):
- Per-planet 6-component breakdown (Uchcha/Kendradi/Ojha-Yugma/Dig/Paksha/Chesta Virupas)
- Ishta% derived from total Virupas

**Transits tab**:
- Date picker (defaults to today)
- Sade Sati banner with phase (Rising/Peak/Setting) colour-coded
- Guru-Chandal warning
- Per-planet table: natal house, AV bindus, strength

### Tests — 29/29

- **Structure**: 9 planets in `GocharaReport.planets`
- **Validity**: longitude 0–360, sign consistent with sign_index, speed sign matches is_retrograde
- **Rahu/Ketu**: always 180° apart; av_bindus = −1 (no AV table)
- **`_whole_sign_house` unit tests**: same-sign=1, adjacent=2, wrap-around, opposite=7
- **Sade Sati phases**: all 4 outcomes (Rising/Peak/Setting/None) + wrap-around (e.g. Moon in Aries, Saturn in Pisces = Rising)
- **Transit house accessor**: GocharaReport.planets[planet].natal_house
- **Default date**: `compute_gochara(chart)` with no date uses today
- **Determinism**: same date → same positions
- **Jupiter fields**: guru_transit_house and guru_chandal_transit valid

---

## Session 10 — Panchanga + Navamsha D9

### Deliverables

- **`src/calculations/panchanga.py`** — 5-limb Vedic almanac + D9 navamsha computation
- **`src/ui/chart_visual.py`** — `navamsha_svg()` added (D9 chart SVG renderer)
- **`src/ui/app.py`** — Panchanga strip in Chart tab + Navamsha D9 expander (Chart tab)
- **`tests/test_panchanga.py`** — 40 tests

### What Was Built

**Panchanga — the 5 limbs**:

| Limb | Formula | 1947 Value |
|------|---------|------------|
| Tithi | `int((moon−sun)%360/12)+1` | 28 (Krishna Trayodashi) |
| Vara | `weekday()` → planet lord | Venus / Friday |
| Nakshatra | `nakshatra_position(moon_lon)` | Pushya Pada 1, lord=Saturn |
| Yoga | `int((sun+moon)%360/(360/27))+1` | Siddhi (index 15, auspicious) |
| Karana | `int(elongation/6)+1` | Vanija (index 55) |

**Karana sequence** (60 per month):
- Index 0: Kimstughna (1st fixed)
- Indices 1–56: 7 movable karanas × 8 cycles (`_MOVABLE_KARANAS[(idx−1)%7]`)
- Indices 57–59: Shakuni, Chatushpada, Naga (fixed)

**D9 Navamsha formula**:
```python
_D9_START = {0: 0, 1: 9, 2: 6, 3: 3}  # Fire→Aries, Earth→Capricorn, Air→Libra, Water→Cancer

def _d9_sign_index(longitude: float) -> int:
    si   = int(longitude / 30) % 12
    pada = int((longitude % 30) * 9 / 30)   # 0–8
    return (_D9_START[si % 4] + pada) % 12
```

**1947 D9 known values**:
- Lagna: Taurus (si=1, Earth, start=Capricorn), degree=7.73°, pada=int(7.73×9/30)=2 → (9+2)%12=11=Pisces ✓
- Moon: Cancer (si=3, Water, start=Cancer), degree=3.98°, pada=1 → (3+1)%12=4=Leo ✓

**Bug fixed during development**:
- `AttributeError: 'NakshatraPosition' has no attribute 'lord'`
- Fix: `nakshatra_position()` returns `.dasha_lord` (not `.lord`). Changed `nak_pos.lord` → `nak_pos.dasha_lord` in `compute_panchanga()`.

**`navamsha_svg()` function** (in `chart_visual.py`):
- Same 520×520px South Indian 4×4 grid as `south_indian_svg()`
- Identical colour scheme (indigo lagna, green/red planets)
- `d9_data: dict[str, int]` — planet names → D9 sign index (excludes "lagna" key)
- `lagna_d9_si: int` — D9 sign index of ascendant

**UI additions (Chart tab)**:
- Panchanga strip: 5 metric cards (Tithi, Vara, Nakshatra, Yoga, Karana)
- Navamsha D9 expander: D9 SVG + side-by-side D1/D9 planet comparison table

### Tests — 40/40

- **Structure**: all 5 limbs present and valid ranges; `navamsha_chart` has 10 keys (lagna + 9 planets)
- **1947 known values**: Vara=Friday/Venus, Nakshatra=Pushya, Tithi=28/Krishna/Trayodashi, Yoga=Siddhi/auspicious, not full moon/new moon
- **D9 values**: Lagna=Pisces, Moon=Leo
- **Tithi arithmetic**: full moon at tithi 15, new moon at tithi 30, paksha boundary
- **D9 unit tests**: Fire/Earth/Air/Water element start signs; full 9-pada Aries cycle (Aries→Sagittarius)
- **`compute_navamsha_chart`**: 10 keys, all 0–11 range
- **Determinism**: identical inputs → identical Panchanga output

---

## Architecture After Sessions 8–10

```
src/calculations/   12 modules
  dignity.py        nakshatra.py       friendship.py      house_lord.py
  chara_karak.py    narayana_dasa.py   shadbala.py        vimshottari_dasa.py
  yogas.py          ashtakavarga.py    gochara.py         panchanga.py

src/ui/app.py       7-tab UI (Chart / Domain Scores / Yogas / Ashtakavarga /
                               Vimshottari Dasha / Transits / Rule Detail)
src/ui/chart_visual.py    south_indian_svg() + navamsha_svg()

tests/              222 tests, 9 test files — all passing
```

---

## Accuracy Bug Status (All Resolved)

| ID | Bug | Status |
|----|-----|--------|
| P-1 | Midnight birth `hour=None` | ✅ Fixed (ephemeris.py) |
| P-4 | Unknown ayanamsha silent | ✅ Fixed (ephemeris.py) |
| N-1 | Narayana Taurus=4yr→7yr | ✅ Fixed (narayana_dasa.py) |
| S-2 | Shadbala Chesta=3851 hardcoded | ✅ Fixed (shadbala.py) |
| E-1 | JDN Gregorian +0.5 correction | ✅ Not present in Python (regression test added) |
| A-2 | Mercury direction row ref | ✅ Not present in Python (regression test added) |
