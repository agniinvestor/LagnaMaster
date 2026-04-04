# Design Spec: S316 Engine Activation — Full Closure

**Date:** 2026-04-04
**Session:** S316 (governance)
**Status:** Approved
**Scope:** 20 open items — 6 primitives, 5 engine features, 2 schema changes, 4 governance decisions, 3 open loops

## Problem

The system is WIDE but SHALLOW. 600 V2 rules exist but:
- 496 rules have modifiers that don't fire
- 97 rules have BB chains that don't execute
- 24 rules are NON-COMPUTABLE (missing primitives)
- Ch.32-42 BLOCKED by missing same_planet_constraint + dynamic_karaka
- No conflict resolution, no activation hooks, no interpretation layer

More encoding without engine activation increases breadth without depth.

## Decision

Close ALL 20 open items in a single session. Three-wave execution with a contract-lock pre-phase.

## Definition of Done

- Rules fire
- Modifiers apply (gates evaluate, amplifies/attenuates scale, negates flips)
- Conflicts resolve deterministically
- Strength is comparable across primitives
- Outputs are rankable (not just present)

---

## Wave 0 — Engine Contracts (MANDATORY FIRST)

### Contract 1: Condition Evaluator Interface

`_check_compound_conditions` remains the universal gateway. Extension via **mutable context accumulator**:

```python
def _check_compound_conditions(
    conditions: list[dict], chart, context: dict | None = None
) -> tuple[bool, int]:
```

- Existing 16 primitives: unchanged, don't use context
- New primitives (argala, shadbala): write to `context["conditions"][f"cond_{idx}"]`
- After all conditions evaluated: `context["aggregates"] = aggregate_condition_metadata(context["conditions"])`
- Return signature unchanged: `(bool, int)`

**Aggregation function:**
```python
def aggregate_condition_metadata(conditions: dict) -> dict:
    """Compute summary aggregates from per-condition metadata."""
    agg = {"bb_strength": 0.0, "bb_houses": []}
    # Argala: sum strengths across argala conditions
    argala_total = sum(
        c["metadata"].get("argala_strength", 0)
        for c in conditions.values()
        if c.get("type") == "argala_condition"
    )
    if argala_total > 0:
        agg["argala_strength_total"] = min(1.0, argala_total)
    # Shadbala: pass through normalized value
    for c in conditions.values():
        if c.get("type") == "shadbala_strength":
            agg["shadbala_normalized"] = c["metadata"].get("shadbala_normalized", 0)
    return agg
```

**Context schema (strict):**
```python
context = {
    "conditions": {
        "cond_0": {
            "type": "argala_condition",
            "metadata": {
                "argala_strength": 0.7,
                "argala_type": "benefic",
                "obstruction": "partial",
                "contributing_houses": [2, 4],
                "net_score": 3.5,
            }
        }
    },
    "aggregates": {
        "argala_strength_total": 0.7,
        "bb_strength": 0.0,
    },
    "gates": {}  # namespaced gate evaluation results
}
```

**Condition IDs:** Auto-generated as `cond_{index}` — positional within each rule's condition list. No schema change to condition dicts.

**Context lifecycle:**
1. Created in `_check_rule_fires`
2. Passed to `_check_compound_conditions` (populated by primitives)
3. Passed to `apply_modifiers` (consumed by modifiers)
4. Attached to final `FiredRule.context`

### Contract 2: Modifier Execution

Application order (locked, do not revisit):
1. **Gates** — can short-circuit → `gated_out=True`
2. **Negates** — flips direction (3-tier: strong>0.7 flips, 0.3-0.7 weakens, <0.3 negligible)
3. **Attenuates** — reduces magnitude multiplicatively
4. **Amplifies** — increases magnitude multiplicatively
5. **Qualifies** — adds annotations, no magnitude change

```python
_EFFECT_ORDER = {"gates": 0, "negates": 1, "attenuates": 2, "amplifies": 3, "qualifies": 4}
```

Gate evaluation:
- Structured condition (list of dicts): evaluate via `_check_compound_conditions` with shared parent context (namespaced under `context["gates"]`)
- String condition (pre-migration): cannot evaluate → logged as unevaluated gate with severity

