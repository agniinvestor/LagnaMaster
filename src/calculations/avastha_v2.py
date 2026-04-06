"""
src/calculations/avastha_v2.py — Session 39 (fixed), S317 consolidated.
Delegates to avasthas.py (BPHS Ch.45 authoritative) for Baaladi.
Lajjitadi from avasthas.py replaces the ad-hoc Sayanadi modifier.
"""

from __future__ import annotations
from dataclasses import dataclass

from src.calculations.avasthas import (
    compute_baaladi as _bphs_baaladi,
    compute_jagradadi,
    compute_lajjitadi,
    BAALADI_EFFECT,
    JAGRADADI_EFFECT,
    LajjitadiAvastha,
)


# Legacy name mapping for backward compatibility with existing consumers
_BAALADI_NAMES = {
    "BAALA": "Bala", "KUMARA": "Kumar", "YUVA": "Yuva",
    "VRIDDHA": "Vridha", "MRITA": "Mrita",
}


def compute_baaladi(planet: str, chart) -> tuple[str, float]:
    """Delegates to BPHS-authoritative avasthas.py (Ch.45 v.3-4)."""
    pos = chart.planets.get(planet)
    if not pos:
        return "Yuva", 1.0
    result = _bphs_baaladi(pos.sign_index, pos.degree_in_sign)
    name = _BAALADI_NAMES.get(result.name, result.value)
    return name, BAALADI_EFFECT[result]


# Lajjitadi modifier mapping — BPHS Ch.45 v.24-29 (p.453)
_LAJJITADI_MOD: dict[LajjitadiAvastha | None, float] = {
    LajjitadiAvastha.GARVITA: 1.25,    # Proud — exalted/MT
    LajjitadiAvastha.MUDITA: 1.15,     # Delighted — friendly + benefic
    None: 1.0,                          # No specific state
    LajjitadiAvastha.LAJJITA: 0.75,    # Ashamed — 5th + malefic
    LajjitadiAvastha.KSHUDITA: 0.70,   # Hungry — enemy sign
    LajjitadiAvastha.TRUSHITA: 0.65,   # Thirsty — watery + enemy
    LajjitadiAvastha.KSHOBHITA: 0.50,  # Agitated — Sun + malefic
}


def compute_sayanadi(planet: str, chart) -> tuple[str, float]:
    """Uses BPHS Lajjitadi (Ch.45 v.11-18) for association-based modifier."""
    lajj = compute_lajjitadi(planet, chart)
    if lajj is None:
        # Fall back to Jagradadi for basic dignity-based modifier
        pos = chart.planets.get(planet)
        if not pos:
            return "Prakrita", 1.0
        jag = compute_jagradadi(planet, pos.sign_index)
        return jag.value, JAGRADADI_EFFECT[jag] * 1.25 if JAGRADADI_EFFECT[jag] > 0 else 1.0
    return lajj.value, _LAJJITADI_MOD.get(lajj, 1.0)


@dataclass
class AvasthaV2:
    planet: str
    sign: str
    degree: float
    baaladi_state: str
    baaladi_pct: float
    sayanadi_state: str
    sayanadi_modifier: float
    combined_modifier: float


@dataclass
class AvasthaReportV2:
    planets: dict

    def modifier_for(self, planet: str) -> float:
        av = self.planets.get(planet)
        return av.combined_modifier if av else 1.0


def compute_avasthas_v2(chart) -> AvasthaReportV2:
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    result = {}
    for p in planets_7:
        pos = chart.planets.get(p)
        if not pos:
            continue
        ba_state, ba_pct = compute_baaladi(p, chart)
        sa_state, sa_mod = compute_sayanadi(p, chart)
        result[p] = AvasthaV2(
            planet=p,
            sign=pos.sign,
            degree=round(pos.degree_in_sign, 4),
            baaladi_state=ba_state,
            baaladi_pct=ba_pct,
            sayanadi_state=sa_state,
            sayanadi_modifier=sa_mod,
            combined_modifier=round(ba_pct * sa_mod, 3),
        )
    return AvasthaReportV2(planets=result)
