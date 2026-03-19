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
src/ephemeris.py        ← pyswisseph DE441 wrapper
        ↓
src/calculations/       ← 10 Jyotish modules (translated from Excel)
  dignity.py            ← exaltation, debilitation, own sign, moolatrikona
  friendship.py         ← natural + temporary planetary friendships
  shadbala.py           ← 6 components: Sthana, Dig, Kala, Chesta, Drik, Naisargika
  narayana_dasa.py      ← 91-year sign-based predictive cycle
  ashtakavarga.py       ← 337 bindu tables, SAV aggregation
  argala.py             ← planetary intervention analysis
  arudha.py             ← pada calculation for all 12 houses
  karakas.py            ← chara + sthira karakas
  combustion.py         ← orb-based combustion detection
  retrograde.py         ← station detection + shadow periods
        ↓
src/scoring.py          ← 26 rules × 12 houses = 312 evaluations per chart
                           Score: [-10, +10] per domain, capped at ±3.0 per planet
                           Schools: Parashari (default), KP, Jaimini (gated)
        ↓
src/api/                ← FastAPI endpoints
  charts.py             ← POST /charts, GET /charts/{id}
  scores.py             ← GET /charts/{id}/scores
        ↓
src/ui/app.py           ← Streamlit: birth input → chart display → domain scores
        ↓
SQLite → PostgreSQL     ← chart store (immutable inserts)
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

## Pilot Build — 6 Sessions (~1 week)

| Session | Deliverable | Validates |
|---------|------------|-----------|
| 1 | `src/ephemeris.py` — pyswisseph wrapper | 1947 lagna + Sun position |
| 2 | `src/calculations/` — 43 CALC sheets → Python (1:1, bugs included) | Output matches Excel |
| 3 | `src/scoring.py` + `src/api/` — scoring engine + FastAPI | API returns scores |
| 4 | `src/ui/app.py` — Streamlit UI end-to-end | Birth input → chart → scores |
| 5 | SQLite persistence + chart history | Charts saved/retrieved |
| 6 | Docker Compose | Shareable local deploy |

---

## Accuracy Iteration — Sessions 7–10

Fix the 6 known bugs from the v5 audit, in severity order:

| ID | Bug | Fix |
|----|-----|-----|
| E-1 | JDN Gregorian correction missing | Add +0.5 day offset in ephemeris.py |
| P-1 | Midnight birth: 0 treated as falsy | `if hour is None` not `if not hour` |
| P-4 | Ayanamsha silent failure | Raise on invalid ayanamsha name |
| N-1 | Narayana Dasha: Taurus = 4yr (should be 7yr) | Fix period table in narayana_dasa.py |
| S-2 | Shadbala J14 formula = 3851 (wrong) | Correct cell reference in shadbala.py |
| A-2 | Mercury direction: wrong row reference | Fix lookup in retrograde.py |

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
