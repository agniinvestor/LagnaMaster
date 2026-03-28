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
| S190 | Verify Shadbala Kala Bala 8 sub-components + PostgreSQL live test + Confidence model in Streamlit UI + Nehru Capricorn Lagna skip investigation | — | 🔴 |

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
| S191 | VedAstro install + cross-validation, ruff no-jhora rule, Protocol interface stubs, classical texts download | G17, G23, G24 | 🔴 |
| S192 | Python Protocol interfaces — module boundary formalization | — | 🔴 |
| S193 | HouseScore distribution dataclass replaces float | G04, G18 | 🔴 |
| S194 | Conditional weight functions W(planet, house, lagna, functional_role) | G06 | 🔴 |
| S195–S200 | Feature decomposition — 23 binary → 150+ continuous features | G22 | 🔴 |
| S201–S210 | OSF pre-registration + ADB license + corpus extractor pipeline | G22 | 🔴 |
| S211 | Redis + pgvector + TimescaleDB + MLflow + family schema | — | 🔴 |
| S212 | Ayanamsha selection + KP school fix (G06 compliance) | G06 | 🔴 |
| S213–S215 | Protocol verification + CI observability + Phase 0 checkpoint | All Phase 0 | 🔴 |

---

## Phase 1 — Classical Knowledge Foundation (S216–S410) ⭐ MOST CRITICAL
**Convergence layer:** Phase 1 deepens **Layer I (Classical Convergence)** exclusively.

**The right encoding priority within Phase 1:**
Not all rules have equal impact. Rules that can fire independently from multiple schools
(Parashari AND KP AND Jaimini) raise the maximum achievable concordance score more than
rules that are Parashari-only. Rules that encode the lagna-conditional behavior of each
planet directly address the root cause of OB-3's low axis-specific r (~0.02). These
should be prioritized within each text encoding session.

**Phase 1 gate (expanded):** Not just rule count — the gate is whether the Layer I
concordance model is producing meaningful multi-school agreement signals. Target:
after Phase 1, ≥20% of predictions should reach concordance ≥0.75 across all three
schools. Below this, Phase 2 feature vector expansion will not have enough signal to work with.



| Sessions | Deliverable | Target |
|----------|-------------|--------|
| S216–S250 | BPHS all 97 chapters AI-assisted encoding | 800+ rules |
| S251–S290 | Brihat Jataka + Uttara Kalamrita + Jataka Parijata + Sarwarthachintamani | 630+ rules |
| S291–S325 | Jaimini Sutras + Lal Kitab + Chandra Kala Nadi (separate schemas) | 370+ rules |
| S326–S360 | Yoga expansion: 13 → 310+ (VedAstro reference) | 310+ yogas |
| S361–S380 | Complete Shadbala + 10 Dasha Systems + D12–D60 + Full Ashtakavarga | 4 gaps closed |
| S381–S410 | Corpus finalization + Jaimini + Special Lagnas + V1.0 lock | 1,500+ total |

**Phase 1 gate:** `corpus_audit.py` 0 errors, V1.0 locked, 100+ high-concordance rules (≥0.8).

---

## Phase 2 — Engine Rebuild (S411–S470)

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
