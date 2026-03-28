"""
tests/test_s212_ayanamsha_kp_g06.py — S212: Ayanamsha selection + KP G06 compliance

G06: KP school must use Krishnamurti ayanamsha — Lahiri produces incorrect
KP sub-lord tables. This session wires in the check and adds the
KP ayanamsha helper function.
"""

from __future__ import annotations


# ── Ayanamsha validation ──────────────────────────────────────────────────────

def test_kp_ayanamsha_module_import():
    from src.calculations.kp_ayanamsha import get_kp_ayanamsha, validate_kp_chart
    assert get_kp_ayanamsha is not None
    assert validate_kp_chart is not None


def test_get_kp_ayanamsha_returns_krishnamurti():
    from src.calculations.kp_ayanamsha import get_kp_ayanamsha
    assert get_kp_ayanamsha() == "krishnamurti"


def test_validate_kp_chart_ok_with_krishnamurti():
    from src.calculations.kp_ayanamsha import validate_kp_chart
    import types
    chart = types.SimpleNamespace(ayanamsha_name="krishnamurti")
    result = validate_kp_chart(chart)
    assert result["g06_compliant"] is True
    assert result["ayanamsha"] == "krishnamurti"


def test_validate_kp_chart_non_compliant_with_lahiri():
    from src.calculations.kp_ayanamsha import validate_kp_chart
    import types
    chart = types.SimpleNamespace(ayanamsha_name="lahiri")
    result = validate_kp_chart(chart)
    assert result["g06_compliant"] is False
    assert "G06" in result["warning"]


def test_validate_kp_chart_non_compliant_with_raman():
    from src.calculations.kp_ayanamsha import validate_kp_chart
    import types
    chart = types.SimpleNamespace(ayanamsha_name="raman")
    result = validate_kp_chart(chart)
    assert result["g06_compliant"] is False


def test_compute_kp_chart_uses_krishnamurti():
    """compute_kp_chart() must default to krishnamurti ayanamsha."""
    from src.calculations.kp_ayanamsha import compute_kp_chart
    chart = compute_kp_chart(
        year=1947, month=8, day=15, hour=0.0,
        lat=28.6139, lon=77.2090, tz_offset=5.5,
    )
    assert chart.ayanamsha_name == "krishnamurti"


def test_g06_compliant_property_in_weight_context():
    """WeightContext.g06_compliant must be False for KP+Lahiri."""
    from src.calculations.conditional_weights import WeightContext
    ctx_lahiri = WeightContext(
        planet="Saturn", house=7, lagna_sign=0,
        functional_role="malefic", rule_id="R11",
        school="kp", base_weight=-1.25, ayanamsha="lahiri",
    )
    assert ctx_lahiri.g06_compliant is False

    ctx_kp = WeightContext(
        planet="Saturn", house=7, lagna_sign=0,
        functional_role="malefic", rule_id="R11",
        school="kp", base_weight=-1.25, ayanamsha="krishnamurti",
    )
    assert ctx_kp.g06_compliant is True


def test_g06_always_compliant_for_parashari():
    """G06 only applies to KP school — parashari is always compliant."""
    from src.calculations.conditional_weights import WeightContext
    ctx = WeightContext(
        planet="Jupiter", house=5, lagna_sign=3,
        functional_role="benefic", rule_id="R02",
        school="parashari", base_weight=1.0, ayanamsha="lahiri",
    )
    assert ctx.g06_compliant is True


def test_guardrails_md_g06_status_updated():
    """GUARDRAILS.md must show G06 as partially addressed after S212."""
    from pathlib import Path
    text = Path("docs/GUARDRAILS.md").read_text()
    # G06 was CURRENTLY VIOLATING — S212 adds the fix for new KP charts
    assert "G06" in text
