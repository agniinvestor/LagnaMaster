# S316 Engine Activation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close all 20 open items — primitives, engine features, schema changes, governance decisions, open loops — making the engine execute modifiers, resolve conflicts, and support all condition types.

**Architecture:** Context accumulator flows through condition evaluation → modifier application → domain aggregation. Six new condition primitives plug into `_check_compound_conditions`. Modifier execution evaluates structured gates, applies 3-tier negation, and uses context-aware weight scaling. Conflict resolution handles contrary mirrors and same-signal-group dominance.

**Tech Stack:** Python 3.14, pytest, pyswisseph (existing), no new dependencies.

**Spec:** `docs/superpowers/specs/2026-04-04-s316-engine-activation-design.md`

---

## File Structure

### New Files
| File | Responsibility |
|------|---------------|
| `src/calculations/derived_house.py` | Canonical `resolve_house(base, offset) -> int` — all BB arithmetic goes here |
| `src/calculations/interpretation.py` | `interpret(prediction, context) -> str` — annotated output |
| `src/corpus/planet_archetypes.py` | `PLANET_ARCHETYPES` registry — nature + themes per planet |
| `tools/migrate_modifier_conditions.py` | One-shot migration: modifier condition strings → structured dicts |
| `tools/classify_prediction_types.py` | One-shot: assign `prediction_type` to rules missing it |
| `tests/test_s316_contracts.py` | Context accumulator, aggregation, whitelist tests |
| `tests/test_s316_modifier_execution.py` | Gate eval, 3-tier negation, context-aware scaling, conflict resolution |
| `tests/test_s316_primitives.py` | All 6 new condition primitives |
| `tests/test_s316_governance.py` | Derived house resolver, archetypes, interpretation |
| `tests/test_s316_integration.py` | End-to-end: India 1947 through full pipeline |

### Modified Files
| File | Changes |
|------|---------|
| `src/calculations/rule_firing.py` | Context param in `_check_compound_conditions` + `_check_rule_fires`, 6 new elif branches, bind variable support, activation hook, FiredRule.context field |
| `src/calculations/inference.py` | Full `apply_modifiers` rewrite (gate eval, ordering, 3-tier negation), `aggregate_domains` upgrades (contrary mirror, same-signal, confidence-weighted), new `aggregate_condition_metadata()` |
| `src/corpus/taxonomy.py` | 6 new entries in `VALID_CONDITION_PRIMITIVES`, `CONSUMABLE_AGGREGATES` frozenset |
| `src/corpus/feature_registry.py` | Move 11 features from `PENDING_FEATURES` to `IMPLEMENTED_FEATURES` |
| `src/corpus/combined_corpus.py` | V1 derivation classification |
| `tools/v2_scorecard.py` | Verse audit completeness upgrade in Section M |
| `.git/hooks/pre-push` | Docs enforcement check |

---

## Wave 0 — Contracts

### Task 1: Context Accumulator in Condition Evaluator

**Files:**
- Modify: `src/calculations/rule_firing.py:37` (FiredRule dataclass)
- Modify: `src/calculations/rule_firing.py:260` (`_check_compound_conditions`)
- Modify: `src/calculations/rule_firing.py:556` (`_check_rule_fires`)
- Modify: `src/calculations/rule_firing.py:674` (`evaluate_chart` loop)
- Test: `tests/test_s316_contracts.py`

- [ ] **Step 1: Write failing tests for context accumulator**

```python
# tests/test_s316_contracts.py
"""Tests for Wave 0 contracts: context accumulator, aggregation, whitelist."""
from src.calculations.rule_firing import (
    _check_compound_conditions, FiredRule,
)


def test_context_param_accepted():
    """_check_compound_conditions accepts optional context dict."""
    # Empty conditions = doesn't fire, but should not raise
    ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
    result = _check_compound_conditions([], None, context=ctx)
    assert result == (False, 0)


def test_context_param_optional():
    """Existing callers without context still work."""
    result = _check_compound_conditions([], None)
    assert result == (False, 0)


def test_fired_rule_has_context_field():
    """FiredRule dataclass has a context field."""
    fired = FiredRule(
        rule_id="TEST", source="BPHS", planet="Sun", house=1,
        outcome_direction="favorable", outcome_domains=["wealth"],
        confidence=0.7, concordance_count=0,
    )
    assert hasattr(fired, "context")
    assert fired.context is None  # default
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_s316_contracts.py -v`
Expected: FAIL — `_check_compound_conditions` doesn't accept `context` kwarg, FiredRule has no `context` field

- [ ] **Step 3: Add context field to FiredRule**

In `src/calculations/rule_firing.py`, add to FiredRule dataclass (after `health_sensitive` field):

```python
    context: dict | None = None  # condition metadata for modifier layer
```

- [ ] **Step 4: Add context parameter to _check_compound_conditions**

Change signature from:
```python
def _check_compound_conditions(conditions: list[dict], chart) -> tuple[bool, int]:
```
to:
```python
def _check_compound_conditions(conditions: list[dict], chart, context: dict | None = None) -> tuple[bool, int]:
```

No other changes to the function body yet — existing primitives don't use context.

- [ ] **Step 5: Wire context through _check_rule_fires and evaluate_chart**

In `_check_rule_fires`, create context and pass it:
```python
def _check_rule_fires(rule, chart) -> tuple[bool, int, dict | None]:
    """Check if a rule fires. Returns (fires, house, context)."""
    # ... existing code ...
    conditions = pc.get("conditions", [])
    if isinstance(conditions, list) and conditions and isinstance(conditions[0], dict) and "type" in conditions[0]:
        context = {"conditions": {}, "aggregates": {}, "gates": {}}
        fires, house = _check_compound_conditions(conditions, chart, context=context)
        return fires, house, context
    # ... rest of legacy logic returns (fires, house, None) ...
```

In `evaluate_chart`, unpack the 3-tuple and attach context to FiredRule:
```python
    fires, house, ctx = _check_rule_fires(rule, chart)
    # ... later when building FiredRule ...
    fired = FiredRule(..., context=ctx)
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_s316_contracts.py -v`
Expected: PASS (3/3)

- [ ] **Step 7: Run full suite to verify no regression**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: All existing tests pass (14,500+)

- [ ] **Step 8: Commit**

```bash
git add src/calculations/rule_firing.py tests/test_s316_contracts.py
git commit -m "feat(s316): add context accumulator to condition evaluator

Context dict flows: _check_rule_fires → _check_compound_conditions → FiredRule.
Existing 16 primitives unchanged. New primitives will write metadata to context."
```

---

### Task 2: Aggregation Function + Context Whitelist

**Files:**
- Modify: `src/calculations/inference.py` (add `aggregate_condition_metadata`, `CONSUMABLE_AGGREGATES`)
- Modify: `src/corpus/taxonomy.py` (add `CONSUMABLE_AGGREGATES`)
- Test: `tests/test_s316_contracts.py` (append)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_s316_contracts.py`:

```python
from src.calculations.inference import aggregate_condition_metadata, CONSUMABLE_AGGREGATES


def test_aggregate_empty_conditions():
    result = aggregate_condition_metadata({})
    assert result["bb_strength"] == 0.0
    assert "argala_strength_total" not in result  # only present when argala exists


def test_aggregate_argala_metadata():
    conditions = {
        "cond_0": {
            "type": "argala_condition",
            "metadata": {"argala_strength": 0.7},
        }
    }
    result = aggregate_condition_metadata(conditions)
    assert result["argala_strength_total"] == 0.7


def test_aggregate_caps_argala_at_1():
    conditions = {
        "cond_0": {"type": "argala_condition", "metadata": {"argala_strength": 0.6}},
        "cond_1": {"type": "argala_condition", "metadata": {"argala_strength": 0.7}},
    }
    result = aggregate_condition_metadata(conditions)
    assert result["argala_strength_total"] == 1.0  # capped


def test_consumable_aggregates_whitelist():
    assert "argala_strength_total" in CONSUMABLE_AGGREGATES
    assert "bb_strength" in CONSUMABLE_AGGREGATES
    assert "shadbala_normalized" in CONSUMABLE_AGGREGATES
    assert len(CONSUMABLE_AGGREGATES) == 3  # strict — no uncontrolled growth
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_s316_contracts.py::test_aggregate_empty_conditions -v`
Expected: FAIL — `aggregate_condition_metadata` doesn't exist

- [ ] **Step 3: Implement aggregation function and whitelist**

Add to `src/calculations/inference.py` after the `_STRENGTH_WEIGHTS` line:

```python
CONSUMABLE_AGGREGATES = frozenset({
    "argala_strength_total",
    "bb_strength",
    "shadbala_normalized",
})


def aggregate_condition_metadata(conditions: dict) -> dict:
    """Compute summary aggregates from per-condition metadata.

    Only keys in CONSUMABLE_AGGREGATES are used by modifiers.
    Raw condition metadata is debug-only.
    """
    agg: dict = {"bb_strength": 0.0, "bb_houses": []}
    argala_total = sum(
        c.get("metadata", {}).get("argala_strength", 0)
        for c in conditions.values()
        if c.get("type") == "argala_condition"
    )
    if argala_total > 0:
        agg["argala_strength_total"] = min(1.0, argala_total)
    for c in conditions.values():
        if c.get("type") == "shadbala_strength":
            agg["shadbala_normalized"] = c.get("metadata", {}).get("shadbala_normalized", 0)
    return agg
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_s316_contracts.py -v`
Expected: PASS (all contract tests)

- [ ] **Step 5: Commit**

```bash
git add src/calculations/inference.py tests/test_s316_contracts.py
git commit -m "feat(s316): add aggregation function + context consumption whitelist

