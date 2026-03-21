"""
src/calculations/scoring_patches.py
Phase 0 scoring corrections — to be integrated into scoring_v3.py.

Session 110 changes:
  - ASPECT_STRENGTH dict: BPHS Ch.26 v.3-5 (Mars/Jupiter/Saturn = 3/4 strength)
  - display_score: tanh normalization preserving gradient
  - Kemadruma: all 3 conditions + 4 cancellations (Phaladeepika Ch.6 v.56-60)
  - Raj Yoga: Parivartana + aspect forms added (BPHS Ch.36 v.1-15)

These patches are applied as standalone functions so they can be imported
into the existing scoring_v3.py without a full rewrite.
"""

from __future__ import annotations
from math import tanh
from dataclasses import dataclass
from typing import Optional

# ─── Aspect Strength ─────────────────────────────────────────────────────────
# Source: BPHS Ch.26 v.3-5
# All unspecified planet-house pairs = 1.0 (full strength)

ASPECT_STRENGTH: dict[tuple[str, int], float] = {
    ("Mars",    4): 0.75,
    ("Mars",    8): 0.75,
    ("Jupiter", 5): 0.75,
    ("Jupiter", 9): 0.75,
    ("Saturn",  3): 0.75,
    ("Saturn", 10): 0.75,
}

def get_aspect_strength(aspector: str, houses_away: int) -> float:
    """
    Returns the fractional strength of an aspect.
    houses_away: 1-12, where 7 = opposition (full aspect for all planets).
    """
    if houses_away == 7:
        return 1.0
    return ASPECT_STRENGTH.get((aspector, houses_away), 0.0)


def aspect_hits(aspector_house: int, target_house: int) -> int:
    """Houses from aspector to target (1-12)."""
    return (target_house - aspector_house) % 12 + 1


# ─── Score gradient ───────────────────────────────────────────────────────────

def display_score(raw_score: float) -> float:
    """
    Smooth compression of raw score to display range.
    Uses tanh to preserve gradient while keeping output in roughly [-10, +10].
    raw_score is unclamped; display is continuous and order-preserving.
    """
    return round(10.0 * tanh(raw_score / 8.0), 2)


def score_rating(display: float) -> str:
    if display >= 6.0:  return "Excellent"
    if display >= 3.0:  return "Strong"
    if display >= 0.0:  return "Moderate"
    if display >= -3.0: return "Weak"
    return "Very Weak"


# ─── Kemadruma Yoga (corrected) ──────────────────────────────────────────────
# Source: Phaladeepika Ch.6 v.56-60; PVRNR Astrology of the Seers Ch.8

@dataclass
class KemadrumaResult:
    is_kemadruma: bool
    condition1_no_adjacent: bool      # no planets in 2nd/12th from Moon
    condition2_no_kendra_moon: bool   # no planets in Kendra from Moon
    condition3_no_benefic_aspect: bool # Moon not aspected by benefic
    # Cancellation flags
    cancel_moon_kendra_lagna: bool
    cancel_benefic_aspect_or_conjunct: bool
    cancel_moon_exalt_or_own: bool
    cancel_lagna_lord_conjunct: bool


