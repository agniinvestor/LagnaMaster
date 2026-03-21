# LagnaMaster — Programme Plan

## Status: Sessions 1–108 COMPLETE ✅ | Phase 0 CRIT fixes begin Session 109 🔄

ENGINE_VERSION = "3.0.0"

> **Source of truth:** Classical Sanskrit texts — BPHS (PVRNR), Phaladeepika (Mantreswara),
> Saravali (Kalyanarma), Brihat Jataka (Varahamihira), Jaimini Sutras.
> The Excel workbook was the prototype source for Sessions 1–56 only and is no longer
> authoritative. See `AUDIT.md` for the full classical audit (March 2026).

---

## Audit Reconciliation — Issues Closed by Sessions 41–100

The classical audit (March 2026) was written against the Session 1–10 state. Many of the
issues it raised were resolved in Sessions 41–100. These are **closed** — do not re-implement.

| Audit Ref | Issue Raised | Resolution | Session |
|-----------|-------------|------------|---------|
| VI (Vargas) | D1+D9 only of 16 mandatory vargas | `vargas.py` — 20 divisional charts D1–D60 | S41–48 |
| XIII-B | Rashi Drishti absent | `jaimini_full.py` — full Jaimini school | S41–48 |
| XIII-C | Arudha Lagnas A1–A12 absent | `argala.py` + `jaimini_full.py` | S31, S41–48 |
| XIII-D | Argala system absent | `argala.py` | S31 |
| VIII-C | Viparita Raja Yoga absent | `extended_yogas.py` 200+ yogas | S41–48 |
| VIII-E | 36 Nabhasa Yogas absent | `nabhasa_yogas.py` + `extended_yogas.py` | S41–48 |
| IX-D | 6 major dasha systems missing | Yogini, Chara, Kalachakra, Ashtottari, Shoola, Tara | S94–100 |
| XV | Kundali Milan 8-Koota absent | `kundali_milan.py` | S41–48 |
| XVII | Upaya (remedial) absent | `upaya.py` — PVRNR Tables 77–78 | S97 |
| XII | Muhurta / Prashna / Hora absent | `muhurta.py`, `prashna.py`, `panchanga.py` | S91–93 |
| XIX-B | No PDF export | `report.py` — reportlab | S41–48 |
| VII-B | Saptavargaja Bala = 0 (no vargas) | vargas.py unblocks this — implement in Phase 0 S111 | S41–48 (partial) |
| I-A | Additive weights non-classical | Design fact documented in AUDIT.md and UI; not a code fix | — |

---

## Phase 0 — Classical Correctness: All 🔴 CRIT Issues (Sessions 109–114)

**Principle:** Fix everything producing wrong output before adding new features.
No new modules. No new UI. Every fix has a cited śhloka.

### Session 109 — Dignity Engine: MT Ranges, Paramotcha, Rahu/Ketu, Neecha Bhanga

**File:** `src/calculations/dignity.py`

**Fix 1 — Mooltrikona degree ranges** (BPHS Ch.3 v.2–9)

Hard-code exact BPHS boundaries. Currently approximated:

| Planet | MT Sign | Correct MT Range | Non-MT Own Sign |
|--------|---------|-----------------|-----------------|
| Sun | Leo | 0°–20° | 20°–30° |
| Moon | Taurus | **4°–30°** | 0°–3°59' Taurus; all of Cancer |
| Mars | Aries | 0°–12° | 12°–30° Aries; all Scorpio |
| Mercury | Virgo | **16°–20°** | 0°–15°59'; 20°–30° Virgo; all Gemini |
| Jupiter | Sagittarius | 0°–10° | 10°–30° Sag; all Pisces |
| Venus | Libra | 0°–15° | 15°–30° Libra; all Taurus |
| Saturn | Aquarius | 0°–20° | 20°–30° Aquarius; all Capricorn |

Mercury is the critical case — MT range is only 4° wide. Any approximation produces wrong results for 87% of Mercury positions in Virgo.

**Fix 2 — Exaltation Paramotcha gradient** (Phaladeepika Ch.2 v.4–7)

Replace binary `EXALT` flag with continuous Uchcha Bala:
`uchcha_bala = 60 × (1 − |degree_in_sign − paramotcha_degree| / 30)`

