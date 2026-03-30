# ROADMAP.md — LagnaMaster Complete Phase Roadmap
> **Update this file when sessions complete, phases gate, or session plans change.**

---

## Critical Path
### Why This Phase Order (Convergence Layer Reasoning)

The phase order is not arbitrary. Each phase builds the foundation that the next phase
requires, organized around the three convergence layers:

**Phases 0–2 (S191–S470): Classical Convergence depth + infrastructure.**
You cannot build a meaningful empirical validation system (Layer III) until the classical
convergence model (Layer I) is deep enough to generate meaningful priors. Testing 23
rules with SHAP analysis will produce noise. Testing 1,500+ rules with proper school
attribution and concordance scoring will produce publishable findings. Phase 0 builds
the infrastructure. Phase 1 fills the classical corpus. Phase 2 rebuilds the engine
with the full corpus, producing the first meaningful Layer I concordance scores.

**Phases 3–4 (S471–S610): Structural convergence inputs + person-specific calibration.**
The 20Q personality protocol (Phase 4) is not primarily an onboarding feature — it is
a structural convergence calibration mechanism. It verifies whether the engine's Layer I
signals are correctly calibrated to this specific person's birth chart. Without it, the
engine issues Layer II assessments (Capacity/Delivery) for a chart it has never verified
against the person. Phase 3 builds the feedback schema that will eventually feed Layer III.

**Phases 5–6 (S611–S790): Temporal model + empirical convergence.**
Phase 5 builds the full temporal cascade (Layer II delivery). Phase 6 builds empirical
convergence (Layer III). These are deliberately sequenced: you need the temporal model
to generate predictions with proper timing windows before you can close those windows
and collect confirmed outcomes.

**Phases 7–10 (S791+): Product, multigenerational, extraction, research.**
Only at this point does the full three-layer model exist. Product monetization (Phase 7)
is built on all three layers being operational. The multigenerational map (Phase 8) is
a Layer I extension — family dasha cascade adds additional classical convergence signals
from related charts. Research frontiers (Phase 10) are what the empirical convergence
layer produces as scientific output.

---



```
S189–S190 (immediate fixes)
→ S191–S215 (Phase 0: Guardrails & Infrastructure)
→ S216–S410 (Phase 1: Classical Knowledge Foundation — MOST CRITICAL)
→ S411–S470 (Phase 2: Engine Rebuild with Full Corpus)
→ S471–S530 (Phase 3: Feedback Architecture & Privacy)
→ S531–S610 (Phase 4: Personality Protocol & Onboarding)
→ S611–S700 (Phase 5: Temporal Model)
→ S701–S790 (Phase 6: ML Pipeline & Empirical Discovery)
→ S791–S840 (Phase 7: Product & Revenue)
→ S841–S900 (Phase 8: Multigenerational Pattern Map)
→ S901–S950 (Phase 9: Service Extraction)
→ S951–S1050+ (Phase 10: Research Frontiers)
```

**Can parallelize:** S216–S410 corpus encoding runs alongside S191–S215. Phase 8 runs alongside Phase 7 from S841.

---

## Immediate: S190

| Session | Deliverable | Guardrails | Status |
|---------|-------------|-----------|--------|
| S190 | Verify Shadbala Kala Bala 8 sub-components ✅ + PostgreSQL live test (PG_DSN env-gated, skipped) + Confidence model in Streamlit UI ✅ + Nehru Capricorn Lagna skip root cause documented ✅ | — | 🟡 |

| Priority | Item | Effort |
|----------|------|--------|
| 🟠 | Verify Shadbala Kala Bala all 8 sub-components (cross-check vs PyJHora algorithm) | 2 hr |
| 🟠 | PostgreSQL live test (spin up PG_DSN, run 3 skipped tests) | 2 hr |
| 🟡 | Confidence model surfaced in Streamlit UI (endpoint exists, no tab yet) | 2 hr |
| 🟡 | Nehru Capricorn Lagna fixture skip — investigate root cause | 1 hr |
| 🔵 | OB-3: Empirical calibration ML pipeline (500+ charts needed) | weeks |
| 🔵 | Mundane astrology consumer pipeline | 3–4 days |

---

## Phase 0 — Guardrails & Infrastructure (S191–S215)

No user-facing code ships until Phase 0 is complete. No empirical analysis runs until OSF pre-registration is filed.

