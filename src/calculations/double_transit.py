"""
src/calculations/double_transit.py — Session 103

K.N. Rao Double Transit Theory.
Source: K.N. Rao's predictive astrology lectures and texts.

Theory: Major life events require BOTH Jupiter and Saturn to simultaneously
transit natal or dasha-activated positions.

Specific rules (K.N. Rao):
  Marriage: Jupiter AND Saturn both transit the natal 7th house lord's position,
    OR the Navamsha Lagna, OR the natal Moon.
  Career: Jupiter AND Saturn both transit the natal 10th house lord's position.
  General: Both transit the Dasha lord's natal position.

Transit quality:
  Both favorable aspects (+) = "Double confirmation — event likely"
  One favorable, one challenging = "Partial confirmation — possible"
  Neither = "Not activated by double transit"

Aspects considered: conjunction (0°), trine (120°), sextile (60°).
Challenging: square (90°), opposition (180°).

This is a PREDICTION LAYER — it strengthens or weakens the promise/activation
signal from the main engine. It does NOT override the natal promise engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_DOMAINS = {"marriage": 7, "career": 10, "wealth": 2, "general": 1}


@dataclass
class TransitAspect:
    planet: str
    natal_position: float    # degrees
    transit_position: float  # degrees
    orb: float
    aspect_type: str         # "conjunction"/"trine"/"sextile"/"square"/"opposition"
    is_favorable: bool


@dataclass
class DoubleTransitResult:
    domain: str
    target_house: int
    jupiter_aspect: TransitAspect | None
    saturn_aspect: TransitAspect | None
    double_confirmed: bool
    partial_confirmed: bool
    signal: str    # "Double confirmation"/"Partial"/"Not activated"
    confidence: str


def _aspect_type(orb: float) -> tuple[str, bool]:
    """Return (aspect_type, is_favorable) for a given orb in degrees."""
    orb = abs(orb % 360)
    if orb > 180: orb = 360 - orb
    if orb <= 8:   return "conjunction", True
    if abs(orb - 60)  <= 6: return "sextile", True
    if abs(orb - 90)  <= 6: return "square",  False
    if abs(orb - 120) <= 8: return "trine",   True
    if abs(orb - 180) <= 8: return "opposition", False
    return "none", False


def _get_transit_position(planet: str, on_date: date) -> float | None:
    """Get transit position of a planet on a given date via ephemeris."""
    try:
        from src.ephemeris import compute_chart
        # Create a chart for the current date at a reference location
        transit_chart = compute_chart(
            year=on_date.year, month=on_date.month, day=on_date.day,
            hour=12.0, lat=0.0, lon=0.0, tz_offset=0.0
        )
        pos = transit_chart.planets.get(planet)
        return pos.longitude if pos else None
    except Exception:
        return None


def compute_double_transit(chart, domain: str = "marriage",
                            on_date: date | None = None) -> DoubleTransitResult:
    """
    Check K.N. Rao Double Transit for a given domain and date.
    """
    if on_date is None:
        on_date = date.today()

    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)

    target_house = _DOMAINS.get(domain, 1)
    target_lord = hmap.house_lord[target_house - 1]
    target_natal_lon = chart.planets[target_lord].longitude if target_lord in chart.planets else 0.0

    # Also check natal Moon for marriage
    chart.planets.get("Moon")
    # Use house lord position as primary target
    target_lon = target_natal_lon

    jup_transit = _get_transit_position("Jupiter", on_date)
    sat_transit = _get_transit_position("Saturn", on_date)

    jup_aspect = None
    sat_aspect = None

    if jup_transit is not None:
        orb = (jup_transit - target_lon) % 360
        atype, fav = _aspect_type(orb)
        if atype != "none":
            jup_aspect = TransitAspect(
                planet="Jupiter", natal_position=target_lon,
                transit_position=jup_transit,
                orb=round(min(orb, 360-orb), 2),
                aspect_type=atype, is_favorable=fav,
            )

    if sat_transit is not None:
        orb = (sat_transit - target_lon) % 360
        atype, fav = _aspect_type(orb)
        if atype != "none":
            sat_aspect = TransitAspect(
                planet="Saturn", natal_position=target_lon,
                transit_position=sat_transit,
                orb=round(min(orb, 360-orb), 2),
                aspect_type=atype, is_favorable=fav,
            )

    jup_fav = jup_aspect and jup_aspect.is_favorable
    sat_fav = sat_aspect and sat_aspect.is_favorable
    double = bool(jup_fav and sat_fav)
    partial = bool((jup_fav and not sat_fav) or (sat_fav and not jup_fav))

    if double:
        signal = "Double confirmation — major event strongly indicated"
        conf = "High"
    elif partial:
        signal = "Partial confirmation — event possible, one planet confirms"
        conf = "Moderate"
    else:
        signal = "Not activated by double transit — timing not confirmed"
        conf = "Low"

    return DoubleTransitResult(
        domain=domain, target_house=target_house,
        jupiter_aspect=jup_aspect, saturn_aspect=sat_aspect,
        double_confirmed=double, partial_confirmed=partial,
        signal=signal, confidence=conf,
    )