| Planet | Exalt Sign | Paramotcha ° | Debil Sign | Neecha ° |
|--------|-----------|-------------|------------|---------|
| Sun | Aries | 10° | Libra | 10° |
| Moon | Taurus | 3° | Scorpio | 3° |
| Mars | Capricorn | 28° | Cancer | 28° |
| Mercury | Virgo | 15° | Pisces | 15° |
| Jupiter | Cancer | 5° | Capricorn | 5° |
| Venus | Pisces | 27° | Virgo | 27° |
| Saturn | Libra | 20° | Aries | 20° |

Add `DEEP_EXALT` enum value (within 5° of Paramotcha). Keep `EXALT` for full sign.

**Fix 3 — Rahu/Ketu dignity** (BPHS Ch.3)

Replace universal `NEUTRAL` with school-declared exaltation/debilitation.
Default: BPHS school — Rahu exalted Taurus, debilitated Scorpio; Ketu exalted Scorpio, debilitated Taurus.
Add `node_dignity_school: 'bphs' | 'raman' | 'south_indian'` to CalcConfig.

**Fix 4 — Neecha Bhanga all 6 conditions** (BPHS Ch.49 v.12–18; Uttarakalamrita Ch.4)

Currently only condition 1 is coded. Implement all 6 as separate booleans on `DignityResult`:

1. ✅ Lord of debilitation sign in Kendra from Lagna
2. ❌ Lord of debilitation sign in Kendra from Moon
3. ❌ Planet that would exalt in the debilitation sign in Kendra from Lagna
4. ❌ Planet that would exalt in the debilitation sign in Kendra from Moon
5. ❌ Debilitated planet aspected by its debilitation sign lord
6. ❌ Debilitated planet in Parivartana with the sign lord

When `neecha_bhanga_count ≥ 2`: classify as `NEECHA_BHANGA_RAJA_YOGA` (+1.5 scoring bonus per Uttarakalamrita Ch.4).

**New tests:** 14 unit tests — MT boundary degrees per planet, Paramotcha gradient at 0°/peak/30°, Rahu in Taurus = EXALT, 6 Neecha Bhanga conditions each independently triggered.

---

### Session 110 — Scoring Engine: Aspect Weights, Score Gradient, Kemadruma, Raj Yoga

**Files:** `src/scoring.py`, `src/scoring_v3.py`, `src/calculations/yogas.py`

**Fix 1 — Partial aspect strengths** (BPHS Ch.26 v.3–5)

BPHS explicitly states Mars/Jupiter/Saturn special aspects are three-quarter (¾) strength, not full. The WC-halving (0.5×) on rules R03/R07/R10/R14 applied this incorrectly and uniformly.

Replace with `ASPECT_STRENGTH` dict:
```python
ASPECT_STRENGTH = {
    ("Mars",    4): 0.75, ("Mars",    8): 0.75,
    ("Jupiter", 5): 0.75, ("Jupiter", 9): 0.75,
    ("Saturn",  3): 0.75, ("Saturn", 10): 0.75,
}  # All other aspects = 1.0 (full)
```
Remove WC-halving entirely. Multiply each aspect rule contribution by `ASPECT_STRENGTH.get((planet, houses_from), 1.0)`.

**Fix 2 — Score gradient** (scoring architecture)

Clipping at [−10, +10] makes charts with raw scores of +11 and +47 indistinguishable.
- Store `raw_score` unclamped (no change to data model — already stored)
- Add `display_score = round(10 * tanh(raw_score / 8), 2)` for smooth compression
- API returns both; UI displays `display_score`; raw accessible via L3

**Fix 3 — Kemadruma: all 3 conditions + 4 cancellations** (Phaladeepika Ch.6 v.56–60)

Current: checks only "no planets in 2nd/12th from Moon."
Full definition requires ALL 3 conditions:
1. No planets in 2nd or 12th from Moon ✅ exists
2. No planets in any Kendra (H1/H4/H7/H10) from Moon ❌
3. Moon not aspected by any benefic ❌

Then check 4 cancellation conditions before confirming:
- Moon in Kendra from Lagna
- Moon conjoined or aspected by a benefic
- Moon in exalted or own sign
- Lagna lord conjoined Moon

**Fix 4 — Raj Yoga: exchange and aspect forms** (BPHS Ch.36 v.1–15)

