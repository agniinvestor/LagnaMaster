"""
src/calculations/scoring_v3.py — Session 40

Scoring Engine v3: wires together all Phase 5 components.
  - Multi-axis scoring (D1, CL, SL, D9, D10)
  - Rule interaction engine (30 pairs)
  - Avastha v2 modifiers (baaladi + sayanadi)
  - Full 7-layer LPI
  - ENGINE_VERSION = "3.0.0"

Public API
----------
  score_chart_v3(chart, dashas, on_date, school) -> ChartScoresV3
  ENGINE_VERSION: str
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from src.calculations.scoring_patches import (
    get_aspect_strength, display_score, check_kemadruma, detect_raj_yogas
)


ENGINE_VERSION = "3.0.0"

@dataclass
class ChartScoresV3:
    lagna_sign: str
    engine_version: str = ENGINE_VERSION
    d1_scores:  dict[int, float] = field(default_factory=dict)
    cl_scores:  dict[int, float] = field(default_factory=dict)
    sl_scores:  dict[int, float] = field(default_factory=dict)
    d9_scores:  dict[int, float] = field(default_factory=dict)
    d10_scores: dict[int, float] = field(default_factory=dict)
    lpi: object = None           # LPIResult
    vimshopaka: object = None    # VimshopakaBala
    avasthas: object = None      # AvasthaReportV2
    raja_yogas: list = field(default_factory=list)
    viparita_yogas: list = field(default_factory=list)
    neecha_bhanga: list = field(default_factory=list)
    rasi_drishti: object = None
    bhavat_bhavam: dict = field(default_factory=dict)
    arudha_padas: object = None
    karakamsha: object = None

    def summary(self) -> str:
        lines = [f"LagnaMaster v3 — {self.lagna_sign} Lagna (engine {self.engine_version})"]
        if self.lpi:
            lines.append(f"Overall LPI: {self.lpi.overall_index:+.2f}")
            for dom, avg in self.lpi.domain_balance.items():
                lines.append(f"  {dom}: {avg:+.2f}")
        return "\n".join(lines)


def score_chart_v3(
    chart,
    dashas: list = None,
    on_date: Optional[date] = None,
    school: str = "parashari",
) -> ChartScoresV3:
    if on_date is None: on_date = date.today()
    if dashas is None:  dashas = []

    from src.calculations.multi_axis_scoring import score_all_axes
    from src.calculations.lpi import compute_lpi
    from src.calculations.divisional_charts import compute_vimshopaka
    from src.calculations.avastha_v2 import compute_avasthas_v2
    from src.calculations.extended_yogas import (
        detect_raja_dhana_yogas, detect_viparita_yogas,
        detect_neecha_bhanga, compute_rasi_drishti, compute_bhavat_bhavam
    )
    from src.calculations.multi_lagna import (
        compute_all_arudha_padas, compute_karakamsha
    )

    axes = score_all_axes(chart, school)
    lpi  = compute_lpi(chart, dashas, on_date, school)
    vim  = compute_vimshopaka(chart)
    avs  = compute_avasthas_v2(chart)
    raja = detect_raja_dhana_yogas(chart, dashas, on_date)
    vip  = detect_viparita_yogas(chart, dashas, on_date)
    nb   = detect_neecha_bhanga(chart, dashas, on_date)
    rd   = compute_rasi_drishti(chart)
    bb   = compute_bhavat_bhavam(chart)
    ap   = compute_all_arudha_padas(chart)

    try:
        kk = compute_karakamsha(chart)
    except Exception:
        kk = None

    return ChartScoresV3(
        lagna_sign=chart.lagna_sign,
        engine_version=ENGINE_VERSION,
        d1_scores=axes.d1.scores,
        cl_scores=axes.cl.scores,
        sl_scores=axes.sl.scores,
        d9_scores=axes.d9.scores,
        d10_scores=axes.d10.scores,
        lpi=lpi, vimshopaka=vim, avasthas=avs,
        raja_yogas=raja, viparita_yogas=vip, neecha_bhanga=nb,
        rasi_drishti=rd, bhavat_bhavam=bb,
        arudha_padas=ap, karakamsha=kk,
    )


# Functional dignity S137
FUNCTIONAL_DIGNITY_NOTE = "use compute_functional_classifications(lagna_si) for R02/R09"


# S162: Functional benefic/malefic by Lagna — replaces natural classification
# Source: V.K. Choudhry Systems Approach Ch.3; PVRNR BPHS Ch.34
def _is_functional_benefic(planet: str, lagna_sign_index: int) -> bool:
    """Returns True if planet is functionally benefic for this Lagna."""
    try:
        from src.calculations.functional_dignity import compute_functional_classifications
        fc = compute_functional_classifications(lagna_sign_index)
        r = fc.get(planet)
        return r.is_functional_benefic if r else False
    except Exception:
        # Fallback to natural classification
        return planet in {"Jupiter", "Venus", "Mercury", "Moon"}

def _is_functional_malefic(planet: str, lagna_sign_index: int) -> bool:
    """Returns True if planet is functionally malefic for this Lagna."""
    try:
        from src.calculations.functional_dignity import compute_functional_classifications
        fc = compute_functional_classifications(lagna_sign_index)
        r = fc.get(planet)
        return r.is_functional_malefic if r else False
    except Exception:
        return planet in {"Saturn", "Mars", "Sun", "Rahu", "Ketu"}


# S163: Dasha-sensitized scoring — call after compute_house_scores()
# Usage: dasha_report = apply_dasha_scoring(raw_scores, chart, query_date)
#        sensitized = {h: dasha_report.score_for_house(h) for h in range(1,13)}
def score_chart_with_dasha(chart, query_date=None):
    """Run house scoring with optional dasha sensitization."""
    raw_scores = {h: float(h - 6) for h in range(1, 13)}  # placeholder
    if query_date is None:
        return raw_scores
    try:
        from src.calculations.dasha_scoring import apply_dasha_scoring
        report = apply_dasha_scoring(raw_scores, chart, query_date)
        return {h: report.score_for_house(h) for h in range(1, 13)}
    except Exception:
        return raw_scores
