# Design Spec: Inference Architecture (Track 5)

**Date:** 2026-04-03
**Session:** S313 (governance)
**Status:** Spec only — implementation deferred to dedicated session
**Dependencies:** Track 1 (modifier standardization) ✅, Track 2 (domain normalization) ✅

## Problem

The rule firing engine evaluates conditions independently — each rule fires or doesn't. There is no:
- Aggregation of multiple rules firing for the same domain
- Conflict resolution when contradictory rules fire
- Modifier execution (gates/amplifies/attenuates/negates/qualifies effects)
- Score computation per domain

## Architecture

### Three-Layer Stack

```
Layer 1: Rule Firing (EXISTS) — conditions → fires/doesn't
Layer 2: Modifier Application (NEW) — modifiers adjust fired rules
Layer 3: Domain Aggregation (NEW) — multiple rules → domain scores
```

### Layer 2: Modifier Application

For each fired rule, apply its modifiers:

```python
def apply_modifiers(rule, chart) -> ModifiedResult:
    base = FiredRule(rule)
    for mod in rule.modifiers:
        if mod["effect"] == "gates":
            if not evaluate_gate(mod, chart):
                return None  # rule doesn't apply
        elif mod["effect"] == "amplifies":
            base.magnitude *= 1.0 + STRENGTH_WEIGHTS[mod["strength"]]
        elif mod["effect"] == "attenuates":
            base.magnitude *= 1.0 - STRENGTH_WEIGHTS[mod["strength"]]
        elif mod["effect"] == "negates":
            base.magnitude *= -1.0  # flip direction
        elif mod["effect"] == "qualifies":
            base.qualifications.append(mod["condition"])
    return base
```

Strength weights: `weak=0.15, medium=0.30, strong=0.50`

### Layer 3: Domain Aggregation

```python
def aggregate_domain(domain, fired_rules) -> DomainScore:
    rules_for_domain = [r for r in fired_rules if r.primary_domain == domain]
    
    favorable = sum(r.magnitude for r in rules_for_domain if r.direction == "favorable")
    unfavorable = sum(r.magnitude for r in rules_for_domain if r.direction == "unfavorable")
    
    return DomainScore(
        domain=domain,
        favorable_score=favorable,
        unfavorable_score=unfavorable,
        net_score=favorable - unfavorable,
        rule_count=len(rules_for_domain),
        strongest_rule=max(rules_for_domain, key=lambda r: abs(r.magnitude)),
    )
```

### Conflict Resolution

When contradictory rules fire (same domain, opposite directions):
1. Net scoring — favorable and unfavorable cancel partially
2. Strongest-wins — the rule with highest magnitude dominates
3. Rule relationships — `contrary_mirror` pairs explicitly cancel

Default: net scoring with strongest-rule annotation.

## Output

```python
@dataclass
class ChartAnalysis:
    chart: BirthChart
    domain_scores: dict[str, DomainScore]  # 8 primary domains
    fired_rules: list[ModifiedResult]
    qualifications: list[str]  # from qualifies modifiers
```

## Implementation Scope

This spec defines the target architecture. Implementation should be:
1. `src/calculations/inference.py` — new file, Layer 2 + Layer 3
2. Integration with existing `rule_firing.py` (Layer 1)
3. Tests with India 1947 fixture

## NOT in scope

- Timing activation (probabilistic windows) — Track 7
- Dasha-period integration
- Bhavat-bhavam scoring
- UI/report generation
