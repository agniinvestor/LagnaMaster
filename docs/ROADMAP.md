# ROADMAP.md — LagnaMaster Complete Phase Roadmap
> **Update this file when sessions complete, phases gate, or session plans change.**

---

## Critical Path

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

## Immediate: S189–S190

| Priority | Item | Effort | Session |
|----------|------|--------|---------|
| 🟠 | C-18: 8 stress-test fixtures (Neecha Bhanga, Graha Yuddha, nakshatra cusp, Parivartana, female, high-lat >55°N, year-boundary, BC date) | 1 day | S189 |
| 🟠 | Verify Shadbala Kala Bala all 8 sub-components | 2 hr | S189 |
| 🟠 | PostgreSQL live test (PG_DSN, run 3 skipped tests) | 2 hr | S189 |
| 🟡 | Confidence model in Streamlit UI | 2 hr | S189 |
| 🟡 | Nehru Capricorn Lagna skip — investigate | 1 hr | S189 |
| 🟡 | BC date charts: `seplm_18.se1` + `semom_18.se1` in `ephe/` | 30 min | S189 |
| 🔵 | OB-3: Empirical calibration ML pipeline (500+ charts) | weeks | S190+ |
| 🔵 | Mundane astrology consumer pipeline | 3–4 days | S190+ |

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

**The feedback schema is the most irreversible decision in the project. It ships complete or not at all.**

DPDP/GDPR compliance (S471–S490). Complete feedback schema with `user_prior_prob_pre` enforced at API layer (S491–S515). Credibility scoring + twin detection (S516–S530).

---

## Phase 4 — Personality Protocol & Onboarding (S531–S610)

Natal 20Q + adversarial controls (S531–S555). Dasha 20Q + autobiography + birth time sensitivity (S556–S580). Progressive onboarding Day 0→Day 21 + failed 20Q UX (S581–S610).

---

## Phase 5 — Temporal Model (S611–S700)

XGBoost MD/AD temporal engine (S611–S640). PD/SD/PrD + daily tone + confidence decay (S641–S680). Multi-dasha concordance + first live Brier score (S681–S700).

---

## Phase 6 — ML Pipeline (S701–S790)

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
