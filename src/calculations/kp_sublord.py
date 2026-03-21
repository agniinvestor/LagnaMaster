"""
src/calculations/kp_sublord.py
KP (Krishnamurti Paddhati) sub-lord system.
249-division nakshatra sub-lord table + nakshatra/sub-lord computation.
Session 155 (Audit K-2).

KP divides the 27 nakshatras into 249 sub-divisions proportional to
Vimshottari dasha periods. The sub-lord of a planet/cusp is the key
determinant of house activation.

Sources:
  K.S. Krishnamurti · Reader Series Vol. 1-6 (Krishnamurti Publications)
  KP system requires: ayanamsha='krishnamurti', node_mode='true'
"""
from __future__ import annotations
from dataclasses import dataclass

# ─── Vimshottari dasha years (classic sequence) ───────────────────────────────
_DASHA_YEARS: dict[str, float] = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
_DASHA_ORDER = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
_TOTAL_YEARS = 120.0

# Nakshatra span = 13.333...° each, total 27 nakshatras
_NAK_SPAN = 360.0 / 27  # 13.3333...°
_NAK_NAMES = [
    "Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu",
    "Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta",
    "Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha",
    "Uttara Ashadha","Shravana","Dhanishtha","Shatabhisha","Purva Bhadrapada",
    "Uttara Bhadrapada","Revati",
]

# Nakshatra to star-lord mapping (9-planet sequence repeating)
_NAK_LORD_IDX = [i % 9 for i in range(27)]  # maps nak_idx → dasha_order idx
_NAK_STAR_LORDS = [_DASHA_ORDER[i % 9] for i in range(27)]


@dataclass
class SubLordEntry:
    """One entry in the KP 249 sub-lord table."""
    star_lord: str          # Nakshatra lord
    sub_lord: str           # Sub-lord (Vimshottari subdivision)
    start_lon: float        # Start longitude (0-360°)
    end_lon: float          # End longitude
    sub_sub_lord: str = ""  # Optional 3rd level


def _build_sublord_table() -> list[SubLordEntry]:
    """
    Build the KP 249 sub-lord table.
    Each nakshatra (13.333°) is divided into 9 sub-divisions
    proportional to Vimshottari years.

    Source: K.S. Krishnamurti Reader Series Vol.1
    """
    table = []
    for nak_idx in range(27):
        star_lord = _NAK_STAR_LORDS[nak_idx]
        nak_start = nak_idx * _NAK_SPAN

        # Sub-lords start from the same planet as the nakshatra lord
        sl_start_idx = _DASHA_ORDER.index(star_lord)

        for sub_idx in range(9):
            sl_planet = _DASHA_ORDER[(sl_start_idx + sub_idx) % 9]
            sl_years = _DASHA_YEARS[sl_planet]
            sub_span = _NAK_SPAN * (sl_years / _TOTAL_YEARS)

            start = nak_start + sum(
                _NAK_SPAN * _DASHA_YEARS[_DASHA_ORDER[(sl_start_idx + i) % 9]] / _TOTAL_YEARS
                for i in range(sub_idx)
            )
            end = start + sub_span

            table.append(SubLordEntry(
                star_lord=star_lord,
                sub_lord=sl_planet,
                start_lon=round(start, 6),
                end_lon=round(end, 6),
            ))

    return table


# Build table once at module load
KP_SUBLORD_TABLE: list[SubLordEntry] = _build_sublord_table()


def get_sublord(longitude: float) -> SubLordEntry:
    """
    Get the KP sub-lord for a given sidereal longitude.
    longitude: 0-360° sidereal

    Source: K.S. Krishnamurti Reader Series Vol.1
    """
    lon = longitude % 360.0
    for entry in KP_SUBLORD_TABLE:
        if entry.start_lon <= lon < entry.end_lon:
            return entry
    # Handle last entry boundary
    return KP_SUBLORD_TABLE[-1]


def get_star_lord(longitude: float) -> str:
    """Returns the Nakshatra (star) lord for a longitude."""
    nak_idx = int(longitude * 3 / 40) % 27
    return _NAK_STAR_LORDS[nak_idx]


@dataclass
class KPSignificators:
    """KP significators for a planet or cusp."""
    planet: str
    longitude: float
    house_occupied: int
    house_owned: list[int]
    star_lord: str
    sub_lord: str
    star_lord_house: int       # house occupied by star lord
    sub_lord_house: int        # house occupied by sub lord
    signified_houses: set[int] # all houses signified via KP theory


def compute_kp_significators(planet: str, longitude: float, chart) -> KPSignificators:
    """
    Compute KP significators for a planet.

    A planet signifies:
    1. The house it occupies (Bhava)
    2. The houses it owns (Rashi)
    3. The houses occupied and owned by its star lord
    4. The houses occupied and owned by its sub lord

    Source: K.S. Krishnamurti Reader Series Vol.2 (Significators)
    """
    lagna_si = chart.lagna_sign_index
    lon = longitude % 360.0

    # House occupied
    si = int(lon / 30) % 12
    house_occ = (si - lagna_si) % 12 + 1

    # Houses owned
    _SL = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",
           5:"Mercury",6:"Venus",7:"Mars",8:"Jupiter",
           9:"Saturn",10:"Saturn",11:"Jupiter"}
    houses_owned = [h for h in range(1,13) if _SL.get((lagna_si+h-1)%12) == planet]

    # Star lord and sub lord
    sl_entry = get_sublord(lon)
    star_lord = sl_entry.star_lord
    sub_lord = sl_entry.sub_lord

    def _planet_house(p: str) -> int:
        if p in chart.planets:
            p_si = chart.planets[p].sign_index
            return (p_si - lagna_si) % 12 + 1
        return 0

    sl_house = _planet_house(star_lord)
    sub_house = _planet_house(sub_lord)

    sl_owned = [h for h in range(1,13) if _SL.get((lagna_si+h-1)%12) == star_lord]
    sub_owned = [h for h in range(1,13) if _SL.get((lagna_si+h-1)%12) == sub_lord]

    all_houses = set([house_occ] + houses_owned)
    if sl_house: all_houses.add(sl_house)
    all_houses.update(sl_owned)
    if sub_house: all_houses.add(sub_house)
    all_houses.update(sub_owned)

    return KPSignificators(
        planet=planet,
        longitude=lon,
        house_occupied=house_occ,
        house_owned=houses_owned,
        star_lord=star_lord,
        sub_lord=sub_lord,
        star_lord_house=sl_house,
        sub_lord_house=sub_house,
        signified_houses=all_houses,
    )


# ─── KP Ruling Planets ────────────────────────────────────────────────────────

def compute_ruling_planets(chart, query_datetime=None) -> list[str]:
    """
    KP Ruling Planets at moment of judgment.
    Consists of:
    - Lagna star lord
    - Lagna sub lord
    - Moon star lord
    - Moon sub lord
    - Day lord (weekday)

    Source: K.S. Krishnamurti Reader Series Vol.4
    """
    lagna_lon = chart.lagna
    moon_lon  = chart.planets["Moon"].longitude if "Moon" in chart.planets else 0.0

    lagna_sl = get_sublord(lagna_lon)
    moon_sl  = get_sublord(moon_lon)

    ruling = list(dict.fromkeys([
        lagna_sl.star_lord, lagna_sl.sub_lord,
        moon_sl.star_lord, moon_sl.sub_lord,
    ]))

    # Add day lord if datetime provided
    if query_datetime is not None:
        day_lords = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
        day_lord = day_lords[query_datetime.weekday() % 7]
        if day_lord not in ruling:
            ruling.append(day_lord)

    return ruling
