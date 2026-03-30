# ARCHITECTURE.md — LagnaMaster Technical Architecture
> **Update this file when modules are added, wired, or refactored.**
> Ground truth for function signatures, data classes, and implementation details.
> Source: DOCS.md in repo root (1177 lines, 44.3KB) — the canonical API reference.

---

## Stack

```
Language:      Python 3.14
Ephemeris:     pyswisseph + JPL DE431 real files (sepl_18.se1 + semo_18.se1)
               Historical (<1800): seplm_18.se1 + semom_18.se1
               Moshier fallback RETIRED as of S188
API:           FastAPI (sync) + Pydantic v2
UI:            Streamlit (analyst) → Next.js (production)
DB:            SQLite default / PostgreSQL via PG_DSN (db_pg routing, S188)
Deploy:        Docker Compose → Kubernetes
Cache:         None → Redis 3-tier (planned S211)
```

**Streamlit Cloud (packages.txt / requirements.txt):**
- `packages.txt`: `gcc g++ python3-dev` — required for pyswisseph compilation
- `requirements.txt`: `fastapi` (NOT `fastapi[standard]`) — avoids Rust dependency from `email-validator` that `fastapi[standard]` pulls in
- `.streamlit/config.toml`: `headless=true`, `enableCORS=false`, serif font, indigo theme

**Swiss Ephemeris flags:**
```python
# In swe.calc_ut() calls — sidereal mode set via swe.set_sid_mode() separately:
flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
# After S188 real files installed, return flags verified:
#   flags=258 = FLG_SWIEPH (2) + FLG_SPEED (256)
#   Confirms JPL DE431 files active — Moshier would return FLG_MOSEPH (4) instead
```

---

## Core Data Flow

```
Birth Data (date, time, lat/lon, tz_offset, ayanamsha)
        ↓
src/ephemeris.py             pyswisseph wrapper → BirthChart
        ↓
src/calculations/            12 Jyotish modules
  dignity.py                 Dignity levels + combustion + Neecha Bhanga
  nakshatra.py               27 nakshatras, 4 padas, D9, Ganda Mool
  friendship.py              Naisargika + Tatkalik → Panchadha Maitri (5-fold)
  house_lord.py              Whole-sign house map, Kendra/Trikona/Dusthana helpers
  chara_karak.py             7 Jaimini Chara Karakas (AK → GK)
  narayana_dasa.py           Sign-based 81-year predictive cycle
  shadbala.py                6-component planetary strength in Virupas
  vimshottari_dasa.py        120-year nakshatra dasha (9 MDs × 9 ADs)
  yogas.py                   13 yoga types: PM/Raj/Dhana/Lunar/Solar/Special
  ashtakavarga.py            Parashari 8-source bindu system (7 planets + Sarva)
  gochara.py                 Transit analysis: GocharaReport, Sade Sati, AV bindus
  panchanga.py               5-limb almanac: Tithi/Vara/Nakshatra/Yoga/Karana + D9
        ↓
src/scoring.py               22 BPHS rules × 12 houses → score in [-10, +10]
src/multi_axis_scoring.py    Extended scoring — school gates, war loser penalty (S187)
src/scoring_v3.py            Dasha-sensitized multi-axis scores D1/D9/D10/CL/SL (S187)
        ↓
src/db_pg.py                 PostgreSQL routing + SQLite fallback (S188)
src/db.py                    SQLite persistence helpers
        ↓
src/api/main.py              FastAPI v3.0.0: 10 endpoints
src/api/models.py            Pydantic v2 models (SVGRequest/Out, GuidanceRequest/Out, etc.)
        ↓
src/ui/app.py                Streamlit 7-tab analyst UI
src/ui/chart_visual.py       South Indian SVG (D1 + D9 Navamsha)
```

---

## Key Tacit Knowledge (from DOCS.md)
> Before reading the module inventory, understand which convergence layer each module
> contributes to. A module is not complete when it passes tests — it is complete when
> it is correctly wired into its convergence layer and that layer's output is used
> by downstream modules. See `docs/PREDICTION_PIPELINE.md` for the full convergence model.

