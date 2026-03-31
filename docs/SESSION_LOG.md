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

---

## Phase 9 — Synthesis & Judgment Layer (Sessions 64–70)

### Session 64 — Dominance Hierarchy Engine
**File:** `src/calculations/dominance_engine.py`
Classical rules specifically encoded (NOT gestalt):
(1) Jupiter in kendra aspects H1/5/7/9 from its position — suppresses mild negatives
    in those houses if Jupiter is not combust. (BPHS Ch.34)
(2) Combust benefics: `is_combust` flag from `dignity.py` → DominanceFactor with
    overrides list naming which yogas are neutralized. (BPHS Ch.3)
(3) Dasha priority: MD lord's house D1 score × 1.5 if in kendra/trikona.
    This is the "primary activation filter" PVRNR uses in chart readings.
Global tone from mean D1 score: >1.5=Positive, >0.5=Mixed Positive, >-0.5=Neutral,
>-1.5=Mixed Negative, else Negative.

### Session 65 — Promise vs Manifestation
**File:** `src/calculations/promise_engine.py`
Three-level model derived from PVRNR's chart reading approach:
Level 1 (Promise): D1 score threshold → promise_present, strength, ceiling.
  Score ≥3.0=Strong (ceiling 9.0), ≥1.5=Moderate (7.0), ≥0.5=Weak (5.0),
  ≥-0.5=Absent (3.0), <-0.5=Negated (1.0).
Level 2 (Capacity): MD or AD lord either rules the house or is in the house.
Level 3 (Delivery): AV SAV ≥28 rekhas for that house = transit supported.
India 1947: H2 Wealth score -5.25 → Negated promise, ceiling 1.0.

### Session 66 — Domain-specific axis weights
**File:** `src/calculations/domain_weighting.py`
Derived from PVRNR p181: "Use the correct divisional chart for the matter of interest."
"Suppose we are looking at happiness from a vehicle. D-16 is the best chart.
Suppose we are trying to analyze a criminal's psychology. D-30 is the best chart.
Suppose we are analyzing marriage. D-9 is the best chart."
For LPI which only has 5 axes (D1/Chandra/Surya/D9/D10), career weights D10 most
heavily because D-10 "shows one's true conduct in society" (PVRNR p102).
Marriage weights D9 most because "D-9 is for marriage as dharma" (p181).
Chandra Lagna given 40% for psychology because Moon = mind per naisargika karakas.

