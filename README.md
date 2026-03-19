# LagnaMaster

Vedic Jyotish birth chart scoring platform — pyswisseph + FastAPI + Streamlit.

**421 tests passing | Sessions 1–19 complete**

## Quick Start (Docker)

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git && cd LagnaMaster
docker compose up --build
# Streamlit UI:  http://localhost:8501
# FastAPI docs:  http://localhost:8000/docs
```

## Quick Start (Local)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q          # 421 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

## What It Does

1. Accepts birth date, time, and geographic coordinates
2. Computes sidereal planet positions via **pyswisseph** (Lahiri ayanamsha)
3. Runs **19 Jyotish calculation modules** across the full Parashari + Jaimini + KP spectrum
4. Scores **22 BPHS rules × 12 houses** → domain score in [−10, +10] per house
5. Renders a **12-tab Streamlit UI** surfacing all modules
6. Stores every chart in **SQLite** (immutable insert pattern)
7. Serves results via **FastAPI** REST

## Session Progress

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1–10 | Pilot: ephemeris → scoring → API → UI → Docker → panchanga | 222 |
| 11 | Pushkara Navamsha + Monte Carlo birth-time sensitivity | 30 |
| 12 | Kundali Milan — Ashtakoot 36-point compatibility | 25 |
| 13 | PDF Chart Report (reportlab) | 15 |
| 14 | Jaimini Chara Dasha (sign-based, 9 MDs) | 20 |
| 15 | Varga Divisional Charts (D2/D3/D4/D7/D9/D10/D12/D60) | 25 |
| 16 | Sapta Varga Vimshopak Bala (20-pt weighted dignity) | 20 |
| 17 | KP Sub-lord System (Star/Sub/Sub-Sub + significators) | 22 |
| 18 | Varshaphala — Annual Solar Return, Muntha, Tajika aspects | 22 |
| 19 | **Streamlit 12-tab UI — all S1-S18 modules integrated** | 20 |

## Streamlit UI — 12 Tabs

| Tab | What you see |
|-----|-------------|
| 📊 Chart | Birth chart SVG + Panchanga + Shadbala + D9 + Pushkara flags + PDF download |
| 🏠 Domain Scores | 12-house scores bar chart with rating badges |
| 🧘 Yogas | Classical yoga cards grouped by category |
| 🔢 Ashtakavarga | Sarvashtakavarga bar + per-planet bindu grids |
| ⏱ Dashas | Vimshottari + Chara Dasha current period and full table |
| 🌍 Transits | Sade Sati phase + Guru-Chandal flag + per-planet AV bindus |
| 📐 Varga Charts | D2–D60 South Indian SVG grids + all-division summary |
| ⚖️ Vimshopak | Sapta Varga 20-pt dignity ranking + per-planet breakdown |
| 🔑 KP Analysis | Sub-lord table + house cusp sub-lords + significators |
| 🌟 Annual Chart | Varshaphala solar return + Muntha + Tajika aspects |
| 💑 Kundali Milan | Ashtakoot 36-pt compatibility for two charts |
| 📋 Rule Detail | Per-house breakdown of all 22 BPHS rules |

## API

```
POST /charts              # compute + store chart
GET  /charts              # list recent charts
GET  /charts/{id}         # retrieve chart
GET  /charts/{id}/scores  # full 22-rule house score breakdown
GET  /health              # health check
```

See [PLAN.md](PLAN.md), [DOCS.md](DOCS.md), and [docs/SESSION_LOG.md](docs/SESSION_LOG.md).
