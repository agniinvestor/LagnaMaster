"""
src/guidance/practitioner_handoff.py — Session 89

When confidence model flags "requires expert review", offers referral
to verified Jyotish practitioners (opt-in directory).

LagnaMaster is the tool. The practitioner is the expert.
User can share a sanitised chart summary (no raw scores) with the practitioner.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class ChartSummary:
    """Sanitised chart summary for sharing with a practitioner — no raw scores."""

    lagna: str
    moon_sign: str
    sun_sign: str
    active_dasha: str
    active_antardasha: str
    notable_features: list[str]  # plain-language, no scores
    confidence_notes: list[str]  # from confidence_model
    practitioner_note: str


def should_recommend_practitioner(
    requires_expert_review: bool,
    critical_exceptions: int,
    confidence_uncertain_houses: int,
) -> bool:
    """Determine if practitioner referral is warranted."""
    return (
        requires_expert_review
        or critical_exceptions > 0
        or confidence_uncertain_houses >= 4
    )


def build_chart_summary(
    chart, dashas=None, on_date=None, confidence_report=None
) -> ChartSummary:
    """Build practitioner-safe chart summary — no raw scores."""
    from datetime import date as _date

    if on_date is None:
        on_date = _date.today()

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

    lagna = _SIGNS[chart.lagna_sign_index % 12]
    moon_si = chart.planets.get("Moon")
    sun_si = chart.planets.get("Sun")
    moon_sign = _SIGNS[moon_si.sign_index % 12] if moon_si else "Unknown"
    sun_sign = _SIGNS[sun_si.sign_index % 12] if sun_si else "Unknown"

    active_md = "Unknown"
    active_ad = "Unknown"
    if dashas:
        try:
            from src.calculations.vimshottari_dasa import current_dasha

            md, ad = current_dasha(dashas, on_date)
            active_md = md.lord
            active_ad = ad.lord
        except Exception:
            pass

    # Notable features (plain language)
    notable = []
    try:
        from src.calculations.planet_chains import compute_stelliums

        for st in compute_stelliums(chart):
            if len(st.planets) >= 3:
                notable.append(
                    f"{len(st.planets)}-planet {st.nature.lower()} stellium "
                    f"in {st.sign_name} (House {st.house})"
                )
    except Exception:
        pass

    try:
        from src.calculations.planet_chains import compute_mutual_receptions

        for mr in compute_mutual_receptions(chart):
            notable.append(f"Mutual reception: {mr.planet1}–{mr.planet2}")
    except Exception:
        pass

    # Confidence notes
    conf_notes = []
    if confidence_report:
        uncertain = [
            h
            for h, hc in confidence_report.houses.items()
            if hc.confidence_label == "Uncertain"
        ]
        if uncertain:
            conf_notes.append(f"Uncertain signals in houses: {uncertain}")
        if confidence_report.requires_expert_review:
            conf_notes.append("Engine flags this chart for practitioner review.")

    return ChartSummary(
        lagna=lagna,
        moon_sign=moon_sign,
        sun_sign=sun_sign,
        active_dasha=active_md,
        active_antardasha=active_ad,
        notable_features=notable,
        confidence_notes=conf_notes,
        practitioner_note=(
            "This summary was prepared by LagnaMaster for review by a Jyotish practitioner. "
            "No predictive claims are made. The practitioner's judgment supersedes "
            "any automated interpretation."
        ),
    )
