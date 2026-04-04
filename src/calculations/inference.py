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
    gate_reason: str = ""
    unevaluated_gates: list[dict] = field(default_factory=list)
    context: dict | None = None


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


# Modifier application order: gates first so we can short-circuit, then negates,
# attenuates, amplifies, qualifies last (informational only).
_EFFECT_ORDER = {"gates": 0, "negates": 1, "attenuates": 2, "amplifies": 3, "qualifies": 4}


def _context_scaled_weight(base_weight: float, condition_context: dict | None) -> float:
    """Scale a modifier weight using the first available consumable aggregate.

    Formula: effective = base * (1 + 0.5 * ctx_strength)
    """
    if not condition_context:
        return base_weight
    aggregates = condition_context.get("aggregates", {})
    for key in CONSUMABLE_AGGREGATES:
        if key in aggregates:
            ctx_strength = float(aggregates[key])
            return base_weight * (1.0 + 0.5 * ctx_strength)
    return base_weight


def apply_modifiers(
    fired: FiredRule,
    rule,
    chart=None,
    condition_context: dict | None = None,
) -> ModifiedRule:
    """Apply modifiers to a fired rule. Returns ModifiedRule or gated-out result.

    Modifiers are applied in strict order: gates → negates → attenuates → amplifies → qualifies.
    Gates with structured conditions (list[dict]) are evaluated via _check_compound_conditions.
    Gates with string conditions are logged as unevaluated with blocking severity.
    Negation uses 3-tier logic: strong flips direction, medium weakens, weak is negligible.
    Weights are scaled by condition context aggregates when available.
    """
    magnitude = fired.confidence  # base magnitude from rule confidence
    direction = fired.outcome_direction
    qualifications: list[str] = []
    gate_reason = ""
    unevaluated_gates: list[dict] = []

    # Use prediction magnitude if available
    if rule.predictions:
        max_pred_mag = max(p.get("magnitude", 0.5) for p in rule.predictions)
        magnitude = max_pred_mag

    # Sort modifiers by effect order
    modifiers = sorted(
        (rule.modifiers or []),
        key=lambda m: _EFFECT_ORDER.get(m.get("effect", ""), 99),
    )

    for mod in modifiers:
        effect = mod.get("effect", "")
        strength = mod.get("strength", "medium")
        base_weight = _STRENGTH_WEIGHTS.get(strength, 0.30)
        weight = _context_scaled_weight(base_weight, condition_context)
        condition = mod.get("condition", "")

        if effect == "gates":
            if isinstance(condition, list):
                # Structured gate — evaluate via compound conditions engine
                from src.calculations.rule_firing import _check_compound_conditions

                gate_ctx = dict(condition_context) if condition_context else None
                fires, _ = _check_compound_conditions(condition, chart, context=gate_ctx)
                if not fires:
                    gate_reason = f"gate failed: {condition}"
                    return ModifiedRule(
                        rule_id=fired.rule_id,
                        primary_domain=getattr(rule, "primary_domain", "character"),
                        direction=direction,
                        magnitude=0.0,
                        source_rule=fired,
                        qualifications=qualifications,
                        gated_out=True,
                        gate_reason=gate_reason,
                        unevaluated_gates=unevaluated_gates,
                        context=condition_context,
                    )
            else:
                # String gate — not evaluable, log with severity
                severity = "blocking" if strength in ("strong", "medium") else "informational"
                unevaluated_gates.append({
                    "condition": condition,
                    "strength": strength,
                    "severity": severity,
                })

        elif effect == "negates":
            # 3-tier negation: strong flips, medium weakens, weak negligible
            if strength == "strong":
                if direction == "favorable":
                    direction = "unfavorable"
                elif direction == "unfavorable":
                    direction = "favorable"
            elif strength == "medium":
                magnitude *= (1.0 - weight)

            # weak: no change (negligible)

        elif effect == "attenuates":
            magnitude *= (1.0 - weight)

        elif effect == "amplifies":
            magnitude *= (1.0 + weight)

        elif effect == "qualifies":
            qualifications.append(condition if isinstance(condition, str) else str(condition))

    return ModifiedRule(
        rule_id=fired.rule_id,
        primary_domain=getattr(rule, "primary_domain", "character"),
        direction=direction,
        magnitude=round(magnitude, 3),
        source_rule=fired,
        qualifications=qualifications,
        gate_reason=gate_reason,
        unevaluated_gates=unevaluated_gates,
        context=condition_context,
    )


def aggregate_domains(
    modified_rules: list[ModifiedRule],
    contrary_mirrors: set[tuple[str, str]] | None = None,
) -> dict[str, DomainScore]:
    """Aggregate fired rules into domain scores.

    Conflict resolution layers:
      1. Contrary mirror cancellation — rule pairs in contrary_mirrors cancel to net 0
      2. Same signal-group dominance — opposite directions in the same signal_group
         keep only the strongest rule (by abs magnitude)
      3. Confidence-weighted scoring — effective = magnitude × source confidence
    """
    from src.corpus.taxonomy import PRIMARY_DOMAIN_PRIORITY

    # --- 1. Contrary mirror cancellation ---
    cancelled_ids: set[str] = set()
    if contrary_mirrors:
        rule_ids = {mr.rule_id for mr in modified_rules if not mr.gated_out}
        for a, b in contrary_mirrors:
            if a in rule_ids and b in rule_ids:
                cancelled_ids.add(a)
                cancelled_ids.add(b)

    # --- 2. Signal-group dominance ---
    suppressed_ids: set[str] = set()
    # Group active rules by (domain, signal_group)
    from collections import defaultdict
    sg_groups: dict[tuple[str, str], list[ModifiedRule]] = defaultdict(list)
    for mr in modified_rules:
        if mr.gated_out or mr.rule_id in cancelled_ids:
            continue
        sg = getattr(mr.source_rule, "signal_group", "") or ""
        if sg:
            sg_groups[(mr.primary_domain, sg)].append(mr)

    for _key, group in sg_groups.items():
        directions = {mr.direction for mr in group}
        if "favorable" in directions and "unfavorable" in directions:
            # Opposite directions present — keep only the strongest
            strongest = max(group, key=lambda m: abs(m.magnitude))
            for mr in group:
                if mr.rule_id != strongest.rule_id:
                    suppressed_ids.add(mr.rule_id)

    # --- 3. Accumulate with confidence weighting ---
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
            # mixed/neutral — split evenly
            ds.favorable_score += effective * 0.5
            ds.unfavorable_score += effective * 0.5

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
