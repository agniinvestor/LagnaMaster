"""
src/calculations/mundane.py — Session 98

Mundane Astrology (PVRNR Ch.35, p460-469).
Predicting collective fortune of nations, groups, institutions.

Chart types:
  1. Nation birth chart (independence/founding date)
  2. Solar ingress charts (Sun entering each sign, esp. Aries = new year)
  3. Lunar new year charts (Sun-Moon conjunction in Pisces)
  4. Swearing-in / inauguration charts
  5. Compressed Vimshottari for short periods (month/year scale)

Mundane house significations (PVRNR p461):
  H1: general state, public health, cabinet
  H2: state revenue, wealth, imports
  H3: telecommunications, transportation, media
  H4: education, real estate, agriculture
  H5: children, crime, mentality of leaders
  H6: debt, diseases, armed forces
  H7: women's health, war, foreign relations
  H8: death rate, treasury, sudden events
  H9: religion, judiciary, foreign affairs
  H10: government, ruling party, leadership
  H11: parliament, gains, alliances
  H12: expenditure, foreign enemies, hospitals
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime

_MUNDANE_HOUSES = {
    1:  "General state of affairs, public health, cabinet",
    2:  "State revenue, wealth, imports, commerce, allies",
    3:  "Telecommunications, transportation, journalism, media",
    4:  "Educational institutions, real estate, trade, agriculture",
    5:  "Children, new births, crime, parks, mentality of leaders",
    6:  "State loans, debt, diseases, armed forces",
    7:  "Health of women, infant mortality, war, foreign relations",
    8:  "Death rate, state treasury, unexpected trouble",
    9:  "Religion, judiciary, foreign affairs, higher education",
    10: "Government, ruling party, prime minister/president",
    11: "Parliament, legislature, gains, alliances",
    12: "Expenditure, foreign enemies, hospitals, secret activities",
}


@dataclass
class MundaneChartAnalysis:
    chart_type: str            # "nation"|"solar_ingress"|"lunar_year"|"swearing_in"
    event_description: str
    date: date
    location: str
    key_themes: list[str]      # top 3 activated houses by strength
    challenges: list[str]      # dusthana emphasis
    compressed_dasha: str | None
    house_significations: dict[int, str]


def analyze_mundane_chart(chart, chart_type: str = "nation",
                           event_description: str = "",
                           event_date: date | None = None,
                           location: str = "National capital") -> MundaneChartAnalysis:
    """
    Analyze a mundane chart (nation, ingress, swearing-in).
    Uses standard D1 scoring; interprets via mundane house significations.
    """
    if event_date is None:
        event_date = date.today()

    try:
        from src.calculations.multi_axis_scoring import score_axis
        ax = score_axis(chart, chart.lagna_sign_index, "D1", "parashari")
        scores = ax.scores
    except Exception:
        scores = {h: 0.0 for h in range(1, 13)}

    # Top themes (strong houses)
    sorted_houses = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    key_themes = [
        f"H{h}: {_MUNDANE_HOUSES[h]} (strong)"
        for h, s in sorted_houses[:3] if s > 0.5
    ]

    # Challenges (weak houses)
    challenges = [
        f"H{h}: {_MUNDANE_HOUSES[h]} (under pressure)"
        for h, s in sorted_houses[-3:] if s < -1.0
    ]

    return MundaneChartAnalysis(
        chart_type=chart_type,
        event_description=event_description or f"{chart_type} chart",
        date=event_date, location=location,
        key_themes=key_themes, challenges=challenges,
        compressed_dasha=None,
        house_significations=_MUNDANE_HOUSES,
    )


def compress_vimshottari(chart, birth_date: date,
                          period_years: float = 1.0) -> list[dict]:
    """
    Compress Vimshottari dasha to a shorter period (PVRNR p464).
    Useful for mundane charts: compress 120yr cycle to 1yr/1month.
    period_years: 1.0 = annual mundane chart, 1/12 = monthly.
    """
    try:
        from src.calculations.vimshottari_dasa import compute_vimshottari_dasa
        dashas = compute_vimshottari_dasa(chart, birth_date)
        factor = period_years / 120.0
        compressed = []
        for d in dashas[:9]:
            compressed_days = d.years * 365.25 * factor
            compressed.append({
                "planet": d.lord,
                "years_compressed": round(d.years * factor, 3),
                "days_compressed": round(compressed_days, 1),
                "original_years": d.years,
            })
        return compressed
    except Exception:
        return []
