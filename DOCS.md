# LagnaMaster — Technical Documentation

> Last updated: 2026-03-19 | Sessions 1–23 | 557/557 tests

## Repository Structure (Session 23)

```
LagnaMaster/
├── streamlit_app.py          Streamlit Cloud entry point
├── PLAN.md / DOCS.md / README.md
├── requirements.txt          16 packages incl. pyjwt, bcrypt, ruff
├── alembic.ini / migrations/
├── .github/workflows/ci.yml  GitHub Actions CI/CD  [S23]
├── docs/SESSION_LOG.md / MEMORY.md
└── src/
    ├── __init__.py
    ├── ephemeris.py  scoring.py  db.py  db_pg.py
    ├── cache.py  report.py  worker.py
    ├── auth.py               S22
    ├── calculations/ (19 modules S1–S17)
    ├── ui/app.py (10 tabs)  chart_visual.py
    └── api/
        ├── main.py  main_v2.py  models.py
        └── auth_router.py    S22
```

## Module Reference — Sessions 22 + 23

### `src/auth.py` + `src/api/auth_router.py` (Session 22)

**Auth module public API:**
```python
init_user_db(path=_SENTINEL)
register_user(username, email, password, path) → UserRecord
authenticate_user(username, password, path)    → UserRecord | None
create_token_pair(user_id)                     → TokenPair
verify_access_token(token)                     → int
verify_refresh_token(token)                    → int
get_user_by_id(user_id, path)                  → UserRecord | None
deactivate_user(user_id, path)
```

**Tokens:** HS256 JWT, `"kind"` claim prevents cross-use. Access=15min, Refresh=7d.
**Passwords:** bcrypt(rounds=12); SHA-256 HMAC fallback when bcrypt absent.
**User DB:** `data/users.db`, `_SENTINEL` pattern, UNIQUE COLLATE NOCASE.

**Router endpoints:**
```
POST /auth/register  → 201 UserOut   (409 on duplicate)
POST /auth/login     → 200 TokenOut  (401 on bad creds)
POST /auth/refresh   → 200 TokenOut  (401 on invalid refresh)
GET  /auth/me        → 200 UserOut   (Bearer required)
POST /auth/logout    → 204
```

**`get_current_user` dependency** — import and use to protect any endpoint:
```python
from src.api.auth_router import get_current_user
@app.get("/protected")
def protected(user = Depends(get_current_user)):
    return {"user_id": user.id}
```

### `.github/workflows/ci.yml` (Session 23)

**Three jobs:**

| Job | Trigger | What it does |
|-----|---------|-------------|
| `test` | push + PR | pytest 3.12, apt gcc/g++/python3-dev, 557 tests |
| `docker` | push to main only (needs: test) | builds API + UI images, pushes to `ghcr.io/agniinvestor/lagnamaster-{api,ui}` |
| `lint` | push + PR | ruff E/F/W (ignores E501, W503) |

**Docker images published:**
- `ghcr.io/agniinvestor/lagnamaster-api:latest` + `:{sha}`
- `ghcr.io/agniinvestor/lagnamaster-ui:latest` + `:{sha}`

**Cache:** GitHub Actions cache (`type=gha`) for both Pip and Docker layer cache.

## Test Suite — 557 total

```
S1–S10  pilot        222
S11–S19 features     225
S20     db_pg+cache   35
S21     celery+UI     25
S22     jwt auth      25   TestReg(6) TestAuth(5) TestTok(6) TestRouter(8)
S23     CI/health     20   TestCIFile(5) TestHealth(8) TestReq(6) TestEntry(4) [approx]
                     ────
                      557
```

## Environment Variables (complete)

| Variable | Default | Purpose |
|----------|---------|---------|
| PG_DSN | — | PostgreSQL (absent=SQLite) |
| REDIS_URL | redis://localhost:6379/0 | Cache |
| CACHE_VERSION | 1 | Score cache buster |
| CELERY_BROKER_URL | redis://localhost:6379/1 | Celery broker |
| CELERY_RESULT_URL | redis://localhost:6379/2 | Celery results |
| JWT_SECRET | dev-secret-change-in-production | **Must change in prod** |
| ACCESS_TTL_MIN | 15 | Access token minutes |
| REFRESH_TTL_DAY | 7 | Refresh token days |

## Development Setup

```bash
pip install -r requirements.txt        # 16 packages
PYTHONPATH=. pytest tests/ -v          # 557 tests
PYTHONPATH=. uvicorn src.api.main:app --reload
PYTHONPATH=. streamlit run src/ui/app.py
```
