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

---

## Phase 7 — Workbook Completeness (Sessions 49–56)

### Session 49 — Full 12-state Sayanadi + Deena wiring
**File:** `src/calculations/sayanadi_full.py`
Source: REF_AvasthaRules §2 (BPHS Ch.45–47). Previous avastha_v2.py had 7 states.
Five decanate states added: Sayana/Upavesh/Netrapani for odd signs (decanates 1/2/3),
Kautuka/Nishcheshta for even signs (decanates 1/2). Deena state now wired from
graha_yuddha.py — `compute_all_sayanadi(chart, yuddha_losers=set())`.
India 1947: Moon in Cancer (own sign) → Sthira (priority 3, modifier 1.25).
Moon decanate would be Kautuka (even, 0°–10°) but Sthira takes priority.

### Session 50 — Panchadha Maitri wired to R06/R07/R13/R14
**File:** `src/calculations/panchadha_maitri.py`
Source: CALC_PanchadhaMaitri §4, CALC_TatkalikFriendship §4, BPHS Ch.15.
Tatkalik: count houses from P1's sign to P2's sign. H2/3/4/10/11/12 = Friend.
Pairs: Nai-F×Tat-F=Adhi Mitra, Nai-F×Tat-E=Sama, Nai-N×Tat-F=Mitra,
Nai-N×Tat-E=Shatru, Nai-E×Tat-F=Sama, Nai-E×Tat-E=Adhi Shatru.
India 1947 matrix verified: Sun views Mars (Gemini, H12 from Cancer) as Tatkalik
Friend. Naisargika: Friend. Combined: Adhi Mitra. Workbook confirms.

### Session 51 — Lagnesh global modifier
**File:** `src/calculations/lagnesh_strength.py`
Source: CALC_LagneshStrength, SCORE_AllHouses row 42.
9-condition table. India 1947: Venus (Lagnesh) in H3 (neither kendra/trikona
nor dukshthan), neutral dignity in Cancer → modifier = 0.00. Confirmed against
workbook live value (col I = 0).

### Session 52 — Dig Bala continuous score
**File:** `src/calculations/dig_bala.py`
Source: CALC_DigBala col G, BPHS Ch.27. Formula: `1 − min_circular_dist / 6`.
All 7 workbook values verified against CALC_DigBala India 1947 column G:
Sun(H3)=0.167, Moon(H3)=0.833, Mars(H2)=0.333, Mercury(H3)=0.667,
Jupiter(H6)=0.167, Venus(H3)=0.833, Saturn(H3)=0.333.

### Session 53 — Graha Yogas (YOGA_Graha sheet)
**File:** `src/calculations/yogas_graha.py`
Source: YOGA_Graha. 4 missing + 2 verified yogas.
India 1947 confirmed present: Budhaditya (Sun+Mercury in Cancer), Gaja Kesari
(Jup H6, Moon H3, diff=3 → mutual kendra), Kahala (H4 lord Mercury + H9 lord
Jupiter mutual kendra diff = |6−3|=3 → kendra distance).
Saraswati: requires Jup+Ven+Mer all in kendra/trikona — Jup in H6 (not strong).

### Session 54 — Narayana Dasha Argala (ND-6)
**File:** `src/calculations/narayana_argala.py`
Source: NOTES_NarayanaDasaCompliance ND-6, PVRNR Narayana Dasha Ch.5.
Argala positions H2(Dhan)/H4(Sukha)/H11(Labha) = primary (0.5 weight each).
H5(Putra) = secondary (0.25). Virodha: H12→cancels H2, H10→H4, H3→H11, H9→H5.
Gross argala = sum(benefic_count×0.15 + malefic_count×0.05).
Virodha reduction = min(gross, virodha_count×0.10). Net capped ±0.5.

### Session 55 — Configuration toggles
**File:** `src/calculations/config_toggles.py`
Source: REF_Config §1.
Ayanamsha IDs from pyswisseph: SE_SIDM_FAGAN_BRADLEY=0, SE_SIDM_LAHIRI=1,
SE_SIDM_RAMAN=3, SE_SIDM_KRISHNAMURTI=5. R22 modifier: outer planets
(Mars/Jup/Sat/Rahu/Ketu) retrograde = +0.10, inner (Mer/Ven) = −0.10,
"ignore" = 0.0, "classical" = 0.0 (full strength traditional view).

### Session 56 — Varga agreement confidence flag
**File:** `src/calculations/varga_agreement.py`
Source: CALC_CompositeVargaScore col I.
★★ (High): all 3 same sign(positive/negative). ★ (Moderate): D1+D9 agree.
○ (Low): D1 and D9 disagree. India 1947 confirmed:
H2 Wealth D1=−5.25, D9=−2.0, D10=−2.5 → all negative → ★★ High.
H1 Self D1=+1.25, D9=−1.35, D10=−1.9 → D1 positive, D9/D10 negative → ○ Low.

