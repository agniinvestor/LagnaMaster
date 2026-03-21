"""
src/calculations/varga.py
=========================
Varga (Divisional) Chart calculator — Session 15.

Computes 7 standard divisional charts from a BirthChart:
  D2  Hora          (2 divisions × 30° = 15° each)
  D3  Drekkana      (3 divisions × 10°)
  D4  Chaturthamsha (4 divisions × 7°30')
  D7  Saptamsha     (7 divisions × 4°17'8.57'')
  D10 Dashamsha     (10 divisions × 3°)
  D12 Dvadasamsha   (12 divisions × 2°30')
  D60 Shashtyamsha  (60 divisions × 0°30')

D9 (Navamsha) is already implemented in panchanga.py — use
compute_navamsha_chart() from there; this module cross-validates it via
_d9_sign_index() for internal consistency checks.

All formulas follow BPHS (Brihat Parashara Hora Shastra) standard.
Rahu/Ketu follow the same positional formula as the other planets.

Public API
----------
    compute_varga(chart: BirthChart) -> VargaChart
    varga_sign_name(sign_index: int) -> str

Data classes
------------
    VargaPlanet(planet, d1_longitude, d1_sign, d1_si, varga_sign_index,
                varga_sign, is_retrograde)
    VargaTable(division, label, lagna_sign_index, lagna_sign, planets)
    VargaChart(planet_tables)
"""

from __future__ import annotations
from dataclasses import dataclass, field

# ── forward-reference guard (avoid circular import with ephemeris) ──────────
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ephemeris import BirthChart

# ── constants ────────────────────────────────────────────────────────────────

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury",
    "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
]


def varga_sign_name(sign_index: int) -> str:
    """Return the sign name for a zero-based sign index (0=Aries … 11=Pisces)."""
    return SIGNS[sign_index % 12]


# ── element helpers ──────────────────────────────────────────────────────────

def _sign_element(si: int) -> int:
    """Return element index: 0=Fire, 1=Earth, 2=Air, 3=Water."""
    return si % 4


def _is_odd_sign(si: int) -> bool:
    """Aries/Gemini/Leo/Libra/Sagittarius/Aquarius are odd (index 0,2,4,6,8,10)."""
    return si % 2 == 0


# ── D2 Hora ──────────────────────────────────────────────────────────────────

def _d2_sign_index(longitude: float) -> int:
    """
    D2 Hora rule (BPHS):
      Odd signs  (Aries, Gemini, Leo...):  0°–15° → Sun's hora (Leo  = 4)
                                           15°–30° → Moon's hora (Cancer = 3)
      Even signs (Taurus, Cancer, Virgo...): 0°–15° → Moon's hora (Cancer = 3)
                                             15°–30° → Sun's hora (Leo  = 4)
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    if _is_odd_sign(si):
        return 4 if deg < 15.0 else 3   # Leo / Cancer
    else:
        return 3 if deg < 15.0 else 4   # Cancer / Leo


# ── D3 Drekkana ──────────────────────────────────────────────────────────────

def _d3_sign_index(longitude: float) -> int:
    """
    D3 Drekkana (Parashari / Somanatha):
      Each sign divided into 3 × 10° decanates.
      k=0 (0°–10°):   same sign
      k=1 (10°–20°):  sign + 4 (5th sign, Trikona)
      k=2 (20°–30°):  sign + 8 (9th sign, Trikona)
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    k = int(deg / 10)
    return (si + k * 4) % 12


# ── D4 Chaturthamsha ─────────────────────────────────────────────────────────

