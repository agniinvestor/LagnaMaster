# LagnaMaster

Vedic Jyotish birth chart computation and synthesis engine — the backend of a
consumer Personal Timing & Guidance Companion.

**~920 tests | Sessions 1–70 complete | 63 calc modules | Engine v3.0.0**
**Product roadmap: Sessions 71–90 (Phases 10–14) — consumer launch path**

---

## What This Is

LagnaMaster has two distinct layers:

**The Engine (Sessions 1–70 — complete)**
A deterministic Jyotish computation platform with 63 calculation modules, ~920 tests,
and full classical coverage from BPHS and PVRNR. Produces technically correct
analytical output across 5 lagna axes with confidence flags, dominance hierarchy,
promise/manifestation modeling, and empirical event logging.

**The Product (Sessions 71–90 — in progress)**
A consumer-facing Personal Timing & Guidance Companion. Bloomberg Terminal aesthetic.
Guidance language, not prediction language. Three-tier explainability. GDPR/DPDP
compliant. Designed to support user agency without fostering dependency or fatalism.

The engine is a Formula 1 car engine. The product is the chassis, cockpit, safety
systems, and regulations — built on top of it.

---

## Quick Start

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit (analyst tool) | http://localhost:8501 |
| FastAPI + Swagger | http://localhost:8000/docs |

**Local:**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ulimit -n 4096
PYTHONPATH=. pytest tests/ -q -p no:warnings
```

---

## Product Vision

> A Personal Timing & Guidance Companion — not a prediction engine, oracle, or authority.

**Goals:** Support user agency. Provide clarity and perspective. Highlight opportunities
and risks. Encourage wise decision-making. Avoid fatalism or dependency. Offer
guidance aligned with dharmic principles.

**Not goals:** Predict outcomes. Replace professional advice. Create engagement loops.
Foster dependency. Present deterministic claims.

---

## Consumer Architecture

```
User request
    │
    ▼
guidance_api.py          ← single consumer-facing contract (S74)
    │
    ├─ score_to_language.py      ← transforms scores to human-safe sentences (S71)
    ├─ explainability_tiers.py   ← L1 / L2 / L3 gating (S73)
    ├─ fatalism_filter.py        ← rewrites deterministic language (S72)
    └─ disclaimer_engine.py      ← scope-limiting + dependency prevention (S75)
         │
         ▼
    [all 63 engine modules — never called directly by consumers]
```

Raw scores (LPI values, house scores) are permanently gated behind L3 opt-in.
The consumer default view shows only: signal strength (5-bar), timing label,
natural-language factors, and confidence indicator.

---

## Score → Language Mapping

| Engine score | Signal | Timing label | L1 guidance |
|-------------|--------|-------------|-------------|
| ≥ +3.0 | ●●●●● | Clear passage | Strong foundations support action. |
| +1.5 to +3 | ●●●●○ | Favourable | Conditions are generally supportive. |
| +0.5 to +1.5 | ●●●○○ | Mixed — lean in | Some supporting factors present. |
| −0.5 to +0.5 | ●●○○○ | Neutral | Signals are mixed. |
| −1.5 to −0.5 | ●○○○○ | Navigate carefully | Some friction present — patience favoured. |
| ≤ −1.5 | ○○○○○ | Significant resistance | Building foundation wiser than forcing outcomes. |

Raw scores are never shown at L1 or L2. This is a hard architectural constraint.

---

## Explainability Tiers

| Tier | Default | Content | Gate |
|------|---------|---------|------|
| L1 | ✓ Always | Single guidance sentence, signal bar, timing label | None |
| L2 | On request | 3–5 factor bullets (planet names, timing triggers — no numbers) | "Why?" button |
| L3 | Opt-in only | Full technical trace: Shadbala, AV rekhas, rule firings, raw scores | Explicit opt-in modal |

---

## Domain-Specific Guidance

```python
# Consumer API (Phase 10+)
from src.guidance.guidance_api import get_guidance

response = get_guidance(
    chart_id="abc123",
    domain="career",        # career / marriage / wealth / health / spirituality
    depth="L1",             # L1 / L2 / L3
    on_date=date.today(),
)

print(response.heading)     # "Career — Navigate carefully"
print(response.summary)     # "This period activates career themes. Sustained,
                            #  structured effort is the mechanism — not speed."