### Convergence Layer → Module Mapping

**Layer I — Classical Convergence** (what the classical tradition says about this chart)
```
multi_axis_scoring.py    — 23 rules × 5 axes (D1/Chandra/Surya/D9/D10)
rule_interaction.py      — 30 rule-pair modifiers
lpi.py                   — 7-layer weighted integration (D1×35% + ...)
varga_agreement.py       — ★★/★/○ cross-varga confirmation
kp_full.py               — KP sublord school contribution
jaimini_full.py          — Jaimini school contribution
scoring_v3.py            — multi-school concordance output
dominance_engine.py      — classical priority overrides
promise_engine.py L1     — D1 score threshold → promise_present
```

**Layer II — Structural Convergence** (is the promise activation-ready right now)
```
promise_engine.py L2+L3  — Capacity (dasha lord) + Delivery (AV transit)
dasha_scoring.py         — dasha-sensitized score adjustments
yoga_fructification.py   — PVRNR three conditions (strength, orb, dignity)
narayana_argala.py       — argala contribution to capacity
av_transit.py            — AV bindu delivery gate
confidence_model.py      — birth time sensitivity (precision of promise)
vimshottari_dasa.py      — timing cascade MD→AD→PD
narayana_dasa.py         — sign-based timing layer
stronger_of_two.py       — disambiguation of competing activations
```

**Layer III — Empirical Convergence** (do confirmed outcomes validate the model — Phase 3+)
```
feedback schema          — user_prior_prob_pre + signal isolation (S491)
Bayesian update pipeline — posterior weight updates (S746)
HDBSCAN clustering       — chart similarity + social proof (S731)
XGBoost + SHAP           — feature importance validation (S701)
```

**Supporting (contributes to multiple layers)**
```
ephemeris.py             — raw calculation substrate for all layers
shadbala.py / dig_bala.py — strength signal feeding into L1 weight functions
ashtakavarga.py          — AV bindus used in L1 (SAV rule) and L2 (delivery gate)
divisional_charts.py     — varga data feeding L1 concordance and L2 promise depth
confidence_model.py      — birth time sensitivity constrains confidence in all layers
```

### Critical Architectural Principle

A module that scores correctly in isolation but is not wired to its convergence layer
output produces no improvement to prediction quality. The four unresolved wiring gaps
(all closed as of S188) were architectural failures of this type — functionally correct
code producing zero downstream effect. When adding new modules, the first question is:
**which convergence layer does this belong to, and what is its output consumed by?**

---



### src/ephemeris.py

```python
def compute_chart(
    year, month, day,
    hour: float,            # 0.0 = midnight; P-1 fix: None treated as 0.0
    lat, lon,
    tz_offset: float = 5.5, # IST = +5.5
    ayanamsha: str = "lahiri",  # P-4 fix: unknown → raises ValueError immediately
    ephe_path=None,
) -> BirthChart

@dataclass
class PlanetPosition:
    name: str; longitude: float    # sidereal 0–360°
    sign: str; sign_index: int     # 0=Aries…11=Pisces
    degree_in_sign: float          # 0–30°
    is_retrograde: bool; speed: float  # deg/day; negative = retrograde

@dataclass
class BirthChart:
    jd_ut: float; ayanamsha_name: str; ayanamsha_value: float
    lagna: float; lagna_sign: str; lagna_sign_index: int; lagna_degree_in_sign: float
    planets: dict[str, PlanetPosition]  # Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu/Ketu
```

**Critical details:**
- **Ketu derived:** `Rahu.longitude + 180° mod 360` — not computed separately from ephemeris
- **Topocentric Moon (S161):** `swe.set_topo(lat, lon, 0)` + `SEFLG_TOPOCTR` flag for Moon only
- **Supported ayanamshas:** `"lahiri"`, `"raman"`, `"krishnamurti"`

---

### src/calculations/dignity.py

**DignityLevel enum — exact names (do not alias):**