Current: conjunction only. Add:
- Parivartana (mutual sign exchange) between Kendra lord and Trikona lord
- Kendra lord aspecting (full 7th) the Trikona lord's sign
- Trikona lord aspecting the Kendra lord's sign
- Cancellation check: if either planet is combust or in dusthana, downgrade to "weak Raj Yoga"

**New tests:** 12 tests — aspect strength values by planet/house, tanh gradient shape, Kemadruma 3 conditions + 4 cancellations, Raj Yoga via exchange and aspect.

---

### Session 111 — Shadbala: Dig Bala, Kala Bala, Drik Bala, Naisargika, Saptavargaja

**File:** `src/calculations/shadbala.py`, `src/calculations/dig_bala.py`

**Fix 1 — Dig Bala formula** (BPHS Ch.27 v.12–15)

Current formula uses house-number distance (`/6`) — dimensionally wrong. BPHS uses degree-arc distance:
```python
peak_cusp_lon = (dig_bala_house - 1) * 30 + (lagna_lon % 30)
arc_dist = min((planet_lon - peak_cusp_lon) % 360,
               (peak_cusp_lon - planet_lon) % 360)
dig_bala = 60 * (180 - arc_dist) / 180
```

**Fix 2 — Kala Bala: 7 missing sub-components** (BPHS Ch.27 v.30–62)

Only Paksha Bala is computed. Add all 8:

| Sub-component | Formula | Max Virupas |
|--------------|---------|------------|
| Nathonnata Bala | Sun/Jupiter/Venus strong by day; Moon/Mars/Saturn by night; Mercury always | 60 |
| Paksha Bala | ✅ exists — verify benefic/malefic inversion | 60 |
| Tribhaga Bala | Day ÷ 3 watches: Jupiter/Sun/Saturn; Night: Moon/Venus/Mars | 60 |
| Vara Bala | Planet ruling birth weekday | 45 |
| Hora Bala | Planet ruling birth hora (hour) | 60 |
| Masa Bala | Planet ruling birth Hindu month | 30 |
| Abda Bala | Planet ruling birth Hindu year | 15 |
| Ayana Bala | Sun's Uttarayana/Dakshinayana × planet preference | 60 |

Weekday lord and Hora lord already in `panchanga.py` — import and reuse.

**Fix 3 — Drik Bala** (BPHS Ch.27 v.22–29)

Currently 0 in all charts. Implement as signed sum of aspectual influences received:
```python
drik_bala = sum(
    aspect_fraction(aspector, planet) * shubha_value(aspector, chart)
    for aspector in all_planets if aspector != planet
)
```
Where `shubha_value` returns +1 for benefic, −1 for malefic (chart-specific, not natural classification).

**Fix 4 — Naisargika Bala values** (BPHS Ch.27)

Assert fixed hierarchy: Sun=60, Moon=51.43, Venus=42.86, Jupiter=34.29, Mercury=25.71, Mars=17.14, Saturn=8.57.
Add unit test asserting these exact values.

**Fix 5 — Saptavargaja Bala** (BPHS Ch.27 v.1–20)

`vargas.py` now provides D1/D2/D3/D7/D9/D12/D30. Compute dignity in each, multiply by virupa table:

| Dignity | Virupas per Varga |
|---------|------------------|
| Own Sign / Mooltrikona | 30 |
| Exaltation / Adhimitra sign | 22.5 |
| Mitra sign | 15 |
| Sama (Neutral) | 7.5 |
| Shatru sign | 3.75 |
| Neecha / Adhi Shatru | 1.875 |

Sum across all 7 vargas. Max = 210 Virupas. This was 0 before vargas were built.

**New tests:** 14 tests — Dig Bala degree-arc formula (all 7 planets vs known values), Kala Bala sub-components from 1947 chart, Drik Bala sign, Naisargika Bala exact values, Saptavargaja Bala non-zero.

---

### Session 112 — Ashtakavarga: Both Shodhana Reductions

**File:** `src/calculations/ashtakavarga.py`

**Fix 1 — Trikona Shodhana** (PVRNR, Ashtakavarga System Ch.4)

For each of 4 trine groups: find minimum bindu value, subtract from all three:
```python
def trikona_shodhana(bindus: list[int]) -> list[int]:
    result = bindus[:]
    for group in [(0,4,8), (1,5,9), (2,6,10), (3,7,11)]:
        m = min(result[i] for i in group)
        for i in group:
            result[i] -= m
    return result
```
Apply to each planet's bindu table before storing or displaying.

