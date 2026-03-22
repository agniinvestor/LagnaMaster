"""
src/calculations/scenario.py — Session 40

Counterfactual / scenario explorer (UX_CounterfactualExplorer).
Lets you override one or more planet positions and recompute all scores.

Usage:
  override = {"Sun": {"longitude": 45.0}}   # Sun moves to Taurus 15°
  scenario_chart = apply_scenario(chart, override)
  scenario_scores = score_chart_v3(scenario_chart)

Public API
----------
  apply_scenario(chart, overrides: dict) -> modified BirthChart copy
  compare_scenarios(base_chart, overrides_list, dashas, on_date, school)
      -> list[ScenarioResult]
"""

from __future__ import annotations
from dataclasses import dataclass
import copy

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


@dataclass
class ScenarioResult:
    label: str
    d1_delta: dict[int, float]  # house -> score change vs base
    lpi_delta: dict[int, float]
    summary: str


def apply_scenario(chart, overrides: dict):
    """
    Return a modified copy of chart with planet longitudes overridden.
    overrides = {"Sun": {"longitude": 45.0}, "Moon": {"longitude": 93.5}}
    """
    new_chart = copy.deepcopy(chart)
    for planet, changes in overrides.items():
        if planet not in new_chart.planets:
            continue
        pos = new_chart.planets[planet]
        if "longitude" in changes:
            lon = changes["longitude"] % 360
            si = int(lon / 30) % 12
            # Rebuild the position
            from src.ephemeris import PlanetPosition

            new_chart.planets[planet] = PlanetPosition(
                name=planet,
                longitude=lon,
                sign=_SIGNS[si],
                sign_index=si,
                degree_in_sign=lon % 30,
                is_retrograde=pos.is_retrograde,
                speed=pos.speed,
            )
    return new_chart


def compare_scenarios(
    base_chart,
    overrides_list: list[tuple[str, dict]],  # [(label, overrides), ...]
    dashas=None,
    on_date=None,
    school="parashari",
) -> list[ScenarioResult]:
    from src.calculations.scoring_v3 import score_chart_v3
    from datetime import date

    if on_date is None:
        on_date = date.today()
    if dashas is None:
        dashas = []

    base = score_chart_v3(base_chart, dashas, on_date, school)
    results = []
    for label, overrides in overrides_list:
        sc = apply_scenario(base_chart, overrides)
        sc_scores = score_chart_v3(sc, dashas, on_date, school)
        d1_delta = {
            h: round(sc_scores.d1_scores[h] - base.d1_scores[h], 3)
            for h in range(1, 13)
        }
        lpi_delta = {}
        if base.lpi and sc_scores.lpi:
            lpi_delta = {
                h: round(
                    sc_scores.lpi.houses[h].full_index - base.lpi.houses[h].full_index,
                    3,
                )
                for h in range(1, 13)
            }
        best_h = max(d1_delta, key=d1_delta.get)
        worst_h = min(d1_delta, key=d1_delta.get)
        summary = (
            f"Scenario '{label}': best gain H{best_h} ({d1_delta[best_h]:+.2f}), "
            f"worst H{worst_h} ({d1_delta[worst_h]:+.2f})"
        )
        results.append(
            ScenarioResult(
                label=label,
                d1_delta=d1_delta,
                lpi_delta=lpi_delta,
                summary=summary,
            )
        )
    return results