| Session | Deliverable | Guardrails | Status |
|---------|-------------|-----------|--------|
| S191 | VedAstro install + cross-validation, ruff no-jhora rule, Protocol interface stubs, classical texts download | G17, G23, G24 | ✅ |
| S192 | Python Protocol interfaces — module boundary formalization | — | ✅ |
| S193 | HouseScore distribution dataclass replaces float | G04, G18 | ✅ |
| S194 | Conditional weight functions W(planet, house, lagna, functional_role) | G06 | ✅ |
| S195–S200 | Feature decomposition — 23 binary → 150+ continuous features | G22 | ✅ |
| S201–S210 | OSF pre-registration + ADB license + corpus extractor pipeline | G22 | ✅ |
| S211 | Redis + pgvector + TimescaleDB + MLflow + family schema | — | ✅ |
| S212 | Ayanamsha selection + KP school fix (G06 compliance) | G06 | ✅ |
| S213–S215 | Protocol verification + CI observability + Phase 0 checkpoint | All Phase 0 | ✅ |

---

## Phase 1 — Classical Knowledge Foundation (S216–S410+) ⭐ MOST CRITICAL
**Convergence layer:** Phase 1 deepens **Layer I (Classical Convergence)** exclusively.

### Phase 1A — Representative Layer (COMPLETE, S216–S262)

2,634 rules across 9 classical texts. Relabeled from "exhaustive" to "representative" —
these are breadth-coverage entries with prose descriptions. Valid as a topic index.
Not suitable as primary ML input. See `docs/CLASSICAL_CORPUS.md` for full Phase 1A inventory.

### Phase 1B — Sutra-Level Encoding (S263–S410)

Phase 1B is the research-grade corpus. **Revised target: ~19,800 structured predictions
total** (Phase 1A 3,301 + ~16,500 new Phase 1B rules). Every Phase 1B rule satisfies a
formal contract: structured `primary_condition`, `modifiers`, `exceptions`,
`outcome_domains` (from fixed taxonomy), `outcome_direction`, `outcome_intensity`,
`lagna_scope`, `verse_ref` (chapter+verse), `concordance_texts` (populated at encoding
time). See `docs/CLASSICAL_CORPUS.md` for the full Rule Contract and Outcome Taxonomy.

**Phase 1B is gated on S263** — the schema definition session that produces the Rule
Contract, Outcome Taxonomy, coverage map template, and concordance workflow. No Phase 1B
encoding begins without these four documents committed.

**Original S301–S309 estimate of ~1,110 rules was a 10x underestimate.** Research-grade
chapter-by-chapter analysis (conducted S270 planning pass) shows the correct totals:
Mansagari = 2,755–3,850 rules (30 chapters), Jataka Tattva = 3,940–5,460 rules
(22 tarangas), Stri Jataka = 1,300–1,840 rules (13 chapters), Muhurtha Chintamani =
2,310–3,120 rules (20 ullasas, separate schema), Yoga Expansion = ~1,649 rules.

**Priority order within Phase 1B:**
1. **Laghu Parashari first (S264–S266)** ✅ — 9×12 functional nature table. 306 rules.
2. **Bhavartha Ratnakara (S267–S272)** — 12 lagnas × all houses. ~800 rules total.
   S267–S269 done (Aries→Virgo, BVR001–390). S270–S272 complete Libra→Pisces.
3. **Saravali (S273–S281)** — 68 chapters, ~1,400 rules. Conjunctions block first
   (Ch.31–51: 21 pairs × 12 signs = 252 rules), then house matrices, then yogas.
4. **Chamatkara Chintamani (S282–S285)** — 28 chapters, ~550 rules. 1B_matrix.
5. **Hora Ratnam (S286–S290)** — 22 chapters, ~600 rules. 1B_matrix + 1B_conditional.
6. **Prasna Marga (S291–S297)** — 32 chapters, ~950 rules. `system: horary` on all rules.
7. **Tajika Neelakanthi (S298–S300)** — 16 chapters, ~255 rules. `system: varshaphala`.
8. **Mansagari (S301–S313)** — 30 chapters, 2,755–3,300 rules. Densest natal text after
   BPHS. Priority: Ch.11 (Rashi phalam — denser than BPHS), Ch.14 (Yogas, 180–250 rules),
   Ch.16 (Antardasha 9×9=81 combinations), Ch.23–27 (Muhurtha within Mansagari).
