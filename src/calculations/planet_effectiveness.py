"""
src/calculations/planet_effectiveness.py — Session 63

Multi-factor planet effectiveness score (PVRNR Ch.15, GPT Gap A2).

Synthesises all strength measures into one 0.0–1.0 effectiveness score:
  1. Shadbala (Ishtabala factor)
  2. Ashtakavarga BAV (rekhas in natal sign)
  3. Avastha (Baaladi × Sayanadi modifiers)
  4. Dig Bala (directional strength)
  5. Amsa level (Dasa Varga count)
  6. Combustion penalty
  7. Graha Yuddha outcome (Deena penalty)

PVRNR explicitly (p201): "use the right set of parameters for the occasion"
— these are combined only for an overall planet effectiveness summary,
not for replacing the specific-purpose computations.

Public API
----------
  compute_planet_effectiveness(planet, chart) -> PlanetEffectiveness
  compute_all_effectiveness(chart) -> dict[str, PlanetEffectiveness]
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PlanetEffectiveness:
    planet: str
    shadbala_factor: float    # 0.0–1.0 from Shadbala
    av_factor: float          # 0.0–1.0 from AV rekhas (0-8 → /8)
    avastha_factor: float     # baaladi_pct × sayanadi_modifier
    dig_bala_factor: float    # 0.0–1.0 continuous score
    amsa_factor: float        # 0.0–1.0 from amsa level (count/10)
    combust_penalty: float    # 0.5 if combust, else 1.0
    yuddha_penalty: float     # 0.5 if loser, else 1.0
    overall: float            # weighted combination
    label: str                # "Highly effective"/"Effective"/"Moderate"/"Weak"/"Ineffective"


def compute_planet_effectiveness(planet: str, chart) -> PlanetEffectiveness:
    """Compute multi-factor effectiveness for one planet."""

    # 1. Shadbala
    shadbala_f = 0.5
    try:
        from src.calculations.shadbala import compute_shadbala
        sb = compute_shadbala(chart)
        planet_sb = sb.planets.get(planet)
        if planet_sb:
            total = planet_sb.total
            # Normalize: avg = 400 Virupas, range ~0–800
            shadbala_f = min(1.0, max(0.0, total / 600.0))
    except Exception:
        pass

    # 2. AV rekhas
    av_f = 0.5
    try:
        from src.calculations.ashtakavarga import compute_ashtakavarga
        av = compute_ashtakavarga(chart)
        pos = chart.planets.get(planet)
        if pos:
            planet_av = getattr(av, planet.lower(), None)
            if planet_av:
                rekhas = planet_av.bindus.get(pos.sign_index, 4)
                av_f = rekhas / 8.0
    except Exception:
        pass

    # 3. Avastha (baaladi × sayanadi)
    avastha_f = 1.0
    try:
        from src.calculations.avastha_v2 import compute_avasthas_v2
        av2 = compute_avasthas_v2(chart)
        pa = av2.planets.get(planet)
        if pa:
            avastha_f = min(1.5, pa.combined_modifier) / 1.5
    except Exception:
        pass

    # 4. Dig Bala
    dig_f = 0.5
    try:
        from src.calculations.dig_bala import compute_dig_bala
        db = compute_dig_bala(chart)
        dig_f = db[planet].score if planet in db else 0.5
    except Exception:
        pass

    # 5. Amsa level
    amsa_f = 0.5
    try:
        from src.calculations.yoga_fructification import compute_amsa_level
        count, _ = compute_amsa_level(planet, chart)
        amsa_f = min(1.0, count / 5.0)  # 5 = Simhasanamsa = distinguished
    except Exception:
        pass

    # 6. Combustion
    combust_p = 1.0
    try:
        from src.calculations.dignity import compute_all_dignities
        dig = compute_all_dignities(chart).get(planet)
        if dig and dig.is_combust:
            combust_p = 0.5
    except Exception:
        pass

    # 7. Graha Yuddha
    yuddha_p = 1.0
    try:
        from src.calculations.graha_yuddha import compute_graha_yuddha
        wars = compute_graha_yuddha(chart)
        losers = {w.loser for w in wars}
        if planet in losers:
            yuddha_p = 0.5
    except Exception:
        pass

    # Weighted combination (PVRNR: no single measure dominates)
    overall = round(
        shadbala_f * 0.20 +
        av_f       * 0.15 +
        avastha_f  * 0.20 +
        dig_f      * 0.15 +
        amsa_f     * 0.15 +
        combust_p  * 0.075 +
        yuddha_p   * 0.075,
        4
    )

    if overall >= 0.75:   label = "Highly effective"
    elif overall >= 0.55: label = "Effective"
    elif overall >= 0.40: label = "Moderate"
    elif overall >= 0.25: label = "Weak"
    else:                 label = "Ineffective"

    return PlanetEffectiveness(
        planet=planet,
        shadbala_factor=round(shadbala_f,4),
        av_factor=round(av_f,4),
        avastha_factor=round(avastha_f,4),
        dig_bala_factor=round(dig_f,4),
        amsa_factor=round(amsa_f,4),
        combust_penalty=combust_p,
        yuddha_penalty=yuddha_p,
        overall=overall,
        label=label,
    )


def compute_all_effectiveness(chart) -> dict[str, PlanetEffectiveness]:
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    return {p: compute_planet_effectiveness(p, chart) for p in planets_7}
