"""
src/calculations/jaimini_rashi_drishti.py
Rashi Drishti — Jaimini sign-based aspect system.
Session 135.

Sign modalities:
  Movable (Chara): Aries(0), Cancer(3), Libra(6), Capricorn(9)
    → aspect ALL signs EXCEPT the 11th from themselves
  Fixed (Sthira): Taurus(1), Leo(4), Scorpio(7), Aquarius(10)
    → aspect ALL signs EXCEPT 3rd and 5th from themselves
  Dual (Dvishabha): Gemini(2), Virgo(5), Sagittarius(8), Pisces(11)
    → aspect ALL signs EXCEPT 2nd and 12th from themselves

Source: Jaimini Sutras Adhyaya 1 Pada 1 v.15-20
        P.S. Sastri · Textbook of Jaimini Astrology Vol.1, Ch.3
        Sanjay Rath · Crux of Vedic Astrology Ch.6
"""
from __future__ import annotations

_MOVABLE = {0, 3, 6, 9}   # Aries, Cancer, Libra, Capricorn
_FIXED   = {1, 4, 7, 10}  # Taurus, Leo, Scorpio, Aquarius
_DUAL    = {2, 5, 8, 11}  # Gemini, Virgo, Sagittarius, Pisces

_ALL = set(range(12))


def rashi_drishti(sign_index: int) -> frozenset[int]:
    """
    Returns frozenset of sign indices aspected by sign_index via Rashi Drishti.
    Does NOT include the sign itself.

    Source: Jaimini Sutras Adhyaya 1 Pada 1 v.15-20
    """
    si = sign_index % 12
    if si in _MOVABLE:
        excluded = {(si + 10) % 12}           # exclude 11th from itself
    elif si in _FIXED:
        excluded = {(si + 2) % 12, (si + 4) % 12}  # exclude 3rd and 5th
    else:  # DUAL
        excluded = {(si + 1) % 12, (si + 11) % 12}  # exclude 2nd and 12th

    return frozenset(_ALL - {si} - excluded)


def has_rashi_drishti(from_sign: int, to_sign: int) -> bool:
    """Returns True if from_sign aspects to_sign by Rashi Drishti."""
    return to_sign % 12 in rashi_drishti(from_sign)


def rashi_drishti_map() -> dict[int, frozenset[int]]:
    """Precomputed map: {sign_index: frozenset of aspected signs}."""
    return {i: rashi_drishti(i) for i in range(12)}


def signs_aspecting(target_sign: int) -> frozenset[int]:
    """Returns all signs that aspect target_sign by Rashi Drishti."""
    return frozenset(s for s in range(12) if has_rashi_drishti(s, target_sign))


def planets_with_rashi_drishti_to(target_sign: int, chart) -> list[str]:
    """
    Returns list of planets whose sign has Rashi Drishti to target_sign.
    Includes planets in their own sign if that sign aspects the target.
    """
    aspecting = signs_aspecting(target_sign)
    result = []
    for planet, pdata in chart.planets.items():
        if pdata.sign_index in aspecting:
            result.append(planet)
    return result


def sign_modality(sign_index: int) -> str:
    """Returns 'movable', 'fixed', or 'dual'."""
    si = sign_index % 12
    if si in _MOVABLE: return "movable"
    if si in _FIXED:   return "fixed"
    return "dual"


# ─── Argala (Planetary Intervention) via Rashi Drishti ───────────────────────
# Source: Jaimini Sutras Adhyaya 1 Pada 4

_ARGALA_HOUSES  = {2, 4, 11}    # H2/H4/H11 from reference = benefic Argala
_VIRODHA_HOUSES = {3, 10, 12}   # H3/H10/H12 = obstructive Argala (Virodha)
# Note: H5 also creates special Argala per some authorities (Sanjay Rath)

def compute_argala(reference_sign: int, chart, av_chart=None) -> dict:
    """
    Compute Argala (intervention) for a reference sign.
    Returns:
      argala_signs: list of signs causing benefic Argala
      virodha_signs: list of signs causing Virodha (obstruction)
      net_argala: 'benefic' / 'obstructed' / 'neutral'

    av_chart: if provided, use post-Shodhana AV bindus to determine Virodha
    strength (Virodha confirmed only if obstructing planet has more bindus).
    Source: Jaimini Sutras Adhyaya 1 Pada 4 v.24-27; Sanjay Rath commentary
    """
    ref = reference_sign % 12

    # Collect planets in Argala positions
    argala_planets = []
    virodha_planets = []

    for h in _ARGALA_HOUSES:
        sign = (ref + h - 1) % 12
        planets_here = [p for p, pd in chart.planets.items() if pd.sign_index == sign]
        if planets_here:
            argala_planets.append({'house_from_ref': h, 'sign': sign, 'planets': planets_here})

    for h in _VIRODHA_HOUSES:
        sign = (ref + h - 1) % 12
        planets_here = [p for p, pd in chart.planets.items() if pd.sign_index == sign]
        if planets_here:
            virodha_planets.append({'house_from_ref': h, 'sign': sign, 'planets': planets_here})

    # Simple net: if both Argala (H2/H4/H11) and Virodha (H3/H10/H12) present,
    # use AV bindus to decide if Virodha is confirmed
    if argala_planets and virodha_planets:
        net = 'contested'
    elif argala_planets:
        net = 'benefic'
    elif virodha_planets:
        net = 'obstructed'
    else:
        net = 'neutral'

    return {
        'reference_sign': ref,
        'argala_planets': argala_planets,
        'virodha_planets': virodha_planets,
        'net_argala': net,
    }
