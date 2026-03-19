# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

**Strategy**: Pilot-first → accuracy iteration. Ship a working end-to-end app in ~1 week, then fix calculation accuracy module by module.

---

## Tech Stack

| Layer | Pilot (v1) | Production (v2) |
|-------|-----------|-----------------|
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
src/calculations/            ← 9 Jyotish modules (translated from Excel CALC sheets)
  dignity.py                 ← exaltation/debilitation/own/mooltrikona, combustion, Neecha Bhanga
  nakshatra.py               ← 27 nakshatras, 4 padas, D9 navamsha, Ganda Mool
  friendship.py              ← Naisargika + Tatkalik → Panchadha Maitri (5-fold)
  house_lord.py              ← whole-sign house map, Kendra/Trikona/Dusthana helpers
  chara_karak.py             ← 7 Jaimini Chara Karakas (AK → GK)
  narayana_dasa.py           ← sign-based 81-year predictive cycle
  shadbala.py                ← 6-component planetary strength in Virupas
  vimshottari_dasa.py        ← 120-year nakshatra dasha: 9 MDs × 9 ADs [Session 6]
  yogas.py                   ← 13 yoga types: PM/Raj/Dhana/Lunar/Solar/Special [Session 7]
        ↓
src/scoring.py               ← 22 BPHS rules × 12 houses = 264 evaluations per chart
                                WC rules (R03/R05/R07/R14) count at 0.5× weight
                                Scores clamped to [-10, +10]; rating Excellent→Very Weak
        ↓
src/api/main.py              ← FastAPI: POST /charts, GET /charts, GET /charts/{id}(/scores)
src/api/models.py            ← Pydantic: BirthDataRequest, ChartOut, ChartScoresOut
        ↓
src/db.py                    ← SQLite immutable inserts (_SENTINEL testability pattern)
        ↓
src/ui/chart_visual.py       ← South Indian SVG chart renderer [Session 6]
src/ui/app.py                ← Streamlit 5-tab UI: Chart/Scores/Yogas/Dasha/Rules [Sessions 4,6,7]
```

---

## Regression Fixture

**1947 India Independence Chart** (primary validator):
- Birth: 1947-08-15 00:00 IST, New Delhi (28.6139°N, 77.2090°E)
- Lagna: 7.7286° Taurus
- Sun: 27.989° Cancer
- Ayanamsha: Lahiri

All modules must pass this fixture before being considered done.

---

## Pilot Build — Sessions 1–7 ✅ Complete

| Session | Deliverable | Status | Tests |
|---------|------------|--------|-------|
| 1 | `src/ephemeris.py` — pyswisseph wrapper | ✅ Done | 14/14 |
| 2 | `src/calculations/` — 7 modules (dignity, nakshatra, friendship, house_lord, chara_karak, narayana_dasa, shadbala) | ✅ Done | 36/36 |
| 3 | `src/scoring.py` + `src/api/` + `src/db.py` — 22-rule engine + FastAPI + SQLite | ✅ Done | 20/20 |
| 4 | `src/ui/app.py` — Streamlit 3-tab UI (Chart / Domain Scores / Rule Detail) | ✅ Done | 6/6 |
| 5 | Docker Compose + Dockerfile + Makefile + integration tests (17) | ✅ Done | 17/17 |
| 6 | `vimshottari_dasa.py` + `chart_visual.py` (South Indian SVG) + 4-tab UI | ✅ Done | 20/20 |
| 7 | `yogas.py` (13 yoga types) + enriched planet table + Yogas tab in UI | ✅ Done | 14/14 |
| 8 | Accuracy fixes: E-1 (JDN +0.5) + A-2 (Mercury direction) | 🔲 Next | — |

**Total tests passing: 127/127**

---

## Accuracy Iteration — Sessions 8–11

Fix the 6 known bugs from the v5 audit, in severity order:

| ID | Bug | Status | Fix |
|----|-----|--------|-----|
| P-1 | Midnight birth: 0 treated as falsy | ✅ Fixed | `if hour is None` in ephemeris.py |
| P-4 | Ayanamsha silent failure | ✅ Fixed | Raise ValueError on unknown ayanamsha |
| N-1 | Narayana Dasha: Taurus = 4yr (should be 7yr) | ✅ Fixed | Period table in narayana_dasa.py |
| S-2 | Shadbala J14 formula = hardcoded 3851 | ✅ Fixed | `min(60, mean_motion/\|speed\|×60)` |
| E-1 | JDN Gregorian +0.5 day correction missing | 🔲 Session 8 | Add offset in ephemeris.py |
| A-2 | Mercury direction: wrong row reference | 🔲 Session 8 | Fix lookup in retrograde.py |

After each fix: re-run 1947 regression fixture.

---

## Phase 3 — Production Hardening (Sessions 18–25)

- PostgreSQL migration (immutable inserts schema)
- Redis 3-tier caching
- Multi-user auth (JWT)
- Monte Carlo ±30min birth time (100 samples, <8s on 4 cores)
- KP and Jaimini school gates
- Docker → K8s
- Streamlit → Next.js

---

## Explicitly Deferred

- Monte Carlo: after all 10 modules are accurate
- Jaimini / KP: after Parashari is complete
- Celery: when concurrent users > 5
- K8s: when concurrent users > 20
- Next.js: after Streamlit validates UX

---

## Known Issues (v5 Excel)

From `LagnaMaster_Audit_v5_PVRNR.docx`:

**Critical**: N-1, E-1, P-1, P-4
**High**: S-2, A-2 (+ 4 others in audit doc)

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
| All 10 modules complete | +5 | ~week 3-4 |
| Production-ready v1 | ~18-20 total | ~5-6 weeks |

Original estimate for human team: 39 weeks.
