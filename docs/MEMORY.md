# LagnaMaster — Project Memory

> Last updated: 2026-03-20 (Session 25)

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–25 |
| Tests passing | 607/607 |
| Next session | 26 — KP/Jaimini school gates |
| Blocking issues | None |
| Open bugs | None |

## Critical invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart always inserts new row
3. _SENTINEL in db.py AND auth.py for test isolation
4. nakshatra.py field: .dasha_lord (NOT .lord)
5. DignityLevel: EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL/ENEMY_SIGN/DEBIL
6. WC rules R03/R05/R07/R14: always × 0.5
7. db_pg.py API: exactly mirrors db.py
8. Cache is optional: get() → None on miss/error
9. Celery: JSON only, PDF = base64 string
10. JWT tokens typed by "kind" claim: cross-use raises ValueError
11. Streamlit Cloud: entry point = streamlit_app.py
12. CI: test job must pass before docker job runs
13. Helm: secrets in K8s Secret `lagnamaster-secrets`, never in values.yaml
14. Next.js: all API calls via /api/* proxy (next.config.js rewrites)

## Environment variables (complete)

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
| NEXT_PUBLIC_API_URL | http://localhost:8000 | Next.js → FastAPI proxy |

## Phase 3 roadmap

| S | Deliverable | Status |
|---|-------------|--------|
| 20 | PostgreSQL + Redis | ✅ |
| 21 | Celery + full UI | ✅ |
| 22 | JWT auth | ✅ |
| 23 | GitHub Actions CI/CD | ✅ |
| 24 | Kubernetes + Helm | ✅ |
| 25 | Next.js frontend | ✅ |
| 26 | KP/Jaimini school gates | 🔲 Next |
| 27 | Monte Carlo Celery scaling | 🔲 |