9. **Jataka Tattva (S314–S331)** — 22 Tarangas, 3,940–5,000 rules. Highest total of any
   single text. Priority: Taranga 11 (Dasha × Ascendant matrix, unique cross-ref),
   Taranga 15 (Medical astrology, systematic), Taranga 17 (Prenatal — nearly unique),
   Taranga 20 (Yoga cancellation rules). `source: JatakaTattva` on all rules.
10. **Stri Jataka (S332–S337)** — 13 chapters, 1,300–1,840 rules. Unique female
    horoscopy domain. ALL rules flagged `domain: female_nativity`. Priority: Ch.4
    (Husband from wife's chart — nowhere else in classical literature), Ch.6 (Widowhood),
    Ch.7 (Chastity/character). ~600–900 rules with zero overlap with other texts.
11. **Muhurtha Chintamani (S338–S347)** — 20 Ullasas, 2,310–3,120 rules. **Separate
    schema** — muhurtha rules have structure `(panchanga_element, value, activity) →
    quality_outcome`, NOT `(planet, house, lagna) → life_outcome`. All rules flagged
    `system: muhurtha`. Priority: Ullasa 2 (tithi × activity, 30×N rules), Ullasa 4–5
    (nakshatra × activity, 27×N rules). Never served to natal engine.
12. **Yoga Expansion (S348–S355)** — ~1,649 rules completing the yoga universe:
    - Nabhasa (37): 3 Ashraya + 2 Dala + 20 Aakruti + 12 Sankhya
    - Moon yogas (32): Sunapha/Anapha/Durudhura/Kemadruma + named variants
    - Solar yogas (25): Vesi/Vasi/Ubhayachari + Budhaditya variants
    - Pancha Mahapurusha (19): 5 base + 14 sign variants
    - Raja yogas (150): 36 generic + 84 lagna-specific + 30 special named
    - Dhana yogas (80): 12 generic + 60 lagna-specific + 8 special
    - Arishta yogas (40): Kala Sarpa 12 variants + Chandal/Shrapit/Angarak
    - Multi-planet conjunctions (120): Saravali Ch.52–56 complete enumeration
    - Viparita Raja (15): 3 base × 3 placements + 3 enhanced
    - Parivartana (66): all 66 house-pair exchanges (Maha/Dainya/Khala classified)
    - Neecha Bhanga (83): 7 planets × 9 cancellation conditions + compound
13. **Verification sessions (S356–S370)** — one per major text, coverage map audit,
    Rule Contract compliance spot-check.

| Sessions | Deliverable | Rules | Gate |
|----------|-------------|-------|------|
| S263 | Schema definition — Rule Contract + Taxonomy + Coverage Map + Concordance Workflow | 0 | All four docs committed ✅ |
| S264–S266 | Laghu Parashari (8 chapters) | ~306 | Coverage map complete ✅ |
| S267–S269 | Bhavartha Ratnakara Aries→Virgo (BVR001–390) | 390 | 6/12 lagnas done ✅ |
| S270–S272 | Bhavartha Ratnakara Libra→Pisces (BVR391–800) | ~410 | All 12 lagnas, all lagna_scope populated |
| S273–S276 | Saravali: Two-planet conjunctions (Ch.31–51, 21 pairs × 12 signs) | ~252 | Concordance vs. BPHS tracked |
| S277–S279 | Saravali: Planet-in-sign (Ch.6–13) + Planet-in-house (Ch.14–22) | ~240 | verse_ref Ch/V populated |
| S280–S281 | Saravali: Dignities + House-lord matrix + Yogas (Ch.23–30, 57–61) | ~550 | Coverage map complete |
| S282–S285 | Chamatkara Chintamani (28 chapters, 1B_matrix) | ~550 | verse_ref all populated |
| S286–S290 | Hora Ratnam (22 chapters, 1B_matrix + 1B_conditional) | ~600 | — |
| S291–S297 | Prasna Marga (32 chapters, 1B_matrix + 1B_compound) | ~950 | system=horary on all rules |
| S298–S300 | Tajika Neelakanthi (16 chapters) | ~255 | system=varshaphala on all rules |
| S301–S304 | Mansagari Part A: Ch.1–10 (Graha in bhava, all 9 planets × 12 houses) | ~620 | 108 bhava placements done |
| S305–S308 | Mansagari Part B: Ch.11–17 (Rashi phalam + Yogas + Dasha + Antardasha 9×9) | ~760 | 81 AD combos done |
| S309–S313 | Mansagari Part C: Ch.18–30 (Ashtakavarga + Graha Bala + Stri + Longevity + Muhurtha) | ~900 | Coverage map complete |
| S314–S318 | Jataka Tattva Part A: Taranga 1–5 (Graha nature + Rashi + Bhava placements) | ~650 | Taranga coverage begun |
| S319–S323 | Jataka Tattva Part B: Taranga 6–11 (Yogas + Dhana + Raja + Dasha × Ascendant matrix) | ~850 | T11 dasha×ascendant matrix done |
| S324–S328 | Jataka Tattva Part C: Taranga 12–17 (Longevity + Arishta + Medical + Prenatal) | ~900 | T15 medical + T17 prenatal done |
| S329–S331 | Jataka Tattva Part D: Taranga 18–22 (Female + Stri + Yoga cancellations + Conclusion) | ~650 | T20 yoga cancellations done |
| S332–S334 | Stri Jataka Part A: Ch.1–7 (Appearance + Character + Marriage + Widowhood + Chastity) | ~900 | Ch.4 husband-from-wife + Ch.6 widowhood done |
| S335–S337 | Stri Jataka Part B: Ch.8–13 (Progeny + Profession + Longevity + Special yogas) | ~700 | Coverage map complete |
| S338–S341 | Muhurtha Chintamani Part A: Ullasa 1–8 (Tithi × activity + Vara + Nakshatra matrices) | ~850 | system=muhurtha, panchanga schema used |
| S342–S345 | Muhurtha Chintamani Part B: Ullasa 9–16 (Specific muhurtha types: Vivaha, Griha, Yatra) | ~900 | All activity types tagged |
| S346–S347 | Muhurtha Chintamani Part C: Ullasa 17–20 + Muhurtha Martanda unique chapters | ~570 | Coverage map complete |
| S348–S350 | Yoga Expansion A: Nabhasa (37) + Moon yogas (32) + Solar yogas (25) + Pancha Mahapurusha (19) | ~113 | All source texts cited |
| S351–S353 | Yoga Expansion B: Raja yogas (150) + Dhana yogas (80) | ~230 | lagna_scope on lagna-specific rules |
| S354–S355 | Yoga Expansion C: Arishta (40) + Parivartana (66) + Neecha Bhanga (83) + Viparita (15) | ~204 | All 66 Parivartana classified |
| S356–S370 | Verification sessions (one per major text, coverage map audit, contract compliance) | 0 | All sections in coverage maps complete |

**Phase 1B total rule target: ~16,500 new rules (19,800 corpus total)**

**Phase 1 gate (final):**
- Every Phase 1B text has a committed coverage map with all sections complete
- ≥90% of Phase 1B rules satisfy the full Rule Contract
- `verse_ref` populated on all Phase 1B rules (chapter + verse)
- `concordance_texts` populated in real-time (not retroactive)
- Outcome taxonomy used consistently — no free-form values
- `corpus_audit.py` 0 errors
- ≥20% of rules reach concordance ≥0.75 across 2+ schools
- Muhurtha rules isolated in separate pipeline — never fed to natal engine

---

## Phase 2 — Engine Rebuild (S411–S470)
*(Phase 2 start held at S411 — Phase 1B verification sessions S356–S370 complete by S410)*

Feature vectors 150 → 500+. Muhurtha engine. OB-3 rerun (target r > 0.05 on ≥2 axes). Observability stack (OpenTelemetry + Prometheus).

---

## Phase 3 — Feedback Architecture & Privacy (S471–S530)
**Convergence layer:** Phase 3 builds the infrastructure for **Layer III (Empirical Convergence)**.

**Critical schema addition:** The feedback schema must capture not just whether a
prediction was confirmed, but the convergence state at the time of prediction — specifically:
what was the school concordance score, what was the varga agreement grade, what was the
Promise/Capacity/Delivery status. Without this, the Layer III Bayesian updates (Phase 6)
cannot distinguish a confirmed high-concordance prediction (strong signal) from a confirmed
low-concordance prediction that happened to be correct (possibly noise).



**The feedback schema is the most irreversible decision in the project. It ships complete or not at all.**

DPDP/GDPR compliance (S471–S490). Complete feedback schema with `user_prior_prob_pre` enforced at API layer (S491–S515). Credibility scoring + twin detection (S516–S530).

---

## Phase 4 — Personality Protocol & Onboarding (S531–S610)
**Convergence layer:** Phase 4 is **Layer II structural calibration** — person-specific.

The 20Q personality protocol is not primarily an onboarding feature. It is the mechanism
by which Layer I's classical signals are verified against the specific person. If the
engine predicts assertiveness (Mars functional benefic in H3) but the person consistently
disconfirms it, the Layer I concordance for that person's chart should be reduced, not the
rule weight globally. This person-specific calibration is what separates structural
convergence from the raw classical model.

**Implication for 20Q design:** Questions must be designed to independently verify
Layer I convergence signals, not the scoring engine's outputs. See G07 (circular validation
risk). The adversarial control question design (10% of questions from different house's
prediction set) is a direct check on whether Layer I concordance is genuinely person-specific.