| Enum | Score | Trigger |
|------|-------|---------|
| `EXALT` | +1.5 | Exaltation sign |
| `MOOLTRIKONA` | +1.0 | Moolatrikona portion of own sign |
| `OWN_SIGN` | +0.75 | Own sign (non-moolatrikona) |
| `FRIEND_SIGN` | +0.25 | Friendly sign |
| `NEUTRAL` | 0.0 | Neutral sign |
| `ENEMY_SIGN` | −0.25 | Enemy sign |
| `DEBIL` | −1.5 | Debilitation sign |

**Combustion (separate from DignityLevel):**
- **Cazimi** (within 1° of Sun): overrides combustion → `+0.5` override in scoring
- **Asta Vakri** (combust + retrograde): reduced negative (`−0.5` vs `−1.0`)
- **Retrograde orb:** `Rx_orb = direct_orb − 2°` (Saravali Ch.3)
- **Neecha Bhanga:** triggered when debilitation lord occupies a Kendra house

```python
def compute_dignity(planet: str, chart: BirthChart) -> DignityInfo
def compute_all_dignities(chart: BirthChart) -> dict[str, DignityInfo]
# DignityInfo: .dignity, .combust, .cazimi, .neecha_bhanga (all bools/enum)
```

---

### src/calculations/nakshatra.py

- **D9 formula:** `(nak_idx * 4 + (pada - 1)) % 12`
- **Ganda Mool:** `Ashwini, Ashlesha, Magha, Jyeshtha, Mula, Shatabhisha, Revati`

```python
def nakshatra_position(longitude: float) -> NakshatraPosition
# Returns: nakshatra_name, pada (1–4), lord, navamsha_sign, is_ganda_mool
```

---

### src/calculations/friendship.py

**Tatkalik rule:**
- Houses 2/3/4/10/11/12 from planet A → planet B is **Temporary Friend** of A
- Houses 1/5/6/7/8/9 from planet A → planet B is **Temporary Enemy** of A
- Relationship is symmetric (mutual)

**Critical:** 22 asymmetric pairs in Naisargika matrix (e.g., Sun friendly to Moon, Moon neutral to Sun).

---

### src/calculations/narayana_dasa.py

**Period table (total = 81 years):**

| Sign | Yrs | Sign | Yrs |
|------|-----|------|-----|
| Aries | 6 | Libra | 1 |
| **Taurus** | **7** | Scorpio | 11 |
| Gemini | 2 | Sagittarius | 5 |
| Cancer | 10 | Capricorn | 7 |
| Leo | 9 | Aquarius | 12 |
| Virgo | 8 | Pisces | 3 |

- Odd Lagna → forward; Even Lagna → backward
- **N-1 fix:** Taurus was 4yr in Excel source, corrected to 7yr

---

### src/calculations/shadbala.py

### src/calculations/kala_bala.py (NEW — S190)

All 8 Kala Bala temporal strength sub-components from BPHS Ch.27.
Convergence layer: **Layer I — classical strength signal**.

| Sub-component | Formula / Rule | Max Virupas |
|--------------|---------------|-------------|
| Nathonnathabala | Sun/Jup/Ven=day, Moon/Mars/Sat=night, Merc=always | 60V |
| Paksha Bala | min(diff,360-diff)/180*60; malefics inverse | 60V |
| Tribhaga Bala | Day: Merc/Sun/Sat; Night: Moon/Ven/Mars; Jup always | 60V |
| Abda Bala | Weekday lord of Mesha Sankranti | 15V |
| Masa Bala | Weekday lord of preceding new moon | 30V |
| Vara Bala | Weekday lord of birth | 45V |
| Hora Bala | Hora lord at birth (Chaldean sequence from day lord) | 60V |
| Ayana Bala | 30 + 30*cos(angle_from_preferred_peak) | 0–60V |

Public API: `compute_kala_bala(jd_ut, lat, lon_geo, planet_longitudes, birth_year) → KalaBalaResult`

**India 1947 verified:** Vara=Venus(45V), Hora=Jupiter(60V), Natho=Moon/Mars/Sat(60V)



