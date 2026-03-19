# LagnaMaster — Project Memory

> Last updated: 2026-03-20 (Session 32)

## Current state

| Item | Value |
|------|-------|
| Sessions done | 1–32 |
| Tests passing | 693/693 |
| Status | Phase 4 complete |
| Next | Phase 5: Vimsopaka Bala, Kala Sarpa, audit log |

## New modules (Phase 4)

```
src/calculations/
  functional_roles.py   S28  per-lagna maleficence matrix
  avastha.py            S29  Deeptadi/Baladi/Lajjitadi
  pressure_engine.py    S30  Life Pressure Index (the core engine)
  argala.py             S31  Argala + Arudha Lagna
  graha_yuddha.py       S32  Planetary war detection
  scoring_v2.py         S32  Declarative engine + ENGINE_VERSION
```

## Critical invariants (updated)

1–16: see previous MEMORY.md
17. functional_roles.py must be called with chart (not lagna_sign_index alone) — needs planet positions for house occupancy
18. pressure_engine components are additive approximations — not a certified Jyotish formula; label accordingly in UI
19. scoring_v2 ENGINE_VERSION must be stored in score_runs table for audit trail
20. graha_yuddha only applies to 5 planets: Mars/Mercury/Jupiter/Venus/Saturn — luminaries and nodes excluded

## Remaining gaps

| Gap | Module needed |
|-----|--------------|
| Vimsopaka Bala | `src/calculations/vimsopaka.py` |
| Kala Sarpa Yoga | add to `yogas.py` |
| Sandhi effects | add to `dignity.py` |
| Audit log | migration + `score_runs.engine_version` column |
| Compound multiplicative model | refactor `pressure_engine.py` |
