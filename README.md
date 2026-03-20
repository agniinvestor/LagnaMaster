# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook
into a deterministic, auditable Python web application.

**~920 tests | Sessions 1–70 complete | 63 calc modules | Engine v3.0.0**

---

## Quick Start

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI + Swagger | http://localhost:8000/docs |

**Local:**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ulimit -n 4096   # macOS: raise file descriptor limit
PYTHONPATH=. pytest tests/ -q -p no:warnings
```

---

## What It Does

1. Computes sidereal planet positions via **pyswisseph** (Lahiri, Raman, KP, Fagan-Bradley)
2. Runs 23 BPHS scoring rules × 12 houses × 5 lagna axes
3. Applies full avastha (12-state Sayanadi), Panchadha Maitri, Lagnesh modifier, Dig Bala
4. Computes 7-layer **Life Pressure Index** with varga agreement confidence
5. Evaluates yoga fructification (orb, affliction, Amsa level per PVRNR p147)
6. **Synthesis layer**: dominance hierarchy, promise vs manifestation, domain weighting
7. Multi-planet chains: stelliums, dispositor chains, mutual receptions
8. House-type modulation (upachaya age effect, malefics in 3/6/11)
9. Interpretive confidence model with expert-review flags
10. Empirical event log with per-rule accuracy tracking

---

## Synthesis Layer (Phase 9)

```python
from src.calculations.dominance_engine  import compute_dominance_factors, dominant_theme
from src.calculations.promise_engine    import compute_full_promise
from src.calculations.domain_weighting  import compute_domain_lpi
from src.calculations.confidence_model  import compute_confidence
from src.calculations.chart_exceptions  import detect_chart_exceptions

# What dominates this chart right now?
dom = compute_dominance_factors(chart, dashas, on_date)
print(dominant_theme(chart, dashas, on_date))
# → "Mercury MD (D1=−0.50); chart tone: Mixed Negative"

# Does the natal chart even promise career success?
promise = compute_full_promise(chart, dashas, on_date)
h10 = promise[10]
print(f"H10 Career: {h10.promise.promise_strength} / {h10.manifestation_timing}")
# → "H10 Career: Weak / Future"

# Career-specific axis weights (D10 dominates)
career = compute_domain_lpi(chart, dashas, on_date, "career")
print(f"Career domain score: {career.domain_score:+.2f}")

# How confident is the interpretation?
conf = compute_confidence(chart)
print(f"Global confidence: {conf.global_confidence:.2f}")
print(f"Expert review needed: {conf.requires_expert_review}")

# Any exceptional chart conditions?
exc = detect_chart_exceptions(chart)
print(exc.exception_summary)
```

---

## Domain-Specific Axis Weights (PVRNR p181)

| Domain | Dominant axis | Primary house |
|--------|--------------|--------------|
| career | D10 × 35% | H10 |
| marriage | D9 × 35% | H7 |
| mind_psychology | Chandra × 40% | H4 |
| wealth | D1 × 35% | H2 |
| health_longevity | D1 × 45% | H8 |
| spirituality | D9 × 45% | H9 |
| children | D1 × 25% + Dasha × 20% | H5 |

---

## Promise vs Manifestation

Classical principle (PVRNR, applied throughout):
*"If the promise is absent, the dasha cannot produce the result."*

| Promise | Dasha | Transit | Timing |
|---------|-------|---------|--------|
| ✓ Strong | ✓ Active | ✓ Supported | **Now** (p~0.80) |
| ✓ Present | ✓ Active | ✗ | **Soon** (p~0.55) |
| ✓ Present | ✗ | — | **Future** (p~0.20) |
| ✗ Absent | any | any | **Blocked** (p~0.05) |

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
| 9 — Synthesis Layer | 64–70 | Dominance engine, Promise/Manifestation, Domain weights, Planet chains, House modulation, Confidence model, Exception detection |

---

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Lahiri/Raman/KP/Fagan-Bradley) |
| Backend | FastAPI + Celery workers |
| Database | SQLite (→ PostgreSQL) + Empirica event log |
| Cache | Redis (optional) |
| UI | Streamlit (10-tab) + Next.js 14 |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT (multi-user) |
| CI/CD | GitHub Actions |
