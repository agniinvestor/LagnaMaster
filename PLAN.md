# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

**Strategy**: Pilot-first → accuracy iteration. Ship a working end-to-end app in ~1 week, then fix calculation accuracy module by module.

---

## Tech Stack

| Layer | Pilot (v1) | Production (v2) |
|-------|-----------|----------------|
| Ephemeris | pyswisseph DE441 | same |
| Backend | FastAPI (sync) | FastAPI + Celery |
| Database | SQLite | PostgreSQL (immutable inserts) |
| Cache | In-memory | Redis 3-tier |
| UI | Streamlit | Next.js |
| Deploy | Docker Compose + ngrok | K8s |
| Auth | Single user | Multi-user JWT |

---

## Architecture

```
Birth Data (date, time, lat/lon)
        ↓
src/ephemeris.py             ← pyswisseph wrapper → BirthChart
        ↓
src/calculations/            ← 12 Jyotish modules (translated from Excel CALC sheets)
  dignity.py                 ← exaltation/debilitation/own/mooltrikona, combustion, Neecha Bhanga
  nakshatra.py               ← 27 nakshatras, 4 padas, D9 navamsha, Ganda Mool
  friendship.py              ← Naisargika + Tatkalik → Panchadha Maitri (5-fold)
  house_lord.py              ← whole-sign house map, Kendra/Trikona/Dusthana helpers
  chara_karak.py             ← 7 Jaimini Chara Karakas (AK → GK)
  narayana_dasa.py           ← sign-based 81-year predictive cycle
  shadbala.py                ← 6-component planetary strength in Virupas
  vimshottari_dasa.py        ← 120-year nakshatra dasha: 9 MDs × 9 ADs [Session 6]
  yogas.py                   ← 13 yoga types: PM/Raj/Dhana/Lunar/Solar/Special [Session 7]
  ashtakavarga.py            ← Parashari 8-source bindu system: 7 planets + Sarva [Session 8]
  gochara.py                 ← Transit analysis: GocharaReport, Sade Sati, AV bindus [Session 9]
  panchanga.py               ← 5-limb almanac: Tithi/Vara/Nakshatra/Yoga/Karana + D9 [Session 10]
  pushkara_navamsha.py       ← 24 PN zones (2/sign), R21 scoring hook [Session 11]
  kundali_milan.py           ← Ashtakoot 36-pt compatibility + Mangal Dosha [Session 12]
        ↓
src/scoring.py               ← 22 BPHS rules × 12 houses = 264 evaluations per chart
                                WC rules (R03/R05/R07/R14) count at 0.5× weight
                                Scores clamped to [-10, +10]; rating Excellent→Very Weak
                                R21 now live: bhavesh in PN → +0.5  [Session 11]
        ↓
src/montecarlo.py            ← ±30 min sensitivity engine, ProcessPoolExecutor [Session 11]
                                SensitivityReport: house stats + lagna/dasha stability
        ↓
src/api/main.py              ← FastAPI: POST /charts, GET /charts, GET /charts/{id}(/scores)
src/api/models.py            ← Pydantic: BirthDataRequest, ChartOut, ChartScoresOut
        ↓
src/db.py                    ← SQLite immutable inserts (_SENTINEL testability pattern)
        ↓
src/ui/chart_visual.py       ← South Indian SVG: south_indian_svg() + navamsha_svg() [Sessions 6,10]
src/ui/app.py                ← Streamlit 8-tab UI: Chart/Scores/Yogas/AV/Dasha/Transits/Rules/Sensitivity
                                [Sessions 4,6,7,8,9,10,11]
```

---

## Regression Fixture

**1947 India Independence Chart** (primary validator):

* Birth: 1947-08-15 00:00 IST, New Delhi (28.6139°N, 77.2090°E)
* Lagna: 7.7286° Taurus
* Sun: 27.989° Cancer
* Ayanamsha: Lahiri

All modules must pass this fixture before being considered done.

---

