"""Jaimini Chara Dasha — sign-based predictive cycle (Session 14)."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, timedelta

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
_MAIN_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ODD_SIGNS = {0, 2, 4, 6, 8, 10}


@dataclass
class CharaDashaEntry:
    sign: str
    sign_index: int
    start: date
    end: date
    years: float
    planets_in_sign: list = field(default_factory=list)
    is_current: bool = False


def _sld(si, chart):
    lord = _SIGN_LORD[si]
    lp = chart.planets.get(lord)
    if lp is None:
        return 1
    return max(1, (lp.sign_index - si) % 12)


def _dy(si, chart):
    ph = [
        p
        for p in _MAIN_PLANETS
        if chart.planets.get(p) and chart.planets[p].sign_index == si
    ]
    return max(1, min(12, len(ph) + _sld(si, chart)))


def _pis(si, chart):
    return [
        p
        for p in _MAIN_PLANETS
        if chart.planets.get(p) and chart.planets[p].sign_index == si
    ]


def _atmakaraka(chart):
    return max(
        _MAIN_PLANETS,
        key=lambda p: chart.planets[p].degree_in_sign if chart.planets.get(p) else -1,
    )


def _balance(lsi, chart, ty):
    ak = _atmakaraka(chart)
    ap = chart.planets.get(ak)
    if ap is None:
        return ty * 0.5
    return max(0.5, (1.0 - ap.degree_in_sign / 30.0) * ty)


def _ay(d, years):
    return d + timedelta(days=int(years * 365.25))


def compute_chara_dasha(chart, birth_date: date) -> list:
    lsi = chart.lagna_sign_index
    seq = (
        [(lsi + i) % 12 for i in range(12)]
        if lsi in _ODD_SIGNS
        else [(lsi - i) % 12 for i in range(12)]
    )
    bal = _balance(lsi, chart, _dy(seq[0], chart))
    entries = []
    cd = birth_date
    for i, si in enumerate(seq):
        yrs = bal if i == 0 else _dy(si, chart)
        end = _ay(cd, yrs)
        entries.append(
            CharaDashaEntry(
                _SIGN_NAMES[si], si, cd, end, round(yrs, 4), _pis(si, chart)
            )
        )
        cd = end
    return entries


def current_chara_dasha(dashas, on_date=None):
    today = on_date or date.today()
    for e in dashas:
        if e.start <= today < e.end:
            e.is_current = True
            return e
    return dashas[-1]


def atmakaraka_sign(chart):
    ak = _atmakaraka(chart)
    pos = chart.planets.get(ak)
    return ak, (pos.sign if pos else "Unknown")
