# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook into a deterministic, auditable web app.

**482 tests passing | Sessions 1–20 complete**

---

## Quick Start (Docker)

```
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
# Streamlit UI: http://localhost:8501
# FastAPI docs: http://localhost:8000/docs
```

## Quick Start (Local)

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q          # 482 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

## With PostgreSQL + Redis (production mode)

```
export PG_DSN=postgresql://lagnamaster:secret@localhost:5432/lagnamaster
export REDIS_URL=redis://localhost:6379/0
alembic upgrade head
PYTHONPATH=. uvicorn src.api.main_v2:app --reload
```

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri ayanamsha by default)
3. Runs 19 Jyotish modules (dignity → panchanga → KP → Tajika → compatibility)
4. Scores **22 BPHS rules × 12 houses** → domain score in [−10, +10] per house
5. Exports printable **PDF chart reports** via reportlab
6. Stores charts in **SQLite** (dev) or **PostgreSQL** (production)
7. Serves results via **FastAPI** REST + **Streamlit** 10-tab UI
8. Caches ephemeris and scores in **Redis** (optional, graceful fallback)

## Regression Fixture

All modules are validated against the **1947 India Independence Chart**:

| Field | Value |
|-------|-------|
| Birth | 1947-08-15 00:00 IST, New Delhi |
| Lagna | 7.7286° **Taurus** |
| Sun | 27.989° Cancer |
| Special | Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer |
| Ayanamsha | Lahiri (~23.1489°) |

## Sessions

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1–10 | Pilot complete (ephemeris → panchanga) | 222 |
| 11 | Pushkara Navamsha + Monte Carlo | 30 |
| 12 | Kundali Milan (Ashtakoot 36-pt) | 25 |
| 13 | PDF Chart Report (reportlab) | 15 |
| 14 | Jaimini Chara Dasha | 20 |
| 15 | KP Sub-lord & Significators | 22 |
| 16 | Tajika Annual Chart | 18 |
| 17 | Compatibility Score (composite) | 20 |
| 18 | API v2 endpoints (yogas, report, milan) | 15 |
| 19 | UI overhaul: 10-tab layout | 20 |
| 20 | PostgreSQL migration + Redis 3-tier caching | 35 |
| 21 | Celery async workers | 🔲 Next |

**Total: 482/482 tests passing**

See [PLAN.md](PLAN.md) for roadmap and [DOCS.md](DOCS.md) for module reference.

## API

```
POST /charts                        compute + store chart
GET  /charts                        list recent charts
GET  /charts/{id}                   retrieve chart
GET  /charts/{id}/scores            22-rule house breakdown
GET  /charts/{id}/yogas             detected yoga list
GET  /charts/{id}/report            download PDF
GET  /charts/{id}/milan/{partner}   Kundali Milan score
GET  /health                        DB + cache status
```
