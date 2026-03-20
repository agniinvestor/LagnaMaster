# LagnaMaster

Vedic Jyotish computation engine + consumer guidance platform.

**~980 tests | Sessions 1–90 complete | 90 modules | Engine v3.0.0**

---

## Architecture

```
Consumer (browser / mobile)
        │
        ▼
┌─────────────────────────────────┐
│  Guidance Pipeline (Phase 10)   │
│  guidance_api.py                │
│  ├─ score_to_language.py        │  scores → 5-bar signal
│  ├─ explainability_tiers.py     │  L1 / L2 / L3 gating
│  ├─ fatalism_filter.py          │  deterministic language → possibility
│  └─ disclaimer_engine.py        │  scope limits + dependency nudges
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│  Jyotish Engine (Phases 1–9)    │
│  63 calculation modules         │
│  scoring_v3.py  ENGINE v3.0.0   │
└─────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────┐
│  Privacy Layer (Phase 11)       │
│  consent_engine.py   GDPR/DPDP  │
│  family_consent.py   per-person │
│  data_minimisation.py GDPR Art5 │
└─────────────────────────────────┘
```

Raw engine scores **never** reach consumers at L1 or L2. All traffic passes
through the guidance pipeline. Engine modules are never called directly from
consumer-facing endpoints.

---

## Quick Start

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit (analyst) | http://localhost:8501 |
| FastAPI + Swagger | http://localhost:8000/docs |
| Next.js (consumer) | http://localhost:3000 |

**Local:**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ulimit -n 4096
PYTHONPATH=. pytest tests/ -q -p no:warnings
```

---

## Consumer Guidance API

```python
from src.guidance.guidance_api import get_guidance
from datetime import date

# L1 — default (no raw scores, single sentence)
r = get_guidance(chart, domain="career", depth="L1", dashas=dashas)
print(r.signal_display)   # ●●●○○
print(r.timing_label)     # "Mixed — lean in"
print(r.summary)          # "Some supporting factors are present; preparation will help."
print(r.disclaimer)       # "This is reflective guidance, not financial advice."

# L2 — factor bullets (on "Why?" click)
r2 = get_guidance(chart, domain="career", depth="L2", dashas=dashas)
print(r2.factors)         # ["Saturn period activates career themes...",
                           #  "Your chart holds moderate potential here..."]

# L3 — full technical trace (explicit opt-in only, resets each session)
r3 = get_guidance(chart, domain="career", depth="L3",
                  dashas=dashas, l3_opted_in=True)
print(r3.technical_detail)  # raw scores, rule firings, Shadbala, AV
```

---

## Score → Signal Mapping

| Engine score | Signal | Timing label |
|-------------|--------|-------------|
| ≥ +3.0 | ●●●●● | Clear passage |
| +1.5 to +3 | ●●●●○ | Favourable |
| +0.5 to +1.5 | ●●●○○ | Mixed — lean in |
| −0.5 to +0.5 | ●●○○○ | Neutral |
| −1.5 to −0.5 | ●○○○○ | Navigate carefully |
| ≤ −1.5 | ○○○○○ | Significant resistance |

---

## Privacy

```python
from src.privacy.consent_engine import grant_consent, right_to_erasure
from src.privacy.family_consent import add_family_member, can_run_compatibility

# Consent (GDPR Art.7)
grant_consent("user1", "core", jurisdiction="EU")

# Right to erasure (GDPR Art.17) — cascades all tables
result = right_to_erasure("user1")   # → {"erased": True, "tombstone": True}

# Family consent — per-person principal
add_family_member("owner", "partner", "spouse", has_consented=True)
ok, reason = can_run_compatibility("owner", "partner")

# Age gate
from src.privacy.consent_engine import check_age_eligibility
ok, msg = check_age_eligibility(2010)  # → (False, "requires 18+")
```

---

## Fatalism Filter

```python
from src.guidance.fatalism_filter import filter_output, is_safe

# Rewrites deterministic language, preserves signal direction
filter_output("financial ruin is possible")
# → "a period requiring financial caution is possible"

filter_output("career will be destroyed by afflictions")
# → "career may be significantly affected by challenges"

is_safe("Conditions are supportive for career decisions.")  # → True
is_safe("This period is doomed to failure.")               # → False
```

---

## Domain Weights

```python
from src.calculations.domain_weighting import compute_domain_lpi, DOMAINS

# Career: D10 × 35% (dominant)
r = compute_domain_lpi(chart, dashas, date.today(), "career")
print(r.domain_score, r.top_houses)

