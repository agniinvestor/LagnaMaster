# LagnaMaster

Vedic Jyotish birth chart scoring platform — pyswisseph + FastAPI + Streamlit.

**401 tests passing | Sessions 1–18 complete**

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
PYTHONPATH=. pytest tests/ -q          # 401 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

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

See [PLAN.md](PLAN.md), [DOCS.md](DOCS.md), and [docs/SESSION_LOG.md](docs/SESSION_LOG.md).