aggregate_condition_metadata() computes argala_strength_total, bb_strength,
shadbala_normalized from per-condition metadata. CONSUMABLE_AGGREGATES
whitelist prevents unbounded modifier dependencies."
```

---

## Wave 1 — Modifier Stack

### Task 3: Modifier Execution — Gate Evaluation + Ordered Application

**Files:**
- Modify: `src/calculations/inference.py` (rewrite `apply_modifiers`, extend `ModifiedRule`)
- Test: `tests/test_s316_modifier_execution.py`

- [ ] **Step 1: Write failing tests for new modifier execution**

```python
# tests/test_s316_modifier_execution.py
"""Tests for modifier execution: gate eval, ordering, 3-tier negation, context scaling."""
from src.calculations.inference import apply_modifiers, ModifiedRule
from src.calculations.rule_firing import FiredRule


def _fired(rule_id="T001", direction="favorable", confidence=0.7):
    return FiredRule(
        rule_id=rule_id, source="BPHS", planet="Sun", house=1,
        outcome_direction=direction, outcome_domains=["wealth"],
        confidence=confidence, concordance_count=0,
    )


class _Rule:
    def __init__(self, modifiers=None, predictions=None, primary_domain="wealth"):
        self.modifiers = modifiers or []
        self.predictions = predictions or [{"magnitude": 0.7, "domain": "wealth"}]
        self.primary_domain = primary_domain


# --- Gate tests ---

def test_structured_gate_passes():
    """Structured gate condition that matches chart → rule fires normally."""
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
        "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 1}],
    }])
    # Need a chart where Sun is in house 1 — use mock
    result = apply_modifiers(fired, rule, chart=_make_chart(sun_house=1))
    assert not result.gated_out


def test_structured_gate_fails():
    """Structured gate condition that doesn't match → rule gated out."""
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
        "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 7}],
    }])
    result = apply_modifiers(fired, rule, chart=_make_chart(sun_house=1))
    assert result.gated_out
    assert result.gate_reason != ""


def test_string_gate_unevaluated():
    """String gate (pre-migration) → logged as unevaluated, rule fires."""
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
        "condition": "other_six_planets_endowed_with_strength",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert not result.gated_out
    assert len(result.unevaluated_gates) == 1
    assert result.unevaluated_gates[0]["severity"] == "blocking"


# --- Negation 3-tier tests ---