def _d4_sign_index(longitude: float) -> int:
    """
    D4 Chaturthamsha:
      Each sign divided into 4 × 7°30'.
      k=0: same sign; k=1: sign+3; k=2: sign+6; k=3: sign+9
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    k = int(deg / 7.5)
    return (si + k * 3) % 12


# ── D7 Saptamsha ─────────────────────────────────────────────────────────────

def _d7_sign_index(longitude: float) -> int:
    """
    D7 Saptamsha (each 4°17'8.57'' = 30/7°):
      Odd  signs: start from the sign itself;        k=0..6: (si + k) % 12
      Even signs: start 7 signs ahead (si+6); k=0..6: (si + 6 + k) % 12
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    k = int(deg * 7 / 30)
    k = min(k, 6)
    if _is_odd_sign(si):
        return (si + k) % 12
    else:
        return (si + 6 + k) % 12


# ── D9 Navamsha (cross-validation only) ──────────────────────────────────────

_D9_START = {0: 0, 1: 9, 2: 6, 3: 3}  # Fire=Aries(0), Earth=Capricorn(9), Air=Libra(6), Water=Cancer(3)


def _d9_sign_index(longitude: float) -> int:
    """
    D9 Navamsha (3°20' per pada).
    Matches panchanga.py formula exactly.
    """
    si = int(longitude / 30) % 12
    pada = int((longitude % 30) * 9 / 30)
    return (_D9_START[si % 4] + pada) % 12


# ── D10 Dashamsha ─────────────────────────────────────────────────────────────

def _d10_sign_index(longitude: float) -> int:
    """
    D10 Dashamsha (3° each):
      Odd  signs: start from sign itself;    k=0..9: (si + k) % 12
      Even signs: start 9 ahead (si+9); k=0..9: (si + 9 + k) % 12
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    k = int(deg / 3)
    k = min(k, 9)
    if _is_odd_sign(si):
        return (si + k) % 12
    else:
        return (si + 9 + k) % 12


# ── D12 Dvadasamsha ───────────────────────────────────────────────────────────

def _d12_sign_index(longitude: float) -> int:
    """
    D12 Dvadasamsha (2°30' each):
      Start from sign itself for all signs; k=0..11: (si + k) % 12
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    k = int(deg / 2.5)
    k = min(k, 11)
    return (si + k) % 12


# ── D60 Shashtyamsha ──────────────────────────────────────────────────────────

def _d60_sign_index(longitude: float) -> int:
    """
    D60 Shashtyamsha (0°30' each, 60 divisions per sign):
      Odd  signs: k=0..59 → k % 12      (starts from Aries)
      Even signs: k=0..59 → (5 + k) % 12  (starts from Virgo)
    """
    si = int(longitude / 30) % 12
    deg = longitude % 30
    k = int(deg * 2)          # 0.5° per division → multiply by 2
    k = min(k, 59)
    if _is_odd_sign(si):
        return k % 12
    else:
        return (5 + k) % 12


# ── dispatch table ────────────────────────────────────────────────────────────

_VARGA_FUNCS = {
    "D2":  _d2_sign_index,
    "D3":  _d3_sign_index,
    "D4":  _d4_sign_index,
    "D7":  _d7_sign_index,
    "D9":  _d9_sign_index,
    "D10": _d10_sign_index,
    "D12": _d12_sign_index,
    "D60": _d60_sign_index,
}

_VARGA_LABELS = {
    "D2":  "Hora",
    "D3":  "Drekkana",
    "D4":  "Chaturthamsha",
    "D7":  "Saptamsha",
    "D9":  "Navamsha",
    "D10": "Dashamsha",
    "D12": "Dvadasamsha",
    "D60": "Shashtyamsha",
}


# ── data classes ──────────────────────────────────────────────────────────────

@dataclass
class VargaPlanet:
    planet: str
    d1_longitude: float    # sidereal, 0–360°
    d1_sign: str           # D1 sign name
    d1_sign_index: int     # 0=Aries … 11=Pisces
    varga_sign_index: int  # divisional sign index
    varga_sign: str        # divisional sign name
    is_retrograde: bool
    speed: float           # degrees/day


@dataclass
class VargaTable:
    """Divisional chart for one varga (e.g. D2, D7)."""
    division: str            # "D2", "D3" …
    label: str               # "Hora", "Drekkana" …
    lagna_sign_index: int    # D1 lagna used as reference
    lagna_sign: str
    varga_lagna_sign_index: int  # ascendant in *this* varga
    varga_lagna_sign: str
    planets: dict[str, VargaPlanet]   # planet name → VargaPlanet

    def planet_sign(self, planet: str) -> str:
        """Return varga sign name for a planet."""
        return self.planets[planet].varga_sign

    def planet_sign_index(self, planet: str) -> int:
        return self.planets[planet].varga_sign_index

    def planets_in_sign(self, sign_index: int) -> list[str]:
        """Return list of planet names placed in a given varga sign."""
        return [p for p, vp in self.planets.items() if vp.varga_sign_index == sign_index]


@dataclass
class VargaChart:
    """Complete set of divisional charts for one BirthChart."""
    tables: dict[str, VargaTable] = field(default_factory=dict)

    # shortcut accessors
    def d2(self) -> VargaTable:  return self.tables["D2"]
    def d3(self) -> VargaTable:  return self.tables["D3"]
    def d4(self) -> VargaTable:  return self.tables["D4"]
    def d7(self) -> VargaTable:  return self.tables["D7"]
    def d9(self) -> VargaTable:  return self.tables["D9"]
    def d10(self) -> VargaTable: return self.tables["D10"]
    def d12(self) -> VargaTable: return self.tables["D12"]
    def d60(self) -> VargaTable: return self.tables["D60"]

    def for_division(self, division: str) -> VargaTable:
        return self.tables[division]


# ── lagna computation ─────────────────────────────────────────────────────────

def _varga_lagna(d1_lagna_lon: float, division: str) -> int:
    """
    Compute the ascendant sign index in a varga chart.
    The lagna is treated as a point (longitude) and put through
    the same divisional formula as any planet.
    """
    fn = _VARGA_FUNCS[division]
    return fn(d1_lagna_lon)


# ── main public function ──────────────────────────────────────────────────────

def compute_varga(chart) -> VargaChart:   # chart: BirthChart
    """
    Compute all 7 divisional charts (D2/D3/D4/D7/D9/D10/D12/D60) for a
    BirthChart.  D9 is included here for completeness and cross-validation
    against panchanga.compute_navamsha_chart().

    Parameters
    ----------
    chart : BirthChart
        Output of src.ephemeris.compute_chart().

    Returns
    -------
    VargaChart
        Contains VargaTable entries keyed by "D2" … "D60".
    """
    vc = VargaChart()
    d1_lagna_lon = chart.lagna  # sidereal, 0–360°

    for division, fn in _VARGA_FUNCS.items():
        label = _VARGA_LABELS[division]

        varga_lagna_si = fn(d1_lagna_lon)
        varga_lagna_sign = varga_sign_name(varga_lagna_si)

        planet_map: dict[str, VargaPlanet] = {}
        for pname in _PLANETS:
            pp = chart.planets.get(pname)
            if pp is None:
                continue
            lon = pp.longitude
            v_si = fn(lon)
            planet_map[pname] = VargaPlanet(
                planet=pname,
                d1_longitude=lon,
                d1_sign=pp.sign,
                d1_sign_index=pp.sign_index,
                varga_sign_index=v_si,
                varga_sign=varga_sign_name(v_si),
                is_retrograde=pp.is_retrograde,
                speed=pp.speed,
            )

        vc.tables[division] = VargaTable(
            division=division,
            label=label,
            lagna_sign_index=chart.lagna_sign_index,
            lagna_sign=chart.lagna_sign,
            varga_lagna_sign_index=varga_lagna_si,
            varga_lagna_sign=varga_lagna_sign,
            planets=planet_map,  # noqa: F841
        )

    return vc
