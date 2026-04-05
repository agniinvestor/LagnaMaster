"""src/calculations/diagnostic_scorer.py — Phase 2 diagnostic scoring equation.

Implements the hierarchical scoring function:
    BASE = CAPACITY × MODIFIER
    SCORE = STRUCTURE_WEIGHT × sigmoid(k × BASE) × ACTIVATION

Where CAPACITY is structured (lord_strength, house_condition, karaka_support),
MODIFIER incorporates reinforcement and friction, and STRUCTURE_WEIGHT is a
soft gate via sigmoid.

Every variable traces to a BPHS source. Magnitudes are calibration targets.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

# ── Helpers ──────────────────────────────────────────────────────────────────

_SIGN_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_UPACHAYA = {3, 6, 10, 11}

_NAT_BENEFIC = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEFIC = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

_EXALT_SIGN = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5,
               "Jupiter": 3, "Venus": 11, "Saturn": 6, "Rahu": 1, "Ketu": 7}
_DEBIL_SIGN = {"Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
               "Jupiter": 9, "Venus": 5, "Saturn": 0, "Rahu": 7, "Ketu": 1}
_OWN_SIGNS = {"Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
              "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
              "Rahu": [10], "Ketu": [7]}
_MT_SIGNS = {"Sun": 4, "Moon": 1, "Mars": 0, "Mercury": 5,
             "Jupiter": 8, "Venus": 6, "Saturn": 10}

_SPECIAL_ASPECTS = {"Mars": {3, 7}, "Jupiter": {4, 8}, "Saturn": {2, 9}}

# Career karakas (BPHS Ch.32)
_H10_KARAKAS = {"Sun", "Saturn", "Mercury"}


def _sigmoid(x: float) -> float:
    """Numerically stable sigmoid."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    ex = math.exp(x)
    return ex / (1.0 + ex)


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _planet_house(chart, planet_name: str) -> int:
    pos = chart.planets.get(planet_name)
    if not pos:
        return 0
    return (pos.sign_index - chart.lagna_sign_index) % 12 + 1


def _planet_sign_index(chart, planet_name: str) -> int:
    pos = chart.planets.get(planet_name)
    return pos.sign_index if pos else -1


def _lord_of_house(chart, house: int) -> str:
    si = (chart.lagna_sign_index + house - 1) % 12
    return _SIGN_LORDS[si]


def _dignity_score(chart, planet_name: str) -> float:
    """BPHS Ch.3 v.18-22 dignity hierarchy → [0, 1]."""
    pos = chart.planets.get(planet_name)
    if not pos:
        return 0.4  # neutral fallback
    si = pos.sign_index
    name = planet_name
    if name in _MT_SIGNS and si == _MT_SIGNS[name]:
        return 0.85
    if name in _EXALT_SIGN and si == _EXALT_SIGN[name]:
        return 1.0
    if name in _OWN_SIGNS and si in _OWN_SIGNS[name]:
        return 0.75
    if name in _DEBIL_SIGN and si == _DEBIL_SIGN[name]:
        return 0.1
    return 0.4  # neutral


def _placement_score(house: int) -> float:
    """BPHS Ch.47 — bhavesh placement quality."""
    if house in _KENDRA:
        return 0.9
    if house in _TRIKONA:
        return 0.85
    if house in _UPACHAYA:
        return 0.6
    if house in _DUSTHANA:
        return 0.2
    return 0.5  # 2nd, etc.


def _impairment_score(chart, planet_name: str) -> float:
    """BPHS Ch.3 v.51-59 (combustion), Saravali Ch.4 (war). Returns [-0.4, +0.1]."""
    score = 0.0
    pos = chart.planets.get(planet_name)
    if not pos:
        return 0.0
    # Combustion
    sun_pos = chart.planets.get("Sun")
    if sun_pos and planet_name != "Sun":
        sep = abs((pos.sign_index * 30 + pos.degree_in_sign) -
                  (sun_pos.sign_index * 30 + sun_pos.degree_in_sign))
        sep = min(sep, 360 - sep)
        if sep < 1.0:
            score += 0.05  # cazimi — strengthened
        elif sep < 8.0:
            score -= 0.3  # combust
    # Retrograde
    is_retro = getattr(pos, "is_retrograde", False) or getattr(pos, "retrograde", False)
    if is_retro:
        if planet_name in ("Jupiter", "Saturn"):
            score += 0.1  # outer planets gain
        elif planet_name in ("Mercury", "Venus"):
            score -= 0.2  # inner planets lose
    # Planetary war
    if planet_name in getattr(chart, "planetary_war_losers", set()):
        score -= 0.4
    return _clamp(score, -0.4, 0.1)


