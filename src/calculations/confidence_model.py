"""
src/calculations/confidence_model.py — Session 69

Interpretive confidence model (GAP 8).

Global confidence score per house incorporating:
  1. Varga agreement (already computed in varga_agreement.py) — weight 30%
  2. Conflicting indicators (benefic + malefic both active) — weight 25%
  3. Data sensitivity (birth time sensitivity from Monte Carlo) — weight 20%
  4. Score boundary proximity (close to 0 = uncertain) — weight 15%
  5. Functional role clarity (clear benefic/malefic roles) — weight 10%

Output: per-house confidence 0.0–1.0 with label.

Public API
----------
  compute_confidence(chart, sensitivity_report) -> ConfidenceReport
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HouseConfidence:
    house: int
    varga_agreement_score: float     # 0.0–1.0
    conflict_score: float            # 0.0–1.0 (high = less conflict = more confident)
    sensitivity_score: float         # 0.0–1.0 (low sensitivity = more confident)
    boundary_score: float            # 0.0–1.0 (far from 0 = more confident)
    role_clarity_score: float        # 0.0–1.0
    overall_confidence: float        # 0.0–1.0 weighted
    confidence_label: str            # "High"/"Moderate"/"Low"/"Uncertain"
    flags: list[str]                 # specific uncertainty flags


@dataclass
class ConfidenceReport:
    houses: dict[int, HouseConfidence]
    global_confidence: float
    most_reliable_houses: list[int]
    least_reliable_houses: list[int]
    requires_expert_review: list[int]


def compute_confidence(chart, sensitivity_report=None) -> ConfidenceReport:
    """Compute interpretive confidence for all 12 houses."""
    from src.calculations.varga_agreement import compute_varga_agreement
    from src.calculations.multi_axis_scoring import score_all_axes

    try:
        agree = compute_varga_agreement(chart)
    except Exception:
        agree = None

    try:
        axes = score_all_axes(chart, "parashari")
        d1_scores = axes.d1.scores if axes.d1 else {}
    except Exception:
        d1_scores = {}

    from src.calculations.house_lord import compute_house_map
    from src.calculations.functional_roles import compute_functional_roles
    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    try:
        fr = compute_functional_roles(chart)
        func_malefics = fr.functional_malefics
        func_benefics = fr.functional_benefics
    except Exception:
        func_malefics = set(); func_benefics = set()

    houses = {}
    for h in range(1, 13):
        flags = []

        # 1. Varga agreement
        if agree:
            flag = agree.flag_for(h)
            va_score = 1.0 if flag == "★★" else 0.65 if flag == "★" else 0.30
            if flag == "○":
                flags.append("Vargas diverge — chart has contradictory varga signals")
        else:
            va_score = 0.5

        # 2. Conflict (benefic + malefic both in house)
        in_house = [p for p, hp in ph.items() if hp == h]
        bens_in = [p for p in in_house if p in func_benefics]
        mals_in = [p for p in in_house if p in func_malefics]
        has_conflict = bool(bens_in and mals_in)
        conflict_score = 0.4 if has_conflict else 1.0
        if has_conflict:
            flags.append(f"Benefic/malefic conflict: {bens_in} vs {mals_in}")

        # 3. Sensitivity from Monte Carlo (if available)
        sens_score = 0.75  # default moderate
        if sensitivity_report:
            try:
                house_data = sensitivity_report.get("houses", {})
                key = str(h)
                if key in house_data:
                    stable = house_data[key].get("stable", True)
                    sens_score = 0.85 if stable else 0.40
                    if not stable:
                        flags.append("Birth time sensitive — minor changes shift this house score")
            except Exception:
                pass

        # 4. Boundary proximity (score near 0 = uncertain)
        raw = d1_scores.get(h, 0.0)
        boundary_score = min(1.0, abs(raw) / 2.0)  # confident when score clearly +/-
        if abs(raw) < 0.5:
            flags.append(f"Score near zero ({raw:+.2f}) — borderline interpretation")

        # 5. Functional role clarity
        lord = hmap.house_lord[h - 1]
        role_clear = lord in func_benefics or lord in func_malefics
        role_score = 0.90 if role_clear else 0.60
        if not role_clear:
            flags.append(f"Lord {lord} has mixed/unclear functional role")

        # Weighted combination
        overall = round(
            va_score      * 0.30 +
            conflict_score * 0.25 +
            sens_score    * 0.20 +
            boundary_score * 0.15 +
            role_score    * 0.10,
            4
        )

        if overall >= 0.75:   label = "High"
        elif overall >= 0.55: label = "Moderate"
        elif overall >= 0.35: label = "Low"
        else:                 label = "Uncertain"

        houses[h] = HouseConfidence(
            house=h, varga_agreement_score=round(va_score, 3),
            conflict_score=round(conflict_score, 3),
            sensitivity_score=round(sens_score, 3),
            boundary_score=round(boundary_score, 3),
            role_clarity_score=round(role_score, 3),
            overall_confidence=overall, confidence_label=label, flags=flags,
        )

    global_conf = round(sum(h.overall_confidence for h in houses.values()) / 12, 4)
    sorted_h = sorted(houses, key=lambda h: houses[h].overall_confidence, reverse=True)
    most_reliable = sorted_h[:3]
    least_reliable = sorted_h[-3:]
    expert_review = [h for h, hc in houses.items() if hc.confidence_label == "Uncertain"
                     or len(hc.flags) >= 3]

    return ConfidenceReport(
        houses=houses, global_confidence=global_conf,
        most_reliable_houses=most_reliable,
        least_reliable_houses=least_reliable,
        requires_expert_review=expert_review,
    )
