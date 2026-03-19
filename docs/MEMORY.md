# LagnaMaster — Project Memory

> Last updated: 2026-03-19 (Session 22)

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–22 |
| Tests passing | 532/532 |
| Next session | 23 — GitHub Actions CI/CD |
| Blocking issues | None |
| Open bugs | None |

## Critical invariants

1. 1947 fixture: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
2. Immutable inserts: save_chart never updates, always inserts
3. _SENTINEL pattern: src/db.py AND src/auth.py — tests set *_PATH before import
4. nakshatra.py field: .dasha_lord (NOT .lord)
5. DignityLevel enum: EXALT/MOOLTRIKONA/OWN_SIGN/FRIEND_SIGN/NEUTRAL/ENEMY_SIGN/DEBIL
6. WC rules R03/R05/R07/R14: always × 0.5
7. db_pg.py API: exactly mirrors db.py signatures
8. Cache is optional: get() returns None on miss/error
9. Celery JSON serialiser: all task args/returns must be JSON-safe; PDF = base64
10. JWT tokens are typed: "kind"="access"|"refresh" — cross-use raises ValueError
11. Streamlit Cloud entry point: streamlit_app.py (repo root), NOT src/ui/app.py

## Environment variables

| Variable | Default | Effect |
|----------|---------|--------|
| PG_DSN | (absent) | Activates PostgreSQL |
| REDIS_URL | redis://localhost:6379/0 | Cache |
| CACHE_VERSION | 1 | Bust score cache |
| CELERY_BROKER_URL | redis://localhost:6379/1 | Celery broker |
| CELERY_RESULT_URL | redis://localhost:6379/2 | Celery results |
| JWT_SECRET | dev-secret-change-in-production | **Must change in prod** |
| ACCESS_TTL_MIN | 15 | Access token minutes |
| REFRESH_TTL_DAY | 7 | Refresh token days |

## Phase 3 roadmap

| S | Deliverable | Status |
|---|-------------|--------|
| 20 | PostgreSQL + Redis | ✅ |
| 21 | Celery + full UI | ✅ |
| 22 | JWT auth | ✅ |
| 23 | GitHub Actions CI/CD | 🔲 Next |
| 24 | Kubernetes + Helm | 🔲 |
| 25 | Next.js frontend | 🔲 |
| 26 | KP/Jaimini school gates | 🔲 |
| 27 | Monte Carlo Celery scaling | 🔲 |

## Doc update rule (every session)

README.md · PLAN.md · DOCS.md · docs/SESSION_LOG.md · docs/MEMORY.md
All five updated atomically in every session commit.
