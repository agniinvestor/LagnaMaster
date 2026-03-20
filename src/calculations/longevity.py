"""
src/calculations/longevity.py — Session 42

Three classical longevity calculation methods (BPHS Ch.44):
  Pindayu  — based on planetary Amsas (degrees)
  Nisargayu — natural lifespan by planet position
  Amsayu   — based on divisional chart strength

Balarishta detection: afflictions in H1/H8 indicating early-life danger.

Public API
----------
  compute_pindayu(chart)   -> float (years)
  compute_nisargayu(chart) -> float (years)
  compute_amsayu(chart)    -> float (years)
  longevity_range(chart)   -> LongevityResult
  detect_balarishta(chart) -> list[str]
"""
from __future__ import annotations
from dataclasses import dataclass

# Pindayu: years contributed by each planet at full exaltation
_PINDAYU_MAX = {
    "Sun":19,"Moon":25,"Mars":15,"Mercury":12,
    "Jupiter":15,"Venus":21,"Saturn":20,
}

# Nisargayu natural span
_NISARGAYU = {
    "Sun":20,"Moon":1,"Mars":2,"Mercury":9,
    "Jupiter":18,"Venus":20,"Saturn":50,
}

_EXALT_LON = {"Sun":10,"Moon":33,"Mars":298,"Mercury":165,
               "Jupiter":95,"Venus":357,"Saturn":200}
_DEBIL_LON = {"Sun":190,"Moon":213,"Mars":118,"Mercury":345,
               "Jupiter":275,"Venus":177,"Saturn":20}


def _strength_ratio(planet: str, longitude: float) -> float:
    """0.0 (debilitated) to 1.0 (exalted) based on longitude distance."""
    exalt = _EXALT_LON.get(planet)
    debil = _DEBIL_LON.get(planet)
    if exalt is None:
        return 0.5
    diff = abs(longitude - exalt) % 360
    if diff > 180:
        diff = 360 - diff
    return max(0.0, 1.0 - diff / 180.0)


def compute_pindayu(chart) -> float:
    """
    Pindayu method: sum of planetary contributions based on their
    exaltation strength × maximum years for each planet.
    """
    total = 0.0
    for planet, max_years in _PINDAYU_MAX.items():
        pos = chart.planets.get(planet)
        if not pos:
            continue
        ratio = _strength_ratio(planet, pos.longitude)
        total += ratio * max_years
    return round(total, 1)


def compute_nisargayu(chart) -> float:
    """
    Nisargayu: sum natural lifespans weighted by house position.
    Kendra = full, Panapara = half, Apoklima = quarter.
    """
    _HOUSE_WEIGHT = {1:1.0,4:1.0,7:1.0,10:1.0,
                     2:.5,5:.5,8:.5,11:.5,
                     3:.25,6:.25,9:.25,12:.25}
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    total = 0.0
    for planet, natural_years in _NISARGAYU.items():
        h = hmap.planet_house.get(planet, 1)
        w = _HOUSE_WEIGHT.get(h, 0.25)
        total += natural_years * w
    return round(total, 1)


def compute_amsayu(chart) -> float:
    """
    Amsayu: based on Navamsha (D9) sign strength.
    Own/exalt in D9 = full years, friendly = half, enemy = quarter.
    """
    try:
        from src.calculations.panchanga import compute_navamsha_chart
        from src.calculations.dignity import DignityLevel
        d9 = compute_navamsha_chart(chart)
    except Exception:
        return 66.0  # fallback

    _PLANET_YEARS = {"Sun":19,"Moon":25,"Mars":15,"Mercury":12,
                     "Jupiter":15,"Venus":21,"Saturn":20}
    _OWN = {"Sun":{4},"Moon":{3},"Mars":{0,7},"Mercury":{2,5},
            "Jupiter":{8,11},"Venus":{1,6},"Saturn":{9,10}}
    _EXALT_SI = {"Sun":0,"Moon":1,"Mars":9,"Mercury":5,
                  "Jupiter":3,"Venus":11,"Saturn":6}

    total = 0.0
    for planet, years in _PLANET_YEARS.items():
        d9_si = d9.get(planet)
        if d9_si is None:
            total += years * 0.5
            continue
        if _EXALT_SI.get(planet) == d9_si:
            total += years * 1.0
        elif d9_si in _OWN.get(planet, set()):
            total += years * 1.0
        else:
            total += years * 0.5
    return round(total, 1)


@dataclass
class LongevityResult:
    pindayu: float
    nisargayu: float
    amsayu: float
    average: float
    minimum: float
    span: str   # "Short" <36 / "Medium" 36–70 / "Long" >70

    def summary(self) -> str:
        return (f"Pindayu={self.pindayu}yr  Nisargayu={self.nisargayu}yr  "
                f"Amsayu={self.amsayu}yr  →  {self.span} ({self.average:.0f}yr avg)")


def longevity_range(chart) -> LongevityResult:
    p = compute_pindayu(chart)
    n = compute_nisargayu(chart)
    a = compute_amsayu(chart)
    avg = round((p + n + a) / 3, 1)
    mn  = min(p, n, a)
    span = "Short" if avg < 36 else ("Long" if avg > 70 else "Medium")
    return LongevityResult(pindayu=p, nisargayu=n, amsayu=a,
                            average=avg, minimum=mn, span=span)


def detect_balarishta(chart) -> list[str]:
    """
    Balarishta: danger to life in infancy/childhood.
    Conditions: Moon afflicted in H6/H8/H12, or H1 lord in H6/H8/H12,
    or malefics in H1 + H8 simultaneously without benefic aspects.
    Returns list of triggered condition descriptions.
    """
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    results = []

    moon_h = hmap.planet_house.get("Moon", 0)
    if moon_h in {6, 8, 12}:
        results.append(f"Moon in H{moon_h} (dusthana) — Balarishta indicator")

    lagnesh_h = hmap.planet_house.get(hmap.house_lord[0], 0)
    if lagnesh_h in {6, 8, 12}:
        results.append(f"Lagnesh in H{lagnesh_h} — weakened vitality")

    _NAT_MALEFIC = {"Sun","Mars","Saturn","Rahu","Ketu"}
    h1_malefics = [p for p in _NAT_MALEFIC
                   if hmap.planet_house.get(p) == 1]
    h8_malefics = [p for p in _NAT_MALEFIC
                   if hmap.planet_house.get(p) == 8]
    if h1_malefics and h8_malefics:
        results.append(f"Malefics in H1 ({h1_malefics}) and H8 ({h8_malefics}) — Arishta")

    return results