Weight scaling (context-aware):
```python
effective_weight = base_weight * (1 + 0.5 * ctx_strength)
```
Where `ctx_strength` comes from condition_context aggregates. Preserves modifier identity — weak argala doesn't nullify strong modifiers.

Stacking: multiplicative (existing behavior, confirmed correct).

### Contract 3: Strength Normalization

- Internal: continuous `[0.0, 1.0]` range
- Bucketing to weak/medium/strong: **only at interpretation layer**
- Existing `_STRENGTH_WEIGHTS = {"weak": 0.15, "medium": 0.30, "strong": 0.50}` remains the encoding-time mapping
- Runtime strength (from argala, shadbala) stays continuous

---

## Wave 1 — Modifier Stack (Sequential, Critical Path)

### 1.1 Modifier Condition Structured (Schema Migration)

Migrate 496 modifier condition strings to structured dicts.

**Process:**
1. `tools/migrate_modifier_conditions.py` scans all modifiers
2. Deterministic parse: strings that map cleanly to existing primitives → auto-convert
3. Ambiguous strings → keep as string with `"structured": false` flag
4. Expected: ~60% auto-convert, ~40% remain as strings

**Post-migration modifier schema:**
```python
# Structured (executable):
{"condition": [{"type": "planet_dignity", "planet": "lord_of_5", "dignity": "exalted"}],
 "effect": "gates", "target": "rule", "strength": "strong", "scope": "local"}

# Unstructured (informational):
{"condition": "other_six_planets_endowed_with_strength",
 "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
 "structured": false}
```

### 1.2 Modifier Execution

Full implementation of `apply_modifiers` per Contract 2.

**ModifiedRule dataclass (extended):**
```python
@dataclass
class ModifiedRule:
    rule_id: str
    primary_domain: str
    direction: str
    magnitude: float
    source_rule: FiredRule
    qualifications: list[str] = field(default_factory=list)
    gated_out: bool = False
    gate_reason: str = ""
    unevaluated_gates: list[dict] = field(default_factory=list)  # {condition, severity}
    context: dict | None = None
```

