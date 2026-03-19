# LagnaMaster — Session Log

> Last updated: 2026-03-19
> Sessions complete: 1–20

---

## Session 1 — `src/ephemeris.py` pyswisseph wrapper
**Date**: 2026-03-19 | **Tests**: 14/14

Delivered `src/ephemeris.py`: wraps pyswisseph `swe.calc_ut` with
`FLG_SIDEREAL | FLG_SPEED` flags, Lahiri/Raman/Krishnamurti ayanamshas,
Moshier fallback, Ketu as Rahu+180°. Defines `BirthChart` and
`PlanetPosition` dataclasses. Fixed P-1 (midnight bug) and P-4 (ayanamsha
silent failure). Validated against 1947 India chart: Lagna=Taurus 7.7286°,
Sun=Cancer 27.989°.

---

## Session 2 — 7 core calculation modules
**Date**: 2026-03-19 | **Tests**: 36/36

Delivered `dignity.py`, `nakshatra.py`, `friendship.py`, `house_lord.py`,
`chara_karak.py`, `narayana_dasa.py`, `shadbala.py`. Fixed N-1 (Narayana
Dasha Taurus=4yr→7yr) and S-2 (Shadbala Chesta hardcoded 3851→formula).
All modules pass 1947 fixture.

---

## Session 3 — Scoring engine + FastAPI + SQLite
**Date**: 2026-03-19 | **Tests**: 20/20

Delivered `src/scoring.py` (22 BPHS rules × 12 houses, WC halving, clamped
[-10,+10]), `src/api/main.py` (5 endpoints), `src/api/models.py` (Pydantic
v2), `src/db.py` (SQLite immutable inserts, _SENTINEL pattern, WAL mode).

---

## Session 4 — Streamlit UI (3 tabs)
**Date**: 2026-03-19 | **Tests**: 6/6

Delivered `src/ui/app.py`: Chart / Domain Scores / Rule Detail tabs.
Sidebar with birth data inputs, Demo 1947 button, Chart History toggle.

---

## Session 5 — Docker Compose + Makefile + integration tests
**Date**: 2026-03-19 | **Tests**: 17/17

Delivered `Dockerfile`, `docker-compose.yml` (api:8000 + ui:8501 + SQLite
volume), `Makefile`, `packages.txt`. Integration tests cover full round-trip,
history ordering, score determinism, all 3 ayanamshas.

---

## Session 6 — Vimshottari Dasha + South Indian SVG
**Date**: 2026-03-19 | **Tests**: 20/20

Delivered `vimshottari_dasa.py` (120yr, 9 MDs × 9 ADs, balance at birth,
AntarDasha proportional formula), `chart_visual.py` (520×520px South Indian
4×4 grid SVG). UI expanded to 4 tabs. 1947 fixture: Moon in Pushya → Saturn
birth dasha.

---

## Session 7 — Yoga detection (13 types)
**Date**: 2026-03-19 | **Tests**: 14/14

Delivered `yogas.py`: Pancha Mahapurusha, Raj, Dhana, Lunar (Gajakesari,
Chandra-Mangala, Adhi, Kemadruma, Shakata), Solar (Budha-Aditya, Vesi, Vasi,
Ubhayachari), Special (Pancha-Graha, Guru-Chandala, Neecha Bhanga Raj).
1947 fixture: Pancha-Graha confirmed. UI Yogas tab added.

---

## Session 8 — Ashtakavarga + E-1/A-2 regression guards
**Date**: 2026-03-19 | **Tests**: 26/26

Delivered `ashtakavarga.py`: 7 planet AV tables + Sarvashtakavarga (fixed
totals: Sun=50, Moon=48, Mars=42, Merc=55, Jup=57, Ven=52, Sat=40, Sarva=344).
Added regression tests for E-1 (JD accuracy ±0.001) and A-2 (Mercury Rx
direction). AV tab added to UI.

---

## Session 9 — Gochara transit analysis
**Date**: 2026-03-19 | **Tests**: 29/29

