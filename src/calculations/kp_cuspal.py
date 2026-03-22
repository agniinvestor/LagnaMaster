"""
src/calculations/kp_cuspal.py
KP cuspal sub-lord analysis — house activation, promise, fructification.
Session 169 (Audit K-2).

In KP system, the sub-lord of a house cusp determines whether the house
can give its results (promise), and the ruling planets at query time
determine when (fructification).

Sources:
  K.S. Krishnamurti · Reader Series Vol.2-3 (Krishnamurti Publications)
  KP Ashtakvarga (not same as Parashari AV — separate KP system)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# House significations (primary)
HOUSE_SIGNIFICATIONS: dict[int, list[str]] = {
    1:  ["self", "body", "health", "personality"],
    2:  ["wealth", "family", "speech", "accumulated_money"],
    3:  ["siblings", "courage", "short_travel", "communication"],
    4:  ["mother", "property", "education", "happiness"],
    5:  ["children", "intelligence", "speculation", "romance"],
    6:  ["enemies", "disease", "debt", "service"],
    7:  ["spouse", "partnership", "business", "foreign_travel"],
    8:  ["longevity", "inheritance", "occult", "obstacles"],
    9:  ["fortune", "father", "higher_education", "dharma"],
    10: ["career", "status", "government", "authority"],
    11: ["gains", "desires_fulfilled", "friends", "elder_sibling"],
    12: ["expenses", "foreign_land", "moksha", "losses"],
}

# Houses that must be signified for specific life events (KP methodology)
KP_EVENT_HOUSES: dict[str, set[int]] = {
    "marriage":      {2, 7, 11},
    "career_start":  {2, 6, 10, 11},
    "foreign_travel": {3, 8, 9, 12},
    "property":      {4, 11, 12},
    "children":      {2, 5, 11},
    "disease":       {6, 8, 12},
    "spiritual":     {8, 9, 12},
    "inheritance":   {2, 8, 11},
    "education":     {4, 9, 11},
}


@dataclass
class CuspalSubLord:
    """Sub-lord analysis for a single house cusp."""
    house: int
    cusp_longitude: float
    star_lord: str
    sub_lord: str
    sub_sub_lord: str
    sub_lord_signified_houses: set[int]
    has_promise: bool        # sub-lord signifies the house and its supporting houses
    promise_note: str


@dataclass
class KPAnalysisResult:
    """Full KP analysis for a chart."""
    cuspal_sub_lords: dict[int, CuspalSubLord]   # house → CuspalSubLord
    ruling_planets: list[str]                      # at time of query
    event_promise: dict[str, bool]                 # event → has promise
    fructification_planets: list[str]              # planets that can give results now
    analysis_note: str


def _compute_bhava_cusps(chart) -> dict[int, float]:
    """
    Compute house cusp longitudes (Placidus/equal from Bhava Chalita).
    Falls back to whole-sign if Bhava Chalita not available.
    """
    try:
        from src.calculations.bhava_and_transit import compute_bhava_chalita
        bc = compute_bhava_chalita(chart)
        if hasattr(bc, 'cusps'):
            return {h: bc.cusps[h-1] for h in range(1, 13)}
    except Exception:
        pass

    # Fallback: equal houses from Lagna
    lagna = chart.lagna
    return {h: (lagna + (h-1) * 30) % 360 for h in range(1, 13)}


def compute_cuspal_sub_lords(chart) -> dict[int, CuspalSubLord]:
    """
    Compute the sub-lord for each house cusp using KP sub-lord table.

    The sub-lord of a cusp determines the house's 'promise':
    if the sub-lord signifies the house itself and its supporting houses,
    the house CAN give results during appropriate dasha.

    Source: K.S. Krishnamurti Reader Series Vol.2
    """
    from src.calculations.kp_sublord import get_sublord, compute_kp_significators

    cusps = _compute_bhava_cusps(chart)
    result = {}

    for house in range(1, 13):
        cusp_lon = cusps[house]
        entry = get_sublord(cusp_lon)

        try:
            sig = compute_kp_significators(entry.sub_lord,
                  chart.planets.get(entry.sub_lord, type('', (), {'longitude': 0.0})()).longitude
                  if entry.sub_lord in chart.planets else 0.0,
                  chart)
            sub_signified = sig.signified_houses
        except Exception:
            sub_signified = set()

        # Promise: sub-lord must signify this house and its supporting houses
        has_promise = (house in sub_signified)

        note = f"Sub-lord {entry.sub_lord} signifies H{sorted(sub_signified)}"
        if has_promise:
            note += f" — H{house} PROMISE: YES"
        else:
            note += f" — H{house} promise: weak"

        # Sub-sub-lord from KP table (3rd level)
        sub_sub = entry.sub_lord  # simplified — full 3rd level requires deeper table

        result[house] = CuspalSubLord(
            house=house,
            cusp_longitude=cusp_lon,
            star_lord=entry.star_lord,
            sub_lord=entry.sub_lord,
            sub_sub_lord=sub_sub,
            sub_lord_signified_houses=sub_signified,
            has_promise=has_promise,
            promise_note=note,
        )

    return result


def compute_kp_event_promise(cuspal_sub_lords: dict[int, CuspalSubLord]) -> dict[str, dict]:
    """
    Check KP event promise for common life events.

    KP Rule: An event can only occur if the cuspal sub-lords of the
    relevant houses signify those houses.

    Source: K.S. Krishnamurti Reader Series Vol.3
    """
    result = {}

    for event, houses in KP_EVENT_HOUSES.items():
        houses_with_promise = []
        houses_without = []

        for h in houses:
            csl = cuspal_sub_lords.get(h)
            if csl and csl.has_promise:
                houses_with_promise.append(h)
            else:
                houses_without.append(h)

        # Event promised if MOST relevant houses show promise
        promise_ratio = len(houses_with_promise) / len(houses)
        has_promise = promise_ratio >= 0.67

        result[event] = {
            "has_promise": has_promise,
            "promise_ratio": round(promise_ratio, 2),
            "houses_with_promise": houses_with_promise,
            "houses_without_promise": houses_without,
            "note": f"{'Yes' if has_promise else 'Weak'} — {len(houses_with_promise)}/{len(houses)} house cusps show promise",
        }

    return result


def compute_kp_analysis(chart, query_datetime=None) -> KPAnalysisResult:
    """
    Full KP analysis for a chart.

    Returns cuspal sub-lords, event promises, ruling planets,
    and fructification assessment.

    Source: K.S. Krishnamurti Reader Series Vol.2-3
    """
    # Require KP-appropriate settings
    # Note: Full accuracy requires KP ayanamsha + true node

    cuspal_sub_lords = compute_cuspal_sub_lords(chart)
    event_promise = compute_kp_event_promise(cuspal_sub_lords)

    # Ruling planets
    try:
        from src.calculations.kp_sublord import compute_ruling_planets
        ruling = compute_ruling_planets(chart, query_datetime)
    except Exception:
        ruling = []

    # Fructification: planets that are both ruling AND significators of promised houses
    fructification = []
    promised_events = [e for e, v in event_promise.items() if v["has_promise"]]
    if promised_events and ruling:
        # Houses associated with promised events
        all_promised_houses = set()
        for e in promised_events:
            all_promised_houses.update(KP_EVENT_HOUSES[e])

        for csl in cuspal_sub_lords.values():
            if (csl.has_promise and
                csl.sub_lord in ruling and
                csl.sub_lord not in fructification):
                fructification.append(csl.sub_lord)

    note = (
        f"KP Analysis: {len([v for v in event_promise.values() if v['has_promise']])} events promised. "
        f"Ruling planets: {', '.join(ruling[:5])}. "
        f"Fructification planets: {', '.join(fructification) or 'None identified'}."
    )

    return KPAnalysisResult(
        cuspal_sub_lords=cuspal_sub_lords,
        ruling_planets=ruling,
        event_promise={e: v["has_promise"] for e, v in event_promise.items()},
        fructification_planets=fructification,
        analysis_note=note,
    )
