# LagnaMaster — Technical Documentation

> Last updated: 2026-03-19
> Sessions complete: 1–21 (507/507 tests passing)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Regression Fixture](#3-regression-fixture)
4. [Module Reference](#4-module-reference)
   - 4.1–4.19: Core modules (ephemeris → panchanga) — unchanged
   - 4.20 pushkara_navamsha.py (S11)
   - 4.21 kundali_milan.py (S12)
   - 4.22 src/report.py (S13)
   - 4.23 jaimini_chara_dasha.py (S14)
   - 4.24 kp_significators.py (S15)
   - 4.25 tajika.py (S16)
   - 4.26 compatibility_score.py (S17)
   - 4.27 src/db_pg.py (S20)
   - 4.28 src/cache.py (S20)
   - 4.29 src/api/main_v2.py (S20)
   - 4.30 migrations/ (S20)
   - **4.31 src/worker.py** *(Session 21)*
   - **4.32 src/ui/app.py — updated** *(Session 21)*
5. [API Reference](#5-api-reference)
6. [Scoring Engine Deep Dive](#6-scoring-engine-deep-dive)
7. [Known Bugs & Status](#7-known-bugs--status)
8. [Test Suite](#8-test-suite)
9. [Development Setup](#9-development-setup)

---

## 1. Project Overview

LagnaMaster transforms a 178-sheet Excel Jyotish workbook into a deterministic, auditable web platform.

**Core flow (Session 21)**:

```
Birth data
    → ephemeris.py               pyswisseph (Tier-1 Redis)
    → calculations/              19 Jyotish modules
    → scoring.py                 22 BPHS rules × 12 houses (Tier-2 Redis)
    → worker.py                  Celery async tasks (Monte Carlo, PDF)
    → report.py                  PDF chart report
    → api/main_v2.py             FastAPI (PostgreSQL + Redis)
    → db_pg.py / db.py           PostgreSQL or SQLite
    → cache.py                   Redis 3-tier (optional)
    → ui/app.py                  Streamlit 10-tab UI (fully wired S21)
```

---

## 2. Repository Structure

```
LagnaMaster/
├── PLAN.md / DOCS.md / README.md
├── requirements.txt              (+celery>=5.3.0 S21)
├── packages.txt / Dockerfile / docker-compose.yml / Makefile
├── alembic.ini                   S20
├── .streamlit/config.toml
├── ephe/
├── migrations/                   S20
│   ├── env.py
│   └── versions/0001_initial_schema.py
├── docs/
│   ├── SESSION_LOG.md
│   └── MEMORY.md
│
├── src/
│   ├── ephemeris.py              S1
│   ├── scoring.py                S3  (R21 live S11)
│   ├── db.py                     S3  SQLite
│   ├── db_pg.py                  S20 PostgreSQL + SQLite fallback
│   ├── cache.py                  S20 Redis 3-tier
│   ├── report.py                 S13 PDF + HTML
│   ├── worker.py                 S21 Celery tasks
│   ├── calculations/
│   │   ├── dignity.py            S2
│   │   ├── nakshatra.py          S2
│   │   ├── friendship.py         S2
│   │   ├── house_lord.py         S2
│   │   ├── chara_karak.py        S2
│   │   ├── narayana_dasa.py      S2
│   │   ├── shadbala.py           S2
│   │   ├── vimshottari_dasa.py   S6
│   │   ├── yogas.py              S7
│   │   ├── ashtakavarga.py       S8
│   │   ├── gochara.py            S9
│   │   ├── panchanga.py          S10
│   │   ├── pushkara_navamsha.py  S11
│   │   ├── kundali_milan.py      S12
│   │   ├── jaimini_chara_dasha.py S14
│   │   ├── kp_significators.py   S15
│   │   ├── tajika.py             S16
│   │   └── compatibility_score.py S17
│   ├── ui/
│   │   ├── app.py                S4,6–21  10 tabs fully wired
│   │   └── chart_visual.py       S6,10
│   └── api/
│       ├── main.py               S3  v1
│       ├── main_v2.py            S20 v2 (PG + Redis)
│       └── models.py             S3,18
│
└── tests/
    ├── fixtures.py
    ├── test_ephemeris.py         14  S1
    ├── test_calculations.py      36  S2
    ├── test_scoring.py           20  S3
    ├── test_integration.py       17  S5
    ├── test_vimshottari.py       20  S6
    ├── test_yogas.py             14  S7
    ├── test_ashtakavarga.py      26  S8
    ├── test_gochara.py           29  S9
    ├── test_panchanga.py         40  S10
    ├── test_pushkara.py          30  S11
    ├── test_kundali_milan.py     25  S12
    ├── test_report.py            15  S13
    ├── test_jaimini.py           20  S14
    ├── test_kp.py                22  S15
    ├── test_tajika.py            18  S16
    ├── test_compatibility.py     20  S17
    ├── test_api_v2.py            15  S18
    ├── test_ui_tabs.py           20  S19
    ├── test_session20.py         35  S20
    └── test_session21.py         25  S21
```

---

## 3. Regression Fixture

```python
INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15, "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5, "ayanamsha": "lahiri",
}
# Lagna=Taurus 7.7286° ±0.05°, Sun=Cancer 27.989°
# Pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn in Cancer
```

---

## 4. Module Reference

*(Sections 4.1–4.30 unchanged — ephemeris, dignity, nakshatra, friendship, house_lord,
chara_karak, narayana_dasa, shadbala, scoring, db, api, vimshottari_dasa, yogas,
chart_visual, ashtakavarga, gochara, panchanga, pushkara_navamsha, kundali_milan,
report, jaimini_chara_dasha, kp_significators, tajika, compatibility_score,
db_pg, cache, main_v2, migrations — see previous DOCS.md.)*

---

### 4.31 `src/worker.py` *(Session 21)*

**Purpose**: Celery async worker — offloads CPU-intensive and time-consuming tasks (Monte Carlo, PDF generation, ephemeris computation) to background workers. The application remains responsive; tasks are polled or awaited by the caller.

**Celery app name**: `lagnamaster`

**Environment variables**:

| Variable | Default | Purpose |
|----------|---------|---------|
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Redis broker (DB 1, separate from cache DB 0) |
| `CELERY_RESULT_URL` | `redis://localhost:6379/2` | Redis result backend (DB 2) |

**Task routing**:

| Task | Queue | Reason |
|------|-------|--------|
| `compute_monte_carlo_task` | `heavy` | 100 ephemeris calls, CPU-bound |
| `generate_pdf_task` | `heavy` | reportlab rendering, memory-bound |
| `compute_chart_task` | `default` | single ephemeris call |

**Starting workers**:
```bash
celery -A src.worker worker --loglevel=info --concurrency=4 -Q default,heavy
```

**Three tasks**:

```python
# 1. Monte Carlo — returns JSON-safe MonteCarloResult dict
compute_monte_carlo_task.delay(
    year, month, day, hour, lat, lon,
    tz_offset=5.5, ayanamsha="lahiri",
    samples=100, window_minutes=30.0,
)
# Result keys: base_scores, mean_scores, std_scores, sensitivity, sample_count

# 2. PDF generation — returns base64-encoded PDF bytes
generate_pdf_task.delay(
    year, month, day, hour, lat, lon,
    tz_offset=5.5, ayanamsha="lahiri", name="",
)
# Result: base64 string — decode with base64.b64decode(result)

# 3. Async chart compute — returns {chart: {...}, scores: {...}}
compute_chart_task.delay(
    year, month, day, hour, lat, lon,
    tz_offset=5.5, ayanamsha="lahiri",
)
```

**Configuration**:
- `task_serializer = "json"` (all args and return values must be JSON-safe)
- `result_expires = 3600` (results kept 1 hour)
- `task_acks_late = True` + `worker_prefetch_multiplier = 1` (safe retry semantics)
- `max_retries = 2` on all tasks with exponential-ish backoff

**Testing without a broker** (eager mode):
```python
from src.worker import celery_app
celery_app.conf.update(task_always_eager=True, task_eager_propagates=True)
result = compute_monte_carlo_task.delay(...).get()  # runs synchronously
```

---

### 4.32 `src/ui/app.py` — updated *(Session 21)*

**Purpose**: Streamlit 10-tab UI fully wiring all modules from Sessions 1–20. Prior to Session 21, Tabs 5 (Dasha), 7 (Milan), 8 (KP), and 9 (Tajika) were scaffolded but incomplete.

**Session 21 additions**:

| Tab | What changed |
|-----|-------------|
| Tab 2 — Scores | Monte Carlo button added; sensitivity table (σ per house, Stable/Sensitive/High labels) shown after run |
| Tab 5 — Dasha | Jaimini Chara Dasha section added below Vimshottari (12 MDs + current period highlighted) |
| Tab 7 — Milan | Composite compatibility index shown below Ashtakoot score (`compute_compatibility`) |
| Tab 8 — KP | Ruling planets refresh on date picker change; house significators table |
| Tab 9 — Tajika | Annual chart SVG via `south_indian_svg(tajika.annual_chart)`, Sahams table, aspects table |
| Sidebar | Celery task status indicator (informational) |

**All 10 tab imports** (must match committed module public APIs exactly):
```python
from src.calculations.pushkara_navamsha import check_pushkara, run_monte_carlo
from src.calculations.kundali_milan import compute_milan
from src.calculations.jaimini_chara_dasha import compute_chara_dasha, current_chara_dasha
from src.calculations.kp_significators import compute_kp
from src.calculations.tajika import compute_tajika
from src.calculations.compatibility_score import compute_compatibility
```

**Key UI patterns**:
- Monte Carlo runs synchronously in the UI thread for now (Celery integration in Session 23 when CI/CD is in place)
- `st.session_state.monte_carlo` persists the result across reruns; cleared on new chart compute
- `st.session_state.partner_chart` and `partner_birth_date` persist the partner chart for Milan tab
- All tables use `st.dataframe(..., hide_index=True)` for consistent formatting

---

## 5. API Reference

*(Unchanged from Session 20 — see previous DOCS.md for full endpoint docs.)*

**Version**: `0.2.0` (main_v2.py)

---

## 6. Scoring Engine Deep Dive

*(Unchanged. R21 Pushkara Navamsha live since Session 11: +0.5 when Bhavesh in Pushkara pada.)*

---

## 7. Known Bugs & Status

All 6 audit bugs resolved. No open bugs.

---

## 8. Test Suite

**507 tests, all passing** (as of Session 21):

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
test_session20.py         35   S20
test_session21.py         25   S21
                         ────
                          507 total
```

**Session 21 test classes**:
- `TestWorkerEager` (10): chart task correctness, MC task structure, PDF bytes, idempotency
- `TestWorkerConfig` (5): broker URL, result URL, serializer, expires, app name
- `TestUIImports` (11): all S11–20 module imports + functional smoke tests
- `TestWorkerDBIntegration` (1): task result → db save → retrieve roundtrip

**Run**:
```bash
PYTHONPATH=. pytest tests/test_session21.py -v
```

---

## 9. Development Setup

```bash
git clone https://github.com/agniinvestor/LagnaMaster.git
cd LagnaMaster
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=. pytest tests/ -v                          # 507 tests
PYTHONPATH=. uvicorn src.api.main:app --reload         # API :8000
PYTHONPATH=. streamlit run src/ui/app.py               # UI :8501

# With Celery (requires Redis)
celery -A src.worker worker --loglevel=info -Q default,heavy
```

**requirements.txt additions (Session 21)**:
```
celery>=5.3.0
```
