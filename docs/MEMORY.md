# LagnaMaster — Project Memory

> Last updated: 2026-03-20 | Session 27 — PROJECT COMPLETE

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–27 (ALL) |
| Tests passing | 657/657 |
| Status | **PRODUCTION READY** |
| Next work | Ongoing maintenance / new feature requests |
| Open bugs | None |

## Source file inventory (final)

```
src/
  ephemeris.py              S1   pyswisseph wrapper
  scoring.py                S3   22-rule BPHS engine (R21 live S11)
  db.py                     S3   SQLite + _SENTINEL
  db_pg.py                  S20  PostgreSQL + SQLite fallback
  cache.py                  S20  Redis 3-tier
  report.py                 S13  PDF + HTML
  worker.py                 S21  Celery (compute_chart, generate_pdf, monte_carlo)
  auth.py                   S22  JWT auth + user DB
  config.py                 S26  school gates (parashari/kp/jaimini)
  calculations/
    dignity … panchanga     S2–S10
    pushkara_navamsha.py    S11  MonteCarloResult + run_monte_carlo (sync)
    kundali_milan.py        S12
    jaimini_chara_dasha.py  S14
    kp_significators.py     S15
    tajika.py               S16
    compatibility_score.py  S17
    monte_carlo.py          S27  Celery chord parallel + async + status
  ui/
    app.py                  S4,6–21  Streamlit 10-tab
    chart_visual.py         S6,10
  api/
    main.py                 S3   v1
    main_v2.py              S20  v2 (PG + Redis)
    auth_router.py          S22  5 auth endpoints
    school_router.py        S26  3 school endpoints
    models.py               S3,18

helm/lagnamaster/           S24  Kubernetes Helm chart
frontend/                   S25  Next.js 14 + TypeScript + Tailwind
.github/workflows/ci.yml    S23  test + docker + lint

tests/ — 657 tests across 23 files (test_session26.py, test_session27.py added)
docs/SESSION_LOG.md / MEMORY.md
```

## All critical invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart never updates rows
3. _SENTINEL in db.py AND auth.py for test isolation
4. nakshatra.py field: .dasha_lord (NOT .lord)
5. DignityLevel: EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL/ENEMY_SIGN/DEBIL
6. WC rules R03/R05/R07/R14: always × 0.5
7. db_pg.py API: exactly mirrors db.py
8. Cache is optional: get() → None on miss/error
9. Celery: JSON only, PDF = base64 string
10. JWT tokens typed by "kind": cross-use raises ValueError
11. Streamlit Cloud: entry point = streamlit_app.py
12. CI: test job must pass before docker job
13. Helm: secrets in K8s Secret, never in values.yaml
14. Next.js: all API calls via /api/* proxy
15. Parashari school is always enabled; KP/Jaimini controlled by ENABLE_KP/ENABLE_JAIMINI
16. monte_carlo.py re-exports run_monte_carlo from pushkara_navamsha for backward compat

## Complete environment variables

| Variable | Default | Notes |
|----------|---------|-------|
| PG_DSN | — | Absent = SQLite |
| REDIS_URL | redis://localhost:6379/0 | Empty = disabled |
| CACHE_VERSION | 1 | Bump to bust scores |
| CELERY_BROKER_URL | redis://localhost:6379/1 | |
| CELERY_RESULT_URL | redis://localhost:6379/2 | |
| JWT_SECRET | dev-secret-... | **Must change in prod** |
| ACCESS_TTL_MIN | 15 | |
| REFRESH_TTL_DAY | 7 | |
| ENABLE_KP | 1 | 0 = disable KP school |
| ENABLE_JAIMINI | 1 | 0 = disable Jaimini school |
| NEXT_PUBLIC_API_URL | http://localhost:8000 | Next.js proxy target |