**Fix 2 — Ekadhipatya Shodhana** (PVRNR, Ashtakavarga System Ch.5)

For dual-ruled sign pairs (Mars: 0/7, Mercury: 2/5, Jupiter: 8/11, Venus: 1/6, Saturn: 9/10):
- If planet occupies one of its own signs: apply conditional reduction per PVRNR Ch.5 rule
- If planet in third sign: reduce lower-bindu sign by subtracting higher, zero the lower

**Fix 3 — Sarvashtakavarga reduction**

After reducing all 7 planet tables, recompute Sarva from reduced tables, then apply Trikona + Ekadhipatya Shodhana to the Sarva table itself.

**New tests:** 12 tests — Trikona Shodhana reduces known values, Ekadhipatya both cases (planet in own sign vs third sign), Sarva = sum of reduced tables, India 1947 reduced totals vs JHora export.

---

### Session 113 — Nakshatra Float Fix + 8 New Regression Fixtures

**Files:** `src/calculations/nakshatra.py`, `src/calculations/vimshottari_dasa.py`, `tests/fixtures.py`

**Fix 1 — Nakshatra index float** (Swiss Ephemeris precision)

Replace `int(moon_lon / 13.333)` with `int(moon_lon * 3 / 40)` in all nakshatra index computations. The value 13.333 is a truncated float of 40/3 — at boundary positions the truncation error misassigns the nakshatra and therefore the entire Vimshottari balance.

**Fix 2 — 8 new regression fixtures** (BV Raman, Notable Horoscopes; PVRNR, Astrology of the Seers)

| Fixture | Chart Type | Validates |
|---------|-----------|-----------|
| `NEECHA_BHANGA` | Debilitated planet with 2+ cancellation conditions active | All 6 NB conditions |
| `GRAHA_YUDDHA` | Mars and Venus within 1° lon + 1° lat | War detection, loser dignity |
| `NAK_CUSP` | Moon within 0.01° of nakshatra boundary | Float-fix correctness |
| `PARIVARTANA` | Two planets in mutual sign exchange | Parivartana detection |
| `FEMALE_CHART` | Female, night birth, Sun/Moon/Lagna in even signs | Mahabhagya Yoga gender rules |
| `HIGH_LATITUDE` | Birth at 61°N (Helsinki area) | Bhava Chalita cusp divergence |
| `YEAR_BOUNDARY` | Birth 1800-01-01 and 2099-12-31 | Ephemeris edge accuracy |
| `KNOWN_CELEBRITY` | Chart from PVRNR's Astrology of the Seers with known events | Dasha timing validation |

**New tests:** 24 tests — nakshatra boundary at 40.000°/80.000°/360.000°, each of the 8 new fixtures computes without error and matches known values.

---

### Session 114 — Cross-Validation vs JHora + Karana Boundary Fix

**Files:** `tests/cross_validate.py` (new), `src/calculations/panchanga.py`

**Fix 1 — JHora cross-validation script**

```python
# tests/cross_validate.py
def cross_validate_against_jhora(jhora_csv_path: str, chart_inputs: dict) -> ValidationReport:
    """
    Compare LagnaMaster output field-by-field against a JHora CSV export.
    Tolerance: positions ±0.1°, Shadbala totals ±5%, yoga names exact match.
    Returns list of (field, lm_value, jhora_value, within_tolerance).
    """
```
Run against JHora 8.0 (free) CSV export for India 1947 + at least 2 other charts. Zero divergences on planet positions. Document any Shadbala divergences with explanation.

**Fix 2 — Karana boundary for 4 fixed Karanas** (BPHS Panchanga chapter)

Fixed Karanas (Kimstughna, Shakuni, Chatushpada, Naga) occur at astronomically fixed positions in the lunar month, not by cycling. Verify and fix:
- Kimstughna: index 0 only (1st half of 1st Tithi of Krishna Paksha each month)
- Vishti/Bhadra: index 7, 14, 21, 28, 35, 42, 49 (7th of each movable cycle)
- Shakuni/Chatushpada/Naga: last 3 half-tithis of month only

**New tests:** 12 tests — cross-validation report structure, India 1947 positions within tolerance, Kimstughna at correct position, Vishti flag on all correct indices.

---

## Phase 1 — All 🟠 HIGH Issues (Sessions 115–124)

### Session 115 — Vargottama + Parivartana + Planetary Latitudes

