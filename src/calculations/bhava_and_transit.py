"""
src/calculations/bhava_and_transit.py
Bhava Chalita overlay + Transit corrections (Vedha, Moon/Sun lagna, Ashtama Shani).

Session 118: Bhava Chalita chart (BPHS Ch.6; BV Raman HJH Vol.1)
Session 122: Vedha obstruction table, transit from Moon + Sun lagna, Ashtama Shani
             (Phaladeepika Ch.26 v.1-18; K.N. Rao, Yogis Destiny Ch.7)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# ─── Bhava Chalita ───────────────────────────────────────────────────────────

@dataclass
class BhavaChalitaMap:
    """
    Bhava Chalita house assignments for all planets.
    Differs from whole-sign when planets are near sign boundaries.
    Source: BPHS Ch.6; BV Raman, How to Judge a Horoscope Vol.1 p.12-14
    """
    bhava_cusps: list[float]             # 12 cusp longitudes
    planet_bhava: dict[str, int]         # planet -> bhava house (1-12)
    lagna_bhava_sign: int                # sign containing bhava cusp 1
    divergent_planets: list[str]         # planets whose bhava differs from whole-sign house


def compute_bhava_chalita(chart, midheaven_lon: Optional[float] = None) -> BhavaChalitaMap:
    """
    Compute Bhava Chalita equal-house chart from Midheaven (MC).
    If midheaven_lon not provided, approximates from Lagna.
    Source: BPHS Ch.6
    """
    if midheaven_lon is None:
        # Approximate: MC ≈ Lagna + 90° (simplified for systems without swe.houses())
        midheaven_lon = (chart.lagna + 90.0) % 360.0

    # 12 equal Bhava cusps from MC
    # Bhava 10 cusp = MC, other cusps at 30° intervals
    # H1 cusp (Lagna Bhava) = MC - 90° ≈ Ascendant
    h10_cusp = midheaven_lon
    cusps = [(h10_cusp + (i - 9) * 30.0) % 360.0 for i in range(12)]

    # Assign each planet to a Bhava
    def bhava_of(longitude: float) -> int:
        """Find which bhava contains this longitude."""
        for i in range(12):
            cusp_start = cusps[i]
            cusp_end = cusps[(i + 1) % 12]
            if cusp_start <= cusp_end:
                if cusp_start <= longitude < cusp_end:
                    return i + 1
            else:  # wraps around 360
                if longitude >= cusp_start or longitude < cusp_end:
                    return i + 1
        return 1

    planet_bhava: dict[str, int] = {}
    divergent = []

    for name, planet in chart.planets.items():
        bhava = bhava_of(planet.longitude)
        planet_bhava[name] = bhava
        # Compare with whole-sign house
        whole_sign_house = (planet.sign_index - chart.lagna_sign_index) % 12 + 1
        if bhava != whole_sign_house:
            divergent.append(name)

    return BhavaChalitaMap(
        bhava_cusps=[round(c, 4) for c in cusps],
        planet_bhava=planet_bhava,
        lagna_bhava_sign=int(cusps[0] / 30) % 12,
        divergent_planets=divergent,
    )


# ─── Vedha obstruction table ─────────────────────────────────────────────────
# Source: Phaladeepika Ch.26 v.10-18
# {transit_house: obstructing_house}

VEDHA_PAIRS: dict[int, int] = {
    1: 5,   2: 12,  3: 12,  4: 3,
    5: 9,   6: 12,  7: 2,   8: 5,
    9: 8,   10: 9,  11: 8,  12: 6,
}


def is_vedha_blocked(
    planet_transit_house: int,
    all_transit_houses: dict[str, int],
    planet_name: str,
) -> tuple[bool, Optional[str]]:
    """
    Check if a transit is Vedha-blocked.
    Returns (is_blocked, blocking_planet_name or None).
    Source: Phaladeepika Ch.26 v.10-18

    'When Saturn is in a good transit house but another planet simultaneously
    occupies its Vedha house, the good results are obstructed.'
    """
    obstructing_house = VEDHA_PAIRS.get(planet_transit_house)
    if obstructing_house is None:
        return False, None

    for other_planet, other_house in all_transit_houses.items():
        if other_planet == planet_name:
            continue
        if other_house == obstructing_house:
            return True, other_planet

    return False, None


# ─── Transit from multiple reference points ───────────────────────────────────
# Source: Phaladeepika Ch.26 v.1-5; BV Raman, HJH Vol.2

@dataclass
class TransitQuality:
    """Transit quality assessed from a single reference point."""
    reference: str          # "Lagna" / "Moon" / "Sun"
    reference_sign: int
    transit_house: int      # house number from this reference
    is_good_house: bool     # classical good/bad house for this planet
    vedha_blocked: bool
    vedha_blocker: Optional[str]
    av_bindus: int


@dataclass
class FullTransitReport:
    """
    Transit quality from all 3 reference points.
    Source: Phaladeepika Ch.26 v.1-5
    'When all three agree, the result is certain;
     when two agree, it is likely; when only one, it is possible.'
    """
    planet: str
    transit_sign: int
    from_lagna: TransitQuality
    from_moon: TransitQuality
    from_sun: TransitQuality
    agreement_count: int    # how many references agree on good/bad
    consensus: str          # "Certain" / "Likely" / "Possible" / "Uncertain"
    ashtama_shani: bool     # Saturn in H8 from natal Moon


# Classical good/bad transit houses by planet
# Source: Phaladeepika Ch.26; BPHS transit chapters
GOOD_TRANSIT_HOUSES: dict[str, set[int]] = {
    "Sun":     {3, 6, 10, 11},
    "Moon":    {1, 3, 6, 7, 10, 11},
    "Mars":    {3, 6, 11},
    "Mercury": {2, 4, 6, 8, 10, 11},
    "Jupiter": {2, 5, 7, 9, 11},
    "Venus":   {1, 2, 3, 4, 5, 8, 9, 11, 12},
    "Saturn":  {3, 6, 11},
    "Rahu":    {3, 6, 11},
    "Ketu":    {3, 6, 11},
}


def compute_full_transit(
    planet: str,
    transit_sign: int,
    natal_chart,
    transit_chart,
    av_bindus: int = -1,
) -> FullTransitReport:
    """
    Assess transit quality from Lagna, Moon, and Sun reference points.
    Source: Phaladeepika Ch.26 v.1-5
    """
    # Compute transit houses from each reference
    natal_lagna_si = natal_chart.lagna_sign_index
    natal_moon_si  = natal_chart.planets["Moon"].sign_index if "Moon" in natal_chart.planets else natal_lagna_si
    natal_sun_si   = natal_chart.planets["Sun"].sign_index  if "Sun"  in natal_chart.planets else natal_lagna_si

    # All planet transit houses (from Lagna) for Vedha check
    all_transit_from_lagna = {
        p: (transit_chart.planets[p].sign_index - natal_lagna_si) % 12 + 1
        for p in transit_chart.planets
    }
    all_transit_from_moon = {
        p: (transit_chart.planets[p].sign_index - natal_moon_si) % 12 + 1
        for p in transit_chart.planets
    }
    all_transit_from_sun = {
        p: (transit_chart.planets[p].sign_index - natal_sun_si) % 12 + 1
        for p in transit_chart.planets
    }

    good_houses = GOOD_TRANSIT_HOUSES.get(planet, set())

    def make_quality(ref: str, ref_si: int, transit_houses: dict[str, int]) -> TransitQuality:
        h = (transit_sign - ref_si) % 12 + 1
        blocked, blocker = is_vedha_blocked(h, transit_houses, planet)
        return TransitQuality(
            reference=ref,
            reference_sign=ref_si,
            transit_house=h,
            is_good_house=(h in good_houses),
            vedha_blocked=blocked,
            vedha_blocker=blocker,
            av_bindus=av_bindus,
        )

    from_lagna = make_quality("Lagna", natal_lagna_si, all_transit_from_lagna)
    from_moon  = make_quality("Moon",  natal_moon_si,  all_transit_from_moon)
    from_sun   = make_quality("Sun",   natal_sun_si,   all_transit_from_sun)

    # Count agreement (good houses not blocked by Vedha)
    effective = [
        q for q in [from_lagna, from_moon, from_sun]
        if not q.vedha_blocked
    ]
    good_count = sum(1 for q in effective if q.is_good_house)
    agreement_count = good_count if good_count >= 2 else (3 - good_count if good_count == 0 else 1)

    if agreement_count == 3:
        consensus = "Certain"
    elif agreement_count == 2:
        consensus = "Likely"
    elif agreement_count == 1:
        consensus = "Possible"
    else:
        consensus = "Uncertain"

    # Ashtama Shani: Saturn in H8 from natal Moon
    # Source: K.N. Rao, Yogis Destiny Ch.7
    ashtama = (
        planet == "Saturn" and
        (transit_sign - natal_moon_si) % 12 + 1 == 8
    )

    return FullTransitReport(
        planet=planet,
        transit_sign=transit_sign,
        from_lagna=from_lagna,
        from_moon=from_moon,
        from_sun=from_sun,
        agreement_count=agreement_count,
        consensus=consensus,
        ashtama_shani=ashtama,
    )
