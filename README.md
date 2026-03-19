# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook into a deterministic, auditable web app.

**447 tests passing | Sessions 1–19 complete**

---

## Quick Start (Docker)

```
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

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q          # 447 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

Or with Make:

```
make install
make run-api    # terminal 1
make run-ui     # terminal 2
make test
```

---

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri ayanamsha by default)
3. Runs 19 Jyotish calculation modules (dignity, nakshatra, friendship, house lord, chara karak, narayana dasha, shadbala, vimshottari dasha, yogas, ashtakavarga, gochara, panchanga, pushkara navamsha, kundali milan, PDF report, Jaimini chara dasha, KP significators, Tajika annual chart, compatibility scoring)
4. Scores **22 BPHS rules × 12 houses** → domain score in [−10, +10] per house
5. Stores every chart in **SQLite** (immutable insert pattern)
6. Serves results via **FastAPI** REST + **Streamlit** UI
7. Exports printable PDF chart reports via **reportlab**

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

```
POST /charts              # compute + store chart
GET  /charts              # list recent charts (?limit=20)
GET  /charts/{id}         # retrieve chart
GET  /charts/{id}/scores  # full 22-rule house score breakdown
GET  /charts/{id}/yogas   # detected yoga list
GET  /charts/{id}/report  # download PDF report
GET  /health              # health check
```

---

## Session Progress

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 1 | `src/ephemeris.py` — pyswisseph wrapper | ✅ | 14 |
| 2 | `src/calculations/` — 7 core Jyotish modules | ✅ | 36 |
| 3 | `src/scoring.py` + `src/api/` + `src/db.py` | ✅ | 20 |
| 4 | `src/ui/app.py` — Streamlit UI | ✅ | 6 |
| 5 | Docker Compose + integration tests | ✅ | 17 |
| 6 | `vimshottari_dasa.py` + `chart_visual.py` (South Indian SVG) | ✅ | 20 |
| 7 | `yogas.py` (13 yoga types) + Yogas tab | ✅ | 14 |
| 8 | `ashtakavarga.py` + AV tab + E-1/A-2 regression guards | ✅ | 26 |
| 9 | `gochara.py` (transit analysis, Sade Sati) + Transits tab | ✅ | 29 |
| 10 | `panchanga.py` (5-limb almanac) + Navamsha D9 chart | ✅ | 40 |
| 11 | `pushkara_navamsha.py` + Monte Carlo ±30 min birth time | ✅ | 30 |
| 12 | `kundali_milan.py` — Ashtakoot 36-point compatibility | ✅ | 25 |
| 13 | `src/report.py` — PDF chart report (reportlab) | ✅ | 15 |
| 14 | `jaimini_chara_dasha.py` — sign-based Jaimini dasha | ✅ | 20 |
| 15 | `kp_significators.py` — KP sub-lord & significator engine | ✅ | 22 |
| 16 | `tajika.py` — Tajika annual (solar return) chart | ✅ | 18 |
| 17 | `compatibility_score.py` — composite compatibility index | ✅ | 20 |
| 18 | API v2: `/charts/{id}/yogas`, `/charts/{id}/report` endpoints | ✅ | 15 |
| 19 | UI overhaul: 10-tab layout + Milan tab + KP tab + Tajika tab | ✅ | 20 |
| 20 | PostgreSQL migration + Redis caching | 🔲 Next | — |

**Total: 447/447 tests passing**

See [PLAN.md](PLAN.md) for the full build plan and [DOCS.md](DOCS.md) for module reference.

---

## Known Bugs — All Resolved

All 6 bugs from the v5 Excel audit (P-1, P-4, N-1, S-2, E-1, A-2) were fixed in Sessions 1–8. No open bugs.
