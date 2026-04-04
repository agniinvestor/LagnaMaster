"""src/calculations/inference.py — Inference engine: modifier application + domain aggregation.

Layers:
  1. Rule Firing (rule_firing.py) — conditions → fires/doesn't
  2. Modifier Application (this file) — modifiers adjust fired rules
  3. Domain Aggregation (this file) — multiple rules → domain scores
"""
from __future__ import annotations
from dataclasses import dataclass, field

from src.calculations.rule_firing import evaluate_chart, FiredRule


# Strength weights for modifier magnitude adjustment
_STRENGTH_WEIGHTS = {"weak": 0.15, "medium": 0.30, "strong": 0.50}

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


@dataclass
class ModifiedRule:
    """A fired rule after modifier application."""
    rule_id: str
    primary_domain: str
    direction: str  # favorable/unfavorable/mixed/neutral
    magnitude: float
    source_rule: FiredRule
    qualifications: list[str] = field(default_factory=list)
    gated_out: bool = False


@dataclass
class DomainScore:
    """Aggregated score for a single domain."""
    domain: str
    favorable_score: float = 0.0
    unfavorable_score: float = 0.0
    net_score: float = 0.0
    rule_count: int = 0
    strongest_rule_id: str = ""
    strongest_magnitude: float = 0.0


@dataclass
class ChartAnalysis:
    """Complete analysis of a birth chart."""
    domain_scores: dict[str, DomainScore] = field(default_factory=dict)
    fired_rules: list[ModifiedRule] = field(default_factory=list)
    total_rules_fired: int = 0
    total_rules_gated: int = 0


def apply_modifiers(fired: FiredRule, rule) -> ModifiedRule:
    """Apply modifiers to a fired rule. Returns ModifiedRule or gated-out result."""
    magnitude = fired.confidence  # base magnitude from rule confidence
    direction = fired.outcome_direction
    qualifications = []

    # Use prediction magnitude if available
    if rule.predictions:
        max_pred_mag = max(p.get("magnitude", 0.5) for p in rule.predictions)
        magnitude = max_pred_mag

    for mod in (rule.modifiers or []):
        effect = mod.get("effect", "")
        strength = mod.get("strength", "medium")
        weight = _STRENGTH_WEIGHTS.get(strength, 0.30)

        if effect == "gates":
            # Gates currently don't evaluate (no modifier condition engine yet)
            # They are documented constraints — in future, evaluate_gate() here
            pass
        elif effect == "amplifies":
            magnitude *= (1.0 + weight)
        elif effect == "attenuates":
            magnitude *= (1.0 - weight)
        elif effect == "negates":
            # Flip direction
            if direction == "favorable":
                direction = "unfavorable"
            elif direction == "unfavorable":
                direction = "favorable"
            magnitude *= weight  # reduce magnitude since negation is conditional
        elif effect == "qualifies":
            qualifications.append(mod.get("condition", ""))

    return ModifiedRule(
        rule_id=fired.rule_id,
        primary_domain=getattr(rule, "primary_domain", "character"),
        direction=direction,
        magnitude=round(magnitude, 3),
        source_rule=fired,
        qualifications=qualifications,
    )


def aggregate_domains(modified_rules: list[ModifiedRule]) -> dict[str, DomainScore]:
    """Aggregate fired rules into domain scores."""
    from src.corpus.taxonomy import PRIMARY_DOMAIN_PRIORITY

    scores = {}
    for domain in PRIMARY_DOMAIN_PRIORITY:
        scores[domain] = DomainScore(domain=domain)

    for mr in modified_rules:
        if mr.gated_out:
            continue
        domain = mr.primary_domain
        if domain not in scores:
            scores[domain] = DomainScore(domain=domain)

        ds = scores[domain]
        ds.rule_count += 1

        if mr.direction == "favorable":
            ds.favorable_score += mr.magnitude
        elif mr.direction == "unfavorable":
            ds.unfavorable_score += mr.magnitude
        else:
            # mixed/neutral — split evenly
            ds.favorable_score += mr.magnitude * 0.5
            ds.unfavorable_score += mr.magnitude * 0.5

        ds.net_score = round(ds.favorable_score - ds.unfavorable_score, 3)

        if abs(mr.magnitude) > ds.strongest_magnitude:
            ds.strongest_magnitude = abs(mr.magnitude)
            ds.strongest_rule_id = mr.rule_id

    return scores


def analyze_chart(chart, rules) -> ChartAnalysis:
    """Full inference: fire rules → apply modifiers → aggregate domains."""
    # Layer 1: Fire rules
    firing_result = evaluate_chart(chart)

    # Build rule lookup
    rule_lookup = {r.rule_id: r for r in rules}

    # Layer 2: Apply modifiers
    modified = []
    gated = 0
    for fired in firing_result.fired_rules:
        rule = rule_lookup.get(fired.rule_id)
        if not rule:
            continue
        mr = apply_modifiers(fired, rule)
        if mr.gated_out:
            gated += 1
        modified.append(mr)

    # Layer 3: Aggregate
    domain_scores = aggregate_domains(modified)

    return ChartAnalysis(
        domain_scores=domain_scores,
        fired_rules=modified,
        total_rules_fired=len(modified),
        total_rules_gated=gated,
    )