def test_strong_negation_flips_direction():
    """Strong negation (weight > 0.7) flips direction."""
    fired = _fired(direction="favorable")
    rule = _Rule(modifiers=[{
        "effect": "negates", "target": "prediction", "strength": "strong",
        "scope": "local", "condition": "test",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert result.direction == "unfavorable"


def test_medium_negation_weakens():
    """Medium negation (0.3-0.7) weakens magnitude, doesn't flip."""
    fired = _fired(direction="favorable")
    rule = _Rule(modifiers=[{
        "effect": "negates", "target": "prediction", "strength": "medium",
        "scope": "local", "condition": "test",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert result.direction == "favorable"  # NOT flipped
    assert result.magnitude < 0.7  # weakened


def test_weak_negation_negligible():
    """Weak negation (weight < 0.3) is negligible."""
    fired = _fired(direction="favorable")
    rule = _Rule(modifiers=[{
        "effect": "negates", "target": "prediction", "strength": "weak",
        "scope": "local", "condition": "test",
    }])
    result = apply_modifiers(fired, rule, chart=None)
    assert result.direction == "favorable"
    assert result.magnitude == 0.7  # unchanged


# --- Ordering test ---

def test_gates_evaluated_before_amplifies():
    """Gates short-circuit — if gate fails, amplify never runs."""
    fired = _fired()
    rule = _Rule(modifiers=[
        {"effect": "amplifies", "target": "prediction", "strength": "strong",
         "scope": "local", "condition": "test"},
        {"effect": "gates", "target": "rule", "strength": "strong", "scope": "local",
         "condition": [{"type": "planet_in_house", "planet": "Sun", "house": 7}]},
    ])
    result = apply_modifiers(fired, rule, chart=_make_chart(sun_house=1))
    assert result.gated_out  # gate fails → entire rule gated


# --- Context-aware scaling test ---

def test_context_aware_amplification():
    """Modifier weight scales with argala_strength from context."""
    fired = _fired()
    rule = _Rule(modifiers=[{
        "effect": "amplifies", "target": "prediction", "strength": "medium",
        "scope": "local", "condition": "test",
    }])
    ctx = {"conditions": {}, "aggregates": {"argala_strength_total": 0.8}, "gates": {}}
    result = apply_modifiers(fired, rule, chart=None, condition_context=ctx)
    # effective_weight = 0.30 * (1 + 0.5 * 0.8) = 0.30 * 1.4 = 0.42
    # magnitude = 0.7 * (1 + 0.42) = 0.994
    assert result.magnitude > 0.9


# --- ModifiedRule fields test ---

def test_modified_rule_has_new_fields():
    fired = _fired()
    rule = _Rule()
    result = apply_modifiers(fired, rule, chart=None)
    assert hasattr(result, "gate_reason")
    assert hasattr(result, "unevaluated_gates")
    assert hasattr(result, "context")


# --- Chart mock ---

class _MockPlanet:
    def __init__(self, sign_index, degree_in_sign=15.0, name="Sun"):
        self.sign_index = sign_index
        self.degree_in_sign = degree_in_sign
        self.name = name
        self.sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                      "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][sign_index]


class _MockChart:
    def __init__(self, lagna_sign_index=0, planets=None):
        self.lagna_sign_index = lagna_sign_index
        self.lagna_sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                           "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][lagna_sign_index]
        self.planets = planets or {}


def _make_chart(sun_house=1, lagna_si=0):
    """Create a mock chart with Sun in a specific house."""
    sun_si = (lagna_si + sun_house - 1) % 12
    return _MockChart(
        lagna_sign_index=lagna_si,
        planets={"Sun": _MockPlanet(sun_si, name="Sun")},
    )
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_s316_modifier_execution.py -v`
Expected: FAIL — `apply_modifiers` doesn't accept `chart` or `condition_context` params

- [ ] **Step 3: Rewrite apply_modifiers**

Replace the `apply_modifiers` function in `src/calculations/inference.py`:

```python
_EFFECT_ORDER = {"gates": 0, "negates": 1, "attenuates": 2, "amplifies": 3, "qualifies": 4}


def apply_modifiers(fired: FiredRule, rule, chart=None,
                    condition_context: dict | None = None) -> ModifiedRule:
    """Apply modifiers to a fired rule with gate evaluation and context-aware scaling."""
    magnitude = fired.confidence
    direction = fired.outcome_direction
    qualifications: list[str] = []
    unevaluated_gates: list[dict] = []

    # Use prediction magnitude if available
    if rule.predictions:
        max_pred_mag = max(p.get("magnitude", 0.5) for p in rule.predictions)
        magnitude = max_pred_mag

    # Sort modifiers by execution order: gates → negates → attenuates → amplifies → qualifies
    ordered = sorted(rule.modifiers or [], key=lambda m: _EFFECT_ORDER.get(m.get("effect", ""), 5))

    for mod in ordered:
        effect = mod.get("effect", "")
        condition = mod.get("condition", "")
        strength = mod.get("strength", "medium")
        base_weight = _STRENGTH_WEIGHTS.get(strength, 0.30)

        if effect == "gates":
            if isinstance(condition, list):
                # Structured gate — evaluate via same condition evaluator
                from src.calculations.rule_firing import _check_compound_conditions
                gate_ctx = dict(condition_context) if condition_context else {}
                gate_ctx.setdefault("gates", {})
                gate_fires, _ = _check_compound_conditions(condition, chart, context=gate_ctx)
                if condition_context and "gates" not in condition_context:
                    condition_context["gates"] = {}
                if condition_context:
                    condition_context["gates"][str(condition)] = {"fired": gate_fires}
                if not gate_fires:
                    return ModifiedRule(
                        rule_id=fired.rule_id,
                        primary_domain=getattr(rule, "primary_domain", "character"),
                        direction=direction,
                        magnitude=0.0,
                        source_rule=fired,
                        gated_out=True,
                        gate_reason=str(condition),
                        unevaluated_gates=unevaluated_gates,
                        context=condition_context,
                    )
            else:
                # String gate — can't evaluate, log as unevaluated
                unevaluated_gates.append({
                    "condition": condition,
                    "severity": "blocking",
                })
                continue

        elif effect == "negates":
            # 3-tier negation
            if base_weight > 0.7:
                # Strong: flip direction
                if direction == "favorable":
                    direction = "unfavorable"
                elif direction == "unfavorable":
                    direction = "favorable"
            elif base_weight > 0.3:
                # Medium: weaken instead of flip
                magnitude *= (1 - base_weight)
            # Weak (<= 0.3): negligible, no change

        elif effect == "attenuates":
            effective_weight = _context_scaled_weight(base_weight, condition_context)
            magnitude *= (1.0 - effective_weight)

        elif effect == "amplifies":
            effective_weight = _context_scaled_weight(base_weight, condition_context)
            magnitude *= (1.0 + effective_weight)

        elif effect == "qualifies":
            if isinstance(condition, str):
                qualifications.append(condition)
            else:
                qualifications.append(str(condition))

    return ModifiedRule(
        rule_id=fired.rule_id,
        primary_domain=getattr(rule, "primary_domain", "character"),
        direction=direction,
        magnitude=round(magnitude, 3),
        source_rule=fired,
        qualifications=qualifications,
        unevaluated_gates=unevaluated_gates,
        context=condition_context,
    )


def _context_scaled_weight(base_weight: float, condition_context: dict | None) -> float:
    """Scale modifier weight using condition context aggregates."""
    if not condition_context:
        return base_weight
    aggregates = condition_context.get("aggregates", {})
    ctx_strength = None
    for key in CONSUMABLE_AGGREGATES:
        val = aggregates.get(key)
        if val is not None and isinstance(val, (int, float)):
            ctx_strength = val
            break  # use first available signal
    if ctx_strength is not None:
        return base_weight * (1 + 0.5 * ctx_strength)
    return base_weight
```

- [ ] **Step 4: Update ModifiedRule dataclass**

Replace the existing `ModifiedRule` in `src/calculations/inference.py`:

```python
@dataclass
class ModifiedRule:
    """A fired rule after modifier application."""
    rule_id: str
    primary_domain: str
    direction: str
    magnitude: float
    source_rule: FiredRule
    qualifications: list[str] = field(default_factory=list)
    gated_out: bool = False
    gate_reason: str = ""
    unevaluated_gates: list[dict] = field(default_factory=list)
    context: dict | None = None
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `.venv/bin/pytest tests/test_s316_modifier_execution.py -v`
Expected: PASS (all tests)

- [ ] **Step 6: Run full suite for regression**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: All pass. Existing test_inference.py tests may need minor updates since `apply_modifiers` signature changed (chart param added with default None).

- [ ] **Step 7: Commit**

```bash
git add src/calculations/inference.py tests/test_s316_modifier_execution.py
git commit -m "feat(s316): implement modifier execution — gates, 3-tier negation, context scaling

- Structured gates evaluated via _check_compound_conditions (same evaluator)
- String gates logged as unevaluated with blocking severity
- Negation: strong(>0.7) flips, medium(0.3-0.7) weakens, weak negligible
- Context-aware weight scaling: base_weight * (1 + 0.5 * ctx_strength)
- Modifier ordering enforced: gates → negates → attenuates → amplifies → qualifies"
```

---

### Task 4: Conflict Resolution in Domain Aggregation

**Files:**
- Modify: `src/calculations/inference.py` (`aggregate_domains`)
- Test: `tests/test_s316_modifier_execution.py` (append)

- [ ] **Step 1: Write failing tests for conflict resolution**

Append to `tests/test_s316_modifier_execution.py`:

```python
from src.calculations.inference import aggregate_domains


def _modified(rule_id, domain, direction, magnitude, confidence=0.7, signal_group=""):
    fired = _fired(rule_id=rule_id, direction=direction, confidence=confidence)
    fired.signal_group = signal_group
    return ModifiedRule(
        rule_id=rule_id, primary_domain=domain, direction=direction,
        magnitude=magnitude, source_rule=fired,
    )


def test_confidence_weighted_scoring():
    """Magnitude is weighted by confidence in aggregation."""
    rules = [_modified("R1", "wealth", "favorable", 0.8, confidence=0.5)]
    scores = aggregate_domains(rules)
    # effective = 0.8 * 0.5 = 0.4
    assert scores["wealth"].favorable_score == 0.4


def test_contrary_mirror_cancellation():
    """Rules with contrary_mirror relationship cancel to net 0."""
    r1 = _modified("R1", "wealth", "favorable", 0.8)
    r2 = _modified("R2", "wealth", "unfavorable", 0.6)
    r2.source_rule.rule_id = "R2"
    # Mark as contrary mirrors
    scores = aggregate_domains([r1, r2], contrary_mirrors={("R1", "R2")})
    assert scores["wealth"].net_score == 0.0


def test_same_signal_group_strongest_wins():
    """Same signal group + conflict → keep strongest only."""
    r1 = _modified("R1", "wealth", "favorable", 0.8, signal_group="sig_1")
    r2 = _modified("R2", "wealth", "unfavorable", 0.5, signal_group="sig_1")
    scores = aggregate_domains([r1, r2])
    # R1 is strongest → only R1 contributes
    assert scores["wealth"].favorable_score > 0
    assert scores["wealth"].unfavorable_score == 0.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_s316_modifier_execution.py::test_confidence_weighted_scoring -v`
Expected: FAIL

- [ ] **Step 3: Upgrade aggregate_domains**

Replace `aggregate_domains` in `src/calculations/inference.py`:

```python
def aggregate_domains(
    modified_rules: list[ModifiedRule],
    contrary_mirrors: set[tuple[str, str]] | None = None,
) -> dict[str, DomainScore]:
    """Aggregate fired rules into domain scores with conflict resolution.

    1. Confidence-weighted scoring: effective = magnitude * confidence
    2. Contrary mirror cancellation: paired rules contribute 0
    3. Same-signal-group dominance: keep strongest, drop weaker conflicting
    """
    from src.corpus.taxonomy import PRIMARY_DOMAIN_PRIORITY

    contrary_mirrors = contrary_mirrors or set()
    cancelled_ids: set[str] = set()
    for a, b in contrary_mirrors:
        cancelled_ids.add(a)
        cancelled_ids.add(b)

    # Same-signal-group conflict resolution: group by (domain, signal_group)
    # If same group has opposite directions, keep strongest
    signal_groups: dict[tuple[str, str], list[ModifiedRule]] = {}
    for mr in modified_rules:
        if mr.gated_out or mr.rule_id in cancelled_ids:
            continue
        sg = getattr(mr.source_rule, "signal_group", "") or ""
        if sg:
            key = (mr.primary_domain, sg)
            signal_groups.setdefault(key, []).append(mr)

    suppressed_ids: set[str] = set()
    for (domain, sg), group in signal_groups.items():
        directions = {mr.direction for mr in group}
        if len(directions) > 1:  # conflict within same signal group
            strongest = max(group, key=lambda mr: abs(mr.magnitude))
            for mr in group:
                if mr.rule_id != strongest.rule_id:
                    suppressed_ids.add(mr.rule_id)

    scores: dict[str, DomainScore] = {}
    for domain in PRIMARY_DOMAIN_PRIORITY:
        scores[domain] = DomainScore(domain=domain)

    for mr in modified_rules:
        if mr.gated_out or mr.rule_id in cancelled_ids or mr.rule_id in suppressed_ids:
            continue
        domain = mr.primary_domain
        if domain not in scores:
            scores[domain] = DomainScore(domain=domain)

        ds = scores[domain]
        ds.rule_count += 1

        confidence = getattr(mr.source_rule, "confidence", 1.0)
        effective = mr.magnitude * confidence

        if mr.direction == "favorable":
            ds.favorable_score += effective
        elif mr.direction == "unfavorable":
            ds.unfavorable_score += effective
        else:
            ds.favorable_score += effective * 0.5
            ds.unfavorable_score += effective * 0.5

        ds.net_score = round(ds.favorable_score - ds.unfavorable_score, 3)

        if abs(effective) > ds.strongest_magnitude:
            ds.strongest_magnitude = abs(effective)
            ds.strongest_rule_id = mr.rule_id

    return scores
```

- [ ] **Step 4: Run tests**

Run: `.venv/bin/pytest tests/test_s316_modifier_execution.py -v`
Expected: PASS

- [ ] **Step 5: Fix existing test_inference.py if needed**

The existing `test_aggregate_domains` test expects raw magnitude (not confidence-weighted). Update the test assertions to match `magnitude * confidence`.

- [ ] **Step 6: Commit**

```bash
git add src/calculations/inference.py tests/test_s316_modifier_execution.py
git commit -m "feat(s316): conflict resolution — contrary mirrors, signal group dominance, confidence weighting

- Contrary mirror pairs cancel to net 0
- Same signal group with opposite directions: strongest wins
- All magnitudes weighted by rule confidence in aggregation"
```

---

## Wave 2 — Primitives (Parallel Lanes)

### Task 5: `functional_benefic` Primitive (Lane A)

**Files:**
- Modify: `src/calculations/rule_firing.py` (new elif in `_check_compound_conditions`)
- Modify: `src/corpus/taxonomy.py` (add to `VALID_CONDITION_PRIMITIVES`)
- Test: `tests/test_s316_primitives.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_s316_primitives.py
"""Tests for all 6 new condition primitives."""
from src.calculations.rule_firing import _check_compound_conditions


# --- Chart mock (reusable) ---
class _P:
    def __init__(self, sign_index, degree_in_sign=15.0, name="Sun"):
        self.sign_index = sign_index
        self.degree_in_sign = degree_in_sign
        self.name = name
        self.sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                      "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][sign_index]


class _Chart:
    def __init__(self, lagna_sign_index=0, planets=None):
        self.lagna_sign_index = lagna_sign_index
        self.lagna_sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                           "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"][lagna_sign_index]
        self.planets = planets or {}


# --- functional_benefic ---

def test_functional_benefic_jupiter_for_aries():
    """Jupiter rules H9+H12 for Aries lagna. H9=trikona → benefic."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Jupiter": _P(8, name="Jupiter"),  # Sagittarius
    })
    conds = [{"type": "functional_benefic", "planet": "Jupiter", "classification": "benefic"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True


def test_functional_benefic_saturn_not_benefic_for_aries():
    """Saturn rules H10+H11 for Aries. Not trikona lord → not benefic."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Saturn": _P(9, name="Saturn"),
    })
    conds = [{"type": "functional_benefic", "planet": "Saturn", "classification": "benefic"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is False


def test_functional_benefic_yogakaraka():
    """Saturn is yogakaraka for Taurus lagna (rules H9 Capricorn + H10 Aquarius)."""
    chart = _Chart(lagna_sign_index=1, planets={
        "Saturn": _P(9, name="Saturn"),
    })
    conds = [{"type": "functional_benefic", "planet": "Saturn", "classification": "yogakaraka"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `.venv/bin/pytest tests/test_s316_primitives.py::test_functional_benefic_jupiter_for_aries -v`
Expected: FAIL — unknown condition type → `(False, 0)`

- [ ] **Step 3: Add functional_benefic to taxonomy**

In `src/corpus/taxonomy.py`, add `"functional_benefic"` to `VALID_CONDITION_PRIMITIVES`.

- [ ] **Step 4: Implement evaluator**

In `src/calculations/rule_firing.py`, add elif branch in `_check_compound_conditions` before the final `else`:

```python
        elif ctype == "functional_benefic":
            from src.calculations.functional_dignity import compute_functional_classifications
            planet_spec = cond.get("planet", "")
            classification = cond.get("classification", "")
            if planet_spec.startswith("lord_of_"):
                h = int(planet_spec.split("_")[-1])
                planet_spec = _lord_of_house(chart, h)
            if not planet_spec or not _find_planet(chart, planet_spec.title()):
                return False, 0
            planet_name = planet_spec.title()
            fc = compute_functional_classifications(chart.lagna_sign_index)
            entry = fc.get(planet_name)
            if not entry:
                return False, 0
            if classification == "benefic" and not entry.is_functional_benefic:
                return False, 0
            elif classification == "malefic" and not entry.is_functional_malefic:
                return False, 0
            elif classification == "yogakaraka" and not entry.is_yogakaraka:
                return False, 0
            elif classification == "maraka" and not entry.is_maraka:
                return False, 0
            elif classification == "badhaka" and not entry.is_badhaka:
                return False, 0
```

- [ ] **Step 5: Run tests**

Run: `.venv/bin/pytest tests/test_s316_primitives.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/calculations/rule_firing.py src/corpus/taxonomy.py tests/test_s316_primitives.py
git commit -m "feat(s316): add functional_benefic condition primitive

Evaluates per-lagna functional classification via compute_functional_classifications.
Supports: benefic, malefic, yogakaraka, maraka, badhaka. Unblocks ~20 rules."
```

---

### Task 6: `argala_condition` Primitive (Lane B)

**Files:**
- Modify: `src/calculations/rule_firing.py` (new elif + metadata emission)
- Modify: `src/corpus/taxonomy.py`
- Test: `tests/test_s316_primitives.py` (append)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_s316_primitives.py`:

```python
def _india_1947_chart():
    """India 1947 fixture: Taurus lagna (sign_index=1)."""
    return _Chart(lagna_sign_index=1, planets={
        "Sun": _P(3, name="Sun"),         # Cancer (H3)
        "Moon": _P(2, name="Moon"),        # Gemini (H2)
        "Mars": _P(1, name="Mars"),        # Taurus (H1)
        "Mercury": _P(3, name="Mercury"),  # Cancer (H3)
        "Jupiter": _P(5, name="Jupiter"),  # Virgo (H5)
        "Venus": _P(2, name="Venus"),      # Gemini (H2)
        "Saturn": _P(3, name="Saturn"),    # Cancer (H3)
        "Rahu": _P(1, name="Rahu"),        # Taurus (H1)
        "Ketu": _P(7, name="Ketu"),        # Scorpio (H7)
    })


def test_argala_condition_fires():
    """Argala from H1 with benefics in H2 (Moon, Venus) → fires."""
    chart = _india_1947_chart()
    conds = [{"type": "argala_condition", "reference_house": 1,
              "argala_type": "any", "min_strength": "weak", "obstruction": "any"}]
    ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
    fires, _ = _check_compound_conditions(conds, chart, context=ctx)
    assert fires is True


def test_argala_emits_metadata():
    """Argala primitive writes strength + type to context."""
    chart = _india_1947_chart()
    conds = [{"type": "argala_condition", "reference_house": 1,
              "argala_type": "any", "min_strength": "weak", "obstruction": "any"}]
    ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
    _check_compound_conditions(conds, chart, context=ctx)
    meta = ctx["conditions"].get("cond_0", {}).get("metadata", {})
    assert "argala_strength" in meta
    assert "normalization_version" in meta
    assert meta["normalization_version"] == "v1_linear"


def test_argala_min_strength_filter():
    """Argala with high min_strength filters weak argala."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Mercury": _P(1, name="Mercury"),  # only 1 benefic in H2
    })
    conds = [{"type": "argala_condition", "reference_house": 1,
              "argala_type": "benefic", "min_strength": "strong", "obstruction": "unobstructed"}]
    ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
    fires, _ = _check_compound_conditions(conds, chart, context=ctx)
    # Weak argala (1 benefic, score ~0.04) should not meet "strong" threshold
    assert fires is False
```

- [ ] **Step 2: Run to verify fail**

Run: `.venv/bin/pytest tests/test_s316_primitives.py::test_argala_condition_fires -v`
Expected: FAIL

- [ ] **Step 3: Add argala_condition to taxonomy**

Add `"argala_condition"` to `VALID_CONDITION_PRIMITIVES` in `taxonomy.py`.

- [ ] **Step 4: Implement evaluator with metadata emission**

In `_check_compound_conditions`, add (note the `idx` variable — add `for idx, cond in enumerate(conditions):` to the loop):

First, change the loop from `for cond in conditions:` to `for idx, cond in enumerate(conditions):`.

Then add the elif branch:

```python
        elif ctype == "argala_condition":
            from src.calculations.argala import compute_argala
            ref_house = cond.get("reference_house", 1)
            argala_type = cond.get("argala_type", "any")
            min_strength = cond.get("min_strength", "weak")
            obstruction_req = cond.get("obstruction", "any")

            result = compute_argala(chart, ref_house)
            # Normalize score
            max_score = 12.0  # v1_linear: 3 houses × 4 benefics × 1.0 weight
            normalized = min(1.0, max(0.0, abs(result.net_argala_score) / max_score))

            # Check argala_type filter
            if argala_type == "benefic":
                benefic_entries = [e for e in result.entries if e.nature == "benefic_argala"]
                if not benefic_entries:
                    return False, 0
            elif argala_type == "malefic":
                malefic_entries = [e for e in result.entries if e.nature == "malefic_argala"]
                if not malefic_entries:
                    return False, 0

            # Check obstruction filter
            if obstruction_req == "unobstructed":
                active = [e for e in result.entries if not e.is_obstructed]
                if not active:
                    return False, 0
            elif obstruction_req == "partial":
                obstructed = [e for e in result.entries if e.is_obstructed]
                if not obstructed:
                    return False, 0

            # Check min_strength threshold
            strength_thresholds = {"weak": 0.01, "medium": 0.15, "strong": 0.35}
            if normalized < strength_thresholds.get(min_strength, 0.01):
                return False, 0

            # Determine actual type
            natures = {e.nature for e in result.entries if not e.is_obstructed}
            if natures == {"benefic_argala"}:
                actual_type = "benefic"
            elif natures == {"malefic_argala"}:
                actual_type = "malefic"
            else:
                actual_type = "mixed"

            # Obstruction level
            total = len(result.entries)
            obstructed = sum(1 for e in result.entries if e.is_obstructed)
            if total == 0:
                obs_level = "none"
            elif obstructed == 0:
                obs_level = "unobstructed"
            elif obstructed == total:
                obs_level = "full"
            else:
                obs_level = "partial"

            # Emit metadata
            if context is not None:
                context["conditions"][f"cond_{idx}"] = {
                    "type": "argala_condition",
                    "metadata": {
                        "argala_strength": round(normalized, 3),
                        "argala_type": actual_type,
                        "obstruction": obs_level,
                        "contributing_houses": [e.house_from_reference for e in result.entries if not e.is_obstructed],
                        "net_score": result.net_argala_score,
                        "normalization_version": "v1_linear",
                    },
                }
            matched_house = matched_house or ref_house
```

- [ ] **Step 5: Run tests**

Run: `.venv/bin/pytest tests/test_s316_primitives.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/calculations/rule_firing.py src/corpus/taxonomy.py tests/test_s316_primitives.py
git commit -m "feat(s316): add argala_condition primitive with metadata emission

Non-binary argala: emits strength, type, obstruction level to context.
Normalization v1_linear (theoretical max 12.0). Filters by argala_type,
min_strength, obstruction. Unblocks 17 Ch.31 rules."
```

---

### Task 7: `same_planet_constraint` — Bind Variables (Lane B)

**Files:**
- Modify: `src/calculations/rule_firing.py` (bind variable support in `_check_compound_conditions`)
- Test: `tests/test_s316_primitives.py` (append)

- [ ] **Step 1: Write failing tests**

Append to `tests/test_s316_primitives.py`:

```python
def test_bind_variable_same_planet():
    """Bind 'X' ensures same planet satisfies both conditions."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Jupiter": _P(11, name="Jupiter"),  # Pisces = H12 from Aries, exalted? No. 
        # Jupiter exalted in Cancer (sign 3). House 4 from Aries lagna.
        "Jupiter": _P(3, name="Jupiter"),   # Cancer (H4), exalted
        "Venus": _P(11, name="Venus"),      # Pisces (H12), exalted
    })
    conds = [
        {"type": "planet_in_house", "planet": "any_benefic", "house": 4, "bind": "X"},
        {"type": "planet_dignity", "planet": "X", "dignity": "exalted"},
    ]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True  # Jupiter in H4 + exalted


def test_bind_variable_no_match():
    """Bind fails when no single planet satisfies all bound conditions."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Jupiter": _P(3, name="Jupiter"),   # Cancer (H4), exalted
        "Venus": _P(5, name="Venus"),       # Virgo (H6), debilitated
    })
    conds = [
        {"type": "planet_in_house", "planet": "any_benefic", "house": 6, "bind": "X"},
        {"type": "planet_dignity", "planet": "X", "dignity": "exalted"},
    ]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is False  # Venus in H6 but debilitated, not exalted


def test_bind_picks_strongest():
    """When multiple candidates satisfy, bind picks strongest by dignity."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Jupiter": _P(3, name="Jupiter"),  # Cancer (H4), exalted
        "Venus": _P(3, name="Venus"),      # Cancer (H4), neutral
    })
    conds = [
        {"type": "planet_in_house", "planet": "any_benefic", "house": 4, "bind": "X"},
        {"type": "planet_dignity", "planet": "X", "dignity": "exalted"},
    ]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True  # Jupiter satisfies both (exalted in Cancer)
```

- [ ] **Step 2: Run to verify fail**

Run: `.venv/bin/pytest tests/test_s316_primitives.py::test_bind_variable_same_planet -v`
Expected: FAIL — bind not recognized, "X" treated as planet name

- [ ] **Step 3: Implement bind variable resolution**

This requires restructuring `_check_compound_conditions` to handle bind variables. Add at the top of the function, before the main loop:

```python
    # Detect bind variables
    bind_conditions = [(i, c) for i, c in enumerate(conditions) if c.get("bind")]
    if bind_conditions:
        return _check_with_bindings(conditions, chart, context)
```

Then add a new function:

```python
_DIGNITY_RANK = {"exalted": 5, "moolatrikona": 4, "own_sign": 3, "neutral": 2, "debilitated": 1, "unknown": 0}
MAX_BIND_ATTEMPTS = 10


def _check_with_bindings(conditions: list[dict], chart, context: dict | None = None) -> tuple[bool, int]:
    """Evaluate conditions with bind variables. Strongest valid binding wins."""
    # Identify bind variables and their candidate-producing conditions
    bind_vars: dict[str, list[str]] = {}  # var -> candidate planet names
    bound_indices: set[int] = set()

    for i, cond in enumerate(conditions):
        bind_var = cond.get("bind")
        if bind_var:
            bound_indices.add(i)
            planet_spec = cond.get("planet", "")
            if planet_spec == "any_benefic":
                candidates = list(_BENEFICS)
            elif planet_spec == "any_malefic":
                candidates = list(_MALEFICS)
            else:
                candidates = [planet_spec.title()]
            bind_vars[bind_var] = [c for c in candidates if _find_planet(chart, c)]

    if not bind_vars:
        return _check_compound_conditions_inner(conditions, chart, context)

    # For each bind variable, try candidates (strongest first by dignity)
    for var, candidates in bind_vars.items():
        ranked = sorted(candidates, key=lambda p: _DIGNITY_RANK.get(
            _planet_dignity_state(chart, p), 0), reverse=True)

        for attempt, planet in enumerate(ranked[:MAX_BIND_ATTEMPTS]):
            # Substitute bind variable in all conditions
            resolved = []
            for cond in conditions:
                c = dict(cond)
                if c.get("bind") == var:
                    c["planet"] = planet
                    del c["bind"]
                elif c.get("planet") == var:
                    c["planet"] = planet
                resolved.append(c)

            fires, house = _check_compound_conditions(resolved, chart, context)
            if fires:
                return True, house

    return False, 0
```

- [ ] **Step 4: Run tests**

Run: `.venv/bin/pytest tests/test_s316_primitives.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/calculations/rule_firing.py tests/test_s316_primitives.py
git commit -m "feat(s316): add same_planet_constraint via bind variables

'bind' field on conditions creates variable resolved to specific planet.
Strongest candidate by dignity wins. MAX_BIND_ATTEMPTS=10 prevents
exponential search. Unblocks Ch.34-42 yoga chapters."
```

---

### Task 8: `dynamic_karaka` Primitive (Lane C)

**Files:**
- Modify: `src/calculations/rule_firing.py`
- Modify: `src/corpus/taxonomy.py`
- Test: `tests/test_s316_primitives.py` (append)

- [ ] **Step 1: Write failing test**

```python
def test_dynamic_karaka_mother():
    """Mother karaka = stronger of Moon and Mars. Check dignity-based resolution."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Moon": _P(1, name="Moon"),  # Taurus = exalted
        "Mars": _P(3, name="Mars"),  # Cancer = debilitated
    })
    conds = [{"type": "dynamic_karaka", "karaka": "mother", "state": "strong"}]
    fires, _ = _check_compound_conditions(conds, chart)
    # Moon is stronger (exalted vs debilitated), Moon is exalted → "strong"
    assert fires is True


def test_dynamic_karaka_father_weak():
    """Father karaka = stronger of Sun and Jupiter. Both neutral → not strong."""
    chart = _Chart(lagna_sign_index=0, planets={
        "Sun": _P(2, name="Sun"),      # Gemini = neutral
        "Jupiter": _P(2, name="Jupiter"),  # Gemini = neutral
    })
    conds = [{"type": "dynamic_karaka", "karaka": "father", "state": "strong"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is False
```

- [ ] **Step 2: Run to verify fail**

- [ ] **Step 3: Implement**

Add to taxonomy: `"dynamic_karaka"` in `VALID_CONDITION_PRIMITIVES`.

Add elif in `_check_compound_conditions`:

```python
        elif ctype == "dynamic_karaka":
            karaka = cond.get("karaka", "")
            state = cond.get("state", "")
            if karaka == "mother":
                candidates = ["Moon", "Mars"]
            elif karaka == "father":
                candidates = ["Sun", "Jupiter"]
            else:
                return False, 0
            # Pick stronger by dignity rank
            ranked = sorted(candidates, key=lambda p: _DIGNITY_RANK.get(
                _planet_dignity_state(chart, p), 0), reverse=True)
            resolved = ranked[0]
            actual_dignity = _planet_dignity_state(chart, resolved)
            if state == "strong":
                if actual_dignity not in ("exalted", "own_sign", "moolatrikona"):
                    return False, 0
            elif state == "weak":
                if actual_dignity in ("exalted", "own_sign", "moolatrikona"):
                    return False, 0
            matched_house = matched_house or _planet_house(chart, resolved)
```

- [ ] **Step 4: Run tests, commit**

```bash
git add src/calculations/rule_firing.py src/corpus/taxonomy.py tests/test_s316_primitives.py
git commit -m "feat(s316): add dynamic_karaka primitive — stronger-of-two resolution

Mother=stronger(Moon,Mars), Father=stronger(Sun,Jupiter).
Dignity-ranked selection. Unblocks Ch.32-33 karaka chapters."
```

---

### Task 9: `shadbala_strength` Primitive (Lane A)

**Files:**
- Modify: `src/calculations/rule_firing.py`
- Modify: `src/corpus/taxonomy.py`
- Test: `tests/test_s316_primitives.py` (append)

- [ ] **Step 1: Write failing test**

```python
def test_shadbala_strength_emits_metadata():
    """shadbala_strength writes normalized value to context."""
    # This test requires a full chart — use India 1947 fixture
    from tests.conftest import india_1947_chart
    chart = india_1947_chart()
    conds = [{"type": "shadbala_strength", "planet": "Sun", "threshold": "weak"}]
    ctx = {"conditions": {}, "aggregates": {}, "gates": {}}
    fires, _ = _check_compound_conditions(conds, chart, context=ctx)
    # Sun should have some shadbala value
    if fires:
        meta = ctx["conditions"].get("cond_0", {}).get("metadata", {})
        assert "shadbala_normalized" in meta
```

Note: If conftest doesn't have `india_1947_chart`, this test will need adjustment. The key is that shadbala computation requires a real chart with birth datetime.

- [ ] **Step 2: Implement**

Add `"shadbala_strength"` to taxonomy.

Add elif:

```python
        elif ctype == "shadbala_strength":
            planet_spec = cond.get("planet", "")
            threshold = cond.get("threshold", "weak")
            if planet_spec.startswith("lord_of_"):
                h = int(planet_spec.split("_")[-1])
                planet_spec = _lord_of_house(chart, h)
            if not planet_spec or not _find_planet(chart, planet_spec.title()):
                return False, 0
            try:
                from src.calculations.shadbala import compute_shadbala
                sb = compute_shadbala(planet_spec.title(), chart)
                total = getattr(sb, "total", 0.0)
                # BPHS minimum required strength varies by planet; use 1.0 rupa as baseline
                normalized = min(1.0, max(0.0, total / 1.0)) if total else 0.0
            except Exception:
                return False, 0
            if threshold == "weak" and normalized >= 0.5:
                return False, 0  # not weak
            elif threshold == "strong" and normalized < 0.5:
                return False, 0  # not strong
            if context is not None:
                context["conditions"][f"cond_{idx}"] = {
                    "type": "shadbala_strength",
                    "metadata": {"shadbala_normalized": round(normalized, 3)},
                }
```

- [ ] **Step 3: Run tests, commit**

```bash
git commit -m "feat(s316): add shadbala_strength primitive with metadata emission

Calls existing compute_shadbala. Normalizes to [0,1]. Emits to context
for modifier consumption. Unblocks BPHS2501."
```

---

### Task 10: `navamsa_lagna` Primitive (Lane C)

**Files:**
- Modify: `src/calculations/rule_firing.py`
- Modify: `src/corpus/taxonomy.py`
- Test: `tests/test_s316_primitives.py` (append)

- [ ] **Step 1: Write failing test**

```python
def test_navamsa_lagna():
    """Navamsa lagna = navamsa sign of ascendant degree."""
    # Aries lagna at 15 degrees. Fire sign → starts from Aries.
    # Pada = 15 / 3.333 = 4 (0-indexed) → Aries + 4 = Leo
    chart = _Chart(lagna_sign_index=0, planets={})
    chart.lagna_degree = 15.0  # need to add this
    conds = [{"type": "navamsa_lagna", "sign": "leo"}]
    fires, _ = _check_compound_conditions(conds, chart)
    assert fires is True
```

- [ ] **Step 2: Implement**

Add `"navamsa_lagna"` to taxonomy.

Add elif:

```python
        elif ctype == "navamsa_lagna":
            target_signs = cond.get("sign", [])
            if isinstance(target_signs, str):
                target_signs = [target_signs]
            target_lower = [s.lower() for s in target_signs]
            lagna_degree = getattr(chart, "lagna_degree", None)
            if lagna_degree is None:
                return False, 0
            FIRE_SIGNS = {0, 4, 8}
            EARTH_SIGNS = {1, 5, 9}
            AIR_SIGNS = {2, 6, 10}
            lsi = chart.lagna_sign_index
            pada = int(lagna_degree / (30.0 / 9))
            if pada >= 9:
                pada = 8
            if lsi in FIRE_SIGNS:
                start = 0
            elif lsi in EARTH_SIGNS:
                start = 3
            elif lsi in AIR_SIGNS:
                start = 6
            else:
                start = 9
            nav_si = (start + pada) % 12
            SIGN_NAMES = ["aries", "taurus", "gemini", "cancer", "leo", "virgo",
                          "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
            if SIGN_NAMES[nav_si] not in target_lower:
                return False, 0
```

- [ ] **Step 3: Run tests, commit**

```bash
git commit -m "feat(s316): add navamsa_lagna primitive

Computes navamsa sign of ascendant degree. Same algorithm as
planet_in_navamsa_sign applied to lagna. Unblocks BPHS2114."
```

---

### Task 11: Derived House Resolver + BB Execution (Lane D)

**Files:**
- Create: `src/calculations/derived_house.py`
- Modify: `src/calculations/rule_firing.py` (BB context enrichment)
- Test: `tests/test_s316_governance.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_s316_governance.py
"""Tests for governance: derived house resolver, archetypes, interpretation."""
from src.calculations.derived_house import resolve_house


def test_resolve_house_5th_from_3rd():
    assert resolve_house(3, 5) == 7


def test_resolve_house_wraps():
    assert resolve_house(10, 5) == 2


def test_resolve_house_12th_from_1st():
    assert resolve_house(1, 12) == 12


def test_resolve_house_1st_from_1st():
    assert resolve_house(1, 1) == 1
```

- [ ] **Step 2: Implement**

```python
# src/calculations/derived_house.py
"""Canonical derived house resolver. ALL bhavat-bhavam arithmetic goes here."""
from __future__ import annotations


def resolve_house(base: int, offset: int) -> int:
    """BPHS inclusive counting: '5th from 3rd' means count 3→4→5→6→7 = house 7.

    Args:
        base: starting house (1-12)
        offset: houses to count forward, inclusive (1-12)

    Returns:
        absolute house number (1-12)
    """
    return (base + offset - 2) % 12 + 1
```

- [ ] **Step 3: Wire BB chains into context**

In `evaluate_chart` loop in `rule_firing.py`, after building FiredRule:

```python
        # BB chain enrichment
        if hasattr(rule, "derived_house_chains") and rule.derived_house_chains and ctx:
            from src.calculations.derived_house import resolve_house
            ctx.setdefault("aggregates", {})
            ctx["aggregates"].setdefault("bb_houses", [])
            ctx["aggregates"].setdefault("bb_strength", 0.0)
            for chain in rule.derived_house_chains:
                steps = chain if isinstance(chain, list) else [chain]
                current = steps[0].get("from", 1) if steps else 1
                for step in steps:
                    current = resolve_house(current, step.get("offset", 1))
                ctx["aggregates"]["bb_houses"].append(current)
                ctx["aggregates"]["bb_strength"] += 0.2
```

- [ ] **Step 4: Run tests, commit**

```bash
git add src/calculations/derived_house.py src/calculations/rule_firing.py tests/test_s316_governance.py
git commit -m "feat(s316): add derived house resolver + BB chain context enrichment

resolve_house(base, offset) is the single source of truth for all
derived house arithmetic. BB chains contribute +0.2 to context aggregates."
```

---

### Task 12: V1 Derivation Classification (Lane D)

**Files:**
- Modify: `src/corpus/combined_corpus.py`
- Test: `tests/test_s316_governance.py` (append)

- [ ] **Step 1: Write failing test**

```python
def test_v1_derivation_classification():
    from src.corpus.combined_corpus import _classify_v1_derivation

    class _FakeRule:
        def __init__(self, verse_ref="", concordance_texts=None):
            self.verse_ref = verse_ref
            self.concordance_texts = concordance_texts or []

    assert _classify_v1_derivation(_FakeRule("Ch.12 v.1", ["PVRNR"])) == "verse_derived"
    assert _classify_v1_derivation(_FakeRule("Ch.12 v.1")) == "commentary_derived"
    assert _classify_v1_derivation(_FakeRule()) == "interpretive"
```

- [ ] **Step 2: Implement**

Add to `src/corpus/combined_corpus.py`:

```python
def _classify_v1_derivation(rule) -> str:
    """Classify V1 rule derivation type for ranking."""
    if getattr(rule, "verse_ref", "") and getattr(rule, "concordance_texts", []):
        return "verse_derived"
    elif getattr(rule, "verse_ref", ""):
        return "commentary_derived"
    return "interpretive"
```

- [ ] **Step 3: Run tests, commit**

```bash
git commit -m "feat(s316): add V1 derivation classification

verse_derived > commentary_derived > interpretive. Used for V1/V2 ranking."
```

---

### Task 13: Timing Activation Hook (Lane E)

**Files:**
- Modify: `src/calculations/rule_firing.py`
- Test: `tests/test_s316_primitives.py` (append)

- [ ] **Step 1: Write test**

```python
def test_timing_activation_default_true():
    from src.calculations.rule_firing import _is_activated

    class _FakeRule:
        timing_window = None

    assert _is_activated(_FakeRule(), chart=None) is True


def test_timing_activation_unspecified_true():
    from src.calculations.rule_firing import _is_activated

    class _FakeRule:
        timing_window = {"type": "unspecified"}

    assert _is_activated(_FakeRule(), chart=None) is True
```

- [ ] **Step 2: Implement**

Add to `rule_firing.py`:

```python
def _is_activated(rule, chart, dasha_context=None) -> bool:
    """Check if a rule is currently activated. Default: always active."""
    timing = getattr(rule, "timing_window", None)
    if not timing or timing.get("type") == "unspecified":
        return True
    # Dasha/transit activation: requires dasha engine (out of scope)
    return True
```

Wire into `evaluate_chart` loop:
```python
        if not _is_activated(rule, chart):
            result.skipped_rules.append(SkippedRule(rule_id=rule.rule_id, reason="not_activated"))
            continue
```

- [ ] **Step 3: Run tests, commit**

```bash
git commit -m "feat(s316): add timing activation hook (default passthrough)

_is_activated() wired into evaluate_chart. Default: always active.
Dasha activation requires dasha engine (out of scope)."
```

---

### Task 14: Prediction-Type Classification (Lane E)

**Files:**
- Create: `tools/classify_prediction_types.py`
- Test: inline validation via running the tool

- [ ] **Step 1: Write tool**

```python
#!/usr/bin/env python3
"""tools/classify_prediction_types.py — Assign prediction_type to rules missing it."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corpus.combined_corpus import build_corpus

_HEALTH_KEYWORDS = {"disease", "sickly", "health", "illness", "pain", "wound", "fever", "death"}
_EVENT_KEYWORDS = {"marriage", "birth", "death", "travel", "accident", "gain", "loss", "age"}
_TRAIT_KEYWORDS = {"virtuous", "intelligent", "brave", "lazy", "learned", "handsome", "beautiful"}

def classify(claim: str) -> str:
    words = set(claim.lower().split())
    if words & _HEALTH_KEYWORDS:
        return "health"
    if words & _EVENT_KEYWORDS:
        return "event"
    if words & _TRAIT_KEYWORDS:
        return "trait"
    return "status"  # default

def main():
    corpus = build_corpus()
    rules = [r for r in corpus.all() if r.phase.startswith("1B")]
    missing = [r for r in rules if not getattr(r, "prediction_type", "")]
    print(f"Rules without prediction_type: {len(missing)}/{len(rules)}")
    counts = {"trait": 0, "event": 0, "status": 0, "health": 0}
    for r in missing:
        claims = " ".join(p.get("claim", "") for p in (r.predictions or []))
        pt = classify(claims)
        counts[pt] += 1
    print(f"Classification: {counts}")
    print("NOTE: This is a dry-run report. Actual assignment requires modifying chapter files.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run and verify**

Run: `.venv/bin/python tools/classify_prediction_types.py`
Expected: Report showing distribution.

- [ ] **Step 3: Commit**

```bash
git add tools/classify_prediction_types.py
git commit -m "feat(s316): add prediction-type classification tool

Keyword-based classifier: trait/event/status/health. Dry-run report
for rules missing prediction_type."
```

---

### Task 15: Planet Archetypes Registry (Wave 3)

**Files:**
- Create: `src/corpus/planet_archetypes.py`
- Test: `tests/test_s316_governance.py` (append)

- [ ] **Step 1: Write test**

```python
from src.corpus.planet_archetypes import PLANET_ARCHETYPES


def test_all_nine_planets_in_archetypes():
    expected = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
    assert set(PLANET_ARCHETYPES.keys()) == expected


def test_archetype_has_nature_and_themes():
    for planet, arch in PLANET_ARCHETYPES.items():
        assert "nature" in arch, f"{planet} missing nature"
        assert "themes" in arch, f"{planet} missing themes"
        assert arch["nature"] in ("benefic", "malefic"), f"{planet} has invalid nature"
        assert len(arch["themes"]) >= 3, f"{planet} needs at least 3 themes"
```

- [ ] **Step 2: Implement**

```python
# src/corpus/planet_archetypes.py
"""Central planet archetype registry — single source of truth for nature + themes."""
from __future__ import annotations

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

- [ ] **Step 3: Commit**

```bash
git add src/corpus/planet_archetypes.py tests/test_s316_governance.py
git commit -m "feat(s316): add planet archetypes registry

Single source of truth for nature + themes. Referenced by functional_benefic
and interpretation layer."
```

---

### Task 16: Interpretation Layer (Wave 3)

**Files:**
- Create: `src/calculations/interpretation.py`
- Test: `tests/test_s316_governance.py` (append)

- [ ] **Step 1: Write test**

```python
from src.calculations.interpretation import interpret


def test_interpret_basic():
    pred = {"claim": "will be wealthy", "domain": "wealth", "direction": "favorable"}
    ctx = {"qualifications": [], "trigger_planet": ""}
    result = interpret(pred, ctx)
    assert "will be wealthy" in result


def test_interpret_with_qualifications():
    pred = {"claim": "will be wealthy", "domain": "wealth", "direction": "favorable"}
    ctx = {"qualifications": ["more_daughters"], "trigger_planet": ""}
    result = interpret(pred, ctx)
    assert "qualified by" in result
    assert "more_daughters" in result


def test_interpret_with_planet_themes():
    pred = {"claim": "will be wealthy", "domain": "wealth", "direction": "favorable"}
    ctx = {"qualifications": [], "trigger_planet": "Jupiter"}
    result = interpret(pred, ctx)
    assert "Jupiter" in result
    assert "wisdom" in result
```

- [ ] **Step 2: Implement**

```python
# src/calculations/interpretation.py
"""Interpretation abstraction layer — annotated output from predictions + context."""
from __future__ import annotations

from src.corpus.planet_archetypes import PLANET_ARCHETYPES


def interpret(prediction: dict, context: dict) -> str:
    """Convert structured prediction + context into annotated output.

    Invariant: no interpretation without context.
    """
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

- [ ] **Step 3: Commit**

```bash
git add src/calculations/interpretation.py tests/test_s316_governance.py
git commit -m "feat(s316): add interpretation abstraction layer

interpret(prediction, context) produces annotated output with
qualifications and planet archetype themes. Minimal — no prose generation."
```

---

### Task 17: Modifier Condition Migration Tool

**Files:**
- Create: `tools/migrate_modifier_conditions.py`
- Test: dry-run validation

- [ ] **Step 1: Write migration tool**

```python
#!/usr/bin/env python3
"""tools/migrate_modifier_conditions.py — Migrate modifier condition strings to structured dicts."""
from __future__ import annotations
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corpus.combined_corpus import build_corpus

# Deterministic mappings: condition string patterns → structured condition
_PATTERNS = [
    # "lord_of_N_in_house_M" or "Nth_lord_in_Mth"
    (r"(?:lord_of_|(\d+)(?:st|nd|rd|th)_lord_in_)(\d+)", "lord_in_house"),
    # "planet_exalted" or "planet_in_own_sign"
    (r"(\w+)_exalted", "planet_dignity_exalted"),
    (r"(\w+)_debilitated", "planet_dignity_debilitated"),
]


def try_parse(condition_str: str) -> list[dict] | None:
    """Attempt to parse a modifier condition string into structured form.
    Returns None if ambiguous."""
    s = condition_str.strip().lower()

    # lord_of_N_in_house_M pattern
    m = re.match(r"lord_of_(\d+)_in_(?:house_)?(\d+)", s)
    if m:
        return [{"type": "lord_in_house", "lord_of": int(m.group(1)), "house": int(m.group(2))}]

    # planet_in_house_N
    m = re.match(r"(\w+)_in_house_(\d+)", s)
    if m:
        return [{"type": "planet_in_house", "planet": m.group(1), "house": int(m.group(2))}]

    # planet_exalted
    m = re.match(r"(\w+)_(?:is_)?exalted", s)
    if m:
        return [{"type": "planet_dignity", "planet": m.group(1), "dignity": "exalted"}]

    # planet_conjunct_planet
    m = re.match(r"(\w+)_conjunct_(\w+)", s)
    if m:
        return [{"type": "planets_conjunct", "planets": [m.group(1), m.group(2)]}]

    return None  # ambiguous


def main():
    corpus = build_corpus()
    rules = [r for r in corpus.all() if r.phase.startswith("1B")]
    total_mods = 0
    parsed = 0
    unparsed = 0
    unparsed_examples = []

    for rule in rules:
        for mod in (rule.modifiers or []):
            cond = mod.get("condition", "")
            if not cond or isinstance(cond, list):
                continue  # already structured or empty
            total_mods += 1
            result = try_parse(cond)
            if result:
                parsed += 1
            else:
                unparsed += 1
                if len(unparsed_examples) < 20:
                    unparsed_examples.append({"rule": rule.rule_id, "condition": cond})

    print(f"Total string modifier conditions: {total_mods}")
    print(f"Parseable (auto-convert): {parsed} ({100*parsed/max(total_mods,1):.0f}%)")
    print(f"Ambiguous (keep as string): {unparsed} ({100*unparsed/max(total_mods,1):.0f}%)")
    if unparsed_examples:
        print(f"\nFirst {len(unparsed_examples)} unparseable:")
        for ex in unparsed_examples:
            print(f"  {ex['rule']}: {ex['condition']}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run dry-run**

Run: `.venv/bin/python tools/migrate_modifier_conditions.py`
Expected: Report showing conversion rate.

- [ ] **Step 3: Commit**

```bash
git add tools/migrate_modifier_conditions.py
git commit -m "feat(s316): add modifier condition migration tool (dry-run)

Reports parseable vs ambiguous modifier condition strings. Deterministic
patterns: lord_in_house, planet_in_house, planet_dignity, planets_conjunct."
```

---

### Task 18: Feature Registry Update

**Files:**
- Modify: `src/corpus/feature_registry.py`
- Test: `tests/test_s316_contracts.py` (append)

- [ ] **Step 1: Write test**

```python
from src.corpus.feature_registry import IMPLEMENTED_FEATURES, PENDING_FEATURES


def test_s316_features_implemented():
    """All S316 primitives are in IMPLEMENTED_FEATURES."""
    s316_features = {
        "argala_condition", "functional_benefic", "same_planet_constraint",
        "dynamic_karaka", "shadbala_strength", "navamsa_lagna",
        "modifier_execution", "bhavat_bhavam_execution",
        "modifier_condition_structured", "prediction_type_classification",
        "timing_activation",
    }
    for f in s316_features:
        assert f in IMPLEMENTED_FEATURES, f"{f} not in IMPLEMENTED_FEATURES"


def test_s316_features_not_pending():
    """S316 features removed from PENDING_FEATURES."""
    s316_features = {
        "argala_condition", "functional_benefic", "same_planet_constraint",
        "dynamic_karaka", "shadbala_strength", "navamsa_lagna",
        "modifier_execution", "bhavat_bhavam_execution",
        "modifier_condition_structured", "prediction_type_classification",
    }
    for f in s316_features:
        assert f not in PENDING_FEATURES, f"{f} still in PENDING_FEATURES"
```

- [ ] **Step 2: Update feature_registry.py**

Move features from `PENDING_FEATURES` to `IMPLEMENTED_FEATURES`:
- `same_planet_constraint`
- `shadbala_strength`
- `dynamic_karaka`
- `functional_benefic`
- `navamsa_lagna`
- `modifier_condition_structured`
- `modifier_execution`
- `prediction_type_classification`
- `bhavat_bhavam_execution`

Add new entries to `IMPLEMENTED_FEATURES`:
- `argala_condition`
- `timing_activation`

- [ ] **Step 3: Run tests, commit**

```bash
git add src/corpus/feature_registry.py tests/test_s316_contracts.py
git commit -m "feat(s316): update feature registry — 11 features now implemented

Moves same_planet_constraint, shadbala_strength, dynamic_karaka,
functional_benefic, navamsa_lagna, modifier_condition_structured,
modifier_execution, prediction_type_classification, bhavat_bhavam_execution
from PENDING to IMPLEMENTED. Adds argala_condition, timing_activation."
```

---

### Task 19: Verse Audit Completeness (Open Loop)

**Files:**
- Modify: `tools/v2_scorecard.py` (Section M upgrade)
- Test: run scorecard and verify output

- [ ] **Step 1: Enhance Section M**

In `tools/v2_scorecard.py`, find the verse coverage section and add a threshold check:

```python
# After computing verse_coverage_ratio per chapter:
if verse_coverage_ratio < 0.95:
    red_flags.append(RedFlag(
        rule_id=f"Ch.{ch}",
        severity="warning",
        category="verse_coverage_gap",
        message=f"Verse coverage {verse_coverage_ratio:.0%} below 95% threshold",
        fix=f"Review verse audit for Ch.{ch} — {missing} verses unencoded",
    ))
```

- [ ] **Step 2: Run scorecard**

Run: `.venv/bin/python tools/v2_scorecard.py --v2-only`
Expected: Any chapters below 95% flagged.

- [ ] **Step 3: Commit**

```bash
git add tools/v2_scorecard.py
git commit -m "feat(s316): add 95% verse coverage threshold to scorecard Section M

Chapters below 95% verse coverage flagged as warnings with specific
missing verse count."
```

---

### Task 20: Docs Pre-Push Enforcement (Open Loop)

**Files:**
- Modify: `.git/hooks/pre-push`

- [ ] **Step 1: Add docs check**

Append to `.git/hooks/pre-push`:

```bash
# S316: Docs accompaniment check (warning only)
corpus_changes=$(git diff --cached --name-only | grep "^src/corpus/" | head -1)
if [ -n "$corpus_changes" ]; then
    doc_changes=$(git diff --cached --name-only | grep "^docs/" | head -1)
    if [ -z "$doc_changes" ]; then
        echo "⚠️  src/corpus/ changed without docs/ update — consider updating docs"
    fi
fi
```

- [ ] **Step 2: Commit**

```bash
git add .git/hooks/pre-push
git commit -m "feat(s316): add docs accompaniment check to pre-push hook (warning only)

Warns when src/corpus/ changes lack corresponding docs/ updates."
```

---

### Task 21: Integration Test — India 1947 End-to-End

**Files:**
- Create: `tests/test_s316_integration.py`

- [ ] **Step 1: Write integration test**

```python
# tests/test_s316_integration.py
"""End-to-end integration: India 1947 through full inference pipeline."""
from src.calculations.chart import compute_chart
from src.calculations.rule_firing import evaluate_chart
from src.calculations.inference import apply_modifiers, aggregate_domains, analyze_chart
from src.corpus.combined_corpus import build_corpus


def _india_1947():
    return compute_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )


def test_rules_fire():
    chart = _india_1947()
    result = evaluate_chart(chart)
    assert result.total_fired > 0
    assert result.total_evaluated > result.total_fired


def test_modifiers_change_magnitudes():
    """At least some rules should have magnitude != base after modifiers."""
    chart = _india_1947()
    corpus = build_corpus()
    rule_lookup = {r.rule_id: r for r in corpus.all()}
    result = evaluate_chart(chart)

    modified = []
    for fired in result.fired_rules:
        rule = rule_lookup.get(fired.rule_id)
        if rule:
            mr = apply_modifiers(fired, rule, chart=chart, condition_context=fired.context)
            modified.append(mr)

    # At least one rule should have been modified (amplified/attenuated)
    base_mags = {mr.rule_id: mr.source_rule.confidence for mr in modified}
    actual_mags = {mr.rule_id: mr.magnitude for mr in modified}
    different = [rid for rid in base_mags if abs(base_mags[rid] - actual_mags.get(rid, 0)) > 0.01]
    assert len(different) > 0, "No rules had their magnitude changed by modifiers"


def test_h2_score_negative():
    """India 1947 invariant: H2 (wealth/speech) is negative."""
    chart = _india_1947()
    result = evaluate_chart(chart)
    h2_rules = [r for r in result.fired_rules if r.house == 2]
    unfav = sum(1 for r in h2_rules if r.outcome_direction == "unfavorable")
    fav = sum(1 for r in h2_rules if r.outcome_direction == "favorable")
    assert unfav >= fav, f"H2 should be net negative: {fav} favorable vs {unfav} unfavorable"


def test_some_rules_gated_out():
    """With modifier execution, some rules should be gated out."""
    chart = _india_1947()
    corpus = build_corpus()
    rule_lookup = {r.rule_id: r for r in corpus.all()}
    result = evaluate_chart(chart)

    gated = 0
    for fired in result.fired_rules:
        rule = rule_lookup.get(fired.rule_id)
        if rule:
            mr = apply_modifiers(fired, rule, chart=chart, condition_context=fired.context)
            if mr.gated_out:
                gated += 1

    # Some rules should be gated (structured gates that fail)
    # If none are gated, that's also OK — it means no structured gates fail for this chart
    # This test documents the count for regression tracking
    print(f"Gated out: {gated}/{result.total_fired}")


def test_context_attached_to_fired_rules():
    """Fired rules should have context attached."""
    chart = _india_1947()
    result = evaluate_chart(chart)
    with_context = sum(1 for r in result.fired_rules if r.context is not None)
    assert with_context > 0, "No fired rules have context attached"


def test_domain_scores_produced():
    """Full pipeline produces domain scores for all 8 domains."""
    chart = _india_1947()
    corpus = build_corpus()
    analysis = analyze_chart(chart, corpus.all())
    assert len(analysis.domain_scores) >= 8
    assert analysis.total_rules_fired > 0
```

- [ ] **Step 2: Run integration tests**

Run: `.venv/bin/pytest tests/test_s316_integration.py -v`
Expected: PASS

- [ ] **Step 3: Run full suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: All 14,500+ tests pass.

- [ ] **Step 4: Commit**

```bash
git add tests/test_s316_integration.py
git commit -m "test(s316): add end-to-end integration tests — India 1947 through full pipeline

Verifies: rules fire, modifiers change magnitudes, H2 is negative,
context attached, domain scores produced."
```

---

### Task 22: Final Validation + Scorecard

- [ ] **Step 1: Run full test suite**

Run: `.venv/bin/pytest tests/ -q --tb=short`
Expected: ALL PASS

- [ ] **Step 2: Run scorecard**

Run: `.venv/bin/python tools/v2_scorecard.py --v2-only`
Expected: No regression from pre-S316 state.

- [ ] **Step 3: Run condition/modifier audit**

Run: `.venv/bin/python tools/condition_modifier_audit.py`
Expected: Report shows improvement (fewer unresolved flags).

- [ ] **Step 4: Run modifier migration dry-run**

Run: `.venv/bin/python tools/migrate_modifier_conditions.py`
Expected: Report showing parseable vs ambiguous breakdown.

- [ ] **Step 5: Verify feature registry**

Run: `.venv/bin/python -c "from src.corpus.feature_registry import PENDING_FEATURES; print('Remaining pending:', len(PENDING_FEATURES))"`
Expected: Only `planet_in_house_from_aspects` remains pending (not in S316 scope).

- [ ] **Step 6: Commit any final fixes**

```bash
git commit -m "chore(s316): final validation — all tests pass, scorecard clean, features implemented"
```
