"""
src/calculations/narayana_argala.py — Session 54

ND-6: Argala influence on Narayana Dasha activation.
PVRNR Narayana Dasha Ch.5.

For the currently active Narayana Dasha sign, compute which planets
cause Argala (H2/H4/H11 from that sign) and which cause Virodha
(H12/H10/H3). Net Argala modifies the Dasha period's activation weight.

Argala positions (from sign being tested):
  H2  → Dhan Argala      (benefic = strong +; malefic = mixed)
  H4  → Sukha Argala     (benefic = strong +; malefic = mixed)
  H11 → Labha Argala     (benefic = strong +; malefic = mixed)
  H5  → Secondary (Putra Argala, half weight)
Virodha (cancels Argala):
  H12 cancels H2 Argala
  H10 cancels H4 Argala
  H3  cancels H11 Argala
  H9  cancels H5 Argala

Net activation modifier range: −0.5 to +0.5
"""

from __future__ import annotations
from dataclasses import dataclass

_NAT_BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

_ARGALA_HOUSES = {2: 0.5, 4: 0.5, 11: 0.5, 5: 0.25}  # relative strength
_VIRODHA_HOUSES = {12: 2, 10: 4, 3: 11, 9: 5}  # cancels argala from which house


@dataclass
class ArgalaOnSign:
    sign_index: int
    sign_name: str
    argala_planets: list[str]  # benefics causing argala
    malefic_argala: list[str]  # malefics causing argala (mixed)
    virodha_planets: list[str]  # planets in virodha positions
    net_modifier: float  # −0.5 to +0.5
    interpretation: str


def compute_argala_on_sign(sign_index: int, chart) -> ArgalaOnSign:
    """
    Compute Argala/Virodha on a given sign (0-based index).
    Used for Narayana Dasha sign activation modifier.
    """
    _SIGNS = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    sign_name = _SIGNS[sign_index % 12]

    # Count planets in Argala positions relative to this sign
    argala_benefics = []
    argala_malefics = []
    virodha_planets = []

    for planet, pos in chart.planets.items():
        # House number of planet relative to sign (1 = same sign)
        house_from_sign = (pos.sign_index - sign_index) % 12 + 1

        if house_from_sign in _ARGALA_HOUSES:
            if planet in _NAT_BENEFIC:
                argala_benefics.append(planet)
            elif planet in _NAT_MALEFIC:
                argala_malefics.append(planet)

        virodha_cancels = _VIRODHA_HOUSES.get(house_from_sign)
        if virodha_cancels is not None:
            virodha_planets.append(planet)

    # Net modifier calculation
    gross_argala = len(argala_benefics) * 0.15 + len(argala_malefics) * 0.05
    virodha_reduction = min(gross_argala, len(virodha_planets) * 0.10)
    net = round(gross_argala - virodha_reduction, 3)
    net = max(-0.5, min(0.5, net))

    if net > 0.2:
        interp = f"Strong Argala on {sign_name} — period activation enhanced"
    elif net > 0:
        interp = f"Mild Argala on {sign_name} — slight enhancement"
    elif virodha_planets:
        interp = f"Virodha cancels Argala on {sign_name} — neutral activation"
    else:
        interp = f"No Argala on {sign_name} — base activation"

    return ArgalaOnSign(
        sign_index=sign_index,
        sign_name=sign_name,
        argala_planets=argala_benefics,
        malefic_argala=argala_malefics,
        virodha_planets=virodha_planets,
        net_modifier=net,
        interpretation=interp,
    )


def narayana_dasha_argala_modifier(chart, on_date=None) -> float:
    """
    Get the Argala modifier for the currently active Narayana Dasha sign.
    Returns a modifier in range −0.5 to +0.5.
    """
    from datetime import date as _date

    if on_date is None:
        on_date = _date.today()
    try:
        from src.calculations.narayana_dasha import compute_narayana_dasha
        from datetime import date

        bd = getattr(chart, "birth_date", date(1947, 8, 15))
        periods = compute_narayana_dasha(chart, bd)
        current = next(
            (p for p in periods if p.start_date <= on_date < p.end_date), None
        )
        if current:
            result = compute_argala_on_sign(current.sign_index, chart)
            return result.net_modifier
    except Exception:
        pass
    return 0.0
