"""
tests/test_s194_conditional_weights.py — S194: Conditional weight functions

Verifies that W(WeightContext) produces classically-grounded, context-aware
weights for the scoring engine.

Classical sources:
  PVRNR · BPHS Ch.34 (Yogakaraka — rules Kendra AND Trikona simultaneously)
  V.K. Choudhry · Systems Approach Ch.3 (functional dignity primacy)
  Phaladeepika Ch.3 v.5-12 (functional benefic/malefic house effects)
  BPHS Ch.11 (Kendra/Trikona are highest in promise)
  GUARDRAIL G06: KP school requires Krishnamurti ayanamsha
"""

from __future__ import annotations


# ─────────────────────────────────────────────────────────────
# 1. WeightContext dataclass fields
# ─────────────────────────────────────────────────────────────


def test_weight_context_fields():
    """WeightContext must expose all required fields."""
    from src.calculations.conditional_weights import WeightContext

    ctx = WeightContext(
        planet="Jupiter",
        house=9,
        lagna_sign=0,
        functional_role="benefic",
        rule_id="R02",
        school="parashari",
        base_weight=1.0,
    )

    assert ctx.planet == "Jupiter"
    assert ctx.house == 9
    assert ctx.lagna_sign == 0
    assert ctx.functional_role == "benefic"
    assert ctx.rule_id == "R02"
    assert ctx.school == "parashari"
    assert ctx.base_weight == 1.0
    assert ctx.ayanamsha == "lahiri"  # default


# ─────────────────────────────────────────────────────────────
# 2. Yogakaraka amplification
# ─────────────────────────────────────────────────────────────


def test_yogakaraka_amplification_parashari():
    """Yogakaraka planet must amplify positive rule weight × 1.5 (Parashari)."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Saturn",
        house=10,
        lagna_sign=1,  # Taurus — Saturn is yogakaraka
        functional_role="yogakaraka",
        rule_id="R04",
        school="parashari",
        base_weight=2.0,
    )
    result = W(ctx)
    assert result == 2.0 * 1.5, f"Expected 3.0, got {result}"


def test_yogakaraka_amplification_jaimini():
    """Yogakaraka planet multiplier is 1.25 in Jaimini school."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Venus",
        house=5,
        lagna_sign=1,  # Taurus — Venus is yogakaraka (Kendra lord H7 + Trikona lord H5? No — for Capricorn/Aquarius)
        functional_role="yogakaraka",
        rule_id="R02",
        school="jaimini",
        base_weight=1.0,
    )
    result = W(ctx)
    assert result == 1.0 * 1.25, f"Expected 1.25, got {result}"


# ─────────────────────────────────────────────────────────────
# 3. Functional benefic + positive rule amplified
# ─────────────────────────────────────────────────────────────


def test_functional_benefic_amplifies_positive_rule():
    """Functional benefic planet in positive rule: W > base_weight."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Jupiter",
        house=1,
        lagna_sign=0,
        functional_role="benefic",
        rule_id="R01",
        school="parashari",
        base_weight=0.5,
    )
    result = W(ctx)
    assert result > ctx.base_weight, (
        f"Functional benefic should amplify positive rule; got W={result} <= base={ctx.base_weight}"
    )


# ─────────────────────────────────────────────────────────────
# 4. Functional malefic + negative rule amplified (more negative)
# ─────────────────────────────────────────────────────────────


def test_functional_malefic_amplifies_negative_rule():
    """Functional malefic planet in negative rule: W < base_weight (more negative)."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Saturn",
        house=8,
        lagna_sign=0,
        functional_role="malefic",
        rule_id="R09",
        school="parashari",
        base_weight=-1.0,
    )
    result = W(ctx)
    assert result < ctx.base_weight, (
        f"Functional malefic should amplify negative rule; got W={result} >= base={ctx.base_weight}"
    )


# ─────────────────────────────────────────────────────────────
# 5. Role mismatch dampens weight
# ─────────────────────────────────────────────────────────────


def test_role_mismatch_dampens_benefic_in_negative_rule():
    """Functional benefic planet mitigates a negative rule: |W| < |base_weight|."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Jupiter",
        house=6,
        lagna_sign=0,
        functional_role="benefic",
        rule_id="R11",
        school="parashari",
        base_weight=-1.25,
    )
    result = W(ctx)
    assert abs(result) < abs(ctx.base_weight), (
        f"Benefic should dampen affliction; got |W|={abs(result)} >= |base|={abs(ctx.base_weight)}"
    )


def test_role_mismatch_dampens_malefic_in_positive_rule():
    """Functional malefic planet reduces a positive rule benefit: W < base_weight."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Mars",
        house=5,
        lagna_sign=0,
        functional_role="malefic",
        rule_id="R02",
        school="parashari",
        base_weight=1.0,
    )
    result = W(ctx)
    assert result < ctx.base_weight, (
        f"Malefic should dampen positive rule; got W={result} >= base={ctx.base_weight}"
    )


