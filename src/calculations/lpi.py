"""
src/calculations/lpi.py — Session 36

Full 7-layer Life Pressure Index (OUTPUT_LifePressureIndex_Full formula).

Layer weights (configurable, defaults from workbook):
  D1  Natal          35%
  CL  Chandra Lagna  15%
  SL  Surya Lagna    10%
  D9  Navamsha       15%
  D10 Dashamsha      10%
  Dasha activation   10%
  Gochar transit      5%

Per-house output:
  full_index   = weighted sum of all 7 layers
  confidence   = "High"/"Med"/"Low" based on inter-axis agreement
  rag          = "Green"/"Amber"/"Red"/"Mixed"
  domain_balance = Dharma/Artha/Kama/Moksha averages
  dasha_modifier = ×1.15 for active MD/AD lord's natal house

Public API
----------
  compute_lpi(chart, dashas, on_date, school) -> LPIResult
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

_LAYER_WEIGHTS = {
    "D1":   0.35,
    "CL":   0.15,
    "SL":   0.10,
    "D9":   0.15,
    "D10":  0.10,
    "dasha":0.10,
    "gochar":0.05,
}

_DOMAINS = {
    "Dharma": [1,5,9],
    "Artha":  [2,6,10],
    "Kama":   [3,7,11],
    "Moksha": [4,8,12],
}

@dataclass
class HouseLPI:
    house: int
    domain: str
    d1: float; cl: float; sl: float; d9: float; d10: float
    dasha_act: float; gochar: float
    full_index: float
    rag: str
    confidence: str
    interpretation: str
    dasha_modifier: float = 1.0
    arudha_note: str = ""

@dataclass
class LPIResult:
    on_date: date
    school: str
    houses: dict[int, HouseLPI]
    domain_balance: dict[str, float]
    strongest_house: int
    weakest_house: int
    overall_index: float
    layer_weights: dict = field(default_factory=lambda: dict(_LAYER_WEIGHTS))


def _rag(score: float) -> str:
    if score >= 3.0:  return "Green"
    if score >= 0.0:  return "Amber"
    if score >= -3.0: return "Amber"
    return "Red"

def _confidence(scores: list[float]) -> str:
    if not scores: return "Low"
    rng = max(scores) - min(scores)
    if rng < 2.0:  return "High"
    if rng < 5.0:  return "Med"
    return "Low"

def _dasha_activation(chart, dashas, on_date: date, house: int) -> float:
    """CALC_DashaModifier logic: active MD/AD lord's natal house gets boosted."""
    try:
        from src.calculations.vimshottari_dasa import current_dasha
        from src.calculations.house_lord import compute_house_map
        md, ad = current_dasha(dashas, on_date)
        hmap = compute_house_map(chart)
        md_house = hmap.planet_house.get(md.lord, 0)
        ad_house = hmap.planet_house.get(ad.lord, 0)
        act = 0.0
        if md_house == house: act += 0.5
        if ad_house == house: act += 0.25
        return act
    except Exception:
        return 0.0

def _dasha_modifier(chart, dashas, on_date: date, house: int) -> float:
    """×1.15 if active MD lord's natal house = this house."""
    try:
        from src.calculations.vimshottari_dasa import current_dasha
        from src.calculations.house_lord import compute_house_map
        md, _ = current_dasha(dashas, on_date)
        hmap = compute_house_map(chart)
        if hmap.planet_house.get(md.lord) == house:
            return 1.15
    except Exception:
        pass
    return 1.0

def _gochar_pressure(chart, on_date: date, house: int) -> float:
    """Simple transit activation: malefic in house → negative, benefic → positive."""
    try:
        from src.calculations.gochara import compute_gochara
        g = compute_gochara(chart, on_date)
        score = 0.0
        malefics = {"Saturn","Mars","Rahu","Ketu"}
        benefics = {"Jupiter","Venus","Mercury"}
        for p, tp in g.planets.items():
            if tp.natal_house == house:
                if p in malefics: score -= 0.5
                if p in benefics: score += 0.5
        if g.sade_sati and house == chart.planets["Moon"].sign_index % 12 + 1:
            score -= {"Peak":0.75,"Rising":0.4,"Setting":0.25}.get(g.sade_sati_phase, 0)
        return max(-2.0, min(2.0, score))
    except Exception:
        return 0.0