| Component | Formula |
|-----------|---------|
| Uchcha Bala | `60 × (180 − dist_from_exalt) / 180` |
| Kendradi Bala | Kendra=60, Panapara=30, Apoklima=15 |
| Ojha-Yugma | Male in odd sign OR female in even = 30V |
| Dig Bala | `60 × (1 − dist_from_peak / 6)` |
| Paksha Bala | Lunar phase |
| Chesta Bala | `min(60, mean_motion / |speed| × 60)` ← **S-2 fix** |

**Dig Bala peaks:** Sun/Mars → H10; Moon/Venus → H4; Mercury/Jupiter → H1; Saturn → H7

---

### src/scoring.py — 22-Rule Engine

**22 Rules (WC = counted at 0.5× weight):**

| Rule | Weight | Description | WC? |
|------|--------|-------------|-----|
| R01 | +0.50 | Gentle sign in house | |
| R02 | +1.00 (+1.5 Yogakaraka) | Benefic in house | |
| R03 | +0.75 | Benefic aspects house | ✓ |
| R04 | +2.00 | Bhavesh in Kendra/Trikona | |
| R05 | +0.50 | Bhavesh with Kendra/Trikona lord | ✓ |
| R06 | +1.00 (+1.5 Yogakaraka) | Bhavesh with benefic | |
| R07 | +0.50 | Benefic aspects Bhavesh sign | ✓ |
| R08 | +0.75 | Bhavesh in Shubh Kartari | |
| R09 | −1.00 | Malefic in house | |
| R10 | −1.00 | Malefic aspects house | |
| R11 | −1.25 | Dusthana lord in house | |
| R12 | −0.75 | House in Paap Kartari | |
| R13 | −1.00 | Bhavesh with malefic | |
| R14 | −0.50 | Malefic aspects Bhavesh sign | ✓ |
| R15 | −2.00 | Bhavesh in Dusthana | |
| R16 | −1.00 | Bhavesh with Dusthana lord | |
| R17 | +0.50 | Sthir Karak in Kendra/Trikona | |
| R18 | −0.50 | Sthir Karak in Dusthana | |
| R19 | −1.00 (cazimi: +0.5; Rx+combust: −0.5) | Bhavesh combust | |
| R20 | +0.50 | Bhavesh in Dig Bala house | |
| R21 | 0.0 | Pushkara Navamsha (stub — deferred) | |
| R22 | Jup/Sat: +0.25; Merc/Ven/Mars: −0.50 | Bhavesh retrograde | |

**Formula:** `raw = Σ(rule.score × (0.5 if WC else 1.0))` → `final = clamp(raw, −10, +10)`

**Ratings:** ≥6=Excellent, ≥3=Strong, ≥0=Moderate, ≥−3=Weak, <−3=Very Weak

**Graha Drishti:** All planets: 7th. Mars: +4th/8th. Jupiter: +5th/9th. Saturn: +3rd/10th.

---

### src/calculations/vimshottari_dasa.py

**Period table:** Ketu=7, Venus=20, Sun=6, Moon=10, Mars=7, Rahu=18, Jupiter=16, Saturn=19, Mercury=17 → **Total 120**

**Sequence:** Ketu → Venus → Sun → Moon → Mars → Rahu → Jupiter → Saturn → Mercury

**AntarDasha duration:** `maha_years × VIMSHOTTARI_YEARS[antar_lord] / 120`

**1947 India:** Moon ~93.98° → Pushya nakshatra (index 7) → Saturn birth dasha (19yr).

---

### src/calculations/ashtakavarga.py

**Fixed totals (chart-independent — use to verify AV implementation):**

| Planet | Total | Planet | Total |
|--------|-------|--------|-------|
| Sun | **50** | Mercury | **55** |
| Moon | **48** | Jupiter | **57** |
| Mars | **42** | Venus | **52** |
| Saturn | **40** | **Sarva** | **344** |

`_PLANETS = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]` — Rahu/Ketu excluded.
Lagna is the 8th contributor (`chart.lagna_sign_index`).

