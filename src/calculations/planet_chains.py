"""
src/calculations/planet_chains.py — Session 67

Multi-planet interaction chains (GPT Gap 4).

A. Stellium dynamics — 3+ planets in same sign
B. Dispositor chains — planet A is in sign owned by planet B which is in sign
   owned by planet C... chain terminates at own sign (final dispositor)
C. Mutual reception — two planets each in other's sign
D. Multi-planet affliction clusters

Public API
----------
  compute_stelliums(chart) -> list[Stellium]
  compute_dispositor_chain(planet, chart) -> DispositorChain
  compute_all_dispositor_chains(chart) -> dict[str, DispositorChain]
  compute_mutual_receptions(chart) -> list[MutualReception]
"""

from __future__ import annotations
from dataclasses import dataclass

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
_NAT_BENEF = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEF = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


@dataclass
class Stellium:
    sign_index: int
    sign_name: str
    planets: list[str]
    benefic_count: int
    malefic_count: int
    nature: str  # "Benefic"/"Malefic"/"Mixed"
    house: int
    interpretation: str


@dataclass
class DispositorChain:
    start_planet: str
    chain: list[str]  # [start, dispositor1, dispositor2, ..., final]
    final_dispositor: str  # planet in own sign (chain terminus)
    chain_length: int
    is_self_disposed: bool  # planet in own sign
    is_mutual: bool  # two-planet mutual reception
    interpretation: str


@dataclass
class MutualReception:
    planet1: str
    planet2: str
    sign1_index: int
    sign2_index: int
    house1: int
    house2: int
    strength: str  # "Strong" (own+own) / "Partial"


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


def compute_stelliums(chart) -> list[Stellium]:
    """Find all signs with 3+ planets."""
    from src.calculations.house_lord import compute_house_map

    compute_house_map(chart)

    # Group planets by sign
    by_sign: dict[int, list[str]] = {}
    for planet, pos in chart.planets.items():
        si = pos.sign_index
        by_sign.setdefault(si, []).append(planet)

    stelliums = []
    for si, planets in by_sign.items():
        if len(planets) < 3:
            continue
        bens = [p for p in planets if p in _NAT_BENEF]
        mals = [p for p in planets if p in _NAT_MALEF]
        if len(bens) > len(mals):
            nature = "Benefic"
        elif len(mals) > len(bens):
            nature = "Malefic"
        else:
            nature = "Mixed"

        # House of this sign
        lagna_si = chart.lagna_sign_index
        house = (si - lagna_si) % 12 + 1

        interp = (
            f"{len(planets)}-planet {nature.lower()} stellium in "
            f"{_SIGNS[si]} (H{house}): {planets}. "
            + (
                "Concentrated power, strong house activation."
                if nature == "Benefic"
                else "Multi-planet affliction cluster, challenges to this house."
                if nature == "Malefic"
                else "Mixed results — benefics and malefics compete."
            )
        )

        stelliums.append(
            Stellium(
                sign_index=si,
                sign_name=_SIGNS[si],
                planets=planets,
                benefic_count=len(bens),
                malefic_count=len(mals),
                nature=nature,
                house=house,
                interpretation=interp,
            )
        )

    return stelliums


def compute_dispositor_chain(
    planet: str, chart, visited: set | None = None
) -> DispositorChain:
    """Trace dispositor chain from a planet to final dispositor (own sign)."""
    if visited is None:
        visited = set()
    chain = [planet]
    current = planet
    max_depth = 9

    while len(chain) < max_depth:
        pos = chart.planets.get(current)
        if not pos:
            break
        si = pos.sign_index
        dispositor = _SIGN_LORD[si % 12]

        # Check if current planet is in its own sign (self-disposed)
        _OWN = {
            "Sun": {4},
            "Moon": {3},
            "Mars": {0, 7},
            "Mercury": {2, 5},
            "Jupiter": {8, 11},
            "Venus": {1, 6},
            "Saturn": {9, 10},
        }
        if si in _OWN.get(current, set()):
            # Self-disposed: final dispositor is current
            break

        if dispositor in visited or dispositor == current:
            break  # cycle detected
        visited.add(current)
        chain.append(dispositor)
        current = dispositor

    final = chain[-1]
    is_self = len(chain) == 1

    # Check mutual reception (2-planet chain back to start)
    is_mutual = False
    if len(chain) == 2:
        final_pos = chart.planets.get(final)
        if final_pos:
            final_disp = _SIGN_LORD[final_pos.sign_index % 12]
            is_mutual = final_disp == chain[0]

    if is_self:
        interp = f"{planet} is self-disposed (in own sign) — independent, strong"
    elif is_mutual:
        interp = f"{planet} and {final} are in mutual reception — strong exchange of energies"
    elif len(chain) <= 3:
        interp = f"{planet} → {' → '.join(chain[1:])} (final dispositor: {final})"
    else:
        interp = f"Long chain: {' → '.join(chain)} — {final} governs {planet}'s ultimate results"

    return DispositorChain(
        start_planet=planet,
        chain=chain,
        final_dispositor=final,
        chain_length=len(chain),
        is_self_disposed=is_self,
        is_mutual=is_mutual,
        interpretation=interp,
    )


def compute_all_dispositor_chains(chart) -> dict[str, DispositorChain]:
    planets_9 = [
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "Rahu",
        "Ketu",
    ]
    return {
        p: compute_dispositor_chain(p, chart) for p in planets_9 if p in chart.planets
    }


def compute_mutual_receptions(chart) -> list[MutualReception]:
    """Find all mutual receptions (parivartana yogas)."""
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    ph = hmap.planet_house
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    seen = set()
    receptions = []

    for p1 in planets_7:
        for p2 in planets_7:
            if p1 >= p2 or (p1, p2) in seen:
                continue
            pos1 = chart.planets.get(p1)
            pos2 = chart.planets.get(p2)
            if not pos1 or not pos2:
                continue
            lord1 = _SIGN_LORD[pos1.sign_index % 12]
            lord2 = _SIGN_LORD[pos2.sign_index % 12]
            if lord1 == p2 and lord2 == p1:
                seen.add((p1, p2))
                _OWN = {
                    "Sun": {4},
                    "Moon": {3},
                    "Mars": {0, 7},
                    "Mercury": {2, 5},
                    "Jupiter": {8, 11},
                    "Venus": {1, 6},
                    "Saturn": {9, 10},
                }
                strength = (
                    "Strong"
                    if (
                        pos1.sign_index in _OWN.get(p2, set())
                        and pos2.sign_index in _OWN.get(p1, set())
                    )
                    else "Partial"
                )
                receptions.append(
                    MutualReception(
                        planet1=p1,
                        planet2=p2,
                        sign1_index=pos1.sign_index,
                        sign2_index=pos2.sign_index,
                        house1=ph.get(p1, 0),
                        house2=ph.get(p2, 0),
                        strength=strength,
                    )
                )

    return receptions
