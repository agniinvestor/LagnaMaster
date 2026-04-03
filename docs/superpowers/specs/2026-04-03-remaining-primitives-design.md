# Design Spec: Remaining Primitives (Track 7)

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Spec only — implementation deferred until yoga chapters (Ch.34-42)
**Priority:** Low — no current encoding blocked

## 1. Same-Planet Constraint

**Problem:** BPHS2303 says "benefic exalted in 12th" meaning the SAME benefic must be both in 12th AND exalted. Current encoding uses two separate conditions which could match two different benefics.

**Solution:** Add `"bind": "same_planet"` field to conditions that must resolve to the same planet:

```json
[
  {"type": "planet_in_house", "planet": "any_benefic", "house": 12, "bind": "X"},
  {"type": "planet_dignity", "planet": "X", "dignity": "exalted"}
]
```

Where `"bind": "X"` creates a variable that the engine resolves to a specific planet, then reuses in subsequent conditions.

**Blocked rules:** 1 (BPHS2303). More expected in yoga chapters.

## 2. Shadbala Strength

**Problem:** BPHS2501 says "8th lord weak in Shadbala" — requires full 6-fold strength calculation.

**Solution:** New condition `planet_shadbala`:

```json
{"type": "planet_shadbala", "planet": "lord_of_8", "threshold": "weak"}
```

Requires implementing Shadbala computation (sthaana bala, dig bala, kaala bala, chesta bala, naisargika bala, drik bala). This is a major computation — deferred.

**Blocked rules:** 1 (BPHS2501).

## 3. Timing Activation

**Problem:** Timing rules are deterministic ("event at age X") but BPHS implies probabilistic windows activated by dasha periods.

**Solution:** Add `activation` field to timing_window:

```json
"timing_window": {
  "type": "age_range",
  "value": [32, 33],
  "precision": "approximate",
  "activation": "dasha_of_trigger_planet"
}
```

Engine evaluates: timing fires only during the dasha/antardasha of the triggering planet within the age window.

**Blocked rules:** 0 (all timing rules work without this, just less precise).

## 4. Mother/Father Indicator (Dynamic Karaka)

**Problem:** BPHS1504 says "stronger of Moon and Mars" as mother indicator.

**Solution:** New condition `dynamic_karaka`:

```json
{"type": "dynamic_karaka", "karaka": "mother", "state": "strong"}
```

Engine resolves "mother karaka" to stronger of Moon/Mars, then checks state.

**Blocked rules:** 1 (BPHS1504).

## Summary

| Primitive | Blocked rules | Priority | Dependency |
|-----------|--------------|----------|------------|
| Same-planet constraint | 1 | Medium | Yoga chapters |
| Shadbala | 1 | Low | Major computation |
| Timing activation | 0 | Low | Dasha engine |
| Dynamic karaka | 1 | Low | Ch.32 karakas |

All deferred. Current modifiers are adequate placeholders.
