# S318 Consolidation Plan — Parallel Implementation Cleanup

**Created:** S317 (2026-04-06)
**Problem:** S317 built parallel implementations without checking existing code first.
Five items need consolidation before new Tier 1 work begins.

## 1. Avastha Consolidation (3 → 1)

### Current state

| Module | Source | Even-Sign Reversal | Baaladi Effects | Consumers |
|--------|--------|-------------------|----------------|-----------|
| `avasthas.py` (S317) | BPHS Ch.45 text | ✅ Correct | BPHS (0.25/0.5/1.0/0.125/0.0) | multi_axis_scoring (Baaladi only) |
| `avastha_v2.py` (S39) | Secondary | ✅ Correct | Non-BPHS (Vridha=0.5) | scoring_v3.py, planet_effectiveness.py |
| `planet_avasthas.py` (S138) | Saravali/Phaladeepika | ❌ **BUG: no reversal** | Non-BPHS (0.65-1.20 range) | Unknown |

### Plan
1. **Primary:** `avasthas.py` becomes the single BPHS-authoritative module
2. **Migrate consumers:** `scoring_v3.py` and `planet_effectiveness.py` switch from `avastha_v2.py` to `avasthas.py`
3. **planet_avasthas.py:** Keep Deeptadi (9-state system from Phaladeepika — not in BPHS, but useful). Fix the even-sign bug. Mark as "alternative school" module.
4. **avastha_v2.py:** Delete after migration — fully superseded by `avasthas.py`

### Unique content to preserve from each
- `avastha_v2.py`: Lajjitadi effects (Kopa, Garvita descriptions) — merge into avasthas.py
- `planet_avasthas.py`: Deeptadi (9 states: Deepta/Swastha/Pramudita/Shanta/Deena/Vikala/Kopa/Khala/Bhita) — keep as separate system, not in BPHS
- `avasthas.py`: Baaladi, Jagradadi, Lajjitadi, Sayanadi — all from BPHS Ch.45

## 2. is_natural_malefic Wiring

### Current state
Function exists in `rule_firing.py` but only called from `shadbala.py:compute_drik_bala()` and `bhava_bala.py`.

### Unwired consumers (still use static `_MALEFICS`/`_BENEFICS`)
- `rule_firing.py` lines 1084-1170: condition matching for corpus rules
- `multi_axis_scoring.py`: Kartari yoga detection uses hardcoded sets
- Any other module that classifies planets as natural benefic/malefic

### Plan
1. Replace `pname not in _MALEFICS` with `not is_natural_malefic(pname, chart)` at lines 1084, 1170
2. Replace `pname not in _BENEFICS` with `is_natural_malefic(pname, chart)` at lines 1086, 1168
3. Update Kartari yoga detection in multi_axis_scoring.py
4. Keep static `_MALEFICS`/`_BENEFICS` as fallback for when chart is unavailable

## 3. Gulika Caller Wiring

### Current state
`compute_mandi_gulika()` in `planetary_state.py` — zero callers in `src/`.

### Plan
1. Find where Mandi/Gulika longitudes are expected (likely in chart object or upagraha dict)
2. Call `compute_mandi_gulika()` during chart construction or upagraha computation
3. Ensure the new `lat`/`lon` parameters are passed from the chart construction context

## 4. D1/D2 Constants Consumer

### Current state
`DHATU_PLANETS`, `MOOLA_PLANETS`, `JEEVA_PLANETS`, `SATWIK_PLANETS`, `RAJASIK_PLANETS`, `TAMASIK_PLANETS` — defined in `dignity.py`, zero consumers.

### Plan
These are classification constants for future features (horary, personality). No immediate consumer needed. Document as "available primitives" — not a consolidation issue.

## 5. Old sputa_drishti_strength Cleanup

### Current state
`sputa_drishti_strength()` and `compute_all_aspects()` in `sputa_drishti.py` — only called internally (not from other modules). Superseded by `bphs_drishti_virupas()`.

### Plan
1. Verify no external callers (already confirmed)
2. Mark as deprecated or remove
3. Keep `get_aspect_strength()` (house-based lookup) — still used by `bhava_bala.py` and `yoga_strength.py` alongside the BPHS continuous function

## Execution Order for S318
1. Avastha consolidation (highest risk — touches scoring pipeline)
2. is_natural_malefic wiring (medium risk — condition matching)
3. Gulika caller wiring (low risk — additive)
4. Old sputa cleanup (low risk — removal)
5. D1/D2 — no action needed
