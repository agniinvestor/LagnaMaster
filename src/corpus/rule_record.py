"""
src/corpus/rule_record.py — RuleRecord dataclass (S202)

Machine-readable encoding of a classical Jyotish rule.
Each rule maps a classical text citation to a testable, computable predicate.

Public API
----------
  RuleRecord    — one classical rule with metadata and confidence score

Classical sources are cited as: BPHS, Phaladeepika, Brihat Jataka,
Uttara Kalamrita, Jataka Parijata, Sarwarthachintamani, Jaimini Sutras,
Lal Kitab, Chandra Kala Nadi.

Confidence
----------
  1.0  = Direct sutra / verse — exact Sanskrit text available
  0.9  = Translation + commentary — well-established interpretation
  0.8  = Cross-referenced across ≥2 texts
  0.7  = Single text, partial commentary
  0.5  = Traditional teaching, no direct text citation
  0.3  = Inference / interpolation — mark as exploratory
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

SchoolType = Literal["parashari", "kp", "jaimini", "all"]
CategoryType = Literal[
    "house_quality",     # house sign nature, gentle/harsh
    "dignity",           # exaltation, debilitation, own sign, etc.
    "strength",          # shadbala, dig bala, etc.
    "yoga",              # yoga combinations
    "dasha",             # dasha interpretation
    "timing",            # transit, activation
    "pushkara",          # pushkara navamsha / amsha
    "kartari",           # kartari yoga (flanking)
    "combustion",        # combust / cazimi
    "retrograde",        # retrograde behavior
    "karak",             # natural significator
    "ashtakavarga",      # SAV / BAV bindus
    "war",               # graha yuddha
    "special",           # special lagnas, argala, etc.
    "other",
]


@dataclass
class RuleRecord:
    """
    One classical rule in machine-readable form.

    Fields
    ------
    rule_id      Short identifier, e.g. "R01" or "BPHS-11-01"
    source       Classical text, e.g. "BPHS", "Phaladeepika"
    chapter      Chapter/section reference, e.g. "Ch.11" or "Ch.6 v.3"
    school       Jyotish school: parashari, kp, jaimini, or all
    category     Rule category (see CategoryType)
    description  Plain-language statement of the rule
    confidence   0.0–1.0 (see module docstring)
    verse        Optional Sanskrit verse or key phrase
    tags         Free-form tags for search
    implemented  Whether this rule is currently computed by the engine
    engine_ref   Module and function that implements this rule, if any
    """
    rule_id: str
    source: str
    chapter: str
    school: SchoolType
    category: CategoryType
    description: str
    confidence: float
    verse: str = ""
    tags: list[str] = field(default_factory=list)
    implemented: bool = False
    engine_ref: str = ""

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"RuleRecord {self.rule_id}: confidence={self.confidence} must be [0,1]"
            )

    def to_dict(self) -> dict:
        return asdict(self)
