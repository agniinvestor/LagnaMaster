"""
src/calculations/shodashavarga_bala.py
Shodashavarga Bala — 16-varga strength system extending Saptavargaja.
Session 147 / G-3 (Audit G-3).

BPHS Ch.6 defines 16 divisional charts. Their combined dignity determines
Shodashavarga Bala, a more complete strength picture than Saptavargaja.

Sources:
  PVRNR · BPHS Ch.6 v.15-22
  Sanjay Rath · Varga Chakra Ch.1
"""
from __future__ import annotations

# Virupa values per varga position
# Higher Virupas = more weight in total Shodashavarga Bala
_VARGA_WEIGHT: dict[int, float] = {
    1:  6.0,   # D1  Rasi        — highest weight
    2:  2.0,   # D2  Hora
    3:  3.0,   # D3  Drekkana
    4:  1.5,   # D4  Chaturthamsha
    7:  1.5,   # D7  Saptamamsha
    9:  5.0,   # D9  Navamsha    — second highest
    10: 3.0,   # D10 Dasamsha
    12: 2.0,   # D12 Dvadashamsha
    16: 1.5,   # D16 Shodashamsha
    20: 1.0,   # D20 Vimshamsha
    24: 1.0,   # D24 Chaturvimshamsha
    27: 1.0,   # D27 Bhamsha
    30: 2.0,   # D30 Trimshamamsha
    40: 0.5,   # D40 Khavedamsha
    45: 0.5,   # D45 Akshavedamsha
    60: 4.0,   # D60 Shashtiamsha — third highest (past karma)
}

# Dignity Virupa values (same scale as Saptavargaja)
_DIGNITY_VIRUPAS: dict[str, float] = {
    "Deep Exaltation": 30.0,
    "Exaltation": 30.0,
    "Mooltrikona": 30.0,
    "Own Sign": 25.0,
    "Adhimitra": 20.0,     # 5-fold best friend
    "Mitra": 15.0,         # Friend
    "Sama": 7.5,           # Neutral
    "Shatru": 3.75,        # Enemy
    "Adhi-Shatru": 1.875,  # Bitter enemy
    "Debilitation": 1.875,
    "Neecha Bhanga Raja": 20.0,
    "Friendly Sign": 15.0,
    "Neutral": 7.5,
    "Enemy Sign": 3.75,
}

_SHODASHA_VARGAS = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]


def compute_shodashavarga_bala(planet: str, chart) -> dict:
    """
    Compute Shodashavarga Bala — 16-varga combined dignity score.

    Returns:
        {
            'total_virupas': float,
            'max_possible': float,
            'strength_pct': float,
            'varga_details': {D_n: {'dignity': str, 'virupas': float}},
            'label': 'Strong'/'Moderate'/'Weak'
        }

    Source: PVRNR · BPHS Ch.6 v.15-22; Sanjay Rath · Varga Chakra Ch.1
    """
    if planet not in chart.planets:
        return {"total_virupas": 0.0, "max_possible": 0.0,
                "strength_pct": 0.0, "varga_details": {}, "label": "Unknown"}

    planet_lon = chart.planets[planet].longitude

    try:
        from src.calculations.vargas import compute_varga_sign
        from src.calculations.dignity import compute_dignity_for_sign, DignityLevel
    except ImportError:
        return {"total_virupas": 0.0, "max_possible": 0.0,
                "strength_pct": 0.0, "varga_details": {},
                "label": "Requires vargas.py and dignity.py"}

    total = 0.0
    max_possible = 0.0
    details = {}

    for varga_n in _SHODASHA_VARGAS:
        weight = _VARGA_WEIGHT.get(varga_n, 1.0)
        max_possible += weight * 30.0  # max 30 Virupas per varga

        try:
            varga_si = compute_varga_sign(planet_lon, varga_n)

            # Get dignity in this varga
            try:
                d = compute_dignity_for_sign(planet, varga_si)
                dignity_name = d.dignity.value if hasattr(d, 'dignity') else "Neutral"
            except Exception:
                dignity_name = "Neutral"

            virupas = _DIGNITY_VIRUPAS.get(dignity_name, 7.5) * weight
            total += virupas
            details[f"D{varga_n}"] = {"dignity": dignity_name, "virupas": round(virupas, 3),
                                       "varga_sign": varga_si}
        except Exception:
            details[f"D{varga_n}"] = {"dignity": "Error", "virupas": 0.0, "varga_sign": -1}

    strength_pct = (total / max_possible * 100) if max_possible > 0 else 0.0

    if strength_pct >= 65:  label = "Strong"
    elif strength_pct >= 40: label = "Moderate"
    else:                    label = "Weak"

    return {
        "total_virupas": round(total, 3),
        "max_possible": round(max_possible, 3),
        "strength_pct": round(strength_pct, 2),
        "varga_details": details,
        "label": label,
    }


def shodashavarga_summary(chart) -> dict[str, dict]:
    """Compute Shodashavarga Bala for all 9 planets."""
    planets = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]
    return {p: compute_shodashavarga_bala(p, chart) for p in planets if p in chart.planets}
