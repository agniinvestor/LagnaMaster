# KPIS.md — LagnaMaster KPI Scorecard
> **Update after every session that moves a metric.**
> Baseline: Post-S188, March 2026.

---

## Domain 1 — Prediction Quality

| Metric | Post-S188 | After Ph.5 | After Ph.6 | 2030 Target |
|--------|----------|-----------|-----------|------------|
| Brier score | Pre-baseline | ≤0.20 | ≤0.17 | ≤0.10 |
| Timing accuracy | Pre-baseline | 45% (MD) | 55% (AD+PD) | 80% |
| Signal isolation (confidence − prior) | Pre-baseline | +0.08 | +0.12 | +0.22 |
| Valence accuracy | Pre-baseline | 55% | 63% | 78% |
| Anti-prediction zone rate (target 15–28%) | Not active | 15% | 18% | 22% |
| Hindsight delta | Not measured | Establish baseline | Track | Publish methodology |

**Alert:** If signal isolation stays flat or shrinks below +0.05 for 2+ months → predictions measuring base rates not planets. Investigate immediately.

---

## Domain 2 — Personality Protocol

| Metric | Post-S188 | After Ph.4 | 2030 Target |
|--------|----------|-----------|------------|
| Natal 20Q confirmation rate | Not built | 58% | 80% |
| Adversarial control signal (house-specific − control) | Not built | Establish baseline | >+15% |
| Dasha autobiography completion | Not built | 30% | 65% |
| Birth time HIGH sensitivity grade rate | Not measured | 40% | 70% |
| Onboarding completion (D0→20Q→3 events) | Not built | 30% | 70% |

---

## Domain 3 — ML Model Health

| Metric | Post-S188 | After Ph.6 | 2030 Target |
|--------|----------|-----------|------------|
| SHAP-FDR validated features (Category A) | 0 | 20+ | 200+ |
| Confirmed training events | 0 | 1,000+ (trigger Ph.6) | 500,000+ |
| Bayesian weight std convergence | σ=0.45 (prior) | σ=0.32 | σ=0.12 |
| OSF pre-registrations filed | 0 | 2 | 24/year |
| Category C findings (rules failing FDR) | N/A | Document all | Corpus updated |

---

## Domain 4 — Classical Corpus Depth

| Metric | Post-S188 | After Ph.1 | 2030 Target |
|--------|----------|-----------|------------|
| BPHS chapters encoded (of 97) | ~15 (15%) | 97 (100%) | 97 |
| Named yogas (of 300+) | 13 types | 310+ | 1,000+ |
| Active dasha systems (of 44) | 2 (Vimshottari + Narayana) | 10 | 44 |
| Structured rules in corpus DB | 23 (hard-coded) | 1,500+ | 3,000+ |
| Classical texts formally ingested (of 12) | 2 | 10 | 12 |
| OB-3 global rho | 0.40 | Maintain ≥0.40 | — |
| OB-3 axis-specific r (avg) | ~0.02 | Target ≥0.05 on ≥2 axes | 0.15+ |

---

## Domain 5 — Engineering Reliability

| Metric | Post-S188 | After Ph.0 | 2030 Target |
|--------|----------|-----------|------------|
| Tests passing | **1338** (3 skipped) | 2,200+ | 8,000+ |
| Lint errors | **0** | 0 (enforced) | 0 |
| Chart P99 latency | ~800ms | <50ms (Redis) | <20ms |
| Ephemeris cache hit rate | 0% (no Redis yet) | ≥90% | ≥98% |
| Services extracted (of 5) | 0 | 0 (protocols defined) | 5 |
| Observability stack | None | OpenTelemetry + Prometheus | Full |
| Swiss Ephemeris | **DE431 real files** ✅ | — | Maintained |
| ADB fixture charts | **200+ (all 12 Lagnas)** | 500+ | 5,000+ |

---

## Domain 6–8 — User, Business, Research

| Domain / Metric | Post-S188 | After Ph.4 | 2030 Target |
|-----------------|----------|-----------|------------|
| User: Feedback submission rate | 0% | 3–5% | 50%+ |
| User: D-7 retention | N/A | 28% | 66% |
| User: D-30 retention | N/A | 15% | 52% |
| Business: Registered users | 0 | 2,000+ | 500,000+ |
| Business: Monthly ARR | $0 | $0 | $25M+ |
| Research: Pre-registration rate | 0% | 100% | 100% |
| Research: Published calibration reports | 1 (OB-3) | 3+ | 16+ |
| Research: Peer review submissions | 0 | 0 | 5+ |
