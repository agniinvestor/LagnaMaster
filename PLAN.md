# LagnaMaster — Build Plan

**Goal**: Transform a 178-sheet Excel Jyotish workbook into a deterministic, auditable, multi-user web platform with a genuine Life Pressure forecasting engine.

## Phase 1 — Pilot ✅ 222/222
S1–S10: ephemeris, calculations×7, scoring, UI, Docker, vimshottari+SVG, yogas, AV, gochara, panchanga

## Phase 2 — Features ✅ 225/225
S11–S19: pushkara+MC, milan, PDF, jaimini, KP, tajika, compat, APIv2, UI10tabs

## Phase 3 — Production ✅ 210/210
S20–S27: PostgreSQL+Redis, Celery, JWT, CI/CD, Kubernetes+Helm, Next.js, school gates, MC chord

## Phase 4 — Pressure Engine ✅ COMPLETE

| S | Deliverable | Status | Tests |
|---|-------------|--------|-------|
| 28 | `functional_roles.py` — per-lagna maleficence, badhaka, maraka, kendradhipati, yogakaraka | ✅ Done | 9 |
| 29 | `avastha.py` — Deeptadi (6), Baladi (5), Lajjitadi (6) psychological states | ✅ Done | 6 |
| 30 | `pressure_engine.py` — Life Pressure Index: structural_vulnerability × dasha_activation × transit_load ÷ resilience; timeline output | ✅ Done | 9 |
| 31 | `argala.py` — Jaimini Argala/Virodhargala obstruction model + Arudha Lagna | ✅ Done | 5 |
| 32 | `graha_yuddha.py` + `scoring_v2.py` — Planetary war outcomes + declarative scoring engine with ENGINE_VERSION | ✅ Done | 7 |

**Grand total: 717/717 tests passing**

## Remaining gaps (future Phase 5)
- Vimsopaka Bala (divisional chart strength)
- Full Kala Sarpa Yoga detection
- Compound temporal activation model (multiplicative natal×dasha×transit)
- Audit log (user-action trail with engine version per run)
- Sandhi/boundary proximity sensitivity in scoring
