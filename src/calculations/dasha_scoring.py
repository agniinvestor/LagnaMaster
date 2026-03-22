"""
src/calculations/dasha_scoring.py
Dasha-sensitized scoring — adds temporal dimension to house scores.
Session 139 (Audit A-3, I-E).

The same natal chart produces different house activation profiles
depending on which Mahadasha/Antardasha is operating at query_date.

Sources:
  K.N. Rao · Planets in Signs and Houses, Introduction
  Hart de Fouw & Robert Svoboda · Light on Life Ch.11
  Gayatri Devi Vasudev · The Art of Prediction in Astrology Ch.4
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date

_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}


@dataclass
class DashaScoreModifier:
    """Modifier set for a single house score based on active dasha."""

    house: int
    base_score: float
    dasha_multiplier: float  # 1.5 if house lord is active dasha, 0.8 if inimical
    dasha_sensitized_score: float  # base_score × dasha_multiplier
    active_md_lord: str
    active_ad_lord: str
    md_is_house_lord: bool
    ad_is_house_lord: bool
    note: str


def _sign_lord(sign_index: int) -> str:
    _SL = {
        0: "Mars",
        1: "Venus",
        2: "Mercury",
        3: "Moon",
        4: "Sun",
        5: "Mercury",
        6: "Venus",
        7: "Mars",
        8: "Jupiter",
        9: "Saturn",
        10: "Saturn",
        11: "Jupiter",
    }
    return _SL.get(sign_index % 12, "Jupiter")


def _house_lord(house: int, lagna_si: int) -> str:
    return _sign_lord((lagna_si + house - 1) % 12)


def _house_from_lord(planet: str, lagna_si: int) -> list[int]:
    """Houses ruled by a planet given Lagna."""
    result = []
    _SL = {
        0: "Mars",
        1: "Venus",
        2: "Mercury",
        3: "Moon",
        4: "Sun",
        5: "Mercury",
        6: "Venus",
        7: "Mars",
        8: "Jupiter",
        9: "Saturn",
        10: "Saturn",
        11: "Jupiter",
    }
    for h in range(1, 13):
        si = (lagna_si + h - 1) % 12
        if _SL.get(si) == planet:
            result.append(h)
    return result


def _houses_6_8_12_from_house(house: int) -> set[int]:
    """Signs that are 6th, 8th, 12th from a given house."""
    return {(house + 5) % 12 or 12, (house + 7) % 12 or 12, (house + 11) % 12 or 12}


def compute_dasha_modifier(
    house: int,
    base_score: float,
    active_md_lord: str,
    active_ad_lord: str,
    lagna_si: int,
) -> DashaScoreModifier:
    """
    Compute dasha-sensitized modifier for a house score.

    Rules (K.N. Rao methodology):
    - If MD or AD lord rules this house → multiply by 1.5 (activation)
    - If MD lord is placed in 6th/8th/12th from this house → multiply by 0.8
    - If both → take higher

    Source: K.N. Rao · Planets in Signs and Houses, Introduction;
            Gayatri Devi Vasudev · Art of Prediction Ch.4
    """
    md_houses = _house_from_lord(active_md_lord, lagna_si)
    ad_houses = _house_from_lord(active_ad_lord, lagna_si)

    md_is_lord = house in md_houses
    ad_is_lord = house in ad_houses

    dusthana_from_house = _houses_6_8_12_from_house(house)
    md_in_dusthana = any(h in dusthana_from_house for h in md_houses)

    if md_is_lord or ad_is_lord:
        multiplier = 1.5
        note = f"{'MD' if md_is_lord else 'AD'} lord activates H{house}"
    elif md_in_dusthana:
        multiplier = 0.8
        note = f"MD lord {active_md_lord} in dusthana from H{house} — suppressed"
    else:
        multiplier = 1.0
        note = "Dasha neutral for this house"

    sensitized = round(base_score * multiplier, 4)

    return DashaScoreModifier(
        house=house,
        base_score=base_score,
        dasha_multiplier=multiplier,
        dasha_sensitized_score=sensitized,
        active_md_lord=active_md_lord,
        active_ad_lord=active_ad_lord,
        md_is_house_lord=md_is_lord,
        ad_is_house_lord=ad_is_lord,
        note=note,
    )


@dataclass
class DashaScoreReport:
    """Full dasha-sensitized score report for all 12 houses."""

    query_date: date
    active_md_lord: str
    active_ad_lord: str
    house_modifiers: list[DashaScoreModifier] = field(default_factory=list)

    @property
    def activated_houses(self) -> list[int]:
        """Houses with multiplier > 1.0 (actively fructifying)."""
        return [m.house for m in self.house_modifiers if m.dasha_multiplier > 1.0]

    @property
    def suppressed_houses(self) -> list[int]:
        """Houses with multiplier < 1.0 (suppressed by dasha)."""
        return [m.house for m in self.house_modifiers if m.dasha_multiplier < 1.0]

    def score_for_house(self, house: int) -> float:
        for m in self.house_modifiers:
            if m.house == house:
                return m.dasha_sensitized_score
        return 0.0


def apply_dasha_scoring(
    base_scores: dict[int, float],
    chart,
    query_date: date,
    dasha_tree=None,
) -> DashaScoreReport:
    """
    Apply dasha-sensitized multipliers to base house scores.

    Args:
        base_scores: {house_number: raw_score} for all 12 houses
        chart: BirthChart
        query_date: date to query (determines active MD/AD)
        dasha_tree: if None, uses Vimshottari MD lord from Moon nakshatra

    Returns: DashaScoreReport with modified scores per house
    """
    lagna_si = chart.lagna_sign_index

    # Determine active dasha lord
    md_lord = "Jupiter"  # default fallback
    ad_lord = "Jupiter"

    if dasha_tree is not None:
        # Walk dasha tree to find current MD/AD
        for md in dasha_tree if hasattr(dasha_tree, "__iter__") else []:
            if hasattr(md, "start") and hasattr(md, "end"):
                if md.start <= query_date <= md.end:
                    md_lord = md.lord
                    if hasattr(md, "antardashas"):
                        for ad in md.antardashas:
                            if (
                                hasattr(ad, "start")
                                and ad.start <= query_date <= ad.end
                            ):
                                ad_lord = ad.lord
                                break
                    break
    else:
        # Derive from Moon nakshatra (Vimshottari)
        _DASHA_LORDS = [
            "Ketu",
            "Venus",
            "Sun",
            "Moon",
            "Mars",
            "Rahu",
            "Jupiter",
            "Saturn",
            "Mercury",
        ]
        if "Moon" in chart.planets:
            moon_lon = chart.planets["Moon"].longitude
            nak_idx = int(moon_lon * 3 / 40) % 27
            md_lord = _DASHA_LORDS[nak_idx % 9]

    modifiers = []
    for house in range(1, 13):
        base = base_scores.get(house, 0.0)
        mod = compute_dasha_modifier(house, base, md_lord, ad_lord, lagna_si)
        modifiers.append(mod)

    return DashaScoreReport(
        query_date=query_date,
        active_md_lord=md_lord,
        active_ad_lord=ad_lord,
        house_modifiers=modifiers,
    )
