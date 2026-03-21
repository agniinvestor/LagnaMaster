# Changelog

Reverse-chronological. Format: `[Session N] — YYYY-MM — brief title`

---

## [Classical Audit] — 2026-03-21

Independent classical audit against BPHS, Phaladeepika, Saravali, Brihat Jataka,
Jaimini Sutras completed. 19 domains, 60+ MECE issues, all cited to classical śhloka.

Key findings:
- Scoring engine is a heuristic — additive weights are non-classical (documented as design fact)
- MT degree ranges approximate; Mercury MT only 16°–20° Virgo (critical)
- Exaltation binary flag should be Paramotcha gradient
- Rahu/Ketu assigned NEUTRAL — wrong under all schools
- Only 1 of 6 Neecha Bhanga conditions implemented
- WC-halving (0.5×) non-classical; BPHS says ¾-strength for special aspects
- Nakshatra index float error (`13.333` truncated); use `int(lon*3/40)`
- AV Shodhana reductions both missing; all transit quality scores wrong
- Single regression fixture (India 1947) — extreme outlier; many rules untested

Published: `AUDIT.md`, `LagnaMaster_Classical_Audit_v2.docx`
Updated: `README.md`, `PLAN.md`, `docs/MEMORY.md`, `CHANGELOG.md`
Phase 0 fixes: Sessions 101–108 (committed on remote)

---

## [Session 100] — 2026-03

**Ashtottari Dasha**
- `src/calculations/ashtottari_dasha.py` — 108yr, 8 planets (no Ketu)
- `qualifies_for_ashtottari()` — Rahu not in H1/H7 required
- Sessions 1–100 complete. Engine v3.0.0. 963 tests.

## [Session 99] — 2026-03

**Contextual Layer (partial DKP)**
- `src/calculations/contextual.py`
- Era-aware profession mapping; latitude warning; explicit practitioner note

## [Session 98] — 2026-03

**Mundane Astrology**
- `src/calculations/mundane.py` — PVRNR Ch.35
- Nation/ingress/swearing-in chart types; `compress_vimshottari()`
- India 1947 nation chart regression confirmed

## [Session 97] — 2026-03

**Upaya (Remedial Measures)**
- `src/calculations/upaya.py` — PVRNR Tables 77–78
- `get_chart_upayas()`: auto-detect combust/debilitated/functional-malefic planets
- Every recommendation carries disclaimer — never stripped

## [Session 96] — 2026-03

**Tara Dasha**
- `src/calculations/tara_dasha.py`
- 9-category nakshatra sequence: Janma/Sampat/Vipat/Kshema/Pratyak/Sadhana/Naidhana/Mitra/Ati-Mitra

## [Session 95] — 2026-03

**Shoola Dasha + Sudasa**
- `src/calculations/shoola_dasha.py`
- Shoola (longevity/Ayur) + Sudasa (material success) from same file

## [Session 94] — 2026-03

**Kalachakra Dasha**
- `src/calculations/kalachakra_dasha.py` — BPHS Ch.36–42
- Savya/Apasavya from Moon's navamsha pada; Deha/Jeeva flags per cycle

## [Session 93] — 2026-03

**Prashna (Horary)**
- `src/calculations/prashna.py` — BPHS Prashna chapters + PVRNR applications
- 10 query types; Yes/Possible/Unlikely/No verdict; High/Moderate/Low confidence

## [Session 92] — 2026-03

**Muhurta Engine**
- `src/calculations/muhurta.py` — PVRNR Table 79 (p473–476)
- 7 task types; Tarabala + Chandrabala; 0–7 score; Excellent/Good/Acceptable/Avoid

## [Session 91] — 2026-03

**Panchanga (complete)**
- `src/calculations/panchanga.py` — supersedes `panchang.py`
- 5 limbs; Hora; Choghadiya; Amrita Siddhi; Sarvaartha Siddhi
- `compute_navamsha_chart()` + `_d9_sign_index()` for backward compatibility

---

## [Sessions 87–90] — 2026-03 (Phase 14 — Maturity Features)

- S87: `guidance/educational_layer.py` — Learn mode; classical reasoning in plain language
- S88: `guidance/reflection_prompts.py` — Socratic framing; not declarative prediction
- S89: `guidance/practitioner_handoff.py` — referral logic; sanitised chart summary export
- S90: `api/mobile_router.py` — /mobile lightweight router; React Native shell pending

## [Sessions 84–86] — 2026-03 (Phase 13 — Feedback Governance)

- S84: `feedback/feedback_loop.py` — human-supervised queue; reproducibility lock
- S85: `feedback/harm_escalation.py` — pattern detection; gentle prompt only; no auto-intervention
- S86: `feedback/dependency_prevention.py` — session frequency monitor; no streaks

## [Sessions 79–83] — 2026-03 (Phase 12 — Bloomberg UI)

- S79: Dashboard shell — Next.js 14 + TypeScript + Tailwind; Bloomberg aesthetic
- S80: Domain panels — DomainCard.tsx + SignalBar.tsx; L1/L2 without raw scores
- S81: Timing calendar — TimingCalendar.tsx; 90-day forward; day colouring
- S82: Layered explanation — "Why?" → L2 → L3 opt-in modal
- S83: Onboarding + consent flow — OnboardingFlow.tsx; GDPR/DPDP/CCPA

## [Sessions 76–78] — 2026-02/03 (Phase 11 — Privacy & Legal)

