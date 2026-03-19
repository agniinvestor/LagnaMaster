---

### 4.20 `src/calculations/pushkara_navamsha.py` (Session 11)

**Purpose**: Identify the 24 Pushkara Navamsha zones (2 per sign × 12 signs, each 3°20' wide) where a planet gains auspicious "nourishing" strength per Uttara Kalamrita / BPHS.

**Zone table** (start degree within sign; each spans 3°20' = 3.333°):

| Sign | Zone 1 | Zone 2 |
|------|--------|--------|
| Aries | 18°20' | 25°00' |
| Taurus | 3°20' | 28°20' |
| Gemini | 13°20' | 25°00' |
| Cancer | 1°40' | 25°00' |
| Leo | 11°40' | 19°10' |
| Virgo | 23°20' | 28°20' |
| Libra | 0°00' | 23°20' |
| Scorpio | 19°10' | 28°20' |
| Sagittarius | 5°00' | 23°20' |
| Capricorn | 10°00' | 28°20' |
| Aquarius | 6°40' | 25°00' |
| Pisces | 13°20' | 25°00' |

**Boundary**: inclusive start, exclusive end — `[start, start + 3.333°)`.

**Public API**:

```python
def is_pushkara_navamsha(sign_index: int, degree_in_sign: float) -> bool

def pushkara_navamsha_planets(chart: BirthChart) -> list[str]
# Returns planet names whose natal position is in a PN zone

def pushkara_navamsha_zones(sign_index: int) -> list[tuple[float, float]]
# Returns [(start1, end1), (start2, end2)] for the sign

def pushkara_strength_label(sign_index: int, degree_in_sign: float) -> str
# "Pushkara Navamsha" if in zone, else ""
```

**Scoring hook (R21 in scoring.py)**: R21 was a 0.0 stub; now calls `is_pushkara_navamsha` on the bhavesh planet → `+0.5` when triggered. No WC flag (direct strength). Apply patch from `docs/session11_scoring_r21_patch.py`.

**1947 India chart**:
- Sun at Cancer 27.989°: zone 2 = [25°, 28.333°) → **Pushkara** → H4 bhavesh gains +0.5
- Moon at Cancer 3.983°: zone 1 = [1°40', 5°) → **Pushkara** → H3 bhavesh gains +0.5

---

### 4.21 `src/montecarlo.py` (Session 11)

**Purpose**: Monte Carlo birth time sensitivity analysis. Samples the birth time uniformly over a ±N-minute window, computes full chart + 22-rule scores for each sample in parallel, returns a `SensitivityReport`.

**Motivation**: Hospital records often round to 5–15 minutes. A ±30-minute window covers most real-world uncertainty. Houses with std > 0.5 across samples are "sensitive" — scores should be interpreted cautiously.

**Performance target**: 100 samples < 8 seconds on 4 CPU cores.

**Data classes**:

```python
@dataclass
class HouseSensitivity:
    house: int
    mean_score: float; std_score: float
    min_score: float; max_score: float
    score_range: float      # max − min
    rating_mode: str        # most common rating across samples
    stable: bool            # True if std_score < 0.5

@dataclass
class SensitivityReport:
    n_samples: int
    birth_time_window_minutes: int
    lagna_stability: float       # fraction with same lagna as original
    dominant_lagna: str
    dasha_stability: float       # fraction with same current MD; 1.0 if no birth_date
    dominant_md_lord: str        # "N/A" if no birth_date
    houses: dict[int, HouseSensitivity]
```

**Public API**:

```python
def compute_sensitivity(
    year, month, day, hour,
    lat, lon, tz_offset=5.5, ayanamsha="lahiri", ephe_path=None,
    n_samples=100, window_minutes=30,
    seed=None, birth_date=None, max_workers=4,
) -> SensitivityReport
```

**Key implementation details**:
- `_worker()` is module-level (not a closure) — required for `ProcessPoolExecutor` pickling on all platforms (Windows/macOS/Linux)
- Birth hours clamped to `[0.0, 23.9999]` — handles midnight births safely
- `dasha_stability` defaults to 1.0 when `birth_date` is not supplied
- `stable` flag threshold: `std_score < 0.5`

**Streamlit integration** (8th tab — "Sensitivity"): see `docs/session11_ui_sensitivity.py` for exact patch. Controls: Samples slider (10–200), Window slider (±5–60 min), Seed number input. Outputs: lagna/dasha stability metrics, per-house bar chart and detail table, Pushkara Navamsha planet list.

---

### 4.22 `src/calculations/kundali_milan.py` (Session 12)

**Purpose**: Ashtakoot (8-quality) compatibility scoring per BPHS / North Indian matchmaking tradition. Compares two birth charts and returns a 0–36 score breakdown plus Mangal Dosha flags.

**Score interpretation**:

| Score | Grade | Meaning |
|-------|-------|---------|
| ≥ 28 | Excellent | Highly compatible |
| 18–27 | Good | Acceptable; 18 is conventional minimum |
| < 18 | Weak | Needs careful consideration |

**8 Kootas** (total max = 36):

| Koota | Max | Method |
|-------|-----|--------|
| Varna | 1 | Moon sign → Varna rank; male rank ≤ female rank = 1 pt |
| Vashya | 2 | Zodiac group dominance (quadruped/human/jalachara/vanachara/keeṭa) |
| Tara | 3 | Nakshatra count mod 9 in both directions → tara auspiciousness; averaged |
| Yoni | 4 | 14 animal types per nakshatra; same=4, 7 enemy pairs=0, neutral=2 |
| Graha Maitri | 5 | Moon-sign lords' Naisargika friendship (5 tiers: 5/5/4/3/1/0) |
| Gana | 6 | Deva/Manava/Rakshasa temperament; 3×3 compatibility matrix |
| Bhakut | 7 | Sign distance mod 12; 6/8 and 5/9 axes = 0 (Bhakut Dosha) |
| Nadi | 8 | Aadi/Madhya/Antya constitution; same = 0 (Nadi Dosha), different = 8 |

**Nakshatra data**: All 27 assignments for Gana, Nadi, Yoni are hardcoded per BPHS standard. Contested nakshatras: Ardra = Manava (not Rakshasa), Vishakha = Rakshasa (not Manava).

**Mangal Dosha detection** (`has_mangal_dosha(chart) -> bool`):
- Mars in H1, H2, H4, H7, H8, or H12 counted from **Lagna**, **Moon sign**, or **Venus sign** (any one reference triggers)
- Cancellation: both charts have dosha → `dosha_cancelled = True`; dosha omitted from `critical_doshas`

**Data classes**:

```python
@dataclass
class KootaScore:
    name: str; max_score: float; score: float
    male_value: str; female_value: str; note: str
    percentage: float   # property: score/max * 100
    is_dosha: bool      # property: score==0 and max>0

@dataclass
class KundaliMilanResult:
    total_score: float; max_score: float   # max = 36
    percentage: float; grade: str
    kootas: dict[str, KootaScore]
    mangal_dosha_male: bool; mangal_dosha_female: bool; dosha_cancelled: bool
    nadi_dosha: bool; bhakut_dosha: bool
    critical_doshas: list[str]
```

**Public API**:

```python
def compute_kundali_milan(chart_male, chart_female) -> KundaliMilanResult
def has_mangal_dosha(chart) -> bool
```

**Design note**: The Naisargika friendship matrix is reproduced inside `kundali_milan.py` (not imported from `friendship.py`) so the module is self-contained and importable without the full `src/calculations/` stack.

**1947 India chart self-compatibility**:
- Nadi Dosha present (same Nadi for Moon in Pushya)
- Gana = 6/6 (same Gana)
- Mangal Dosha: Mars in Gemini (si=2), Lagna Taurus (si=1) → H2 → triggered

---

### 4.23 `src/ui/kundali_page.py` (Session 12)

**Purpose**: Self-contained Streamlit page for Kundali Milan compatibility analysis. Can run standalone or be embedded as a tab in `app.py`.

**Run standalone**:

```bash
PYTHONPATH=. streamlit run src/ui/kundali_page.py
```

**Embed in app.py** (see `docs/session12_app_patch.py`):

```python
from src.ui.kundali_page import render_kundali_tab
with tab9:
    render_kundali_tab()
```

**UI elements**:
- Dual birth-data input form (Chart A / Chart B) with date, hour/minute sliders, lat/lon, tz, ayanamsha
- Demo button (pre-fills illustrative birth dates)
- SVG arc gauge (0–36) — green ≥28, amber ≥18, red <18
- `st.metric` cards: Total Gunas, lagna stability, Mangal Dosha flags
- Critical dosha banner (red `st.error`) or clean `st.success`
- Koota detail dataframe with ASCII progress bars
- `st.bar_chart` koota breakdown
- Side-by-side South Indian SVG charts in expander
- Interpretation guide in expander

---

## 8. Test Suite — updated Session 12

**277 tests, all passing** (as of Session 12):

```
tests/test_ephemeris.py        14 tests
tests/test_calculations.py     36 tests
tests/test_scoring.py          20 tests
tests/test_integration.py      17 tests
tests/test_vimshottari.py      20 tests
tests/test_yogas.py            14 tests
tests/test_ashtakavarga.py     26 tests
tests/test_gochara.py          29 tests
tests/test_panchanga.py        40 tests
tests/test_pushkara.py         10 tests  ← Session 11
tests/test_montecarlo.py       20 tests  ← Session 11
tests/test_kundali_milan.py    25 tests  ← Session 12
                              ─────────
                              271 total  + existing scoring R21 tests
```

**Kundali Milan test patterns** (`test_kundali_milan.py`):
- `TestResultStructure` (8 tests): type, 8 kootas, correct max_scores, scores in range, total = koota sum, total bounded 36, percentage consistency, grade validity
- `TestGrades` (3 tests): Excellent/Good/Weak thresholds
- `TestNadiDosha` (3 tests): same-Nadi gives 0, different=8, nadi_dosha flag + critical_doshas
- `TestBhakutDosha` (4 tests): 6/8 axis=0, 5/9 axis=0, 1/7=7, bhakut_dosha flag
- `TestMangalDosha` (4 tests): H1 from lagna triggers, H7 triggers, H3 no-trigger, mutual cancellation
- `TestSelfCompatibility` (5 tests): runs, Nadi Dosha, Gana=6, determinism, Mangal Dosha 1947
- `TestKootaBounds` (3 tests): parametrized — Tara in [0,3], Yoni in {0,2,4}, Nadi only {0,8}