```python
def compute_ashtakavarga(chart: BirthChart) -> AshtakavargaChart
# AshtakavargaChart.sarva.bindus: list[int]  ← sum must = 344
# .strength(sign_index): "Strong" (≥5) / "Average" (3-4) / "Weak" (≤2)
```

---

### src/db.py

**`_SENTINEL` pattern (testability):** Functions default to the module-level `DB_PATH` variable. Tests monkey-patch `src.db.DB_PATH` before import. The sentinel prevents capturing the default at definition time, making the monkey-patch work correctly.

**WAL mode:** `PRAGMA journal_mode=WAL` set on every connection — safe for concurrent readers.

---

### src/api/main.py — FastAPI v3.0.0 (S188)

**Lifespan:** `asynccontextmanager` (NOT deprecated `@app.on_event`) — calls `init_db()` on startup.

**Routing:** `src.db_pg` — Postgres when `PG_DSN` is set; **automatic SQLite fallback** when not.

**`/charts/{id}/scores` note:** Scores **always recomputed** from stored birth data (not cached). Ensures scores reflect latest rule logic after any engine update.

**All 10 endpoints:**

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | `{"status":"ok","version":"3.0.0"}` |
| `POST` | `/charts` | Compute + store chart (201) |
| `GET` | `/charts` | List recent charts |
| `GET` | `/charts/{id}` | Retrieve chart (404 if missing) |
| `GET` | `/charts/{id}/scores` | 22-rule house scores (always recomputed) |
| `POST` | `/charts/{id}/svg` | North/South Indian SVG |
| `POST` | `/charts/{id}/pdf` | 2-page PDF (weasyprint/HTML fallback) |
| `POST` | `/charts/{id}/guidance` | Consumer L1/L2/L3 guidance |
| `GET` | `/charts/{id}/confidence` | Lagna/nakshatra boundary warnings |
| `GET` | `/charts/{id}/scores/v3` | Dasha-sensitized multi-axis scores |

---

### src/ui/chart_visual.py — South Indian SVG

**Layout:** CELL=130px, total=520×520px. Fixed sign positions (4×4 grid):

```python
# sign_index → grid (row, col):
{11:(0,0), 0:(0,1), 1:(0,2), 2:(0,3),
 10:(1,0),                   3:(1,3),
  9:(2,0),                   4:(2,3),
  8:(3,0), 7:(3,1), 6:(3,2), 5:(3,3)}
# Centre cells (1,1)–(2,2): diagonal cross + chart label
```

- Lagna: `fill="#EDE7FF"`, border `#4B0082`
- Benefics (Jupiter, Venus, Moon, Mercury): `color="#1a7a1a"` (green)
- Malefics (Sun, Mars, Saturn, Rahu, Ketu): `color="#8b0000"` (red)

```python
def south_indian_svg(chart: BirthChart, name: str = "") -> str
def navamsha_svg(d9_data: dict[str, int], lagna_d9_si: int, label="D9 Navamsha") -> str
```

---

### src/ui/app.py

### src/ui/confidence_tab.py (NEW — S190)

Streamlit Birth Time Sensitivity tab. Closes **UI-1** (open since S188).
Surfaces the existing `GET /charts/{id}/confidence` endpoint.

Wire into app.py:
```python
from src.ui.confidence_tab import render_confidence_tab
with tab_confidence:
    render_confidence_tab(chart_id=st.session_state.get("chart_id"))
```

 — Critical Import Names

```python
from src.calculations.nakshatra import nakshatra_position
from src.calculations.dignity import compute_all_dignities, DignityLevel
from src.calculations.yogas import detect_yogas
from src.calculations.vimshottari_dasa import compute_vimshottari_dasa, current_dasha
from src.calculations.ashtakavarga import compute_ashtakavarga, _PLANETS as _AV_PLANETS
from src.calculations.shadbala import compute_shadbala
from src.calculations.gochara import compute_gochara
from src.calculations.panchanga import compute_panchanga
from src.ui.chart_visual import south_indian_svg, navamsha_svg
```

**Session state keys:** `chart`, `scores`, `chart_id`, `birth_date`, `show_history`

---

### src/multi_axis_scoring.py + src/scoring_v3.py (S187)

