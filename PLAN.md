# LagnaMaster — Programme Plan

## Status: Sessions 1–100 COMPLETE ✅ | Sessions 101–108 in progress on remote 🔄

ENGINE_VERSION = "3.0.0"

> **Source of truth:** Classical Sanskrit texts — BPHS (PVRNR), Phaladeepika (Mantreswara),
> Saravali (Kalyanarma), Brihat Jataka (Varahamihira), Jaimini Sutras.
> The Excel workbook (`Lagna_Master5_clean.xlsx`) was the prototype source for Sessions 1–56.
> It has been superseded by classical text references from Session 57 onward and is no longer
> authoritative. See `AUDIT.md` for the full classical audit.

---

## Phase 0 — Classical Correctness (Sessions 101–108) 🔄

**Committed on remote 2026-03-21. Run `git pull` to get these changes.**

Fixes identified by the March 2026 classical audit against primary Sanskrit authorities.
Every fix has a cited śhloka. No new features — correctness only.

| Issue | Fix | Source |
|-------|-----|--------|
| MT degree ranges approximate | Hard-code exact BPHS ranges; Mercury 16°–20° Virgo (4° window only) | BPHS Ch.3 v.2–9 |
| Exaltation binary flag | Add Paramotcha degrees; Uchcha Bala = `60×(1−\|deg−paramotcha\|/30)` | Phaladeepika Ch.2 v.4–7 |
| Rahu/Ketu NEUTRAL in all signs | Implement exaltation per BPHS school (Rahu: Taurus, Ketu: Scorpio) | BPHS Ch.3 |
| Neecha Bhanga: 1 of 6 conditions | Implement all 6 as separate booleans; NEECHA_BHANGA_RAJA when ≥2 | BPHS Ch.49 v.12–18 |
| WC-halving (0.5×) non-classical | Replace with BPHS ¾-strength for Mars/Jupiter/Saturn special aspects | BPHS Ch.26 v.3–5 |
| Nakshatra index: `int(lon/13.333)` | Use `int(lon*3/40)` — exact integer arithmetic | Swiss Ephem. precision |
| AV Trikona Shodhana missing | Implement reduction; raw bindus are meaningless for prediction | PVRNR AV System Ch.4 |
| AV Ekadhipatya Shodhana missing | Implement dual-lordship reduction | PVRNR AV System Ch.5 |
| Kala Bala: 7 of 8 sub-components missing | Add Vara, Hora, Tribhaga, Abda, Masa, Nathonnata, Ayana | BPHS Ch.27 v.30–62 |
| Drik Bala = 0 in all charts | Implement aspect-sum across all planet pairs | BPHS Ch.27 v.22–29 |
| Single regression fixture | Add 8 new fixtures: Neecha Bhanga, Graha Yuddha, nakshatra cusp, Parivartana, female chart, high-latitude, year-boundary, celebrity | BV Raman Notable Horoscopes |
| No JHora cross-validation | Add `cross_validate.py` — diff all fields vs JHora CSV export | Jagannatha Hora 8.0 |

---

## Phase 15–18 — Muhurta, Prashna, Additional Dashas, Upaya, Mundane (Sessions 91–100) ✅

### Session 91 — Panchanga (5 limbs of the almanac)
**File:** `src/calculations/panchanga.py`
Complete Panchanga engine replacing the incomplete predecessor `panchang.py`.
Tithi, Vara, Nakshatra, Yoga, Karana (7 variable + 4 fixed karanas).
Amrita Siddhi and Sarvaartha Siddhi from Vara×Nakshatra lookup tables.
Hora (planetary hour from sunrise) and Choghadiya (8 day/8 night periods).
Added `compute_navamsha_chart()` and `_d9_sign_index()` for backward compatibility.
Note: supersedes `panchang.py`; `test_panchanga_legacy.py` is an empty stub.

