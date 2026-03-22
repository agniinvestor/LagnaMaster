"""
src/scoring.py
===============
22-rule scoring engine: evaluates each of 12 houses on BPHS rules.
Score per house: clamped to [-10, +10].
Source: LEGEND_ScoringRules + SCORE_H1..H12 (Excel).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from src.ephemeris import BirthChart, SIGNS
from src.calculations.house_lord import (
    compute_house_map, HouseMap,
    is_kendra, is_trikona, is_dusthana,
)
from src.calculations.dignity import compute_all_dignities


# ---------------------------------------------------------------------------
# House meta: life domain names + Sthir Karakas
# ---------------------------------------------------------------------------

HOUSE_DOMAIN = {
    1: "Self & Vitality",
    2: "Wealth & Family",
    3: "Courage & Skills",
    4: "Home & Happiness",
    5: "Intellect & Children",
    6: "Challenges",
    7: "Relationships",
    8: "Transformation",
    9: "Fortune & Dharma",
    10: "Career & Status",
    11: "Gains & Income",
    12: "Liberation & Loss",
}

# Sthir (fixed) Karakas per house (BPHS Ch.10 / REF_Planets col K)
STHIR_KARAK: dict[int, list[str]] = {
    1:  ["Sun"],
    2:  ["Jupiter"],
    3:  ["Mars"],
    4:  ["Moon"],
    5:  ["Jupiter"],
    6:  ["Mars", "Saturn"],
    7:  ["Venus"],
    8:  ["Saturn"],
    9:  ["Jupiter"],
    10: ["Sun", "Mercury", "Jupiter", "Saturn"],
    11: ["Jupiter"],
    12: ["Saturn"],
}

# Scoring weights (LEGEND_ScoringRules)
W = {
    "R01": +0.50,   # Shubh Rashi in house
    "R02": +1.00,   # Benefic in house (+1.5 if Yogakaraka)
    "R03": +0.75,   # Benefic aspects house  (WC)
    "R04": +2.00,   # Bhavesh in Kendra/Trikon
    "R05": +0.50,   # Bhavesh with Kendra/Trikon lord (WC)
    "R06": +1.00,   # Bhavesh with benefic (+1.5 if Yogakaraka)
    "R07": +0.50,   # Benefic aspects Bhavesh sign  (WC)
    "R08": +0.75,   # Bhavesh in Shubh Kartari
    "R09": -1.00,   # Malefic in house
    "R10": -1.00,   # Malefic aspects house
    "R11": -1.25,   # Dusthana lord in house
    "R12": -0.75,   # House in Paap Kartari
    "R13": -1.00,   # Bhavesh with malefic
    "R14": -0.50,   # Malefic aspects Bhavesh sign  (WC)
    "R15": -2.00,   # Bhavesh in Dusthana
    "R16": -1.00,   # Bhavesh with Dusthana lord
    "R17": +0.50,   # Sthir Karak in Kendra/Trikon
    "R18": -0.50,   # Sthir Karak in Dusthana
    "R19": -1.00,   # Bhavesh combust (-1.0; cazimi +0.5; Rx+combust -0.5)
    "R20": +0.50,   # Bhavesh in Dig Bala house
    "R22": +0.10,   # Bhavesh retrograde (context-dependent)
}

WC_RULES = {"R03", "R05", "R07", "R14"}   # half weight in aggregate


# ---------------------------------------------------------------------------
# Planet classification helpers
# ---------------------------------------------------------------------------

_NATURAL_BENEFIC  = {"Moon", "Mercury", "Jupiter", "Venus"}
_NATURAL_MALEFIC  = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_GENTLE_SIGNS     = {1, 2, 3, 5, 8, 11}  # Taurus/Gem/Can/Vir/Sco/Aqu (0-indexed)
# "Gentle" as per SCORE_H1 R01: Gemini/Cancer/Leo/Libra/Sagittarius/Pisces
# REF_Zodiac row 17 — sign_idx 0-indexed: 2=Gem,3=Can,4=Leo,6=Lib,8=Sag,11=Pis
_GENTLE_SIGN_IDX  = {2, 3, 4, 6, 8, 11}


def _is_benefic(planet: str, chart: BirthChart) -> bool:
    return planet in _NATURAL_BENEFIC


def _is_malefic(planet: str, chart: BirthChart) -> bool:
    return planet in _NATURAL_MALEFIC


def _is_yogakaraka(planet: str, lagna_sign_idx: int) -> bool:
    """
    Yogakaraka = planet ruling both a Kendra and Trikona simultaneously.
    Most common: Saturn for Taurus/Libra Lagna; Mars for Cancer/Leo Lagna.
    """
    _YOGAKARAKA_MAP: dict[int, str] = {
        1:  "Saturn",    # Taurus lagna: Saturn rules H9(Capricorn) + H10(Aquarius)...
        # Actually standard: Taurus=Saturn (rules 9+10? no...
        # Taurus lagna: H1=Tau, H2=Gem, H3=Can, H4=Leo, H5=Vir, H6=Lib, H7=Sco, H8=Sag, H9=Cap, H10=Aqu, H11=Pis, H12=Ari
        # Saturn rules H9(Cap)+H10(Aqu) = Trikona(9)+Kendra(10) → Yogakaraka ✓
        3:  "Venus",     # Cancer: Venus rules H4+H11 → not YK; standard YK=Mars (H5+H10)
        4:  "Mars",      # Leo lagna: Mars rules H4(Scorpio)+H9(Aries) — trikona+kendra → YK
        6:  "Saturn",    # Scorpio lagna: Saturn rules H3+H4 — not YK
        # This is simplified — full YK depends on specific sign placements
    }
    return _YOGAKARAKA_MAP.get(lagna_sign_idx) == planet


# ---------------------------------------------------------------------------
# Graha Drishti (Parashari aspects) — house-based
# All planets cast 7th aspect (full); Mars+4th+8th; Jupiter+5th+9th; Saturn+3rd+10th
# ---------------------------------------------------------------------------

def _houses_aspected_by(planet_house: int) -> set[int]:
    """Return set of house numbers aspected by a planet in planet_house (1-12)."""
    h = planet_house
    # 7th aspect (all planets)
    aspects = {(h - 1 + 6) % 12 + 1}  # h + 6, wrapping 1-12
    return aspects


def _planet_aspects_house(planet: str, planet_house: int, target_house: int) -> bool:
    """Return True if planet in planet_house casts a full aspect to target_house."""
    def wrap(h):
        return (h - 1) % 12 + 1

    offsets = [6]  # 7th aspect (all planets)
    if planet == "Mars":
        offsets += [3, 7]      # 4th + 8th
    elif planet == "Jupiter":
        offsets += [4, 8]      # 5th + 9th
    elif planet == "Saturn":
        offsets += [2, 9]      # 3rd + 10th
    # Rahu/Ketu: 5th+9th aspects per some schools; skip for Parashari base

    aspected = {wrap(planet_house + o) for o in offsets}
    return target_house in aspected


# ---------------------------------------------------------------------------
# Kartari check (hemming)
# ---------------------------------------------------------------------------

def _shubh_kartari(sign_idx: int, house_map: HouseMap, chart: BirthChart) -> bool:
    """True if sign is hemmed between benefics in adjacent signs."""
    prev_sign = (sign_idx - 1) % 12
    next_sign = (sign_idx + 1) % 12
    prev_benefic = any(
        p.sign_index == prev_sign and _is_benefic(name, chart)
        for name, p in chart.planets.items()
    )
    next_benefic = any(
        p.sign_index == next_sign and _is_benefic(name, chart)
        for name, p in chart.planets.items()
    )
    return prev_benefic and next_benefic


def _paap_kartari(sign_idx: int, house_map: HouseMap, chart: BirthChart) -> bool:
    """True if sign is hemmed between malefics in adjacent signs."""
    prev_sign = (sign_idx - 1) % 12
    next_sign = (sign_idx + 1) % 12
    prev_malefic = any(
        p.sign_index == prev_sign and _is_malefic(name, chart)
        for name, p in chart.planets.items()
    )
    next_malefic = any(
        p.sign_index == next_sign and _is_malefic(name, chart)
        for name, p in chart.planets.items()
    )
    return prev_malefic and next_malefic


# ---------------------------------------------------------------------------
# Dig Bala peak houses (from shadbala module)
# ---------------------------------------------------------------------------

_DIG_BALA_PEAK_HOUSE: dict[str, list[int]] = {
    "Sun":     [10],
    "Moon":    [4],
    "Mars":    [10, 3],
    "Mercury": [1],
    "Jupiter": [1, 9],
    "Venus":   [4],
    "Saturn":  [7],
}


# ---------------------------------------------------------------------------
# Rule result dataclass
# ---------------------------------------------------------------------------

@dataclass
class RuleResult:
    rule: str
    description: str
    score: float
    is_wc: bool = False      # Worth Considering (half weight in aggregate)
    triggered: bool = False  # True if rule contributed non-zero


@dataclass
class HouseScore:
    house: int
    domain: str
    bhavesh: str             # house lord planet name
    bhavesh_house: int       # house where lord sits
    rules: list[RuleResult] = field(default_factory=list)
    raw_score: float = 0.0
    final_score: float = 0.0  # clamped to [-10, +10]
    rating: str = ""

    def _aggregate(self) -> float:
        total = 0.0
        for r in self.rules:
            contribution = r.score * (0.5 if r.is_wc else 1.0)
            total += contribution
        return total


@dataclass
class ChartScores:
    lagna_sign: str
    houses: dict[int, HouseScore] = field(default_factory=dict)

    def summary(self) -> str:
        lines = [f"Lagna: {self.lagna_sign}", f"{'H':>3} {'Domain':<24} {'Score':>7} {'Rating'}"]
        lines.append("-" * 55)
        for h in range(1, 13):
            hs = self.houses[h]
            lines.append(f"{h:>3} {hs.domain:<24} {hs.final_score:>7.2f} {hs.rating}")
        return "\n".join(lines)


def _rating(score: float) -> str:
    if score >= 6:   return "Excellent"
    if score >= 3:   return "Strong"
    if score >= 0:   return "Moderate"
    if score >= -3:  return "Weak"
    return "Very Weak"


# ---------------------------------------------------------------------------
# Main scoring engine
# ---------------------------------------------------------------------------

def score_chart(chart: BirthChart, query_date=None) -> ChartScores:
    """
    Apply 22 BPHS rules across all 12 houses.
    Returns ChartScores with per-house breakdown.
    """
    house_map = compute_house_map(chart)
    dignities = compute_all_dignities(chart)
    lagna_idx = chart.lagna_sign_index
    dusthana = {6, 8, 12}

    # Dusthana lords (lords of houses 6, 8, 12)
    dusthana_lords = {house_map.house_lord[h - 1] for h in dusthana}
    # Kendra/Trikon lords
    kendra_trikon_houses = {1, 4, 5, 7, 9, 10}
    kt_lords = {house_map.house_lord[h - 1] for h in kendra_trikon_houses}

    result = ChartScores(lagna_sign=chart.lagna_sign)

    for house in range(1, 13):
        house_sign_idx = house_map.house_sign[house - 1]
        bhavesh = house_map.house_lord[house - 1]
        bhavesh_house = house_map.planet_house[bhavesh]
        bhavesh_sign_idx = chart.planets[bhavesh].sign_index

        rules: list[RuleResult] = []

        # --- R01: Shubh (Gentle) Rashi in house ---
        r01_score = W["R01"] if house_sign_idx in _GENTLE_SIGN_IDX else 0.0
        rules.append(RuleResult("R01", "Gentle sign in house", r01_score, triggered=r01_score != 0))

        # --- R02: Benefic in house ---
        r02_score = 0.0
        for pname, p in chart.planets.items():
            if p.sign_index == house_sign_idx:
                if _is_benefic(pname, chart):
                    bonus = 1.5 if _is_yogakaraka(pname, lagna_idx) else 1.0
                    r02_score += bonus
        rules.append(RuleResult("R02", "Benefic in house", r02_score, triggered=r02_score != 0))

        # --- R03: Benefic aspects house (WC) ---
        r03_score = 0.0
        for pname, p in chart.planets.items():
            if p.sign_index != house_sign_idx:  # not conjunct (that's R02)
                if _is_benefic(pname, chart):
                    ph = house_map.planet_house[pname]
                    if _planet_aspects_house(pname, ph, house):
                        r03_score += W["R03"]
        rules.append(RuleResult("R03", "Benefic aspects house", r03_score, is_wc=True, triggered=r03_score != 0))

        # --- R04: Bhavesh in Kendra or Trikon ---
        r04_score = 0.0
        if (is_kendra(bhavesh_house) or is_trikona(bhavesh_house)) and not is_dusthana(bhavesh_house):
            r04_score = W["R04"]
        rules.append(RuleResult("R04", "Bhavesh in Kendra/Trikon", r04_score, triggered=r04_score != 0))

        # --- R05: Bhavesh with Kendra/Trikon lord (WC) ---
        r05_score = 0.0
        for pname, p in chart.planets.items():
            if pname != bhavesh and p.sign_index == bhavesh_sign_idx and pname in kt_lords:
                r05_score = W["R05"]
                break
        rules.append(RuleResult("R05", "Bhavesh with Kendra/Trikon lord", r05_score, is_wc=True, triggered=r05_score != 0))

        # --- R06: Bhavesh with benefic ---
        r06_score = 0.0
        for pname, p in chart.planets.items():
            if pname != bhavesh and p.sign_index == bhavesh_sign_idx:
                if _is_benefic(pname, chart):
                    bonus = 1.5 if _is_yogakaraka(pname, lagna_idx) else 1.0
                    r06_score += bonus
        rules.append(RuleResult("R06", "Bhavesh with benefic", r06_score, triggered=r06_score != 0))

        # --- R07: Benefic aspects Bhavesh sign (WC) ---
        r07_score = 0.0
        bhavesh_house_num = bhavesh_house
        for pname, p in chart.planets.items():
            if pname != bhavesh and _is_benefic(pname, chart):
                ph = house_map.planet_house[pname]
                if _planet_aspects_house(pname, ph, bhavesh_house_num):
                    r07_score += W["R07"]
        rules.append(RuleResult("R07", "Benefic aspects Bhavesh sign", r07_score, is_wc=True, triggered=r07_score != 0))

        # --- R08: Bhavesh in Shubh Kartari ---
        r08_score = W["R08"] if _shubh_kartari(bhavesh_sign_idx, house_map, chart) else 0.0
        rules.append(RuleResult("R08", "Bhavesh in Shubh Kartari", r08_score, triggered=r08_score != 0))

        # --- R09: Malefic in house ---
        r09_score = 0.0
        for pname, p in chart.planets.items():
            if p.sign_index == house_sign_idx and _is_malefic(pname, chart):
                r09_score += W["R09"]
        rules.append(RuleResult("R09", "Malefic in house", r09_score, triggered=r09_score != 0))

        # --- R10: Malefic aspects house ---
        r10_score = 0.0
        for pname, p in chart.planets.items():
            if p.sign_index != house_sign_idx and _is_malefic(pname, chart):
                ph = house_map.planet_house[pname]
                if _planet_aspects_house(pname, ph, house):
                    r10_score += W["R10"]
        rules.append(RuleResult("R10", "Malefic aspects house", r10_score, triggered=r10_score != 0))

        # --- R11: Dusthana lord in house ---
        r11_score = 0.0
        for pname, p in chart.planets.items():
            if p.sign_index == house_sign_idx and pname in dusthana_lords:
                r11_score += W["R11"]
        rules.append(RuleResult("R11", "Dusthana lord in house", r11_score, triggered=r11_score != 0))

        # --- R12: House in Paap Kartari ---
        r12_score = W["R12"] if _paap_kartari(house_sign_idx, house_map, chart) else 0.0
        rules.append(RuleResult("R12", "House in Paap Kartari", r12_score, triggered=r12_score != 0))

        # --- R13: Bhavesh with malefic ---
        r13_score = 0.0
        for pname, p in chart.planets.items():
            if pname != bhavesh and p.sign_index == bhavesh_sign_idx and _is_malefic(pname, chart):
                r13_score += W["R13"]
        rules.append(RuleResult("R13", "Bhavesh with malefic", r13_score, triggered=r13_score != 0))

        # --- R14: Malefic aspects Bhavesh sign (WC) ---
        r14_score = 0.0
        for pname, p in chart.planets.items():
            if pname != bhavesh and _is_malefic(pname, chart):
                ph = house_map.planet_house[pname]
                if _planet_aspects_house(pname, ph, bhavesh_house_num):
                    r14_score += W["R14"]
        rules.append(RuleResult("R14", "Malefic aspects Bhavesh", r14_score, is_wc=True, triggered=r14_score != 0))

        # --- R15: Bhavesh in Dusthana ---
        r15_score = W["R15"] if is_dusthana(bhavesh_house) else 0.0
        rules.append(RuleResult("R15", "Bhavesh in Dusthana", r15_score, triggered=r15_score != 0))

        # --- R16: Bhavesh with Dusthana lord ---
        r16_score = 0.0
        for pname, p in chart.planets.items():
            if pname != bhavesh and p.sign_index == bhavesh_sign_idx and pname in dusthana_lords:
                r16_score += W["R16"]
        rules.append(RuleResult("R16", "Bhavesh with Dusthana lord", r16_score, triggered=r16_score != 0))

        # --- R17/R18: Sthir Karak in Kendra/Trikon or Dusthana ---
        r17_score = 0.0
        r18_score = 0.0
        for karak in STHIR_KARAK.get(house, []):
            if karak in chart.planets:
                kh = house_map.planet_house[karak]
                if is_kendra(kh) or is_trikona(kh):
                    r17_score += W["R17"]
                if is_dusthana(kh):
                    r18_score += W["R18"]
        rules.append(RuleResult("R17", "Sthir Karak in Kendra/Trikon", r17_score, triggered=r17_score != 0))
        rules.append(RuleResult("R18", "Sthir Karak in Dusthana", r18_score, triggered=r18_score != 0))

        # --- R19: Bhavesh combust ---
        r19_score = 0.0
        if bhavesh in dignities:
            d = dignities[bhavesh]
            if d.cazimi:
                r19_score = +0.5
            elif d.combust and d.is_retrograde:
                r19_score = -0.5   # Asta Vakri (reduced effect)
            elif d.combust:
                r19_score = W["R19"]
        rules.append(RuleResult("R19", "Bhavesh combust", r19_score, triggered=r19_score != 0))

        # --- R20: Bhavesh in Dig Bala house ---
        r20_score = 0.0
        if bhavesh in _DIG_BALA_PEAK_HOUSE:
            if bhavesh_house in _DIG_BALA_PEAK_HOUSE[bhavesh]:
                r20_score = W["R20"]
        rules.append(RuleResult("R20", "Bhavesh in Dig Bala house", r20_score, triggered=r20_score != 0))

        # --- R21: Pushkara Navamsha (deferred — always 0 in pilot) ---
        rules.append(RuleResult("R21", "Bhavesh Pada in Pushkara Navamsha", 0.0, triggered=False))

        # --- R22: Bhavesh retrograde ---
        r22_score = 0.0
        if bhavesh in chart.planets and chart.planets[bhavesh].is_retrograde:
            if bhavesh in ("Jupiter", "Saturn"):
                r22_score = +0.25   # introspective — slightly beneficial
            elif bhavesh in ("Mercury", "Venus", "Mars"):
                r22_score = -0.50   # delayed significations
            else:
                r22_score = W["R22"]
        rules.append(RuleResult("R22", "Bhavesh retrograde", r22_score, triggered=r22_score != 0))

        # --- Aggregate ---
        raw = sum(
            r.score * (0.5 if r.is_wc else 1.0)
            for r in rules
        )
        final = max(-10.0, min(10.0, raw))

        result.houses[house] = HouseScore(
            house=house,
            domain=HOUSE_DOMAIN[house],
            bhavesh=bhavesh,
            bhavesh_house=bhavesh_house,
            rules=rules,
            raw_score=raw,
            final_score=final,
            rating=_rating(final),
        )

    return result
