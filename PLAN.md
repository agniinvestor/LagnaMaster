# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform.

**Strategy**: Pilot-first → accuracy iteration. Ship working end-to-end app, then expand module by module.

---

## Tech Stack

| Layer | Pilot (v1) | Production (v2) |
|-------|-----------|----------------|
| Ephemeris | pyswisseph (Moshier fallback) | pyswisseph + DE441 |
| Backend | FastAPI (sync) | FastAPI + Celery |
| Database | SQLite | PostgreSQL |
| Cache | In-memory | Redis 3-tier |
| UI | Streamlit (12-tab) | Next.js |
| Deploy | Docker Compose | K8s |
| Auth | Single user | Multi-user JWT |

---

## Architecture

```
Birth Data (date, time, lat/lon)
        ↓
src/ephemeris.py             ← pyswisseph wrapper → BirthChart
        ↓
src/calculations/            ← 18 Jyotish modules
  dignity.py                 ← S2: exaltation/debilitation, combustion, Neecha Bhanga
  nakshatra.py               ← S2: 27 nakshatras, 4 padas, D9, Ganda Mool
  friendship.py              ← S2: Naisargika + Tatkalik → Panchadha Maitri
  house_lord.py              ← S2: whole-sign house map, Kendra/Trikona helpers
  chara_karak.py             ← S2: 7 Jaimini Chara Karakas
  narayana_dasa.py           ← S2: sign-based 81-year dasha
  shadbala.py                ← S2: 6-component planetary strength
  vimshottari_dasa.py        ← S6: 120-year nakshatra dasha (9 MDs × 9 ADs)
  yogas.py                   ← S7: 13 yoga types
  ashtakavarga.py            ← S8: Parashari 8-source bindu tables
  gochara.py                 ← S9: Transit analysis, Sade Sati
  panchanga.py               ← S10: 5-limb almanac + D9
  pushkara_navamsha.py       ← S11: Pushkara Navamsha detection
  kundali_milan.py           ← S12: Ashtakoot 36-pt compatibility
  chara_dasha.py             ← S14: Jaimini Chara Dasha
  varga.py                   ← S15: D2/D3/D4/D7/D9/D10/D12/D60
  sapta_varga.py             ← S16: Sapta Varga Vimshopak Bala (20-pt)
  kp.py                      ← S17: KP Sub-lord system
  varshaphala.py             ← S18: Annual Solar Return, Muntha, Tajika
        ↓
src/scoring.py               ← 22 BPHS rules × 12 houses
src/montecarlo.py            ← S11: ±30-min birth-time sensitivity
src/reports/pdf_report.py    ← S13: reportlab PDF export
        ↓
src/api/main.py              ← FastAPI: POST/GET /charts + /scores + /health
src/api/models.py            ← Pydantic v2
src/db.py                    ← SQLite immutable inserts
        ↓
src/ui/app.py                ← S19: Streamlit 12-tab UI (all S1-S18 surfaces)
src/ui/chart_visual.py       ← South Indian SVG: D1 + D9 + Varga
```

---

## Regression Fixture

**1947 India Independence Chart** — primary validator for every module.
Birth: 1947-08-15 00:00 IST, New Delhi (28.6139°N, 77.2090°E)
Lagna: 7.7286° Taurus | Sun: 27.989° Cancer | Ayanamsha: Lahiri

---

## Pilot Build — Sessions 1–10 ✅ Complete (222 tests)

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 1 | `ephemeris.py` — pyswisseph wrapper | 14 |
| 2 | 7 calculation modules (dignity → shadbala) | 36 |
| 3 | `scoring.py` + FastAPI + SQLite | 20 |
| 4 | `ui/app.py` — Streamlit 3-tab UI | 6 |
| 5 | Docker Compose + integration tests | 17 |
| 6 | `vimshottari_dasa.py` + South Indian SVG | 20 |
| 7 | `yogas.py` (13 yoga types) | 14 |
| 8 | `ashtakavarga.py` + E-1/A-2 regression guards | 26 |
| 9 | `gochara.py` (transit, Sade Sati) | 29 |
| 10 | `panchanga.py` (5-limb almanac) + D9 navamsha | 40 |

---

## Expansion Build — Sessions 11–19 ✅ Complete (199 tests)

