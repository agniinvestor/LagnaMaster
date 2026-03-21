"""
src/calculations/yoga_fructification.py — Session 58

Yoga fructification conditions (PVRNR p135-137, p148).

PVRNR explicitly states (p147):
  (1) Planets must be free from afflictions by functional malefics
  (2) Conjunction/aspect must be close (within 6°)
  (3) Planets must not be combust, debilitated, in inimical house, or bad avastha

Amsa level classification from Dasa Varga (10 varga count):
  Paarijataamsa   = 2  → Moderate
  Uttamaamsa      = 3  → Good
  Gopuraamsa      = 4  → Notable
  Simhasanamsa    = 5  → Distinguished
  Paaravataamsa   = 6  → Excellent (for divine persons in p148)
  Devalokaamsa    = 7  → Divine
  Brahmalokaamsa  = 8  → Exceptional
  Airaavataamsa   = 9  → Supreme

Public API
----------
  compute_yoga_amsa_level(planets, chart) -> AmsaLevel
  yoga_fructification_score(yoga_planets, chart) -> FructificationResult
  check_yoga_affliction(planet, chart) -> list[str]
"""
from __future__ import annotations
from dataclasses import dataclass

_AMSA_NAMES = {
    0: "No amsa",
    1: "Kaahala",
    2: "Paarijataamsa",
    3: "Uttamaamsa",
    4: "Gopuraamsa",
    5: "Simhasanamsa",
    6: "Paaravataamsa",
    7: "Devalokaamsa",
    8: "Brahmalokaamsa",
    9: "Airaavataamsa",
    10: "Iraavataamsa",
}

# Dasa Varga: D1, D2, D3, D7, D9, D10, D12, D16, D30, D60
_DASA_VARGA_STRONG = {"own", "exaltation", "mooltrikona"}


def compute_amsa_level(planet: str, chart) -> tuple[int, str]:
    """
    Count how many Dasa Varga charts the planet occupies own/exalt/mooltrikona.
    Returns (count, amsa_name).
    """
    try:
        from src.calculations.divisional_charts import compute_divisional_signs
        div = compute_divisional_signs(chart)
    except Exception:
        return (0, "No amsa")

    _EXALT_SI = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
    _OWN = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
            "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}
    _MOOLT = {"Sun":4,"Moon":1,"Mars":0,"Mercury":5,"Jupiter":8,"Venus":6,"Saturn":9}

    # 10 Dasa Varga divisions: D1,D2,D3,D7,D9,D10,D12,D16,D30,D60
    dasa_vargas = ["D1","D2","D3","D7","D9","D10","D12","D16","D30","D60"]
    count = 0
    # DivisionalMap uses attribute access: div.D1, div.D9 etc.
    for dv in dasa_vargas:
        try:
            varga_map = getattr(div, dv, None)
            if varga_map is None:
                continue
            # varga_map is a dict {planet: sign_index}
            if isinstance(varga_map, dict):
                si = varga_map.get(planet)
            elif hasattr(varga_map, planet):
                si = getattr(varga_map, planet)
            else:
                si = None
        except Exception:
            si = None
        if si is None and dv == "D1":
            pos = chart.planets.get(planet)
            si = pos.sign_index if pos else None
        if si is not None:
            if si in _OWN.get(planet, set()):
                count += 1
            elif _EXALT_SI.get(planet) == si:
                count += 1
            elif _MOOLT.get(planet) == si:
                count += 1

    amsa_name = _AMSA_NAMES.get(count, f"{count} vargas")
    return (count, amsa_name)


@dataclass
class FructificationResult:
    planets: list[str]
    base_present: bool
    affliction_free: bool      # condition 1
    close_conjunction: bool    # condition 2: within 6°
    dignity_adequate: bool     # condition 3: not combust/debil/inimical
    amsa_count: int
    amsa_name: str
    fructification_score: float   # 0.0–1.0
    weaknesses: list[str]
    verdict: str   # "Full"/"Partial"/"Weak"/"Minimal"


