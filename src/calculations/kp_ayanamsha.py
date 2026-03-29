"""
src/calculations/kp_ayanamsha.py — KP Ayanamsha Compliance (S212 / G06)

GUARDRAIL G06: KP (Krishnamurti Paddhati) school requires the Krishnamurti
ayanamsha. Using Lahiri with KP produces incorrect sub-lord tables because
the KP sub-lord boundaries were calibrated against the Krishnamurti value.

This module provides:
  - get_kp_ayanamsha()     — returns the required ayanamsha name
  - validate_kp_chart()    — checks a chart for G06 compliance
  - compute_kp_chart()     — compute_chart() wrapper defaulting to krishnamurti

Source: K.S. Krishnamurti, "Krishnamurti Padhdhati" Vol.1 Ch.1 — the sub-lord
table was derived using the Krishnamurti ayanamsha specifically.

Public API
----------
  KP_AYANAMSHA         Constant: "krishnamurti"
  get_kp_ayanamsha()   Returns KP_AYANAMSHA
  validate_kp_chart()  Returns compliance dict with g06_compliant bool
  compute_kp_chart()   compute_chart wrapper with ayanamsha="krishnamurti"
"""

from __future__ import annotations

KP_AYANAMSHA: str = "krishnamurti"


def get_kp_ayanamsha() -> str:
    """Return the ayanamsha name required for KP calculations."""
    return KP_AYANAMSHA


def validate_kp_chart(chart) -> dict:
    """
    Validate that a chart uses the correct ayanamsha for KP analysis.

    Args:
        chart: BirthChart with ayanamsha_name attribute

    Returns:
        dict with keys:
          g06_compliant (bool)  — True if Krishnamurti ayanamsha
          ayanamsha (str)       — actual ayanamsha name used
          warning (str)         — empty if compliant; G06 warning if not
    """
    actual = getattr(chart, "ayanamsha_name", "unknown").lower()
    compliant = actual == KP_AYANAMSHA
    warning = ""
    if not compliant:
        warning = (
            f"G06 VIOLATION: KP school requires krishnamurti ayanamsha, "
            f"but chart uses '{actual}'. "
            f"KP sub-lord tables are calibrated for krishnamurti only. "
            f"Use compute_kp_chart() or pass ayanamsha='krishnamurti' to compute_chart()."
        )
    return {
        "g06_compliant": compliant,
        "ayanamsha": actual,
        "warning": warning,
    }


def compute_kp_chart(
    year: int,
    month: int,
    day: int,
    hour: float,
    lat: float,
    lon: float,
    tz_offset: float = 5.5,
):
    """
    Compute a BirthChart using the Krishnamurti ayanamsha (G06 compliant).

    This is a convenience wrapper around src.ephemeris.compute_chart
    that defaults to ayanamsha='krishnamurti' for KP analysis.

    Args:
        year, month, day, hour, lat, lon, tz_offset: same as compute_chart
        (Note: tz_offset defaults to 5.5 = IST)

    Returns:
        BirthChart with ayanamsha_name='krishnamurti'
    """
    from src.ephemeris import compute_chart
    return compute_chart(
        year=year, month=month, day=day, hour=hour,
        lat=lat, lon=lon, tz_offset=tz_offset,
        ayanamsha=KP_AYANAMSHA,
    )