print(response.factors)     # ["Saturn period emphasises persistence over speed",
                            #  "10th house timing is moderately active"]
print(response.timing_note) # "Next 6 weeks: mixed signals; clearer from April"
print(response.confidence)  # "Moderate"
print(response.disclaimer)  # "This is reflective guidance, not professional advice."
```

---

## Fatalism Filter

The filter rewrites any output containing deterministic or catastrophising language
before it reaches the API response:

| ❌ Raw engine output | ✔ Consumer output |
|---------------------|------------------|
| Career prospects severely damaged | Career requires more navigation than usual |
| Marriage is unlikely | Partnership timing may involve patience |
| Financial ruin possible | Caution and planning are especially valuable now |
| 8th house affliction: health crisis | Health deserves attention and professional care |

---

## Privacy & Legal

| Regulation | Status |
|-----------|--------|
| GDPR (Article 7 consent, Article 17 erasure) | Phase 11 (S76) |
| CCPA / CPRA | Phase 11 (S76) |
| India DPDP Act | Phase 11 (S76) |
| Child age gating (under-18 block) | Phase 11 (S76) |
| Data minimisation | Phase 11 (S78) |

Birth time stored to minute precision only. IP addresses hashed. Location to city level.
Raw birth data deleted after 90 days of inactivity. Event log anonymised after 1 year.

---

## Session History

| Phase | Sessions | Key deliverables |
|-------|----------|-----------------|
| 1 — Pilot | 1–10 | Ephemeris, calc modules, D1 scoring, FastAPI, SQLite, Streamlit, Docker |
| 2 — Features | 11–19 | Pushkara, Kundali Milan, PDF, Jaimini, KP, Tajika, API v2, 12-tab UI |
| 3 — Production | 20–27 | PostgreSQL, Redis, Celery, JWT, CI/CD, Kubernetes, Next.js, School gates |
| 4 — Pressure Engine | 28–32 | Functional roles, Avastha, LPI v1, Argala, Graha Yuddha, Scoring v2 |
| 5 — Workbook Parity | 33–40 | Multi-lagna, 5-axis scoring, Rule interactions, 7-layer LPI, Scoring v3 |
| 6 — Classical Depth | 41–48 | Ishta/Kashta, Longevity, Yogini Dasha, Full KP, 200+ Yogas, Empirica |
| 7 — Workbook Complete | 49–56 | 12-state Sayanadi, Panchadha Maitri, Lagnesh modifier, Dig Bala |
| 8 — PVRNR Textbook | 57–63 | Orb strength, Yoga fructification, Stronger-of-two, AV transit, Arudha perception |
| 9 — Synthesis Layer | 64–70 | Dominance engine, Promise/Manifestation, Domain weights, Planet chains, Confidence |
| **10 — Language & Safety** | **71–75** | **score_to_language, fatalism_filter, explainability_tiers, guidance_api, disclaimer_engine** |
| **11 — Privacy & Legal** | **76–78** | **GDPR consent + erasure, family consent gates, data minimisation** |
| **12 — Consumer Frontend** | **79–83** | **Bloomberg-style UI, domain dashboards, timing calendar, layered explanation UI** |
| **13 — Feedback Governance** | **84–86** | **Human-supervised feedback, harm escalation, dependency prevention** |
| **14 — Maturity** | **87–90** | **Educational layer, reflection prompts, practitioner handoff, mobile** |

---

## Design Constraints (Non-Negotiable)

1. Raw LPI and house scores never appear in the default consumer view
2. No streak mechanics, badges, or engagement loops
3. No financial, medical, or legal claims
4. Feedback loop is human-supervised — no automated model changes
5. Right-to-erasure cascade removes all computed outputs and birth data
6. All guidance uses possibility language, not deterministic claims
7. Family charts require per-person explicit consent
8. L3 technical detail requires explicit opt-in each session

---

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Lahiri/Raman/KP/Fagan-Bradley) |
| Backend | FastAPI + Celery workers |
| Database | SQLite (→ PostgreSQL) + Empirica event log |
| Cache | Redis (optional) |
| Analyst UI | Streamlit (10-tab) |
| Consumer UI | Next.js 14 (Phase 12) |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT (multi-user) |
| CI/CD | GitHub Actions |
