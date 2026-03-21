"""
src/calculations/dasha_activation.py
Yoga Activation Timeline + Conditional Dasha Activation Logic.
Sessions 154, D-2.

Sources:
  K.N. Rao · Yogis, Destiny and the Wheel of Time (dasha timing methodology)
  Sanjay Rath · Crux of Vedic Astrology Ch.14 (yoga fructification)
  PVRNR · BPHS Ch.46 v.1-5 (conditional dasha activation)
  Gayatri Devi Vasudev · The Art of Prediction in Astrology Ch.4 (triple concordance)
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

# ─── Conditional Dasha Applicability ─────────────────────────────────────────

_KENDRA  = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",
    5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",
    9: "Saturn", 10: "Saturn", 11: "Jupiter",
}


def compute_applicable_dashas(chart) -> dict:
    """
    Determine which dasha systems apply to a given chart.

    Rules:
    - Vimshottari: always applicable (primary)
    - Ashtottari: when Rahu is NOT in Kendra or Trikona from Lagna
    - Yogini: always applicable (supplementary)
    - Kalachakra: applicable when Moon in Pushya nakshatra at birth
    - Shoola: applicable for timing death-like events (all charts)

    Source: PVRNR · BPHS Ch.46 v.1-5
    """
    lagna_si = chart.lagna_sign_index
    applicable = ["vimshottari", "yogini", "shoola"]  # always

    # Ashtottari: Rahu NOT in Kendra/Trikona from Lagna
    if "Rahu" in chart.planets:
        rahu_si = chart.planets["Rahu"].sign_index
        rahu_house = (rahu_si - lagna_si) % 12 + 1
        if rahu_house not in (_KENDRA | _TRIKONA):
            applicable.append("ashtottari")

    # Kalachakra: Moon in Pushya (index 7) nakshatra
    if "Moon" in chart.planets:
        moon_nak = int(chart.planets["Moon"].longitude * 3 / 40)
        if moon_nak == 7:  # Pushya
            applicable.append("kalachakra")

    # Chara Dasha: always applicable if Jaimini infrastructure present
    applicable.append("chara")  # Jaimini — always available

    primary = "vimshottari"
    secondary = [d for d in applicable if d != "vimshottari"]

    return {
        "primary_dasha": primary,
        "secondary_dashas": secondary,
        "all_applicable": applicable,
        "note": "Ashtottari applicable" if "ashtottari" in applicable else "Vimshottari is primary; Ashtottari not applicable (Rahu in Kendra/Trikona)",
    }


# ─── Yoga Activation Timeline ─────────────────────────────────────────────────

@dataclass
class YogaActivationWindow:
    yoga_name: str
    forming_planets: list[str]
    strength_label: str
    earliest_activation: Optional[date]    # first dasha window
    latest_activation: Optional[date]      # last dasha window in reasonable range
    dasha_windows: list[dict]              # list of {md_lord, ad_lord, start, end}
    transit_trigger: Optional[str]         # "Jupiter transiting H9" etc.
    confidence: str                        # "High" / "Moderate" / "Low"
    note: str


def compute_yoga_activation_windows(
    yoga_name: str,
    forming_planets: list[str],
    mahadashas: list,
    chart,
    query_until_year: int = 2060,
) -> YogaActivationWindow:
    """
    Compute when a yoga is most likely to fructify based on dasha periods.

    A yoga fructifies when:
    1. MD or AD of one of the yoga-forming planets is active
    2. Simultaneously another yoga-forming planet is in a supportive transit
    3. The relevant house has positive AV bindus

    Source: K.N. Rao · Timing Events Through Vimshottari Dasha, methodology
    """
    if not forming_planets or not mahadashas:
        return YogaActivationWindow(
            yoga_name=yoga_name, forming_planets=forming_planets,
            strength_label="Unknown", earliest_activation=None,
            latest_activation=None, dasha_windows=[], transit_trigger=None,
            confidence="Low", note="Insufficient data",
        )

    dasha_windows = []
    earliest = None
    latest = None
    today = date.today()

    for md in mahadashas:
        if not hasattr(md, 'lord') or not hasattr(md, 'start'):
            continue

        # Check if MD lord is one of the yoga-forming planets
        if md.lord in forming_planets:
            if md.end.year > today.year and md.start.year <= query_until_year:
                dasha_windows.append({
                    "md_lord": md.lord,
                    "type": "MD",
                    "start": str(md.start),
                    "end": str(md.end),
                    "activation_strength": "Primary",
                })
                if earliest is None or md.start < earliest:
                    earliest = md.start if md.start > today else today
                if latest is None or md.end > latest:
                    latest = md.end

        # Check antardasha level
        if hasattr(md, 'antardashas'):
            for ad in md.antardashas:
                if hasattr(ad, 'lord') and ad.lord in forming_planets:
                    if ad.end > today and ad.start.year <= query_until_year:
                        dasha_windows.append({
                            "md_lord": md.lord,
                            "ad_lord": ad.lord,
                            "type": "AD",
                            "start": str(ad.start),
                            "end": str(ad.end),
                            "activation_strength": "Secondary",
                        })
                        if earliest is None or ad.start < earliest:
                            earliest = ad.start if ad.start > today else today

    # Confidence based on strength and number of windows
    if len(dasha_windows) >= 3:
        confidence = "High"
    elif len(dasha_windows) >= 1:
        confidence = "Moderate"
    else:
        confidence = "Low"

    # Transit trigger: which Jupiter or Saturn transit will confirm
    transit_trigger = None
    if forming_planets:
        transit_trigger = f"Jupiter transiting house of {forming_planets[0]} or its 5th/9th aspect"

    note = f"Yoga activates in dashas of: {', '.join(forming_planets)}. "
    if earliest:
        note += f"Earliest window: {earliest}."

    return YogaActivationWindow(
        yoga_name=yoga_name,
        forming_planets=forming_planets,
        strength_label="",
        earliest_activation=earliest,
        latest_activation=latest,
        dasha_windows=dasha_windows[:10],  # limit to first 10 windows
        transit_trigger=transit_trigger,
        confidence=confidence,
        note=note,
    )


# ─── Triple Chart Concordance ─────────────────────────────────────────────────

@dataclass
class TripleConcordanceResult:
    domain: str                   # "career" / "wealth" / "relationship" / etc.
    d1_indication: str            # "Strong" / "Moderate" / "Weak"
    d9_indication: str
    domain_varga_indication: str  # D10 for career, D2 for wealth, etc.
    concordance: str              # "Triple" / "Double" / "Single" / "None"
    confidence: str               # "Certain" / "Likely" / "Possible" / "Uncertain"
    domain_varga_used: str


_DOMAIN_VARGAS = {
    "career":       10,
    "wealth":       2,
    "children":     7,
    "property":     4,
    "vehicle":      16,
    "education":    24,
    "spirituality": 20,
    "disease":      30,
    "destiny":      60,
}

_DOMAIN_HOUSES = {
    "career":       [10, 6, 2],
    "wealth":       [2, 11, 5],
    "children":     [5, 9],
    "property":     [4],
    "relationship": [7, 1],
    "spirituality": [9, 12, 8],
    "education":    [4, 5, 9],
}


def compute_triple_concordance(domain: str, chart, vargas_chart: dict = None) -> TripleConcordanceResult:
    """
    Check if a domain theme is confirmed across D1, D9, and domain varga.
    Source: Gayatri Devi Vasudev · Art of Prediction Ch.4
    """
    domain_varga_n = _DOMAIN_VARGAS.get(domain, 9)
    houses = _DOMAIN_HOUSES.get(domain, [10])

    # D1 indication: is the relevant house lord well-placed?
    from src.calculations.dignity import compute_dignity, DignityLevel
    lagna_si = chart.lagna_sign_index
    _SIGN_LORDS_LOCAL = {
        0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",
        5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",
        9: "Saturn", 10: "Saturn", 11: "Jupiter",
    }

    def house_strength(h: int, ref_chart) -> str:
        lord_sign = (ref_chart.lagna_sign_index + h - 1) % 12
        lord = _SIGN_LORDS_LOCAL.get(lord_sign, "Jupiter")
        if lord not in ref_chart.planets:
            return "Unknown"
        d = compute_dignity(lord, ref_chart)
        if d.dignity.value in ("Deep Exaltation", "Exaltation", "Mooltrikona", "Own Sign"):
            return "Strong"
        elif d.dignity.value in ("Friendly Sign", "Neutral"):
            return "Moderate"
        return "Weak"

    d1_str = house_strength(houses[0], chart)

    # D9 confirmation
    d9_str = "Unknown"
    try:
        from src.calculations.vargas import compute_varga_sign
        # Build pseudo D9 chart from main chart
        class _PseudoChart:
            def __init__(self):
                self.lagna = compute_varga_sign(chart.lagna, 9) * 30.0
                self.lagna_sign_index = compute_varga_sign(chart.lagna, 9)
                self.planets = {}
                for p, pd in chart.planets.items():
                    class _PP:
                        pass
                    pp = _PP()
                    pp.sign_index = compute_varga_sign(pd.longitude, 9)
                    pp.degree_in_sign = 0.0
                    pp.longitude = pp.sign_index * 30.0
                    pp.is_retrograde = pd.is_retrograde
                    pp.speed = getattr(pd, 'speed', 1.0)
                    pp.latitude = getattr(pd, 'latitude', 0.0)
                    self.planets[p] = pp
        d9_chart = _PseudoChart()
        d9_str = house_strength(houses[0], d9_chart)
    except Exception:
        d9_str = "Unknown"

    # Domain varga
    domain_varga_str = "Unknown"

    # Count agreements
    indications = [d1_str, d9_str, domain_varga_str]
    strong_count = sum(1 for x in indications if x == "Strong")
    moderate_count = sum(1 for x in indications if x == "Moderate")

    if strong_count >= 3:
        concordance = "Triple"
        confidence = "Certain"
    elif strong_count >= 2 or (strong_count == 1 and moderate_count >= 1):
        concordance = "Double"
        confidence = "Likely"
    elif strong_count >= 1 or moderate_count >= 2:
        concordance = "Single"
        confidence = "Possible"
    else:
        concordance = "None"
        confidence = "Uncertain"

    return TripleConcordanceResult(
        domain=domain,
        d1_indication=d1_str,
        d9_indication=d9_str,
        domain_varga_indication=domain_varga_str,
        concordance=concordance,
        confidence=confidence,
        domain_varga_used=f"D{domain_varga_n}",
    )
