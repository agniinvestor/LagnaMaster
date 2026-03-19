# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook into a deterministic, auditable web app.

**532 tests passing | Sessions 1–22 complete**

## Quick Start (Docker)

```
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
docker compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI docs | http://localhost:8000/docs |

## Quick Start (Local)

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

## Streamlit Cloud

Entry point: `streamlit_app.py` (repo root). Set this in your Streamlit Cloud app settings.

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
| 17 | Compatibility Score | 20 |
| 18 | API v2 endpoints | 15 |
| 19 | UI overhaul: 10-tab layout | 20 |
| 20 | PostgreSQL + Redis 3-tier caching | 35 |
| 21 | Celery async workers + full UI wiring | 25 |
| 22 | Multi-user JWT auth | 25 |
| 23 | GitHub Actions CI/CD | 🔲 Next |

**Total: 532/532 tests passing**

See [PLAN.md](PLAN.md) · [DOCS.md](DOCS.md) · [docs/SESSION_LOG.md](docs/SESSION_LOG.md)

## API Auth

```
POST /auth/register    create account
POST /auth/login       get access + refresh tokens
POST /auth/refresh     renew access token
GET  /auth/me          current user profile
POST /auth/logout      client-side (204)
```

All chart endpoints accept `Authorization: Bearer <access_token>`.
