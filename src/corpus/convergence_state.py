"""src/corpus/convergence_state.py — Convergence state recording schema (Tier 3, Item 2).

Defines the schema for recording convergence state at prediction time.
When a prediction is issued to a user, the convergence state captures
what evidence supported it — enabling Phase 3 Bayesian updates to
weight high-concordance confirmations differently from low-concordance ones.

This module defines the SCHEMA only. The actual recording happens in Phase 3
when the feedback loop is built.

Usage:
    from src.corpus.convergence_state import ConvergenceState

    state = ConvergenceState.from_fired_rules(fired_rules, house=7)
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ConvergenceState:
    """Convergence state at the time a prediction is issued.

    Recorded alongside every user-facing prediction to enable
    proper Bayesian weight assignment in Phase 3.
    """
    # Layer I: Classical concordance
    concordance_count: int = 0            # How many texts agree
    concordance_sources: list[str] = field(default_factory=list)  # Which texts
    concordance_score: float = 0.0        # 0-1 normalized agreement

    # Layer II: Structural convergence
    rules_fired_count: int = 0            # How many rules contributed
    signal_group_count: int = 0           # How many INDEPENDENT signals
    mean_confidence: float = 0.0          # Average confidence of contributing rules
    dominant_direction: str = "neutral"    # What direction most rules agree on

    # Metadata
    corpus_hash: str = ""                 # Which corpus version
    house: int = 0                        # Which house prediction relates to
    entity_target: str = "native"         # Who the prediction is about

    @classmethod
    def from_fired_rules(cls, fired_rules: list, house: int = 0) -> "ConvergenceState":
        """Build convergence state from a list of FiredRule objects for a house."""
        house_rules = [r for r in fired_rules if r.house == house] if house else fired_rules
        if not house_rules:
            return cls(house=house)

        conc_sources: set[str] = set()
        signal_groups: set[str] = set()
        total_conf = 0.0

        for r in house_rules:
            total_conf += r.confidence
            if r.concordance_count > 0:
                conc_sources.add(r.source)
            if hasattr(r, "signal_group") and r.signal_group:
                signal_groups.add(r.signal_group)

        fav = sum(1 for r in house_rules if r.outcome_direction == "favorable")
        unfav = sum(1 for r in house_rules if r.outcome_direction == "unfavorable")

        return cls(
            concordance_count=len(conc_sources),
            concordance_sources=sorted(conc_sources),
            concordance_score=len(conc_sources) / max(len(house_rules), 1),
            rules_fired_count=len(house_rules),
            signal_group_count=len(signal_groups),
            mean_confidence=total_conf / len(house_rules),
            dominant_direction="favorable" if fav > unfav else ("unfavorable" if unfav > fav else "neutral"),
            house=house,
            entity_target=house_rules[0].entity_target if hasattr(house_rules[0], "entity_target") else "native",
        )
