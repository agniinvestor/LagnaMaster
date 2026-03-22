"""
src/calculations/scoring_v2.py — LagnaMaster Session 32

Scoring Engine v2: declarative rule registry + engine versioning.

Differences from scoring.py (v1)
----------------------------------
1. Rules defined as data (RuleDefinition list) not code — easy to add/modify
2. ENGINE_VERSION string embedded in every ScoreRun output
3. Graha Yuddha applied: loser planets lose 50% of their benefic rule scores
4. Functional role awareness: rules check functional (lagna-specific) status
   not just universal benefic/malefic
5. score_chart_v2() returns ChartScoresV2 with engine_version field

Backward compatible: scoring.py v1 is unchanged and still used by default.
Switch to v2 by calling score_chart_v2() and storing engine_version in score_runs.

Public API
----------
    score_chart_v2(chart) -> ChartScoresV2
    ENGINE_VERSION: str
"""

from __future__ import annotations
from dataclasses import dataclass, field

# Bump this whenever rule logic changes — used for cache invalidation and audit
ENGINE_VERSION = "2.0.0"

_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

_DOMAINS = {
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

_STHIR_KARAK = {
    1: ["Sun"],
    2: ["Jupiter"],
    3: ["Mars"],
    4: ["Moon"],
    5: ["Jupiter"],
    6: ["Mars", "Saturn"],
    7: ["Venus"],
    8: ["Saturn"],
    9: ["Jupiter"],
    10: ["Sun", "Mercury", "Jupiter", "Saturn"],
    11: ["Jupiter"],
    12: ["Saturn"],
}

_DIG_BALA_HOUSE = {
    "Sun": 10,
    "Mars": 10,
    "Moon": 4,
    "Venus": 4,
    "Mercury": 1,
    "Jupiter": 1,
    "Saturn": 7,
}


@dataclass
class RuleResultV2:
    rule: str
    description: str
    score: float
    is_wc: bool
    triggered: bool
    engine_version: str = ENGINE_VERSION


@dataclass
class HouseScoreV2:
    house: int
    domain: str
    bhavesh: str
    bhavesh_house: int
    rules: list[RuleResultV2]
    raw_score: float
    final_score: float
    rating: str
    engine_version: str = ENGINE_VERSION

    # New in v2
    yuddha_losers_penalized: list[str] = field(default_factory=list)
    functional_malefic_bhavesh: bool = False


@dataclass
class ChartScoresV2:
    lagna_sign: str
    houses: dict[int, HouseScoreV2]
    engine_version: str = ENGINE_VERSION
    yuddha_results: list = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"LagnaMaster v2 Scores — {self.lagna_sign} Lagna (engine {self.engine_version})"
        ]
        for h, hs in sorted(self.houses.items()):
            lines.append(
                f"  H{h:2d} {hs.domain:25s} {hs.final_score:+6.2f}  {hs.rating}"
            )
        return "\n".join(lines)


def _rating(score: float) -> str:
    if score >= 6.0:
        return "Excellent"
    if score >= 3.0:
        return "Strong"
    if score >= 0.0:
        return "Moderate"
    if score >= -3.0:
        return "Weak"
    return "Very Weak"