---

## Phase 8 — PVRNR Textbook Tier 1 (Sessions 57–63)

### Session 57 — Orb-sensitive conjunction strength
**File:** `src/calculations/orb_strength.py`  
Source: PVRNR "Vedic Astrology: An Integrated Approach" p147, p149.
p147 explicit: "The conjunction or aspect should be close (say, within 6° or so)."
p149 Rajiv Gandhi: Sun+Jupiter 8° apart → weak yoga, became PM not emperor.
p149 Akbar: Venus+Saturn <1° apart → very strong yoga, became great emperor.
Linear decay: `1 - orb/15`. At exactly 6°: strength=0.60 (above 0.5 threshold).
At 8°: 0.467. Beyond 15°: 0.0. `is_pvrnr_close()` = True if ≤6°.

### Session 58 — Yoga fructification conditions + Amsa level
**File:** `src/calculations/yoga_fructification.py`  
Source: PVRNR p147-148. Three conditions explicitly listed by PVRNR (p147):
"(1) The two planets should be free from afflictions from functional malefics.
(2) The conjunction should be close (say, within 6°).
(3) The two planets should not be combust, debilitated or in an inimical house."
Amsa level from p64+148: Dasa Varga = D1,D2,D3,D7,D9,D10,D12,D16,D30,D60.
Count how many the planet occupies own/exalt/mooltrikona. p148 example:
Akbar's Venus+Saturn in Uttamaamsa+Paarijataamsa → Simhasanamsa level combined.
DivisionalMap uses attribute access (`getattr(div, 'D9')`), not dict access.

### Session 59 — Stronger-of-two planet/rasi framework
**File:** `src/calculations/stronger_of_two.py`  
Source: PVRNR p194 (Rudra calculation). PVRNR gives exact hierarchy:
"We say that a planet is stronger if it conjoins more planets. If both conjoin
the same number, a planet in exaltation or own rasi is stronger. A planet
joining exalted planets is stronger. A planet aspected by many planets (rasi
aspect) is stronger. Finally, a planet which is more advanced in its rasi is
stronger." India 1947: Sun in Cancer with 4 cotenants (Moon/Mercury/Venus/Mars).

### Session 60 — AV-weighted transit
**File:** `src/calculations/av_transit.py`  
Source: PVRNR p154: "If we can judge benefic positions with respect to 8 references
in rasi chart, there is no reason why we should not do it in all divisional charts.
This becomes invaluable when interpreting transits." SAV thresholds from p165:
≥30 rekhas = strong house (D-10 lagna of Vajpayee=35 rekhas). SAV=33 in H8
"explains the struggle in Vajpayee's career."

### Session 61 — Arudha reality vs perception model
**File:** `src/calculations/arudha_perception.py`  
Source: PVRNR Ch.9 p97-104. p97: "Usually, how one is perceived by others is
more important in material life than who one really is." p103 vehicle example:
"Venus in own sign in A4 + Saturn in H4 → luxurious vehicle (perceived happy)
but not actually happy. Saturn in A4 + Venus/Jupiter in H4 → small vehicle
(perceived unhappy) but happy with it." p102: malefics 3rd/6th from AL =
"perceived as bold person who hits enemies hard — usually materially successful."

### Session 62 — PVRNR textbook yogas
**File:** `src/calculations/yogas_pvrnr.py`  
Source: PVRNR Ch.11 p125-130. Key additions:
- Jaya Yoga (p129): requires 10th lord in DEEP exaltation + 6th lord debilitated.
  Checks exact degree proximity to deep exaltation point per planet.
- Brahma Yoga (p130): requires Jupiter in kendra from 9th lord AND Venus in kendra
  from 11th lord AND Mercury in kendra from lagnesh/10th lord — all three conditions.
- Amala Yoga checks both lagna and Moon references (p125 explicitly says "from lagna or Moon").

### Session 63 — Planet effectiveness synthesis
**File:** `src/calculations/planet_effectiveness.py`  
Source: PVRNR Ch.15 p201. PVRNR's caution: "Attempting to use various techniques
in an interchangeable manner only leads to confusion. One should strive to
understand the meanings of various parameters and use the right set for the occasion."
This module provides a summary view only — explicit documentation in docstring
warns against substituting it for specific-purpose strength computations.
Weights derived from PVRNR's emphasis ordering: Avastha and Shadbala highest
(most discussed in Ch.15), AV/Dig/Amsa moderate, penalties lowest.