def _aspects_house(planet_name: str, planet_house: int, target_house: int) -> bool:
    """Parashari graha drishti."""
    diff = (target_house - planet_house) % 12
    if diff == 6:
        return True
    return diff in _SPECIAL_ASPECTS.get(planet_name, set())


def _is_func_benefic(chart, planet_name: str) -> bool:
    """Per-lagna functional benefic."""
    try:
        from src.calculations.functional_dignity import compute_functional_classifications
        fc = compute_functional_classifications(chart.lagna_sign_index)
        entry = fc.get(planet_name)
        return entry.is_functional_benefic if entry else False
    except Exception:
        return planet_name in _NAT_BENEFIC


def _is_func_malefic(chart, planet_name: str) -> bool:
    try:
        from src.calculations.functional_dignity import compute_functional_classifications
        fc = compute_functional_classifications(chart.lagna_sign_index)
        entry = fc.get(planet_name)
        return entry.is_functional_malefic if entry else False
    except Exception:
        return planet_name in _NAT_MALEFIC


# ── Diagnostic Scorer ────────────────────────────────────────────────────────

@dataclass
class DiagnosticResult:
    """Complete diagnostic scoring result for one house."""
    house: int
    structure_raw: float
    structure_weight: float
    lord_strength: float
    house_condition: float
    karaka_support: float
    capacity: float
    reinforcement: float
    friction: float
    modifier: float
    base: float
    activation: float
    score: float
    details: dict = field(default_factory=dict)