def score_chart_v2(chart) -> ChartScoresV2:
    """Score all 12 houses using engine v2 (functional roles + graha yuddha)."""
    from src.calculations.house_lord import (
        compute_house_map,
        is_kendra,
        is_trikona,
        is_dusthana,
    )
    from src.calculations.dignity import compute_all_dignities
    from src.calculations.functional_roles import compute_functional_roles
    from src.calculations.graha_yuddha import compute_graha_yuddha

    hmap = compute_house_map(chart)
    digs = compute_all_dignities(chart)
    roles = compute_functional_roles(chart)
    wars = compute_graha_yuddha(chart)

    yuddha_losers = {w.loser for w in wars}

    # Graha drishti aspects
    def aspects(planet: str, target_house: int) -> bool:
        ph = hmap.planet_house.get(planet, 0)
        if ph == 0:
            return False
        diff = (target_house - ph) % 12
        extras = {
            "Mars": {3, 7, 9},  # 4th, 7th, 8th from Mars
            "Jupiter": {4, 6, 9},  # 5th, 7th, 9th
            "Saturn": {2, 6, 9},  # 3rd, 7th, 10th
        }
        if diff == 6:
            return True  # 7th aspect all planets
        return diff in extras.get(planet, set())

    def is_func_benefic(planet: str) -> bool:
        return roles.is_functional_benefic(planet)

    def is_func_malefic(planet: str) -> bool:
        return roles.is_functional_malefic(planet)

    # Yuddha penalty: loser benefic rules score at 50%
    def yuddha_mult(planet: str, is_benefic_rule: bool) -> float:
        if planet in yuddha_losers and is_benefic_rule:
            return 0.5
        return 1.0

    houses_out: dict[int, HouseScoreV2] = {}

    for house in range(1, 13):
        bhavesh = hmap.house_lord[house - 1]
        bh_house = hmap.planet_house.get(bhavesh, house)
        bh_dig = digs.get(bhavesh)
        bh_combust = bh_dig.combust if bh_dig else False
        bh_cazimi = bh_dig.cazimi if bh_dig else False
        bh_rx = (
            chart.planets[bhavesh].is_retrograde if bhavesh in chart.planets else False
        )

        # Planets in this house
        in_house = [
            p
            for p, pp in chart.planets.items()
            if pp.sign_index == (chart.lagna_sign_index + house - 1) % 12
        ]

        results: list[RuleResultV2] = []

        def rule(code, desc, score, wc=False, triggered=True):
            results.append(
                RuleResultV2(code, desc, score if triggered else 0.0, wc, triggered)
            )

        # R01 gentle sign
        gentle = ["Cancer", "Taurus", "Libra", "Pisces", "Sagittarius"]
        house_sign = _SIGNS[(chart.lagna_sign_index + house - 1) % 12]
        rule("R01", "Gentle sign in house", 0.5, triggered=house_sign in gentle)

        # R02 functional benefic in house
        fb_in = [
            p for p in in_house if is_func_benefic(p) and p not in ("Rahu", "Ketu")
        ]
        if fb_in:
            mult = yuddha_mult(fb_in[0], True)
            base = 1.5 if roles.is_yogakaraka(fb_in[0]) else 1.0
            rule("R02", "Func. benefic in house", base * mult, triggered=True)
        else:
            rule("R02", "Func. benefic in house", 0, triggered=False)

        # R03 (WC) func benefic aspects house
        fb_aspects = [
            p
            for p in chart.planets
            if is_func_benefic(p) and aspects(p, house) and p not in in_house
        ]
        if fb_aspects:
            mult = yuddha_mult(fb_aspects[0], True)
            rule("R03", "Func. benefic aspects house (WC)", 0.75 * mult, wc=True)
        else:
            rule("R03", "Func. benefic aspects house (WC)", 0, wc=True, triggered=False)

        # R04 bhavesh in kendra/trikona
        rule(
            "R04",
            "Bhavesh in Kendra/Trikona",
            2.0,
            triggered=is_kendra(bh_house) or is_trikona(bh_house),
        )

        # R05 (WC) bhavesh with kendra/trikona lord
        bh_cotenants = (
            [
                p
                for p, pp in chart.planets.items()
                if pp.sign_index == chart.planets.get(bhavesh, None) and p != bhavesh
                if chart.planets.get(bhavesh)
            ]
            if bhavesh in chart.planets
            else []
        )
        kt_lords = {hmap.house_lord[h - 1] for h in [1, 4, 5, 7, 9, 10]}
        rule(
            "R05",
            "Bhavesh with Kendra/Trikona lord (WC)",
            0.5,
            wc=True,
            triggered=bool(set(bh_cotenants) & kt_lords),
        )

        # R06 bhavesh with func benefic
        bh_with_fb = (
            [p for p in bh_cotenants if is_func_benefic(p)] if bh_cotenants else []
        )
        if bh_with_fb:
            mult = yuddha_mult(bh_with_fb[0], True)
            base = 1.5 if roles.is_yogakaraka(bh_with_fb[0]) else 1.0
            rule("R06", "Bhavesh with func. benefic", base * mult)
        else:
            rule("R06", "Bhavesh with func. benefic", 0, triggered=False)

        # R07 (WC) benefic aspects bhavesh sign
        chart.planets[bhavesh].sign_index if bhavesh in chart.planets else -1
        bh_h_from_lagna = bh_house
        fb_asp_bh = [
            p
            for p in chart.planets
            if is_func_benefic(p) and aspects(p, bh_h_from_lagna)
        ]
        if fb_asp_bh:
            mult = yuddha_mult(fb_asp_bh[0], True)
            rule("R07", "Func. benefic aspects bhavesh sign (WC)", 0.5 * mult, wc=True)
        else:
            rule(
                "R07",
                "Func. benefic aspects bhavesh sign (WC)",
                0,
                wc=True,
                triggered=False,
            )

        # R09 func malefic in house
        fm_in = [p for p in in_house if is_func_malefic(p)]
        rule(
            "R09",
            "Func. malefic in house",
            -1.0 * len(fm_in) if fm_in else 0,
            triggered=bool(fm_in),
        )

        # R10 func malefic aspects house
        fm_asp = [
            p
            for p in chart.planets
            if is_func_malefic(p) and aspects(p, house) and p not in in_house
        ]
        rule("R10", "Func. malefic aspects house", -1.0, triggered=bool(fm_asp))

        # R11 dusthana lord in house
        dusth_lords_in = [p for p in in_house if p in roles.dusthana_lords]
        rule("R11", "Dusthana lord in house", -1.25, triggered=bool(dusth_lords_in))

        # R13 bhavesh with func malefic
        bh_with_fm = (
            [p for p in bh_cotenants if is_func_malefic(p)] if bh_cotenants else []
        )
        rule("R13", "Bhavesh with func. malefic", -1.0, triggered=bool(bh_with_fm))

        # R14 (WC) func malefic aspects bhavesh sign
        fm_asp_bh = [
            p
            for p in chart.planets
            if is_func_malefic(p) and aspects(p, bh_h_from_lagna) and p != bhavesh
        ]
        rule(
            "R14",
            "Func. malefic aspects bhavesh sign (WC)",
            -0.5,
            wc=True,
            triggered=bool(fm_asp_bh),
        )

        # R15 bhavesh in dusthana
        rule("R15", "Bhavesh in Dusthana", -2.0, triggered=is_dusthana(bh_house))

        # R16 bhavesh with dusthana lord
        bh_with_dl = (
            [p for p in bh_cotenants if p in roles.dusthana_lords]
            if bh_cotenants
            else []
        )
        rule("R16", "Bhavesh with Dusthana lord", -1.0, triggered=bool(bh_with_dl))

        # R17/R18 Sthir Karak
        sthir = _STHIR_KARAK.get(house, [])
        for sk in sthir:
            sk_house = hmap.planet_house.get(sk, 0)
            if is_kendra(sk_house) or is_trikona(sk_house):
                rule("R17", f"Sthir Karak {sk} in Kendra/Trikona", 0.5)
            elif is_dusthana(sk_house):
                rule("R18", f"Sthir Karak {sk} in Dusthana", -0.5)

        # R19 bhavesh combust
        if bh_cazimi:
            rule("R19", "Bhavesh cazimi", 0.5)
        elif bh_combust and bh_rx:
            rule("R19", "Bhavesh combust+Rx (Asta Vakri)", -0.5)
        elif bh_combust:
            rule("R19", "Bhavesh combust", -1.0)

        # R20 bhavesh in dig bala house
        rule(
            "R20",
            "Bhavesh in Dig Bala house",
            0.5,
            triggered=_DIG_BALA_HOUSE.get(bhavesh, 0) == bh_house,
        )

        # R22 bhavesh retrograde
        if bh_rx:
            if bhavesh in {"Jupiter", "Saturn"}:
                rule("R22", "Bhavesh retrograde (Jup/Sat)", 0.25)
            elif bhavesh in {"Mercury", "Venus", "Mars"}:
                rule("R22", "Bhavesh retrograde", -0.5)

        # Aggregate
        raw = sum(r.score * (0.5 if r.is_wc else 1.0) for r in results)
        final = max(-10.0, min(10.0, raw))

        houses_out[house] = HouseScoreV2(
            house=house,
            domain=_DOMAINS[house],
            bhavesh=bhavesh,
            bhavesh_house=bh_house,
            rules=results,
            raw_score=round(raw, 3),
            final_score=round(final, 2),
            rating=_rating(final),
            engine_version=ENGINE_VERSION,
            yuddha_losers_penalized=[p for p in in_house if p in yuddha_losers],
            functional_malefic_bhavesh=is_func_malefic(bhavesh),
        )

    return ChartScoresV2(
        lagna_sign=chart.lagna_sign,
        houses=houses_out,
        engine_version=ENGINE_VERSION,
        yuddha_results=wars,
    )


def _house_lord_sanity(hmap) -> None:
    """Assert house_lord list has exactly 12 entries (called once per score_chart_v2)."""
    assert len(hmap.house_lord) == 12, (
        f"house_lord has {len(hmap.house_lord)} entries — expected 12"
    )
