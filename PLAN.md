# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

## Tech Stack

| Layer | Pilot (v1) | Production (v2) |
|-------|-----------|----------------|
| Ephemeris | pyswisseph DE441 | same |
| Backend | FastAPI (sync) | FastAPI + Celery |
| Database | SQLite | PostgreSQL |
| Cache | In-memory | Redis 3-tier |
| UI | Streamlit | Next.js |
| Deploy | Docker Compose | K8s |
| Auth | Single user | Multi-user JWT |

## Pilot Build — Sessions 1–10 ✅ Complete

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 1 | `src/ephemeris.py` | ✅ Done | 14 |
| 2 | `src/calculations/` — 7 modules | ✅ Done | 36 |
| 3 | `src/scoring.py` + `src/api/` + `src/db.py` | ✅ Done | 20 |
| 4 | `src/ui/app.py` — Streamlit 3-tab UI | ✅ Done | 6 |
| 5 | Docker Compose + integration tests | ✅ Done | 17 |
| 6 | `vimshottari_dasa.py` + `chart_visual.py` | ✅ Done | 20 |
| 7 | `yogas.py` (13 yoga types) | ✅ Done | 14 |
| 8 | `ashtakavarga.py` + E-1/A-2 regression guards | ✅ Done | 26 |
| 9 | `gochara.py` (transit analysis, Sade Sati) | ✅ Done | 29 |
| 10 | `panchanga.py` (5-limb almanac) + D9 navamsha | ✅ Done | 40 |

**Pilot total: 222/222 tests passing**

## Expansion Build — Sessions 11–17 ✅ Complete

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 11 | `pushkara_navamsha.py` + `montecarlo.py` | ✅ Done | 30 |
| 12 | `kundali_milan.py` (Ashtakoot 36-pt) | ✅ Done | 25 |
| 13 | `src/reports/pdf_report.py` (reportlab) | ✅ Done | 15 |
| 14 | `chara_dasha.py` (Jaimini Chara Dasha) | ✅ Done | 20 |
| 15 | `varga.py` (D2/D3/D4/D7/D9/D10/D12/D60) | ✅ Done | 25 |
| 16 | `sapta_varga.py` (Vimshopak Bala, 20-pt) | ✅ Done | 20 |
| 17 | `kp.py` (KP Star/Sub lords + significators) | ✅ Done | 22 |

**Expansion total: 137/137 tests passing**
**Grand total: 359/359 tests passing**

## Accuracy Audit ✅ Complete (Sessions 8–10)

| ID | Bug | Status |
|----|-----|--------|
| P-1 | Midnight birth: hour=0 falsy | ✅ Fixed S1 |
| P-4 | Ayanamsha silent failure | ✅ Fixed S1 |
| N-1 | Narayana Dasha Taurus = 4yr | ✅ Fixed S2 |
| S-2 | Shadbala J14 hardcoded 3851 | ✅ Fixed S2 |
| E-1 | JDN +0.5 day correction | ✅ Not in Python; regression test S8 |
| A-2 | Mercury direction wrong row | ✅ Not in Python; regression test S8 |

## Phase 3 — Production Hardening (Sessions 18–25)

* PostgreSQL migration + Redis 3-tier caching
* Multi-user auth (JWT) + Celery workers
* Docker → Kubernetes + Streamlit → Next.js

## Regression Fixture

1947 India Independence Chart: 1947-08-15 00:00 IST, New Delhi.
Lagna: 7.7286° Taurus. Ayanamsha: Lahiri. All modules validated.
