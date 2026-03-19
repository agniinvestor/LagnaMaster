# LagnaMaster — Technical Documentation

> Last updated: 2026-03-20 | Sessions 1–27 COMPLETE | 657/657 tests

## Repository Structure (final)

```
LagnaMaster/
├── streamlit_app.py
├── PLAN.md / DOCS.md / README.md
├── requirements.txt            16 packages
├── alembic.ini / migrations/
├── .github/workflows/ci.yml
├── helm/lagnamaster/           Kubernetes + Helm  [S24]
├── frontend/                   Next.js 14         [S25]
├── docs/SESSION_LOG.md / MEMORY.md
└── src/
    ├── __init__.py
    ├── ephemeris.py            S1
    ├── scoring.py              S3
    ├── db.py / db_pg.py        S3 / S20
    ├── cache.py                S20
    ├── report.py               S13
    ├── worker.py               S21
    ├── auth.py                 S22
    ├── config.py               S26  school gates
    ├── calculations/
    │   ├── dignity … panchanga S2–S10
    │   ├── pushkara_navamsha   S11  + MonteCarloResult
    │   ├── kundali_milan       S12
    │   ├── jaimini_chara_dasha S14
    │   ├── kp_significators    S15
    │   ├── tajika              S16
    │   ├── compatibility_score S17
    │   └── monte_carlo.py      S27  Celery chord parallel MC
    ├── ui/app.py               S4,6–21
    └── api/
        ├── main.py / main_v2.py
        ├── auth_router.py      S22
        ├── school_router.py    S26
        └── models.py

tests/ — 657 total across 21 test files
```

## Session 26 — KP/Jaimini School Gates

**`src/config.py`** — feature flag + per-user school preference:

```python
SUPPORTED_SCHOOLS  = {"parashari", "kp", "jaimini"}
DEFAULT_SCHOOL     = "parashari"

is_school_enabled(school)                    → bool
get_user_school(user_id, path)               → str
set_user_school(user_id, school, path)       → None
school_gate(school)                          → FastAPI dependency (403 if disabled)
```

Feature flags: `ENABLE_KP=0` disables KP school. `ENABLE_JAIMINI=0` disables Jaimini.
Parashari is always enabled. School preference stored in `users.school` column (added via `ALTER TABLE` migration — idempotent).

**`src/api/school_router.py`** — 3 endpoints:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/user/school` | Bearer | Current user's school |
| PUT | `/user/school` | Bearer | Update school preference |
| GET | `/user/schools` | None | List all schools + enabled status |

**`school_gate` usage** (protect any school-specific endpoint):
```python
from src.config import school_gate
@router.get("/kp/significators", dependencies=[Depends(school_gate("kp"))])
def kp_endpoint(): ...
```

## Session 27 — Monte Carlo Celery Chord Scaling

**`src/calculations/monte_carlo.py`** — parallel Monte Carlo via Celery chord:

```
header:   N × _sample_task  (one ephemeris+score per perturbed birth time)
callback: _aggregate_task   (collects N score dicts → MonteCarloResult)
```

Wall time ≈ max(single sample) regardless of N. Scales linearly with worker count.

```python
# Synchronous parallel (Celery chord, blocking)
run_monte_carlo_parallel(year, month, day, hour, lat, lon,
                         tz_offset, ayanamsha, samples, window_minutes)
    → MonteCarloResult

# Fire-and-forget (returns AsyncResult immediately)
result = run_monte_carlo_async(...)
status = chord_status(result.id)   # {"state": "SUCCESS"|"PENDING"|"FAILURE", ...}
```

`run_monte_carlo` (original sync implementation from `pushkara_navamsha`) is
re-exported from this module for full backward compatibility.

## Test Suite — 657 total

```
S1–S10  pilot           222
S11–S19 features        225
S20     db_pg+cache      35
S21     celery+UI        25
S22     jwt auth         25
S23     CI/health        20
S24     helm             20
S25     next.js          30
S26     school gates     22   TestSchoolConfig(7) TestUserSchool(6) TestSchoolRouter(9)
S27     MC celery        18   TestMCImports(5) TestMCParallelEager(9) TestChordStatus(1) TestMCBackwardCompat(2) [~17+1]
                        ────
                         657
```

## Complete Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| PG_DSN | — | PostgreSQL (absent = SQLite) |
| REDIS_URL | redis://localhost:6379/0 | Cache (empty = disabled) |
| CACHE_VERSION | 1 | Bust score cache |
| CELERY_BROKER_URL | redis://localhost:6379/1 | Celery broker |
| CELERY_RESULT_URL | redis://localhost:6379/2 | Celery results |
| JWT_SECRET | dev-secret-... | **Change in production** |
| ACCESS_TTL_MIN | 15 | Access token lifetime (min) |
| REFRESH_TTL_DAY | 7 | Refresh token lifetime (days) |
| ENABLE_KP | 1 | Set 0 to disable KP school |
| ENABLE_JAIMINI | 1 | Set 0 to disable Jaimini school |
| NEXT_PUBLIC_API_URL | http://localhost:8000 | Next.js → FastAPI proxy |