### Session 67 — Planet chains
**File:** `src/calculations/planet_chains.py`
India 1947 Cancer stellium verified: Sun(27.99°), Moon(3.98°), Mars(7.46°),
Mercury(13.67°), Venus(22.56°), Saturn(20.47°) — 6 planets in Cancer.
Rahu/Ketu in Aries/Libra. Jupiter in Libra. Only Rahu/Ketu/Jupiter outside Cancer.
Dispositor chain example: Jupiter in Libra → Venus (Libra lord) in Cancer →
Moon (Cancer lord) in Cancer → Moon self-disposed (own sign Cancer). Length=3.
Mutual reception check: any planet A in sign owned by planet B AND B in sign owned by A.
India 1947: no mutual reception (Jupiter/Venus not in each other's own signs).

### Session 68 — House-type modulation
**File:** `src/calculations/house_modulation.py`
BPHS upachaya doctrine: "Natural malefics in the 3rd and 6th houses from AL show
someone perceived as a bold person who hits enemies hard. Since such impressions
are usually formed about materially successful people, malefics in the 3rd and 6th
from AL make one bold and materially successful." (PVRNR p102)
General BPHS principle: malefics in H3/H6/H11 (upachayas) are beneficial.
Age modifier for upachayas based on PVRNR's statements about these houses
improving with persistence and effort over time (explicit in several chart readings).

### Session 69 — Confidence model
**File:** `src/calculations/confidence_model.py`
India 1947 H2 Wealth: D1=−5.25, D9=−2.0, D10=−2.5 → all negative → ★★ (varga
agreement component = 1.0). Score boundary = |−5.25|/2 = 1.0 (capped). Very
high confidence this house is genuinely challenging.
H1 Self: D1=+1.25, D9=−1.35, D10=−1.9 → ○ diverge (va_score=0.30). Lower
confidence — mixed varga signals.

### Session 70 — Chart exception detection
**File:** `src/calculations/chart_exceptions.py`
India 1947 chart: massive Cancer stellium triggers no "exception" by itself
(stelliums detected in planet_chains.py, not here). The exception module checks
for structural conditions (empty kendras, lagnesh in 8th, etc.).
India 1947: Jupiter in H6 (Libra), Mars in H2 (Gemini), no planets in H1/H7/H10.
H4 Cancer has 6 planets. H1 is empty but some kendras have planets (H4=✓, H6=near).
No "empty kendras" exception fires because H4 (Cancer) is occupied.
Combust check: Venus 22.56° + Saturn 20.47° both in Cancer with Sun 27.99° —
Venus within combust orb of Sun (5.43°, standard orb 10°), Venus IS combust.

---

## Consumer Product Vision (March 2026)

### Design review: Sessions 71–90 roadmap

Approved product direction following architectural review against GPT product design spec.

**Readiness gap analysis (Session 70 baseline):**
Engine computation layer: ~100% complete.
Language/safety layer: ~0% — blocking consumer launch.
Privacy/legal: ~15% — blocking consumer launch.
Consumer frontend: ~10% (Streamlit analyst tool exists; Bloomberg consumer UI does not).
Feedback governance: ~20% (empirica event log exists; human review queue does not).
Overall consumer readiness: ~25%.

**Critical architectural decision confirmed:**
Raw LPI and house scores must be permanently gated behind L3 opt-in.
Engine modules are never called directly from consumer-facing endpoints.
All consumer traffic passes through the four-stage guidance pipeline.
This single constraint eliminates the largest category of psychological harm risk.

**Four blocking gaps before any external user sees the product:**
1. score_to_language.py + fatalism_filter.py (S71, S72)
2. explainability_tiers.py (S73)
3. GDPR/DPDP consent and deletion flows (S76)
4. Bloomberg-style consumer frontend (S79–S83)

**Score-to-language mapping rationale:**
A user who sees "−4.2" next to Wealth receives a potential psychological harm.
The 5-bar signal system (inspired by mobile signal strength indicators) communicates
direction without inviting numerical comparison, obsession, or fatalism.
"Navigate carefully" preserves the signal while removing the catastrophe framing.

**Fatalism filter rationale:**
The engine produces technically correct output. "8th house affliction" is a valid
classical descriptor. But presented verbatim to a consumer, it produces fear, not
insight. The filter is not whitewashing — it preserves signal direction while
removing determinism. "Significant resistance in health area" and "health crisis
indicated" carry the same actionable meaning; only the second causes harm.

**Dependency prevention rationale:**
Jyotish is traditionally a tool for self-understanding and dharma alignment, not
compulsive fate-checking. The product actively discourages overuse: no streaks,
no badges, no unsolicited notifications, session frequency caps, and an explicit
philosophy statement in onboarding that guidance is most useful when combined with
personal judgment and trusted advisors.

**Family consent rationale:**
Computing compatibility scores for a person who has not consented to use the platform
is a privacy violation regardless of the consenting party's intentions.
Each family member is a separate consent principal. Non-consenting members are
excluded from all analysis. The Kundali Milan engine exists but is gated.

**Practitioner handoff rationale:**
The confidence model (S69) already produces "requires expert review" flags.
For these cases, the platform should not attempt to answer — it should connect the
user to a verified Jyotish practitioner. LagnaMaster is the tool; the practitioner
is the expert. This boundary preserves human dignity and avoids overreach.

---

## Final State — Sessions 1–90 (March 2026)

### Summary

All 90 sessions complete. ~980 tests passing. 0 failures.

The platform has two complete layers:

**Jyotish Engine (Sessions 1–70)**
63 calculation modules covering the full classical corpus:
BPHS, PVRNR textbook, Jaimini, KP, Tajika, all standard and extended yogas,
Vimshottari + Narayana + Yogini + Yogini Dasha, LPI with 7-layer weighting,
dominance hierarchy, promise/manifestation model, domain-specific axis weights,
planet chains, house modulation, confidence model, exception detection.

**Consumer Product Layer (Sessions 71–90)**
14 modules across guidance, privacy, and feedback packages.
Key: raw scores never reach consumers; fatalism filter on all output;
GDPR Art.7+17 compliant; per-person family consent; human-supervised feedback.

### Phase 10 fix log (Session 90 + hotfix)

`dependency_prevention.py` date comparison bug: `datetime('now')` in SQLite
stores UTC; `date.today()` returns local (IST = UTC+5:30). Fix: store
`datetime.now()` (local), compare with `started_at LIKE 'YYYY-MM-DD%'`
prefix match. Tests: 60/60 after fix.

### mobile_router wiring

`main_v2.py` did not contain the `empirica_router` import pattern used as
the insertion anchor. Mobile router manually appended:
```python
from src.api.mobile_router import router as mobile_router
app.include_router(mobile_router)
```

### Readiness assessment (final)

| Dimension | Status |
|-----------|--------|
| Jyotish classical coverage | Complete — all CALC_ sheets implemented |
| Consumer language safety | Complete — 5-tier signal + fatalism filter |
| GDPR / DPDP / CCPA | Complete — consent + erasure + minimisation |
| Consumer frontend | Components built — integration testing pending |
| Feedback governance | Complete — human-supervised queue |
| Dependency prevention | Complete — session monitor + nudge |
| Educational / reflective | Complete — learn mode + Socratic prompts |
| Practitioner handoff | Complete — sanitised summary + referral logic |
| Mobile API | Complete — L1-only router, user-scheduled alerts |
| Theoretical limits | Documented — Kalachakra, DKP, gestalt synthesis |

---

## Phase 15–18 (Sessions 91–100) — Muhurta, Prashna, Additional Dashas, Upaya, Mundane

### Fix log

**panchanga.py name collision:**
Original `panchang.py` (Phase 2) was superseded by the new `panchanga.py`.
`test_panchanga.py` → renamed `test_panchanga_legacy.py` → replaced with empty stub.
Root cause: `panchang.py` no longer exists; its functions were rewritten in `panchanga.py`.
Added `compute_navamsha_chart()` and `_d9_sign_index()` to `panchanga.py` for
backward compatibility with `multi_axis_scoring.py` and `test_varga.py`.

**DivisionalMap subscript errors:**
`DivisionalMap` is a dataclass with `planets: dict[str, dict[str, int]]` and
`lagna: dict[str, int]`. It is NOT subscriptable and has no `.get()`.
Fixed in `multi_lagna.py` (ak_d9_si), `longevity.py` (d9.get(planet)),
`multi_axis_scoring.py` (d9_map.get("lagna", 0) → lagna_sign_index directly),
`test_varga.py` (nav["lagna"] → valid range assert).

**Bandhu Yoga scope error:**
Bandhu Yoga block was inserted outside function scope (0-indent) by earlier fix script.
Then re-inserted inside function but BEFORE `ak_planet` was defined (which it never was).
Final fix: self-contained block that computes its own AK from `compute_chara_karakas()`
inside a try/except. No reliance on outer scope variable.

**jaimini_full.py function deletion:**
Regex `re.sub` with DOTALL flag accidentally deleted `compute_karakamsha_scores()`,
`compute_jaimini_longevity()`, and `pada_relationship_score()` functions.
Restored from `git show b19b218:src/calculations/jaimini_full.py`.

### Session 91 — Panchanga
India 1947 verified: Sun at 117.99° (Cancer), Moon at 93.98° (Cancer).
Moon-Sun diff = -24° → adjusted to 336° → tithi = 29 (Krishna Chaturdashi).
Nakshatra: 93.98 × 27/360 = 7.05 → Pushya (index 7). ✓

### Session 94 — Kalachakra
India 1947: Moon at 93.98° → nak_idx = 7 (Pushya), pada 0.
Pushya group index 1 → savya sequence. Start sign: Cn (Cancer).
Periods from Cancer: 21yr → Sg: 10yr → Cp: 4yr → Aq: 4yr → Pi: 1yr → ...

### Session 97 — Upaya
India 1947: Jupiter at 205.88° (Libra) → enemy sign → Kshuditha avastha.
Venus at 112.56° → within Sun combust orb → Kopa.
Both appear in get_chart_upayas() output with disclaimers.

### Final state at Session 100
963 tests passing, 2 skipped (legacy panchanga stub), 0 failures.
All previously documented exclusions (Kalachakra, Muhurta, Prashna, Upaya, Mundane)
are now implemented. Remaining genuine limits:
- Full Prashna Marga horary corpus (requires separate source text)
- Medical/financial astrology as distinct disciplines
- Complete Desha-Kala-Patra (not parameterisable)


### Session S187 — Scoring Pipeline Wiring
- `multi_axis_scoring.py`: Graha Yuddha war loser −1.5 bhavesh penalty
  (Saravali Ch.4 v.18-22)
- `scoring_v3.py`: `score_chart_with_dasha()` stub → real dasha-sensitized
  implementation; `strict_school` param wired to `score_axis()`
- Commit: `0b1a17d`

### Session S188 — XIX Output API + Postgres Routing
- New FastAPI endpoints: `POST /charts/{id}/svg`, `POST /charts/{id}/pdf`,
  `POST /charts/{id}/guidance`, `GET /charts/{id}/confidence`,
  `GET /charts/{id}/scores/v3`
- `src/db_pg.py`: Postgres routing with SQLite fallback (`PG_DSN` env var)
- New Pydantic models: SVGRequest, SVGOut, GuidanceRequest, GuidanceOut,
  ConfidenceOut, ChartV3Out, MundaneRequest, MundaneOut
- `weasyprint>=60.0` added to requirements
- Commit: `feat(S188)`

### Session S189 — ADB XML Importer + Diverse Fixtures + Streamlit UI
- `tools/adb_xml_importer.py`: Official ADB XML export parser (replaces Playwright
  scraper); uses `jd_ut` from `<sbtime>` directly — no timezone guesswork;
  5,063 charts computed from c_sample.zip (0 errors)
- `tests/fixtures/diverse_chart_fixtures.py`: Sections B-H added — Neecha Bhanga,
  Graha Yuddha, Parivartana, Kemadruma, Nakshatra boundary, High-latitude, Female
- `POST /mundane/analyze` endpoint wired
- `ephe/semom_18.se1` (BC Moon) downloaded
- `src/ui/app.py`: Streamlit 4-tab UI — SVG, Scores, Confidence, Guidance
- Commits: `2caea96`, `87c48ba`

### CI Guard Session (March 22 2026)
Root cause of 103 CI failures identified and fixed:

**Lint (ruff)**: 732 errors → 0
- `ruff format` on 203 files; `--unsafe-fixes` for F401; manual `# noqa` for
  intentional late imports and re-exports

**CI workflow**: trailing `\` after `exit $STATUS` → `exit: too many arguments`
- Removed stray continuation character; tests were passing but CI reported failure

**Infrastructure installed**:
- `.git/hooks/pre-push`: runs pytest locally before every push
- `tools/ci_watch.py`: fetches CI failures to local terminal via `gh run view`
- `tools/setup_ci_guard.py`: one-shot installer for both tools

**Final numbers**: 1338 passed, 3 skipped | ruff: 0 errors | CI: green
104 historical failed runs deleted.

---

## Phase 0 — Guardrails & Infrastructure (Sessions 191–215)

### Session 193 — HouseScore Distribution Dataclass
**Files:** `src/calculations/house_score.py`, `tests/test_s193_housescore_distribution.py`
- `HouseScore` dataclass: `house`, `score`, `mean`, `std`, `p10`, `p90` + `to_dict()`
- `compute_house_scores(chart, school)` → `dict[int, HouseScore]` via D1 axis scoring
  and confidence-interval propagation (birth-time uncertainty ±5 min)
- `ChartScoresV3.house_distributions` field added (backward-compat, populated by
  `score_chart_v3()`)
- Invariant #37: `p10 ≤ mean ≤ p90` enforced by construction (normal-distribution
  percentile derivation from 95 % CI width)
- 6 new tests (fields, JSON serialisation, distribution ordering, dict shape,
  India 1947 H2-negative regression)
- **1484 → 1490 passing**

### Session 194 — Conditional Weight Functions W(planet, house, lagna, functional_role)
**Files:** `src/calculations/conditional_weights.py`, `tests/test_s194_conditional_weights.py`
- `WeightContext` dataclass: `planet`, `house`, `lagna_sign`, `functional_role`,
  `rule_id`, `school`, `base_weight`, `ayanamsha`
- `W(ctx: WeightContext) -> float` with classical modifiers:
  - Yogakaraka early-return × YK_MULT (1.5 Parashari/KP, 1.25 Jaimini) — BPHS Ch.34
  - Functional benefic + positive rule × 1.2 (amplifies promise) — Phaladeepika Ch.3
  - Functional malefic + negative rule × 1.2 (amplifies affliction)
  - Role mismatch × 0.75 (cross-direction mitigation) — Systems Approach Ch.3
  - Kendra/Trikona + positive rule × 1.1 — BPHS Ch.11
  - Dusthana + negative rule × 1.1 — BPHS Ch.37
- `g06_compliant` property: KP school requires Krishnamurti ayanamsha (G06)
- `build_context()` convenience constructor
- Invariants #38 (yogakaraka early-return) + #39 (neutral/non-special → exact passthrough)
- Ready for Phase 2 engine rebuild — not yet wired into live scoring
- 13 new tests; **1490 → 1503 passing**

## Phase 1B — Sutra-Level Corpus Encoding (Sessions 263–305+)

### Sessions 263–266 — Schema + Laghu Parashari
**Files:** `docs/PHASE1B_RULE_CONTRACT.md`, `docs/PHASE1B_OUTCOME_TAXONOMY.md`, `docs/PHASE1B_CONCORDANCE_WORKFLOW.md`, `src/corpus/laghu_parashari_*.py`
- S263: Schema definition — Rule Contract, Outcome Taxonomy, Coverage Map, Concordance Workflow
- S264: Laghu Parashari Functional Nature Table — LPF001-108 (9×12 matrix)
- S265: Laghu Parashari Sections B, C, D — LPY/LPK/LPD (81 rules)
- S266: Laghu Parashari Sections E, F — LPA/LPM coverage complete

### Sessions 267–272 — Bhavartha Ratnakara (COMPLETE)
**Files:** `src/corpus/bhavartha_ratnakara_1.py` through `bhavartha_ratnakara_6.py`
- S267: Aries + Taurus — BVR001-130
- S268: Gemini + Cancer — BVR131-260
- S269: Leo + Virgo — BVR261-390
- S270: Libra + Scorpio — BVR391-520
- S271: Sagittarius + Capricorn — BVR521-650
- S272: Aquarius + Pisces — BVR651-780 (ALL 12 LAGNAS COMPLETE)
- 780 rules total, 65 per lagna, phase=1B_conditional, lagna_scope populated

### Sessions 273–280 — Saravali Block A: Conjunctions (COMPLETE)
**Files:** `src/corpus/saravali_conjunctions_1.py` through `saravali_conjunctions_8.py`
- S273: Sun-Moon, Sun-Mars, Sun-Mercury — SAV001-130
- S274: Sun-Jupiter, Sun-Venus, Sun-Saturn — SAV131-260
- S275: Moon-Mars, Moon-Mercury, Moon-Jupiter — SAV261-390
- S276: Moon-Venus, Moon-Saturn, Mars-Mercury — SAV391-520
- S277: Mars-Jupiter, Mars-Venus, Mars-Saturn — SAV521-650
- S278: Mercury-Jupiter, Mercury-Venus, Mercury-Saturn — SAV651-780
- S279: Jupiter-Venus, Jupiter-Saturn, Venus-Saturn — SAV781-910
- S280: Three+ planet conjunctions, special conditions — SAV911-1040
- 1,040 rules total, phase=1B_compound, lagna_scope=[] (universal)

### Sessions 281–288 — Saravali Block B: Planet-in-Sign (COMPLETE)
**Files:** `src/corpus/saravali_signs_1.py` through `saravali_signs_8.py`
- S281: Sun in 12 signs (Ch.25) — SAV1041-1170 (130 rules)
- S282: Moon in 12 signs (Ch.26) — SAV1171-1300 (130 rules)
- S283: Mars in 12 signs (Ch.27) — SAV1301-1430 (130 rules)
- S284: Mercury in 12 signs (Ch.28) — SAV1431-1560 (130 rules)
- S285: Jupiter in 12 signs (Ch.29) — SAV1561-1702 (142 rules)
- S286: Venus in 12 signs (Ch.30) — SAV1703-1861 (159 rules)
- S287: Saturn in 12 signs (Ch.31) — SAV1862-2002 (141 rules)
- S288: Rahu/Ketu in 12 signs (Ch.32-33) — SAV2003-2132 (130 rules)
- 1,092 rules total, phase=1B_matrix, rule counts driven by text depth

### Sessions 289–296 — Saravali Block C: Planet-in-House (COMPLETE)
**Files:** `src/corpus/saravali_houses_1.py` through `saravali_houses_8.py`
- S289: Sun in 12 houses (Ch.34) — 68 rules
- S290: Moon in 12 houses (Ch.35) — 60 rules
- S291: Mars in 12 houses (Ch.36) — 57 rules
- S292: Mercury in 12 houses (Ch.37) — 57 rules
- S293: Jupiter in 12 houses (Ch.38) — 60 rules
- S294: Venus in 12 houses (Ch.39) — 56 rules
- S295: Saturn in 12 houses (Ch.40) — 57 rules
- S296: Rahu/Ketu in 12 houses (Ch.41-42) — 81 rules
- 496 rules total, phase=1B_matrix

### Sessions 297–305 — Saravali Block D: Special Topics (COMPLETE)
**Files:** `src/corpus/saravali_special_1.py` through `saravali_special_9.py`
- S297: Planet natures, signs, houses (Ch.1-5) — 45 rules
- S298: Longevity, Arishta, Ayurdaya (Ch.6-8) — 32 rules
- S299: Raja Yogas, Ava Yogas (Ch.9-10) — 30 rules
- S300: Nabhasa/Solar/Lunar/Chandra Yogas (Ch.11-14) — 38 rules
- S301: Bhava effects detailed (Ch.43-48) — 30 rules
- S302: Female horoscopy, Marriage, Progeny (Ch.49-53) — 28 rules
- S303: Dasha results, AV, Transits (Ch.54-60) — 23 rules
- S304: Death, Lost horoscopy, Drekkana (Ch.61-65) — 20 rules
- S305: Nimitta, Planetary war, Summary (Ch.66-68) — 24 rules
- 270 rules total, phase=1B_matrix
- **SARAVALI COMPLETE: 2,898 rules across all 68 chapters**

### BPHS Phase 1B Re-encode (S306–S340)
- S306: Ch.12-15 (1st-4th House Effects) — 82 rules (BPHS0001-BPHS0382)
  - Ch.12 Tanu Bhava: 23 rules, Ch.13 Dhana Bhava: 14 rules
  - Ch.14 Sahaj Bhava: 19 rules, Ch.15 Sukha Bhava: 26 rules
  - 61% concordance populated, 25 high-confidence rules (>=0.81)
  - Coverage map: 85/218 Block A predictive slokas encoded
- S307: Ch.16-19 (5th-8th House Effects) — 75 rules (BPHS0400-BPHS0719)
  - Ch.16 Putra Bhava: 24 rules, Ch.17 Ari Bhava: 14 rules
  - Ch.18 Yuvati Bhava: 18 rules, Ch.19 Randhra Bhava: 19 rules
  - 55% concordance, Option B modifier protocol, coverage map 160/218
- S308: Ch.20-23 (9th-12th House Effects) — 63 rules (BPHS0800-BPHS1110)
  - Ch.20 Dharma Bhava: 22 rules (fortune, father, dharma, timing)
  - Ch.21 Karma Bhava: 19 rules (career, fame, deeds, patronage)
  - Ch.22 Labha Bhava: 11 rules (gains, Nishka timing, exchanges)
  - Ch.23 Vyaya Bhava: 11 rules (expenses, moksha, foreign, wandering)
  - 33% concordance, Block A (Ch.12-23) COMPLETE: 223/249 predictive slokas
  - Sloka counts corrected from actual reading (Ch.20 has 32 slokas, not 13)