| Session | Deliverable | Tests |
|---------|-------------|-------|
| 11 | `pushkara_navamsha.py` + `montecarlo.py` | 30 |
| 12 | `kundali_milan.py` (Ashtakoot 36-pt) | 25 |
| 13 | `src/reports/pdf_report.py` (reportlab) | 15 |
| 14 | `chara_dasha.py` (Jaimini Chara Dasha) | 20 |
| 15 | `varga.py` (D2/D3/D4/D7/D9/D10/D12/D60) | 25 |
| 16 | `sapta_varga.py` (Vimshopak Bala 20-pt) | 20 |
| 17 | `kp.py` (KP Star/Sub/Sub-Sub + significators) | 22 |
| 18 | `varshaphala.py` (Solar Return, Muntha, Tajika) | 22 |
| 19 | `ui/app.py` — 12-tab Streamlit UI (all S1-S18) | 20 |

**Grand total: 421/421 tests passing**

---

## Session 19 — Streamlit UI ✅ Complete

12-tab layout surfacing all S1-S18 modules:

| Tab | Content | New in S19? |
|-----|---------|------------|
| 📊 Chart | SVG + Panchanga + Shadbala + D9 + Pushkara + Monte Carlo + PDF | Enhanced |
| 🏠 Domain Scores | 12-house bar chart + rating badges | Existing |
| 🧘 Yogas | Yoga cards by category | Existing |
| 🔢 Ashtakavarga | Sarva bar + per-planet grids | Existing |
| ⏱ Dashas | Vimshottari + Chara Dasha (S14) | Enhanced |
| 🌍 Transits | Sade Sati, Guru-Chandal, per-planet table | Existing |
| 📐 Varga Charts | D2-D60 SVG grids + planet table (S15) | ✅ NEW |
| ⚖️ Vimshopak | 20-pt dignity table + ranking bar (S16) | ✅ NEW |
| 🔑 KP Analysis | Sub-lord table + house significators (S17) | ✅ NEW |
| 🌟 Annual Chart | Solar return + Tajika aspects (S18) | ✅ NEW |
| 💑 Kundali Milan | Ashtakoot 36-pt compatibility (S12) | ✅ NEW |
| 📋 Rule Detail | Per-house 22-rule breakdown | Existing |

---

## Accuracy Audit ✅ All 6 Bugs Resolved (Sessions 1–10)

| ID | Bug | Resolution |
|----|-----|-----------|
| P-1 | Midnight birth: hour=0 falsy | `if hour is None` — Fixed S1 |
| P-4 | Ayanamsha silent failure | Raise ValueError — Fixed S1 |
| N-1 | Narayana Dasha Taurus = 4yr | Period table corrected — Fixed S2 |
| S-2 | Shadbala J14 hardcoded 3851 | Proper Chesta formula — Fixed S2 |
| E-1 | JDN +0.5 day correction | Not in Python code; regression test added S8 |
| A-2 | Mercury direction wrong row | Not in Python code; regression test added S8 |

---

## Phase 3 — Production Hardening (Sessions 20–27)

* PostgreSQL migration + Redis 3-tier caching
* Multi-user auth (JWT + role-based access)
* Celery workers for concurrent chart computation
* Placidus house cusps for proper KP (replaces whole-sign pilot)
* Docker → Kubernetes
* Streamlit → Next.js frontend
* Monte Carlo parallelisation (4 cores, <8s for 100 samples)

---

## Explicitly Deferred

* Celery: when concurrent users > 5
* K8s: when concurrent users > 20
* Next.js: after Streamlit validates all UX patterns
* Placidus KP: after whole-sign pilot validated by users

---

## Source Reference Files

| File | Description |
|------|-------------|
| `Lagna_Master5_clean.xlsx` | v5 workbook — 178 sheets, formula source of truth |
| `LagnaMaster_Audit_v5_PVRNR.docx` | Audit: 4 critical + 6 high issues, fix table |
| `LagnaMaster_ProgrammePlan_v1.docx` | Original 39-week programme plan |

---

## Timeline

| Milestone | Sessions | Calendar |
|-----------|---------|----------|
| Pilot live (end-to-end) | S1-6 | ~week 1 |
| All bugs fixed, regression passing | S7-10 | ~week 2 |
| Expansion modules (S11-S18) | S11-18 | ~weeks 3-5 |
| Full UI integration (S19) | S19 | ~week 5 |
| Production hardening | S20-27 | ~weeks 6-9 |

Original estimate for human team: 39 weeks.
