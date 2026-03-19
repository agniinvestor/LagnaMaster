# LagnaMaster — Technical Documentation

> Last updated: 2026-03-19
> Sessions complete: 1–20 (482/482 tests passing)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Regression Fixture](#3-regression-fixture)
4. [Module Reference](#4-module-reference)
   - 4.1 src/ephemeris.py
   - 4.2–4.8 Core calculation modules (dignity → shadbala)
   - 4.9 src/scoring.py
   - 4.10 src/db.py
   - 4.11 src/api/main.py
   - 4.12 src/api/models.py
   - 4.13 src/calculations/vimshottari_dasa.py
   - 4.14 src/calculations/yogas.py
   - 4.15 src/ui/chart_visual.py
   - 4.16 src/ui/app.py
   - 4.17 src/calculations/ashtakavarga.py
   - 4.18 src/calculations/gochara.py
   - 4.19 src/calculations/panchanga.py
   - 4.20 src/calculations/pushkara_navamsha.py *(Session 11)*
   - 4.21 src/calculations/kundali_milan.py *(Session 12)*
   - 4.22 src/report.py *(Session 13)*
   - 4.23 src/calculations/jaimini_chara_dasha.py *(Session 14)*
   - 4.24 src/calculations/kp_significators.py *(Session 15)*
   - 4.25 src/calculations/tajika.py *(Session 16)*
   - 4.26 src/calculations/compatibility_score.py *(Session 17)*
   - **4.27 src/db_pg.py** *(Session 20)*
   - **4.28 src/cache.py** *(Session 20)*
   - **4.29 src/api/main_v2.py** *(Session 20)*
   - **4.30 migrations/** *(Session 20)*
5. [API Reference](#5-api-reference)
6. [Scoring Engine Deep Dive](#6-scoring-engine-deep-dive)
7. [Known Bugs & Status](#7-known-bugs--status)
8. [Test Suite](#8-test-suite)
9. [Development Setup](#9-development-setup)

---

## 1. Project Overview

LagnaMaster transforms a 178-sheet Excel Jyotish workbook into a deterministic, auditable web platform.

**Core flow**:

```
Birth data (date, time, lat/lon)
    → ephemeris.py               pyswisseph (Tier-1 Redis cache)
    → calculations/              19 Jyotish modules
    → scoring.py                 22 BPHS rules × 12 houses (Tier-2 cache)
    → report.py                  PDF chart report
    → api/main_v2.py             FastAPI (PostgreSQL + Redis)
    → db_pg.py / db.py           PostgreSQL (auto-select) or SQLite
    → cache.py                   Redis 3-tier (optional)
    → ui/app.py                  Streamlit 10-tab UI
```

**Tech stack**:

| Layer | Current | Production target |
|-------|---------|-------------------|
| Ephemeris | pyswisseph Moshier | + DE441 files |
| Backend | FastAPI (sync) | FastAPI + Celery |
| Database | SQLite → PostgreSQL | PostgreSQL |
| Cache | Redis 3-tier (optional) | Redis |
| UI | Streamlit | Next.js |
| Deploy | Docker Compose | Kubernetes |
| Auth | Single user | Multi-user JWT |

---

## 2. Repository Structure

```
LagnaMaster/
├── PLAN.md / DOCS.md / README.md
├── requirements.txt / packages.txt
├── Dockerfile / docker-compose.yml / Makefile
├── alembic.ini                 Alembic config [Session 20]
├── .streamlit/config.toml
├── ephe/                       Swiss Ephemeris data (optional)
├── migrations/                 Alembic migrations [Session 20]
│   ├── env.py
│   └── versions/0001_initial_schema.py
├── docs/
│   ├── SESSION_LOG.md          Full session history
│   └── MEMORY.md               Cross-session project memory
├── data/charts.db              SQLite (created at runtime)
│
├── src/
│   ├── ephemeris.py            S1
│   ├── scoring.py              S3  (R21 live since S11)
│   ├── db.py                   S3  SQLite immutable inserts
│   ├── db_pg.py                S20 PostgreSQL + SQLite fallback
│   ├── cache.py                S20 Redis 3-tier
│   ├── report.py               S13 PDF + HTML report
│   ├── calculations/
│   │   ├── dignity.py          S2
│   │   ├── nakshatra.py        S2  (.dasha_lord field)
│   │   ├── friendship.py       S2
│   │   ├── house_lord.py       S2
│   │   ├── chara_karak.py      S2
│   │   ├── narayana_dasa.py    S2
│   │   ├── shadbala.py         S2
│   │   ├── vimshottari_dasa.py S6
│   │   ├── yogas.py            S7
│   │   ├── ashtakavarga.py     S8
│   │   ├── gochara.py          S9
│   │   ├── panchanga.py        S10
│   │   ├── pushkara_navamsha.py S11
│   │   ├── kundali_milan.py    S12
│   │   ├── jaimini_chara_dasha.py S14
│   │   ├── kp_significators.py S15
│   │   ├── tajika.py           S16
│   │   └── compatibility_score.py S17
│   ├── ui/
│   │   ├── app.py              S4,6–19  10 tabs
│   │   └── chart_visual.py     S6,10
│   └── api/
│       ├── main.py             S3  v1 (SQLite only)
│       ├── main_v2.py          S20 v2 (PG + Redis)
│       └── models.py           S3,18
│
└── tests/
    ├── fixtures.py             INDIA_1947
    ├── test_ephemeris.py       14  S1
    ├── test_calculations.py    36  S2
    ├── test_scoring.py         20  S3
    ├── test_integration.py     17  S5
    ├── test_vimshottari.py     20  S6
    ├── test_yogas.py           14  S7
    ├── test_ashtakavarga.py    26  S8
    ├── test_gochara.py         29  S9
    ├── test_panchanga.py       40  S10
    ├── test_pushkara.py        30  S11
    ├── test_kundali_milan.py   25  S12
    ├── test_report.py          15  S13
    ├── test_jaimini.py         20  S14
    ├── test_kp.py              22  S15
    ├── test_tajika.py          18  S16
    ├── test_compatibility.py   20  S17
    ├── test_api_v2.py          15  S18
    ├── test_ui_tabs.py         20  S19
    └── test_session20.py       35  S20
```

---

## 3. Regression Fixture

```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15, "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5, "ayanamsha": "lahiri",
}
# Expected: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
# Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer
```

---

## 4. Module Reference

*(Sections 4.1–4.26 unchanged — see previous DOCS.md for full detail on
ephemeris, dignity, nakshatra, friendship, house_lord, chara_karak,
narayana_dasa, shadbala, scoring, db, api, vimshottari_dasa, yogas,
chart_visual, app, ashtakavarga, gochara, panchanga, pushkara_navamsha,
kundali_milan, report, jaimini_chara_dasha, kp_significators, tajika,
compatibility_score.)*

---

### 4.27 `src/db_pg.py` *(Session 20)*

**Purpose**: PostgreSQL persistence layer that mirrors `src/db.py`'s public API exactly. Auto-selects backend via `PG_DSN` environment variable; falls back to SQLite when absent.

**Backend selection**:
```
PG_DSN set + psycopg2 installed → PostgreSQL (ThreadedConnectionPool)
PG_DSN absent OR psycopg2 missing → SQLite (delegates to src.db)
```

**Connection pool**: `psycopg2.pool.ThreadedConnectionPool`, min=`PG_POOL_MIN` (default 1), max=`PG_POOL_MAX` (default 10). All connections use `RealDictCursor` so rows behave like dicts.

**Schema** (created by `init_db()` if not present, also managed by Alembic):
```sql
CREATE TABLE charts (
    id          SERIAL PRIMARY KEY,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    name        TEXT,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    hour        DOUBLE PRECISION NOT NULL,
    lat         DOUBLE PRECISION NOT NULL,
    lon         DOUBLE PRECISION NOT NULL,
    tz_offset   DOUBLE PRECISION NOT NULL DEFAULT 5.5,
    ayanamsha   TEXT NOT NULL DEFAULT 'lahiri',
    chart_json  JSONB NOT NULL,
    scores_json JSONB
);
CREATE TABLE score_runs (
    id       SERIAL PRIMARY KEY,
    chart_id INTEGER REFERENCES charts(id),
    run_at   TIMESTAMPTZ DEFAULT NOW(),
    scores_json JSONB NOT NULL
);
```

**JSONB vs TEXT**: Unlike SQLite (which stores JSON as TEXT), PostgreSQL stores `chart_json` and `scores_json` as JSONB. `_pg_row_to_dict()` re-serialises them to strings so callers see identical types regardless of backend.

**Public API** (identical signatures to `src/db.py`):
```python
def init_db() -> None
def save_chart(year, month, day, hour, lat, lon, tz_offset, ayanamsha,
               chart_json, scores_json=None, name=None) -> int
def get_chart(chart_id: int) -> dict | None
def list_charts(limit: int = 50) -> list[dict]
def health_check() -> dict   # {"backend": "postgres"|"sqlite", "ok": bool}
```

**Immutable insert**: every `save_chart` call always inserts a new row — charts are never updated. `RETURNING id` retrieves the generated primary key.

---

### 4.28 `src/cache.py` *(Session 20)*

**Purpose**: Redis 3-tier caching with complete graceful degradation. When Redis is unreachable all operations silently no-op; the application continues at full correctness with no performance benefit.

**Three tiers**:

| Tier constant | Key prefix | TTL | Content |
|---------------|-----------|-----|---------|
| `TIER_EPHEMERIS = "eph"` | `lm:eph:{sha1}` | 7 days | BirthChart dict (planet positions are immutable for a given instant) |
| `TIER_SCORES = "scr"` | `lm:scr:{id}:v{ver}` | 1 day | ChartScores dict (versioned by `CACHE_VERSION` env-var) |
| `TIER_AV = "av"` | `lm:av:{id}` | 1 day | AshtakavargaChart dict |

**Key builders**:
```python
make_ephemeris_key(year, month, day, hour, lat, lon, tz_offset, ayanamsha) -> str
# SHA-1 of pipe-joined params, truncated to 16 hex chars

make_scores_key(chart_id: int) -> str
# "{chart_id}:v{CACHE_VERSION}"  — bump CACHE_VERSION to invalidate all scores

make_av_key(chart_id: int) -> str
# str(chart_id)
```

**Core operations**:
```python
def get(tier: str, key: str) -> dict | None   # None on miss or Redis error
def set(tier: str, key: str, value: Any) -> None   # no-op on error
def delete(tier: str, key: str) -> None
def flush_tier(tier: str) -> int   # returns count of deleted keys
def health_check() -> dict   # {"backend": "redis", "ok": bool, ...}
```

**Connection**: `redis.Redis.from_url(REDIS_URL, socket_connect_timeout=2, socket_timeout=2)`. On first call attempts `PING`; if it fails sets `_disabled=True` and skips all subsequent Redis calls for the lifetime of the process.

**All values JSON-serialised** before storage. `get()` JSON-deserialises the returned string.

---

### 4.29 `src/api/main_v2.py` *(Session 20)*

**Purpose**: Drop-in FastAPI replacement for `src/api/main.py`. Identical public endpoints; adds PostgreSQL persistence and Redis caching internally.

**Cache flow for `POST /charts`**:
1. Build ephemeris key from request params
2. `cache.get(TIER_EPHEMERIS, eph_key)` — if hit, skip `compute_chart()`
3. Run `score_chart()` (always — scores are cheap)
4. `db.save_chart()` — immutable insert to PG or SQLite
5. `cache.set(TIER_SCORES, scores_key, scores_dict)` — prime Tier 2

**Cache flow for `GET /charts/{id}/scores`**:
1. `cache.get(TIER_SCORES, scores_key)` — return immediately if hit
2. On miss: fetch from DB, recompute, prime cache, return

**Updated `GET /health`** response shape:
```json
{
  "status": "ok",
  "version": "0.2.0",
  "db":    {"backend": "postgres", "ok": true},
  "cache": {"backend": "redis",    "ok": true, "version": "7.2.4"}
}
```

**`_reconstruct_chart(cj: dict) -> BirthChart`**: internal helper that re-inflates a stored JSON dict into a full `BirthChart` object with typed `PlanetPosition` instances, used when serving cached/stored charts.

---

### 4.30 `migrations/` *(Session 20)*

**Purpose**: Alembic migration scaffold for PostgreSQL schema management.

**Files**:
- `alembic.ini` — `script_location = migrations`, DSN overridden by `PG_DSN` env-var
- `migrations/env.py` — online + offline migration modes; reads `PG_DSN` at runtime
- `migrations/versions/0001_initial_schema.py` — creates `charts` and `score_runs` tables with indexes

**Run migrations**:
```bash
export PG_DSN=postgresql://lagnamaster:secret@localhost:5432/lagnamaster
alembic upgrade head      # apply all pending migrations
alembic downgrade -1      # roll back one migration
alembic history           # show migration log
```

**Indexes created**:
- `idx_charts_created`: `charts(created_at DESC)` — powers `list_charts()` ordering
- `idx_charts_name`: partial index on `charts(name) WHERE name IS NOT NULL`
- `idx_score_runs_chart`: `score_runs(chart_id)` — foreign key lookup

---

## 5. API Reference

**Base URL** (local): `http://localhost:8000`

All v1 endpoints unchanged. New in v2:

### GET /health (v2)
```json
{
  "status": "ok",
  "version": "0.2.0",
  "db":    {"backend": "postgres"|"sqlite", "ok": true|false},
  "cache": {"backend": "redis", "ok": true|false, "version": "7.x"}
}
```

### GET /charts/{id}/yogas *(Session 18)*
Response: `list[YogaOut]` — sorted by category then nature.

### GET /charts/{id}/report *(Session 18)*
Response: PDF binary, `Content-Type: application/pdf`.

### GET /charts/{id}/milan/{partner_id} *(Session 18)*
Response: `MilanOut` (total, 8 koot scores, Mangal Dosha flags, label).

---

## 6. Scoring Engine Deep Dive

*(Unchanged from Session 10 baseline. R21 Pushkara Navamsha fully live since Session 11 — adds +0.5 when Bhavesh occupies a Pushkara pada.)*

---

## 7. Known Bugs & Status

All 6 audit bugs resolved. No open bugs.

| ID | Bug | Status |
|----|-----|--------|
| P-1 | `hour=0` falsy | ✅ Fixed S1 |
| P-4 | Ayanamsha silent default | ✅ Fixed S1 |
| N-1 | Narayana Dasha Taurus=4yr | ✅ Fixed S2 |
| S-2 | Shadbala Chesta=3851 | ✅ Fixed S2 |
| E-1 | JDN +0.5 day | ✅ Not in Python; regression test S8 |
| A-2 | Mercury Rx row reference | ✅ Not in Python; regression test S8 |

---

## 8. Test Suite

**482 tests, all passing** (as of Session 20):

```
test_ephemeris.py         14   S1
test_calculations.py      36   S2
test_scoring.py           20   S3
test_integration.py       17   S5
test_vimshottari.py       20   S6
test_yogas.py             14   S7
test_ashtakavarga.py      26   S8
test_gochara.py           29   S9
test_panchanga.py         40   S10
test_pushkara.py          30   S11
test_kundali_milan.py     25   S12
test_report.py            15   S13
test_jaimini.py           20   S14
test_kp.py                22   S15
test_tajika.py            18   S16
test_compatibility.py     20   S17
test_api_v2.py            15   S18
test_ui_tabs.py           20   S19
test_session20.py         35   S20   db_pg + cache + api_v2 health
                         ────
                          482 total
```

**Running the Session 20 tests (no external services needed)**:
```bash
PYTHONPATH=. pytest tests/test_session20.py -v
# PostgreSQL tests auto-skipped without PG_DSN
# Redis tests verify graceful no-op degradation
```

**Running with PostgreSQL**:
```bash
export PG_DSN=postgresql://lagnamaster:secret@localhost:5432/lagnamaster
PYTHONPATH=. pytest tests/test_session20.py -v -k "Postgres"
```

---

## 9. Development Setup

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# SQLite + no Redis (default dev mode)
PYTHONPATH=. pytest tests/ -v                          # 482 tests
PYTHONPATH=. uvicorn src.api.main:app --reload         # :8000
PYTHONPATH=. streamlit run src/ui/app.py               # :8501

# PostgreSQL + Redis (production mode)
export PG_DSN=postgresql://lagnamaster:secret@localhost:5432/lagnamaster
export REDIS_URL=redis://localhost:6379/0
createdb lagnamaster
alembic upgrade head
PYTHONPATH=. uvicorn src.api.main_v2:app --reload
```

**requirements.txt** additions from Session 20:
```
psycopg2-binary>=2.9.9
redis>=5.0.0
alembic>=1.13.0
sqlalchemy>=2.0.0
```