### Session 92 — Muhurta Engine
**File:** `src/calculations/muhurta.py`
Source: PVRNR Table 79 (p473–476). 7 task types: marriage, business_launch,
house_construction, house_entry, travel, surgery, education, general.
Per-task: good/bad Tithis, Varas, Nakshatras, Lagnas from Table 79.
Tarabala: count from birth nakshatra → 9 categories; {1,3,5,7} = auspicious.
Chandrabala: Moon's current sign from birth Moon sign; {1,3,6,7,10,11} = good.
`score_muhurta()` → 0–7: Excellent(≥5)/Good(≥4)/Acceptable(≥3)/Avoid.
PVRNR p487: "Planetary strength is more important than strictly following thumbrules."

### Session 93 — Prashna (Horary)
**File:** `src/calculations/prashna.py`
Source: BPHS Prashna chapters; Prashna Marga; PVRNR applications.
10 query types: general, lost_article, illness, travel, legal, marriage,
career, wealth, children, property.
Key house scoring + Moon placement + lagna lord placement → Yes/Possible/Unlikely/No.
Confidence: High/Moderate/Low based on positive signal count.

### Session 94 — Kalachakra Dasha
**File:** `src/calculations/kalachakra_dasha.py`
Source: BPHS Ch.36–42; PVRNR preface p8 ("most respectable dasha").
Moon's navamsha pada (0–3) determines Savya/Apasavya sequence.
Sign periods: Ar=7, Ta=16, Ge=9, Cn=21, Le=5, Vi=9, Li=16, Sc=7, Sg=10, Cp=4, Aq=4, Pi=1.
Deha (body) and Jeeva (life) flags per cycle. `current_kalachakra_period()` included.

### Session 95 — Shoola Dasha + Sudasa
**File:** `src/calculations/shoola_dasha.py`
Source: BPHS; PVRNR preface p8 ("two ayur dasas"; "timing material success").
Shoola: lagna-trine-based; Trishoola spikes.
Sudasa: starts from stronger of lagna/8th (using `stronger_of_two.py`).

### Session 96 — Tara Dasha
**File:** `src/calculations/tara_dasha.py`
9-category nakshatra sequence from birth nakshatra.
Vimshottari period lengths. Auspicious categories annotated.

### Session 97 — Upaya (Remedial Measures)
**File:** `src/calculations/upaya.py`
Source: PVRNR Ch.34 (p450–458), Tables 77–78.
`get_chart_upayas()`: auto-detects combust/debilitated/functional-malefic planets.
EVERY recommendation carries disclaimer: "classical prescriptions for reflection only."

### Session 98 — Mundane Astrology
**File:** `src/calculations/mundane.py`
Source: PVRNR Ch.35 (p460–469).
Chart types: nation, solar ingress, lunar new year, swearing-in.
`compress_vimshottari()`: scale 120yr cycle to any period (PVRNR p464).
India 1947 regression: nation chart analysis confirmed.

### Session 99 — Contextual Layer (partial DKP)
**File:** `src/calculations/contextual.py`
Era-aware profession mapping, latitude warning, marriage timing by birth era.
Explicit practitioner note: full Desha-Kala-Patra requires practitioner judgment.

### Session 100 — Ashtottari Dasha
**File:** `src/calculations/ashtottari_dasha.py`
Source: BPHS Ch.47; PVRNR preface p8.
8-planet sequence; total 108 years.
`qualifies_for_ashtottari()`: Rahu not in H1 or H7 required.

---

## Phase 9 — Synthesis & Judgment Layer (Sessions 64–70) ✅

### Session 64 — Dominance Hierarchy Engine
**File:** `src/calculations/dominance_engine.py`
Named classical overrides from BPHS: benefic kendra suppression, combust benefic yoga blocking, dasha lord activation weight.
`DominanceReport`: global_tone, affliction_dominated and yoga_dominated house lists.

### Session 65 — Promise vs Manifestation
**File:** `src/calculations/promise_engine.py`
Three-level: Promise (natal) → Capacity (dasha) → Delivery (transit).
Timing: Now / Soon / Future / Blocked.

### Session 66 — Domain-Specific Axis Weighting
**File:** `src/calculations/domain_weighting.py`
7 domains; classical varga weights per domain (PVRNR Ch.13 p181).
`compute_domain_lpi()` → `DomainLPIResult`.

