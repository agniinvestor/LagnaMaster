# LagnaMaster

Vedic Jyotish birth chart scoring platform — fully production-ready.

**![CI](https://github.com/agniinvestor/LagnaMaster/actions/workflows/ci.yml/badge.svg) 657 tests passing | Sessions 1–27 complete ✅**

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
| Next.js UI | cd frontend && npm run dev → :3000 |

## Local

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest tests/ -q          # 657 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```

## Kubernetes (Helm)

```
kubectl create secret generic lagnamaster-secrets \
  --from-literal=JWT_SECRET=<secret> \
  --from-literal=PG_DSN=postgresql://... \
  --from-literal=REDIS_URL=redis://...
helm install lagnamaster ./helm/lagnamaster
```

## Sessions

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1–10 | Pilot — ephemeris → panchanga | 222 |
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
| 21 | Celery async workers + full UI | 25 |
| 22 | Multi-user JWT auth | 25 |
| 23 | GitHub Actions CI/CD | 20 |
| 24 | Kubernetes + Helm chart | 20 |
| 25 | Next.js 14 frontend | 30 |
| 26 | KP/Jaimini school gates | 22 |
| 27 | Monte Carlo Celery chord scaling | 18 |

**Total: 657/657 tests passing**

## Stack

| Layer | Implementation |
|-------|---------------|
| Ephemeris | pyswisseph (Moshier / DE441) |
| Calculations | 19 Jyotish modules (Parashari + KP + Jaimini) |
| Scoring | 22-rule BPHS engine |
| Backend | FastAPI + Celery |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Cache | Redis 3-tier |
| Auth | JWT multi-user + school preference |
| UI | Streamlit 10-tab + Next.js 14 |
| Deploy | Docker Compose / Kubernetes + Helm |
| CI/CD | GitHub Actions → GHCR |

See [PLAN.md](PLAN.md) · [DOCS.md](DOCS.md) · [docs/SESSION_LOG.md](docs/SESSION_LOG.md)
