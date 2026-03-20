# LagnaMaster — Session Log

## Phase 5 — Workbook Parity (Sessions 33–40)

### Session 33 — Multi-lagna engine
**Files:** `src/calculations/multi_lagna.py`
- Chandra Lagna (emotional axis), Surya Lagna (authority axis), Karakamsha (soul axis)
- Yogakaraka lookup for all 12 lagnas (from CALC_YogakarakaMap)
- All 12 Arudha Padas with exception rule — India 1947 AL=Virgo verified

### Session 34 — Extended scoring (5 axes)
**Files:** `src/calculations/multi_axis_scoring.py`
- 23-rule engine (R01–R23) across D1, Chandra, Surya, D9, D10
- R23: SAV bindu rule (≥5 bindus → bonus per school weight)
- School weights from REF_SchoolConfig (Parashari/KP/Jaimini)
- Yogakaraka multiplier: 1.5× Parashari/KP, 1.25× Jaimini

### Session 35 — Rule interaction engine
**Files:** `src/calculations/rule_interaction.py`
- All 30 rule-pair modifiers from REF_RuleInteractionMatrix
- Types: Amplified / Mixed Promise / Nullified / Neg-Amplified / Contextual

### Session 36 — Full 7-layer LPI
**Files:** `src/calculations/lpi.py`
- D1×35% + CL×15% + SL×10% + D9×15% + D10×10% + Dasha×10% + Gochar×5%
- DashaModifier ×1.15 for active MD lord's natal house
- Confidence (High/Med/Low) from inter-axis agreement range
- Domain balance: Dharma/Artha/Kama/Moksha averages
- Per-house RAG: Green ≥3.0 / Amber ≥0 / Red <0

### Session 37 — Divisional charts
**Files:** `src/calculations/divisional_charts.py`
- All 16 Shodasavargas (D1–D60) with correct sign formulas
- Vimshopaka Bala: weight table from REF_VimshopakaBala (max 20 pts)
- D60 Shastiamsha: all 60 division names + quality from REF_D60SignMap
- India 1947: D9 lagna = Pisces verified

### Session 38 — Complete yoga system
**Files:** `src/calculations/extended_yogas.py`
- 8 Raja Yoga pairs (Kendra×Trikona) + 5 Dhana Yoga pairs
- Viparita: Harsha / Sarala / Vimala + Dainya
- Neecha Bhanga: 3-condition check, all 7 planets
- Rasi Drishti: 12×12 sign aspect matrix from CALC_RasiDrishti
- Bhavat Bhavam chain formula
- All with dasha weighting (dormant=0.5×, active=1.0×)

### Session 39 — Avastha fix + Narrative
**Files:** `src/calculations/avastha_v2.py`, `src/calculations/narrative.py`
- **CRITICAL FIX:** Baaladi even-sign reversal. Sun 27.99° Cancer → Bala (not Mrita).
  Moon 3.98° Cancer → Mrita (not Bala). Verified against CALC_Avasthas.
- Sayanadi 12-state system
- Plain-English narrative report from 7-layer LPI

### Session 40 — Scoring v3 + Scenario explorer
**Files:** `src/calculations/scoring_v3.py`, `src/calculations/scenario.py`
- ENGINE_VERSION="3.0.0" — single entry point for all Phase 5 components
- Scenario explorer: override planet longitudes, compare counterfactual charts

---

## Phase 4 — Pressure Engine (Sessions 28–32)
See previous SESSION_LOG entries. ENGINE_VERSION="2.0.0".

## Phases 1–3 — Pilot, Features, Production (Sessions 1–27)
See docs/MEMORY.md for full session-by-session history.

---

## Phase 6 — Classical Depth (Sessions 41–48)

### Session 41 — Ishta / Kashta Phala
**File:** `src/calculations/ishta_kashta.py`  
BPHS Ch.27 formula grounded in REF_ShadbalaData. Uchcha_Bala computed from
angular distance to exaltation longitude. Cheshta_Bala from speed vs mean motion
(retrograde=60, stationary=30). India 1947: Sun at 27.99° Cancer — moderate
Uchcha_Bala confirmed (not exalted in Cancer, exaltation is Aries).

### Session 42 — Longevity Doctrine + Balarishta
**File:** `src/calculations/longevity.py`  
Three methods from BPHS Ch.44. Pindayu uses planet max-years weighted by
exaltation strength ratio. Nisargayu uses natural lifespan × house weight
(Kendra=1.0, Panapara=0.5, Apoklima=0.25). Amsayu uses D9 dignity strength.
Balarishta: three classical indicators — Moon in dusthana, Lagnesh in dusthana,
simultaneous malefics in H1+H8.

### Session 43 — Yogini Dasha
**File:** `src/calculations/yogini_dasha.py`  
Starting Yogini: `(nakshatra_index mod 8)` where index = `floor(moon_lon × 27 / 360)`.
Bug fix: original code called `compute_nakshatra()` which doesn't exist by that
name — replaced with direct longitude formula. Balance proportional to Moon's
position within its nakshatra. Antara periods proportional within each 
Mahadasha (same Yogini sequence, scaled).

### Session 44 — Full KP Engine
**File:** `src/calculations/kp_full.py`  
Sub-lord algorithm matches REF_KPSubLordTable exactly: `_SUB_SPAN_DEG[planet] = 
nakshatra_span × planet_years / 120`. Sub-lord sequence starts from the nakshatra
lord's position in Vimshottari order. Sub-sub spans are further proportional
subdivision. India 1947 regression: Lagna at 37.73° = Krittika (Sun nakshatra),
nak_lord = Sun — confirmed.

### Session 45 — Extended Yoga Library
**File:** `src/calculations/yogas_extended.py`  
Nabhasa Sankhya: count occupied signs, map to Gola(1)→Yugma(2)→Shoola(3)→
Kedara(4)→Pasha(5)→Dama(6)→Veena(7). India 1947 Kemadruma test: Moon in
Cancer (H3) has Jupiter also in Cancer — Kemadruma absent, confirmed.
Lakshmi Yoga from Phaladeepika Ch.6 (Venus + 9th lord strong in kendra/trikona).

### Session 46 — Special Lagnas
**File:** `src/calculations/special_lagnas.py`  
Indu Lagna planet values from BPHS: Sun=30, Moon=16, Mars=6, Mercury=8,
Jupiter=10, Venus=12, Saturn=1. 9th lords from both Lagna and Moon, sum their
Indu values mod 12, count from Moon's sign.

### Session 47 — Full Jaimini System
**File:** `src/calculations/jaimini_full.py`  
Brahma/Maheshvara/Rudra longevity: Brahma = strongest odd-house planet,
Maheshvara = lord of 8th from AK's sign, Rudra = stronger of H8/H12 lords
by house strength score (Kendra=4, Panapara=2, Apoklima=1). Pada relationship:
sign difference 0=+2.0, 4or8=+1.5, 5or7=−1.5.

### Session 48 — Empirical Validation Backend
**Files:** `src/calculations/empirica.py`, `src/api/empirica_router.py`  
Three 1947 India seed events loaded from REF_EmpiricaSchema: EVT_001 (1971 war
victory, H10 Career, d1=3.5, Saturn MD, manifested=1), EVT_002 (1991 economic
liberalisation, H11 Finance, d1=2.0, Jupiter MD, manifested=1), EVT_003 (2001
Parliament attack, H6 Conflicts, d1=−2.5, Saturn MD, manifested=1). Rule lift
formula: accuracy = manifested_when_fired / fired_count, lift = accuracy / base_rate.
