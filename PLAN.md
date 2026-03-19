# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

## Tech Stack

| Layer | Current | Target |
|-------|---------|--------|
| Ephemeris | pyswisseph Moshier | + DE441 |
| Backend | FastAPI (sync) | + Celery |
| Database | SQLite → PostgreSQL | PostgreSQL |
| Cache | Redis 3-tier (optional) | Redis |
| Auth | **JWT multi-user (S22)** | JWT |
| Task Queue | Celery (S21) | Celery + Flower |
| UI | Streamlit 10-tab | Next.js |
| Deploy | Docker Compose | Kubernetes |

## Architecture

```
Birth Data → ephemeris.py → calculations/ (19 modules) → scoring.py
          → report.py → worker.py (Celery) → api/main_v2.py
          → db_pg.py / db.py → cache.py → ui/app.py
Auth:       src/auth.py + src/api/auth_router.py [S22]
Migrations: migrations/ (Alembic) [S20]
```

## Regression Fixture

1947 India Independence Chart — Lagna=Taurus 7.7286°, Sun=Cancer 27.989°, Ayanamsha=Lahiri

## Phase 1 — Pilot — Sessions 1–10 ✅ 222/222

| S | Deliverable | Tests |
|---|-------------|-------|
| 1 | ephemeris.py | 14 |
| 2 | 7 core calc modules | 36 |
| 3 | scoring + api + db | 20 |
| 4 | Streamlit 3-tab UI | 6 |
| 5 | Docker + integration | 17 |
| 6 | vimshottari + SVG | 20 |
| 7 | yogas (13 types) | 14 |
| 8 | ashtakavarga | 26 |
| 9 | gochara | 29 |
| 10 | panchanga + D9 | 40 |

## Phase 2 — Features — Sessions 11–19 ✅ 225/225

| S | Deliverable | Tests |
|---|-------------|-------|
| 11 | pushkara_navamsha + Monte Carlo | 30 |
| 12 | kundali_milan (36-pt) | 25 |
| 13 | report.py (PDF) | 15 |
| 14 | jaimini_chara_dasha | 20 |
| 15 | kp_significators (249) | 22 |
| 16 | tajika annual chart | 18 |
| 17 | compatibility_score | 20 |
| 18 | API v2 endpoints | 15 |
| 19 | UI 10-tab scaffold | 20 |

## Phase 3 — Production — Sessions 20–27

| S | Deliverable | Status | Tests |
|---|-------------|--------|-------|
| 20 | db_pg + cache + Alembic | ✅ Done | 35 |
| 21 | Celery + full UI wiring | ✅ Done | 25 |
| 22 | JWT multi-user auth | ✅ Done | 25 |
| 23 | GitHub Actions CI/CD | 🔲 Next | — |
| 24 | Kubernetes + Helm | 🔲 | — |
| 25 | Next.js frontend | 🔲 | — |
| 26 | KP/Jaimini school gates | 🔲 | — |
| 27 | Monte Carlo Celery scaling | 🔲 | — |

**Grand total: 532/532 tests passing**

## Accuracy Audit ✅ All Resolved

P-1 ✅ P-4 ✅ N-1 ✅ S-2 ✅ E-1 ✅ A-2 ✅
