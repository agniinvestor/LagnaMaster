"""
src/calculations/argala.py — LagnaMaster Session 31

Jaimini Argala (intervention) and Virodhargala (counter-intervention) system.

Argala models how planets in specific houses FROM a reference point
either support (argala) or obstruct (virodhargala) that reference point.

Primary argala houses (from reference): H2, H4, H11
  Secondary argala: H5 (some traditions include)
Counter-argala (virodha): H12 opposes H2-argala
                           H10 opposes H4-argala
                           H3  opposes H11-argala

Arudha Lagna (AL): the mirror image of the lagna —
  how the world PERCEIVES the native (reputation, social position).
  Formula: count from lagna lord's position back to lagna.

Public API
----------
    compute_argala(chart, reference_house) -> ArgalaResult
    compute_arudha_lagna(chart) -> ArudhaResult
"""

from __future__ import annotations
from dataclasses import dataclass

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
_SIGN_LORD = {
    0: "Mars",
    1: "Venus",
    2: "Mercury",
    3: "Moon",
    4: "Sun",
    5: "Mercury",
    6: "Venus",
    7: "Mars",
    8: "Jupiter",
    9: "Saturn",
    10: "Saturn",
    11: "Jupiter",
}
_NAT_BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


@dataclass
class ArgalaEntry:
    house_from_reference: int  # 2, 4, 5, 11
    argala_type: str  # "primary" or "secondary"
    planets: list[str]
    nature: str  # "benefic_argala" / "malefic_argala" / "mixed"
    is_obstructed: bool  # True if virodhargala cancels it
    obstruction_planets: list[str]
    net_effect: str  # "supports" / "obstructs" / "cancelled" / "neutral"


@dataclass
class ArgalaResult:
    reference_house: int
    reference_sign: str
    entries: list[ArgalaEntry]
    net_argala_score: float  # positive = net support, negative = net obstruction
    summary: str


def compute_argala(chart, reference_house: int = 1) -> ArgalaResult:
    """Compute argala on a reference house (default: H1 = Lagna)."""
    lsi = chart.lagna_sign_index
    ref_si = (lsi + reference_house - 1) % 12

    # Build sign->planets map
    sign_planets: dict[int, list[str]] = {i: [] for i in range(12)}
    for p, pos in chart.planets.items():
        sign_planets[pos.sign_index].append(p)

    def house_from_ref(h: int) -> int:
        """Sign index that is h houses from reference."""
        return (ref_si + h - 1) % 12

    entries = []
    net_score = 0.0

    for argala_h, virodha_h, atype in [
        (2, 12, "primary"),
        (4, 10, "primary"),
        (11, 3, "primary"),
        (5, 9, "secondary"),
    ]:
        argala_si = house_from_ref(argala_h)
        virodha_si = house_from_ref(virodha_h)

        arg_planets = sign_planets.get(argala_si, [])
        vir_planets = sign_planets.get(virodha_si, [])

        if not arg_planets and not vir_planets:
            continue

        benefics = [p for p in arg_planets if p in _NAT_BENEFIC]
        malefics = [p for p in arg_planets if p in _NAT_MALEFIC]
        vir_count = len(vir_planets)
        arg_count = len(arg_planets)

        is_obstructed = vir_count >= arg_count and bool(vir_planets)

        if benefics and not malefics:
            nature = "benefic_argala"
            if not is_obstructed:
                net_score += len(benefics) * 0.5
        elif malefics and not benefics:
            nature = "malefic_argala"
            if not is_obstructed:
                net_score -= len(malefics) * 0.5
        else:
            nature = "mixed"

        if is_obstructed:
            net_effect = "cancelled"
        elif nature == "benefic_argala":
            net_effect = "supports"
        elif nature == "malefic_argala":
            net_effect = "obstructs"
        else:
            net_effect = "neutral"

        entries.append(
            ArgalaEntry(
                house_from_reference=argala_h,
                argala_type=atype,
                planets=arg_planets,  # noqa: F841
                nature=nature,
                is_obstructed=is_obstructed,
                obstruction_planets=vir_planets,
                net_effect=net_effect,
            )
        )

    summary = (
        f"Net argala on H{reference_house}: "
        f"{'supportive' if net_score > 0 else 'obstructive' if net_score < 0 else 'neutral'} "
        f"({net_score:+.1f})"
    )

    return ArgalaResult(
        reference_house=reference_house,
        reference_sign=_SIGNS[ref_si],
        entries=entries,
        net_argala_score=round(net_score, 2),
        summary=summary,
    )


@dataclass
class ArudhaResult:
    arudha_lagna_sign: str
    arudha_lagna_sign_index: int
    lagna_lord: str
    lagna_lord_sign: str
    lagna_lord_sign_index: int
    malefics_on_al: list[str]  # planets in AL sign
    al_condition: str  # "Strong" / "Afflicted" / "Mixed" / "Neutral"
    pressure_note: str


def compute_arudha_lagna(chart) -> ArudhaResult:
    """
    Compute the Arudha Lagna (AL) — mirror of Lagna.

    Method (Parashari):
      1. Find Lagna lord (L) and its sign
      2. Count from Lagna to L's sign: that distance = D
      3. Count D signs forward from L's sign → that is the AL
      Exception: if AL falls on Lagna sign or 7th from Lagna, move 10 signs forward.
    """
    lsi = chart.lagna_sign_index
    lagna_lord = _SIGN_LORD[lsi]
    ll_pos = chart.planets.get(lagna_lord)
    if ll_pos is None:
        ll_si = lsi  # fallback
    else:
        ll_si = ll_pos.sign_index

    # Distance from Lagna to lagna lord's sign (1-based count)
    dist = (ll_si - lsi) % 12 + 1  # 1..12
    # AL sign = dist signs from lagna lord's sign
    al_si = (ll_si + dist - 1) % 12

    # Exception rules
    if al_si == lsi or al_si == (lsi + 6) % 12:
        al_si = (al_si + 9) % 12  # move 10 signs forward (= +9 in 0-based)

    # Planets in AL sign
    al_planets = [p for p, pos in chart.planets.items() if pos.sign_index == al_si]
    malefics_on_al = [p for p in al_planets if p in _NAT_MALEFIC]
    benefics_on_al = [p for p in al_planets if p in _NAT_BENEFIC]

    if malefics_on_al and not benefics_on_al:
        condition = "Afflicted"
        note = f"AL afflicted by {malefics_on_al} — social/reputational pressure"
    elif benefics_on_al and not malefics_on_al:
        condition = "Strong"
        note = "AL supported by benefics — positive public perception"
    elif malefics_on_al and benefics_on_al:
        condition = "Mixed"
        note = "AL has mixed influence — variable public standing"
    else:
        condition = "Neutral"
        note = "AL unoccupied — moderate public visibility"

    return ArudhaResult(
        arudha_lagna_sign=_SIGNS[al_si],
        arudha_lagna_sign_index=al_si,
        lagna_lord=lagna_lord,
        lagna_lord_sign=_SIGNS[ll_si],
        lagna_lord_sign_index=ll_si,
        malefics_on_al=malefics_on_al,
        al_condition=condition,
        pressure_note=note,
    )
