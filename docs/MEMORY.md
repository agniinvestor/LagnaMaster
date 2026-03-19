# LagnaMaster — Project Memory

> Last updated: 2026-03-19 (Session 23)
> Read this at the start of every session.

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–23 |
| Tests passing | 557/557 |
| Next session | 24 — Kubernetes + Helm |
| Blocking issues | Streamlit Cloud: set Main file = streamlit_app.py |
| Open bugs | None |

## Source file inventory

```
src/
  ephemeris.py           S1
  scoring.py             S3   R21 live since S11
  db.py                  S3   SQLite + _SENTINEL
  db_pg.py               S20  PostgreSQL + SQLite fallback
  cache.py               S20  Redis 3-tier
  report.py              S13  PDF + HTML
  worker.py              S21  Celery (3 tasks)
  auth.py                S22  JWT auth + user DB
  calculations/ (19)     S2–S17
  ui/app.py              S4,6–21  10 tabs fully wired
  ui/chart_visual.py     S6,10
  api/main.py            S3   v1
  api/main_v2.py         S20  v2 PG+Redis
  api/auth_router.py     S22  5 auth endpoints
  api/models.py          S3,18

.github/workflows/ci.yml  S23  test + docker + lint

tests/  (557 total)
  S1–S10: 222 · S11–S19: 225 · S20: 35 · S21: 25 · S22: 25 · S23: 25
```

## Critical invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart always inserts new row
3. _SENTINEL in db.py AND auth.py for test isolation
4. nakshatra.py: field is .dasha_lord (NOT .lord)
5. DignityLevel: EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL/ENEMY_SIGN/DEBIL
6. WC rules R03/R05/R07/R14: always × 0.5
7. db_pg.py API: exactly mirrors db.py
8. Cache is optional: get() → None on miss/error
9. Celery: JSON only, PDF = base64 string
10. JWT tokens typed by "kind" claim: cross-use raises ValueError
11. Streamlit Cloud: entry point = streamlit_app.py (NOT src/ui/app.py)
12. CI: test job must pass before docker job runs (needs: test)

## Environment variables

| Variable | Default | Notes |
|----------|---------|-------|
| PG_DSN | — | Absent = SQLite |
| REDIS_URL | redis://localhost:6379/0 | Empty = disabled |
| CACHE_VERSION | 1 | Bump to bust scores |
| CELERY_BROKER_URL | redis://localhost:6379/1 | |
| CELERY_RESULT_URL | redis://localhost:6379/2 | |
| JWT_SECRET | dev-secret-... | **Change in production** |
| ACCESS_TTL_MIN | 15 | |
| REFRESH_TTL_DAY | 7 | |

## Doc update rule (every session)

README.md · PLAN.md · DOCS.md · docs/SESSION_LOG.md · docs/MEMORY.md
All five updated atomically in every session commit.