def score_h10(chart, activation: float = 1.0) -> DiagnosticResult:
    """Score H10 (career) using the diagnostic equation.

    CAREER_SCORE = STRUCTURE_WEIGHT × sigmoid(k × CAPACITY × MODIFIER) × ACTIVATION
    """
    house = 10
    house_si = (chart.lagna_sign_index + house - 1) % 12
    lord = _lord_of_house(chart, house)
    lord_h = _planet_house(chart, lord)

    # ── Layer 1: STRUCTURE ───────────────────────────────────────────────
    ld = _dignity_score(chart, lord)
    lp = _placement_score(lord_h) if lord_h > 0 else 0.5
    li = _impairment_score(chart, lord)

    structure_raw = 0.5 * ld + 0.3 * lp + 0.2 * (1.0 + li)
    structure_weight = _sigmoid(8.0 * (structure_raw - 0.3))

    # ── Layer 2: CAPACITY ────────────────────────────────────────────────

    # Sub-component A: Lord Strength
    lord_strength = _clamp(0.6 * ld + 0.25 * lp + 0.15 * (1.0 + li), 0.0, 1.0)

    # Sub-component B: House Condition
    p_house_map = {p: _planet_house(chart, p) for p in chart.planets}
    in_house = [p for p, h in p_house_map.items() if h == house]

    benefic_in = sum(0.15 for p in in_house if _is_func_benefic(chart, p))
    malefic_in = sum(-0.15 for p in in_house if _is_func_malefic(chart, p))

    benefic_aspect = sum(0.08 for p in chart.planets
                         if _is_func_benefic(chart, p)
                         and p not in in_house
                         and p_house_map.get(p, 0) > 0
                         and _aspects_house(p, p_house_map[p], house))
    malefic_aspect = sum(-0.08 for p in chart.planets
                          if _is_func_malefic(chart, p)
                          and p not in in_house
                          and p_house_map.get(p, 0) > 0
                          and _aspects_house(p, p_house_map[p], house))

    # Kartari
    left_si = (house_si - 1) % 12
    right_si = (house_si + 1) % 12
    sign_planets = {}
    for p, pos in chart.planets.items():
        sign_planets.setdefault(pos.sign_index, []).append(p)
    left_p = sign_planets.get(left_si, [])
    right_p = sign_planets.get(right_si, [])
    left_benefic = any(p in _NAT_BENEFIC for p in left_p)
    right_benefic = any(p in _NAT_BENEFIC for p in right_p)
    left_malefic = any(p in _NAT_MALEFIC for p in left_p)
    right_malefic = any(p in _NAT_MALEFIC for p in right_p)
    kartari = 0.0
    if left_benefic and right_benefic:
        kartari = 0.10
    elif left_malefic and right_malefic:
        kartari = -0.10

    # Sign quality
    gentle = {3, 1, 6, 11, 8}
    sign_q = 0.05 if house_si in gentle else 0.0

    house_condition = _clamp(0.5 + benefic_in + malefic_in + benefic_aspect + malefic_aspect + kartari + sign_q, 0.0, 1.0)

    # Sub-component C: Karaka Support
    karaka_score = 0.0
    for k in _H10_KARAKAS:
        k_h = _planet_house(chart, k)
        if k_h == house:
            karaka_score += 0.10
        elif k_h > 0 and _aspects_house(k, k_h, house):
            karaka_score += 0.05
        elif k_h in _DUSTHANA:
            karaka_score -= 0.08

    # Ashtakavarga
    try:
        from src.calculations.ashtakavarga import compute_all_ashtakavarga
        av = compute_all_ashtakavarga(chart)
        sav = av.get("sarva", {})
        bindus = sav.get(house_si, 0) if isinstance(sav, dict) else 0
        av_score = 0.10 if bindus >= 5 else (-0.10 if bindus <= 3 else 0.0)
    except Exception:
        av_score = 0.0

    karaka_support = _clamp(0.5 + karaka_score + av_score, 0.0, 1.0)

    # CAPACITY
    capacity = 0.45 * lord_strength + 0.35 * house_condition + 0.20 * karaka_support

    # ── Layer 3: REINFORCEMENT ───────────────────────────────────────────
    primary_yoga = 0.0
    secondary_yoga = 0.0

    # Dharma-Karma Adhipati Yoga: 9th + 10th lords connected
    lord_9 = _lord_of_house(chart, 9)
    lord_10 = lord
    l9_h = _planet_house(chart, lord_9)
    l10_h = _planet_house(chart, lord_10)
    if l9_h == l10_h and l9_h > 0:
        primary_yoga = max(primary_yoga, 0.4)
    elif l9_h > 0 and l10_h > 0 and _aspects_house(lord_9, l9_h, l10_h):
        primary_yoga = max(primary_yoga, 0.3)

    # Raja Yoga: any kendra lord + trikona lord conjunction
    kendra_lords = {_lord_of_house(chart, h) for h in _KENDRA}
    trikona_lords = {_lord_of_house(chart, h) for h in _TRIKONA}
    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl != tl and _planet_house(chart, kl) == _planet_house(chart, tl) and _planet_house(chart, kl) > 0:
                primary_yoga = max(primary_yoga, 0.3)

    # Bhavesh with kendra/trikona lord
    lord_companions = [p for p, h in p_house_map.items() if h == lord_h and p != lord]
    for comp in lord_companions:
        if comp in kendra_lords or comp in trikona_lords:
            secondary_yoga += 0.1

    reinforcement = min(1.0, primary_yoga + 0.5 * min(secondary_yoga, 0.3))

    # ── Layer 4: FRICTION ────────────────────────────────────────────────
    mean_c = (lord_strength + house_condition + karaka_support) / 3.0
    raw_var = math.sqrt(((lord_strength - mean_c) ** 2 +
                          (house_condition - mean_c) ** 2 +
                          (karaka_support - mean_c) ** 2) / 3.0)
    friction = min(1.0, raw_var / 0.471)

    # ── Combine ──────────────────────────────────────────────────────────
    alpha = 0.5
    beta = 0.5
    k = 4.0

    modifier = _clamp(1.0 + alpha * reinforcement - beta * friction, 0.5, 1.5)
    base = capacity * modifier
    score = structure_weight * _sigmoid(k * base) * activation

    return DiagnosticResult(
        house=house,
        structure_raw=round(structure_raw, 4),
        structure_weight=round(structure_weight, 4),
        lord_strength=round(lord_strength, 4),
        house_condition=round(house_condition, 4),
        karaka_support=round(karaka_support, 4),
        capacity=round(capacity, 4),
        reinforcement=round(reinforcement, 4),
        friction=round(friction, 4),
        modifier=round(modifier, 4),
        base=round(base, 4),
        activation=round(activation, 4),
        score=round(score, 4),
        details={
            "lord": lord, "lord_house": lord_h,
            "lord_dignity": round(ld, 3), "lord_placement": round(lp, 3),
            "lord_impairment": round(li, 3),
        },
    )


def score_h10_simplified(chart) -> float:
    """Model C: STRUCTURE_WEIGHT × CAPACITY only. No reinforcement, friction, activation."""
    r = score_h10(chart, activation=1.0)
    return round(r.structure_weight * r.capacity, 4)
