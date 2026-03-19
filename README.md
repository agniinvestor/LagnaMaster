# LagnaMaster

Vedic Jyotish birth chart scoring platform. Transforms a 178-sheet Excel workbook into a deterministic, auditable web app.

**![CI](https://github.com/agniinvestor/LagnaMaster/actions/workflows/ci.yml/badge.svg) 627 tests passing | Sessions 1–25 complete**

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
| Next.js UI | http://localhost:3000 (cd frontend && npm run dev) |

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
| 23 | GitHub Actions CI/CD | 20 |
| 24 | Kubernetes + Helm chart | 20 |
| 25 | Next.js frontend (TypeScript + Tailwind) | 30 |
| 26 | KP/Jaimini school gates | 🔲 Next |

**Total: 627/627 tests passing**

See [PLAN.md](PLAN.md) · [DOCS.md](DOCS.md) · [docs/SESSION_LOG.md](docs/SESSION_LOG.md)

## Stack

| Layer | Current |
|-------|---------|
| Ephemeris | pyswisseph (Moshier / DE441) |
| Backend | FastAPI + Celery |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Cache | Redis 3-tier |
| Auth | JWT multi-user |
| UI | Streamlit 10-tab + **Next.js 14** |
| Deploy | Docker Compose / **Kubernetes + Helm** |
| CI/CD | GitHub Actions → GHCR |