Natal 20Q + adversarial controls (S531–S555). Dasha 20Q + autobiography + birth time sensitivity (S556–S580). Progressive onboarding Day 0→Day 21 + failed 20Q UX (S581–S610).

---

## Phase 5 — Temporal Model (S611–S700)

XGBoost MD/AD temporal engine (S611–S640). PD/SD/PrD + daily tone + confidence decay (S641–S680). Multi-dasha concordance + first live Brier score (S681–S700).

---

## Phase 6 — ML Pipeline (S701–S790)
**Convergence layer:** Phase 6 builds and validates **Layer III (Empirical Convergence)**.

**Primary OSF research hypothesis (must be pre-registered at S461 before Phase 6 begins):**
Does multi-factor convergence (Layer I classical concordance × Layer II structural
activation) predict life outcomes at a statistically validated rate above any single
factor's baseline? This is the novel scientific question — not whether individual
classical rules predict outcomes, but whether the *agreement* between independent
classical frameworks is itself a predictive signal.

This reframes the SHAP analysis: the most important features are not individual rules
(Category A/C) but convergence interaction terms — does high-concordance + strong
capacity predict outcomes better than high-concordance alone? The answer to this question
is what justifies the entire convergence architecture.



XGBoost + SHAP (pre-registered, FDR-corrected) — Categories A/B/C (S701–S730). HDBSCAN clustering (S731–S745). Bayesian weight updates after 1,000+ events (S746–S760). Cox survival analysis — **internal only, never user-facing** (S761–S775). Chart embeddings pgvector (S776–S790).