**File:** `src/calculations/dignity.py`, `src/calculations/planet_chains.py`, `src/ephemeris.py`

- **Vargottama** (PVRNR, Vedic Astrology Ch.9): `is_vargottama(lon)` — D1 sign == D9 sign. Add to `PlanetPosition`. Apply +0.75 Shadbala Uchcha Bala bonus. Three Vargottama zones: 0°–3°20', 13°20'–16°40', 26°40'–30° are most powerful (also Sandhi).
- **Parivartana Yoga** (PVRNR, Astrology of the Seers Ch.11): `detect_parivartana(chart)` — classify Maha/Kahala/Dainya. Override dignity to OWN_SIGN for both planets. This exists partially in `planet_chains.py` — extend with dignity override.
- **Planetary latitudes**: `latitude: float` already returned by pyswisseph but discarded. Add to `PlanetPosition`. Required for Graha Yuddha (Session 116).

### Session 116 — Graha Yuddha with Latitudes

**File:** `src/calculations/graha_yuddha.py`

Current implementation detects war by longitude proximity only. BPHS/Saravali Ch.4 v.12–18 requires BOTH longitude diff < 1° AND latitude diff < 1°. Winner determined by northward latitude (smaller north lat = loser). Add latitude-based winner detection. Apply DEBIL-equivalent dignity to loser for scoring.

### Session 117 — Combustion Orbs by School + Sandhi Flag

**File:** `src/calculations/dignity.py`

- **Combustion orbs by school**: Add `COMBUSTION_ORBS_BY_SCHOOL` dict (BPHS vs Raman school differ on Venus/Saturn). Default BPHS values. Expose via CalcConfig.
- **Sandhi flag** (Phaladeepika Ch.2 v.30): `is_sandhi(lon)` — True if `degree_in_sign < 1°` or `degree_in_sign > 29°`. Sandhi planets give confused results regardless of sign dignity. Add to `PlanetPosition`. Apply −0.5 Shadbala modifier and note in scoring.

### Session 118 — Bhava Chalita Overlay

**File:** `src/calculations/house_lord.py`, `src/ui/chart_visual.py`

- Compute Midheaven (MC) from `swe.houses()`. Derive 12 equal Bhava Chalita cusps from MC.
- Add `bhava_chalita_houses: dict[str, int]` to `BirthChart` — each planet's Bhava Chalita house (may differ from whole-sign house for planets near sign boundaries).
- Display as second column in chart UI Rule Detail tab. Flag planets whose whole-sign house ≠ Bhava Chalita house.
- Source: BPHS Ch.6; BV Raman, How to Judge a Horoscope Vol.1 p.12–14.

### Session 119 — PM Yoga D9 Strength + Vesi/Vasi Node Fix + Additional Yoga Fixes

**File:** `src/calculations/yogas.py`

- **PM Yoga D9 check** (Sanjay Rath, Crux of Vedic Astrology Ch.5): After S109 vargas, add D9 dignity check to PM Yoga. Vargottama = full-strength; D9 in own/exalt sign = standard; D9 debilitated = weak PM Yoga.
- **Vesi/Vasi node exclusion** (Phaladeepika Ch.7 v.10–12): Confirm Rahu/Ketu excluded from counts. Sun and Moon also excluded from Vesi/Vasi counts.
- **Sunapha/Anapha/Durudhura** (BPHS Ch.38): Planets in 2nd from Moon (Sunapha), 12th from Moon (Anapha), or both (Durudhura) — Sun excluded. Add to yogas.py.

### Session 120 — Pratyantar Dasha (3rd Level)

**File:** `src/calculations/vimshottari_dasa.py`

Add `PratyantarDasha` as 3rd level under `AntarDasha`:
```python
pratyantar_years = maha_years × antar_years × pratyantar_lord_years / 120 / 120
```
Same sequence as MD/AD. `current_dasha()` returns `tuple[MahaDasha, AntarDasha, PratyantarDasha]`.
Source: K.N. Rao, Timing Events Through Vimshottari Dasha (core methodology uses Pratyantar).

### Session 121 — Narayana Dasha Direction Verification

**File:** `src/calculations/narayana_dasha.py`

Verify direction re-evaluates per sign (not only from Lagna parity). Per Sanjay Rath, Nadiamsa and Chara Dasha Ch.4: direction reverses at each sign transition. The initial Lagna parity sets only the first sign's direction; each subsequent sign decides its own direction by its own parity.