Delivered `gochara.py`: transit BirthChart at noon UTC, whole-sign house
mapping, Sade Sati phases (Rising/Peak/Setting), Guru-Chandal transit flag,
AV bindus for transit signs. Shadbala expander added to Chart tab. Transits
tab added.

---

## Session 10 — Panchanga + Navamsha D9
**Date**: 2026-03-19 | **Tests**: 40/40

Delivered `panchanga.py`: 5-limb almanac (Tithi, Vara, Nakshatra, Yoga,
Karana with inauspicious flags), D9 formula (_D9_START fire/earth/air/water).
`navamsha_svg()` added to `chart_visual.py`. 1947 known values: Tithi=28
Krishna, Vara=Friday/Venus, Nakshatra=Pushya, Yoga=Siddhi, D9 Lagna=Pisces.

**Pilot complete: 222/222 tests passing.**

---

## Session 11 — Pushkara Navamsha + Monte Carlo
**Date**: 2026-03-19 | **Tests**: 30/30

Delivered `pushkara_navamsha.py`: 14 Pushkara padas across 12 signs.
Activates R21 in scoring engine (+0.5 when Bhavesh in Pushkara pada).
Monte Carlo engine: 100 samples ±30 min, per-house σ, sensitivity labels
(Stable/Sensitive/High), <8s single core.

---

## Session 12 — Kundali Milan (Ashtakoot 36-pt)
**Date**: 2026-03-19 | **Tests**: 25/25

Delivered `kundali_milan.py`: 8 koots (Varna 1, Vashya 2, Tara 3, Yoni 4,
Graha Maitri 5, Gana 6, Bhakoot 7, Nadi 8 = 36 total). Mangal Dosha
detection + cancellation rules. Labels: Excellent(≥28)/Good(≥24)/Average(≥18)/
Below Average(≥12)/Incompatible(<12).

---

## Session 13 — PDF Chart Report (reportlab)
**Date**: 2026-03-19 | **Tests**: 15/15

Delivered `src/report.py`: 7-section PDF (title page, D1 SVG, panchanga
strip, domain scores table, yoga list, Vimshottari dasha timeline, D9 SVG)
via reportlab. Also produces self-contained HTML report. Served via API
`GET /charts/{id}/report`.

---

## Session 14 — Jaimini Chara Dasha
**Date**: 2026-03-19 | **Tests**: 20/20

Delivered `jaimini_chara_dasha.py`: 12-sign chara dasha keyed by AK sign.
Period = planets in sign + 1 (with lord placement and exalt/debil modifiers).
Direction: odd signs forward, even signs reverse. 12 MDs × 12 ADs.

---

## Session 15 — KP Significators
**Date**: 2026-03-19 | **Tests**: 22/22

Delivered `kp_significators.py`: 249 sub-lord divisions (Vimshottari ×
Vimshottari), planet sub-lord table, house significators (occupation +
aspect + sub-lord), ruling planets (5-planet set from weekday/Moon/Lagna
lords). KP tab added to UI.

---

## Session 16 — Tajika Annual Chart
**Date**: 2026-03-19 | **Tests**: 18/18

Delivered `tajika.py`: solar return BirthChart at exact natal Sun longitude
return, Varshaphal Lagna, Muntha (1 sign/year from birth lagna), 11 Arabic
Part Sahams, Itthasala (applying) and Ishrafa (separating) Tajika aspects
within 1° orb. Tajika tab added to UI.

---

## Session 17 — Compatibility Score
**Date**: 2026-03-19 | **Tests**: 20/20

Delivered `compatibility_score.py`: composite index =
0.50 × Ashtakoot_norm + 0.25 × dasha_sync + 0.25 × AV_norm.
Dasha sync: Panchadha Maitri between current MD lords of both charts.
AV norm: chart-2 planets' AV bindus in chart-1 Sarva.

---

## Session 18 — API v2 endpoints
**Date**: 2026-03-19 | **Tests**: 15/15

Added `GET /charts/{id}/yogas`, `GET /charts/{id}/report` (PDF binary),
`GET /charts/{id}/milan/{partner_id}`. Updated `src/api/models.py` with
`YogaOut`, `MilanOut`. Version bumped to 0.2.0.

