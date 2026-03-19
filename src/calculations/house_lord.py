"""
src/calculations/house_lord.py
================================
House (Bhava) assignments and Bhavesh (house lord) mapping.
Source: CALC_BhaveshMap, REF_Zodiac row 7 (sign lords).
"""

from __future__ import annotations
from dataclasses import dataclass
from src.ephemeris import BirthChart, SIGNS


# Classical sign lords (index 0=Aries…11=Pisces)
_SIGN_LORD = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars",  "Jupiter", "Saturn", "Saturn", "Jupiter",
]

def sign_lord(sign_idx: int) -> str:
    return _SIGN_LORD[sign_idx % 12]


@dataclass
class HouseMap:
    """Maps each house number to its sign and lord for a given chart."""
    lagna_sign_idx: int
    # house_sign[i] = sign_index of house i+1 (i=0 → house 1)
    house_sign: list[int]        # length 12
    house_lord: list[str]        # length 12
    # planet_house[planet_name] = house number (1-12)
    planet_house: dict[str, int]


def compute_house_map(chart: BirthChart) -> HouseMap:
    """
    Compute whole-sign house map.
    In whole-sign: house 1 = Lagna sign, house 2 = next sign, etc.
    """
    lagna_idx = chart.lagna_sign_index
    house_sign = [(lagna_idx + h) % 12 for h in range(12)]
    house_lord_list = [sign_lord(s) for s in house_sign]

    planet_house = {}
    for name, p in chart.planets.items():
        # House of planet = how many signs ahead of Lagna (1-indexed)
        house_num = (p.sign_index - lagna_idx) % 12 + 1
        planet_house[name] = house_num

    return HouseMap(
        lagna_sign_idx=lagna_idx,
        house_sign=house_sign,
        house_lord=house_lord_list,
        planet_house=planet_house,
    )


def is_kendra(house: int) -> bool:
    return house in (1, 4, 7, 10)

def is_trikona(house: int) -> bool:
    return house in (1, 5, 9)

def is_dusthana(house: int) -> bool:
    return house in (6, 8, 12)

def is_upachaya(house: int) -> bool:
    return house in (3, 6, 10, 11)
