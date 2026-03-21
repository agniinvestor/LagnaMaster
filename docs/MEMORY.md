# LagnaMaster — Project Memory

> Last updated: 2026-03-21
> Sessions complete locally: 1–100
> Sessions 101–108: committed on remote — run `git pull` before next session

---

## Current State

| Item | Value |
|------|-------|
| Sessions (local) | 1–100 complete |
| Sessions (remote) | 101–108 committed (Phase 0 classical correctness) |
| Tests passing | 963 |
| Engine version | 3.0.0 |
| Stack | pyswisseph · FastAPI + Celery + Redis · PostgreSQL · Next.js 14 · K8s Helm · JWT · GitHub Actions |
| Next action | `git pull` then continue Phase 0 (Sessions 109+) per AUDIT.md |

---

## Repository Layout

```
src/
  ephemeris.py              BirthChart, PlanetPosition (pyswisseph wrapper)
  scoring.py                22-rule pilot heuristic (Sessions 1–10)
  scoring_v2.py             Declarative engine + ENGINE_VERSION (S32)
  scoring_v3.py             Full 23-rule × 5-axis engine — current production
  multi_axis_scoring.py     5-axis composite: D1/D9/D10/Chandra/AL
  db.py                     SQLite (pilot)
  db_pg.py                  PostgreSQL immutable inserts (production)
  cache.py                  Redis 3-tier
  report.py                 reportlab PDF
  worker.py                 Celery workers
  auth.py                   JWT + bcrypt
  config.py                 CalcConfig dataclass
  montecarlo.py             ±30 min birth time rectification

  calculations/             63 modules (full list below)
  guidance/                 8 modules — consumer safety pipeline
  privacy/                  3 modules — GDPR/DPDP/CCPA
  feedback/                 3 modules — governance
  api/
    main.py                 FastAPI v1 (pilot)
    main_v2.py              FastAPI v2 — production (include all routers here)
    auth_router.py
    school_router.py        Parashari / Jaimini / KP school gate
    empirica_router.py      Accuracy event logging
    mobile_router.py        /mobile lightweight endpoints
    models.py               Pydantic v2

frontend/                   Next.js 14 + TypeScript + Tailwind
  src/components/guidance/  DomainCard.tsx, SignalBar.tsx
  src/components/timing/    TimingCalendar.tsx
  src/components/onboarding/ OnboardingFlow.tsx
  src/app/api/guidance/     route.ts

helm/lagnamaster/           Kubernetes Helm chart
migrations/                 Alembic PostgreSQL migrations
```

---

## Calculation Module Inventory (63 modules)

### Astronomical Foundation
- `ephemeris.py` — BirthChart; ayanamshas: Lahiri(1)/Raman(3)/KP(5)/Fagan-Bradley(0)
- `nakshatra.py` — 27 nakshatras, padas, D9 navamsha, Ganda Mool
- `house_lord.py` — whole-sign, Kendra/Trikona/Dusthana/Upachaya
- `friendship.py` — Naisargika + Tatkalik friendships
- `panchadha_maitri.py` — full 7×7 PanchadhaMatrix; wired to scoring (S50)
- `dignity.py` — dignity levels, combustion, Cazimi, Neecha Bhanga
- `shadbala.py` — 6-component Virupas (partial — Phase 0 fixes pending)
- `dig_bala.py` — continuous 0.0–1.0 score; all 7 planets verified (S52)
- `sayanadi_full.py` — 12-state Avastha; full priority chain (S49)
- `avastha.py` — Deeptadi/Baladi/Lajjitadi states (S29)
- `graha_yuddha.py` — planetary war; 5 planets only (Mars/Merc/Jup/Ven/Sat) (S32)
- `orb_strength.py` — orb-sensitive strength; pvrnr_close ≤6°; reduces_yoga >8° (S57)
- `config_toggles.py` — CalcConfig; ayanamsha/node/retro toggles (S55)

### Divisional Charts
- `vargas.py` — 20 divisional charts D1–D60
- `varga_agreement.py` — ★★/★/○ per-house D1/D9/D10 confidence (S56)

### Dasha Systems (9)
- `vimshottari_dasa.py` — 120yr; MD × AD × PD
- `narayana_dasha.py` — 81yr Rasi dasha
- `yogini_dasha.py` — 36yr, 8 Yoginis
- `chara_dasha.py` — Jaimini sign dasha
- `kalachakra_dasha.py` — 100yr; Moon D9 pada; Savya/Apasavya; Deha/Jeeva (S94)
- `ashtottari_dasha.py` — 108yr, 8 planets; conditional (S100)
- `shoola_dasha.py` — Shoola (longevity) + Sudasa (material success) (S95)
- `tara_dasha.py` — 9-category nakshatra: Janma→Ati-Mitra (S96)
- `narayana_argala.py` — Argala modifier on active Narayana Dasha sign (S54)