**Unevaluated gate severity:**
- `"blocking"` — gates effect with string condition (should gate but can't)
- `"informational"` — qualifies effect with string condition

**Negation logic (3-tier):**
```python
if weight > 0.7:  # strong negation: flip direction
    direction = flip(direction)
elif weight > 0.3:  # medium: weaken instead of flip
    magnitude *= (1 - weight)
else:  # weak: negligible
    pass
```

### 1.3 Conflict Resolution

In `aggregate_domains`:

1. **Net scoring** — current behavior (favorable - unfavorable)
2. **Contrary mirror cancellation** — rules with `rule_relationship.type == "contrary_mirror"` cancel to net 0
3. **Same-signal-group dominance** — if rules share `signal_group` and conflict, keep strongest only
4. **Confidence-weighted scoring** — `effective_magnitude = magnitude × confidence`

### 1.4 Integration Test Layer

After Wave 1, run India 1947 fixture through full pipeline:
- Rule firing → modifier application → conflict resolution → domain scores
- Verify: H2 score remains negative (existing invariant)
- Verify: gates reduce total fired rules (some rules now gated out)
- Verify: modifiers change magnitudes (not all 1.0)

---

## Wave 2 — Parallel Blast (5 Lanes)

### Lane A — Strength & Nature System

#### `functional_benefic` primitive

**Condition schema:**
```python
{"type": "functional_benefic", "planet": "Jupiter", "classification": "benefic"}
```

Classifications: `"benefic"` | `"malefic"` | `"yogakaraka"` | `"maraka"` | `"badhaka"`

**Evaluator:** Resolve planet → `compute_functional_classifications(chart.lagna_sign_index)` → check match. Binary output (no metadata needed).

Unblocks: ~20 rules (Ch.15, Ch.24, LP).

#### `shadbala_strength` primitive

**Condition schema:**
```python
{"type": "shadbala_strength", "planet": "lord_of_8", "threshold": "weak"}
```

**Evaluator:** `compute_shadbala(chart)` → normalize total_strength to [0,1] using BPHS minimum required strengths. Emits metadata:
```python
context["conditions"][f"cond_{idx}"]["metadata"] = {
    "shadbala_normalized": 0.35,
    "shadbala_components": {"sthana": 0.4, "dig": 0.6, ...}
}
```

Unblocks: 1 rule (BPHS2501).

### Lane B — Structural Primitives

#### `argala_condition` primitive

**Condition schema:**
```python
{
    "type": "argala_condition",
    "reference_house": 1,
    "argala_type": "benefic",       # "benefic" | "malefic" | "any"
    "min_strength": "medium",       # "weak" | "medium" | "strong"
    "obstruction": "unobstructed"   # "unobstructed" | "partial" | "any"
}
```

**Evaluator:** Calls existing `compute_argala(chart, reference_house)`.

**Normalization (MANDATORY):**
```python
def theoretical_max_argala(reference_house: int) -> float:
    """Maximum possible argala score for a house.
    
    3 primary argala houses (2nd, 4th, 11th from reference).
    Max per house: all benefics present, no obstruction.
    Benefic weight = 1.0 per planet, max 4 benefics = 4.0 per house.
    Total theoretical max = 12.0
    """
    return 12.0

normalized = min(1.0, max(0.0, result.net_argala_score / theoretical_max_argala(ref)))
```

**Metadata emission:**
```python
context["conditions"][f"cond_{idx}"] = {
    "type": "argala_condition",
    "metadata": {
        "argala_strength": normalized,
        "argala_type": actual_type,
        "obstruction": obstruction_level,
        "contributing_houses": [e.source_house for e in result.entries if e.active],
        "net_score": result.net_argala_score,
    }
}
```

Unblocks: 17 Ch.31 rules.

#### `same_planet_constraint` (bind variables)

**Schema:** `"bind"` field on conditions:
```python
[
    {"type": "planet_in_house", "planet": "any_benefic", "house": 12, "bind": "X"},
    {"type": "planet_dignity", "planet": "X", "dignity": "exalted"}
]
```

**Evaluator change:** In `_check_compound_conditions`, when a condition has `bind` and planet is a candidate list (any_benefic, any_malefic), iterate candidates. Lock the first that satisfies all downstream bound conditions.

**Bounded determinism:**
```python
MAX_BIND_ATTEMPTS = 10  # prevents exponential search
```

Short-circuit on first full match across all bound conditions.

Unblocks: Ch.34-42 (9 yoga chapters).

### Lane C — Identity / Role System

#### `dynamic_karaka` primitive

**Condition schema:**
```python
{"type": "dynamic_karaka", "karaka": "mother", "state": "strong"}
```

**Resolution rules (from BPHS):**
- Mother: stronger of Moon and Mars
- Father: stronger of Sun and Jupiter

"Stronger" = better dignity rank: exalted(5) > moolatrikona(4) > own_sign(3) > neutral(2) > debilitated(1).

Unblocks: Ch.32-33.

#### `navamsa_lagna` primitive

**Condition schema:**
```python
{"type": "navamsa_lagna", "sign": "aries"}
```

**Evaluator:** Compute navamsa sign of ascendant degree (same algorithm as `planet_in_navamsa_sign`, applied to lagna).

Unblocks: 1 rule (BPHS2114).

### Lane D — Engine Features

#### Bhavat Bhavam Execution

97 rules have `derived_house_chains`. Currently metadata-only.

**Canonical resolver:**
```python
# src/calculations/derived_house.py

def resolve_house(base: int, offset: int) -> int:
    """BPHS inclusive counting: '5th from 3rd' = house 7."""
    return (base + offset - 2) % 12 + 1
```

**Integration:** After primary conditions pass, BB chains contribute to context:
```python
if rule.derived_house_chains:
    for chain in rule.derived_house_chains:
        resolved = resolve_derived_house(chain, chart)
        context["aggregates"]["bb_houses"].append(resolved)
        context["aggregates"]["bb_strength"] = context["aggregates"].get("bb_strength", 0) + 0.2
```

BB strength is secondary evidence — modifiers can consume it for context-aware scaling.

**Enforcement:** ALL derived house arithmetic in rule_firing.py routed through `resolve_house()`. No direct `(base + offset - 2) % 12 + 1` anywhere else.

#### V1 Derivation Classification

```python
def _classify_v1_derivation(rule) -> str:
    if rule.verse_ref and rule.concordance_texts:
        return "verse_derived"
    elif rule.verse_ref:
        return "commentary_derived"
    else:
        return "interpretive"
```

Used in domain aggregation: V2 > V1. Within V1: verse_derived > commentary_derived > interpretive.

### Lane E — Activation / Timing

#### Timing Activation

**Hook in rule firing:**
```python
def _is_activated(rule, chart, dasha_context=None) -> bool:
    timing = getattr(rule, "timing_window", None)
    if not timing or timing.get("type") == "unspecified":
        return True
    # Dasha/transit activation: requires dasha engine (out of scope)
    return True
```

Wired as pre-check in `_check_rule_fires`. Default passthrough. Dasha activation logic is out of scope (requires dasha engine not yet built — see NOT IN SCOPE).

#### Prediction-Type Classification

`tools/classify_prediction_types.py` — keyword-based classifier:
- `"trait"` — personality/character
- `"event"` — life event with timing
- `"status"` — state/condition
- `"health"` — health outcome

Auto-assign where unambiguous, flag where unclear. Updates `prediction_type` field on rules.

---

## Wave 3 — Governance + Closure

### 3.1 Derived House Relationship (Foundation)

`src/calculations/derived_house.py` — canonical resolver (see Lane D above).

Tests: `resolve_house(3, 5) == 7`, `resolve_house(10, 5) == 2`, `resolve_house(1, 12) == 12`.

Refactor: grep all direct house arithmetic in rule_firing.py and route through.

### 3.2 Planet Archetypes (Shared Dependency)

```python
# src/corpus/planet_archetypes.py

PLANET_ARCHETYPES: dict[str, dict] = {
    "Sun":     {"nature": "malefic", "themes": ["authority", "father", "soul", "government"]},
    "Moon":    {"nature": "benefic", "themes": ["mind", "mother", "emotions", "public"]},
    "Mars":    {"nature": "malefic", "themes": ["energy", "courage", "siblings", "property"]},
    "Mercury": {"nature": "benefic", "themes": ["intellect", "speech", "commerce", "adaptability"]},
    "Jupiter": {"nature": "benefic", "themes": ["wisdom", "children", "dharma", "expansion"]},
    "Venus":   {"nature": "benefic", "themes": ["luxury", "spouse", "art", "pleasure"]},
    "Saturn":  {"nature": "malefic", "themes": ["delay", "discipline", "karma", "longevity"]},
    "Rahu":    {"nature": "malefic", "themes": ["obsession", "foreign", "unconventional", "amplification"]},
    "Ketu":    {"nature": "malefic", "themes": ["detachment", "spirituality", "past_karma", "loss"]},
}
```

Enforcement: `functional_benefic` references this for base nature. `_MALEFICS`/`_BENEFICS` in rule_firing.py derived from this registry (single source of truth).

### 3.3 Activation Conditions (Execution Layer)

Decision: Activation is a **separate layer** from condition evaluation. See Timing Activation (Lane E). Hook exists, default passthrough. Dasha/transit wiring requires dasha engine (out of scope — see NOT IN SCOPE).

### 3.4 Interpretation Abstraction Layer (Final Output)

```python
# src/calculations/interpretation.py

def interpret(prediction: dict, context: dict) -> str:
    """Annotated output from structured prediction + context."""
    claim = prediction.get("claim", "")
    qualifications = context.get("qualifications", [])
    planet = context.get("trigger_planet", "")
    archetype = PLANET_ARCHETYPES.get(planet, {})
    
    parts = [claim]
    if qualifications:
        parts.append(f"(qualified by: {', '.join(qualifications)})")
    if archetype.get("themes"):
        parts.append(f"[{planet} themes: {', '.join(archetype['themes'][:2])}]")
    
    return " ".join(parts)
```

Invariant: **No interpretation without context.** Semantic/render split noted for when templating is needed; current implementation is annotated output only.

### 3.5 Verse Audit Completeness

Extend `tools/v2_scorecard.py` Section M: flag chapters below 95% verse coverage with specific missing verse refs. Run on Ch.12-23 to identify the 5-8% gap.

### 3.6 India 1947 Fixture Diversity

Generate cross-validated tests across multiple chart configurations using existing PyJHora pipeline. Target: 216 additional tests covering 12 lagnas × varied planet positions.

### 3.7 Docs Pre-Push Enforcement

Extend `.git/hooks/pre-push`: when `src/corpus/` files are modified, verify corresponding docs updates exist. Warning (not blocking) for first iteration.

---

## Files Changed

### New Files
| File | Purpose |
|------|---------|
| `src/calculations/derived_house.py` | Canonical derived house resolver |
| `src/calculations/interpretation.py` | Interpretation abstraction layer |
| `src/corpus/planet_archetypes.py` | Central planet archetype registry |
| `tools/migrate_modifier_conditions.py` | Modifier condition migration script |
| `tools/classify_prediction_types.py` | Prediction type classifier |

### Modified Files
| File | Change |
|------|--------|
| `src/calculations/rule_firing.py` | Context accumulator, 6 new condition evaluators, bind variable support, activation hook, route house arithmetic through derived_house |
| `src/calculations/inference.py` | Full modifier execution (gate eval, 3-tier negation, context-aware scaling), conflict resolution upgrades, confidence-weighted scoring |
| `src/corpus/taxonomy.py` | New condition primitives in VALID_CONDITION_PRIMITIVES |
| `src/corpus/feature_registry.py` | Move 11 features from PENDING to IMPLEMENTED |
| `src/corpus/combined_corpus.py` | V1 derivation classification |
| `tools/v2_scorecard.py` | Verse audit completeness (Section M upgrade) |
| `.git/hooks/pre-push` | Docs enforcement |
| `src/corpus/bphs_v2_ch*.py` (19 files) | Modifier condition migration |

### Test Files
| File | Purpose |
|------|---------|
| `tests/test_s316_contracts.py` | Wave 0 contract tests |
| `tests/test_s316_modifier_execution.py` | Wave 1 modifier execution + conflict resolution |
| `tests/test_s316_primitives.py` | Wave 2 all 6 primitives |
| `tests/test_s316_governance.py` | Wave 3 derived house, archetypes, interpretation |
| `tests/test_s316_integration.py` | End-to-end: India 1947 through full pipeline |

---

## Execution Order

```
Wave 0 (sequential):   Contracts → taxonomy + context schema + tests
Wave 1 (sequential):   Modifier migration → modifier execution → conflict resolution → integration tests
Wave 2 (5 parallel lanes):
  Lane A: functional_benefic + shadbala_strength
  Lane B: argala_condition + same_planet_constraint
  Lane C: dynamic_karaka + navamsa_lagna
  Lane D: BB execution + V1 classification + derived_house resolver
  Lane E: timing activation + prediction-type classification
Wave 3 (sequential):   Planet archetypes → interpretation layer → verse audit → fixture diversity → docs hook
```

---

## Success Criteria

1. All 600 V2 rules fire with modifier application (gates evaluated where structured)
2. 6 new primitives unblock Ch.31 (argala), Ch.32-33 (karaka), Ch.34-42 (yogas), LP (functional benefic)
3. Conflict resolution is deterministic (contrary mirrors cancel, same-group strongest wins)
4. India 1947 fixture passes end-to-end with correct H2 negative score
5. All 11 pending features moved to IMPLEMENTED in feature_registry.py
6. Full test suite green (14,500+ tests including new S316 tests)
7. `v2_scorecard.py --all` shows no regression

## Not In Scope

- Dasha/transit activation logic (hook exists, implementation deferred)
- Full Shadbala engine rewrite (uses existing computation)
- V1 rule migration or exclusion (separate concern)
- Interpretation templating or prose generation
- UI/report rendering