### Session 122 — Transit: Vedha + Moon/Sun Lagna + Ashtama Shani

**File:** `src/calculations/gochara.py`

- **Vedha obstruction** (Phaladeepika Ch.26 v.10–18): Add `VEDHA_PAIRS = {1:5, 2:12, 3:12, 4:3, 5:9, 6:12, 7:2, 8:5, 9:8, 10:9, 11:8, 12:6}`. Add `is_vedha_blocked: dict[str, bool]` to `GocharaReport`. Flag in UI.
- **Transit from Moon + Sun lagna** (Phaladeepika Ch.26 v.1–5): Compute transit house from natal Moon and natal Sun as reference points. Add `moon_lagna_houses` and `sun_lagna_houses` dicts to `GocharaReport`.
- **Ashtama Shani** (K.N. Rao, Yogis Destiny Ch.7): Flag when Saturn is in H8 from natal Moon (often more difficult than Sade Sati itself). Add `ashtama_shani: bool` to `GocharaReport`.

### Session 123 — Upagrahas (Mandi/Gulika)

**File:** `src/calculations/upagrahas.py` (new)

Source: BPHS Ch.25; Phaladeepika Ch.26.
Mandi and Gulika computed from weekday, birth time, day/night duration:
```python
mandi_lon = sunrise_lon + (weekday_lord_order × day_duration / 8)
gulika_lon = mandi_lon - (day_duration / 8)  # Gulika precedes Mandi
```
Requires sunrise time from `swe.rise_trans()`. Add to `BirthChart.upagrahas` dict. Add to SVG chart display.

### Session 124 — Ayanamsha Expansion + Node Mode Toggle

**File:** `src/calculations/config_toggles.py`, `src/ephemeris.py`

- **Additional ayanamshas**: Expose all 36 pyswisseph `SE_SIDM_*` constants in `AYANAMSHA_MAP`. Priority additions: True Chitrapaksha (used by PVRNR), Yukteshwar, Fagan-Bradley, True Mula/Galactic Centre.
- **Ayanamsha warning**: Add `lagna_ayanamsha_sensitive: bool` flag when Lagna is within 1° of a sign boundary — ayanamsha choice may change the Lagna sign.
- **Node mode**: `node_mode: 'mean' | 'true'` in CalcConfig. Default mean (Parashari standard per PVRNR). True node for KP school. Difference can reach 1.5°.

---

## Phase 2 — Depth (Sessions 125–134)

