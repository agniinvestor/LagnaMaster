# LagnaMaster — Project Memory

> Last updated: 2026-03-19 (Session 20)
> This file is the authoritative cross-session memory.
> Read it at the start of every session before touching any code.

---

## Project identity

Vedic Jyotish birth chart scoring platform. Translates a 178-sheet Excel
workbook into a deterministic Python web app. Primary validator: 1947 India
Independence Chart (Taurus Lagna, pancha-graha yoga in Cancer).

Repo: https://github.com/agniinvestor/LagnaMaster

---

## Current state (Session 20 complete)

| Item | Value |
|------|-------|
| Sessions done | 1–20 |
| Tests passing | 482/482 |
| Next session | 21 — Redis integration tests + Celery async workers |
| Blocking issues | None |
| Open bugs | None (all 6 audit bugs resolved Sessions 1–8) |

---

## Source file inventory

```
src/
  ephemeris.py              Session 1   BirthChart, PlanetPosition
  scoring.py                Session 3   22-rule engine (R21 live since S11)
  db.py                     Session 3   SQLite, immutable inserts
  db_pg.py                  Session 20  PostgreSQL + SQLite auto-select
  cache.py                  Session 20  Redis 3-tier (graceful degradation)
  report.py                 Session 13  PDF + HTML chart report
  calculations/
    dignity.py              Session 2
    nakshatra.py            Session 2   field: .dasha_lord (NOT .lord)
    friendship.py           Session 2
    house_lord.py           Session 2
    chara_karak.py          Session 2
    narayana_dasa.py        Session 2
    shadbala.py             Session 2
    vimshottari_dasa.py     Session 6
    yogas.py                Session 7
    ashtakavarga.py         Session 8
    gochara.py              Session 9
    panchanga.py            Session 10
    pushkara_navamsha.py    Session 11  activates R21 in scoring.py
    kundali_milan.py        Session 12  Ashtakoot 36-pt
    jaimini_chara_dasha.py  Session 14
    kp_significators.py     Session 15  249 sub-lord divisions
    tajika.py               Session 16  solar return
    compatibility_score.py  Session 17  composite index
  ui/
    app.py                  Sessions 4,6–19   10 tabs (S19)
    chart_visual.py         Sessions 6,10     south_indian_svg + navamsha_svg
  api/
    main.py                 Session 3   v1 (SQLite, no cache)
    main_v2.py              Session 20  v2 (PG+Redis, same endpoints)
    models.py               Sessions 3,18

migrations/
  alembic.ini               Session 20
  env.py                    Session 20
  versions/
    0001_initial_schema.py  Session 20  charts + score_runs tables

tests/
  fixtures.py               INDIA_1947 fixture
  test_ephemeris.py         14  S1
  test_calculations.py      36  S2
  test_scoring.py           20  S3
  test_integration.py       17  S5
  test_vimshottari.py       20  S6
  test_yogas.py             14  S7
  test_ashtakavarga.py      26  S8
  test_gochara.py           29  S9
  test_panchanga.py         40  S10
  test_pushkara.py          30  S11
  test_kundali_milan.py     25  S12
  test_report.py            15  S13
  test_jaimini.py           20  S14
  test_kp.py                22  S15
  test_tajika.py            18  S16
  test_compatibility.py     20  S17
  test_api_v2.py            15  S18
  test_ui_tabs.py           20  S19
  test_session20.py         35  S20

docs/
  SESSION_LOG.md            this project's session history
  MEMORY.md                 this file
```

---

## Critical invariants — never break these

1. **1947 fixture**: every module must produce its known outputs for
   `year=1947, month=8, day=15, hour=0.0, lat=28.6139, lon=77.209, tz=5.5, ayanamsha=lahiri`.
   Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°.

2. **Immutable inserts**: charts are never updated. Every `save_chart` call
   creates a new row. This applies to both SQLite and PostgreSQL.

3. **`_SENTINEL` pattern in `src/db.py`**: tests set `src.db.DB_PATH` before
   importing API. Do not change this.

4. **`nakshatra.py` field name**: `.dasha_lord` not `.lord`.

5. **`DignityLevel` enum names**: `EXALT`, `MOOLTRIKONA`, `OWN_SIGN`,
   `FRIEND_SIGN`, `NEUTRAL`, `ENEMY_SIGN`, `DEBIL`. Do not alias.

6. **WC rules R03/R05/R07/R14**: always multiplied by 0.5 in score aggregation.

7. **`db_pg.py` public API** must exactly mirror `db.py` — same function
   signatures, same return types — so callers need zero changes.

8. **Cache is always optional**: `cache.get` returns None on miss/error,
   `cache.set` is a no-op on error. Application must never depend on cache
   being populated.

---

## Environment variables

| Variable | Default | Effect |
|----------|---------|--------|
| `PG_DSN` | (absent) | Activates PostgreSQL in db_pg.py |
| `PG_POOL_MIN` | 1 | Min pool connections |
| `PG_POOL_MAX` | 10 | Max pool connections |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis for cache.py; empty=disabled |
| `CACHE_VERSION` | 1 | Bump to invalidate score caches |

---

## Phase 3 roadmap (Sessions 20–27)

| Session | Deliverable | Status |
|---------|-------------|--------|
| 20 | PostgreSQL migration + Redis 3-tier caching | ✅ Done |
| 21 | Redis integration tests + Celery async workers | 🔲 Next |
| 22 | Multi-user JWT auth | 🔲 |
| 23 | GitHub Actions CI/CD + Docker image publishing | 🔲 |
| 24 | Kubernetes deployment manifests + Helm chart | 🔲 |
| 25 | Next.js frontend (replaces Streamlit) | 🔲 |
| 26 | KP and Jaimini school gate configuration | 🔲 |
| 27 | Monte Carlo concurrent scaling (Celery) | 🔲 |

---

## Doc update rule (enforce every session)

Every session commit must update all three docs atomically:

- `README.md` — tick session row, update test count header
- `PLAN.md` — mark ✅ Done, update grand total, advance 🔲 Next
- `DOCS.md` — add module section (API, dataclasses, details), update repo
  structure and test table
- `docs/SESSION_LOG.md` — append new session entry
- `docs/MEMORY.md` — update current state table + file inventory