## Pilot Build — Sessions 1–10 ✅ Complete

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 1 | `src/ephemeris.py` — pyswisseph wrapper | ✅ Done | 14/14 |
| 2 | `src/calculations/` — 7 modules (dignity, nakshatra, friendship, house_lord, chara_karak, narayana_dasa, shadbala) | ✅ Done | 36/36 |
| 3 | `src/scoring.py` + `src/api/` + `src/db.py` — 22-rule engine + FastAPI + SQLite | ✅ Done | 20/20 |
| 4 | `src/ui/app.py` — Streamlit 3-tab UI (Chart / Domain Scores / Rule Detail) | ✅ Done | 6/6 |
| 5 | Docker Compose + Dockerfile + Makefile + integration tests (17) | ✅ Done | 17/17 |
| 6 | `vimshottari_dasa.py` + `chart_visual.py` (South Indian SVG) + 4-tab UI | ✅ Done | 20/20 |
| 7 | `yogas.py` (13 yoga types) + enriched planet table + Yogas tab in UI | ✅ Done | 14/14 |
| 8 | `ashtakavarga.py` (Parashari 8-source bindu tables) + AV tab in UI + E-1/A-2 regression guards | ✅ Done | 26/26 |
| 9 | `gochara.py` (transit analysis, Sade Sati) + Shadbala UI surface + Transits tab | ✅ Done | 29/29 |
| 10 | `panchanga.py` (5-limb almanac) + Navamsha D9 chart + `navamsha_svg()` | ✅ Done | 40/40 |

**Pilot total: 222/222 tests passing**

---

## Accuracy & Sensitivity Phase — Sessions 11–17

| Session | Deliverable | Status | Tests |
|---------|-------------|--------|-------|
| 11 | `pushkara_navamsha.py` + R21 live + `montecarlo.py` + Sensitivity tab | ✅ Done | 30/30 |
| 12 | Kundali Milan (chart compatibility / Ashtakoot scoring) | 🔲 Next | — |
| 13 | PDF chart report export (`reportlab` or `weasyprint`) | 🔲 | — |
| 14 | Jaimini Chara Dasha (sign-based, complements Vimshottari) | 🔲 | — |
| 15 | Sarvashtakavarga Kakshya bindus + Gochara AV-weighted scoring | 🔲 | — |
| 16 | Performance benchmark + profiling (target: chart <200 ms) | 🔲 | — |
| 17 | Pre-production cleanup: logging, error handling, API versioning | 🔲 | — |

**Total tests after Session 11: 252/252**

---

## Phase 3 — Production Hardening (Sessions 18–25)

* PostgreSQL migration (immutable inserts schema)
* Redis 3-tier caching
* Multi-user auth (JWT)
* Monte Carlo ±30min birth time (100 samples, <8s on 4 cores) ✅ Session 11
* KP and Jaimini school gates
* Docker → K8s
* Streamlit → Next.js

---

## Explicitly Deferred

* Jaimini / KP: after Parashari is complete (Session 14 starts Chara Dasha)
* Celery: when concurrent users > 5
* K8s: when concurrent users > 20
* Next.js: after Streamlit validates UX

---

## Accuracy Audit — Sessions 8–11 ✅ Complete

All 6 known bugs + R21 stub resolved:

| ID | Bug | Status | Resolution |
|----|-----|--------|-----------|
| P-1 | Midnight birth: 0 treated as falsy | ✅ Fixed | `if hour is None` in ephemeris.py |
| P-4 | Ayanamsha silent failure | ✅ Fixed | Raise ValueError on unknown ayanamsha |
| N-1 | Narayana Dasha: Taurus = 4yr (should be 7yr) | ✅ Fixed | Period table in narayana_dasa.py |
| S-2 | Shadbala J14 formula = hardcoded 3851 | ✅ Fixed | `min(60, mean_motion/|speed|×60)` |
| E-1 | JDN Gregorian +0.5 day correction missing | ✅ Not present in Python code | regression test added |
| A-2 | Mercury direction: wrong row reference | ✅ Not present in Python code | regression test added |
| R21 | Pushkara Navamsha scoring stub (always 0) | ✅ Fixed (Session 11) | 24-zone lookup → +0.5 when triggered |

---

## Known Issues (v5 Excel)

From `LagnaMaster_Audit_v5_PVRNR.docx`:

**Critical**: N-1, E-1, P-1, P-4 — all resolved  
**High**: S-2, A-2 — all resolved  
**Deferred**: R21 Pushkara Navamsha — resolved Session 11  

---

## Source Files

| File | Description |
|------|-------------|
| `Lagna_Master5_clean.xlsx` | v5 workbook — 178 sheets, formula source of truth |
| `LagnaMaster_Audit_v5_PVRNR.docx` | Audit: 4 critical + 6 high issues, fix table |
| `LagnaMaster_ProgrammePlan_v1.docx` | Original 39-week programme plan (reference) |

---

## Timeline

| Milestone | Sessions | Calendar |
|-----------|----------|----------|
| Pilot live (end-to-end working) | 6 | ~1 week |
| All bugs fixed, regression passing | +4 | ~week 2 |
| All 10 modules complete + Monte Carlo + PN | +1 (Session 11) | ~week 3 |
| Kundali Milan, PDF, Chara Dasha | +3 (12–14) | ~week 4 |
| Production-ready v1 | ~18–20 total | ~5–6 weeks |

Original estimate for human team: 39 weeks.
