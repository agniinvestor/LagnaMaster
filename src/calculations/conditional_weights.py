"""
src/calculations/conditional_weights.py — Session 194

Conditional weight function W(planet, house, lagna, functional_role).

Replaces the flat static weight tables used in multi_axis_scoring with a
context-aware modifier that encodes classical scoring principles:

  1. Yogakaraka (rules Kendra + Trikona simultaneously) → × YK_MULT
  2. Functional benefic + positive rule → × 1.2   (amplifies promise)
  3. Functional malefic + negative rule → × 1.2   (amplifies affliction)
  4. Role mismatch → × 0.75  (mitigates cross-direction effect)
  5. Kendra/Trikona house + positive rule → × 1.1
  6. Dusthana house + negative rule → × 1.1

GUARDRAIL G06: KP school requires Krishnamurti ayanamsha.
  WeightContext.g06_compliant = True only when school != "kp" OR ayanamsha = "krishnamurti".
  Downstream callers can gate on this before issuing KP predictions.

Public API
----------
  WeightContext                              — dataclass
  W(ctx: WeightContext) -> float             — conditional weight
  build_context(planet, house, lagna_sign,
                functional_role, rule_id,
                school, base_weight,
                ayanamsha) -> WeightContext  — convenience constructor

Classical sources
-----------------
  PVRNR · BPHS Ch.34 (Yogakaraka definition)
  V.K. Choudhry · Systems Approach for Interpreting Horoscopes Ch.3
  Mantreswara · Phaladeepika Ch.3 v.5-12 (functional benefic/malefic effects)
  BPHS Ch.11 Bhava Phala (Kendra/Trikona highest in promise)
  BPHS Ch.37 (Dusthana — 6th/8th/12th house affliction)
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ── School-specific Yogakaraka multipliers (mirrors multi_axis_scoring) ───────
_YK_MULT: dict[str, float] = {
    "parashari": 1.5,
    "kp": 1.5,
    "jaimini": 1.25,
}

# ── House classification sets ─────────────────────────────────────────────────
_KENDRA: frozenset[int] = frozenset({1, 4, 7, 10})
_TRIKONA: frozenset[int] = frozenset({1, 5, 9})
_KENDRA_TRIKONA: frozenset[int] = _KENDRA | _TRIKONA  # H1 is in both
_DUSTHANA: frozenset[int] = frozenset({6, 8, 12})

# ── Role alignment modifier table ─────────────────────────────────────────────
# (functional_role, is_positive_rule) -> multiplier
_ROLE_MOD: dict[tuple[str, bool], float] = {
    ("benefic", True): 1.2,   # benefic enhances positive promise
    ("benefic", False): 0.75,  # benefic mitigates affliction
    ("malefic", True): 0.75,   # malefic dampens positive promise
    ("malefic", False): 1.2,   # malefic amplifies affliction
    # yogakaraka handled separately (returns early with YK_MULT)
    # neutral / maraka / badhaka: no role modifier → 1.0
}


@dataclass
class WeightContext:
    """
    Context for a single conditional weight computation.

    Attributes:
        planet:          Planet name, e.g. "Jupiter"
        house:           Bhava being scored (1–12)
        lagna_sign:      Lagna sign index (0=Aries … 11=Pisces)
        functional_role: One of "benefic", "malefic", "yogakaraka",
                         "neutral", "maraka", "badhaka"
        rule_id:         Rule identifier "R01"–"R23"
        school:          "parashari" | "kp" | "jaimini"
        base_weight:     Raw rule weight from static weight table
        ayanamsha:       Ayanamsha used (G06: KP requires "krishnamurti")
    """

    planet: str
    house: int
    lagna_sign: int
    functional_role: str
    rule_id: str
    school: str
    base_weight: float
    ayanamsha: str = field(default="lahiri")

    @property
    def g06_compliant(self) -> bool:
        """
        G06: KP school requires Krishnamurti ayanamsha.
        Returns True for non-KP schools (no ayanamsha constraint).
        Returns True for KP only when ayanamsha == "krishnamurti".
        """
        if self.school != "kp":
            return True
        return self.ayanamsha == "krishnamurti"


def W(ctx: WeightContext) -> float:
    """
    Compute the context-conditional weight for a rule application.

    Applies classical modifiers in order:
      1. Yogakaraka early-return (× YK_MULT, no further modification)
      2. Role-alignment modifier (benefic/malefic vs rule direction)
      3. House-type modifier (kendra/trikona vs dusthana)

    Zero-weight base_weight is passed through unchanged (rule did not fire).

    Args:
        ctx: WeightContext with all scoring context

    Returns:
        float — adjusted weight (positive or negative, same sign as base_weight)
    """
    w = ctx.base_weight

    # Zero base: rule did not fire — no amplification meaningful
    if w == 0.0:
        return 0.0

    # 1. Yogakaraka: highest functional status — apply multiplier and return
    #    Source: PVRNR BPHS Ch.34; rules both Kendra AND Trikona simultaneously
    if ctx.functional_role == "yogakaraka":
        yk = _YK_MULT.get(ctx.school, 1.5)
        return round(w * yk, 4)

    is_positive_rule = w > 0

    # 2. Role-alignment modifier
    #    Source: Phaladeepika Ch.3 v.5-12; Systems Approach Ch.3
    role_mod = _ROLE_MOD.get((ctx.functional_role, is_positive_rule), 1.0)
    w = w * role_mod

    # 3. House-type modifier
    #    Kendra/Trikona amplify positive promise; Dusthana amplify affliction
    #    Source: BPHS Ch.11 Bhava Phala
    if ctx.house in _KENDRA_TRIKONA and is_positive_rule:
        w *= 1.1
    elif ctx.house in _DUSTHANA and not is_positive_rule:
        w *= 1.1

    return round(w, 4)


def build_context(
    planet: str,
    house: int,
    lagna_sign: int,
    functional_role: str,
    rule_id: str,
    school: str,
    base_weight: float,
    ayanamsha: str = "lahiri",
) -> WeightContext:
    """Convenience constructor for WeightContext."""
    return WeightContext(
        planet=planet,
        house=house,
        lagna_sign=lagna_sign,
        functional_role=functional_role,
        rule_id=rule_id,
        school=school,
        base_weight=base_weight,
        ayanamsha=ayanamsha,
    )