- S76: `privacy/consent_engine.py` — GDPR Art.7+17; right to erasure cascade; age gate
- S77: `privacy/family_consent.py` — per-member consent principals; Kundali Milan gated
- S78: `privacy/data_minimisation.py` — birth time to minute; IP hashed; 90-day retention

## [Sessions 71–75] — 2026-02 (Phase 10 — Language & Safety)

- S71: `guidance/score_to_language.py` — 5-tier; raw scores gated; no deterministic language
- S72: `guidance/fatalism_filter.py` — post-processor; rewrites "will fail", "doomed" etc.
- S73: `guidance/explainability_tiers.py` — L1/L2/L3; L3 opt-in resets each session
- S74: `guidance/guidance_api.py` — single consumer contract; POST /guidance
- S75: `guidance/disclaimer_engine.py` — domain disclaimers; dependency prevention

---

## [Sessions 64–70] — 2026-02 (Phase 9 — Synthesis & Judgment)

- S64: `dominance_engine.py` — classical override rules; DominanceReport
- S65: `promise_engine.py` — Promise/Capacity/Delivery 3-level timing model
- S66: `domain_weighting.py` — 7 domains; per-domain varga weights
- S67: `planet_chains.py` — stelliums, dispositor chains, mutual reception
- S68: `house_modulation.py` — Upachaya age maturation; malefics in 3/6/10/11 beneficial
- S69: `confidence_model.py` — 5-component weighted model; requires_expert_review list
- S70: `chart_exceptions.py` — 7 exception checks with severity

## [Sessions 57–63] — 2026-02 (Phase 8 — PVRNR Textbook Tier 1)

- S57: `orb_strength.py` — PVRNR p147/p149; pvrnr_close ≤6°; reduces_yoga >8°
- S58: `yoga_fructification.py` — 3-condition check; Amsa levels; FructificationResult
- S59: `stronger_of_two.py` — PVRNR p194 5-condition hierarchy
- S60: `av_transit.py` — AV-weighted transit; SAV/BAV thresholds
- S61: `arudha_perception.py` — PVRNR Ch.9; AL reality vs perception 2×2 matrix
- S62: `yogas_pvrnr.py` — 8 yogas from PVRNR Ch.11
- S63: `planet_effectiveness.py` — 7-measure 0.0–1.0 synthesis

## [Sessions 49–56] — 2026-02 (Phase 7 — Workbook Completeness)

- S49: `sayanadi_full.py` — 12-state Avastha; full priority chain; decanate states
- S50: `panchadha_maitri.py` — full 7×7 PanchadhaMatrix; wired to scoring
- S51: `lagnesh_strength.py` — 9-condition cross-cutting modifier for all 12 houses
- S52: `dig_bala.py` — continuous 0.0–1.0 Dig Bala; all 7 planets verified
- S53: `yogas_graha.py` — YOGA_Graha sheet: Budhaditya/Saraswati/Chandra-Mangal/Kahala
- S54: `narayana_argala.py` — Argala modifier on active Narayana Dasha sign
- S55: `config_toggles.py` — CalcConfig; ayanamsha/node/retro toggles with to_dict()/from_dict()
- S56: `varga_agreement.py` — ★★/★/○ per-house D1/D9/D10 confidence flag

---

## [Sessions 41–48] — 2026-01 (Phase 6)

- Ishta/Kashta Bala; longevity calculation; Yogini Dasha; KP school gate
- 200+ yoga library (`extended_yogas.py`); Empirica accuracy event router

## [Sessions 33–40] — 2026-01 (Phase 5)

- 5-axis LPI; multi_axis_scoring.py; Scoring v2/v3; rule_interactions.py

## [Sessions 28–32] — 2026-01 (Phase 4)

- S28: `functional_roles.py` — per-lagna functional maleficence matrix
- S29: `avastha.py` — Deeptadi/Baladi/Lajjitadi states
- S30: `pressure_engine.py` — Life Pressure Index composite engine
- S31: `argala.py` — Argala + Arudha Lagna
- S32: `graha_yuddha.py` + `scoring_v2.py` — planetary war; ENGINE_VERSION

## [Sessions 21–27] — 2026-01 (Phase 3)

- GitHub Actions CI/CD; Streamlit Cloud deploy; 200+ yoga detection

## [Sessions 11–20] — 2026-01 (Phase 2)

- Streamlit UI; Docker; JWT auth; PostgreSQL migration; Alembic; K8s Helm chart

## [Sessions 1–10] — 2026-01 (Phase 1 — Pilot)

- S1: `ephemeris.py` — pyswisseph wrapper; BirthChart; P-1/P-4 fixed
- S2: 7 core modules — dignity, nakshatra, friendship, house_lord, chara_karak, narayana_dasa, shadbala; N-1/S-2 fixed
- S3: `scoring.py` + FastAPI + SQLite
- S4: Streamlit 3-tab UI
- S5: Docker Compose + Makefile + integration tests
- S6: `vimshottari_dasa.py` + South Indian SVG
- S7: `yogas.py` — 13 yoga types
- S8: `ashtakavarga.py` + accuracy guards (E-1/A-2 confirmed absent in Python)
- S9: `gochara.py` — transits, Sade Sati
- S10: `panchanga.py` — 5-limb almanac + D9 navamsha

## S109-124 Phase 0/1/2 — see PLAN.md for full session listing
