"""
src/calculations/special_lagnas.py
Special Lagnas: Hora, Ghati, Bhava, Varnada, Sree, Indu, Pranapada, Upapada.
Session 130 (Phase 2).

Sources:
  Jaimini Sutras Adhyaya 1 (Hora Lagna, Ghati Lagna, Varnada)
  BPHS Ch.13 (Sree Lagna, Pranapada)
  Hora Makaranda (Indu Lagna)
  PVRNR, Vedic Astrology App.C (formulae)
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SpecialLagnas:
    hora_lagna: int        # Hora Lagna sign index 0-11
    ghati_lagna: int       # Ghati Lagna sign index
    bhava_lagna: int       # Bhava Lagna sign index
    varnada_lagna: int     # Varnada Lagna sign index
    sree_lagna: int        # Sree / Shree Lagna sign index
    indu_lagna: int        # Indu Lagna sign index
    pranapada: int         # Pranapada Lagna sign index
    upapada: int           # Upapada Lagna (A12, Arudha of H12) sign index


def compute_special_lagnas(
    chart,
    birth_dt: datetime = None,
    sunrise_dt: Optional[datetime] = None,
) -> SpecialLagnas:
    """
    Compute all special Lagnas.
    sunrise_dt: sunrise at birth location on birth date.
    If not provided, approximates 06:00 local time.
    """
    if birth_dt is None:
        from datetime import datetime as _dt
        birth_dt = _dt.now()
    if sunrise_dt is None:
        sunrise_dt = birth_dt.replace(hour=6, minute=0, second=0)

    lagna_si = chart.lagna_sign_index

    # Time elapsed since sunrise in hours
    elapsed_hours = (birth_dt - sunrise_dt).total_seconds() / 3600.0
    elapsed_ghatis = elapsed_hours * 2.5  # 1 Ghati = 24 minutes = 0.4 hours

    # ── Hora Lagna ──
    # Moves 1 sign every 2.5 Ghatis (1 hour) from Lagna at sunrise
    hora_offset = int(elapsed_hours) % 12
    hora_lagna = (lagna_si + hora_offset) % 12

    # ── Ghati Lagna ──
    # Moves 1 sign every 5 Ghatis (2 hours)
    ghati_offset = int(elapsed_ghatis / 5) % 12
    ghati_lagna = (lagna_si + ghati_offset) % 12

    # ── Bhava Lagna ──
    # Moves at rate of Sun: 1 sign every 2 hours (approx)
    bhava_offset = int(elapsed_hours / 2) % 12
    bhava_lagna = (lagna_si + bhava_offset) % 12

    # ── Varnada Lagna ──
    # Derived from Hora Lagna and Ghati Lagna: Source: Jaimini Sutras
    # If both HL and GL are in odd signs or both even: take the difference
    # If one odd one even: add them
    hl_odd = hora_lagna % 2 == 0   # Aries=0=odd sign in Jyotish (index 0)
    gl_odd = ghati_lagna % 2 == 0
    if hl_odd == gl_odd:
        varnada = abs(hora_lagna - ghati_lagna) % 12
    else:
        varnada = (hora_lagna + ghati_lagna) % 12

    # ── Sree Lagna ──
    # Based on Moon's longitude and its sign lord's strength
    # Simplified: Moon longitude + (lord of Moon sign index) * 30 % 360
    moon_si = chart.planets["Moon"].sign_index if "Moon" in chart.planets else 0
    moon_lon = chart.planets["Moon"].longitude if "Moon" in chart.planets else 0.0

    _LORDS_PERIOD = {
        "Sun": 6, "Moon": 10, "Mars": 7, "Mercury": 17,
        "Jupiter": 16, "Venus": 20, "Saturn": 19,
        "Rahu": 18, "Ketu": 7,
    }
    _SIGN_LORDS = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",
        5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",
        9: "Saturn", 10: "Saturn", 11: "Jupiter",
    }

    moon_lord = _SIGN_LORDS.get(moon_si, "Moon")
    lord_period = _LORDS_PERIOD.get(moon_lord, 10)
    sree_lon = (moon_lon + lord_period * 30) % 360
    sree_lagna = int(sree_lon / 30) % 12

    # ── Indu Lagna ──
    # Sum of H9 lord's period value from Lagna and Moon, then from Moon
    # Source: Hora Makaranda
    lagna_h9_sign = (lagna_si + 8) % 12
    moon_h9_sign  = (moon_si + 8) % 12
    lagna_h9_lord = _SIGN_LORDS.get(lagna_h9_sign, "Jupiter")
    moon_h9_lord  = _SIGN_LORDS.get(moon_h9_sign, "Jupiter")
    indu_total = (_LORDS_PERIOD.get(lagna_h9_lord, 10) + _LORDS_PERIOD.get(moon_h9_lord, 10)) % 12
    indu_lagna = (moon_si + indu_total) % 12

    # ── Pranapada ──
    # Sun longitude + birth time contribution
    # Source: BPHS Ch.13
    sun_lon = chart.planets["Sun"].longitude if "Sun" in chart.planets else 0.0
    pranapada_lon = (sun_lon + elapsed_ghatis * 4) % 360
    pranapada = int(pranapada_lon / 30) % 12

    # ── Upapada Lagna (A12) ──
    # Arudha of 12th house
    # Source: Jaimini Sutras (Arudha Lagna formula)
    h12_sign = (lagna_si + 11) % 12
    h12_lord = _SIGN_LORDS.get(h12_sign, "Jupiter")
    if h12_lord in chart.planets:
        lord_si = chart.planets[h12_lord].sign_index
        dist = (lord_si - h12_sign) % 12
        upapada_si = (lord_si + dist) % 12
        # Special rule: if upapada falls on same sign as H12 or its 7th, shift 10
        if upapada_si == h12_sign or upapada_si == (h12_sign + 6) % 12:
            upapada_si = (upapada_si + 9) % 12
    else:
        upapada_si = h12_sign

    return SpecialLagnas(
        hora_lagna=hora_lagna,
        ghati_lagna=ghati_lagna,
        bhava_lagna=bhava_lagna,
        varnada_lagna=varnada,
        sree_lagna=sree_lagna,
        indu_lagna=indu_lagna,
        pranapada=pranapada,
        upapada=upapada_si,
    )


# ── Backward-compatibility properties ──
_SIGN_NAMES_SL = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                  "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

def _add_compat(cls):
    """Add _sign and _index properties for each lagna field."""
    fields = ["hora_lagna","ghati_lagna","bhava_lagna","varnada_lagna",
              "sree_lagna","indu_lagna","pranapada","upapada"]
    for f in fields:
        def make_sign(fname):
            return property(lambda self: _SIGN_NAMES_SL[getattr(self, fname)])
        def make_index(fname):
            return property(lambda self: getattr(self, fname))
        setattr(cls, f + "_sign", make_sign(f))
        setattr(cls, f + "_index", make_index(f))
        setattr(cls, f + "_sign_name", make_sign(f))
    return cls

SpecialLagnas = _add_compat(SpecialLagnas)
