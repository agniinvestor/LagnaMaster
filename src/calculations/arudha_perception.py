"""
src/calculations/arudha_perception.py — Session 61

Arudha Lagna perception model (PVRNR Ch.9 p85-104).

AL = maya/illusion about self. House = actual reality.
Conflict between them shows hidden success or apparent failure.

PVRNR rules (p102):
  Malefics in 3rd/6th from AL → bold, hits enemies, materially successful
  Benefics in 3rd/6th from AL → gentle, restrained, saintly nature
  11th from AL → financial gains
  12th from AL → expenditures

Reality vs Perception framework:
  Strong house (actual) + Strong AL → genuine success, recognized
  Strong house + Weak AL  → hidden success, underestimated by world
  Weak house  + Strong AL → apparent success, overestimated by world
  Weak house  + Weak AL   → recognized struggles

Public API
----------
  compute_al_perception(chart, house) -> PerceptionAnalysis
  compute_full_perception_model(chart) -> dict[int, PerceptionAnalysis]
"""
from __future__ import annotations
from dataclasses import dataclass

_NAT_BENEFIC = {"Jupiter","Venus","Mercury","Moon"}
_NAT_MALEFIC = {"Sun","Mars","Saturn","Rahu","Ketu"}


@dataclass
class PerceptionAnalysis:
    house: int
    actual_score: float          # from scoring engine (reality)
    al_sign_index: int           # arudha pada sign
    al_score: float              # score from arudha's perspective
    conflict_type: str           # "Aligned"/"Hidden Success"/"Apparent Success"/"Recognized Struggle"
    malefics_3_6_from_al: list[str]    # → bold, successful
    benefics_3_6_from_al: list[str]    # → gentle/saintly
    material_strength: float    # composite: positive = materially prosperous
    commentary: str


def _house_score_from_sign(si: int, chart, school: str = "parashari") -> float:
    """Get the D1 score for the house containing a given sign index."""
    try:
        from src.calculations.multi_axis_scoring import score_axis
        lagna_si = chart.lagna_sign_index
        ax = score_axis(chart, lagna_si, "D1", school)
        # Find which house has this sign
        h = (si - lagna_si) % 12 + 1
        return ax.scores.get(h, 0.0)
    except Exception:
        return 0.0


def compute_al_perception(chart, house: int) -> PerceptionAnalysis:
    """Perception analysis for a given house."""
    from src.calculations.multi_lagna import compute_all_arudha_padas
    try:
        arudha_all = compute_all_arudha_padas(chart)
        al_pada = arudha_all.padas.get(house)
        al_si = al_pada.sign_index if al_pada else chart.lagna_sign_index
    except Exception:
        al_si = chart.lagna_sign_index

    # Actual score (reality)
    try:
        from src.calculations.multi_axis_scoring import score_axis
        lagna_si = chart.lagna_sign_index
        ax = score_axis(chart, lagna_si, "D1", "parashari")
        actual_score = ax.scores.get(house, 0.0)
    except Exception:
        actual_score = 0.0

    # AL-based score: score of AL sign as a reference
    al_score = _house_score_from_sign(al_si, chart)

    # Planets in 3rd and 6th from AL
    h3_from_al = (al_si + 2) % 12
    h6_from_al = (al_si + 5) % 12
    mals_36 = [p for p, pos in chart.planets.items()
               if pos.sign_index in {h3_from_al, h6_from_al} and p in _NAT_MALEFIC]
    bens_36 = [p for p, pos in chart.planets.items()
               if pos.sign_index in {h3_from_al, h6_from_al} and p in _NAT_BENEFIC]

    # Conflict type
    act_pos = actual_score > 0
    al_pos  = al_score > 0
    if act_pos and al_pos:
        conflict = "Aligned"
        comment = "Reality and perception aligned — success is genuine and recognized"
    elif act_pos and not al_pos:
        conflict = "Hidden Success"
        comment = "Strong actual house but weak AL — hidden achievement, underestimated"
    elif not act_pos and al_pos:
        conflict = "Apparent Success"
        comment = "Weak actual house but strong AL — perceived better than reality"
    else:
        conflict = "Recognized Struggle"
        comment = "Both actual and perception weak — struggles are visible"

    # Material strength from AL indicators
    material = (len(mals_36) * 0.5 - len(bens_36) * 0.25 + max(-2, min(2, al_score)) * 0.5)
    material = round(material, 3)

    return PerceptionAnalysis(
        house=house, actual_score=round(actual_score, 3),
        al_sign_index=al_si, al_score=round(al_score, 3),
        conflict_type=conflict,
        malefics_3_6_from_al=mals_36,
        benefics_3_6_from_al=bens_36,
        material_strength=material,
        commentary=comment,
    )


def compute_full_perception_model(chart) -> dict[int, PerceptionAnalysis]:
    """Compute perception analysis for all 12 houses."""
    return {h: compute_al_perception(chart, h) for h in range(1, 13)}
