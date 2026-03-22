"""
src/calculations/rule_interaction.py — Session 35

Implements the 30 rule-pair interaction modifiers from REF_RuleInteractionMatrix.
When two specific rules fire simultaneously, the combined score is adjusted.

Types:
  Amplified          → add bonus to house total
  Mixed Promise      → floor the combined pair contribution
  Nullified          → one rule cancels the other
  Amplified negative → add negative penalty
  Contextual         → apply modifier from context

Public API
----------
  apply_rule_interactions(rule_scores: dict[str, float]) -> float
      Takes a dict of {rule_code: contribution} for one house,
      returns the interaction modifier to ADD to the raw total.
"""

from __future__ import annotations
from typing import NamedTuple


class Interaction(NamedTuple):
    rule_a: str
    rule_b: str
    kind: str  # "amplified","mixed","nullified","neg_amplified","contextual"
    modifier: float  # what to apply when both fire


# 30 pairs from REF_RuleInteractionMatrix (workbook-verified)
_INTERACTIONS: list[Interaction] = [
    Interaction("R04", "R02", "amplified", +0.5),
    Interaction("R04", "R21", "amplified", +0.5),
    Interaction("R04", "R20", "amplified", +0.5),
    Interaction("R06", "R02", "amplified", +0.25),
    Interaction("R02", "R08", "amplified", +0.25),
    Interaction("R04", "R13", "mixed", +0.5),  # net floored to +0.5
    Interaction("R04", "R15", "nullified", 0.0),  # already guarded in R04
    Interaction("R04", "R19", "mixed", +0.25),  # net floored to +0.25
    Interaction("R02", "R09", "mixed", 0.0),  # sum floored to 0
    Interaction("R06", "R14", "mixed", 0.0),  # net floored to 0
    Interaction("R04", "R16", "mixed", +0.25),
    Interaction("R06", "R11", "mixed", -0.25),
    Interaction("R03", "R10", "mixed", 0.5),  # sum × 0.5
    Interaction("R09", "R08", "nullified", 0.0),  # kartari bonus nullified
    Interaction("R15", "R04", "nullified", 0.0),  # already handled by R04
    Interaction("R11", "R06", "contextual", 0.0),  # check dasha context
    Interaction("R04", "R22", "contextual", 0.0),  # R22 modifier applies as-is
    Interaction("R17", "R04", "amplified", +0.25),
    Interaction("R19", "R04", "contextual", 0.0),  # same as R04+R19
    Interaction("R15", "R21", "contextual", -1.0),  # penalty reduced
    Interaction("R15", "R20", "contextual", -1.5),  # partially mitigated
    Interaction("R04", "R05", "amplified", +0.5),
    Interaction("R09", "R12", "neg_amplified", -0.5),
    Interaction("R11", "R15", "neg_amplified", -1.0),
    Interaction("R02", "R06", "amplified", +0.5),  # YK only
    Interaction("R04", "R06", "amplified", +0.25),
    Interaction("R09", "R11", "neg_amplified", -0.5),
    Interaction("R13", "R15", "neg_amplified", -1.0),
    Interaction("R03", "R07", "amplified", +0.25),
    Interaction("R10", "R14", "neg_amplified", -0.5),
]


def apply_rule_interactions(fired: set[str], scores: dict[str, float]) -> float:
    """
    fired  = set of rule codes that triggered (score != 0)
    scores = {rule_code: contribution}
    Returns the net interaction modifier to add to the raw house score.
    """
    modifier = 0.0
    for ix in _INTERACTIONS:
        if ix.rule_a not in fired or ix.rule_b not in fired:
            continue
        sa = scores.get(ix.rule_a, 0.0)
        sb = scores.get(ix.rule_b, 0.0)

        if ix.kind == "amplified":
            modifier += ix.modifier
        elif ix.kind == "neg_amplified":
            modifier += ix.modifier
        elif ix.kind == "mixed":
            combined = sa + sb
            if ix.modifier == 0.5 and ix.rule_a == "R03":
                # R03+R10: sum × 0.5
                modifier += combined * 0.5 - combined
            elif ix.modifier >= 0:
                modifier += max(ix.modifier, combined) - combined
            else:
                modifier += max(ix.modifier, combined) - combined
        elif ix.kind == "nullified":
            pass  # already handled in R04 guard
        elif ix.kind == "contextual":
            if ix.modifier != 0:
                modifier += ix.modifier

    return modifier