### Yoga Detection (200+)
- `yogas.py` — core 13 types
- `extended_yogas.py` — 200+ yogas including Nabhasa and Viparita Raja
- `yogas_graha.py` — YOGA_Graha sheet; Budhaditya/Saraswati/Chandra-Mangal/Kahala (S53)
- `yogas_pvrnr.py` — PVRNR Ch.11: Guru-Mangala/Amala/Sankha/Vasumati etc. (S62)
- `yoga_fructification.py` — 3-condition check; Amsa levels; Full/Partial/Weak/Minimal (S58)

### Scoring Engines
- `scoring.py` — 22-rule pilot; clamped [−10,+10]
- `scoring_v2.py` — declarative; ENGINE_VERSION audit trail
- `scoring_v3.py` — 23-rule; 5 lagna axes; current production
- `multi_axis_scoring.py` — D1/D9/D10/Chandra/AL composite
- `rule_interactions.py` — named compound interactions

### Synthesis & Judgment (Phase 9)
- `functional_roles.py` — per-lagna functional maleficence matrix (S28)
- `pressure_engine.py` — Life Pressure Index composite (S30)
- `argala.py` — Argala + Arudha Lagna (S31)
- `arudha_perception.py` — AL reality vs perception 2×2 model (S61)
- `lagnesh_strength.py` — 9-condition cross-cutting modifier for all 12 houses (S51)
- `stronger_of_two.py` — PVRNR p194 5-condition hierarchy (S59)
- `planet_chains.py` — stelliums, dispositor chains, mutual reception (S67)
- `planet_effectiveness.py` — 7-measure 0.0–1.0 effectiveness (S63)
- `av_transit.py` — AV-weighted transit; SAV/BAV thresholds (S60)
- `dominance_engine.py` — classical override rules: kendra suppression, combust blocking (S64)
- `promise_engine.py` — Promise/Capacity/Delivery 3-level timing (S65)
- `domain_weighting.py` — 7 domains; per-domain varga weights (S66)
- `house_modulation.py` — Upachaya age maturation; malefics in 3/6/10/11 beneficial (S68)
- `confidence_model.py` — 5-component: varga/conflict/sensitivity/boundary/role (S69)
- `chart_exceptions.py` — 7 exception checks with severity (S70)

### Specialised Branches (Sessions 91–100)
- `panchanga.py` — 5-limb almanac; Hora; Choghadiya; Amrita/Sarvaartha Siddhi
- `muhurta.py` — 7 task types; PVRNR Table 79; Tarabala/Chandrabala; 0–7 score
- `prashna.py` — horary; 10 query types; Yes/Possible/Unlikely/No verdict
- `upaya.py` — remedial; PVRNR Tables 77–78; auto-detect afflictions
- `mundane.py` — nation/ingress/swearing-in; compress_vimshottari()
- `contextual.py` — partial DKP; era-aware profession mapping; practitioner note required

### Consumer Safety Pipeline (Phases 10–14)
- `guidance/score_to_language.py` — numerical → human-safe; 5-tier; raw scores gated
- `guidance/fatalism_filter.py` — rewrites deterministic language post-processing
- `guidance/explainability_tiers.py` — L1/L2/L3 (L3 opt-in resets each session)
- `guidance/guidance_api.py` — single consumer contract; POST /guidance
- `guidance/disclaimer_engine.py` — domain-specific disclaimers; dependency prevention
- `guidance/educational_layer.py` — Learn mode; classical reasoning
- `guidance/reflection_prompts.py` — Socratic framing
- `guidance/practitioner_handoff.py` — referral logic; sanitised chart summary

### Privacy & Compliance
- `privacy/consent_engine.py` — GDPR Art.7+17; DPDP; CCPA; right to erasure cascade
- `privacy/family_consent.py` — per-member consent; Kundali Milan requires both
- `privacy/data_minimisation.py` — birth time to minute; IP hashed; 90-day retention

### Feedback Governance
- `feedback/feedback_loop.py` — human-supervised queue; reproducibility lock
- `feedback/harm_escalation.py` — pattern detection; gentle prompt only
- `feedback/dependency_prevention.py` — session frequency monitor; no streaks

---

## Critical Invariants

