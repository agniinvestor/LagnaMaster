"""
src/calculations/narrative.py — Session 39

Plain-English narrative report generator (OUTPUT_NarrativeReport).
Produces per-house domain interpretation from 7-layer LPI scores.

Public API
----------
  generate_narrative(lpi_result, chart, dashas, on_date) -> NarrativeReport
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional

_HOUSE_THEME = {
    1:"Self · identity · body · vitality · personality",
    2:"Wealth · family · speech · values · accumulated resources",
    3:"Courage · siblings · communication · skills · short journeys",
    4:"Home · mother · happiness · property · emotional security",
    5:"Intellect · creativity · children · speculation · past merit",
    6:"Health · debt · enemies · service · daily work · competition",
    7:"Marriage · business partners · legal matters · public dealings",
    8:"Longevity · transformation · inheritance · hidden matters · research",
    9:"Fortune · dharma · father · higher learning · guru · long journeys",
    10:"Career · status · authority · public role · government",
    11:"Gains · income · aspirations · elder siblings · social network",
    12:"Liberation · foreign lands · expenses · isolation · spiritual life",
}

_RAG_LABEL = {"Green":"positive","Amber":"mixed","Red":"challenged","Mixed":"mixed"}


@dataclass
class HouseNarrative:
    house: int
    domain: str
    theme: str
    full_index: float
    rag: str
    confidence: str
    active_dasha: str
    text: str


@dataclass
class NarrativeReport:
    on_date: date
    lagna_sign: str
    houses: dict[int, HouseNarrative]
    domain_summaries: dict[str, str]
    overall_summary: str


def generate_narrative(lpi_result, chart, dashas=None, on_date=None) -> NarrativeReport:
    if on_date is None: on_date = date.today()

    try:
        from src.calculations.vimshottari_dasa import current_dasha
        md, ad = current_dasha(dashas or [], on_date)
        dasha_str = f"{md.lord} MD / {ad.lord} AD"
    except Exception:
        dasha_str = "Dasha unavailable"

    _DOMAIN_HOUSE = {1:"Dharma",5:"Dharma",9:"Dharma",
                     2:"Artha",6:"Artha",10:"Artha",
                     3:"Kama",7:"Kama",11:"Kama",
                     4:"Moksha",8:"Moksha",12:"Moksha"}

    houses = {}
    for h, hlpi in lpi_result.houses.items():
        fi = hlpi.full_index
        rag = hlpi.rag
        conf = hlpi.confidence
        theme = _HOUSE_THEME.get(h, "")

        if fi >= 3.0:
            quality = "strong — life area shows genuine promise"
        elif fi >= 0.5:
            quality = "mixed with positive lean — challenges exist but support present"
        elif fi >= -0.5:
            quality = "balanced — neither strongly supported nor afflicted"
        elif fi >= -3.0:
            quality = "under pressure — more affliction than support; requires attention"
        else:
            quality = "significantly challenged across multiple axes"

        conf_str = {"High":"High-confidence signal — inter-axis agreement is strong",
                    "Med": "Medium confidence — some axis divergence present",
                    "Low": "Low confidence — significant divergence; nuanced reading needed",
                   }.get(conf, "")

        text = (f"H{h} {hlpi.domain} ({_RAG_LABEL.get(rag,'mixed')}): {quality}. "
                f"{conf_str}. Active dasha: {dasha_str}. "
                f"Full Index: {fi:+.2f}. Theme: {theme}.")

        houses[h] = HouseNarrative(
            house=h, domain=hlpi.domain, theme=theme,
            full_index=fi, rag=rag, confidence=conf,
            active_dasha=dasha_str, text=text,
        )

    domain_summaries = {}
    for dom, dom_avg in lpi_result.domain_balance.items():
        if dom_avg >= 1.0:   qual = "generally supported"
        elif dom_avg >= -1.0: qual = "mixed"
        else:                 qual = "under collective pressure"
        domain_summaries[dom] = f"{dom} axis ({qual}, avg {dom_avg:+.2f})"

    overall = lpi_result.overall_index
    if overall >= 2.0:   ov_text = "Chart shows overall positive momentum currently."
    elif overall >= 0.0: ov_text = "Chart is in a mixed period — pockets of strength and challenge."
    else:                ov_text = "Chart is under collective pressure — key life areas need attention."

    return NarrativeReport(
        on_date=on_date,
        lagna_sign=chart.lagna_sign,
        houses=houses,
        domain_summaries=domain_summaries,
        overall_summary=ov_text,
    )