### Session 67 — Multi-Planet Chains
**File:** `src/calculations/planet_chains.py`
Stelliums, dispositor chains (max depth 9), mutual reception (parivartana).
India 1947: Cancer stellium = 5 planets confirmed.

### Session 68 — House-Type Modulation
**File:** `src/calculations/house_modulation.py`
Upachaya age maturation (35/60+ year modifiers). Malefics beneficial in 3/6/10/11.
`apply_house_modulation(scores, chart, age_years)`.

### Session 69 — Interpretive Confidence Model
**File:** `src/calculations/confidence_model.py`
5 components: varga agreement (30%) / conflict (25%) / sensitivity (20%) / boundary (15%) / role clarity (10%).
`requires_expert_review` list for houses with Uncertain label or ≥3 flags.

### Session 70 — Chart Exception Detection
**File:** `src/calculations/chart_exceptions.py`
7 checks: empty kendras, lagnesh in H8, dusthana lords all strong, Moon severely afflicted,
multiple combust benefics, hemisphere imbalance, score extreme.
`special_rules_apply` names specific BPHS doctrines triggered.

---

## Phase 8 — PVRNR Textbook Tier 1 (Sessions 57–63) ✅

### Session 57 — Orb-sensitive conjunction/aspect strength
**File:** `src/calculations/orb_strength.py`
PVRNR p147/p149. Formula: `strength = max(0, 1 - orb / 15)`.
`is_pvrnr_close()` (≤6°), `reduces_yoga()` (>8°). Parivartana detected.

### Session 58 — Yoga fructification conditions
**File:** `src/calculations/yoga_fructification.py`
PVRNR p147 three conditions. Amsa levels: Paarijataamsa → Airaavataamsa.
`FructificationResult`: Full/Partial/Weak/Minimal.

### Session 59 — Stronger-of-two framework
**File:** `src/calculations/stronger_of_two.py`
PVRNR p194 explicit 5-condition hierarchy.
Used for: Scorpio/Aquarius dual lords, Narayana Dasha start, longevity lords.

### Session 60 — AV-weighted transit interpretation
**File:** `src/calculations/av_transit.py`
PVRNR p154/p165. SAV ≥30=strong, <25=weak. BAV: ≥6/5/4/3/≤2.
`TransitAVReport` from `compute_transit_av_score()`.

### Session 61 — Arudha reality vs perception model
**File:** `src/calculations/arudha_perception.py`
PVRNR Ch.9 p97. 2×2 matrix: actual × perceived strength.

### Session 62 — PVRNR textbook yogas
**File:** `src/calculations/yogas_pvrnr.py`
8 yogas from PVRNR Ch.11: Guru-Mangala, Amala, Sankha, Vasumati,
Lagnaadhi, Jaya, Pushkala, Brahma.

### Session 63 — Multi-factor planet effectiveness
**File:** `src/calculations/planet_effectiveness.py`
7 measures → 0.0–1.0: Shadbala 20% / Avastha 20% / AV 15% / Dig Bala 15% / Amsa 15% / Combustion 7.5% / Yuddha 7.5%.

---

## Phase 7 — Workbook Completeness (Sessions 49–56) ✅

### Session 49 — Full 12-state Sayanadi
**File:** `src/calculations/sayanadi_full.py`
All 12 states including 5 decanate-based. Priority chain with modifiers.
Deena wired from `graha_yuddha.py`. Source: BPHS Ch.45–47.

### Session 50 — Panchadha Maitri wired to scoring
**File:** `src/calculations/panchadha_maitri.py`
Tatkalik + Naisargika → 5-fold: Adhi Mitra(+1.0)→Adhi Shatru(−1.0).
`compute_panchadha_matrix(chart)` returns full 7×7 `PanchadhaMatrix`.

### Session 51 — Lagnesh Global Modifier
**File:** `src/calculations/lagnesh_strength.py`
9-condition lookup; modifier −0.75 to +0.75 applied to ALL 12 house scores.

### Session 52 — Dig Bala Continuous Score
**File:** `src/calculations/dig_bala.py`
Replaces binary with 0.0–1.0. Formula: `1 − circular_dist(current, peak) / 6`.
All 7 workbook values verified.

