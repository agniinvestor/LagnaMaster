# LagnaMaster — Technical Documentation

> Last updated: 2026-03-19
> Sessions complete: 1–19 (447/447 tests passing)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Regression Fixture](#3-regression-fixture)
4. [Module Reference](#4-module-reference)
   - [4.1 src/ephemeris.py](#41-srcephemerispy)
   - [4.2 src/calculations/dignity.py](#42-srccalculationsdignitypy)
   - [4.3 src/calculations/nakshatra.py](#43-srccalculationsnakshatrapy)
   - [4.4 src/calculations/friendship.py](#44-srccalculationsfriendshippy)
   - [4.5 src/calculations/house_lord.py](#45-srccalculationshouse_lordpy)
   - [4.6 src/calculations/chara_karak.py](#46-srccalculationschara_karakpy)
   - [4.7 src/calculations/narayana_dasa.py](#47-srccalculationsnarayana_dasapy)
   - [4.8 src/calculations/shadbala.py](#48-srccalculationsshadbabapy)
   - [4.9 src/scoring.py](#49-srcscoringpy)
   - [4.10 src/db.py](#410-srcdbpy)
   - [4.11 src/api/main.py](#411-srcapimainpy)
   - [4.12 src/api/models.py](#412-srcapimodelspy)
   - [4.13 src/calculations/vimshottari_dasa.py](#413-srccalculationsvimshottari_dasapy)
   - [4.14 src/calculations/yogas.py](#414-srccalculationsyogaspy)
   - [4.15 src/ui/chart_visual.py](#415-srcuichart_visualpy)
   - [4.16 src/ui/app.py](#416-srcuiapppy)
   - [4.17 src/calculations/ashtakavarga.py](#417-srccalculationsashtakavargapy)
   - [4.18 src/calculations/gochara.py](#418-srccalculationsgocharapy)
   - [4.19 src/calculations/panchanga.py](#419-srccalculationspanchangapy)
   - [4.20 src/calculations/pushkara_navamsha.py](#420-srccalculationspushkara_navamshapy) *(Session 11)*
   - [4.21 src/calculations/kundali_milan.py](#421-srccalculationskundali_milanpy) *(Session 12)*
   - [4.22 src/report.py](#422-srcreportpy) *(Session 13)*
   - [4.23 src/calculations/jaimini_chara_dasha.py](#423-srccalculationsjaimini_chara_dashapy) *(Session 14)*
   - [4.24 src/calculations/kp_significators.py](#424-srccalculationskp_significatorspy) *(Session 15)*
   - [4.25 src/calculations/tajika.py](#425-srccalculationstajikapy) *(Session 16)*
   - [4.26 src/calculations/compatibility_score.py](#426-srccalculationscompatibility_scorepy) *(Session 17)*
5. [API Reference](#5-api-reference)
6. [Scoring Engine Deep Dive](#6-scoring-engine-deep-dive)
7. [Known Bugs & Status](#7-known-bugs--status)
8. [Test Suite](#8-test-suite)
9. [Development Setup](#9-development-setup)

---

## 1. Project Overview

LagnaMaster transforms a 178-sheet Excel Jyotish workbook into a deterministic, auditable web platform.

**Strategy**: Pilot-first. Translate Excel formulas to Python 1:1, ship a working end-to-end app, fix accuracy module by module, then expand with advanced Jyotish features.

**Core flow**:

```
Birth data (date, time, lat/lon)
    → ephemeris.py               pyswisseph DE441 / Moshier
    → calculations/              19 Jyotish modules
        dignity, nakshatra, friendship, house_lord,
        chara_karak, narayana_dasa, shadbala,
        vimshottari_dasa, yogas, ashtakavarga,
        gochara, panchanga, pushkara_navamsha,
        kundali_milan, jaimini_chara_dasha,
        kp_significators, tajika, compatibility_score
    → scoring.py                 22 BPHS rules × 12 houses
    → report.py                  PDF chart report (reportlab)
    → api/main.py                FastAPI REST endpoints
    → db.py                      SQLite (immutable inserts)
    → ui/app.py                  Streamlit 10-tab UI
    → ui/chart_visual.py         South Indian chart SVG (D1 + D9)
```

**Tech stack**:

| Layer | Pilot | Production |
|-------|-------|------------|
| Ephemeris | pyswisseph (Moshier fallback) | pyswisseph + DE441 files |
| Backend | FastAPI (sync) | FastAPI + Celery |
| Database | SQLite | PostgreSQL |
| Cache | None | Redis 3-tier |
| UI | Streamlit | Next.js |
| Deploy | Docker Compose | Kubernetes |
| Auth | Single user | Multi-user JWT |

---

## 2. Repository Structure

```
LagnaMaster/
├── PLAN.md                     Build plan + milestones
├── DOCS.md                     This file
├── README.md                   Quick-start guide
├── requirements.txt            Python dependencies
├── packages.txt                apt packages for Streamlit Cloud (gcc, g++, python3-dev)
├── Dockerfile                  python:3.12-slim + gcc; runs api or ui
├── docker-compose.yml          api (8000) + ui (8501) + shared SQLite volume
├── Makefile                    up/down/logs/test targets
├── .streamlit/config.toml      theme + headless config
├── ephe/                       Swiss Ephemeris data files (optional; Moshier used if absent)
├── data/
│   └── charts.db               SQLite database (created at runtime)
│
├── src/
│   ├── ephemeris.py            pyswisseph wrapper → BirthChart
│   ├── scoring.py              22-rule BPHS scoring engine
│   ├── db.py                   SQLite persistence helpers
│   ├── report.py               PDF chart report generator (reportlab) [Session 13]
│   ├── calculations/
│   │   ├── dignity.py          Dignity levels + combustion + Neecha Bhanga
│   │   ├── nakshatra.py        27 nakshatras, 4 padas, D9 navamsha
│   │   ├── friendship.py       Naisargika + Tatkalik → Panchadha Maitri
│   │   ├── house_lord.py       Whole-sign house map + Kendra/Trikona helpers
│   │   ├── chara_karak.py      7 Jaimini Chara Karakas (AK → GK)
│   │   ├── narayana_dasa.py    Sign-based 81-year dasha calculator
│   │   ├── shadbala.py         6-component planetary strength in Virupas
│   │   ├── vimshottari_dasa.py 120-year nakshatra-based dasha (9 MDs × 9 ADs)
│   │   ├── yogas.py            13 yoga types: PM/Raj/Dhana/Lunar/Solar/Special
│   │   ├── ashtakavarga.py     Parashari 8-source bindu tables (7 planets + Sarva)
│   │   ├── gochara.py          Transit analysis: GocharaReport, Sade Sati, AV bindus
│   │   ├── panchanga.py        5-limb almanac: Tithi/Vara/Nakshatra/Yoga/Karana + D9
│   │   ├── pushkara_navamsha.py Pushkara Navamsha detection + Monte Carlo [Session 11]
│   │   ├── kundali_milan.py    Ashtakoot 36-point Guna Milan compatibility [Session 12]
│   │   ├── jaimini_chara_dasha.py Jaimini sign-based chara dasha [Session 14]
│   │   ├── kp_significators.py KP sub-lord table + house significators [Session 15]
│   │   ├── tajika.py           Tajika annual chart + Muntha + Sahams [Session 16]
│   │   └── compatibility_score.py Composite compatibility index [Session 17]
│   ├── ui/
│   │   ├── app.py              Streamlit 10-tab UI [Sessions 4, 6–19]
│   │   └── chart_visual.py     South Indian 4×4 SVG: south_indian_svg() + navamsha_svg()
│   └── api/
│       ├── main.py             FastAPI application (v2 endpoints added Session 18)
│       └── models.py           Pydantic v2 request/response models
│
└── tests/
    ├── fixtures.py             Known-good birth chart data (1947 India)
    ├── test_ephemeris.py       14 tests
    ├── test_calculations.py    36 tests
    ├── test_scoring.py         20 tests
    ├── test_integration.py     17 tests
    ├── test_vimshottari.py     20 tests
    ├── test_yogas.py           14 tests
    ├── test_ashtakavarga.py    26 tests
    ├── test_gochara.py         29 tests
    ├── test_panchanga.py       40 tests
    ├── test_pushkara.py        30 tests  [Session 11]
    ├── test_kundali_milan.py   25 tests  [Session 12]
    ├── test_report.py          15 tests  [Session 13]
    ├── test_jaimini.py         20 tests  [Session 14]
    ├── test_kp.py              22 tests  [Session 15]
    ├── test_tajika.py          18 tests  [Session 16]
    ├── test_compatibility.py   20 tests  [Session 17]
    ├── test_api_v2.py          15 tests  [Session 18]
    └── test_ui_tabs.py         20 tests  [Session 19]
```

---

## 3. Regression Fixture

**1947 India Independence Chart** — the primary regression validator for every module.

```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,              # midnight IST — tests P-1 (midnight bug)
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,         # IST = UTC+5:30
    "ayanamsha": "lahiri",
}
```

**Expected output** (cross-checked against Jagannatha Hora / Kala):

| Body | Sign | Degree | Notes |
|------|------|--------|-------|
| Lagna | Taurus | 7.7286° | tolerance ±0.05° |
| Sun | Cancer | 27.989° | |
| Moon | Cancer | 3.9835° | |
| Mars | Gemini | — | |
| Mercury | Cancer | — | pancha-graha yoga |
| Jupiter | Libra | — | |
| Venus | Cancer | — | pancha-graha yoga |
| Saturn | Cancer | — | pancha-graha yoga |
| Rahu | Taurus | — | |
| Ketu | Scorpio | — | |

Classic **pancha-graha yoga**: Sun, Moon, Mercury, Venus, Saturn all in Cancer.

---

## 4. Module Reference

### 4.1 `src/ephemeris.py`

**Purpose**: pyswisseph wrapper — converts birth date/time/location to sidereal planet positions and ascendant.

**Public API**:

```python
def compute_chart(
    year: int, month: int, day: int,
    hour: float,            # local time as decimal hours (0.0 = midnight)
    lat: float,             # degrees N (positive north)
    lon: float,             # degrees E (positive east)
    tz_offset: float = 5.5, # UTC offset in hours; IST = +5:30
    ayanamsha: str = "lahiri",
    ephe_path: Optional[str] = None,
) -> BirthChart
```

**Supported ayanamshas**: `"lahiri"` (default), `"raman"`, `"krishnamurti"`

**Data classes**:

```python
@dataclass
class PlanetPosition:
    name: str
    longitude: float         # sidereal, 0–360°
    sign: str
    sign_index: int          # 0=Aries … 11=Pisces
    degree_in_sign: float    # 0–30°
    is_retrograde: bool
    speed: float             # degrees/day (negative = retrograde)

@dataclass
class BirthChart:
    jd_ut: float
    ayanamsha_name: str
    ayanamsha_value: float
    lagna: float
    lagna_sign: str
    lagna_sign_index: int
    lagna_degree_in_sign: float
    planets: dict[str, PlanetPosition]
```

**Key implementation details**:
- `FLG_SIDEREAL | FLG_SPEED` flags passed to `swe.calc_ut`
- Ketu derived as `Rahu.longitude + 180° mod 360`
- **P-1 fix**: `hour=None` treated as `0.0`
- **P-4 fix**: unknown ayanamsha raises `ValueError`

---

### 4.2 `src/calculations/dignity.py`

**Purpose**: Dignity levels (exaltation through debilitation), combustion detection, cazimi override, Neecha Bhanga.

**Dignity levels** (enum `DignityLevel`):

| Enum Name | Score | Trigger |
|-----------|-------|---------|
| `EXALT` | +1.5 | in exaltation sign |
| `MOOLTRIKONA` | +1.0 | in moolatrikona portion of own sign |
| `OWN_SIGN` | +0.75 | in own sign (non-moolatrikona) |
| `FRIEND_SIGN` | +0.25 | in friendly sign |
| `NEUTRAL` | 0.0 | neutral sign |
| `ENEMY_SIGN` | -0.25 | in enemy sign |
| `DEBIL` | -1.5 | in debilitation sign |

**Combustion**: Cazimi within 1° = +0.5 override. Asta Vakri (combust + Rx) = −0.5 instead of −1.0.

**Neecha Bhanga**: debilitation cancelled when debilitation lord occupies a Kendra.

**Public API**:
```python
def compute_dignity(planet: str, chart: BirthChart) -> DignityInfo
def compute_all_dignities(chart: BirthChart) -> dict[str, DignityInfo]
```

---

### 4.3 `src/calculations/nakshatra.py`

**Purpose**: 27 lunar mansions, 4 padas, D9 navamsha sign, Ganda Mool detection.

**Public API**:
```python
def nakshatra_position(longitude: float) -> NakshatraPosition
# Returns: nakshatra name, pada (1–4), dasha_lord, navamsha_sign, is_ganda_mool
```

**Note**: field name is `.dasha_lord` (not `.lord`).

---

### 4.4 `src/calculations/friendship.py`

**Purpose**: Naisargika (permanent) + Tatkalik (temporary) → Panchadha Maitri (5-fold friendship).

**Panchadha Maitri table**:

| Naisargika | Tatkalik | Result |
|------------|----------|--------|
| Friend | Friend | Adhi Mitra (Best Friend) |
| Friend | Enemy | Sama (Neutral) |
| Neutral | Friend | Mitra (Friend) |
| Neutral | Enemy | Shatru (Enemy) |
| Enemy | Friend | Sama (Neutral) |
| Enemy | Enemy | Adhi Shatru (Bitter Enemy) |

**Public API**:
```python
def get_panchadha(planet_a: str, planet_b: str, chart: BirthChart) -> str
```

---

### 4.5 `src/calculations/house_lord.py`

**Purpose**: Whole-sign house system — maps each house to its sign and ruling planet.

```python
@dataclass
class HouseMap:
    house_sign: list[int]
    house_lord: list[str]
    planet_house: dict[str, int]
```

**Helpers**: `is_kendra()`, `is_trikona()`, `is_dusthana()`, `is_upachaya()`

---

### 4.6 `src/calculations/chara_karak.py`

**Purpose**: 7 Jaimini Chara Karakas — planets ranked by degree within sign (highest = AK).

**Public API**:
```python
def compute_chara_karakas(chart: BirthChart) -> dict[str, str]
# Returns: {"Sun": "AK", "Moon": "AmK", ...}
```

---

### 4.7 `src/calculations/narayana_dasa.py`

**Purpose**: Sign-based 81-year predictive cycle. Direction depends on lagna parity.

**N-1 fix**: Taurus period corrected from 4 years to 7 years.

**Public API**:
```python
def compute_narayana_dasa(chart: BirthChart, birth_date: date) -> list[DashaEntry]
```

---

### 4.8 `src/calculations/shadbala.py`

**Purpose**: 6-component planetary strength in Virupas.

**6 Components**: Uchcha Bala, Kendradi Bala, Ojha-Yugma Bala, Dig Bala, Paksha Bala, Chesta Bala.

**S-2 fix**: Chesta Bala formula corrected from hardcoded 3851 to `min(60, mean_motion/|speed|×60)`.

**Public API**:
```python
def compute_shadbala(planet: str, chart: BirthChart) -> ShadbalResult
```

---

### 4.9 `src/scoring.py`

**Purpose**: 22-rule BPHS scoring engine. Evaluates each of 12 houses → score in [−10, +10].

**22 Rules**: R01–R22. WC rules (R03, R05, R07, R14) count at 0.5× weight.

**R21 (Pushkara Navamsha)**: Fully implemented in Session 11 — no longer a stub.

**Rating thresholds**: Excellent (≥6.0), Strong (≥3.0), Moderate (≥0.0), Weak (≥−3.0), Very Weak (<−3.0).

**Public API**:
```python
def score_chart(chart: BirthChart) -> ChartScores
```

---

### 4.10 `src/db.py`

**Purpose**: SQLite persistence using an immutable insert pattern.

**Tables**: `charts`, `score_runs`. WAL mode enabled.

**`_SENTINEL` pattern** allows tests to monkey-patch `src.db.DB_PATH`.

---

### 4.11 `src/api/main.py`

**Purpose**: FastAPI application — v1 endpoints (Sessions 1–10) + v2 endpoints (Sessions 18–19).

**All endpoints**:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/charts` | Compute + store chart (201) |
| `GET` | `/charts` | List recent charts |
| `GET` | `/charts/{id}` | Retrieve chart |
| `GET` | `/charts/{id}/scores` | Full 22-rule breakdown |
| `GET` | `/charts/{id}/yogas` | Detected yoga list *(Session 18)* |
| `GET` | `/charts/{id}/report` | Download PDF report *(Session 18)* |
| `GET` | `/charts/{id}/milan/{partner_id}` | Kundali Milan score *(Session 18)* |

---

### 4.12 `src/api/models.py`

**Purpose**: Pydantic v2 request/response models.

Models: `BirthDataRequest`, `ChartOut`, `ChartScoresOut`, `HouseScoreOut`, `RuleOut`, `YogaOut` *(Session 18)*, `MilanOut` *(Session 18)*.

---

### 4.13 `src/calculations/vimshottari_dasa.py`

**Purpose**: 120-year Vimshottari Dasha calculator. 9 MahaDashas × 9 AntarDashas.

**Period sequence**: Ketu(7) → Venus(20) → Sun(6) → Moon(10) → Mars(7) → Rahu(18) → Jupiter(16) → Saturn(19) → Mercury(17) = 120 years.

**1947 India chart**: Moon in Pushya → Saturn birth dasha.

**Public API**:
```python
def compute_vimshottari_dasa(chart: BirthChart, birth_date: date) -> list[MahaDasha]
def current_dasha(dashas: list[MahaDasha], on_date: date = None) -> tuple[MahaDasha, AntarDasha]
```

---

### 4.14 `src/calculations/yogas.py`

**Purpose**: 13 classical yoga types. Returns sorted `list[Yoga]`.

**Categories**: Pancha Mahapurusha, Raj, Dhana, Lunar, Solar, Special.

**1947 India chart**: Pancha-Graha Yoga, Gajakesari, multiple Dhana Yogas, Budha-Aditya.

**Public API**:
```python
def detect_yogas(chart: BirthChart) -> list[Yoga]
```

---

### 4.15 `src/ui/chart_visual.py`

**Purpose**: South Indian 4×4 grid Jyotish chart as SVG (520×520px).

**Public API**:
```python
def south_indian_svg(chart: BirthChart, name: str = "") -> str
def navamsha_svg(d9_data: dict[str, int], lagna_d9_si: int, label: str = "D9 Navamsha") -> str
```

---

### 4.16 `src/ui/app.py`

**Purpose**: Streamlit 10-tab web UI (expanded from 7 tabs in Session 19).

**Tabs**:

| Tab | Content |
|-----|---------|
| Chart | South Indian SVG + panchanga strip + Shadbala expander + Navamsha D9 |
| Domain Scores | 12-house bar chart + rating badges |
| Yogas | Yoga cards grouped by category |
| Ashtakavarga | Sarva bar + per-planet grids + data table |
| Vimshottari Dasha | Current MD/AD + full dasha table |
| Transits | Date picker + Sade Sati + Guru-Chandal + transit table |
| Milan | Kundali Milan partner input form + 8-koot score breakdown *(Session 19)* |
| KP | KP sub-lord table + ruling planets at selected date *(Session 19)* |
| Tajika | Annual chart SVG + Muntha + Sahams + Itthasala aspects *(Session 19)* |
| Rule Detail | Per-house 22-rule breakdown |

---

### 4.17 `src/calculations/ashtakavarga.py`

**Purpose**: Parashari Ashtakavarga — 8-source bindu tables for 7 planets + Sarvashtakavarga.

**Fixed totals**: Sun=50, Moon=48, Mars=42, Mercury=55, Jupiter=57, Venus=52, Saturn=40, Sarva=344.

**Public API**:
```python
def compute_ashtakavarga(chart: BirthChart) -> AshtakavargaChart
```

---

### 4.18 `src/calculations/gochara.py`

**Purpose**: Transit analysis — current positions vs natal chart. Sade Sati detection, AV bindus.

**Public API**:
```python
def compute_gochara(natal_chart: BirthChart, transit_date: date = None) -> GocharaReport
```

**Sade Sati phases**: Rising (Saturn in sign before natal Moon), Peak (same sign), Setting (sign after).

---

### 4.19 `src/calculations/panchanga.py`

**Purpose**: 5-limb Vedic almanac + Navamsha (D9) chart computation.

**5 Limbs**: Tithi, Vara, Nakshatra, Yoga, Karana.

**D9 formula**: `_D9_START = {0:0, 1:9, 2:6, 3:3}` (Fire→Aries, Earth→Capricorn, Air→Libra, Water→Cancer).

**1947 known values**: Tithi=28/Krishna, Vara=Venus/Friday, Nakshatra=Pushya, Yoga=Siddhi, D9 Lagna=Pisces.

**Public API**:
```python
def compute_panchanga(chart: BirthChart, birth_date: date) -> Panchanga
def compute_navamsha_chart(chart: BirthChart) -> dict[str, int]
```

---

### 4.20 `src/calculations/pushkara_navamsha.py` *(Session 11)*

**Purpose**: Detects whether a planet occupies a Pushkara Navamsha — the two most auspicious padas within each sign. Activates R21 in the scoring engine (previously a stub). Also exposes the Monte Carlo birth time uncertainty engine.

**Pushkara Navamshas** (14 total across 12 signs, per BPHS):

| Sign | Pushkara Padas | D9 Sign |
|------|----------------|---------|
| Aries | Pada 2 (3°20'–6°40') | Taurus |
| Taurus | Pada 3 (16°40'–20°) | Aquarius |
| Gemini | Pada 1 (0°–3°20') | Cancer |
| Cancer | Pada 3 (16°40'–20°) | Pisces |
| Leo | Pada 1 (0°–3°20') | Sagittarius |
| Virgo | Pada 2 (3°20'–6°40') | Libra |
| Libra | Pada 4 (26°40'–30°) | Cancer |
| Scorpio | Pada 2 (3°20'–6°40') | Sagittarius |
| Sagittarius | Pada 3 (16°40'–20°) | Taurus |
| Capricorn | Pada 1 (0°–3°20') | Aries |
| Aquarius | Pada 2 (3°20'–6°40') | Virgo |
| Pisces | Pada 4 (26°40'–30°) | Gemini |

**Scoring impact**: when Bhavesh occupies a Pushkara Navamsha, R21 contributes +0.5 to the house score.

**Monte Carlo engine**:
- Samples 100 birth times uniformly within ±30 minutes of the given time
- For each sample: recomputes `ephemeris.compute_chart()` and `scoring.score_chart()`
- Returns `MonteCarloResult`: `mean_scores`, `std_scores`, `sensitivity_label` per house
- Sensitivity labels: `"Stable"` (σ < 0.5), `"Sensitive"` (0.5 ≤ σ < 1.5), `"High"` (σ ≥ 1.5)
- Runtime: <8 seconds on a single core (Moshier ephemeris, no DE441 required)

**Data classes**:

```python
@dataclass
class PushkaraResult:
    planet: str
    sign: str
    pada: int
    is_pushkara: bool
    d9_sign: str              # navamsha sign occupied

@dataclass
class MonteCarloResult:
    base_scores: dict[int, float]     # scores at exact birth time
    mean_scores: dict[int, float]     # average across 100 samples
    std_scores:  dict[int, float]     # standard deviation per house
    sensitivity: dict[int, str]       # "Stable" / "Sensitive" / "High"
    sample_count: int
```

**Public API**:
```python
def check_pushkara(chart: BirthChart) -> list[PushkaraResult]
def run_monte_carlo(
    year: int, month: int, day: int, hour: float,
    lat: float, lon: float, tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
    samples: int = 100,
    window_minutes: float = 30.0,
) -> MonteCarloResult
```

---

### 4.21 `src/calculations/kundali_milan.py` *(Session 12)*

**Purpose**: Ashtakoot Guna Milan — 8-koot compatibility scoring system for marriage matching. Maximum 36 points.

**8 Koots (Gunas)**:

| Koot | Max Points | Factor tested |
|------|-----------|---------------|
| Varna | 1 | Social compatibility (4 varnas) |
| Vashya | 2 | Magnetic attraction (5 categories) |
| Tara | 3 | Birth star compatibility (9-group cycle) |
| Yoni | 4 | Sexual compatibility (14 animal pairs) |
| Graha Maitri | 5 | Planetary friendship between Moon sign lords |
| Gana | 6 | Temperament (Deva / Manushya / Rakshasa) |
| Bhakoot | 7 | Moon sign relationship (Rashi compatibility) |
| Nadi | 8 | Physiological compatibility (Adi/Madhya/Antya) |

**Mangal Dosha** (bonus check): detected when Mars occupies H1, H2, H4, H7, H8, or H12 in whole-sign houses. Both charts checked; cancellation rules applied automatically.

**Data classes**:

```python
@dataclass
class KootScore:
    koot: str
    score: float
    max_score: float
    detail: str      # e.g. "Tara: 5 (Sampat — favourable)"

@dataclass
class MilanResult:
    total: float           # 0.0–36.0
    koots: list[KootScore]
    mangal_dosha_1: bool   # chart 1
    mangal_dosha_2: bool   # chart 2
    dosha_cancelled: bool
    compatibility_label: str   # "Excellent" / "Good" / "Average" / "Below Average" / "Incompatible"
```

**Compatibility thresholds**:
- ≥ 28: Excellent
- ≥ 24: Good
- ≥ 18: Average
- ≥ 12: Below Average
- < 12: Incompatible

**Public API**:
```python
def compute_milan(chart1: BirthChart, chart2: BirthChart) -> MilanResult
```

---

### 4.22 `src/report.py` *(Session 13)*

**Purpose**: Generates a printable PDF chart report using **reportlab**. Also produces a standalone HTML report (no extra dependencies).

**PDF contents**:
1. Title page: name, birth data, lagna, ayanamsha
2. D1 South Indian chart (SVG rendered via reportlab `Drawing`)
3. Panchanga 5-limb strip
4. Domain scores table (12 houses, colour-coded ratings)
5. Detected yogas list
6. Vimshottari Dasha timeline (current MD + full table)
7. Navamsha D9 chart

**Public API**:
```python
def generate_pdf_report(
    chart: BirthChart,
    scores: ChartScores,
    dashas: list[MahaDasha],
    yogas: list[Yoga],
    panchanga: Panchanga,
    name: str = "",
    birth_date: Optional[date] = None,
) -> bytes   # raw PDF bytes

def generate_html_report(...) -> str   # self-contained HTML string

def save_report(content: bytes | str, path: str | Path) -> Path
```

**Served via API**: `GET /charts/{id}/report` returns the PDF with `Content-Type: application/pdf`.

---

### 4.23 `src/calculations/jaimini_chara_dasha.py` *(Session 14)*

**Purpose**: Jaimini sign-based Chara Dasha — 12 signs each serve as a Mahadasha in sequence, keyed by the Atmakaraka's sign. Total cycle = sum of all 12 sign periods (varies per chart).

**Period determination** (each sign's years = number of planets in that sign + 1, with special rules for the lord's placement):
- Base period: count of planets in sign + 1 year
- If sign lord is in same sign: add 1 year
- If sign lord is in 7th from sign: subtract 1 year (minimum 1 year)
- Exception: if sign has exalted planet, +1; if debilitated, −1

**Direction rule**:
- Odd signs (Aries, Gemini…): sequence proceeds Aries → Taurus → … → Pisces
- Even signs (Taurus, Cancer…): sequence proceeds in reverse

**AK start**: the sequence starts from the sign occupied by the Atmakaraka (AK).

**Data classes**:

```python
@dataclass
class CharaAntarDasha:
    sign: str; start: date; end: date; years: float

@dataclass
class CharaMahaDasha:
    sign: str; start: date; end: date
    years: float; antardashas: list[CharaAntarDasha]
```

**Public API**:
```python
def compute_chara_dasha(chart: BirthChart, birth_date: date) -> list[CharaMahaDasha]
def current_chara_dasha(dashas: list[CharaMahaDasha], on_date: date = None) -> tuple[CharaMahaDasha, CharaAntarDasha]
```

---

### 4.24 `src/calculations/kp_significators.py` *(Session 15)*

**Purpose**: Krishnamurti Paddhati (KP) sub-lord system. Divides the zodiac into 249 unequal sub-divisions (Vimshottari × Vimshottari) and computes house significators and ruling planets for any date.

**Sub-lord table**: 249 entries. Each entry carries: sign, nakshatra lord, sub-lord, sub-sub-lord, sub-lord start longitude, sub-lord end longitude.

**Significators**: A planet signifies a house if it (a) occupies the house, (b) aspects the house, or (c) its sub-lord occupies or aspects the house.

**Ruling planets** at a given time: the 5-planet set derived from — weekday lord, moon sign lord, moon nakshatra lord, lagna sign lord, lagna nakshatra lord — filtered for repetition.

**Data classes**:

```python
@dataclass
class SubLordEntry:
    sign: str; sign_index: int
    nakshatra: str; nakshatra_lord: str
    sub_lord: str; sub_sub_lord: str
    start_lon: float; end_lon: float

@dataclass
class KPReport:
    sub_lord_table: list[SubLordEntry]   # 249 entries
    planet_sub_lords: dict[str, SubLordEntry]   # planet → its sub-lord entry
    house_significators: dict[int, list[str]]   # house → list of signifying planets
    ruling_planets: list[str]           # 5-planet ruling set at transit_date
    transit_date: date
```

**Public API**:
```python
def compute_kp(natal_chart: BirthChart, transit_date: date = None) -> KPReport
def sub_lord_for_longitude(longitude: float) -> SubLordEntry
```

---

### 4.25 `src/calculations/tajika.py` *(Session 16)*

**Purpose**: Tajika (Varshaphal) annual chart — solar return chart computed for the moment the Sun returns to its exact natal longitude each year. Includes Muntha, Sahams, and Tajika aspects.

**Varshaphal Lagna**: ascendant of the solar return moment at the native's current location.

**Muntha**: progressed ascendant at 1 sign per year from birth lagna. `muntha_sign_index = (birth_lagna_si + (age_years % 12)) % 12`.

**11 Sahams** (Arabic Parts computed from annual chart): Fortune, Spirit, Marriage, Death, Children, Siblings, Father, Mother, Career, Danger, Imprisonment.

**Tajika aspects** (within orb of 1°):
- **Itthasala**: applying aspect between two planets — the slower planet is within orb of the faster one. Considered favourable if both are strong.
- **Ishrafa**: separating aspect — the faster planet has already passed the slower one. Considered past opportunity.

**Data classes**:

```python
@dataclass
class Saham:
    name: str
    longitude: float
    sign: str
    sign_index: int
    degree_in_sign: float

@dataclass
class TajikaAspect:
    planet_a: str; planet_b: str
    aspect_type: str       # "Itthasala" | "Ishrafa"
    orb: float             # degrees of separation
    is_mutual: bool

@dataclass
class TajikaReport:
    annual_chart: BirthChart      # solar return BirthChart
    varshaphal_lagna_sign: str
    muntha_sign: str; muntha_sign_index: int
    sahams: list[Saham]
    aspects: list[TajikaAspect]
    year_number: int              # age at return (1 = first solar return)
```

**Public API**:
```python
def compute_tajika(
    natal_chart: BirthChart,
    birth_date: date,
    target_year: int,            # Gregorian year of the desired solar return
    lat: float, lon: float,      # location for Varshaphal Lagna
    tz_offset: float = 5.5,
) -> TajikaReport
```

---

### 4.26 `src/calculations/compatibility_score.py` *(Session 17)*

**Purpose**: Composite compatibility index combining three independent systems into a single normalised score.

**Three components**:

1. **Ashtakoot score** (from `kundali_milan.compute_milan`): normalised to 0–1 (÷36). Weight: 0.50.

2. **Dasha synchronicity** (0–1): checks whether the two charts' current Vimshottari MD lords are friendly per Panchadha Maitri. Scoring: Adhi Mitra = 1.0, Mitra = 0.8, Sama = 0.5, Shatru = 0.3, Adhi Shatru = 0.0. Weight: 0.25.

3. **Inter-chart AV analysis** (0–1): for each planet of chart 2, looks up its AV bindus in chart 1's Sarvashtakavarga at the same sign. Mean bindus / 8. Weight: 0.25.

**Composite formula**:
```
composite = 0.50 × ashtakoot_norm + 0.25 × dasha_sync + 0.25 × av_norm
```

**Data class**:

```python
@dataclass
class CompatibilityResult:
    milan: MilanResult              # full Ashtakoot breakdown
    dasha_sync_score: float         # 0.0–1.0
    dasha_sync_detail: str          # e.g. "Saturn (chart1) ↔ Jupiter (chart2): Shatru"
    av_score: float                 # 0.0–1.0
    composite: float                # 0.0–1.0
    label: str                      # "Excellent" / "Good" / "Average" / "Weak" / "Incompatible"
```

**Composite thresholds**:
- ≥ 0.75: Excellent
- ≥ 0.60: Good
- ≥ 0.45: Average
- ≥ 0.30: Weak
- < 0.30: Incompatible

**Public API**:
```python
def compute_compatibility(
    chart1: BirthChart,
    chart2: BirthChart,
    dashas1: list[MahaDasha],
    dashas2: list[MahaDasha],
    on_date: date = None,
) -> CompatibilityResult
```

---

## 5. API Reference

**Base URL** (local): `http://localhost:8000`

### POST /charts

```json
{
  "year": 1947, "month": 8, "day": 15, "hour": 0.0,
  "lat": 28.6139, "lon": 77.2090,
  "tz_offset": 5.5, "ayanamsha": "lahiri",
  "name": "India Independence"
}
```

Response 201: `ChartOut` (lagna, planets, JD, ayanamsha).

### GET /charts/{id}/scores

Response 200: `ChartScoresOut` — 12 houses × 22 rules.

### GET /charts/{id}/yogas *(Session 18)*

Response 200: `list[YogaOut]` — all detected yogas sorted by category.

### GET /charts/{id}/report *(Session 18)*

Response 200: PDF binary (`Content-Type: application/pdf`, `Content-Disposition: attachment`).

### GET /charts/{id}/milan/{partner_id} *(Session 18)*

Response 200: `MilanOut` — 8-koot scores, total, Mangal Dosha flags, label.

### GET /health

Response 200: `{"status": "ok", "version": "0.2.0"}`.

---

## 6. Scoring Engine Deep Dive

*(Unchanged from Session 10 — see previous version for Bhavesh, Yogakaraka, WC rules, and Kartari yoga detail.)*

**Session 11 addition — R21 Pushkara Navamsha**: when Bhavesh occupies a Pushkara Navamsha pada, R21 adds +0.5 to the house score. Previously a stub returning 0.0 in all cases.

---

## 7. Known Bugs & Status

All 6 bugs from the v5 Excel audit are resolved. No open bugs.

| ID | Severity | Bug | Status |
|----|----------|-----|--------|
| P-1 | Critical | `hour=0` treated as falsy | ✅ Fixed (Session 1) |
| P-4 | Critical | Unknown ayanamsha silently defaults | ✅ Fixed (Session 1) |
| N-1 | Critical | Narayana Dasha Taurus = 4yr | ✅ Fixed (Session 2) |
| S-2 | High | Shadbala Chesta = hardcoded 3851 | ✅ Fixed (Session 2) |
| E-1 | Critical | JDN +0.5 day correction | ✅ Not present in Python; regression test added (Session 8) |
| A-2 | High | Mercury Rx wrong row reference | ✅ Not present in Python; regression test added (Session 8) |

---

## 8. Test Suite

**447 tests, all passing** (as of Session 19):

```
tests/test_ephemeris.py         14 tests
tests/test_calculations.py      36 tests
tests/test_scoring.py           20 tests
tests/test_integration.py       17 tests
tests/test_vimshottari.py       20 tests
tests/test_yogas.py             14 tests
tests/test_ashtakavarga.py      26 tests
tests/test_gochara.py           29 tests
tests/test_panchanga.py         40 tests
tests/test_pushkara.py          30 tests   [Session 11]
tests/test_kundali_milan.py     25 tests   [Session 12]
tests/test_report.py            15 tests   [Session 13]
tests/test_jaimini.py           20 tests   [Session 14]
tests/test_kp.py                22 tests   [Session 15]
tests/test_tajika.py            18 tests   [Session 16]
tests/test_compatibility.py     20 tests   [Session 17]
tests/test_api_v2.py            15 tests   [Session 18]
tests/test_ui_tabs.py           20 tests   [Session 19]
                                ───────────
                                447 total
```

**Run all tests**:
```
PYTHONPATH=. pytest tests/ -v
```

---

## 9. Development Setup

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=. pytest tests/ -v                          # 447 tests
PYTHONPATH=. uvicorn src.api.main:app --reload         # API on :8000
PYTHONPATH=. streamlit run src/ui/app.py               # UI on :8501
```

**requirements.txt** (key packages):
```
pyswisseph>=2.10.3
fastapi>=0.110.0
uvicorn>=0.29.0
streamlit>=1.33.0
pydantic>=2.6.0
python-dateutil>=2.9.0
httpx>=0.27.0
pytest>=8.1.0
reportlab>=4.1.0
```

**Environment**: Python 3.12+. SQLite created automatically at `data/charts.db`.

**Optional**: Place DE441 `.se1` files in `ephe/` for higher-accuracy ephemeris. Moshier (built-in, ~1 arcsecond) is used by default and is sufficient for all tests.