def compute_lpi(
    chart,
    dashas: list,
    on_date: Optional[date] = None,
    school: str = "parashari",
) -> LPIResult:
    if on_date is None:
        on_date = date.today()

    from src.calculations.multi_axis_scoring import score_all_axes
    from src.calculations.multi_lagna import compute_all_arudha_padas

    axes = score_all_axes(chart, school)
    arudha = compute_all_arudha_padas(chart)

    _HOUSE_DOMAIN = {}
    for dom, houses in _DOMAINS.items():
        for h in houses:
            _HOUSE_DOMAIN[h] = dom

    _DOMAIN_THEMES = {
        1:"Self & Vitality",2:"Wealth & Family",3:"Courage & Skills",
        4:"Home & Happiness",5:"Intellect & Children",6:"Challenges & Health",
        7:"Partnerships",8:"Transformation",9:"Fortune & Dharma",
        10:"Career & Status",11:"Gains & Network",12:"Liberation & Loss",
    }

    houses: dict[int, HouseLPI] = {}
    for h in range(1, 13):
        d1  = axes.d1.scores[h]
        cl  = axes.cl.scores[h]
        sl  = axes.sl.scores[h]
        d9  = axes.d9.scores[h]
        d10 = axes.d10.scores[h]
        da  = _dasha_activation(chart, dashas, on_date, h)
        gc  = _gochar_pressure(chart, on_date, h)
        dm  = _dasha_modifier(chart, dashas, on_date, h)

        fi = (d1  * _LAYER_WEIGHTS["D1"]    +
              cl  * _LAYER_WEIGHTS["CL"]    +
              sl  * _LAYER_WEIGHTS["SL"]    +
              d9  * _LAYER_WEIGHTS["D9"]    +
              d10 * _LAYER_WEIGHTS["D10"]   +
              da  * _LAYER_WEIGHTS["dasha"] +
              gc  * _LAYER_WEIGHTS["gochar"])
        fi *= dm
        fi = round(max(-10.0, min(10.0, fi)), 3)

        axis_vals = [d1, cl, sl, d9, d10]
        conf = _confidence(axis_vals)
        rag  = _rag(fi)

        pos_count = sum(1 for v in axis_vals if v > 0)
        neg_count = sum(1 for v in axis_vals if v < 0)
        if pos_count >= 4:   interp = "Positive across most axes"
        elif neg_count >= 4: interp = "Challenged across most axes"
        elif conf == "Low":  interp = "Significant divergence between axes"
        else:                interp = "Mixed signals — nuanced reading needed"

        ap = arudha.padas.get(h)
        arudha_note = f"A{h}({ap.name})={ap.sign}" if ap else ""

        houses[h] = HouseLPI(
            house=h, domain=_HOUSE_DOMAIN[h],
            d1=round(d1,3), cl=round(cl,3), sl=round(sl,3),
            d9=round(d9,3), d10=round(d10,3),
            dasha_act=round(da,3), gochar=round(gc,3),
            full_index=fi, rag=rag, confidence=conf,
            interpretation=interp, dasha_modifier=dm,
            arudha_note=arudha_note,
        )

    domain_balance = {}
    for dom, dom_houses in _DOMAINS.items():
        domain_balance[dom] = round(
            sum(houses[h].full_index for h in dom_houses) / len(dom_houses), 3
        )

    all_fi = {h: houses[h].full_index for h in range(1, 13)}
    strongest = max(all_fi, key=all_fi.get)
    weakest   = min(all_fi, key=all_fi.get)
    overall   = round(sum(all_fi.values()) / 12, 3)

    return LPIResult(
        on_date=on_date, school=school, houses=houses,
        domain_balance=domain_balance,
        strongest_house=strongest, weakest_house=weakest,
        overall_index=overall,
    )
