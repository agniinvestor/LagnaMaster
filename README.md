# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook into a deterministic, auditable web app.

**93 tests passing | Sessions 1–5 complete**

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
3. Runs 7 Jyotish calculation modules (dignity, nakshatra, friendship, house lord, chara karak, narayana dasha, shadbala)
4. Scores **22 BPHS rules × 12 houses** → domain score in [−10, +10] per house
5. Stores every chart in **SQLite** (immutable insert pattern)
6. Serves results via **FastAPI** REST + **Streamlit** UI

---

## Regression Fixture

All modules are validated against the **1947 India Independence Chart**:

| Field | Value |
|-------|-------|
| Birth | 1947-08-15 00:00 IST, New Delhi |
| Lagna | 7.7286° **Taurus** |
| Sun | 27.989° Cancer |
| Special | Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer |
| Ayanamsha | Lahiri (~23.1489° at this epoch) |

---

## Stack

| Layer | Pilot (current) | Production (v2) |
|-------|-----------------|-----------------|
| Ephemeris | pyswisseph Moshier | + DE441 data files |
| Backend | FastAPI (sync) | + Celery workers |
| Database | SQLite | PostgreSQL |
| UI | Streamlit | Next.js |
| Deploy | Docker Compose | Kubernetes |
| Auth | Single user | Multi-user JWT |

---

## API Reference

```bash
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
|---------|------------|--------|-------|
| 1 | `src/ephemeris.py` — pyswisseph wrapper | ✅ | 14 |
| 2 | `src/calculations/` — 7 Jyotish modules | ✅ | 36 |
| 3 | `src/scoring.py` + `src/api/` + `src/db.py` | ✅ | 20 |
| 4 | `src/ui/app.py` — Streamlit UI | ✅ | 6 |
| 5 | Docker Compose + integration tests | ✅ | 17 |
| 6 | End-to-end smoke test + accuracy baseline | 🔲 | — |

**Total: 93/93 tests passing**

See [PLAN.md](PLAN.md) for the full build plan and [DOCS.md](DOCS.md) for module reference.

---

## Known Bugs (Deferred to Session 7)

| ID | Severity | Description |
|----|----------|-------------|
| E-1 | Critical | JDN Gregorian +0.5 day correction missing |
| A-2 | High | Mercury direction uses wrong row reference |

Bugs P-1, P-4, N-1, S-2 were fixed in Sessions 1–2.