---

## Session 19 — UI overhaul: 10 tabs
**Date**: 2026-03-19 | **Tests**: 20/20

`src/ui/app.py` expanded from 7 to 10 tabs: added Milan (Kundali Milan
partner form + 8-koot breakdown), KP (sub-lord table + ruling planets),
Tajika (annual chart SVG + Muntha + Sahams + aspects). UI performance pass.

**Phase 2 complete: 447/447 tests passing.**

---

## Session 20 — PostgreSQL migration + Redis 3-tier caching
**Date**: 2026-03-19 | **Tests**: 35/35 (new) | **Cumulative**: 482/482

### Deliverables

**`src/db_pg.py`** — PostgreSQL persistence layer (psycopg2 ThreadedConnectionPool).
Mirrors the `src/db.py` SQLite public API exactly (`init_db`, `save_chart`,
`get_chart`, `list_charts`, `health_check`). Auto-selects backend via `PG_DSN`
env-var; falls back to SQLite transparently — all existing tests pass unchanged.
JSONB columns for `chart_json`/`scores_json`. WAL-safe connection pool
(min=1, max=10).

**`src/cache.py`** — Redis 3-tier caching with graceful degradation.
- Tier 1 `eph`: ephemeris computations, TTL 7 days, keyed by SHA-1(birth params)
- Tier 2 `scr`: scores, TTL 1 day, keyed by chart_id + CACHE_VERSION env-var
- Tier 3 `av`: ashtakavarga tables, TTL 1 day, keyed by chart_id
When Redis is unreachable all operations are silent no-ops — application
continues normally with no performance benefit but no errors.

**`src/api/main_v2.py`** — Drop-in FastAPI replacement using both new layers.
Ephemeris results pulled from Tier 1 cache before pyswisseph call on repeat
requests. Scores primed into Tier 2 on first compute. `GET /health` now
returns structured `db` + `cache` sub-objects.

**`migrations/`** — Alembic migration scaffold.
- `alembic.ini` — DSN from PG_DSN env-var
- `migrations/env.py` — online + offline modes
- `migrations/versions/0001_initial_schema.py` — creates `charts` +
  `score_runs` tables, indexes on `created_at` and `name`

### Test coverage (35 new tests)
- `TestDbPgSQLiteFallback` (4 tests): health, save/get roundtrip, 404 miss, immutable inserts, ordering
- `TestDbPgPostgres` (2 tests, skipped without PG_DSN): PG health, PG save/get
- `TestCacheNoRedis` (4 tests): get returns None, set silent, health not-ok, flush returns 0
- `TestCacheKeyBuilders` (5 tests): determinism, ayanamsha diff, version diff, av key type, id diff
- `TestApiV2Health` (4 tests): 200, keys present, db backend, cache not-ok

### New environment variables
| Variable | Default | Purpose |
|----------|---------|---------|
| `PG_DSN` | (absent) | PostgreSQL DSN; absent → SQLite |
| `PG_POOL_MIN` | 1 | Min pool connections |
| `PG_POOL_MAX` | 10 | Max pool connections |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis URL; empty → disabled |
| `CACHE_VERSION` | 1 | Bump to invalidate all score caches |

### New dependencies (requirements.txt additions)
```
psycopg2-binary>=2.9.9
redis>=5.0.0
alembic>=1.13.0
sqlalchemy>=2.0.0
```

### Migration workflow
```bash
# Set DSN
export PG_DSN=postgresql://lagnamaster:secret@localhost:5432/lagnamaster

# Create DB and run migrations
createdb lagnamaster
alembic upgrade head

# Start API with PG + Redis
export REDIS_URL=redis://localhost:6379/0
PYTHONPATH=. uvicorn src.api.main_v2:app --reload
```

### Architecture note
`src/db.py` (SQLite) is unchanged. `src/db_pg.py` wraps it as a fallback,
so the test matrix stays green with zero external services. The API can be
pointed at `main_v2.py` for production or kept at `main.py` for local dev.
