"""
src/calculations/transit_quality_advanced.py
Advanced transit quality: Tarabala, Chandrabala, 64th navamsha,
22nd drekkana, double transit theory, Chandra Shtama.
Sessions 142-143.

Sources:
  Mantreswara · Phaladeepika Ch.26 v.20-25 (Tarabala)
  PVRNR · BPHS Transit chapters (Chandrabala)
  PVRNR · BPHS (64th navamsha)
  K.N. Rao · Yogis, Destiny and the Wheel of Time Ch.5 (64th navamsha)
  Sanjay Rath · Crux of Vedic Astrology Ch.14 (double transit)
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# ─── Tarabala ─────────────────────────────────────────────────────────────────
# Source: Phaladeepika Ch.26 v.20-25

TARA_NAMES = [
    "Janma",        # 1 - birth star: difficult for activities
    "Sampat",       # 2 - wealth: generally auspicious
    "Vipat",        # 3 - danger: avoid travel, major decisions
    "Kshema",       # 4 - comfort: good for comfort, moderate
    "Pratyak",      # 5 - obstacle: obstacles; avoid
    "Sadhana",      # 6 - achievement: excellent for achievement
    "Naidhana",     # 7 - destruction: most inauspicious
    "Mitra",        # 8 - friend: good for friendships/partnerships
    "Param Mitra",  # 9 - best friend: most auspicious
]

TARA_QUALITY = {
    "Janma": "difficult",
    "Sampat": "auspicious",
    "Vipat": "inauspicious",
    "Kshema": "moderate",
    "Pratyak": "inauspicious",
    "Sadhana": "excellent",
    "Naidhana": "very_inauspicious",
    "Mitra": "auspicious",
    "Param Mitra": "most_auspicious",
}


def tarabala(natal_nakshatra_idx: int, transit_nakshatra_idx: int) -> dict:
    """
    Compute Tarabala for a transit nakshatra relative to natal nakshatra.
    Count from natal nakshatra to transit nakshatra (inclusive).
    Result cycles 1-9 and the position gives the Tara name and quality.

    Source: Phaladeepika Ch.26 v.20-25
    """
    count = ((transit_nakshatra_idx - natal_nakshatra_idx) % 27) + 1
    tara_pos = ((count - 1) % 9)  # 0-8 index into TARA_NAMES
    tara_name = TARA_NAMES[tara_pos]
    return {
        "count_from_natal": count,
        "tara_name": tara_name,
        "tara_position": tara_pos + 1,  # 1-9
        "quality": TARA_QUALITY[tara_name],
        "is_auspicious": TARA_QUALITY[tara_name] in ("auspicious", "excellent", "most_auspicious", "moderate"),
    }


# ─── Chandrabala ──────────────────────────────────────────────────────────────

CHANDRABALA_GOOD_POSITIONS = {1, 3, 5, 6, 7, 10, 11}  # transit Moon positions from natal Moon
CHANDRABALA_BAD_POSITIONS  = {4, 8, 12}
# Note: H2, H9 are neutral; H6 is special (upachaya — challenging but growth)


def chandrabala(natal_moon_sign: int, transit_moon_sign: int) -> dict:
    """
    Chandrabala — Moon's transit strength relative to natal Moon.
    Source: Standard Muhurtha texts; Phaladeepika
    """
    house_from_natal = ((transit_moon_sign - natal_moon_sign) % 12) + 1
    if house_from_natal in CHANDRABALA_GOOD_POSITIONS:
        quality = "favorable"
    elif house_from_natal in CHANDRABALA_BAD_POSITIONS:
        quality = "unfavorable"
    else:
        quality = "neutral"

    return {
        "house_from_natal_moon": house_from_natal,
        "quality": quality,
        "is_favorable": quality == "favorable",
        "chandrabala_dosha": quality == "unfavorable",
    }


# ─── 64th Navamsha and 22nd Drekkana ─────────────────────────────────────────

def compute_sensitive_points(chart) -> dict[str, float]:
    """
    Compute 64th Navamsha and 22nd Drekkana sensitive points from Moon and Lagna.

    64th Navamsha from Moon: (Moon_lon + 64 × 3.333°) mod 360
    64th Navamsha from Lagna: (Lagna_lon + 64 × 3.333°) mod 360
    22nd Drekkana from Lagna: (Lagna_lon + 22 × 10°) mod 360

    Source: PVRNR · BPHS; BV Raman · Notable Horoscopes; K.N. Rao Ch.5
    """
    NAV_WIDTH = 40.0 / 3.0  # 3.333...° per navamsha
    DRK_WIDTH = 10.0         # 10° per drekkana

    moon_lon  = chart.planets["Moon"].longitude if "Moon" in chart.planets else 0.0
    lagna_lon = chart.lagna

    return {
        "64th_navamsha_moon":   (moon_lon  + 63 * NAV_WIDTH) % 360,
        "64th_navamsha_lagna":  (lagna_lon + 63 * NAV_WIDTH) % 360,
        "22nd_drekkana_lagna":  (lagna_lon + 21 * DRK_WIDTH) % 360,
        "note": "Malefic transits within 1° of these points bring adverse results",
    }


def is_transiting_sensitive_point(
    transit_lon: float,
    sensitive_points: dict[str, float],
    orb: float = 1.5,
) -> dict[str, bool]:
    """
    Check if a transit longitude is within orb of any sensitive point.
    """
    result = {}
    for name, point_lon in sensitive_points.items():
        if name == "note":
            continue
        diff = abs(transit_lon - point_lon) % 360
        diff = min(diff, 360 - diff)
        result[name] = diff <= orb
    return result


# ─── Double Transit Theory ────────────────────────────────────────────────────
# Source: Sanjay Rath · Crux of Vedic Astrology Ch.14

def compute_double_transit_activation(
    natal_chart,
    transit_chart,
) -> list[dict]:
    """
    Identify houses where BOTH Jupiter and Saturn simultaneously
    transit or aspect, triggering high-probability event manifestation.

    Source: Sanjay Rath · Crux of Vedic Astrology Ch.14
    """
    from src.calculations.bhava_and_transit import GOOD_TRANSIT_HOUSES

    lagna_si = natal_chart.lagna_sign_index
    results = []

    jup_transit_si  = transit_chart.planets["Jupiter"].sign_index if "Jupiter" in transit_chart.planets else -1
    sat_transit_si  = transit_chart.planets["Saturn"].sign_index  if "Saturn"  in transit_chart.planets else -1

    if jup_transit_si == -1 or sat_transit_si == -1:
        return results

    # Houses Jupiter is in or aspects from transit position
    def transit_houses_affected(planet_si: int, planet: str) -> set[int]:
        """Houses a transiting planet occupies or aspects."""
        from src.calculations.sputa_drishti import _ASPECT_TABLE
        occupied_house = (planet_si - lagna_si) % 12 + 1
        affected = {occupied_house}
        # Add aspect houses
        aspect_table = _ASPECT_TABLE.get(planet, {7: 1.0})
        for houses_from in aspect_table:
            if houses_from == 7:
                affected.add((occupied_house + 6) % 12 or 12)
            else:
                h = (occupied_house + houses_from - 1) % 12 or 12
                affected.add(h)
        return affected

    jup_houses = transit_houses_affected(jup_transit_si, "Jupiter")
    sat_houses  = transit_houses_affected(sat_transit_si, "Saturn")

    # Houses where both simultaneously operate
    double_houses = jup_houses & sat_houses

    for h in sorted(double_houses):
        results.append({
            "house": h,
            "jupiter_transit_sign": jup_transit_si,
            "saturn_transit_sign": sat_transit_si,
            "activation_strength": "high",
            "note": f"H{h} activated by both Jupiter and Saturn — major events likely",
        })

    return results


# ─── Chandra Shtama ───────────────────────────────────────────────────────────

def chandra_shtama(natal_moon_sign: int, planet: str, transit_sign: int) -> bool:
    """
    Returns True if planet is transiting the 8th sign from natal Moon.
    For Moon's own transit of its 8th: particularly potent.
    Source: Classical Gochara texts; K.N. Rao references.
    """
    house_from_moon = ((transit_sign - natal_moon_sign) % 12) + 1
    return house_from_moon == 8


# ─── Comprehensive Transit Quality ────────────────────────────────────────────

@dataclass
class AdvancedTransitResult:
    planet: str
    transit_sign: int
    transit_nakshatra_idx: int
    tarabala: dict
    chandrabala: dict                          # only for Moon transit
    ashtama_shani: bool
    chandra_shtama: bool
    sensitive_point_hits: dict[str, bool]
    overall_quality: str                       # "excellent" / "good" / "neutral" / "caution" / "avoid"
    quality_score: float                       # -1.0 to +1.0


def compute_advanced_transit(
    planet: str,
    transit_sign: int,
    transit_nakshatra_idx: int,
    natal_chart,
    sensitive_points: Optional[dict] = None,
) -> AdvancedTransitResult:
    """
    Comprehensive transit quality assessment.
    """
    natal_moon_si   = natal_chart.planets["Moon"].sign_index if "Moon" in natal_chart.planets else 0
    natal_moon_nak  = int(natal_chart.planets["Moon"].longitude * 3 / 40) if "Moon" in natal_chart.planets else 0

    # Tarabala
    tb = tarabala(natal_moon_nak, transit_nakshatra_idx)

    # Chandrabala (for Moon transits especially)
    cb = chandrabala(natal_moon_si, transit_sign)

    # Ashtama Shani
    is_ashtama_shani = (planet == "Saturn" and
                        ((transit_sign - natal_moon_si) % 12) + 1 == 8)

    # Chandra Shtama
    is_chandra_shtama = chandra_shtama(natal_moon_si, planet, transit_sign)

    # Sensitive point hits
    if sensitive_points is None:
        sensitive_points = compute_sensitive_points(natal_chart)

    transit_lon = transit_sign * 30 + 15  # midpoint of sign
    sp_hits = is_transiting_sensitive_point(transit_lon, sensitive_points)

    # Score
    score = 0.0
    if tb["is_auspicious"]: score += 0.3
    else: score -= 0.3
    if cb["is_favorable"]: score += 0.2
    elif cb["chandrabala_dosha"]: score -= 0.2
    if is_ashtama_shani: score -= 0.5
    if any(sp_hits.values()): score -= 0.3

    score = max(-1.0, min(1.0, score))

    if score >= 0.4:     quality = "excellent"
    elif score >= 0.1:   quality = "good"
    elif score >= -0.1:  quality = "neutral"
    elif score >= -0.4:  quality = "caution"
    else:                quality = "avoid"

    return AdvancedTransitResult(
        planet=planet,
        transit_sign=transit_sign,
        transit_nakshatra_idx=transit_nakshatra_idx,
        tarabala=tb,
        chandrabala=cb,
        ashtama_shani=is_ashtama_shani,
        chandra_shtama=is_chandra_shtama,
        sensitive_point_hits=sp_hits,
        overall_quality=quality,
        quality_score=round(score, 3),
    )
