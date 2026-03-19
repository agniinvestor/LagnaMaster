# LagnaMaster
Vedic Jyotish birth chart scoring platform.

**312 tests passing | Sessions 1–14 complete**

## Quick Start
```bash
git clone https://github.com/agniinvestor/LagnaMaster.git && cd LagnaMaster
docker compose up --build
# Streamlit UI: http://localhost:8501
# FastAPI docs: http://localhost:8000/docs
```

## Local
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q          # 312 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

## Sessions
| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1–10 | Pilot complete (ephemeris→panchanga) | 222 |
| 11 | Pushkara Navamsha + Monte Carlo | 30 |
| 12 | Kundali Milan (Ashtakoot 36-pt) | 25 |
| 13 | PDF Chart Report (reportlab) | 15 |
| 14 | Jaimini Chara Dasha | 20 |

See PLAN.md and DOCS.md for full reference.