def check_kemadruma(chart) -> KemadrumaResult:
    """
    Full Kemadruma check with all 3 conditions and 4 cancellations.
    Source: Phaladeepika Ch.6 v.56-60
    """
    if "Moon" not in chart.planets:
        return KemadrumaResult(False, False, False, False, False, False, False, False)

    moon_si = chart.planets["Moon"].sign_index
    lagna_si = chart.lagna_sign_index

    planets_7 = [p for p in chart.planets if p not in ("Rahu", "Ketu")]
    natural_benefics = {"Moon", "Mercury", "Jupiter", "Venus"}

    # ── Condition 1: No planets in 2nd or 12th from Moon ──
    adjacent_signs = {(moon_si + 1) % 12, (moon_si - 1) % 12}
    cond1 = not any(
        chart.planets[p].sign_index in adjacent_signs
        for p in planets_7 if p != "Moon"
    )

    # ── Condition 2: No planets in Kendra (1/4/7/10) from Moon ──
    kendra_from_moon = {(moon_si + k) % 12 for k in (0, 3, 6, 9)}
    cond2 = not any(
        chart.planets[p].sign_index in kendra_from_moon
        for p in planets_7 if p != "Moon"
    )

    # ── Condition 3: Moon not aspected by any benefic ──
    # Full 7th aspect + Jupiter's 5th/9th (¾ strength still counts as aspect)
    moon_house = (moon_si - lagna_si) % 12 + 1
    cond3 = True
    for p in planets_7:
        if p == "Moon":
            continue
        if p not in natural_benefics:
            continue
        p_house = (chart.planets[p].sign_index - lagna_si) % 12 + 1
        ha = aspect_hits(p_house, moon_house)
        if ha == 7:  # full 7th aspect
            cond3 = False
            break
        if p == "Jupiter" and ha in (5, 9):
            cond3 = False
            break

    # ── Cancellation 1: Moon in Kendra from Lagna ──
    moon_from_lagna = (moon_si - lagna_si) % 12 + 1
    cancel1 = moon_from_lagna in (1, 4, 7, 10)

    # ── Cancellation 2: Moon conjoined or aspected by benefic ──
    cancel2 = not cond3  # same logic as condition 3 inverted

    # ── Cancellation 3: Moon in exalted or own sign ──
    # Moon exalted in Taurus (1), own in Cancer (3)
    cancel3 = moon_si in (1, 3)

    # ── Cancellation 4: Lagna lord conjoined Moon ──
    _SIGN_LORDS_SP = {0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"}
    lagna_lord = _SIGN_LORDS_SP.get(lagna_si)
    cancel4 = (
        lagna_lord is not None and
        lagna_lord in chart.planets and
        chart.planets[lagna_lord].sign_index == moon_si
    )

    any_cancel = cancel1 or cancel2 or cancel3 or cancel4
    is_kema = cond1 and cond2 and cond3 and not any_cancel

    return KemadrumaResult(
        is_kemadruma=is_kema,
        condition1_no_adjacent=cond1,
        condition2_no_kendra_moon=cond2,
        condition3_no_benefic_aspect=cond3,
        cancel_moon_kendra_lagna=cancel1,
        cancel_benefic_aspect_or_conjunct=cancel2,
        cancel_moon_exalt_or_own=cancel3,
        cancel_lagna_lord_conjunct=cancel4,
    )


# ─── Raj Yoga (corrected — adds exchange and aspect forms) ──────────────────
# Source: BPHS Ch.36 v.1-15

@dataclass
class RajYogaResult:
    present: bool
    strength: str            # "Strong" / "Moderate" / "Weak"
    kendra_lord: str
    trikona_lord: str
    formation_type: str      # "conjunction" / "exchange" / "aspect"
    is_cancelled: bool
    cancel_reason: str


def check_raj_yoga_pair(kendra_lord: str, trikona_lord: str, chart) -> Optional[RajYogaResult]:
    """
    Check Raj Yoga between a specific Kendra lord and Trikona lord.
    Returns None if no yoga, RajYogaResult if found.
    Source: BPHS Ch.36 v.1-15
    """
    if kendra_lord not in chart.planets or trikona_lord not in chart.planets:
        return None
    if kendra_lord == trikona_lord:
        return None  # same planet

    k_si = chart.planets[kendra_lord].sign_index
    t_si = chart.planets[trikona_lord].sign_index
    lagna_si = chart.lagna_sign_index

    # Formation type
    formation = None
    if k_si == t_si:
        formation = "conjunction"
    else:
        # Check Parivartana (mutual sign exchange)
        from src.calculations.house_lord import SIGN_LORDS
        k_rules = _owns_sign(kendra_lord, t_si)
        t_rules = _owns_sign(trikona_lord, k_si)
        if k_rules and t_rules:
            formation = "exchange"
        else:
            # Check mutual full 7th aspect
            k_house = (k_si - lagna_si) % 12 + 1
            t_house = (t_si - lagna_si) % 12 + 1
            if aspect_hits(k_house, t_house) == 7 or aspect_hits(t_house, k_house) == 7:
                formation = "aspect"

    if formation is None:
        return None

    # Cancellation checks
    is_cancelled = False
    cancel_reason = ""

    # Combust check
    for lord in (kendra_lord, trikona_lord):
        from src.calculations.dignity import compute_dignity
        d = compute_dignity(lord, chart)
        if d.combust and not d.cazimi:
            is_cancelled = True
            cancel_reason = f"{lord} is combust"
            break

    # Dusthana placement
    if not is_cancelled:
        for lord in (kendra_lord, trikona_lord):
            h = (chart.planets[lord].sign_index - lagna_si) % 12 + 1
            if h in (6, 8, 12):
                is_cancelled = True
                cancel_reason = f"{lord} in dusthana (H{h})"
                break

    # Strength assessment
    if is_cancelled:
        strength = "Cancelled"
    elif formation == "conjunction":
        strength = "Strong"
    elif formation == "exchange":
        strength = "Strong"
    else:
        strength = "Moderate"

    return RajYogaResult(
        present=not is_cancelled,
        strength=strength,
        kendra_lord=kendra_lord,
        trikona_lord=trikona_lord,
        formation_type=formation,
        is_cancelled=is_cancelled,
        cancel_reason=cancel_reason,
    )


def detect_raj_yogas(chart) -> list[RajYogaResult]:
    """
    Detect all Raj Yogas in the chart.
    Source: BPHS Ch.36 v.1-15
    """
    from src.calculations.house_lord import compute_house_map, SIGN_LORDS
    hmap = compute_house_map(chart)  # noqa: F841
    lagna_si = chart.lagna_sign_index

    kendras   = [1, 4, 7, 10]
    trikonas  = [1, 5, 9]
    dusthanas = [6, 8, 12]

    kendra_lords  = set()
    trikona_lords = set()

    for h in kendras:
        sign = (lagna_si + h - 1) % 12
        lord = SIGN_LORDS.get(sign)
        if lord:
            kendra_lords.add(lord)

    for h in trikonas:
        sign = (lagna_si + h - 1) % 12
        lord = SIGN_LORDS.get(sign)
        if lord:
            trikona_lords.add(lord)

    # H1 lord is both — only include in Trikona set
    results = []
    checked = set()
    for kl in kendra_lords:
        for tl in trikona_lords:
            pair = tuple(sorted([kl, tl]))
            if pair in checked or kl == tl:
                continue
            checked.add(pair)

            # Skip if either lord also rules a dusthana (standard Parashari rule)
            # Exception: H1 is both Kendra and Trikona — always included
            kl_houses = [h for h in range(1, 13)
                         if SIGN_LORDS.get((lagna_si + h - 1) % 12) == kl]
            tl_houses = [h for h in range(1, 13)
                         if SIGN_LORDS.get((lagna_si + h - 1) % 12) == tl]

            kl_dusthana = any(h in dusthanas for h in kl_houses)
            tl_dusthana = any(h in dusthanas for h in tl_houses)

            # Allow if one of them ALSO rules a Kendra or Trikona
            kl_kt = any(h in kendras + trikonas for h in kl_houses)
            tl_kt = any(h in kendras + trikonas for h in tl_houses)

            if kl_dusthana and not kl_kt:
                continue
            if tl_dusthana and not tl_kt:
                continue

            r = check_raj_yoga_pair(kl, tl, chart)
            if r is not None:
                results.append(r)

    return results


def _owns_sign(planet: str, sign_index: int) -> bool:
    """Check if planet rules this sign."""
    from src.calculations.dignity import OWN_SIGNS
    return sign_index in OWN_SIGNS.get(planet, [])
