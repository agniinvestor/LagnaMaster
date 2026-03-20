"""
src/calculations/special_lagnas.py — Session 46

Five special lagnas from BPHS:
  Hora Lagna   — wealth lagna (from Sun's position)
  Ghati Lagna  — power lagna (based on birth time Ghatis)
  Sree Lagna   — prosperity lagna (Moon-based)
  Indu Lagna   — lunar wealth lagna (BPHS Ch.14)
  Pranapada    — vital lagna (Sun + ascendant offset)

Public API
----------
  compute_special_lagnas(chart) -> SpecialLagnas
"""
from __future__ import annotations
from dataclasses import dataclass

_SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
          "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

# Indu Lagna: planet values (Virupas) used for offset calculation
_INDU_VALUES = {"Sun":30,"Moon":16,"Mars":6,"Mercury":8,
                 "Jupiter":10,"Venus":12,"Saturn":1}
_SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
              6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}


@dataclass
class SpecialLagnas:
    hora_lagna_sign: str
    hora_lagna_index: int
    ghati_lagna_sign: str
    ghati_lagna_index: int
    sree_lagna_sign: str
    sree_lagna_index: int
    indu_lagna_sign: str
    indu_lagna_index: int
    pranapada_sign: str
    pranapada_index: int


def compute_special_lagnas(chart) -> SpecialLagnas:
    """Compute all 5 special lagnas."""
    sun_lon  = chart.planets["Sun"].longitude
    moon_lon = chart.planets["Moon"].longitude
    lagna    = chart.lagna % 360
    hour     = getattr(chart, 'birth_hour', 0.0)

    # ── Hora Lagna ────────────────────────────────────────────────────────────
    # Each hour after sunrise, Hora Lagna advances 30°.
    # Approximation: Sun's longitude + (birth_hour × 30°)
    hora_lon = (sun_lon + hour * 30) % 360
    hora_si  = int(hora_lon / 30) % 12

    # ── Ghati Lagna ───────────────────────────────────────────────────────────
    # Each Ghati (24 minutes), Ghati Lagna advances 1/2 sign = 15°.
    # 1 hour = 2.5 Ghatis, so Ghati Lagna advances 37.5° per hour.
    ghati_lon = (lagna + hour * 37.5) % 360
    ghati_si  = int(ghati_lon / 30) % 12

    # ── Sree Lagna ────────────────────────────────────────────────────────────
    # Moon's longitude from Sun, added to Lagna.
    moon_from_sun = (moon_lon - sun_lon) % 360
    sree_lon = (lagna + moon_from_sun) % 360
    sree_si  = int(sree_lon / 30) % 12

    # ── Indu Lagna ────────────────────────────────────────────────────────────
    # Sum the Indu values of the 9th lords from Lagna and from Moon.
    # Add the sum (mod 12) to Moon's sign to get Indu Lagna house from Moon.
    lagna_si = int(lagna / 30) % 12
    moon_si  = int(moon_lon / 30) % 12

    lord9_from_lagna = _SIGN_LORD[(lagna_si + 8) % 12]
    lord9_from_moon  = _SIGN_LORD[(moon_si + 8) % 12]

    indu_sum = (_INDU_VALUES.get(lord9_from_lagna, 0) +
                _INDU_VALUES.get(lord9_from_moon, 0)) % 12
    indu_si  = (moon_si + indu_sum) % 12

    # ── Pranapada ─────────────────────────────────────────────────────────────
    # Sun's longitude + (Sun's distance from Aries start ÷ 15) × 30°
    # Simplified: Pranapada = Sun_lon + (Sun_lon mod 30) × 2 (BPHS variant)
    sun_deg_in_sign = sun_lon % 30
    prana_lon = (sun_lon + sun_deg_in_sign * 2) % 360
    prana_si  = int(prana_lon / 30) % 12

    return SpecialLagnas(
        hora_lagna_sign=_SIGNS[hora_si],   hora_lagna_index=hora_si,
        ghati_lagna_sign=_SIGNS[ghati_si], ghati_lagna_index=ghati_si,
        sree_lagna_sign=_SIGNS[sree_si],   sree_lagna_index=sree_si,
        indu_lagna_sign=_SIGNS[indu_si],   indu_lagna_index=indu_si,
        pranapada_sign=_SIGNS[prana_si],   pranapada_index=prana_si,
    )