---

## Phase 7 — Product & Revenue (S791–S840)

5 revenue tiers: Free/$0, Core/$8, Deep/$18, Precision/$35, Family/$45. Life Audit ($79–149). Muhurtha optimizer ($75–130). Pre-decision oracle with Brier context.

---

## Phase 8 — Multigenerational Pattern Map (S841–S900)

**Family Dasha Cascade (Bhavat Bhavam principle — classical, never computationally implemented before):**
- Father enters Saturn MD → user's H9 activates → career/dharma themes
- Mother enters Rahu MD → user's H4 activates → domestic disruption
- Spouse enters 8th lord dasha → user's H7 activates with 8th energy
- Child enters Jupiter MD → user's H5 activates → creative success

D12 ancestral analysis available to ALL users from Day 0 (no family data needed — computable from user's own chart alone).

---

## Phase 9 — Service Extraction (S901–S950)

Strangler-fig migration. Protocol interfaces from Phase 0 enable code movement not rewriting.

| Sessions | Service | Trigger |
|----------|---------|---------|
| S901–S910 | Temporal Engine | >1,000 concurrent users or GPU workers needed |
| S911–S920 | Feedback Service | Reliability requirements (training data must never be lost) |
| S921–S935 | ML Service | Training jobs >5min blocking API |
| S936–S945 | Notification Service | Different deployment pattern (scheduled) |
| S946–S950 | Family Service | Independent privacy requirements |

---

## Phase 10 — Research Frontiers (S951–S1050+)

Hindi/Tamil/Telugu/Bengali localisation. Astrologer RLHF cohort. Twin registry (Swedish 85K pairs, Australian 30K pairs). Biosignal pipeline (HealthKit/Oura). AstroLM foundation model preparation. Peer review manuscript submissions.