| Session | Deliverable | Source |
|---------|------------|--------|
| 125 | Bhava Bala: Bhavadhipati + Dig Bala + Drishti Bala per house | BPHS Ch.27 v.32–41 |
| 126 | Kakshya analysis in AV transits (3°45' sub-divisions) | BV Raman, AV System Ch.9 |
| 127 | Ishta/Kashta Bala (√(Uchcha×Chesta) / √((60−U)×(60−C))) | BPHS Ch.27 v.70–75 |
| 128 | Sputa Drishti (exact degree-based aspect orb) | Saravali; Sarvartha Chintamani |
| 129 | 8-Karaka Chara Karaka option (Rahu eligible as AK) | BPHS Ch.32 |
| 130 | Special Lagnas: Hora, Ghati, Bhava, Varnada, Sree, Indu, Pranapada | Jaimini Sutras; BPHS Ch.13 |
| 131 | Dasha Sandhi alerting (last/first 6 months of each MD) | K.N. Rao, Astrology Destiny Ch.3 |
| 132 | North Indian + East Indian chart styles in SVG | Visual standard |
| 133 | Ayurdaya (longevity): Pindayu + Amsayu + Nisargayu | BPHS Ch.44 |
| 134 | Expanded yoga library: target 150+ named yogas with śhloka citations | Uttarakalamrita Khandas 1–4 |

---

## Phase 3 — Production Hardening (Sessions 135+)

| Item | Trigger |
|------|---------|
| End-to-end integration test: Next.js ↔ FastAPI ↔ guidance pipeline | Before public launch |
| React Native mobile shell (router done at S90) | Mobile launch |
| Practitioner opt-in directory (S89 infrastructure ready) | Post-launch |
| GDPR privacy policy and ToS text | Legal team |
| First 50 empirica events for accuracy baseline | S48 router ready |
| KP Sub-lord system (true node, cusp significators) | After S124 node mode |
| Varshaphala / Solar Return with Muntha + Tajika aspects | Post-Phase 2 |
| ML-based yoga strength calibration from verified chart corpus | Research phase |

---

## Sessions 91–108 — Complete ✅

*(Full session specs in previous plan entries below — unchanged)*

---

## Phase 15–18 — Muhurta, Prashna, Additional Dashas, Upaya, Mundane (Sessions 91–100) ✅

### Session 91 — Panchanga (5 limbs of the almanac)
**File:** `src/calculations/panchanga.py`
Complete Panchanga engine replacing `panchang.py`. Tithi, Vara, Nakshatra, Yoga, Karana.
Amrita Siddhi + Sarvaartha Siddhi. Hora. Choghadiya. `compute_navamsha_chart()` backward compat.

### Session 92 — Muhurta Engine
**File:** `src/calculations/muhurta.py`
PVRNR Table 79. 7 task types. Tarabala + Chandrabala. 0–7 score: Excellent/Good/Acceptable/Avoid.

### Session 93 — Prashna (Horary)
**File:** `src/calculations/prashna.py`
10 query types. Yes/Possible/Unlikely/No verdict. High/Moderate/Low confidence.

### Session 94 — Kalachakra Dasha
**File:** `src/calculations/kalachakra_dasha.py`
BPHS Ch.36–42. Savya/Apasavya from Moon's navamsha pada. Deha/Jeeva flags.

### Session 95 — Shoola Dasha + Sudasa
**File:** `src/calculations/shoola_dasha.py`
Shoola (longevity) + Sudasa (material success).

### Session 96 — Tara Dasha
**File:** `src/calculations/tara_dasha.py`
9-category nakshatra: Janma→Ati-Mitra. Vimshottari period lengths.

### Session 97 — Upaya (Remedial Measures)
**File:** `src/calculations/upaya.py`
PVRNR Tables 77–78. Auto-detect afflictions. Disclaimer on every recommendation — never removed.

### Session 98 — Mundane Astrology
**File:** `src/calculations/mundane.py`
PVRNR Ch.35. Nation/ingress/swearing-in. `compress_vimshottari()`.

### Session 99 — Contextual Layer (partial DKP)
**File:** `src/calculations/contextual.py`
Era-aware profession mapping. Explicit practitioner note — partial DKP only.

### Session 100 — Ashtottari Dasha
**File:** `src/calculations/ashtottari_dasha.py`
BPHS Ch.47. 108yr, 8 planets. `qualifies_for_ashtottari()` required.

### Sessions 101–108 — Phase 0 initial fixes (remote)
DivisionalMap compat fixes (`longevity.py`, `multi_lagna.py`). Docs refresh. Audit published.

---

## Phase 7–9 and Phases 10–14 — Sessions 49–90 ✅

*(See CHANGELOG.md for full session-by-session history)*

---

## Genuine Theoretical Limits (Correctly Excluded)

| Item | Reason |
|------|--------|
| Kalachakra full textual variants | Contradictory commentators; BPHS version implemented |
| Desha-Kala-Patra in full | Requires practitioner situational judgment |
| Gestalt synthesis | Named BPHS rules encoded; nonlinear expert weighting is not |
| Prashna Marga full corpus | Separate discipline with different inputs |
| Medical / financial astrology | Separate disciplines with liability implications |
| Causal event labelling | Planetary signatures computable; sociological labelling is not |

---

## Source Authority Hierarchy

1. **BPHS** — Brihat Parasara Hora Sastra (PVRNR translation, Sagar Publications)
2. **Phaladeepika** — Mantreswara (G.S. Kapoor, Ranjan Publications)
3. **Saravali** — Kalyanarma (R. Santhanam, Ranjan Publications)
4. **Brihat Jataka** — Varahamihira (B.S. Rao, Ranjan Publications)
5. **Jaimini Sutras** — Sanjay Rath commentary (Sagittarius Publications)
6. **Uttarakalamrita** — Kalidasa (P.S. Sastri, Ranjan Publications)
7. Modern: BV Raman · K.N. Rao · Sanjay Rath · Hart de Fouw & Robert Svoboda · Gayatri Devi Vasudev · Komilla Sutton · Dennis Harness

The Excel workbook is not a source. It was a prototype input for Sessions 1–56 only.
