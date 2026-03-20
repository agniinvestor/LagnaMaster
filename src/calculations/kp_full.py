"""
src/calculations/kp_full.py — Session 44

Full KP (Krishnamurti Paddhati) engine:
  - Sub-lord chain: sign lord → nakshatra lord → sub-lord → sub-sub-lord
  - Cuspal sub-lords for all 12 houses (requires birth time)
  - Significators per house with sub-lord promise evaluation
  - Ruling Planets (RP) method: current dasha/transit lords

Public API
----------
  kp_sub_lord_chain(longitude) -> KPChain
  compute_kp_cusps(chart)      -> list[KPCusp]  (12 house cusps)
  kp_ruling_planets(chart, on_date) -> list[str]
  kp_event_promise(chart, house, on_date) -> KPPromise
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date

# Vimshottari sequence for sub-lord calculation
_VIM_SEQ = ["Ketu","Venus","Sun","Moon","Mars","Rahu",
            "Jupiter","Saturn","Mercury"]
_VIM_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,
              "Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}

# Each nakshatra = 13°20' = 800'/60 degrees
_NAK_SPAN = 360 / 27          # 13.3333°
_SUB_SPAN_DEG = {p: _NAK_SPAN * y / 120 for p, y in _VIM_YEARS.items()}


def _sub_at(longitude: float) -> tuple[str, str, str, str]:
    """Return (sign_lord, nak_lord, sub_lord, sub_sub_lord) for any longitude."""
    _SIGN_LORD = {0:"Mars",1:"Venus",2:"Mercury",3:"Moon",4:"Sun",5:"Mercury",
                  6:"Venus",7:"Mars",8:"Jupiter",9:"Saturn",10:"Saturn",11:"Jupiter"}
    _NAK_LORD  = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"] * 3

    lon = longitude % 360
    si  = int(lon / 30)
    sign_lord = _SIGN_LORD[si]

    nak_idx = int(lon / _NAK_SPAN) % 27
    nak_lord = _NAK_LORD[nak_idx]

    # Position within nakshatra
    pos_in_nak = lon - nak_idx * _NAK_SPAN

    # Find sub-lord: cumulative spans within nakshatra
    # Sub-lord sequence starts from the nakshatra lord
    start_idx = _VIM_SEQ.index(nak_lord)
    cumulative = 0.0
    sub_lord = nak_lord
    sub_sub_lord = nak_lord
    for i in range(9):
        planet = _VIM_SEQ[(start_idx + i) % 9]
        span = _SUB_SPAN_DEG[planet]
        if cumulative + span > pos_in_nak:
            sub_lord = planet
            # Sub-sub: further divide
            pos_in_sub = pos_in_nak - cumulative
            start_j = _VIM_SEQ.index(planet)
            sub_span = span
            cum_j = 0.0
            for j in range(9):
                pl_j = _VIM_SEQ[(start_j + j) % 9]
                sub_sub_span = _SUB_SPAN_DEG[pl_j] * span / _NAK_SPAN
                if cum_j + sub_sub_span > pos_in_sub:
                    sub_sub_lord = pl_j
                    break
                cum_j += sub_sub_span
            break
        cumulative += span

    return sign_lord, nak_lord, sub_lord, sub_sub_lord


@dataclass
class KPChain:
    longitude: float
    sign_lord: str
    nak_lord: str
    sub_lord: str
    sub_sub_lord: str

    def lords(self) -> list[str]:
        return [self.sign_lord, self.nak_lord, self.sub_lord, self.sub_sub_lord]


def kp_sub_lord_chain(longitude: float) -> KPChain:
    sl, nl, sub, ss = _sub_at(longitude)
    return KPChain(longitude=round(longitude % 360, 4),
                   sign_lord=sl, nak_lord=nl, sub_lord=sub, sub_sub_lord=ss)


@dataclass
class KPCusp:
    house: int
    longitude: float
    sign_lord: str
    nak_lord: str
    sub_lord: str
    sub_sub_lord: str
    significators: list[str] = field(default_factory=list)


def compute_kp_cusps(chart) -> list[KPCusp]:
    """
    Compute KP sub-lord chain for all 12 house cusps.
    Uses Whole Sign cusps (lagna degree projected across signs).
    For full Placidus: would require pyswisseph swe.houses() with 'P' system.
    """
    lagna_lon = chart.lagna % 360
    cusps = []
    for h in range(1, 13):
        cusp_lon = (lagna_lon + (h - 1) * 30) % 360
        sl, nl, sub, ss = _sub_at(cusp_lon)
        cusps.append(KPCusp(
            house=h, longitude=round(cusp_lon, 4),
            sign_lord=sl, nak_lord=nl, sub_lord=sub, sub_sub_lord=ss,
        ))
    return cusps


def kp_ruling_planets(chart, on_date: date | None = None) -> list[str]:
    """
    Ruling Planets: lords of current day, Moon's sign, Moon's nakshatra,
    Moon's sub-lord, Lagna sign lord, Lagna nakshatra lord.
    """
    if on_date is None:
        on_date = date.today()
    rps = set()

    # Lagna chain
    chain = kp_sub_lord_chain(chart.lagna)
    rps.update([chain.sign_lord, chain.nak_lord, chain.sub_lord])

    # Moon chain
    moon_lon = chart.planets["Moon"].longitude
    mchain = kp_sub_lord_chain(moon_lon)
    rps.update([mchain.sign_lord, mchain.nak_lord, mchain.sub_lord])

    # Day lord (weekday)
    _DAY_LORD = {0:"Moon",1:"Mars",2:"Mercury",3:"Jupiter",
                 4:"Venus",5:"Saturn",6:"Sun"}
    rps.add(_DAY_LORD[on_date.weekday()])

    return sorted(rps)


@dataclass
class KPPromise:
    house: int
    sub_lord: str
    signifies_house: bool
    ruling_planets: list[str]
    promise_level: str   # "Strong"/"Moderate"/"Weak"
    reason: str


def kp_event_promise(chart, house: int, on_date: date | None = None) -> KPPromise:
    """
    KP event promise for a house: checks if cusp sub-lord signifies the house
    through its own placement and ownership.
    """
    if on_date is None:
        on_date = date.today()
    cusps = compute_kp_cusps(chart)
    cusp = cusps[house - 1]
    rps = kp_ruling_planets(chart, on_date)

    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)

    sub = cusp.sub_lord
    sub_house = hmap.planet_house.get(sub, 0)
    sub_owns = [h for h in range(1, 13) if hmap.house_lord[h-1] == sub]

    signifies = (sub_house == house or house in sub_owns)
    in_rp = sub in rps

    if signifies and in_rp:
        level = "Strong"
        reason = f"Sub-lord {sub} signifies H{house} AND is a Ruling Planet"
    elif signifies:
        level = "Moderate"
        reason = f"Sub-lord {sub} signifies H{house} but not in Ruling Planets"
    else:
        level = "Weak"
        reason = f"Sub-lord {sub} does not directly signify H{house}"

    return KPPromise(house=house, sub_lord=sub, signifies_house=signifies,
                     ruling_planets=rps, promise_level=level, reason=reason)
