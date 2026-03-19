# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook into a deterministic, auditable web app.

**277 tests passing | Sessions 1–12 complete**

---

## Quick Start (Docker)

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI + Swagger | http://localhost:8000/docs |

Data persists in a Docker named volume (`chart_data`). To wipe: `docker compose down -v`.

---

## Quick Start (Local)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run tests
PYTHONPATH=. pytest tests/ -q

# Start API
PYTHONPATH=. uvicorn src.api.main:app --reload

# Start UI (separate terminal)
PYTHONPATH=. streamlit run src/ui/app.py
```

Or with Make:

```bash
make install
make run-api    # terminal 1
make run-ui     # terminal 2
make test
```

---

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri ayanamsha by default)
3. Runs 13 Jyotish calculation modules (dignity, nakshatra, friendship, house lord,
   chara karak, narayana dasha, shadbala, vimshottari dasha, yogas, ashtakavarga,
   gochara, panchanga, pushkara navamsha)
4. Scores **22 BPHS rules × 12 houses** → domain score in [−10, +10] per house
   (R21 Pushkara Navamsha now live: +0.5 when bhavesh is in PN zone)
5. Runs **Monte Carlo sensitivity analysis** — 100 samples ±30 min, <8s on 4 cores
6. Stores every chart in **SQLite** (immutable insert pattern)
7. Serves results via **FastAPI** REST + **Streamlit** 8-tab UI

---

## Regression Fixture

All modules are validated against the **1947 India Independence Chart**:

| Field | Value |
|-------|-------|
| Birth | 1947-08-15 00:00 IST, New Delhi |
| Lagna | 7.7286° **Taurus** |
| Sun | 27.989° Cancer — Pushkara Navamsha ✅ |
| Moon | 3.983° Cancer — Pushkara Navamsha ✅ |
| Special | Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer |
| Ayanamsha | Lahiri (~23.1489° at this epoch) |

---

## Stack

| Layer | Pilot (current) | Production (v2) |
|-------|----------------|----------------|
| Ephemeris | pyswisseph Moshier | + DE441 data files |
| Backend | FastAPI (sync) | + Celery workers |
| Database | SQLite | PostgreSQL |
| UI | Streamlit (8 tabs) | Next.js |
| Deploy | Docker Compose | Kubernetes |
| Auth | Single user | Multi-user JWT |

---

## API Reference

```
POST /charts              # compute + store chart
GET  /charts              # list recent charts (?limit=20)
GET  /charts/{id}         # retrieve chart
GET  /charts/{id}/scores  # full 22-rule house score breakdown
GET  /health              # health check
```

Example — create a chart:

```bash
curl -X POST http://localhost:8000/charts \
  -H "Content-Type: application/json" \
  -d '{"year":1947,"month":8,"day":15,"hour":0.0,"lat":28.6139,"lon":77.2090}'
```

---

## Session Progress

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 1 | `src/ephemeris.py` — pyswisseph wrapper | ✅ | 14 |
| 2 | `src/calculations/` — 7 Jyotish modules | ✅ | 36 |
| 3 | `src/scoring.py` + `src/api/` + `src/db.py` | ✅ | 20 |
| 4 | `src/ui/app.py` — Streamlit UI | ✅ | 6 |
| 5 | Docker Compose + integration tests | ✅ | 17 |
| 6 | Vimshottari dasha + South Indian SVG | ✅ | 20 |
| 7 | Yogas (13 types) + UI tab | ✅ | 14 |
| 8 | Ashtakavarga + E-1/A-2 regression guards | ✅ | 26 |
| 9 | Gochara transits + Sade Sati | ✅ | 29 |
| 10 | Panchanga + Navamsha D9 | ✅ | 40 |
| 11 | Pushkara Navamsha (R21 live) + Monte Carlo sensitivity | ✅ | 30 |
| 12 | Kundali Milan — Ashtakoot 36-pt + Mangal Dosha + 9th tab | ✅ | 25 |
| 13 | PDF chart report export | 🔲 Next | — |

**Total: 277/277 tests passing**

See [PLAN.md](PLAN.md) for the full build plan and [DOCS.md](DOCS.md) for module reference.

---

## Known Bugs

All 6 original audit bugs + R21 stub resolved. No open issues.