### Session 53 — Graha Yogas
**File:** `src/calculations/yogas_graha.py`
4 missing + 2 confirmations: Budhaditya, Saraswati, Chandra-Mangal, Kahala, Parvata, Gaja Kesari.

### Session 54 — Narayana Dasha Argala (ND-6)
**File:** `src/calculations/narayana_argala.py`
PVRNR Ch.5. Argala positions H2/H4/H11/H5(×0.5). Virodha cancellations.
Net modifier −0.5 to +0.5.

### Session 55 — Configuration Toggles
**File:** `src/calculations/config_toggles.py`
Ayanamshas: Lahiri/Raman/Krishnamurti/Fagan-Bradley. Node: mean/true.
Retrograde policy: apply ±0.10 / ignore / classical full-strength.
`CalcConfig` with `to_dict()`/`from_dict()`.

### Session 56 — Varga Agreement Confidence Flag
**File:** `src/calculations/varga_agreement.py`
★★/★/○ confidence per house from D1/D9/D10 agreement.
India 1947 H2 Wealth: D1=−5.25, D9=−2.0, D10=−2.5 → ★★ confirmed.

---

## Phases 1–6 (Sessions 1–48) ✅

| Phase | Sessions | Key Work |
|-------|----------|----------|
| 1 | 1–10 | `ephemeris.py`, 7 core modules, scoring, FastAPI, SQLite |
| 2 | 11–20 | Streamlit UI, Docker, JWT, PostgreSQL migration, K8s Helm |
| 3 | 21–27 | GitHub Actions CI/CD, Streamlit Cloud deploy, 200+ yoga library |
| 4 | 28–32 | `functional_roles.py`, `avastha.py`, `pressure_engine.py`, `argala.py`, `graha_yuddha.py` |
| 5 | 33–40 | 5-axis LPI, Scoring v2/v3, `multi_axis_scoring.py`, rule interactions |
| 6 | 41–48 | Ishta/Kashta Bala, longevity calc, Yogini Dasha, KP school, Empirica router |

---

## Consumer Product Vision

**Product:** Personal Timing & Guidance Companion
**Aesthetic:** Bloomberg Terminal — professional, data-dense, calm, no mysticism
**Core constraint:** Raw scores permanently gated behind L3 opt-in
**Signal system:** 5-bar (mobile-signal style)
**Language:** Possibility framing, not deterministic claims

**Consumer readiness (Session 100):**

| Layer | Status |
|-------|--------|
| Jyotish engine (natal) | ✅ Complete (63 modules, 963 tests) |
| All dasha systems | ✅ Complete |
| Muhurta / Prashna | ✅ Complete (Sessions 91–93) |
| Upaya / Mundane | ✅ Complete (Sessions 97–98) |
| Language & safety pipeline | ✅ Complete (Sessions 71–75) |
| Privacy & legal (GDPR/DPDP) | ✅ Complete (Sessions 76–78) |
| Consumer frontend (Next.js) | ✅ Built — integration testing pending |
| Feedback governance | ✅ Complete (Sessions 84–86) |
| Mobile API | ✅ Router built — React Native shell pending |
| Phase 0 classical correctness | 🔄 Sessions 101–108 on remote |

**Remaining to production:**
1. End-to-end integration testing: Next.js ↔ FastAPI ↔ guidance pipeline
2. React Native mobile shell (router complete at S90)
3. Practitioner opt-in directory (S89 infrastructure ready)
4. GDPR privacy policy and ToS text (legal team)
5. First 50 empirica events for accuracy baseline (S48 router ready)

---

## Genuine Theoretical Limits (Correctly Excluded)

| Item | Reason |
|------|--------|
| Kalachakra Dasha (all textual variants) | Contradictory across commentators; BPHS version implemented |
| Desha-Kala-Patra (full) | Requires practitioner situational judgment |
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
5. **Jaimini Sutras** — with Sanjay Rath commentary (Sagittarius Publications)
6. Modern: BV Raman · K.N. Rao · Sanjay Rath · Hart de Fouw & Robert Svoboda · Gayatri Devi Vasudev

The Excel workbook is not a source. It was a prototype input for Sessions 1–56 only.
