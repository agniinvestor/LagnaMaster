# LagnaMaster — Project Memory

> Last updated: 2026-03-19 (Session 21)
> Read this at the start of every session before touching any code.

---

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–21 |
| Tests passing | 507/507 |
| Next session | 22 — Multi-user JWT auth |
| Blocking issues | None |
| Open bugs | None |

---

## Source file inventory

```
src/
  ephemeris.py                S1
  scoring.py                  S3  (R21 live since S11)
  db.py                       S3  SQLite immutable inserts
  db_pg.py                    S20 PostgreSQL + SQLite fallback
  cache.py                    S20 Redis 3-tier
  report.py                   S13 PDF + HTML
  worker.py                   S21 Celery (3 tasks: MC, PDF, chart)
  calculations/
    dignity.py                S2
    nakshatra.py              S2  — field .dasha_lord (NOT .lord)
    friendship.py             S2
    house_lord.py             S2
    chara_karak.py            S2
    narayana_dasa.py          S2
    shadbala.py               S2
    vimshottari_dasa.py       S6
    yogas.py                  S7
    ashtakavarga.py           S8
    gochara.py                S9
    panchanga.py              S10
    pushkara_navamsha.py      S11  R21 active
    kundali_milan.py          S12
    jaimini_chara_dasha.py    S14
    kp_significators.py       S15  249 sub-lords
    tajika.py                 S16
    compatibility_score.py    S17
  ui/
    app.py                    S4,6–21  10 tabs, all modules wired
    chart_visual.py           S6,10
  api/
    main.py                   S3  v1 (SQLite only, kept for local dev)
    main_v2.py                S20 v2 (PG + Redis)
    models.py                 S3,18

migrations/
  alembic.ini / env.py / versions/0001_initial_schema.py  S20

tests/
  test_ephemeris.py           14  S1
  test_calculations.py        36  S2
  test_scoring.py             20  S3
  test_integration.py         17  S5
  test_vimshottari.py         20  S6
  test_yogas.py               14  S7
  test_ashtakavarga.py        26  S8
  test_gochara.py             29  S9
  test_panchanga.py           40  S10
  test_pushkara.py            30  S11
  test_kundali_milan.py       25  S12
  test_report.py              15  S13
  test_jaimini.py             20  S14
  test_kp.py                  22  S15
  test_tajika.py              18  S16
  test_compatibility.py       20  S17
  test_api_v2.py              15  S18
  test_ui_tabs.py             20  S19
  test_session20.py           35  S20
  test_session21.py           25  S21
  TOTAL                      507

docs/
  SESSION_LOG.md
  MEMORY.md
```

---

## Critical invariants — never break

1. **1947 fixture**: Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°.
2. **Immutable inserts**: `save_chart` always inserts a new row, never updates.
3. **`_SENTINEL` pattern**: `src/db.py` — tests set `DB_PATH` before import.
4. **`nakshatra.py` field**: `.dasha_lord` not `.lord`.
5. **`DignityLevel` enum names**: `EXALT / MOOLTRIKONA / OWN_SIGN / FRIEND_SIGN / NEUTRAL / ENEMY_SIGN / DEBIL`.
6. **WC rules R03/R05/R07/R14**: always multiplied by 0.5 in scoring.
7. **`db_pg.py` API**: exactly mirrors `db.py` — same signatures, same return types.
8. **Cache is optional**: `cache.get` returns None on miss/error. App never depends on cache being warm.
9. **Celery JSON serialiser**: all task args and return values must be JSON-safe. PDF bytes returned as base64 string.
10. **Celery eager mode for tests**: `task_always_eager=True` — set before each test class, restore after.

---

## Environment variables

| Variable | Default | Effect |
|----------|---------|--------|
| `PG_DSN` | (absent) | Activates PostgreSQL |
| `PG_POOL_MIN/MAX` | 1 / 10 | Pool size |
| `REDIS_URL` | `redis://localhost:6379/0` | Cache; empty=disabled |
| `CACHE_VERSION` | 1 | Bumps to bust score cache |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery broker |
| `CELERY_RESULT_URL` | `redis://localhost:6379/2` | Celery results |

---

## Phase 3 roadmap

| Session | Deliverable | Status |
|---------|-------------|--------|
| 20 | PostgreSQL + Redis | ✅ |
| 21 | Celery + full UI wiring | ✅ |
| 22 | Multi-user JWT auth | 🔲 Next |
| 23 | GitHub Actions CI/CD | 🔲 |
| 24 | Kubernetes + Helm | 🔲 |
| 25 | Next.js frontend | 🔲 |
| 26 | KP/Jaimini school gates | 🔲 |
| 27 | Monte Carlo Celery scaling | 🔲 |

---

## Doc update rule (enforce every session)

Every commit must atomically update:
- `README.md` — tick session row, update test count header
- `PLAN.md` — mark ✅ Done, update grand total, advance 🔲 Next
- `DOCS.md` — add module section, update repo structure + test table
- `docs/SESSION_LOG.md` — append session entry
- `docs/MEMORY.md` — update state table + file inventory
