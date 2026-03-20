# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook
into a deterministic, auditable Python web application.

**873 tests | Sessions 1–63 complete | 56 calc modules | Engine v3.0.0**

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

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri, Raman, KP, or Fagan-Bradley)
3. Runs 23 BPHS scoring rules × 12 houses × 5 lagna axes (D1/Chandra/Surya/D9/D10)
4. Applies Lagnesh global modifier, Dig Bala continuous scores, full 12-state Sayanadi
5. Computes the 7-layer **Life Pressure Index** with varga agreement confidence flags
6. Evaluates yoga fructification conditions (orb, affliction, dignity, Amsa level)
7. Models Arudha perception (reality vs how the world perceives)
8. Synthesises multi-factor planet effectiveness across all strength measures
9. Detects 200+ yogas with dasha-weighted scoring
10. Records birth-event correlations for empirical accuracy measurement
11. Serves results via FastAPI REST + Streamlit UI + Next.js frontend

---

## Life Pressure Index

```
LPI = D1×35% + Chandra×15% + Surya×10% + D9×15% + D10×10% + Dasha×10% + Gochar×5%
```

```python
from src.calculations.scoring_v3 import score_chart_v3
from src.calculations.varga_agreement import compute_varga_agreement
from src.calculations.yoga_fructification import yoga_fructification_score
from src.calculations.planet_effectiveness import compute_all_effectiveness

result  = score_chart_v3(chart, dashas, on_date=date.today(), school="parashari")
agree   = compute_varga_agreement(chart)
effects = compute_all_effectiveness(chart)

for h, hl in result.lpi.houses.items():
    flag = agree.flag_for(h)
    print(f"H{h}: {hl.full_index:+.2f} [{hl.rag}] {flag}")

# Yoga strength — does it actually deliver?
r = yoga_fructification_score(["Jupiter","Moon"], chart)
print(f"Gaja Kesari: {r.verdict} ({r.fructification_score:.2f})")
print(f"Weaknesses: {r.weaknesses}")

# Planet effectiveness synthesis
for planet, eff in effects.items():
    print(f"{planet}: {eff.label} ({eff.overall:.2f})")
```

---

## Yoga Fructification (PVRNR p147)

Three conditions explicitly stated by PVRNR for a yoga to deliver full results:

1. **Free from functional malefic afflictions** — conjunct functional malefics reduce power
2. **Close conjunction** — within 6° (PVRNR's stated threshold); 8° = weak (Rajiv Gandhi example)
3. **Not combust, debilitated, or in inimical house**

Amsa level (Dasa Varga count) determines the magnitude of results:

| Count | Amsa | Quality |
|-------|------|---------|
| 2 | Paarijataamsa | Moderate |
| 3 | Uttamaamsa | Good |
| 4 | Gopuraamsa | Notable |
| 5 | Simhasanamsa | Distinguished |
| 6 | Paaravataamsa | Excellent |
| 7+ | Devaloka/Brahmaloka/Airaavata | Divine/Supreme |

---

## Stronger-of-Two Framework (PVRNR p194)

Used for dual-lord signs (Scorpio/Aquarius), Narayana Dasha start sign, longevity lords:

```python
from src.calculations.stronger_of_two import stronger_planet, stronger_sign

# Scorpio has dual lords: Mars and Ketu — which is stronger?
lord = stronger_planet("Mars", "Ketu", chart)

# Narayana Dasha: starts from stronger of Lagna or 7th
start_si = stronger_sign(lagna_si, (lagna_si+6)%12, chart)
```

Hierarchy: cotenants > exalt/own > exalted cotenants > rasi aspects > degree advancement.

---

## Regression Fixture — India 1947

All India 1947 regressions pass:

| Phase 8 check | Value | Status |
|---------------|-------|--------|
| Orb Sun–Mercury | same sign Cancer | Conjunction detected |
| Budhaditya fructification | present + close | Partial/Full |
| Cotenant count Sun | 4 (Moon/Mer/Ven/Mars in Cancer) | ✓ |
| AL perception H2 Wealth | both actual/AL weak | Recognized Struggle |

---

## Session History

| Phase | Sessions | Key deliverables |
|-------|----------|-----------------|
| 1 — Pilot | 1–10 | Ephemeris, calc modules, D1 scoring, FastAPI, SQLite, Streamlit, Docker |
| 2 — Features | 11–19 | Pushkara, Kundali Milan, PDF, Jaimini, KP, Tajika, API v2, 12-tab UI |
| 3 — Production | 20–27 | PostgreSQL, Redis, Celery, JWT, CI/CD, Kubernetes, Next.js, School gates |
| 4 — Pressure Engine | 28–32 | Functional roles, Avastha, LPI v1, Argala, Graha Yuddha, Scoring v2 |
| 5 — Workbook Parity | 33–40 | Multi-lagna, 5-axis scoring, Rule interactions, 7-layer LPI, D60, Scoring v3 |
| 6 — Classical Depth | 41–48 | Ishta/Kashta, Longevity, Yogini Dasha, Full KP, 200+ Yogas, Jaimini, Empirica |
| 7 — Workbook Complete | 49–56 | 12-state Sayanadi, Panchadha Maitri, Lagnesh modifier, Dig Bala, Config toggles |
| 8 — PVRNR Textbook | 57–63 | Orb strength, Yoga fructification, Stronger-of-two, AV transit, Arudha perception, PVRNR yogas, Planet effectiveness |

---

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Lahiri/Raman/KP/Fagan-Bradley) |
| Backend | FastAPI + Celery workers |
| Database | SQLite (→ PostgreSQL via PG_DSN) + Empirica event log |
| Cache | Redis (optional) |
| UI | Streamlit (10-tab) + Next.js 14 |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT (multi-user) |
| CI/CD | GitHub Actions |