# All domains
print(DOMAINS)
# ['career', 'marriage', 'mind_psychology', 'wealth',
#  'health_longevity', 'spirituality', 'children']
```

| Domain | Dominant axis | Primary house |
|--------|--------------|--------------|
| career | D10 × 35% | H10 |
| marriage | D9 × 35% | H7 |
| mind_psychology | Chandra × 40% | H4 |
| wealth | D1 × 35% | H2 |
| health_longevity | D1 × 45% | H8 |
| spirituality | D9 × 45% | H9 |

---

## Feedback & Safety

```python
from src.feedback.feedback_loop import record_feedback
from src.feedback.harm_escalation import check_usage_pattern
from src.feedback.dependency_prevention import log_session, check_dependency_status

# Record feedback — 'concerning' → human review queue (never auto-retrain)
r = record_feedback("user1", "chart1", "career", "concerning", "2026-03-21")
print(r.queued_for_review)  # True

# Usage safety check
signal = check_usage_pattern({"health_longevity": 4}, 3, 8, [])
if signal.show_to_user:
    print(signal.prompt)    # gentle prompt — no crisis resources

# Dependency monitoring — nudge at 3/day or 15/week
log_session("user1", "career")
status = check_dependency_status("user1")
if status.show_nudge:
    print(status.nudge_text)
```

---

## Reflection Mode (Socratic)

```python
from src.guidance.reflection_prompts import get_reflection_prompt
from src.guidance.educational_layer import get_educational_content

# Converts guidance to a question
q = get_reflection_prompt("career", "Navigate carefully")
# → "What aspect of your career feels most like it needs patience right now?"

# Educational context — no raw scores
for item in get_educational_content("career"):
    print(item.topic, "—", item.classical_source)
# → "Dasha activation — BPHS Ch.46"
# → "Upachaya houses — BPHS Ch.7"
```

---

## Session History

| Phase | Sessions | Status | Key deliverables |
|-------|----------|--------|-----------------|
| 1 — Pilot | 1–10 | ✅ | Ephemeris, D1 scoring, FastAPI, Streamlit, Docker |
| 2 — Features | 11–19 | ✅ | Kundali Milan, PDF, Jaimini, KP, Tajika, API v2 |
| 3 — Production | 20–27 | ✅ | PostgreSQL, Redis, Celery, JWT, CI/CD, Kubernetes |
| 4 — Pressure Engine | 28–32 | ✅ | LPI v1, Argala, Graha Yuddha, Scoring v2 |
| 5 — Workbook Parity | 33–40 | ✅ | 5-axis scoring, Rule interactions, LPI v2, Scoring v3 |
| 6 — Classical Depth | 41–48 | ✅ | Ishta/Kashta, Longevity, Yogini Dasha, 200+ Yogas |
| 7 — Workbook Complete | 49–56 | ✅ | 12-state Sayanadi, Panchadha Maitri, Dig Bala |
| 8 — PVRNR Textbook | 57–63 | ✅ | Orb strength, Yoga fructification, Stronger-of-two |
| 9 — Synthesis Layer | 64–70 | ✅ | Dominance engine, Promise/Manifestation, Confidence |
| 10 — Language & Safety | 71–75 | ✅ | score_to_language, fatalism_filter, explainability |
| 11 — Privacy & Legal | 76–78 | ✅ | GDPR consent+erasure, family consent, data minimisation |
| 12 — Consumer Frontend | 79–83 | ✅ | Bloomberg UI, domain cards, timing calendar, onboarding |
| 13 — Feedback | 84–86 | ✅ | Human-supervised queue, harm escalation, dependency |
| 14 — Maturity | 87–90 | ✅ | Educational layer, reflection prompts, practitioner handoff |

---

## Non-Negotiable Design Constraints

1. Raw LPI and house scores never reach consumers at L1 or L2
2. L3 opt-in resets each session — no persistent technical mode
3. Signal system is 5-bar only — no percentages, no star ratings
4. All guidance uses possibility language, never deterministic claims
5. Feedback loop is human-supervised — no automated parameter changes
6. Right-to-erasure cascade removes all data and writes tombstone
7. Family charts require per-person explicit consent
8. No streak mechanics, no engagement loops, no unsolicited notifications
9. Dependency nudge at ≥ 3 sessions/day or ≥ 15/week
10. Practitioner referral available when confidence flags "Uncertain"

---

## Stack

| Layer | Technology |
|-------|-----------|
| Ephemeris | pyswisseph (Lahiri / Raman / KP / Fagan-Bradley) |
| Backend | FastAPI + Celery + Redis |
| Database | SQLite → PostgreSQL + consent/erasure/feedback tables |
| Analyst UI | Streamlit (10-tab, internal) |
| Consumer UI | Next.js 14 + TypeScript + Tailwind |
| Mobile | FastAPI /mobile router (React Native shell) |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT (multi-user) |
| CI/CD | GitHub Actions |
| Privacy | GDPR Art.7+17 · DPDP · CCPA/CPRA |