def yoga_fructification_score(yoga_planets: list[str], chart) -> FructificationResult:
    """
    Evaluate whether a yoga will actually deliver its full results.
    PVRNR p147: three explicit conditions.
    """
    weaknesses = []

    # Condition 1: Free from functional malefic afflictions
    affliction_free = True
    from src.calculations.functional_roles import compute_functional_roles
    from src.calculations.house_lord import compute_house_map
    try:
        fr = compute_functional_roles(chart)
        compute_house_map(chart)
        func_malefics = fr.functional_malefics | fr.dusthana_lords

        for p in yoga_planets:
            pos = chart.planets.get(p)
            if not pos:
                continue
            afflictors = [a for a in func_malefics
                          if a != p and chart.planets.get(a) and
                          chart.planets[a].sign_index == pos.sign_index]
            if afflictors:
                affliction_free = False
                weaknesses.append(f"{p} afflicted by functional malefic(s): {afflictors}")
    except Exception:
        pass

    # Condition 2: Close conjunction (within 6°)
    from src.calculations.orb_strength import yoga_conjunction_strength, _circular_diff
    conj_strength = yoga_conjunction_strength(yoga_planets, chart)
    close_conjunction = conj_strength >= 0.5  # within 6° threshold

    pairs_orbs = []
    for i in range(len(yoga_planets)):
        for j in range(i+1, len(yoga_planets)):
            p1 = yoga_planets[i]; p2 = yoga_planets[j]
            pos1 = chart.planets.get(p1); pos2 = chart.planets.get(p2)
            if pos1 and pos2 and pos1.sign_index == pos2.sign_index:
                orb = _circular_diff(pos1.longitude, pos2.longitude)
                pairs_orbs.append((p1, p2, orb))
                if orb > 6.0:
                    weaknesses.append(f"{p1}–{p2} orb {orb:.1f}° > 6° (PVRNR threshold)")

    # Condition 3: Not combust, debilitated, or inimical
    dignity_adequate = True
    _EXALT_SI = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,"Jupiter":3,"Venus":11,"Saturn":6}
    _DEBIL_SI = {"Sun":6,"Moon":7,"Mars":3,"Mercury":11,"Jupiter":9,"Venus":5,"Saturn":0}
    _OWN = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
            "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}

    try:
        from src.calculations.dignity import compute_all_dignities
        dignities = compute_all_dignities(chart)
    except Exception:
        dignities = {}

    for p in yoga_planets:
        pos = chart.planets.get(p)
        if not pos:
            continue
        dig = dignities.get(p)
        if dig and dig.is_combust:
            dignity_adequate = False
            weaknesses.append(f"{p} is combust — yoga power reduced")
        si = pos.sign_index
        if _DEBIL_SI.get(p) == si:
            dignity_adequate = False
            weaknesses.append(f"{p} is debilitated — yoga power reduced")

    # Amsa level: minimum across yoga planets
    amsa_counts = [compute_amsa_level(p, chart)[0] for p in yoga_planets]
    amsa_count = min(amsa_counts) if amsa_counts else 0
    amsa_name = _AMSA_NAMES.get(amsa_count, f"{amsa_count}")

    if amsa_count < 2:
        weaknesses.append(f"Amsa level low ({amsa_name}) — ordinary results at most")

    # Compute overall fructification score
    score = 1.0
    if not affliction_free:   score *= 0.60
    if not close_conjunction: score *= (0.50 + 0.50 * conj_strength)
    if not dignity_adequate:  score *= 0.65
    # Amsa bonus/penalty
    amsa_modifier = min(1.5, 0.7 + amsa_count * 0.1)
    score = min(1.0, score * amsa_modifier)
    score = round(score, 3)

    if score >= 0.75: verdict = "Full"
    elif score >= 0.50: verdict = "Partial"
    elif score >= 0.25: verdict = "Weak"
    else: verdict = "Minimal"

    return FructificationResult(
        planets=yoga_planets, base_present=True,
        affliction_free=affliction_free,
        close_conjunction=close_conjunction,
        dignity_adequate=dignity_adequate,
        amsa_count=amsa_count, amsa_name=amsa_name,
        fructification_score=score,
        weaknesses=weaknesses, verdict=verdict,
    )


def check_yoga_affliction(planet: str, chart) -> list[str]:
    """Return list of afflictions on a planet (functional malefics, combust, debil)."""
    issues = []
    try:
        from src.calculations.functional_roles import compute_functional_roles
        fr = compute_functional_roles(chart)
        pos = chart.planets.get(planet)
        if not pos:
            return issues
        afflictors = [a for a in fr.functional_malefics
                      if a != planet and chart.planets.get(a) and
                      chart.planets[a].sign_index == pos.sign_index]
        if afflictors:
            issues.append(f"Conjunct functional malefic(s): {afflictors}")
        from src.calculations.dignity import compute_all_dignities
        dig = compute_all_dignities(chart).get(planet)
        if dig and dig.is_combust:
            issues.append("Combust")
        _DEBIL = {"Sun":6,"Moon":7,"Mars":3,"Mercury":11,"Jupiter":9,"Venus":5,"Saturn":0}
        if _DEBIL.get(planet) == pos.sign_index:
            issues.append("Debilitated")
    except Exception:
        pass
    return issues
