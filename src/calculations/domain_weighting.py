"""
src/calculations/domain_weighting.py — Session 66

Domain-specific axis weighting (PVRNR Ch.13 p181).

PVRNR explicit (p181): "Use the correct divisional chart for the matter of interest."
Examples from the text:
  D-16: happiness from vehicle
  D-30: criminal psychology
  D-9: marriage (as dharma/soul union)
  D-10: career (actual conduct in society)
  Chandra Lagna: emotional/relational axis dominates for psychological matters

LPI default weights (D1×35%, Chandra×15%, Surya×10%, D9×15%, D10×10%, Dasha×10%, Gochar×5%)
are replaced with domain-specific weights when querying a specific life domain.

Public API
----------
  get_domain_weights(domain) -> dict[str, float]
  compute_domain_lpi(chart, dashas, on_date, domain) -> DomainLPIResult
  DOMAINS: list of supported domain names
"""

from __future__ import annotations
from dataclasses import dataclass

# Domain → custom LPI axis weights
# Keys match the axes in LPI: D1, Chandra, Surya, D9, D10, Dasha, Gochar
_DOMAIN_WEIGHTS = {
    "career": {
        "D1": 0.20,
        "Chandra": 0.05,
        "Surya": 0.10,
        "D9": 0.10,
        "D10": 0.35,
        "Dasha": 0.15,
        "Gochar": 0.05,
        "primary_house": 10,
        "rationale": "D10 dominates career. PVRNR: '10th from AL in D-10 shows perceptions about career.'",
    },
    "marriage": {
        "D1": 0.20,
        "Chandra": 0.10,
        "Surya": 0.05,
        "D9": 0.35,
        "D10": 0.05,
        "Dasha": 0.15,
        "Gochar": 0.10,
        "primary_house": 7,
        "rationale": "D9 dominates dharmic unions. PVRNR: 'D-9 is the best chart for marriage.'",
    },
    "mind_psychology": {
        "D1": 0.20,
        "Chandra": 0.40,
        "Surya": 0.10,
        "D9": 0.10,
        "D10": 0.05,
        "Dasha": 0.10,
        "Gochar": 0.05,
        "primary_house": 4,
        "rationale": "Chandra Lagna dominates emotional/psychological matters.",
    },
    "wealth": {
        "D1": 0.35,
        "Chandra": 0.10,
        "Surya": 0.10,
        "D9": 0.10,
        "D10": 0.10,
        "Dasha": 0.15,
        "Gochar": 0.10,
        "primary_house": 2,
        "rationale": "D1 H2 and H11 primary for wealth accumulation.",
    },
    "health_longevity": {
        "D1": 0.45,
        "Chandra": 0.15,
        "Surya": 0.10,
        "D9": 0.10,
        "D10": 0.05,
        "Dasha": 0.10,
        "Gochar": 0.05,
        "primary_house": 8,
        "rationale": "D1 dominates physical vitality. H1/H8 are the life axis.",
    },
    "spirituality": {
        "D1": 0.15,
        "Chandra": 0.10,
        "Surya": 0.05,
        "D9": 0.45,
        "D10": 0.05,
        "Dasha": 0.15,
        "Gochar": 0.05,
        "primary_house": 9,
        "rationale": "D9 = dharma/soul chart. PVRNR: 'D-20 for religious activities.'",
    },
    "children": {
        "D1": 0.25,
        "Chandra": 0.10,
        "Surya": 0.10,
        "D9": 0.20,
        "D10": 0.05,
        "Dasha": 0.20,
        "Gochar": 0.10,
        "primary_house": 5,
        "rationale": "D7 (saptamsha) ideal but not in LPI axes. D9 secondary.",
    },
    "default": {
        "D1": 0.35,
        "Chandra": 0.15,
        "Surya": 0.10,
        "D9": 0.15,
        "D10": 0.10,
        "Dasha": 0.10,
        "Gochar": 0.05,
        "primary_house": None,
        "rationale": "Default LPI weights (balanced multi-domain).",
    },
}

DOMAINS = [k for k in _DOMAIN_WEIGHTS if k != "default"]


def get_domain_weights(domain: str) -> dict:
    """Return LPI weights for a specific life domain."""
    return _DOMAIN_WEIGHTS.get(domain.lower(), _DOMAIN_WEIGHTS["default"])


@dataclass
class DomainLPIResult:
    domain: str
    primary_house: int | None
    weights_used: dict
    house_scores: dict[int, float]  # weighted composite per house
    top_houses: list[int]  # top 3 strongest for this domain
    weak_houses: list[int]  # bottom 3 weakest for this domain
    domain_score: float  # overall domain score
    rationale: str


def compute_domain_lpi(
    chart, dashas=None, on_date=None, domain: str = "default"
) -> DomainLPIResult:
    """Compute LPI with domain-specific axis weights."""
    from datetime import date as _date

    if on_date is None:
        on_date = _date.today()

    weights = get_domain_weights(domain)
    primary_house = weights.get("primary_house")

    try:
        from src.calculations.multi_axis_scoring import score_all_axes

        axes = score_all_axes(chart, "parashari")
        d1 = axes.d1.scores if axes.d1 else {}
        cl = axes.cl.scores if axes.cl else {}
        sl = axes.sl.scores if axes.sl else {}
        d9 = axes.d9.scores if axes.d9 else {}
        d10 = axes.d10.scores if axes.d10 else {}
    except Exception:
        d1 = cl = sl = d9 = d10 = {}

    # Dasha modifier
    dasha_boost = {h: 0.0 for h in range(1, 13)}
    if dashas:
        try:
            from src.calculations.vimshottari_dasa import current_dasha
            from src.calculations.house_lord import compute_house_map

            md, _ = current_dasha(dashas, on_date)
            md_h = compute_house_map(chart).planet_house.get(md.lord, 0)
            if md_h:
                dasha_boost[md_h] = d1.get(md_h, 0) * 0.15
        except Exception:
            pass

    house_scores = {}
    for h in range(1, 13):
        score = (
            d1.get(h, 0) * weights["D1"]
            + cl.get(h, 0) * weights["Chandra"]
            + sl.get(h, 0) * weights["Surya"]
            + d9.get(h, 0) * weights["D9"]
            + d10.get(h, 0) * weights["D10"]
            + dasha_boost[h]
        )
        house_scores[h] = round(score, 3)

    sorted_h = sorted(house_scores, key=house_scores.get, reverse=True)
    top = sorted_h[:3]
    weak = sorted_h[-3:]

    primary_score = house_scores.get(primary_house, 0) if primary_house else 0
    domain_score = round(
        0.4 * primary_score + 0.6 * (sum(house_scores.values()) / 12), 3
    )

    return DomainLPIResult(
        domain=domain,
        primary_house=primary_house,
        weights_used={
            k: v for k, v in weights.items() if k not in ("primary_house", "rationale")
        },
        house_scores=house_scores,
        top_houses=top,
        weak_houses=weak,
        domain_score=domain_score,
        rationale=weights.get("rationale", ""),
    )
