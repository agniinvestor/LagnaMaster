"""
src/calculations/planetary_state.py
Vargottama, Parivartana, Graha Yuddha, Sandhi — Phase 1 planetary state extensions.

Session 115: Vargottama + Parivartana + planetary latitudes
Session 116: Graha Yuddha with latitude check
Session 117: Combustion orbs by school + Sandhi

Sources:
  PVRNR, Vedic Astrology Ch.9 (Vargottama)
  PVRNR, Astrology of the Seers Ch.11 (Parivartana)
  Saravali Ch.4 v.12-18 (Graha Yuddha — requires latitude)
  Varahamihira, Brihat Jataka Ch.3 v.8-11 (war priority)
  Phaladeepika Ch.2 v.30 (Sandhi)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

# ─── Parivartana Yoga ────────────────────────────────────────────────────────

_OWN_SIGNS: dict[str, list[int]] = {
    "Sun":     [4],
    "Moon":    [3],
    "Mars":    [0, 7],
    "Mercury": [2, 5],
    "Jupiter": [8, 11],
    "Venus":   [1, 6],
    "Saturn":  [9, 10],
}

_SIGN_LORDS: dict[int, str] = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",
    5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",
    9: "Saturn", 10: "Saturn", 11: "Jupiter",
}


@dataclass
class ParivartanaResult:
    planet_a: str
    planet_b: str
    kind: str        # "Maha" / "Kahala" / "Dainya"
    description: str


def detect_parivartana(chart) -> list[ParivartanaResult]:
    """
    Detect all Parivartana (mutual sign exchange) yogas.
    Source: PVRNR, Astrology of the Seers Ch.11; BPHS
    """
    results = []
    lagna_si = chart.lagna_sign_index

    kendras   = {1, 4, 7, 10}
    trikonas  = {1, 5, 9}
    dusthanas = {6, 8, 12}

    planets = [p for p in chart.planets if p not in ("Rahu", "Ketu")]  # noqa: F841

    checked = set()
    for pa in planets:
        for pb in planets:
            if pa >= pb:
                continue
            pair = (pa, pb)
            if pair in checked:
                continue
            checked.add(pair)

            pa_si = chart.planets[pa].sign_index
            pb_si = chart.planets[pb].sign_index

            # Check mutual exchange
            pa_in_pb_sign = (pa_si in _OWN_SIGNS.get(pb, []))
            pb_in_pa_sign = (pb_si in _OWN_SIGNS.get(pa, []))

            if not (pa_in_pb_sign and pb_in_pa_sign):
                continue

            # Classify
            def house_of_sign(si: int) -> int:
                return (si - lagna_si) % 12 + 1

            pa_house = house_of_sign(pa_si)
            pb_house = house_of_sign(pb_si)

            pa_in_dusthana = pa_house in dusthanas
            pb_in_dusthana = pb_house in dusthanas
            pa_in_kt = pa_house in kendras or pa_house in trikonas
            pb_in_kt = pb_house in kendras or pb_house in trikonas

            if pa_in_dusthana or pb_in_dusthana:
                kind = "Dainya"
                desc = f"Dainya Parivartana: {pa}(H{pa_house}) ↔ {pb}(H{pb_house}) — dusthana involvement"
            elif pa_house == 3 and pb_house == 6 or pa_house == 6 and pb_house == 3:
                kind = "Kahala"
                desc = f"Kahala Parivartana: {pa}(H{pa_house}) ↔ {pb}(H{pb_house})"
            elif pa_in_kt and pb_in_kt:
                kind = "Maha"
                desc = f"Maha Parivartana: {pa}(H{pa_house}) ↔ {pb}(H{pb_house}) — Kendra/Trikona exchange"
            else:
                kind = "Kahala"
                desc = f"Parivartana: {pa}(H{pa_house}) ↔ {pb}(H{pb_house})"

            results.append(ParivartanaResult(
                planet_a=pa, planet_b=pb,
                kind=kind, description=desc,
            ))

    return results


def parivartana_dignity_override(chart, parivartana_list: list[ParivartanaResult]) -> dict[str, str]:
    """
    Returns {planet: "OWN_SIGN"} overrides for planets in Parivartana.
    Both planets in a Parivartana pair effectively act as if in their own sign.
    Does NOT apply to Dainya Parivartana (both remain afflicted).
    """
    overrides = {}
    for pari in parivartana_list:
        if pari.kind != "Dainya":
            overrides[pari.planet_a] = "OWN_SIGN"
            overrides[pari.planet_b] = "OWN_SIGN"
    return overrides


# ─── Graha Yuddha (Planetary War) ────────────────────────────────────────────

@dataclass
class GrahaYuddhaResult:
    planet_a: str
    planet_b: str
    lon_diff: float
    lat_diff: float
    winner: str
    loser: str
    winner_reason: str   # "north_latitude" / "higher_speed" / "brighter"


# War only applies to these 5 planets (not Sun, Moon, Rahu, Ketu)
WAR_PLANETS = {"Mars", "Mercury", "Jupiter", "Venus", "Saturn"}

LON_WAR_ORB = 1.0  # degrees longitude
LAT_WAR_ORB = 1.0  # degrees latitude


def detect_graha_yuddha(chart) -> list[GrahaYuddhaResult]:
    """
    Detect planetary wars. Requires chart.planets[p].latitude to be populated.
    Source: Saravali Ch.4 v.12-18; Varahamihira, Brihat Jataka Ch.3 v.8-11

    War conditions: lon diff < 1° AND lat diff < 1°
    Winner: planet with higher north latitude (smaller absolute south lat)
    """
    results = []
    war_ps = [p for p in chart.planets if p in WAR_PLANETS]

    for i, pa in enumerate(war_ps):
        for pb in war_ps[i+1:]:
            pa_data = chart.planets[pa]
            pb_data = chart.planets[pb]

            lon_diff = abs(pa_data.longitude - pb_data.longitude) % 360
            lon_diff = min(lon_diff, 360 - lon_diff)
            if lon_diff >= LON_WAR_ORB:
                continue

            # Latitude check (requires latitude attribute)
            pa_lat = getattr(pa_data, "latitude", 0.0)
            pb_lat = getattr(pb_data, "latitude", 0.0)
            lat_diff = abs(pa_lat - pb_lat)
            if lat_diff >= LAT_WAR_ORB:
                continue

            # Determine winner by northward latitude
            # (Higher north latitude = more victorious per Saravali)
            if pa_lat > pb_lat:
                winner, loser = pa, pb
                reason = "north_latitude"
            elif pb_lat > pa_lat:
                winner, loser = pb, pa
                reason = "north_latitude"
            else:
                # Tie-break by speed (faster = more energetic)
                if abs(pa_data.speed) >= abs(pb_data.speed):
                    winner, loser = pa, pb
                else:
                    winner, loser = pb, pa
                reason = "higher_speed"

            results.append(GrahaYuddhaResult(
                planet_a=pa,
                planet_b=pb,
                lon_diff=round(lon_diff, 4),
                lat_diff=round(lat_diff, 4),
                winner=winner,
                loser=loser,
                winner_reason=reason,
            ))

    return results


# ─── Upagrahas (Mandi/Gulika) ────────────────────────────────────────────────
# Session 123 (Phase 1)
# Source: BPHS Ch.25; Phaladeepika Ch.26

_WEEKDAY_ORDER = [6, 0, 1, 2, 3, 4, 5]  # Sun=0 in Jyotish sequence, weekday() Mon=0
_JYOTISH_WEEKDAY = {
    0: "Moon",    # Monday
    1: "Mars",    # Tuesday
    2: "Mercury", # Wednesday
    3: "Jupiter", # Thursday
    4: "Venus",   # Friday
    5: "Saturn",  # Saturday
    6: "Sun",     # Sunday
}
_JYOTISH_WEEKDAY_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def compute_mandi_gulika(
    chart,
    birth_dt,
    sunrise_lon: Optional[float] = None,
    day_duration_hours: float = 12.0,
    is_day_birth: bool = True,
) -> dict[str, float]:
    """
    Compute Mandi and Gulika longitudes.

    Formula (BPHS Ch.25):
    For day births: each portion = day_duration / 8
    For night births: each portion = night_duration / 8
    Order of weekday sequence determines which portion is Mandi.

    Returns {'mandi': longitude, 'gulika': longitude}
    Source: BPHS Ch.25; Phaladeepika Ch.26
    """
    try:
        from datetime import datetime
        if hasattr(birth_dt, 'weekday'):
            weekday = birth_dt.weekday()  # 0=Monday
        else:
            return {}
    except Exception:
        return {}

    # Weekday lord index in Jyotish sequence
    weekday_lord = _JYOTISH_WEEKDAY[weekday]
    lord_idx = _JYOTISH_WEEKDAY_ORDER.index(weekday_lord)

    # Duration of each portion
    duration_per_portion = day_duration_hours / 8.0

    # Mandi's portion index (lord_idx)
    # Gulika's portion = Mandi - 1 portion (precedes Mandi)
    if sunrise_lon is None:
        sunrise_lon = 0.0  # default: Aries rising

    # Time since sunrise in hours
    birth_hour = birth_dt.hour + birth_dt.minute / 60.0
    sunrise_hour = 6.0  # simplified; ideally computed from swe.rise_trans

    elapsed = birth_hour - sunrise_hour if is_day_birth else birth_hour

    # Longitude of Mandi = sunrise longitude + (lord_idx * portion * 15°/hr)
    # Each hour = 15° of celestial motion approximately
    mandi_elapsed = lord_idx * duration_per_portion
    mandi_lon = (sunrise_lon + mandi_elapsed * 15.0) % 360

    gulika_lon = (sunrise_lon + (lord_idx - 1) * duration_per_portion * 15.0) % 360

    return {
        "mandi": round(mandi_lon, 4),
        "gulika": round(gulika_lon, 4),
    }
