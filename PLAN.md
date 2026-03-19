# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

## Tech Stack

| Layer | Current | Target |
|-------|---------|--------|
| Ephemeris | pyswisseph Moshier | + DE441 |
| Backend | FastAPI (sync) | + Celery |
| Database | SQLite → PostgreSQL | PostgreSQL |
| Cache | Redis 3-tier | Redis |
| Auth | JWT multi-user (S22) | JWT |
| CI/CD | GitHub Actions (S23) | Actions + GHCR |
| UI | Streamlit 10-tab | Next.js |
| Deploy | Docker Compose | Kubernetes |

## Architecture

```
Birth Data → ephemeris.py → calculations/ (19 modules) → scoring.py
          → report.py → worker.py (Celery) → api/main_v2.py
          → db_pg.py / db.py + cache.py → ui/app.py
Auth:  src/auth.py + src/api/auth_router.py  [S22]
CI/CD: .github/workflows/ci.yml              [S23]
```

## Regression Fixture

1947 India Independence Chart — Lagna=Taurus 7.7286°, Sun=Cancer 27.989°

## Phase 1 — Pilot — Sessions 1–10 ✅ 222/222

S1 ephemeris(14) · S2 calc×7(36) · S3 scoring+api+db(20) · S4 UI(6)
S5 Docker(17) · S6 vimshottari+SVG(20) · S7 yogas(14) · S8 AV(26)
S9 gochara(29) · S10 panchanga+D9(40)

## Phase 2 — Features — Sessions 11–19 ✅ 225/225

S11 pushkara+MC(30) · S12 milan(25) · S13 PDF(15) · S14 jaimini(20)
S15 KP(22) · S16 tajika(18) · S17 compat(20) · S18 APIv2(15) · S19 UI10(20)

## Phase 3 — Production — Sessions 20–27

| S | Deliverable | Status | Tests |
|---|-------------|--------|-------|
| 20 | PostgreSQL + Redis + Alembic | ✅ Done | 35 |
| 21 | Celery + full UI wiring | ✅ Done | 25 |
| 22 | JWT multi-user auth | ✅ Done | 25 |
| 23 | GitHub Actions CI/CD + GHCR | ✅ Done | 20 |
| 24 | Kubernetes manifests + Helm | 🔲 Next | — |
| 25 | Next.js frontend | 🔲 | — |
| 26 | KP/Jaimini school gates | 🔲 | — |
| 27 | Monte Carlo Celery scaling | 🔲 | — |

**Grand total: 557/557 tests passing**

## Accuracy Audit ✅ All Resolved

P-1 ✅ P-4 ✅ N-1 ✅ S-2 ✅ E-1 ✅ A-2 ✅
