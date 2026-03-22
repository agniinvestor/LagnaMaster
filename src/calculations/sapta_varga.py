"""
src/calculations/sapta_varga.py
================================
Sapta Varga Dignity — Vimshopak Bala — Session 16.

Computes the classical 20-point weighted dignity score for each planet
across the 7 vargas used in Parashari Sapta Varga analysis:
    D1  Rasi         weight 3
    D2  Hora         weight 2
    D3  Drekkana     weight 2
    D7  Saptamsha    weight 1
    D9  Navamsha     weight 5
    D10 Dashamsha    weight 3
    D12 Dvadasamsha  weight 4
                    ──────────
    Total            20

For each planet in each varga, dignity is determined by the sign it
occupies in that division (not by exact degree), then multiplied by a
fractional dignity score:

    Exaltation    (Uchcha)      → 1.000 × weight
    Moolatrikona               → 0.750 × weight
    Own sign      (Swa)        → 0.500 × weight
    Friend sign   (Mitra)      → 0.375 × weight
    Neutral sign  (Sama)       → 0.250 × weight
    Enemy sign    (Shatru)     → 0.125 × weight
    Debilitation  (Neecha)     → 0.000 × weight

Reference: BPHS ch. 45 "Vimshopak Bala".
Rahu/Ketu: treated as having no exaltation/own/debilitation in this
system and are assigned Neutral dignity in every varga (score = 0.25×w).

Public API
----------
    compute_vimshopak(chart: BirthChart) -> VimshopakResult
    vimshopak_grade(score: float) -> str

Data classes
------------
    VargaDignity   — dignity for one planet in one varga
    PlanetVimshopak — full 7-varga row for one planet (+ total score)
    VimshopakResult — all 9 planets + lagna (ascendant)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

# ── varga weights (must sum to 20) ───────────────────────────────────────────

SAPTA_VARGA_WEIGHTS: dict[str, float] = {
    "D1": 3.0,
    "D2": 2.0,
    "D3": 2.0,
    "D7": 1.0,
    "D9": 5.0,
    "D10": 3.0,
    "D12": 4.0,
}
assert abs(sum(SAPTA_VARGA_WEIGHTS.values()) - 20.0) < 1e-9, "Weights must sum to 20"

# ── dignity fraction table ────────────────────────────────────────────────────

_DIGNITY_FRACTION = {
    "Exaltation": 1.000,
    "Moolatrikona": 0.750,
    "OwnSign": 0.500,
    "Friend": 0.375,
    "Neutral": 0.250,
    "Enemy": 0.125,
    "Debilitation": 0.000,
}

# ── planet tables (BPHS standard) ─────────────────────────────────────────────

# sign indices: Ar=0 Ta=1 Ge=2 Cn=3 Le=4 Vi=5 Li=6 Sc=7 Sg=8 Cp=9 Aq=10 Pi=11

_EXALT: dict[str, int] = {
    "Sun": 0,
    "Moon": 1,
    "Mars": 9,
    "Mercury": 5,
    "Jupiter": 3,
    "Venus": 11,
    "Saturn": 6,
}
_DEBIL: dict[str, int] = {
    "Sun": 6,
    "Moon": 7,
    "Mars": 3,
    "Mercury": 11,
    "Jupiter": 9,
    "Venus": 5,
    "Saturn": 0,
}
_OWN: dict[str, set[int]] = {
    "Sun": {4},
    "Moon": {3},
    "Mars": {0, 7},
    "Mercury": {2, 5},
    "Jupiter": {8, 11},
    "Venus": {1, 6},
    "Saturn": {9, 10},
}
_MOOLTRIKONA: dict[str, int] = {
    # Only the sign matters here (degree range irrelevant for varga analysis)
    "Sun": 4,  # Leo
    "Moon": 1,  # Taurus
    "Mars": 0,  # Aries
    "Mercury": 5,  # Virgo
    "Jupiter": 8,  # Sagittarius
    "Venus": 6,  # Libra
    "Saturn": 10,  # Aquarius
}

# Naisargika (permanent) friendship table: True = Friend, None = Neutral, False = Enemy
# Rows = planet, Cols = sign lord encountered (Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn)
# Only used when Rahu/Ketu or a planet encounters another's sign.
_NAI: dict[str, dict[str, str]] = {
    #           Sun     Moon    Mars    Mercury Jupiter Venus   Saturn
    "Sun": {
        "Sun": "F",
        "Moon": "F",
        "Mars": "F",
        "Mercury": "N",
        "Jupiter": "F",
        "Venus": "E",
        "Saturn": "E",
    },
    "Moon": {
        "Sun": "F",
        "Moon": "F",
        "Mars": "N",
        "Mercury": "F",
        "Jupiter": "F",
        "Venus": "F",
        "Saturn": "N",
    },
    "Mars": {
        "Sun": "F",
        "Moon": "N",
        "Mars": "F",
        "Mercury": "E",
        "Jupiter": "F",
        "Venus": "E",
        "Saturn": "N",
    },
    "Mercury": {
        "Sun": "F",
        "Moon": "E",
        "Mars": "E",
        "Mercury": "F",
        "Jupiter": "N",
        "Venus": "F",
        "Saturn": "N",
    },
    "Jupiter": {
        "Sun": "F",
        "Moon": "F",
        "Mars": "F",
        "Mercury": "E",
        "Jupiter": "F",
        "Venus": "E",
        "Saturn": "N",
    },
    "Venus": {
        "Sun": "E",
        "Moon": "N",
        "Mars": "N",
        "Mercury": "F",
        "Jupiter": "N",
        "Venus": "F",
        "Saturn": "F",
    },
    "Saturn": {
        "Sun": "E",
        "Moon": "E",
        "Mars": "N",
        "Mercury": "F",
        "Jupiter": "N",
        "Venus": "F",
        "Saturn": "F",
    },
}

# Sign lords for all 12 signs (Rahu/Ketu have no lordship in Parashari)
_SIGN_LORD: list[str] = [
    "Mars",  # Aries 0
    "Venus",  # Taurus 1
    "Mercury",  # Gemini 2
    "Moon",  # Cancer 3
    "Sun",  # Leo 4
    "Mercury",  # Virgo 5
    "Venus",  # Libra 6
    "Mars",  # Scorpio 7
    "Jupiter",  # Sagittarius 8
    "Saturn",  # Capricorn 9
    "Saturn",  # Aquarius 10
    "Jupiter",  # Pisces 11
]

_PLANETS_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ALL_PLANETS = _PLANETS_7 + ["Rahu", "Ketu"]


# ── dignity determination ─────────────────────────────────────────────────────


def _sign_dignity(planet: str, sign_index: int) -> str:
    """
    Return the dignity label for `planet` placed in `sign_index`.
    Rahu/Ketu always return "Neutral" (no classical exalt/own/debil in Parashari).
    """
    if planet not in _PLANETS_7:
        return "Neutral"

    si = sign_index % 12

    if _EXALT.get(planet) == si:
        return "Exaltation"
    if _DEBIL.get(planet) == si:
        return "Debilitation"
    if _MOOLTRIKONA.get(planet) == si:
        # Only count Moolatrikona if NOT the same as a pure own sign
        # (Sun's Leo is both mooltrikona and own — mooltrikona takes priority)
        return "Moolatrikona"
    if si in _OWN.get(planet, set()):
        return "OwnSign"

    # Friendship with sign lord
    lord = _SIGN_LORD[si]
    if lord == planet:
        return "OwnSign"  # shouldn't normally reach here
    nai = _NAI.get(planet, {}).get(lord, "N")
    if nai == "F":
        return "Friend"
    if nai == "E":
        return "Enemy"
    return "Neutral"


def _dignity_points(planet: str, sign_index: int, weight: float) -> float:
    """Return Vimshopak points for `planet` in `sign_index` for a varga of `weight`."""
    label = _sign_dignity(planet, sign_index)
    return _DIGNITY_FRACTION[label] * weight


# ── varga sign resolvers (inline — avoids heavy import of varga.py) ──────────


def _d1_si(lon: float) -> int:
    return int(lon / 30) % 12


def _d2_si(lon: float) -> int:
    si = int(lon / 30) % 12
    deg = lon % 30
    return (4 if deg < 15.0 else 3) if (si % 2 == 0) else (3 if deg < 15.0 else 4)


def _d3_si(lon: float) -> int:
    si = int(lon / 30) % 12
    k = int((lon % 30) / 10)
    return (si + k * 4) % 12


def _d7_si(lon: float) -> int:
    si = int(lon / 30) % 12
    k = min(int((lon % 30) * 7 / 30), 6)
    return (si + k) % 12 if (si % 2 == 0) else (si + 6 + k) % 12


_D9_START = {0: 0, 1: 9, 2: 6, 3: 3}


def _d9_si(lon: float) -> int:
    si = int(lon / 30) % 12
    pada = int((lon % 30) * 9 / 30)
    return (_D9_START[si % 4] + pada) % 12


def _d10_si(lon: float) -> int:
    si = int(lon / 30) % 12
    k = min(int((lon % 30) / 3), 9)
    return (si + k) % 12 if (si % 2 == 0) else (si + 9 + k) % 12


def _d12_si(lon: float) -> int:
    si = int(lon / 30) % 12
    k = min(int((lon % 30) / 2.5), 11)
    return (si + k) % 12


_VARGA_FN = {
    "D1": _d1_si,
    "D2": _d2_si,
    "D3": _d3_si,
    "D7": _d7_si,
    "D9": _d9_si,
    "D10": _d10_si,
    "D12": _d12_si,
}


# ── data classes ──────────────────────────────────────────────────────────────


@dataclass
class VargaDignity:
    """Dignity assessment for one planet in one varga."""

    division: str
    weight: float
    sign_index: int
    sign_name: str
    dignity: str  # "Exaltation" / "Moolatrikona" / "OwnSign" / "Friend" / "Neutral" / "Enemy" / "Debilitation"
    points: float  # dignity_fraction × weight


@dataclass
class PlanetVimshopak:
    """Full Sapta Varga Vimshopak row for one planet."""

    planet: str
    varga_dignities: dict[str, VargaDignity]  # division → VargaDignity
    total: float  # sum of all .points (0–20)
    grade: str  # "Excellent" / "Good" / "Average" / "Weak" / "Very Weak"

    def dignity_in(self, division: str) -> str:
        return self.varga_dignities[division].dignity

    def sign_in(self, division: str) -> str:
        return self.varga_dignities[division].sign_name


@dataclass
class VimshopakResult:
    """Vimshopak Bala for all planets (and lagna ascendant)."""

    planets: dict[str, PlanetVimshopak]  # includes "Lagna" key

    def for_planet(self, planet: str) -> PlanetVimshopak:
        return self.planets[planet]

    def ranking(self) -> list[tuple[str, float]]:
        """Return planets sorted by Vimshopak score descending (lagna excluded)."""
        return sorted(
            [(p, pv.total) for p, pv in self.planets.items() if p != "Lagna"],
            key=lambda x: x[1],
            reverse=True,
        )


# ── grade thresholds ──────────────────────────────────────────────────────────


def vimshopak_grade(score: float) -> str:
    """Return qualitative grade for a Vimshopak total (0–20)."""
    if score >= 15.0:
        return "Excellent"
    if score >= 10.0:
        return "Good"
    if score >= 6.0:
        return "Average"
    if score >= 3.0:
        return "Weak"
    return "Very Weak"


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


# ── main public function ──────────────────────────────────────────────────────


def compute_vimshopak(chart) -> VimshopakResult:  # chart: BirthChart
    """
    Compute Sapta Varga Vimshopak Bala for all 9 planets plus the Lagna.

    Parameters
    ----------
    chart : BirthChart
        Output of src.ephemeris.compute_chart().

    Returns
    -------
    VimshopakResult
        Contains a PlanetVimshopak entry for each of the 9 planets plus "Lagna".
    """
    result_planets: dict[str, PlanetVimshopak] = {}

    # Build entries for all 9 planets + Lagna
    subjects: dict[str, float] = {
        p: chart.planets[p].longitude for p in _ALL_PLANETS if p in chart.planets
    }
    subjects["Lagna"] = chart.lagna

    for subject, lon in subjects.items():
        varga_dignities: dict[str, VargaDignity] = {}
        total = 0.0

        for div, weight in SAPTA_VARGA_WEIGHTS.items():
            fn = _VARGA_FN[div]
            si = fn(lon)
            sign_name = _SIGN_NAMES[si]
            planet_key = (
                subject if subject != "Lagna" else "Sun"
            )  # Lagna uses sign dignity table
            dignity = _sign_dignity(planet_key if subject != "Lagna" else "Sun", si)
            # For Lagna: use the sign lord approach but don't associate with a planet's own tables
            # Convention: Lagna gets the dignity of the sign lord of its varga sign
            if subject == "Lagna":
                lord = _SIGN_LORD[si]
                dignity = _sign_dignity(lord, si)  # lord's dignity in its own sign
                # Simplification: Lagna in own-lord's sign → OwnSign; exalt sign of lord → Friend, etc.
                # Standard approach: Lagna just gets the sign quality (neutral unless lord in own sign)
                dignity = "OwnSign"  # Lagna ascendant is always considered in own-sign dignity
            pts = _DIGNITY_FRACTION[dignity] * weight
            total += pts
            varga_dignities[div] = VargaDignity(
                division=div,
                weight=weight,
                sign_index=si,
                sign_name=sign_name,
                dignity=dignity,
                points=pts,
            )

        grade = vimshopak_grade(total)
        result_planets[subject] = PlanetVimshopak(
            planet=subject,
            varga_dignities=varga_dignities,
            total=round(total, 4),
            grade=grade,
        )

    return VimshopakResult(planets=result_planets)
