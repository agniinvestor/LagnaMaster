"""src/calculations/feature_expansion.py — Expand V2 corpus into continuous feature vectors.

Converts 600 V2 rules into continuous features per chart. Each rule produces
a signal ∈ [-1, 1] based on how strongly its conditions are met, weighted by
the dignity and functional status of involved planets.

This is Phase 2 S411-S425 work: expanding from 156 features (23 rules) to
600+ features (full V2 corpus).
"""
from __future__ import annotations

from dataclasses import dataclass

from src.calculations.diagnostic_scorer import (
    _planet_house, _lord_of_house, _is_func_benefic,
    _is_func_malefic, _placement_score, _clamp,
    _EXALT_SIGN, _DEBIL_SIGN, _OWN_SIGNS, _MT_SIGNS,
)


def _continuous_dignity(chart, planet_name: str) -> float:
    """Dignity as continuous value in [-1, 1].
    Exalted=1.0, MT=0.7, own=0.5, neutral=0.0, debilitated=-1.0."""
    pos = chart.planets.get(planet_name)
    if not pos:
        return 0.0
    si = pos.sign_index
    name = planet_name
    if name in _MT_SIGNS and si == _MT_SIGNS[name]:
        return 0.7
    if name in _EXALT_SIGN and si == _EXALT_SIGN[name]:
        return 1.0
    if name in _OWN_SIGNS and si in _OWN_SIGNS[name]:
        return 0.5
    if name in _DEBIL_SIGN and si == _DEBIL_SIGN[name]:
        return -1.0
    return 0.0


def _functional_sign(chart, planet_name: str) -> float:
    """Functional benefic=+1, malefic=-1, neutral=0."""
    if _is_func_benefic(chart, planet_name):
        return 1.0
    if _is_func_malefic(chart, planet_name):
        return -1.0
    return 0.0


def compute_rule_signal(rule, chart) -> float:
    """Compute continuous signal for one V2 rule against a chart.

    Returns: float in [-1, 1] where:
        0 = rule doesn't fire or neutral
        +1 = strong favorable signal
        -1 = strong unfavorable signal
    """
    pc = rule.primary_condition
    if not pc:
        return 0.0

    conditions = pc.get("conditions", [])
    if not conditions or not isinstance(conditions, list):
        return 0.0
    if not isinstance(conditions[0], dict) or "type" not in conditions[0]:
        return 0.0

    # Check if rule fires (all conditions must pass)
    from src.calculations.rule_firing import _check_compound_conditions
    fires, house = _check_compound_conditions(conditions, chart)
    if not fires:
        return 0.0

    # Rule fires — now compute signal strength
    direction_mult = 1.0 if rule.outcome_direction == "favorable" else (
        -1.0 if rule.outcome_direction == "unfavorable" else 0.5
    )

    # Strength based on condition type
    strength = 0.5  # base: rule fires but no strength info

    cond = conditions[0]
    ctype = cond.get("type", "")

    if ctype == "lord_in_house":
        lord_of = cond.get("lord_of", 0)
        lord = _lord_of_house(chart, lord_of) if lord_of else ""
        if lord:
            dignity = _continuous_dignity(chart, lord)
            placement = _placement_score(_planet_house(chart, lord))
            strength = 0.5 + 0.3 * dignity + 0.2 * (placement - 0.5)

    elif ctype == "planet_in_house":
        planet = cond.get("planet", "")
        if planet and not planet.startswith(("any_", "lord_")):
            dignity = _continuous_dignity(chart, planet.title())
            func = _functional_sign(chart, planet.title())
            strength = 0.5 + 0.3 * dignity + 0.2 * func
        else:
            strength = 0.5  # any_benefic/any_malefic — binary

    elif ctype == "planet_dignity":
        planet = cond.get("planet", "")
        if planet.startswith("lord_of_"):
            h = int(planet.split("_")[-1])
            planet = _lord_of_house(chart, h)
        if planet:
            strength = 0.5 + 0.5 * abs(_continuous_dignity(chart, planet.title()))

    elif ctype == "planets_conjunct":
        planets = cond.get("planets", [])
        if len(planets) >= 2:
            dignities = []
            for p in planets:
                if p.startswith("lord_of_"):
                    h = int(p.split("_")[-1])
                    p = _lord_of_house(chart, h)
                if p and chart.planets.get(p.title()):
                    dignities.append(_continuous_dignity(chart, p.title()))
            if dignities:
                strength = 0.5 + 0.3 * (sum(dignities) / len(dignities))

    elif ctype in ("upagraha_in_house", "argala_condition"):
        strength = 0.5  # binary — no continuous gradient available

    elif ctype == "planet_in_derived_house":
        planet = cond.get("planet", "")
        if planet and not planet.startswith(("any_", "lord_")):
            strength = 0.5 + 0.3 * _continuous_dignity(chart, planet.title())

    else:
        strength = 0.5  # unknown type — neutral

    signal = _clamp(direction_mult * strength * rule.confidence, -1.0, 1.0)
    return round(signal, 4)


@dataclass
class ExpandedFeatureVector:
    """Feature vector with one continuous signal per V2 rule."""
    rule_ids: list[str]
    signals: list[float]  # parallel to rule_ids
    n_fired: int = 0
    n_rules: int = 0

    def to_dict(self) -> dict[str, float]:
        return {rid: sig for rid, sig in zip(self.rule_ids, self.signals)}

    def to_list(self) -> list[float]:
        return list(self.signals)


def extract_expanded_features(chart, rules: list) -> ExpandedFeatureVector:
    """Extract continuous feature vector from full V2 corpus for one chart."""
    rule_ids = []
    signals = []
    n_fired = 0

    for rule in rules:
        rid = rule.rule_id
        sig = compute_rule_signal(rule, chart)
        rule_ids.append(rid)
        signals.append(sig)
        if sig != 0.0:
            n_fired += 1

    return ExpandedFeatureVector(
        rule_ids=rule_ids,
        signals=signals,
        n_fired=n_fired,
        n_rules=len(rules),
    )
