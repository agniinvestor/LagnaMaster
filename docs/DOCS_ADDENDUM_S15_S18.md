# LagnaMaster — DOCS Addendum: Sessions 15–18

> Last updated: 2026-03-19

Append the sections below to DOCS.md after section 4.19 (panchanga.py).

---

## 4.20 `src/calculations/varga.py` — Varga Divisional Charts

Computes 8 divisional charts (D2/D3/D4/D7/D9/D10/D12/D60) from any BirthChart.

**Data classes**:
```python
@dataclass
class VargaPlanet:
    planet: str; d1_longitude: float; d1_sign: str; d1_sign_index: int
    varga_sign_index: int; varga_sign: str; is_retrograde: bool; speed: float

@dataclass
class VargaTable:
    division: str; label: str
    lagna_sign_index: int; lagna_sign: str
    varga_lagna_sign_index: int; varga_lagna_sign: str
    planets: dict[str, VargaPlanet]
    def planet_sign(planet) -> str
    def planet_sign_index(planet) -> int
    def planets_in_sign(sign_index) -> list[str]

@dataclass
class VargaChart:
    tables: dict[str, VargaTable]
    def d2/d3/d4/d7/d9/d10/d12/d60() -> VargaTable
    def for_division(division) -> VargaTable
```

**Public API**: `compute_varga(chart: BirthChart) -> VargaChart`

**Cross-validation**: D9 output must match `panchanga.compute_navamsha_chart()`.

---

## 4.21 `src/calculations/sapta_varga.py` — Vimshopak Bala

20-point weighted dignity score across 7 vargas. Weights: D1=3, D2=2, D3=2, D7=1, D9=5, D10=3, D12=4.

**Dignity fractions**: Exaltation=1.0, Moolatrikona=0.75, OwnSign=0.5, Friend=0.375, Neutral=0.25, Enemy=0.125, Debilitation=0.0

**Data classes**:
```python
@dataclass
class VargaDignity:
    division: str; weight: float; sign_index: int; sign_name: str
    dignity: str; points: float

@dataclass
class PlanetVimshopak:
    planet: str; varga_dignities: dict[str, VargaDignity]
    total: float; grade: str
    def dignity_in(division) -> str
    def sign_in(division) -> str

@dataclass
class VimshopakResult:
    planets: dict[str, PlanetVimshopak]   # 9 planets + "Lagna"
    def for_planet(planet) -> PlanetVimshopak
    def ranking() -> list[tuple[str, float]]
```

**Public API**: `compute_vimshopak(chart: BirthChart) -> VimshopakResult`

**Grade thresholds**: Excellent≥15, Good≥10, Average≥6, Weak≥3, Very Weak<3.
Rahu/Ketu always Neutral (no Parashari exalt/debil).

---

## 4.22 `src/calculations/kp.py` — KP Sub-lord System

**Public API**:
```python
def kp_sub_at(longitude: float) -> KPPosition
def compute_kp(chart: BirthChart) -> KPChart
```

**Data classes**:
```python
@dataclass
class KPPosition:
    longitude: float; nakshatra: str; nakshatra_index: int
    star_lord: str; sub_lord: str; sub_sub_lord: str
    sub_degree_start: float; sub_degree_end: float

@dataclass
class KPPlanet:
    planet: str; longitude: float; sign: str; sign_index: int
    is_retrograde: bool; kp: KPPosition
    # Shortcuts: .star_lord / .sub_lord / .sub_sub_lord / .nakshatra

@dataclass
class KPHouseSignificator:
    house: int; cusp_longitude: float; cusp_star_lord: str; cusp_sub_lord: str
    occupants: list[str]; house_lord: str; significators: list[str]

@dataclass
class KPChart:
    lagna_kp: KPPosition; planets: dict[str, KPPlanet]
    houses: dict[int, KPHouseSignificator]
    def for_planet(planet) -> KPPlanet
    def house_sub_lord(house) -> str
    def significators_of(house) -> list[str]
```

**Sub sequence**: Within each nakshatra, subs start from the nakshatra's own star lord (not Ketu).
**Pilot**: Whole-sign house cusps (0° of each sign). Placidus deferred to Phase 3.

---

## 4.23 `src/calculations/varshaphala.py` — Varshaphala Annual Solar Return

**Public API**:
```python
def compute_varshaphala(
    natal_chart: BirthChart,
    natal_birth_date: date,
    target_year: int,
    lat: float, lon: float,
    tz_offset: float = 5.5,
    ayanamsha: str = "lahiri",
) -> VarshaphalaReport
```

**Data classes**:
```python
@dataclass
class TajikaAspect:
    planet_a: str; planet_b: str; aspect_type: str
    angle: float; orb: float; applying: bool

@dataclass
class VarshaphalaReport:
    solar_return_jd: float; solar_return_date: date
    varsha_chart: BirthChart
    varsha_lagna_sign: str; varsha_lagna_sign_index: int
    years_elapsed: int
    muntha_sign_index: int; muntha_sign: str; varsha_pati: str
    tajika_aspects: list[TajikaAspect]
    def aspects_of_type(atype) -> list[TajikaAspect]
    def aspects_for_planet(planet) -> list[TajikaAspect]
```

**Tajika aspects**:
| Name | Angle | Max Orb |
|------|-------|---------|
| Itthasala | 60° (sextile) | 3° |
| Ishrafa | 120° (trine) | 4° |
| Nakta | 90° (square) | 3° |
| Kambool | 180° (opposition) | 5° |
| Dainya | 30° (semi-sextile) | 2° |

**Solar return algorithm**: Binary search (60 iterations, sub-arcsecond precision).
Handles Pisces→Aries 360° wrap via signed angular difference.

**Muntha formula**: `(natal_lagna_sign_index + years_elapsed) % 12`
**Varsha Pati**: sign lord of Muntha sign.

---

## 8. Test Suite (through Session 18)

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
tests/test_pushkara.py         30 tests  (S11)
tests/test_kundali_milan.py    25 tests  (S12)
tests/test_montecarlo.py       }
tests/test_chara_dasha.py      20 tests  (S14)
tests/test_varga.py            25 tests  (S15)
tests/test_sapta_varga.py      20 tests  (S16)
tests/test_kp.py               22 tests  (S17)
tests/test_varshaphala.py      22 tests  (S18)
                              ──────────
                              401 total
```
