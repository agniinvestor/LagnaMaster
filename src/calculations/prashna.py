"""
src/calculations/prashna.py — Session 93

Prashna (Horary) Jyotish: answer questions from the chart of the query moment.
Used when birth data is uncertain or for specific present questions.

Key inputs: time and place of query → compute ephemeris chart at that moment.
Key factors: Prashna lagna, Hora lord, Moon's nakshatra + house, AK planet.

Query types: general, lost_article, illness, travel, legal, marriage, career

BPHS Prashna chapters; Prashna Marga (classical text).
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

_PRASHNA_QUERY_HOUSES = {
    "general":       1,
    "lost_article":  4,   # 4th = stored things; 2nd = movable possessions
    "illness":       6,   # 6th = disease; 8th = chronic
    "travel":        3,   # 3rd = short; 12th = foreign
    "legal":         7,   # 7th = opponents
    "marriage":      7,
    "career":        10,
    "wealth":        2,
    "children":      5,
    "property":      4,
}

_HORA_LORDS = ["Sun","Venus","Mercury","Moon","Saturn","Jupiter","Mars"]


@dataclass
class PrashnaAnalysis:
    query_type: str
    hora_lord: str
    hora_quality: str        # "Auspicious"/"Neutral"/"Inauspicious"
    moon_nakshatra: str
    moon_house: int
    key_house: int
    key_house_lord: str
    key_house_score: float
    lagna_strong: bool
    verdict: str             # "Yes — likely"/"Possible"/"Unlikely"/"No"
    confidence: str          # "High"/"Moderate"/"Low"
    reasoning: list[str]


# Hora quality by planet and query type
_HORA_QUALITY = {
    "Sun":     {"general":"Auspicious","career":"Auspicious","legal":"Auspicious"},
    "Moon":    {"general":"Auspicious","marriage":"Auspicious","travel":"Auspicious"},
    "Mars":    {"general":"Inauspicious","illness":"Neutral","legal":"Auspicious"},
    "Mercury": {"general":"Auspicious","career":"Auspicious","wealth":"Auspicious"},
    "Jupiter": {"general":"Auspicious","marriage":"Auspicious","children":"Auspicious"},
    "Venus":   {"general":"Auspicious","marriage":"Auspicious","wealth":"Auspicious"},
    "Saturn":  {"general":"Inauspicious","career":"Neutral","legal":"Neutral"},
}


def analyze_prashna(chart, query_type: str = "general",
                     query_dt: datetime | None = None) -> PrashnaAnalysis:
    """
    Analyze a Prashna chart for the specified query type.
    chart: ephemeris chart computed for the query moment.
    """
    if query_dt is None:
        query_dt = datetime.now()

    from src.calculations.panchanga import compute_hora, _NAKSHATRA_NAMES
    from src.calculations.house_lord import compute_house_map

    # Hora
    hora_lord, hora_num = compute_hora(query_dt)
    hora_q_map = _HORA_QUALITY.get(hora_lord, {})
    hora_quality = hora_q_map.get(query_type, hora_q_map.get("general", "Neutral"))

    # Moon's nakshatra in prashna chart
    moon_pos = chart.planets.get("Moon")
    moon_nak = int(moon_pos.longitude * 27 / 360) % 27 if moon_pos else 0
    moon_nak_name = _NAKSHATRA_NAMES[moon_nak]

    hmap = compute_house_map(chart)
    moon_house = hmap.planet_house.get("Moon", 1)
    key_house = _PRASHNA_QUERY_HOUSES.get(query_type, 1)
    key_house_lord = hmap.house_lord[key_house - 1]

    # Score key house from prashna chart
    try:
        from src.calculations.multi_axis_scoring import score_axis
        ax = score_axis(chart, chart.lagna_sign_index, "D1", "parashari")
        key_score = ax.scores.get(key_house, 0.0)
    except Exception:
        key_score = 0.0

    # Lagna strength
    lagna_lord = hmap.house_lord[0]
    lagna_lord_h = hmap.planet_house.get(lagna_lord, 0)
    lagna_strong = lagna_lord_h in {1,4,5,7,9,10}

    # Verdict logic
    reasoning = []
    positive_signals = 0

    if hora_quality == "Auspicious":
        positive_signals += 2
        reasoning.append(f"{hora_lord} hora is auspicious for {query_type}")

    if key_score > 1.5:
        positive_signals += 2
        reasoning.append(f"H{key_house} ({query_type} house) is strong")
    elif key_score > 0.5:
        positive_signals += 1
        reasoning.append(f"H{key_house} shows moderate support")
    elif key_score < -1.0:
        positive_signals -= 2
        reasoning.append(f"H{key_house} is afflicted — challenge indicated")

    if lagna_strong:
        positive_signals += 1
        reasoning.append("Prashna lagna lord is well-placed")

    if moon_house in {1,4,5,7,9,10,11}:
        positive_signals += 1
        reasoning.append(f"Moon in H{moon_house} supports the query")

    if not reasoning:
        reasoning.append(f"Moon in {moon_nak_name} nakshatra — general indicator for {query_type} query")

    if positive_signals >= 4:
        verdict, conf = "Yes — strongly indicated", "High"
    elif positive_signals >= 2:
        verdict, conf = "Possibly — moderate indication", "Moderate"
    elif positive_signals >= 0:
        verdict, conf = "Uncertain — mixed signals", "Low"
    else:
        verdict, conf = "Unlikely — unfavorable indicators", "Moderate"

    return PrashnaAnalysis(
        query_type=query_type, hora_lord=hora_lord, hora_quality=hora_quality,
        moon_nakshatra=moon_nak_name, moon_house=moon_house,
        key_house=key_house, key_house_lord=key_house_lord,
        key_house_score=round(key_score, 3), lagna_strong=lagna_strong,
        verdict=verdict, confidence=conf, reasoning=reasoning,
    )
