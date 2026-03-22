"""
src/calculations/drekkana_variants.py
Three Drekkana computation methods — Parasara, Jagannatha, Somanatha.
Session 170 (Audit VI-B).

The D3 Drekkana has THREE different valid computation methods in classical texts,
each used for a different purpose:
  - Parasara: sibling analysis (default in Parashari)
  - Jagannatha: spirituality, deeper karma
  - Somanatha: physical constitution, vitality

Sources:
  Sanjay Rath · Varga Chakra Ch.3 (all three systems)
  PVRNR · BPHS Ch.6 (Parasara method — standard)
"""

from __future__ import annotations

_SIGN_NAMES = [
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


def parasara_drekkana(longitude: float) -> int:
    """
    Parasara Drekkana (D3) — standard Parashari method.
    1st drekkana (0°-10°): same sign
    2nd drekkana (10°-20°): 5th sign from natal sign
    3rd drekkana (20°-30°): 9th sign from natal sign

    Source: PVRNR · BPHS Ch.6; standard Parashari practice
    Use for: siblings, courage, vitality, longevity hints
    """
    lon = longitude % 360
    sign = int(lon / 30)
    deg_in_sign = lon % 30
    drekkana_part = int(deg_in_sign / 10)  # 0, 1, or 2

    if drekkana_part == 0:
        return sign
    elif drekkana_part == 1:
        return (sign + 4) % 12  # 5th sign
    else:
        return (sign + 8) % 12  # 9th sign


def jagannatha_drekkana(longitude: float) -> int:
    """
    Jagannatha Drekkana — spirituality and deeper karma.
    Each drekkana follows its own progression based on planetary lords.

    The sequence for each sign's three drekkanas:
    - Movable signs (Aries=0, Cancer=3, Libra=6, Cap=9):
        1st→Aries(0), 2nd→Taurus(1), 3rd→Gemini(2) ... (sequential from Aries)
    - Fixed signs (Taurus=1, Leo=4, Scorpio=7, Aqu=10):
        1st→Leo(4), 2nd→Virgo(5), 3rd→Libra(6) ... (sequential from Leo)
    - Dual signs (Gemini=2, Virgo=5, Sag=8, Pisces=11):
        1st→Sag(8), 2nd→Cap(9), 3rd→Aquarius(10) ... (sequential from Sag)

    Source: Sanjay Rath · Varga Chakra Ch.3
    Use for: spiritual matters, deities, deeper karma indicators
    """
    lon = longitude % 360
    sign = int(lon / 30)
    deg_in_sign = lon % 30
    part = int(deg_in_sign / 10)  # 0, 1, or 2

    _MOVABLE = {0, 3, 6, 9}
    _FIXED = {1, 4, 7, 10}

    if sign in _MOVABLE:
        base = 0  # Aries
    elif sign in _FIXED:
        base = 4  # Leo
    else:
        base = 8  # Sagittarius

    return (base + part) % 12


def somanatha_drekkana(longitude: float) -> int:
    """
    Somanatha Drekkana — physical constitution, vitality, body analysis.
    Computed using the following rule:
    - Odd signs: 1st→same sign, 2nd→next sign, 3rd→sign after that
    - Even signs: 1st→same sign, 2nd→preceding sign, 3rd→sign before that

    Source: Sanjay Rath · Varga Chakra Ch.3
    Use for: physical constitution, sports ability, bodily features
    """
    lon = longitude % 360
    sign = int(lon / 30)
    deg_in_sign = lon % 30
    part = int(deg_in_sign / 10)  # 0, 1, or 2

    is_odd = sign % 2 == 0  # 0-indexed: Aries(0)=odd per classical convention

    if part == 0:
        return sign
    elif is_odd:
        return (sign + part) % 12  # forward
    else:
        return (sign - part) % 12  # backward


def drekkana_sign(longitude: float, method: str = "parasara") -> int:
    """
    Compute D3 Drekkana sign using specified method.

    Args:
        longitude: sidereal longitude (0-360°)
        method: "parasara" (default), "jagannatha", or "somanatha"

    Returns: sign index (0-11)

    Source: Sanjay Rath · Varga Chakra Ch.3
    """
    methods = {
        "parasara": parasara_drekkana,
        "jagannatha": jagannatha_drekkana,
        "somanatha": somanatha_drekkana,
    }
    fn = methods.get(method.lower(), parasara_drekkana)
    return fn(longitude)


def all_drekkana_signs(longitude: float) -> dict[str, int]:
    """
    Compute D3 sign in all three Drekkana systems.
    Returns dict with method name → sign index.
    """
    return {
        "parasara": parasara_drekkana(longitude),
        "jagannatha": jagannatha_drekkana(longitude),
        "somanatha": somanatha_drekkana(longitude),
    }


def drekkana_chart_positions(chart, method: str = "parasara") -> dict[str, dict]:
    """
    Compute Drekkana positions for all planets using specified method.

    Returns: {planet: {sign_index, sign_name, method}}
    """
    result = {}
    for planet, pd in chart.planets.items():
        si = drekkana_sign(pd.longitude, method)
        result[planet] = {
            "sign_index": si,
            "sign_name": _SIGN_NAMES[si],
            "method": method,
        }
    return result
