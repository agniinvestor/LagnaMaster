# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

**Strategy**: Pilot-first → accuracy iteration → feature expansion → production hardening.

---

## Tech Stack

| Layer | Current | Production target |
|-------|---------|-------------------|
| Ephemeris | pyswisseph (Moshier) | + DE441 files |
| Backend | FastAPI (sync) | FastAPI + Celery |
| Database | SQLite → PostgreSQL | PostgreSQL |
| Cache | Redis 3-tier (optional) | Redis |
| Task Queue | Celery (S21) | Celery + Flower |
| UI | Streamlit 10-tab | Next.js |
| Deploy | Docker Compose | Kubernetes |
| Auth | Single user | Multi-user JWT |

---

## Architecture

```
Birth Data (date, time, lat/lon)
        ↓
src/ephemeris.py             ← pyswisseph → BirthChart
        ↓  [Tier-1 Redis: TTL 7d]
src/calculations/            ← 19 Jyotish modules
        ↓
src/scoring.py               ← 22 BPHS rules × 12 houses
        ↓  [Tier-2 Redis: TTL 1d]
src/report.py                ← PDF report (reportlab)
        ↓
src/worker.py                ← Celery tasks (async Monte Carlo + PDF) [S21]
        ↓
src/api/main_v2.py           ← FastAPI v2 (PG + Redis)
        ↓
src/db_pg.py / src/db.py     ← PostgreSQL + SQLite fallback
src/cache.py                 ← Redis 3-tier
        ↓
src/ui/app.py                ← Streamlit 10-tab UI [fully wired S21]
src/ui/chart_visual.py       ← South Indian SVG (D1 + D9)

migrations/
  alembic.ini · env.py · versions/0001_initial_schema.py

docs/
  SESSION_LOG.md · MEMORY.md
```

---

## Regression Fixture

**1947 India Independence Chart**:
- Birth: 1947-08-15 00:00 IST, New Delhi (28.6139°N, 77.2090°E)
- Lagna: 7.7286° Taurus · Sun: 27.989° Cancer · Ayanamsha: Lahiri

---

## Phase 1 — Pilot Build — Sessions 1–10 ✅ Complete

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 1 | `ephemeris.py` | ✅ | 14/14 |
| 2 | 7 core calculation modules | ✅ | 36/36 |
| 3 | `scoring.py` + `api/` + `db.py` | ✅ | 20/20 |
| 4 | Streamlit 3-tab UI | ✅ | 6/6 |
| 5 | Docker Compose + integration tests | ✅ | 17/17 |
| 6 | `vimshottari_dasa.py` + SVG chart | ✅ | 20/20 |
| 7 | `yogas.py` (13 types) | ✅ | 14/14 |
| 8 | `ashtakavarga.py` + E-1/A-2 guards | ✅ | 26/26 |
| 9 | `gochara.py` (transits, Sade Sati) | ✅ | 29/29 |
| 10 | `panchanga.py` + Navamsha D9 | ✅ | 40/40 |

**Subtotal: 222/222**

---

## Phase 2 — Feature Expansion — Sessions 11–19 ✅ Complete

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 11 | `pushkara_navamsha.py` + Monte Carlo ±30min | ✅ | 30/30 |
| 12 | `kundali_milan.py` — Ashtakoot 36-pt | ✅ | 25/25 |
| 13 | `src/report.py` — PDF via reportlab | ✅ | 15/15 |
| 14 | `jaimini_chara_dasha.py` | ✅ | 20/20 |
| 15 | `kp_significators.py` — 249 sub-lords | ✅ | 22/22 |
| 16 | `tajika.py` — Tajika annual chart | ✅ | 18/18 |
| 17 | `compatibility_score.py` — composite index | ✅ | 20/20 |
| 18 | API v2: yogas, report, milan endpoints | ✅ | 15/15 |
| 19 | UI 10-tab layout scaffolded | ✅ | 20/20 |

**Subtotal: 225/225**

---

## Phase 3 — Production Hardening — Sessions 20–27

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 20 | `db_pg.py` (PostgreSQL) + `cache.py` (Redis) + Alembic | ✅ Done | 35/35 |
| 21 | `src/worker.py` (Celery) + full `src/ui/app.py` wiring | ✅ Done | 25/25 |
| 22 | Multi-user JWT auth (register/login/refresh/me) | 🔲 Next | — |
| 23 | GitHub Actions CI/CD + Docker image publishing | 🔲 | — |
| 24 | Kubernetes manifests + Helm chart | 🔲 | — |
| 25 | Next.js frontend (replaces Streamlit) | 🔲 | — |
| 26 | KP / Jaimini school gate configuration | 🔲 | — |
| 27 | Monte Carlo concurrent scaling (Celery pool) | 🔲 | — |

**Grand total: 507/507 tests passing**

---

## Accuracy Audit ✅ All Resolved

| ID | Bug | Status |
|----|-----|--------|
| P-1 | Midnight birth falsy | ✅ Fixed S1 |
| P-4 | Ayanamsha silent failure | ✅ Fixed S1 |
| N-1 | Narayana Dasha Taurus = 4yr | ✅ Fixed S2 |
| S-2 | Shadbala Chesta = hardcoded 3851 | ✅ Fixed S2 |
| E-1 | JDN Gregorian +0.5 day | ✅ Not in Python; regression test S8 |
| A-2 | Mercury Rx wrong row | ✅ Not in Python; regression test S8 |

---

## Source Files

| File | Description |
|------|-------------|
| `Lagna_Master5_clean.xlsx` | v5 workbook — 178 sheets, formula source of truth |
| `LagnaMaster_Audit_v5_PVRNR.docx` | Audit: 4 critical + 6 high issues |
| `docs/SESSION_LOG.md` | Full session history |
| `docs/MEMORY.md` | Cross-session project memory |