```python
# War loser check — Invariant #35:
bh_war_loser = bhavesh in getattr(chart, 'planetary_war_losers', set())
# If True → −1.5 penalty to house score (permanent, Saravali Ch.4 v.18-22)

# strict_school — Invariant #36:
def score_axis(chart, axis, strict_school=False) -> AxisScore
def score_all_axes(chart, strict_school=False) -> AllAxesScore
# When True: school_score_adjustment() deducts Jaimini contributions
# NOTE: R17/R18 currently score 0.0 — so strict_school=True has no numeric effect yet

# Dasha scoring:
def score_chart_v3(chart, on_date=None) -> ChartV3Out
# When on_date supplied: score_chart_with_dasha() called after score_all_axes()
# MUTATES axes.d1.scores in-place (does not create a new object)
```
## S194 — New module
- `src/calculations/conditional_weights.py` — `WeightContext` + `W()` conditional weight function (G06-aware, Phase 2 engine rebuild ready)

---

## Corpus Module Inventory (src/corpus/)

### Infrastructure
| Module | Session | Purpose |
|--------|---------|---------|
| `registry.py` | S202 | `CorpusRegistry` — add/query/count/all operations |
| `rule_record.py` | S202/S263 | `RuleRecord` dataclass — 26 fields (12 Phase 1B mandatory) |
| `combined_corpus.py` | S202+ | `build_corpus()` → aggregated `CorpusRegistry` singleton |

### Phase 1A — Representative Rules
| Module | Session | Rules | Source Text |
|--------|---------|-------|-------------|
| `existing_rules.py` | S202 | 23 | Engine rules R01-R23 |
| `bphs_extended.py` | S206 | ~50 | BPHS extended |
| `phaladeepika_rules.py` | S206 | ~40 | Phaladeepika |
| `brihat_jataka_rules.py` | S206 | ~40 | Brihat Jataka |
| `uttara_kalamrita_rules.py` | S207 | ~40 | Uttara Kalamrita |
| `jataka_parijata_rules.py` | S207 | ~40 | Jataka Parijata |
| *...25+ additional Phase 1A modules...* | S216-S262 | ~2,600 | BPHS lords/yogas/dignities, KP, Jaimini, Lal Kitab, etc. |

### Phase 1B — Sutra-Level Encoding

#### Laghu Parashari (S264-S266, 306 rules)
| Module | Rules | Content |
|--------|-------|---------|
| `laghu_parashari_functional.py` | 108 | LPF001-108: 9×12 functional nature table |
| `laghu_parashari_bcd.py` | 81 | LPY/LPK/LPD: yogakaraka, kendradhipati, dasha rules |
| `laghu_parashari_ef.py` | ~117 | LPA/LPM: antardasha, maraka rules |

#### Bhavartha Ratnakara (S267-S272, 780 rules, COMPLETE)
| Module | Rules | Content |
|--------|-------|---------|
| `bhavartha_ratnakara_1.py` | 130 | BVR001-130: Aries + Taurus |
| `bhavartha_ratnakara_2.py` | 130 | BVR131-260: Gemini + Cancer |
| `bhavartha_ratnakara_3.py` | 130 | BVR261-390: Leo + Virgo |
| `bhavartha_ratnakara_4.py` | 130 | BVR391-520: Libra + Scorpio |
| `bhavartha_ratnakara_5.py` | 130 | BVR521-650: Sagittarius + Capricorn |
| `bhavartha_ratnakara_6.py` | 130 | BVR651-780: Aquarius + Pisces |

#### Saravali (S273-S305, 2,898 rules, COMPLETE — all 68 chapters)

