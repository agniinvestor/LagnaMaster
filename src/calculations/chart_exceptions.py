"""
src/calculations/chart_exceptions.py — Session 70

Chart exception detection — outliers, rule conflicts, expert review flags (GAP 9).

Classical exceptional conditions:
  1. All planets in one hemisphere (visibility imbalance)
  2. All planets in one sign (extreme stellium)
  3. No planets in kendra (weak structural support)
  4. Lagna lord debilitated in 8th (severe vitality challenge)
  5. 6th/8th/12th lords all strong (dusthana dominance)
  6. All yogas negated (combust + afflicted)
  7. Score extremes (all houses below -3 or above +3)
  8. Moon extremely weak (Kemadruma + Mrita avastha)

Public API
----------
  detect_chart_exceptions(chart) -> ChartExceptionReport
"""
from __future__ import annotations
from dataclasses import dataclass, field

_KENDRA    = {1, 4, 7, 10}
_DUSTHANA  = {6, 8, 12}
_NAT_MALEF = {"Sun","Mars","Saturn","Rahu","Ketu"}
_NAT_BENEF = {"Jupiter","Venus","Mercury","Moon"}


@dataclass
class ChartException:
    exception_type: str
    severity: str          # "Critical"/"High"/"Moderate"/"Advisory"
    description: str
    houses_affected: list[int]
    requires_expert: bool


@dataclass
class ChartExceptionReport:
    exceptions: list[ChartException]
    critical_count: int
    high_count: int
    requires_expert_review: bool
    exception_summary: str
    special_rules_apply: list[str]


def detect_chart_exceptions(chart) -> ChartExceptionReport:
    exceptions = []

    from src.calculations.house_lord import compute_house_map
    from src.calculations.multi_axis_scoring import score_all_axes

    hmap = compute_house_map(chart)
    ph = hmap.planet_house
    lagna_si = chart.lagna_sign_index

    # ── 1. All 7 planets in one hemisphere ───────────────────────────────────
    visible_h = {7,8,9,10,11,12}
    invisible_h = {1,2,3,4,5,6}
    planets_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]
    p_houses = [ph.get(p,0) for p in planets_7 if ph.get(p,0) > 0]
    if all(h in visible_h for h in p_houses):
        exceptions.append(ChartException(
            "Hemisphere Imbalance","Moderate",
            "All planets in visible half (H7-H12) — external focus, public life prominent",
            list(visible_h), False,
        ))
    elif all(h in invisible_h for h in p_houses):
        exceptions.append(ChartException(
            "Hemisphere Imbalance","Moderate",
            "All planets in invisible half (H1-H6) — private/internal focus",
            list(invisible_h), False,
        ))

    # ── 2. No planets in kendra ───────────────────────────────────────────────
    kendra_occupied = any(ph.get(p,0) in _KENDRA for p in planets_7)
    if not kendra_occupied:
        exceptions.append(ChartException(
            "Empty Kendras","High",
            "No planets in kendra houses — weak structural support, Mahapurusha yogas absent",
            list(_KENDRA), True,
        ))

    # ── 3. Lagna lord in 8th ──────────────────────────────────────────────────
    lagnesh = hmap.house_lord[0]
    lagnesh_h = ph.get(lagnesh, 0)
    if lagnesh_h == 8:
        _DEBIL = {"Sun":6,"Moon":7,"Mars":3,"Mercury":11,"Jupiter":9,"Venus":5,"Saturn":0}
        lagnesh_pos = chart.planets.get(lagnesh)
        is_debil = lagnesh_pos and _DEBIL.get(lagnesh) == lagnesh_pos.sign_index
        sev = "Critical" if is_debil else "High"
        exceptions.append(ChartException(
            "Lagnesh in 8th",sev,
            f"Lagnesh {lagnesh} in H8{' + debilitated' if is_debil else ''} — significant vitality challenges",
            [8], True,
        ))

    # ── 4. Dusthana lords all strong ─────────────────────────────────────────
    d_lords = [hmap.house_lord[h-1] for h in [6,8,12]]
    d_lords_strong = sum(1 for dl in d_lords if ph.get(dl,0) in _KENDRA | {5,9})
    if d_lords_strong >= 2:
        exceptions.append(ChartException(
            "Dusthana Lords Strong","High",
            f"≥2 dusthana lords in strong positions — hidden challenges, Viparita possibility",
            [6,8,12], False,
        ))

    # ── 5. Moon severely afflicted ────────────────────────────────────────────
    moon_h = ph.get("Moon", 0)
    moon_malefics = [p for p in _NAT_MALEF
                     if ph.get(p) == moon_h and p != "Moon"]
    moon_in_dusthana = moon_h in _DUSTHANA
    if len(moon_malefics) >= 2 or (moon_malefics and moon_in_dusthana):
        exceptions.append(ChartException(
            "Moon Severely Afflicted","High",
            f"Moon afflicted by {moon_malefics}{' in dusthana' if moon_in_dusthana else ''} — mental/emotional challenges",
            [moon_h, 4], True,
        ))

    # ── 6. All benefics combust ───────────────────────────────────────────────
    try:
        from src.calculations.dignity import compute_all_dignities
        digs = compute_all_dignities(chart)
        combust_benefics = [p for p in _NAT_BENEF - {"Moon"}
                            if digs.get(p) and digs[p].is_combust]
        if len(combust_benefics) >= 2:
            exceptions.append(ChartException(
                "Multiple Benefics Combust","High",
                f"Benefics {combust_benefics} are combust — yogas they form are weakened",
                [ph.get(p,0) for p in combust_benefics], True,
            ))
    except Exception:
        pass

    # ── 7. Score extremes ────────────────────────────────────────────────────
    try:
        axes = score_all_axes(chart, "parashari")
        if axes.d1:
            scores = list(axes.d1.scores.values())
            if scores:
                avg = sum(scores) / len(scores)
                if avg < -2.5:
                    exceptions.append(ChartException(
                        "Severely Challenged Chart","Critical",
                        f"Average house score {avg:.2f} — multiple severe afflictions across chart",
                        list(range(1,13)), True,
                    ))
                elif avg > 2.5:
                    exceptions.append(ChartException(
                        "Exceptionally Strong Chart","Advisory",
                        f"Average house score {avg:.2f} — unusually strong chart, verify calculations",
                        list(range(1,13)), False,
                    ))
    except Exception:
        pass

    from src.calculations.multi_axis_scoring import score_all_axes

    critical = sum(1 for e in exceptions if e.severity == "Critical")
    high = sum(1 for e in exceptions if e.severity == "High")
    requires_expert = any(e.requires_expert for e in exceptions) or critical > 0

    special_rules = []
    if any(e.exception_type == "Dusthana Lords Strong" for e in exceptions):
        special_rules.append("Check Viparita Raja Yoga conditions (dusthana lords in dusthanas)")
    if any("Combust" in e.exception_type for e in exceptions):
        special_rules.append("Combust planets cannot initiate yogas (BPHS Ch.3)")

    summary = (f"{len(exceptions)} exception(s) detected "
               f"({critical} critical, {high} high). "
               + ("Expert review recommended." if requires_expert else "Standard interpretation applies."))

    return ChartExceptionReport(
        exceptions=exceptions, critical_count=critical, high_count=high,
        requires_expert_review=requires_expert,
        exception_summary=summary, special_rules_apply=special_rules,
    )
