"""
src/calculations/chara_karak.py
=================================
Jaimini Chara Karakas — variable significators ranked by degree within sign.
Source: CALC_CharaKarak (Excel), Jaimini Sutram 1.1.5-7.
"""

from __future__ import annotations
from dataclasses import dataclass
from src.ephemeris import BirthChart

_KARAK_NAMES = [
    "Atmakaraka",     # AK  — soul, life's deepest karmic lesson
    "Amatyakaraka",   # AmK — career/mind, minister to the soul
    "Bhratrikaraka",  # BK  — siblings, courage
    "Matrikaraka",    # MK  — mother, home, happiness
    "Putrakaraka",    # PK  — children, creativity, past-life merit
    "Gnatikaraka",    # GK  — obstacles, rivals, disease
    "Darakaraka",     # DK  — spouse, business partners
]

_KARAK_ABBR = ["AK", "AmK", "BK", "MK", "PK", "GK", "DK"]

_KARAK_SIGNIFICATION = [
    "Soul · life's deepest karmic lesson",
    "Career/mind · profession and intellect",
    "Siblings · courage · co-workers",
    "Mother · home · emotional nourishment",
    "Children · creativity · past-life merit",
    "Obstacles/rivals · enemies · disease · litigation",
    "Spouse · life partner · business partners",
]


@dataclass
class CharaKarak:
    rank: int           # 1=AK (highest degree) … 7=DK (lowest)
    karak_name: str     # e.g. "Atmakaraka"
    abbreviation: str   # e.g. "AK"
    planet: str         # e.g. "Sun"
    degree_in_sign: float
    signification: str


def compute_chara_karakas(chart: BirthChart) -> list[CharaKarak]:
    """
    Rank the 7 classical planets (Sun-Saturn) by degree within sign.
    Highest degree = Atmakaraka. Rahu/Ketu excluded.
    Returns list of 7 CharaKarak objects sorted rank 1→7.
    """
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    ranked = sorted(
        [(name, chart.planets[name].degree_in_sign) for name in classical if name in chart.planets],
        key=lambda x: x[1],
        reverse=True,   # highest degree first = AK
    )

    result = []
    for rank, (planet, degree) in enumerate(ranked, start=1):
        result.append(CharaKarak(
            rank=rank,
            karak_name=_KARAK_NAMES[rank - 1],
            abbreviation=_KARAK_ABBR[rank - 1],
            planet=planet,
            degree_in_sign=degree,
            signification=_KARAK_SIGNIFICATION[rank - 1],
        ))
    return result
