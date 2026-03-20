# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook
into a deterministic, auditable Python web application.

**743 tests passing | Sessions 1–40 complete | Engine v3.0.0**

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

**Local (no Docker):**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q          # 743 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run streamlit_app.py
```

---

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri ayanamsha)
3. Runs 23 BPHS scoring rules × 12 houses × 5 lagna axes (D1/Chandra/Surya/D9/D10)
4. Computes the 7-layer **Life Pressure Index** per house
5. Detects Raja/Dhana/Viparita/Neecha Bhanga yogas with dasha weighting
6. Produces Rasi Drishti, Bhavat Bhavam, Vimshopaka Bala, D60 Shastiamsha
7. Stores every chart in SQLite (immutable insert pattern)
8. Serves results via FastAPI REST + Streamlit UI + Next.js frontend

---

## Life Pressure Index

Full 7-layer synthesis per house:

```
LPI = D1×35% + Chandra×15% + Surya×10% + D9×15% + D10×10% + Dasha×10% + Gochar×5%
```

```python
from src.calculations.scoring_v3 import score_chart_v3

result = score_chart_v3(chart, dashas, on_date=date.today(), school="parashari")
print(result.summary())

# Per-house full index with RAG and confidence
for h, hl in result.lpi.houses.items():
    print(f"H{h}: {hl.full_index:+.2f} [{hl.rag}] {hl.confidence}")

# Domain balance
print(result.lpi.domain_balance)  # {Dharma: -0.71, Artha: -0.63, ...}

# Scenario explorer
from src.calculations.scenario import compare_scenarios
compare_scenarios(chart, [("Sun to Leo", {"Sun": {"longitude": 120.0}})], dashas)
```

---

## Regression Fixture

All 743 tests validate against the **1947 India Independence Chart**:

| Field | Value |
|-------|-------|
| Birth | 1947-08-15 00:00 IST, New Delhi |
| Lagna | 7.7286° **Taurus** |
| Sun | 27.989° Cancer |
| Ayanamsha | Lahiri (~23.1489°) |
| Arudha Lagna | Virgo (H5) |
| D9 Lagna | Pisces |
| Baaladi Sun | Bala (infant) — even-sign reversal verified |

---

## Jyotish Coverage

| Module | Status |
|--------|--------|
| D1 scoring — 23 rules (R01–R23) | ✅ |
| Chandra Lagna / Surya Lagna scoring | ✅ |
| D9 Navamsha / D10 Dashamsha scoring | ✅ |
| Karakamsha (soul axis) | ✅ |
| 30-pair Rule Interaction Engine | ✅ |
| 7-layer Life Pressure Index | ✅ |
| All 12 Arudha Padas (AL, A2–A12, DL, UL) | ✅ |
| Vimshopaka Bala (16 vargas, max 20 pts) | ✅ |
| D60 Shastiamsha (60 division names) | ✅ |
| Raja + Dhana Yogas (13 pairs) | ✅ |
| Viparita Raja + Neecha Bhanga | ✅ |
| Rasi Drishti (12×12 sign aspects) | ✅ |
| Bhavat Bhavam | ✅ |
| Baaladi avastha (even-sign reversal) | ✅ |
| Sayanadi avastha (12 mood states) | ✅ |
| Shadbala | ✅ |
| Ashtakavarga (SAV + R23) | ✅ |
| Vimshottari + Narayana + Jaimini Chara Dasha | ✅ |
| Gochara + Sade Sati | ✅ |
| KP Significators | ✅ |
| Varshaphala (Tajika) | ✅ |
| Kundali Milan (36-point compatibility) | ✅ |
| Monte Carlo birth-time sensitivity | ✅ |
| Narrative report generator | ✅ |
| Scenario / counterfactual explorer | ✅ |

---

## API Reference

```
POST /charts                    # compute + store chart
GET  /charts                    # list recent charts
GET  /charts/{id}               # retrieve chart
GET  /charts/{id}/scores        # full 23-rule breakdown
GET  /health                    # system health
POST /auth/register             # register user
POST /auth/login                # get JWT tokens
GET  /user/school               # get scoring school (Parashari/KP/Jaimini)
PUT  /user/school               # set scoring school
```

---

## Session Progress

| Phase | Sessions | Tests | Key deliverables |
|-------|----------|-------|-----------------|
| 1 — Pilot | 1–10 | 222 | Ephemeris, 7 calc modules, D1 scoring, FastAPI, SQLite, Streamlit, Docker |
| 2 — Features | 11–19 | 225 | Pushkara, Kundali Milan, PDF, Jaimini, KP, Tajika, Compatibility, API v2, 12-tab UI |
| 3 — Production | 20–27 | 210 | PostgreSQL, Redis, Celery, JWT, CI/CD, Kubernetes, Next.js, School gates, Monte Carlo |
| 4 — Pressure Engine | 28–32 | 36 | Functional roles, Avastha, LPI v1, Argala, Graha Yuddha, Scoring v2 |
| 5 — Workbook Parity | 33–40 | 50 | Multi-lagna, 5-axis scoring, Rule interactions, 7-layer LPI, Divisional charts, Yogas, Avastha fix, Scoring v3 |

**Total: 743 tests | Engine v3.0.0 | ~160/178 workbook sheets**

---

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Lahiri) |
| Backend | FastAPI + Celery workers |
| Database | SQLite (→ PostgreSQL via PG_DSN) |
| Cache | Redis (optional) |
| UI | Streamlit (10-tab) + Next.js 14 |
| Deploy | Docker Compose + Kubernetes Helm |
| Auth | JWT (multi-user) |
| CI/CD | GitHub Actions |

## Environment Variables

| Variable | Default | Notes |
|----------|---------|-------|
| PG_DSN | — | Absent = SQLite |
| REDIS_URL | redis://localhost:6379/0 | Empty = disabled |
| CACHE_VERSION | 1 | Bump to bust scores |
| JWT_SECRET | dev-secret | **Change in prod** |
| ENABLE_KP | 1 | 0 = disable |
| ENABLE_JAIMINI | 1 | 0 = disable |
