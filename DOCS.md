# LagnaMaster — Technical Documentation

> Last updated: 2026-03-19
> Sessions complete: 1, 2, 3 (pilot build — Sessions 4–6 remaining)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Regression Fixture](#3-regression-fixture)
4. [Module Reference](#4-module-reference)
   - [src/ephemeris.py](#41-srcephemerispy)
   - [src/calculations/dignity.py](#42-srccalculationsdignitypy)
   - [src/calculations/nakshatra.py](#43-srccalculationsnakshatrapy)
   - [src/calculations/friendship.py](#44-srccalculationsfriendshippy)
   - [src/calculations/house_lord.py](#45-srccalculationshouse_lordpy)
   - [src/calculations/chara_karak.py](#46-srccalculationschara_karakpy)
   - [src/calculations/narayana_dasa.py](#47-srccalculationsnarayana_dasapy)
   - [src/calculations/shadbala.py](#48-srccalculationsshadbabapy)
   - [src/scoring.py](#49-srcscoringpy)
   - [src/db.py](#410-srcdbpy)
   - [src/api/main.py](#411-srcapimainpy)
   - [src/api/models.py](#412-srcapimodelspy)
5. [API Reference](#5-api-reference)
6. [Scoring Engine Deep Dive](#6-scoring-engine-deep-dive)
7. [Known Bugs & Status](#7-known-bugs--status)
8. [Test Suite](#8-test-suite)
9. [Development Setup](#9-development-setup)

---

## 1. Project Overview

LagnaMaster transforms a 178-sheet Excel Jyotish workbook into a deterministic, auditable web platform.

**Strategy**: Pilot-first. Translate Excel formulas to Python 1:1 (preserving bugs), ship a working end-to-end app, then fix calculation accuracy module by module in Sessions 7–10.

**Core flow**:
```
Birth data (date, time, lat/lon)
    → ephemeris.py          pyswisseph DE441 / Moshier
    → calculations/         7 Jyotish modules (Excel CALC sheets → Python)
    → scoring.py            22 BPHS rules × 12 houses
    → api/main.py           FastAPI REST endpoints
    → db.py                 SQLite (immutable inserts)
    → ui/app.py             Streamlit (Session 4)
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
├── requirements.txt            Python dependencies
├── ephe/                       Swiss Ephemeris data files (optional; Moshier used if absent)
├── data/
│   └── charts.db               SQLite database (created at runtime)
│
├── src/
│   ├── ephemeris.py            pyswisseph wrapper → BirthChart
│   ├── scoring.py              22-rule BPHS scoring engine
│   ├── db.py                   SQLite persistence helpers
│   ├── calculations/
│   │   ├── dignity.py          Dignity levels + combustion + Neecha Bhanga
│   │   ├── nakshatra.py        27 nakshatras, 4 padas, D9 navamsha
│   │   ├── friendship.py       Naisargika + Tatkalik → Panchadha Maitri
│   │   ├── house_lord.py       Whole-sign house map + Kendra/Trikona helpers
│   │   ├── chara_karak.py      7 Jaimini Chara Karakas (AK → GK)
│   │   ├── narayana_dasa.py    Sign-based 81-year dasha calculator
│   │   └── shadbala.py         6-component planetary strength in Virupas
│   └── api/
│       ├── main.py             FastAPI application
│       └── models.py           Pydantic request/response models
│
└── tests/
    ├── fixtures.py             Known-good birth chart data (1947 India)
    ├── test_ephemeris.py       14 tests — wrapper + position accuracy
    ├── test_calculations.py    36 tests — all 7 calculation modules
    └── test_scoring.py         20 tests — scoring engine + API endpoints
```

---

## 3. Regression Fixture

**1947 India Independence Chart** — the primary regression validator for every module.

```python
# Birth: 1947-08-15 00:00 IST, New Delhi
# Coordinates: 28.6139°N, 77.2090°E
# Ayanamsha: Lahiri (~23.1489° at this epoch)

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
H1 lord (Venus) is bhavesh for Taurus lagna.

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
    sign: str                # e.g. "Taurus"
    sign_index: int          # 0=Aries … 11=Pisces
    degree_in_sign: float    # 0–30°
    is_retrograde: bool
    speed: float             # degrees/day (negative = retrograde)

@dataclass
class BirthChart:
    jd_ut: float             # Julian Day (UT)
    ayanamsha_name: str
    ayanamsha_value: float   # e.g. ~23.15° in 1947
    lagna: float             # sidereal longitude, 0–360°
    lagna_sign: str
    lagna_sign_index: int
    lagna_degree_in_sign: float
    planets: dict[str, PlanetPosition]   # Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu
```

**Key implementation details**:
- `FLG_SIDEREAL | FLG_SPEED` flags passed to `swe.calc_ut` — ayanamsha subtracted automatically
- Ketu derived as `Rahu.longitude + 180° mod 360`
- Moshier ephemeris (built-in, ~1 arcsec accuracy) used if no `ephe/` data files exist
- **P-1 fix**: `hour=None` treated as `0.0` (midnight)
- **P-4 fix**: unknown ayanamsha raises `ValueError` immediately, never silently defaults

---

### 4.2 `src/calculations/dignity.py`

**Purpose**: Dignity levels (exaltation through debilitation), combustion detection, cazimi override, Neecha Bhanga.

**Dignity levels** (enum `DignityLevel`):
| Level | Score | Trigger |
|-------|-------|---------|
| DEEP_EXALT | +2.0 | within 1° of exact exaltation point |
| EXALTED | +1.5 | in exaltation sign |
| MOOLATRIKONA | +1.0 | in moolatrikona portion of own sign |
| OWN_SIGN | +0.75 | in own sign (non-moolatrikona) |
| FRIENDLY | +0.25 | in friendly sign |
| NEUTRAL | 0.0 | |
| ENEMY | -0.25 | in enemy sign |
| DEBILITATED | -1.5 | in debilitation sign |
| DEEP_DEBIL | -2.0 | within 1° of exact debilitation point |

**Combustion detection**:
- Each planet has a combustion orb (e.g. Moon: 12°, Mars: 17°, Mercury: 14°/12° direct/Rx)
- **Cazimi** (within 1° of Sun): overrides combustion → positive effect (+0.5 in scoring)
- **Retrograde orb**: `Rx_orb = direct_orb − 2°` (per Saravali Ch.3)
- **Asta Vakri** (combust + Rx): reduced negative effect (`-0.5` vs `-1.0`)

**Neecha Bhanga** (cancellation of debilitation):
- Triggered when the debilitation lord (lord of debilitation sign) occupies a Kendra house
- Result: debilitation effectively cancelled → neutral dignity

**Public API**:
```python
def compute_dignity(planet: str, chart: BirthChart) -> DignityInfo
def compute_all_dignities(chart: BirthChart) -> dict[str, DignityInfo]
```

---

### 4.3 `src/calculations/nakshatra.py`

**Purpose**: 27 lunar mansions, 4 padas (quarters), D9 navamsha sign, Ganda Mool detection.

**27 Nakshatras** (each spanning 13°20' = 800'):
- Each nakshatra has 4 padas of 3°20' each
- Navamsha (D9) sign formula: `(nak_idx * 4 + (pada - 1)) % 12`

**Ganda Mool nakshatras** (inauspicious junction points):
`Ashwini, Ashlesha, Magha, Jyeshtha, Mula, Shatabhisha, Revati`

**Public API**:
```python
def nakshatra_position(longitude: float) -> NakshatraPosition
# Returns: nakshatra name, pada (1–4), lord, navamsha_sign, is_ganda_mool
```

---

### 4.4 `src/calculations/friendship.py`

**Purpose**: Naisargika (permanent) + Tatkalik (temporary) planetary friendship → Panchadha Maitri (5-fold friendship).

**Tatkalik friendship rule**:
- Planets in houses 2/3/4/10/11/12 from another planet = Temporary Friend
- Planets in houses 1/5/6/7/8/9 from another planet = Temporary Enemy
- Symmetric (mutual)

**Panchadha Maitri table**:
| Naisargika | Tatkalik | Result |
|------------|----------|--------|
| Friend | Friend | Adhi Mitra (Best Friend) |
| Friend | Enemy | Sama (Neutral) |
| Neutral | Friend | Mitra (Friend) |
| Neutral | Enemy | Shatru (Enemy) |
| Enemy | Friend | Sama (Neutral) |
| Enemy | Enemy | Adhi Shatru (Bitter Enemy) |

**Note**: 22 asymmetric pairs preserved in the Naisargika matrix (e.g. Sun is friendly to Moon but Moon is neutral to Sun).

**Public API**:
```python
def get_naisargika(planet_a: str, planet_b: str) -> str   # "Friend"/"Neutral"/"Enemy"
def get_tatkalik(planet_a: str, planet_b: str, chart: BirthChart) -> str
def get_panchadha(planet_a: str, planet_b: str, chart: BirthChart) -> str
```

---

### 4.5 `src/calculations/house_lord.py`

**Purpose**: Whole-sign house system — maps each house to its sign and ruling planet.

**Whole-sign system**: House 1 = Lagna sign; each subsequent house is the next sign in order.

```python
@dataclass
class HouseMap:
    house_sign: list[int]    # house_sign[0] = sign_index of H1 (= lagna_sign_index)
    house_lord: list[str]    # house_lord[0] = lord of H1
    planet_house: dict[str, int]  # e.g. {"Sun": 3, "Moon": 3, ...}
```

**Helper functions**:
```python
def is_kendra(house: int) -> bool      # H1/H4/H7/H10
def is_trikona(house: int) -> bool     # H1/H5/H9
def is_dusthana(house: int) -> bool    # H6/H8/H12
def is_upachaya(house: int) -> bool    # H3/H6/H10/H11
```

**Sign lords** (BPHS standard):
- Aries/Scorpio → Mars; Taurus/Libra → Venus; Gemini/Virgo → Mercury
- Cancer → Moon; Leo → Sun; Sagittarius/Pisces → Jupiter; Capricorn/Aquarius → Saturn
- Rahu/Ketu have no sign lordship in Parashari

---

### 4.6 `src/calculations/chara_karak.py`

**Purpose**: 7 Jaimini Chara Karakas — planets ranked by degree within their sign (highest = Atmakaraka).

**7 Karakas** (in rank order, highest degree first):
1. Atmakaraka (AK) — soul significator
2. Amatyakaraka (AmK) — career/mind
3. Bhratrukaraka (BK) — siblings
4. Matrukaraka (MK) — mother
5. Pitrukaraka (PK) — father
6. Putrakaraka (PuK) — children
7. Gnatikaraka (GK) — relatives/obstacles

**1947 India chart**: Sun = AK (27.99°), Moon = DK/AmK (3.98° — lowest in Cancer)

**Public API**:
```python
def compute_chara_karakas(chart: BirthChart) -> dict[str, str]
# Returns: {"Sun": "AK", "Moon": "AmK", ...}
```

---

### 4.7 `src/calculations/narayana_dasa.py`

**Purpose**: Sign-based 81-year predictive cycle. Direction depends on lagna parity.

**Dasha periods** (total = 81 years):
| Sign | Years | | Sign | Years |
|------|----|--|------|-------|
| Aries | 6 | | Libra | 1 |
| Taurus | **7** | | Scorpio | 11 |
| Gemini | 2 | | Sagittarius | 5 |
| Cancer | 10 | | Capricorn | 7 |
| Leo | 9 | | Aquarius | 12 |
| Virgo | 8 | | Pisces | 3 |

**Direction rule**:
- Odd Lagna sign (Aries, Gemini, Leo…) → forward (Aries → Taurus → Gemini…)
- Even Lagna sign (Taurus, Cancer, Virgo…) → backward (Taurus → Aries → Pisces…)

**N-1 fix**: Taurus was 4 years in the Excel source; corrected to 7 years (standard BPHS).

**1947 India chart** (Taurus Lagna, even → backward):
- Dasha 1: Taurus (7y), Dasha 2: Aries (6y), Dasha 3: Pisces (3y)…

**Public API**:
```python
def compute_narayana_dasa(chart: BirthChart, birth_date: date) -> list[DashaEntry]
# DashaEntry: sign, start_date, end_date, years
```

---

### 4.8 `src/calculations/shadbala.py`

**Purpose**: 6-component planetary strength in Virupas (points). Higher = stronger planet.

**6 Components**:

| Component | Max Virupas | Formula |
|-----------|-------------|---------|
| Uchcha Bala (Positional) | 60 | `60 × (180 − dist_from_exalt) / 180` |
| Kendradi Bala | 60 | Kendra=60, Panapara=30, Apoklima=15 |
| Ojha-Yugma Bala | 30 | Male planet in odd sign OR female in even sign = 30V |
| Dig Bala | 60 | `60 × (1 − dist_from_peak / 6)` |
| Paksha Bala | 60 | Lunar phase; benefics wax, malefics wane |
| Chesta Bala | 60 | `min(60, mean_motion / |actual_speed| × 60)`; Rx planet = 60V |

**Dig Bala peak positions**:
- Sun/Mars: H10; Moon/Venus: H4; Mercury/Jupiter: H1; Saturn: H7

**S-2 fix**: Excel cell J14 formula was `3851` (hardcoded error). Corrected to proper Chesta formula: `min(60, mean_motion/|speed|×60)`.

**Public API**:
```python
def compute_shadbala(planet: str, chart: BirthChart) -> ShadbalResult
# ShadbalResult: uchcha, kendradi, ojha_yugma, dig, paksha, chesta, total
```

---

### 4.9 `src/scoring.py`

**Purpose**: 22-rule BPHS scoring engine. Evaluates each of 12 houses and returns a score in [-10, +10].

**22 Rules** (source: LEGEND_ScoringRules in Excel):

| Rule | Weight | Description | WC? |
|------|--------|-------------|-----|
| R01 | +0.50 | Gentle sign in house | |
| R02 | +1.00 (+1.5 if Yogakaraka) | Benefic in house | |
| R03 | +0.75 | Benefic aspects house | ✓ |
| R04 | +2.00 | Bhavesh in Kendra/Trikon | |
| R05 | +0.50 | Bhavesh with Kendra/Trikon lord | ✓ |
| R06 | +1.00 (+1.5 if Yogakaraka) | Bhavesh with benefic | |
| R07 | +0.50 | Benefic aspects Bhavesh sign | ✓ |
| R08 | +0.75 | Bhavesh in Shubh Kartari | |
| R09 | -1.00 | Malefic in house | |
| R10 | -1.00 | Malefic aspects house | |
| R11 | -1.25 | Dusthana lord in house | |
| R12 | -0.75 | House in Paap Kartari | |
| R13 | -1.00 | Bhavesh with malefic | |
| R14 | -0.50 | Malefic aspects Bhavesh sign | ✓ |
| R15 | -2.00 | Bhavesh in Dusthana | |
| R16 | -1.00 | Bhavesh with Dusthana lord | |
| R17 | +0.50 | Sthir Karak in Kendra/Trikon | |
| R18 | -0.50 | Sthir Karak in Dusthana | |
| R19 | -1.00 (cazimi: +0.5; Rx+combust: -0.5) | Bhavesh combust | |
| R20 | +0.50 | Bhavesh in Dig Bala house | |
| R21 | 0.0 | Pushkara Navamsha (deferred — stub) | |
| R22 | Jup/Sat: +0.25; Merc/Ven/Mars: -0.50 | Bhavesh retrograde | |

**WC (Worth Considering) rules** (R03, R05, R07, R14): count at 0.5× weight in aggregate.

**Scoring formula**:
```
raw_score = Σ(rule.score × (0.5 if WC else 1.0))
final_score = clamp(raw_score, -10.0, +10.0)
```

**Rating thresholds**:
| Score | Rating |
|-------|--------|
| ≥ 6.0 | Excellent |
| ≥ 3.0 | Strong |
| ≥ 0.0 | Moderate |
| ≥ -3.0 | Weak |
| < -3.0 | Very Weak |

**Graha Drishti** (Parashari aspects used in R03/R07/R10/R14):
- All planets: 7th aspect
- Mars additionally: 4th + 8th
- Jupiter additionally: 5th + 9th
- Saturn additionally: 3rd + 10th

**Kartari yoga** (hemming):
- Shubh Kartari (R08): sign hemmed between benefics in adjacent signs
- Paap Kartari (R12): sign hemmed between malefics in adjacent signs

**House domains and Sthir Karakas** (R17/R18):
| House | Domain | Sthir Karak |
|-------|---------|-------------|
| H1 | Self & Vitality | Sun |
| H2 | Wealth & Family | Jupiter |
| H3 | Courage & Skills | Mars |
| H4 | Home & Happiness | Moon |
| H5 | Intellect & Children | Jupiter |
| H6 | Challenges | Mars, Saturn |
| H7 | Relationships | Venus |
| H8 | Transformation | Saturn |
| H9 | Fortune & Dharma | Jupiter |
| H10 | Career & Status | Sun, Mercury, Jupiter, Saturn |
| H11 | Gains & Income | Jupiter |
| H12 | Liberation & Loss | Saturn |

**Public API**:
```python
def score_chart(chart: BirthChart) -> ChartScores

@dataclass
class ChartScores:
    lagna_sign: str
    houses: dict[int, HouseScore]
    def summary(self) -> str    # ASCII table of all 12 houses

@dataclass
class HouseScore:
    house: int
    domain: str
    bhavesh: str        # house lord
    bhavesh_house: int
    rules: list[RuleResult]
    raw_score: float
    final_score: float  # clamped to [-10, +10]
    rating: str

@dataclass
class RuleResult:
    rule: str           # e.g. "R04"
    description: str
    score: float
    is_wc: bool
    triggered: bool
```

---

### 4.10 `src/db.py`

**Purpose**: SQLite persistence using an immutable insert pattern (charts are never updated).

**Tables**:
```sql
CREATE TABLE charts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT    NOT NULL,         -- ISO 8601 UTC
    name        TEXT,                     -- optional label
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    hour        REAL    NOT NULL,
    lat         REAL    NOT NULL,
    lon         REAL    NOT NULL,
    tz_offset   REAL    NOT NULL DEFAULT 5.5,
    ayanamsha   TEXT    NOT NULL DEFAULT 'lahiri',
    chart_json  TEXT    NOT NULL,         -- JSON: lagna + all planets
    scores_json TEXT                      -- JSON: 12 house scores (may be null)
);

CREATE TABLE score_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_id    INTEGER NOT NULL REFERENCES charts(id),
    run_at      TEXT    NOT NULL,
    scores_json TEXT    NOT NULL
);
```

**Public API**:
```python
def init_db(path=_SENTINEL) -> None
def save_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha,
               chart_json, scores_json=None, name=None, path=_SENTINEL) -> int
def get_chart(chart_id: int, path=_SENTINEL) -> dict | None
def list_charts(limit: int = 50, path=_SENTINEL) -> list[dict]
```

**`_SENTINEL` pattern** (testability): functions default to the module-level `DB_PATH` variable. Tests monkey-patch `src.db.DB_PATH` before import; the sentinel allows this to work correctly without capturing the default at definition time.

**WAL mode**: `PRAGMA journal_mode=WAL` set on every connection — safe for concurrent readers.

---

### 4.11 `src/api/main.py`

**Purpose**: FastAPI application with 5 endpoints.

**Lifespan**: Uses `asynccontextmanager` lifespan (not deprecated `@app.on_event`) — calls `init_db()` on startup.

**Endpoints**:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check; returns `{"status": "ok", "version": "0.1.0"}` |
| `POST` | `/charts` | Compute + store chart from birth data; returns `ChartOut` (201) |
| `GET` | `/charts` | List recent charts; returns `list[ChartSummary]` |
| `GET` | `/charts/{chart_id}` | Retrieve stored chart; returns `ChartOut` (404 if missing) |
| `GET` | `/charts/{chart_id}/scores` | Recompute full 22-rule scores; returns `ChartScoresOut` |

**Note on `/charts/{id}/scores`**: Scores are always recomputed from stored birth data (not cached). This ensures scores reflect the latest rule logic after any scoring engine updates.

---

### 4.12 `src/api/models.py`

**Purpose**: Pydantic v2 request/response models with field-level validation.

```python
class BirthDataRequest(BaseModel):
    year:      int    # 1800–2100
    month:     int    # 1–12
    day:       int    # 1–31
    hour:      float  # 0.0–23.99 (0.0 = midnight)
    lat:       float  # -90.0–90.0 (N positive)
    lon:       float  # -180.0–180.0 (E positive)
    tz_offset: float  # default 5.5 (IST)
    ayanamsha: str    # "lahiri"/"raman"/"krishnamurti"; validated
    name:      str | None  # optional label

class ChartOut(BaseModel):
    id: int
    lagna_sign: str
    lagna_sign_index: int
    lagna_degree: float
    ayanamsha_name: str
    ayanamsha_value: float
    jd_ut: float
    planets: dict[str, PlanetOut]

class ChartScoresOut(BaseModel):
    chart_id: int
    lagna_sign: str
    houses: dict[int, HouseScoreOut]

class HouseScoreOut(BaseModel):
    house: int
    domain: str
    bhavesh: str
    bhavesh_house: int
    final_score: float
    raw_score: float
    rating: str
    rules: list[RuleOut]
```

---

## 5. API Reference

**Base URL** (local): `http://localhost:8000`

### POST /charts
Create a chart from birth data.

**Request body** (`application/json`):
```json
{
  "year": 1947, "month": 8, "day": 15,
  "hour": 0.0,
  "lat": 28.6139, "lon": 77.2090,
  "tz_offset": 5.5,
  "ayanamsha": "lahiri",
  "name": "India Independence"
}
```

**Response** (201):
```json
{
  "id": 1,
  "lagna_sign": "Taurus",
  "lagna_sign_index": 1,
  "lagna_degree": 7.7286,
  "ayanamsha_name": "lahiri",
  "ayanamsha_value": 23.1489,
  "jd_ut": 2432412.2708,
  "planets": {
    "Sun":  {"name": "Sun",  "sign": "Cancer", "sign_index": 3, "degree_in_sign": 27.989, "longitude": 117.989, "is_retrograde": false, "speed": 0.953},
    "Moon": {"name": "Moon", "sign": "Cancer", "sign_index": 3, "degree_in_sign": 3.983,  "longitude": 93.983,  "is_retrograde": false, "speed": 13.1},
    ...
  }
}
```

### GET /charts/{id}/scores

**Response** (200):
```json
{
  "chart_id": 1,
  "lagna_sign": "Taurus",
  "houses": {
    "1": {
      "house": 1, "domain": "Self & Vitality",
      "bhavesh": "Venus", "bhavesh_house": 3,
      "final_score": 2.5, "raw_score": 2.5, "rating": "Moderate",
      "rules": [
        {"rule": "R01", "description": "Gentle sign in house", "score": 0.0, "is_wc": false},
        {"rule": "R04", "description": "Bhavesh in Kendra/Trikon", "score": 0.0, "is_wc": false},
        ...
      ]
    },
    "2": {...},
    ...
  }
}
```

---

## 6. Scoring Engine Deep Dive

### How Bhavesh (House Lord) is Determined

For a Taurus Lagna chart (H1 = Taurus):
- H1 lord (Bhavesh) = Venus (rules Taurus)
- H2 = Gemini → Mercury
- H3 = Cancer → Moon
- H4 = Leo → Sun
- H5 = Virgo → Mercury
- H6 = Libra → Venus
- H7 = Scorpio → Mars
- H8 = Sagittarius → Jupiter
- H9 = Capricorn → Saturn
- H10 = Aquarius → Saturn
- H11 = Pisces → Jupiter
- H12 = Aries → Mars

### Yogakaraka Logic

A Yogakaraka is a planet that simultaneously rules a Kendra (H1/H4/H7/H10) and a Trikona (H1/H5/H9). For Taurus Lagna:
- Saturn rules H9 (Capricorn, trikona) and H10 (Aquarius, kendra) → **Yogakaraka**
- When Saturn is the bhavesh with a benefic (R06) or is itself benefic (R02), weight is 1.5× instead of 1.0×

### WC Rule Halving

R03, R05, R07, R14 are "Worth Considering" — they are real influences but weaker than direct placements. In aggregation:
```python
contribution = score * (0.5 if rule.is_wc else 1.0)
```
This matches the Excel SCORE_H* sheets where WC columns are summed at half weight.

### Kartari Yoga

Shubh Kartari (R08): Venus and Jupiter flanking the lagna sign (Taurus), with one in Aries and one in Gemini.
Paap Kartari (R12): Rahu and Mars flanking the lagna sign.

---

## 7. Known Bugs & Status

From `LagnaMaster_Audit_v5_PVRNR.docx` (v5 Excel audit):

| ID | Severity | Module | Bug | Status |
|----|----------|--------|-----|--------|
| P-1 | Critical | ephemeris.py | `hour=0` treated as falsy → midnight birth fails | ✅ Fixed |
| P-4 | Critical | ephemeris.py | Unknown ayanamsha silently uses default | ✅ Fixed |
| N-1 | Critical | narayana_dasa.py | Taurus period = 4yr (should be 7yr) | ✅ Fixed |
| S-2 | High | shadbala.py | Chesta Bala cell J14 = hardcoded 3851 | ✅ Fixed |
| E-1 | Critical | ephemeris.py | JDN Gregorian +0.5 day correction missing | 🔲 Session 7 |
| A-2 | High | retrograde.py | Mercury direction uses wrong row reference | 🔲 Session 7 |

**Note**: E-1 and A-2 are deferred to the accuracy iteration phase (Sessions 7–10). The pilot ships with bugs preserved as per the pilot-first strategy.

---

## 8. Test Suite

**70 tests, all passing** (as of Session 3):

```
tests/test_ephemeris.py       14 tests
tests/test_calculations.py    36 tests
tests/test_scoring.py         20 tests
```

**Run**:
```bash
cd /path/to/LagnaMaster
PYTHONPATH=. .venv/bin/pytest tests/ -v
```

**Key test patterns**:

1. **1947 fixture validation**: All ephemeris and scoring tests use `INDIA_1947` as the primary input. Any regression in position accuracy breaks these tests immediately.

2. **API test DB isolation** (`test_scoring.py::TestAPI`):
   ```python
   @pytest.fixture(scope="class")
   def client(self, tmp_path_factory):
       import src.db as db
       db.DB_PATH = tmp_path_factory.mktemp("data") / "test.db"
       from fastapi.testclient import TestClient
       from src.api.main import app
       db.init_db()   # init AFTER setting DB_PATH
       return TestClient(app)
   ```

3. **Aspect engine tests**: `test_planet_aspects_engine`, `test_mars_special_aspects`, `test_saturn_special_aspects` verify Graha Drishti offsets directly against `_planet_aspects_house()`.

4. **Score validation**: H2 and H7 expected negative for 1947 chart (matches Excel OUTPUT_LifeDomains).

---

## 9. Development Setup

```bash
# Clone
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install pyswisseph fastapi[standard] httpx pytest pydantic

# Run tests
PYTHONPATH=. pytest tests/ -v

# Start API server
PYTHONPATH=. uvicorn src.api.main:app --reload

# API docs (Swagger UI)
open http://localhost:8000/docs
```

**Optional: Swiss Ephemeris data files** (higher accuracy):
Place DE441 `.se1` files in `ephe/` directory. Without them, Moshier ephemeris is used (~1 arcsecond accuracy — sufficient for the pilot).

**Environment**: Python 3.12+. No database setup required — SQLite file created automatically in `data/charts.db`.
