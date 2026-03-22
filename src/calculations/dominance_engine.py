"""
src/calculations/dominance_engine.py — Session 64

Dominance Hierarchy Engine — resolves which chart factors dominate.

Classical rules encoded:
  BENEFIC OVERRIDE: Jupiter in kendra without severe affliction can suppress
    negatives in the houses it aspects/occupies (BPHS Ch.34).
  MALEFIC DOMINANCE: Combust, debilitated, or severely afflicted planets
    cannot initiate yogas they are part of (BPHS Ch.3, PVRNR p147).
  DASHA PRIORITY: Running dasha lord's natal strength is the primary filter —
    a strong dasha lord elevates the whole period; weak one depresses it.
  ACTIVATION DOMINANCE: Active dasha lord's house(s) get ×1.5 weight.
  AFFLICTION THRESHOLD: If a house has both benefic yoga AND severe malefic
    affliction, the affliction dominates when > 2.0 points of malefic influence.

Public API
----------
  compute_dominance_factors(chart, dashas, on_date) -> DominanceReport
  dominant_theme(chart, dashas, on_date) -> str
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_NAT_BENEF = {"Jupiter", "Venus", "Mercury", "Moon"}
_NAT_MALEF = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}


@dataclass
class DominanceFactor:
    factor_type: (
        str  # "Benefic Override"/"Malefic Dominance"/"Dasha Priority"/"Activation"
    )
    planet: str
    houses_affected: list[int]
    strength: float  # magnitude of the dominance effect
    description: str
    overrides: list[str]  # what this factor suppresses


@dataclass
class DominanceReport:
    factors: list[DominanceFactor]
    benefic_overrides: list[DominanceFactor]
    malefic_dominances: list[DominanceFactor]
    dasha_priority: DominanceFactor | None
    dominant_positive_house: int | None
    dominant_negative_house: int | None
    affliction_dominated_houses: list[int]
    yoga_dominated_houses: list[int]
    global_tone: (
        str  # "Positive"/"Mixed Positive"/"Neutral"/"Mixed Negative"/"Negative"
    )


def compute_dominance_factors(
    chart, dashas=None, on_date: date | None = None
) -> DominanceReport:
    if on_date is None:
        on_date = date.today()

    from src.calculations.house_lord import compute_house_map
    from src.calculations.functional_roles import compute_functional_roles
    from src.calculations.multi_axis_scoring import score_all_axes

    hmap = compute_house_map(chart)
    fr = compute_functional_roles(chart)
    ph = hmap.planet_house

    try:
        axes = score_all_axes(chart, "parashari")
        d1_scores = axes.d1.scores if axes.d1 else {}
    except Exception:
        d1_scores = {}

    factors = []

    # ── Benefic Override Rules ────────────────────────────────────────────────
    # Jupiter in kendra: aspects H1,H5,H7,H9 from its position
    jup_h = ph.get("Jupiter", 0)
    if jup_h in _KENDRA:
        # Jupiter aspects 5th and 9th from its position + 7th
        jup_aspects = {
            jup_h,
            (jup_h + 4) % 12 + 1,
            (jup_h + 6) % 12 + 1,
            (jup_h + 8) % 12 + 1,
        }
        jup_aspects = {h for h in jup_aspects if 1 <= h <= 12}
        try:
            from src.calculations.dignity import compute_all_dignities

            dig = compute_all_dignities(chart).get("Jupiter")
            jup_strong = not (dig and dig.combust)
        except Exception:
            jup_strong = True
        if jup_strong:
            factors.append(
                DominanceFactor(
                    factor_type="Benefic Override",
                    planet="Jupiter",
                    houses_affected=list(jup_aspects),
                    strength=1.5,
                    description=f"Jupiter in H{jup_h} (kendra) — aspects strengthen benefic promise in houses {sorted(jup_aspects)}",
                    overrides=["mild malefic influences in aspected houses"],
                )
            )

    # Venus in own sign in kendra/trikona
    ven_h = ph.get("Venus", 0)
    ven_si = chart.planets.get("Venus")
    _VEN_OWN = {1, 6}  # Taurus si=1, Libra si=6
    if ven_h in _KENDRA | _TRIKONA and ven_si and ven_si.sign_index in _VEN_OWN:
        factors.append(
            DominanceFactor(
                factor_type="Benefic Override",
                planet="Venus",
                houses_affected=[ven_h],
                strength=1.25,
                description=f"Venus in own sign in H{ven_h} — protective benefic influence",
                overrides=["moderate afflictions to that house"],
            )
        )

    # ── Malefic Dominance Rules ───────────────────────────────────────────────
    # Combust planets cannot initiate yogas
    try:
        from src.calculations.dignity import compute_all_dignities

        digs = compute_all_dignities(chart)
        for planet, dig in digs.items():
            if dig and dig.combust and planet in _NAT_BENEF:
                factors.append(
                    DominanceFactor(
                        factor_type="Malefic Dominance",
                        planet=planet,
                        houses_affected=[ph.get(planet, 0)],
                        strength=-1.5,
                        description=f"{planet} combust — cannot initiate yogas it is part of (BPHS Ch.3)",
                        overrides=[f"yogas involving {planet}"],
                    )
                )
    except Exception:
        pass

    # Severe affliction: functional malefic conjunct within tight orb
    for planet, pos in chart.planets.items():
        if planet in fr.functional_malefics:
            house = ph.get(planet, 0)
            if house in {6, 8, 12}:  # malefic in dusthana can be ok
                continue
            # Check if it afflicts any yoga lords
            for other, other_pos in chart.planets.items():
                if other != planet and other_pos.sign_index == pos.sign_index:
                    orb = abs(pos.longitude - other_pos.longitude) % 360
                    if orb > 180:
                        orb = 360 - orb
                    if orb < 6:  # tight affliction
                        factors.append(
                            DominanceFactor(
                                factor_type="Malefic Dominance",
                                planet=planet,
                                houses_affected=[house],
                                strength=-1.25,
                                description=f"{planet} (func malefic) within {orb:.1f}° of {other} — severe affliction",
                                overrides=[f"positive effects of {other} in H{house}"],
                            )
                        )

    # ── Dasha Priority ────────────────────────────────────────────────────────
    dasha_priority = None
    if dashas:
        try:
            from src.calculations.vimshottari_dasa import current_dasha

            md, ad = current_dasha(dashas, on_date)
            md_house = ph.get(md.lord, 0)
            md_d1 = d1_scores.get(md_house, 0.0)
            # Dasha lord in strong house = positive period
            md_strong = md_house in _KENDRA | _TRIKONA
            md_score = md_d1
            dasha_priority = DominanceFactor(
                factor_type="Dasha Priority",
                planet=md.lord,
                houses_affected=[md_house, ph.get(ad.lord, 0)],
                strength=md_score * 1.5 if md_strong else md_score,
                description=f"MD {md.lord} (H{md_house}, D1={md_d1:+.2f}) + AD {ad.lord} — primary activation filter",
                overrides=["static natal promise for this period"],
            )
            factors.append(dasha_priority)
        except Exception:
            pass

    # ── Classify houses ───────────────────────────────────────────────────────
    benefic_fs = [f for f in factors if f.factor_type == "Benefic Override"]
    malefic_fs = [f for f in factors if f.factor_type == "Malefic Dominance"]

    # Houses where affliction score > yoga score (affliction dominated)
    affliction_dominated = []
    yoga_dominated = []
    for h in range(1, 13):
        score = d1_scores.get(h, 0.0)
        if score < -2.0:
            affliction_dominated.append(h)
        elif score > 2.0:
            yoga_dominated.append(h)

    # Global tone from D1 scores
    avg_score = sum(d1_scores.values()) / 12 if d1_scores else 0
    if avg_score > 1.5:
        tone = "Positive"
    elif avg_score > 0.5:
        tone = "Mixed Positive"
    elif avg_score > -0.5:
        tone = "Neutral"
    elif avg_score > -1.5:
        tone = "Mixed Negative"
    else:
        tone = "Negative"

    dom_pos = max(d1_scores, key=d1_scores.get) if d1_scores else None
    dom_neg = min(d1_scores, key=d1_scores.get) if d1_scores else None

    return DominanceReport(
        factors=factors,
        benefic_overrides=benefic_fs,
        malefic_dominances=malefic_fs,
        dasha_priority=dasha_priority,
        dominant_positive_house=dom_pos,
        dominant_negative_house=dom_neg,
        affliction_dominated_houses=affliction_dominated,
        yoga_dominated_houses=yoga_dominated,
        global_tone=tone,
    )


def dominant_theme(chart, dashas=None, on_date: date | None = None) -> str:
    """Return a single sentence describing the dominant chart theme."""
    report = compute_dominance_factors(chart, dashas, on_date)
    if report.dasha_priority:
        dp = report.dasha_priority
        return f"{dp.planet} MD ({dp.description.split('—')[1].strip()}); chart tone: {report.global_tone}"
    return f"Chart tone: {report.global_tone}; strongest house: H{report.dominant_positive_house}"