# ─────────────────────────────────────────────────────────────
# 6. House-type modifiers
# ─────────────────────────────────────────────────────────────


def test_kendra_house_amplifies_positive_weight():
    """Kendra house (H1/H4/H7/H10) amplifies a positive rule vs a neutral house."""
    from src.calculations.conditional_weights import W, WeightContext

    kendra_ctx = WeightContext(
        planet="Jupiter",
        house=10,  # kendra
        lagna_sign=0,
        functional_role="neutral",
        rule_id="R01",
        school="parashari",
        base_weight=0.5,
    )
    neutral_ctx = WeightContext(
        planet="Jupiter",
        house=3,  # neutral
        lagna_sign=0,
        functional_role="neutral",
        rule_id="R01",
        school="parashari",
        base_weight=0.5,
    )
    assert W(kendra_ctx) > W(neutral_ctx), (
        "Kendra house should produce higher positive weight than neutral house"
    )


def test_dusthana_amplifies_negative_weight():
    """Dusthana house (H6/H8/H12) makes negative rules more negative."""
    from src.calculations.conditional_weights import W, WeightContext

    dusthana_ctx = WeightContext(
        planet="Saturn",
        house=8,  # dusthana
        lagna_sign=0,
        functional_role="neutral",
        rule_id="R09",
        school="parashari",
        base_weight=-1.0,
    )
    kendra_ctx = WeightContext(
        planet="Saturn",
        house=1,  # kendra
        lagna_sign=0,
        functional_role="neutral",
        rule_id="R09",
        school="parashari",
        base_weight=-1.0,
    )
    assert W(dusthana_ctx) < W(kendra_ctx), (
        "Dusthana house should produce more negative weight than kendra"
    )


# ─────────────────────────────────────────────────────────────
# 7. Neutral role passes through base weight (with possible house modifier only)
# ─────────────────────────────────────────────────────────────


def test_neutral_role_no_role_modifier():
    """Neutral planet in non-kendra/dusthana house: W == base_weight (no role mod)."""
    from src.calculations.conditional_weights import W, WeightContext

    ctx = WeightContext(
        planet="Mercury",
        house=3,   # neutral house (upachaya, not kendra/dusthana)
        lagna_sign=0,
        functional_role="neutral",
        rule_id="R01",
        school="parashari",
        base_weight=0.5,
    )
    result = W(ctx)
    assert result == ctx.base_weight, (
        f"Neutral role in neutral house should pass through; got {result} != {ctx.base_weight}"
    )


# ─────────────────────────────────────────────────────────────
# 8. G06: KP school ayanamsha compliance
# ─────────────────────────────────────────────────────────────


def test_g06_kp_lahiri_not_compliant():
    """KP school with Lahiri ayanamsha must flag g06_compliant=False (G06)."""
    from src.calculations.conditional_weights import WeightContext

    ctx = WeightContext(
        planet="Moon",
        house=2,
        lagna_sign=3,
        functional_role="neutral",
        rule_id="R03",
        school="kp",
        base_weight=0.75,
        ayanamsha="lahiri",
    )
    assert ctx.g06_compliant is False, (
        "KP school with Lahiri ayanamsha should be G06 non-compliant"
    )


def test_g06_kp_krishnamurti_compliant():
    """KP school with Krishnamurti ayanamsha must flag g06_compliant=True (G06)."""
    from src.calculations.conditional_weights import WeightContext

    ctx = WeightContext(
        planet="Moon",
        house=2,
        lagna_sign=3,
        functional_role="neutral",
        rule_id="R03",
        school="kp",
        base_weight=0.75,
        ayanamsha="krishnamurti",
    )
    assert ctx.g06_compliant is True


def test_g06_parashari_always_compliant():
    """Parashari school is always G06-compliant (no Krishnamurti requirement)."""
    from src.calculations.conditional_weights import WeightContext

    ctx = WeightContext(
        planet="Sun",
        house=1,
        lagna_sign=0,
        functional_role="malefic",
        rule_id="R04",
        school="parashari",
        base_weight=2.0,
    )
    assert ctx.g06_compliant is True