1. `compute_chart()`: `hour=0` is valid (midnight) — NEVER treat as falsy
2. Ketu = Rahu + 180° mod 360 — always derived, never from ephemeris
3. Whole-sign houses for Parashari natal; Bhava Chalita is a pending overlay
4. `scoring_v3.ENGINE_VERSION` must be stored in `score_runs.engine_version` for audit
5. `functional_roles.py` requires full `chart` object — needs planet positions for house occupancy
6. `pressure_engine.py` is additive approximation — label as "heuristic" in all UI output
7. `graha_yuddha.py` applies to 5 planets ONLY: Mars/Mercury/Jupiter/Venus/Saturn — never luminaries or nodes
8. The scoring engine is a heuristic — additive weights are non-classical; never present as authoritative verdicts
9. `upaya.py` recommendations ALWAYS carry disclaimer — never stripped in any response
10. Consumer API L1/L2 must NEVER expose raw house scores or Shadbala virupas
11. L3 opt-in resets each session — not persisted — prevents normalisation of raw scores
12. Right to erasure is a cascade: birth data + outputs + event logs → tombstone record
13. `qualifies_for_ashtottari()` MUST be called before using ashtottari dasha — Rahu not in H1/H7
14. `panchanga.py` supersedes `panchang.py` — never call the old module
15. `config_toggles.py` CalcConfig must use `to_dict()`/`from_dict()` for API reproducibility
16. `varga_agreement.py` ★★/★/○ flags feed into `confidence_model.py` as the 30% component
17. `montecarlo.py` only runs after all modules pass India 1947 regression
18. `db_pg.py` immutable inserts — chart records never updated; only new `score_runs` rows
19. Ashtottari is conditional — if chart doesn't qualify, fall back to Vimshottari
20. `contextual.py` is explicitly partial DKP — practitioner note is not optional

---

## Regression Fixture

```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15, "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5, "ayanamsha": "lahiri"
}
# Lagna: Taurus 7.7286° (±0.05°)
# Sun: Cancer 27.989° | Moon: Cancer 3.9835°
# Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn in Cancer
# H2 Wealth: D1=−5.25, D9=−2.0, D10=−2.5 → ★★ varga agreement
# Ashtottari: does NOT qualify (Rahu in H1 from Taurus lagna)
```

---

## Phase 0 Correctness Issues (Sessions 101–108 on Remote)

These were identified by the March 2026 classical audit. See `AUDIT.md` for full citations.

| ID | Module | Issue | Status |
|----|--------|-------|--------|
| C-01 | `dignity.py` | MT degree ranges approximate; Mercury MT = 16°–20° only | 🔄 S101+ |
| C-02 | `dignity.py` | Exaltation binary flag; needs Paramotcha gradient | 🔄 S101+ |
| C-03 | `dignity.py` | Rahu/Ketu NEUTRAL everywhere; wrong under all schools | 🔄 S101+ |
| C-04 | `dignity.py` | 5 Neecha Bhanga conditions missing (only 1 of 6 coded) | 🔄 S101+ |
| C-05 | `scoring.py` | WC-halving (0.5×) non-classical; replace with BPHS ¾-strength | 🔄 S101+ |
| C-06 | `vimshottari_dasa.py` | Nakshatra float: `int(lon/13.333)` → use `int(lon*3/40)` | 🔄 S101+ |
| C-07 | `ashtakavarga.py` | Trikona Shodhana missing; raw bindus meaningless | 🔄 S101+ |
| C-08 | `ashtakavarga.py` | Ekadhipatya Shodhana missing | 🔄 S101+ |
| C-09 | `shadbala.py` | 7 of 8 Kala Bala sub-components missing | 🔄 S101+ |
| C-10 | `shadbala.py` | Drik Bala = 0 in all charts | 🔄 S101+ |

---

## Genuinely Excluded (Theoretical Limits)

| Item | Reason |
|------|--------|
| Kalachakra full textual variants | Contradictory commentators; BPHS version implemented |
| Desha-Kala-Patra in full | Practitioner situational judgment — not parameterisable |
| Gestalt synthesis | Named rules encoded; nonlinear expert weighting is not |
| Prashna Marga full corpus | Separate text, different framework |
| Medical/financial astrology | Separate disciplines with liability implications |

# Sessions 109-124 additions added — see PLAN.md for full detail


## Sessions 135-160
S135 Rashi Drishti. S137 functional_dignity. S138 avasthas. S142 transit_quality_advanced. S146 upagrahas_derived. S147 shadbala_patches. S149 varshaphala. S150 karakamsha. S140/145 yoga_strength. S154 dasha_activation.
