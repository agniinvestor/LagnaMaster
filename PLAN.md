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
src/calculations/            ← 18 Jyotish modules
  dignity.py                 ← exaltation/debilitation/own/mooltrikona, combustion, Neecha Bhanga
  nakshatra.py               ← 27 nakshatras, 4 padas, D9 navamsha, Ganda Mool
  friendship.py              ← Naisargika + Tatkalik → Panchadha Maitri (5-fold)
  house_lord.py              ← whole-sign house map, Kendra/Trikona/Dusthana helpers
  chara_karak.py             ← 7 Jaimini Chara Karakas (AK → GK)
  narayana_dasa.py           ← sign-based 81-year predictive cycle
  shadbala.py                ← 6-component planetary strength in Virupas
  vimshottari_dasa.py        ← 120-year nakshatra dasha: 9 MDs × 9 ADs [S6]
  yogas.py                   ← 13 yoga types: PM/Raj/Dhana/Lunar/Solar/Special [S7]
  ashtakavarga.py            ← Parashari 8-source bindu system: 7 planets + Sarva [S8]
  gochara.py                 ← Transit analysis: GocharaReport, Sade Sati, AV bindus [S9]
  panchanga.py               ← 5-limb almanac: Tithi/Vara/Nakshatra/Yoga/Karana + D9 [S10]
  pushkara_navamsha.py       ← Pushkara Navamsha detection + Monte Carlo sensitivity [S11]
  kundali_milan.py           ← Ashtakoot Kundali Milan: 8 kutas × 36 pts [S12]
  chara_dasha.py             ← Jaimini Chara Dasha: sign-based 9 MDs × 9 ADs [S14]
  varga.py                   ← Varga divisional charts: D2/D3/D4/D7/D9/D10/D12/D60 [S15]
  sapta_varga.py             ← Sapta Varga Vimshopak Bala: 20-pt weighted dignity [S16]
  kp.py                      ← KP Sub-lord system: Star/Sub/Sub-Sub + significators [S17]
  varshaphala.py             ← Varshaphala annual solar return: Muntha, Tajika aspects [S18]
        ↓
src/scoring.py               ← 22 BPHS rules × 12 houses = 264 evaluations per chart
src/montecarlo.py            ← Birth-time sensitivity: ±30 min, 100 samples [S11]
src/reports/                 ← PDF export (reportlab) [S13]
        ↓
src/api/main.py              ← FastAPI: POST/GET /charts + /scores + /health
src/api/models.py            ← Pydantic v2 request/response models
src/db.py                    ← SQLite immutable inserts (_SENTINEL testability pattern)
        ↓
src/ui/chart_visual.py       ← South Indian SVG: D1 + D9 navamsha charts
src/ui/app.py                ← Streamlit multi-tab UI
```

---

## Regression Fixture

**1947 India Independence Chart** — primary validator for every module.

* Birth: 1947-08-15 00:00 IST, New Delhi (28.6139°N, 77.2090°E)
* Lagna: 7.7286° Taurus | Sun: 27.989° Cancer | Ayanamsha: Lahiri

---

## Pilot Build — Sessions 1–10 ✅ Complete (222 tests)

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1 | `ephemeris.py` — pyswisseph wrapper | 14 |
| 2 | 7 calculation modules (dignity → shadbala) | 36 |
| 3 | `scoring.py` + FastAPI + SQLite | 20 |
| 4 | Streamlit UI (3-tab) | 6 |
| 5 | Docker Compose + integration tests | 17 |
| 6 | `vimshottari_dasa.py` + South Indian SVG | 20 |
| 7 | `yogas.py` (13 yoga types) | 14 |
| 8 | `ashtakavarga.py` + E-1/A-2 regression guards | 26 |
| 9 | `gochara.py` (transit analysis, Sade Sati) | 29 |
| 10 | `panchanga.py` (5-limb almanac) + D9 navamsha | 40 |

---

## Expansion Build — Sessions 11–18 ✅ Complete (179 tests)

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 11 | `pushkara_navamsha.py` + `montecarlo.py` (±30 min, 100 samples) | 30 |
| 12 | `kundali_milan.py` (Ashtakoot 36-pt compatibility) | 25 |
| 13 | `src/reports/` (PDF export structure, reportlab) | 15 |
| 14 | `chara_dasha.py` (Jaimini Chara Dasha, sign-based) | 20 |
| 15 | `varga.py` (D2/D3/D4/D7/D9/D10/D12/D60 divisional charts) | 25 |
| 16 | `sapta_varga.py` (Sapta Varga Vimshopak Bala, 20-pt) | 20 |
| 17 | `kp.py` (KP Star/Sub/Sub-Sub lords + house significators) | 22 |
| 18 | `varshaphala.py` (Annual Solar Return, Muntha, Tajika aspects) | 22 |

**Grand total: 401/401 tests passing**

---

## Accuracy Audit ✅ All 6 Bugs Resolved

| ID | Bug | Resolution |
|----|-----|-----------|
| P-1 | Midnight birth: hour=0 falsy | `if hour is None` — Fixed S1 |
| P-4 | Ayanamsha silent failure | Raise ValueError — Fixed S1 |
| N-1 | Narayana Dasha Taurus = 4yr | Period table corrected — Fixed S2 |
| S-2 | Shadbala J14 hardcoded 3851 | Proper Chesta formula — Fixed S2 |
| E-1 | JDN +0.5 day correction | Not in Python code; regression test added S8 |
| A-2 | Mercury direction wrong row | Not in Python code; regression test added S8 |

---

## Phase 3 — Production Hardening (Sessions 19–26)

* PostgreSQL migration (immutable inserts schema)
* Redis 3-tier caching
* Multi-user auth (JWT + role-based)
* Celery workers for concurrent chart computation
* Docker → Kubernetes
* Streamlit → Next.js frontend
* UI integration: Varga/Vimshopak/KP/Varshaphala tabs

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
|-----------|---------|----------|
| Pilot live (end-to-end working) | 6 | ~week 1 |
| All bugs fixed, regression passing | +4 | ~week 2 |
| All 10 core modules complete | +5 | ~week 3 |
| Expansion modules (S11–S18) | +8 | ~weeks 4–5 |
| Production-ready v1 | ~19–22 total | ~6–8 weeks |

Original estimate for human team: 39 weeks.