**Block A — Conjunctions (1,040 rules)**
| Module | Rules | Content |
|--------|-------|---------|
| `saravali_conjunctions_1.py` | 130 | SAV001-130: Sun-Moon/Mars/Mercury |
| `saravali_conjunctions_2.py` | 130 | SAV131-260: Sun-Jupiter/Venus/Saturn |
| `saravali_conjunctions_3.py` | 130 | SAV261-390: Moon-Mars/Mercury/Jupiter |
| `saravali_conjunctions_4.py` | 130 | SAV391-520: Moon-Venus/Saturn, Mars-Mercury |
| `saravali_conjunctions_5.py` | 130 | SAV521-650: Mars-Jupiter/Venus/Saturn |
| `saravali_conjunctions_6.py` | 130 | SAV651-780: Mercury-Jupiter/Venus/Saturn |
| `saravali_conjunctions_7.py` | 130 | SAV781-910: Jupiter-Venus/Saturn, Venus-Saturn |
| `saravali_conjunctions_8.py` | 130 | SAV911-1040: Three+ planet conjunctions |

**Block B — Planet-in-Sign (1,092 rules)**
| Module | Rules | Content |
|--------|-------|---------|
| `saravali_signs_1.py` | 130 | SAV1041-1170: Sun in 12 signs (Ch.25) |
| `saravali_signs_2.py` | 130 | SAV1171-1300: Moon in 12 signs (Ch.26) |
| `saravali_signs_3.py` | 130 | SAV1301-1430: Mars in 12 signs (Ch.27) |
| `saravali_signs_4.py` | 130 | SAV1431-1560: Mercury in 12 signs (Ch.28) |
| `saravali_signs_5.py` | 142 | SAV1561-1702: Jupiter in 12 signs (Ch.29) |
| `saravali_signs_6.py` | 159 | SAV1703-1861: Venus in 12 signs (Ch.30) |
| `saravali_signs_7.py` | 141 | SAV1862-2002: Saturn in 12 signs (Ch.31) |
| `saravali_signs_8.py` | 130 | SAV2003-2132: Rahu/Ketu in 12 signs (Ch.32-33) |

**Block C — Planet-in-House (496 rules)**
| Module | Rules | Content |
|--------|-------|---------|
| `saravali_houses_1.py` | 68 | Sun in 12 houses (Ch.34) |
| `saravali_houses_2.py` | 60 | Moon in 12 houses (Ch.35) |
| `saravali_houses_3.py` | 57 | Mars in 12 houses (Ch.36) |
| `saravali_houses_4.py` | 57 | Mercury in 12 houses (Ch.37) |
| `saravali_houses_5.py` | 60 | Jupiter in 12 houses (Ch.38) |
| `saravali_houses_6.py` | 56 | Venus in 12 houses (Ch.39) |
| `saravali_houses_7.py` | 57 | Saturn in 12 houses (Ch.40) |
| `saravali_houses_8.py` | 81 | Rahu/Ketu in 12 houses (Ch.41-42) |

**Block D — Special Topics (270 rules)**
| Module | Rules | Content |
|--------|-------|---------|
| `saravali_special_1.py` | 45 | Planet natures, signs, houses (Ch.1-5) |
| `saravali_special_2.py` | 32 | Longevity, Arishta, Ayurdaya (Ch.6-8) |
| `saravali_special_3.py` | 30 | Raja Yogas, Ava Yogas (Ch.9-10) |
| `saravali_special_4.py` | 38 | Nabhasa/Solar/Lunar/Chandra Yogas (Ch.11-14) |
| `saravali_special_5.py` | 30 | Bhava effects detailed (Ch.43-48) |
| `saravali_special_6.py` | 28 | Female horoscopy, Marriage, Progeny (Ch.49-53) |
| `saravali_special_7.py` | 23 | Dasha results, AV, Transits (Ch.54-60) |
| `saravali_special_8.py` | 20 | Death, Lost horoscopy, Drekkana (Ch.61-65) |
| `saravali_special_9.py` | 24 | Nimitta, Planetary war, Summary (Ch.66-68) |

### Corpus Totals (as of S305)
| Source | Rules | Status |
|--------|-------|--------|
| Phase 1A (representative) | ~2,600 | Complete |
| Laghu Parashari | 306 | Complete |
| Bhavartha Ratnakara | 780 | Complete (12/12 lagnas) |
| Saravali | 2,898 | Complete (68/68 chapters) |
| **TOTAL** | **~6,585** | — |
