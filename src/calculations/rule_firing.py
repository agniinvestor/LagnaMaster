"""src/calculations/rule_firing.py — Evaluate which corpus rules fire for a chart.

Bridges the corpus (6,500+ rules) to the scoring engine by evaluating each
rule's primary_condition against a computed chart.

Usage:
    from src.calculations.rule_firing import evaluate_chart
    result = evaluate_chart(chart)
    # result.fired_rules: list of FiredRule
    # result.house_summary: dict[int, HouseRuleSummary]
    # result.feature_vector(): dict of ML-ready features
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class FiredRule:
    """A single corpus rule that fires for this chart."""
    rule_id: str
    source: str
    planet: str
    house: int  # 0 if not house-specific
    outcome_direction: str
    outcome_domains: list[str]
    confidence: float
    concordance_count: int  # how many texts agree


@dataclass
class HouseRuleSummary:
    """Aggregated rule-firing statistics for one house."""
    house: int
    total_fired: int = 0
    favorable_count: int = 0
    unfavorable_count: int = 0
    mixed_count: int = 0
    neutral_count: int = 0
    mean_confidence: float = 0.0
    source_count: int = 0  # unique sources that fired rules for this house
    concordance_score: float = 0.0  # fraction of rules with concordance
    dominant_direction: str = "neutral"


@dataclass
class RuleFiringResult:
    """Complete rule-firing evaluation for a chart."""
    fired_rules: list[FiredRule] = field(default_factory=list)
    house_summary: dict[int, HouseRuleSummary] = field(default_factory=dict)
    total_fired: int = 0
    total_evaluated: int = 0

    def feature_vector(self) -> dict[str, float]:
        """Return ML-ready features from rule firing.

        Features per house (12 houses × 7 features = 84 features):
          h{N}_rules_fired: total rules that fired
          h{N}_favorable_ratio: fraction of fired rules that are favorable
          h{N}_unfavorable_ratio: fraction of fired rules that are unfavorable
          h{N}_mean_confidence: average confidence of fired rules
          h{N}_source_count: number of unique source texts
          h{N}_concordance_score: fraction with cross-text concordance
          h{N}_direction_score: +1 if dominant favorable, -1 if unfavorable, 0 mixed

        Global features (5):
          global_total_fired: total rules fired across all houses
          global_favorable_ratio: overall favorable ratio
          global_mean_confidence: overall mean confidence
          global_concordance_ratio: fraction of all fired rules with concordance
          global_source_diversity: unique sources across all fired rules
        """
        features: dict[str, float] = {}

        for h in range(1, 13):
            s = self.house_summary.get(h)
            prefix = f"h{h:02d}"
            if s and s.total_fired > 0:
                features[f"{prefix}_rules_fired"] = float(s.total_fired)
                features[f"{prefix}_favorable_ratio"] = s.favorable_count / s.total_fired
                features[f"{prefix}_unfavorable_ratio"] = s.unfavorable_count / s.total_fired
                features[f"{prefix}_mean_confidence"] = s.mean_confidence
                features[f"{prefix}_source_count"] = float(s.source_count)
                features[f"{prefix}_concordance_score"] = s.concordance_score
                dir_score = (s.favorable_count - s.unfavorable_count) / s.total_fired
                features[f"{prefix}_direction_score"] = dir_score
            else:
                features[f"{prefix}_rules_fired"] = 0.0
                features[f"{prefix}_favorable_ratio"] = 0.0
                features[f"{prefix}_unfavorable_ratio"] = 0.0
                features[f"{prefix}_mean_confidence"] = 0.0
                features[f"{prefix}_source_count"] = 0.0
                features[f"{prefix}_concordance_score"] = 0.0
                features[f"{prefix}_direction_score"] = 0.0

        # Global features
        if self.total_fired > 0:
            all_fav = sum(1 for r in self.fired_rules if r.outcome_direction == "favorable")
            all_conc = sum(1 for r in self.fired_rules if r.concordance_count > 0)
            all_sources = len({r.source for r in self.fired_rules})
            features["global_total_fired"] = float(self.total_fired)
            features["global_favorable_ratio"] = all_fav / self.total_fired
            features["global_mean_confidence"] = sum(r.confidence for r in self.fired_rules) / self.total_fired
            features["global_concordance_ratio"] = all_conc / self.total_fired
            features["global_source_diversity"] = float(all_sources)
        else:
            features["global_total_fired"] = 0.0
            features["global_favorable_ratio"] = 0.0
            features["global_mean_confidence"] = 0.0
            features["global_concordance_ratio"] = 0.0
            features["global_source_diversity"] = 0.0

        return features


def _planet_house(chart, planet_name: str) -> int:
    """Get house number (1-12) for a planet using sign-based system."""
    p = chart.planets.get(planet_name)
    if not p:
        # Try capitalized variations
        for key in chart.planets:
            if key.lower() == planet_name.lower():
                p = chart.planets[key]
                break
    if not p:
        return 0
    return (p.sign_index - chart.lagna_sign_index) % 12 + 1


def _planet_sign(chart, planet_name: str) -> str:
    """Get sign name for a planet."""
    p = chart.planets.get(planet_name)
    if not p:
        for key in chart.planets:
            if key.lower() == planet_name.lower():
                p = chart.planets[key]
                break
    if not p:
        return ""
    return p.sign.lower()


def _normalize_planet_name(name: str) -> str:
    """Normalize planet name for lookup."""
    return name.lower().replace(" ", "")


def _check_rule_fires(rule, chart) -> tuple[bool, int]:
    """Check if a rule's primary_condition is satisfied by this chart.

    Returns (fires: bool, house: int).
    House is 0 for non-house-specific rules.
    """
    pc = rule.primary_condition
    if not pc:
        return False, 0

    planet = pc.get("planet", "")
    ptype = pc.get("placement_type", "")
    pval = pc.get("placement_value", [])

    # Normalize planet name
    planet_norm = _normalize_planet_name(planet)

    # Skip compound/multi-planet rules that need conjunction detection
    # (we'll add conjunction checking later)
    if planet_norm in ("house_lord", "nodes", "general", "none", ""):
        return False, 0

    # Handle conjunction rules (e.g., "sun_moon", "mars_jupiter")
    if "_" in planet_norm and ptype in ("conjunction_in_house", "conjunction_condition",
                                         "multi_conjunction"):
        # Check if both/all planets are in the same house
        parts = planet_norm.split("_")
        if len(parts) == 2:
            h1 = _planet_house(chart, parts[0].title())
            h2 = _planet_house(chart, parts[1].title())
            if h1 > 0 and h2 > 0 and h1 == h2:
                if ptype == "conjunction_in_house":
                    # Check if they're in the specified house
                    target_house = pval[0] if pval else 0
                    if isinstance(target_house, int) and target_house == h1:
                        return True, h1
                    if not pval or not isinstance(pval[0] if pval else None, int):
                        return True, h1
                else:
                    return True, h1
        return False, 0

    # Sign placement rules
    if ptype == "sign_placement":
        target_sign = pval[0] if pval else ""
        if isinstance(target_sign, str):
            actual_sign = _planet_sign(chart, planet_norm.title())
            if actual_sign == target_sign.lower():
                # Determine house for this planet
                h = _planet_house(chart, planet_norm.title())
                return True, h
        return False, 0

    # House placement rules
    if ptype == "house_placement":
        target_house = pc.get("house", pval[0] if pval else 0)
        if isinstance(target_house, int) and target_house > 0:
            actual_house = _planet_house(chart, planet_norm.title())
            if actual_house == target_house:
                return True, target_house
        return False, 0

    # Sign condition / house condition (modifier rules)
    # These are supplementary/general rules — they modify base rules,
    # not standalone predictions. Skip for now; they'll be wired when
    # the modifier system is built.
    if ptype in ("sign_condition", "house_condition", "conjunction_condition"):
        return False, 0

    # Yoga rules — need dedicated yoga detection logic
    if ptype in ("yoga", "special"):
        return False, 0

    # Lagna-conditional rules (BVR)
    if ptype in ("house_placement",) and rule.lagna_scope:
        # Check if chart's lagna matches the rule's lagna_scope
        chart_lagna = chart.lagna_sign.lower()
        if chart_lagna not in rule.lagna_scope:
            return False, 0
        # Lagna matches — check house placement
        target_house = pc.get("house", pval[0] if pval else 0)
        if isinstance(target_house, int):
            actual_house = _planet_house(chart, planet_norm.title())
            if actual_house == target_house:
                return True, target_house
        return False, 0

    return False, 0


def evaluate_chart(chart) -> RuleFiringResult:
    """Evaluate all Phase 1B corpus rules against a chart.

    Returns a RuleFiringResult with fired rules, house summaries,
    and an ML-ready feature vector.
    """
    from src.corpus.combined_corpus import build_corpus

    corpus = build_corpus()
    phase1b_rules = [r for r in corpus.all() if r.phase.startswith("1B")]

    result = RuleFiringResult()
    result.total_evaluated = len(phase1b_rules)

    for rule in phase1b_rules:
        fires, house = _check_rule_fires(rule, chart)
        if not fires:
            continue

        conc_count = len(rule.concordance_texts) if rule.concordance_texts else 0

        fired = FiredRule(
            rule_id=rule.rule_id,
            source=rule.source,
            planet=rule.primary_condition.get("planet", ""),
            house=house,
            outcome_direction=rule.outcome_direction,
            outcome_domains=rule.outcome_domains,
            confidence=rule.confidence,
            concordance_count=conc_count,
        )
        result.fired_rules.append(fired)

    result.total_fired = len(result.fired_rules)

    # Build house summaries
    for h in range(1, 13):
        house_rules = [r for r in result.fired_rules if r.house == h]
        if not house_rules:
            result.house_summary[h] = HouseRuleSummary(house=h)
            continue

        fav = sum(1 for r in house_rules if r.outcome_direction == "favorable")
        unfav = sum(1 for r in house_rules if r.outcome_direction == "unfavorable")
        mixed = sum(1 for r in house_rules if r.outcome_direction == "mixed")
        neutral = sum(1 for r in house_rules if r.outcome_direction == "neutral")
        mean_conf = sum(r.confidence for r in house_rules) / len(house_rules)
        sources = len({r.source for r in house_rules})
        conc_frac = sum(1 for r in house_rules if r.concordance_count > 0) / len(house_rules)

        if fav > unfav and fav > mixed:
            dominant = "favorable"
        elif unfav > fav and unfav > mixed:
            dominant = "unfavorable"
        elif mixed > 0:
            dominant = "mixed"
        else:
            dominant = "neutral"

        result.house_summary[h] = HouseRuleSummary(
            house=h,
            total_fired=len(house_rules),
            favorable_count=fav,
            unfavorable_count=unfav,
            mixed_count=mixed,
            neutral_count=neutral,
            mean_confidence=mean_conf,
            source_count=sources,
            concordance_score=conc_frac,
            dominant_direction=dominant,
        )

    return result
