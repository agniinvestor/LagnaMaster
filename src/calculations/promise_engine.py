"""
src/calculations/promise_engine.py — Session 65

Promise vs Manifestation distinction (PVRNR implicit throughout).

PVRNR: "If the promise is absent, the dasha cannot produce the result."
(Applied in chart reading examples: first check natal promise, then timing.)

Three levels:
  Promise  — natal chart indicators (is the potential there?)
  Capacity — dasha activation (is the timing favorable?)
  Delivery — transit support + AV rekhas (is now the right moment?)

Public API
----------
  compute_house_promise(chart, house) -> PromiseLevel
  compute_full_promise(chart, dashas, on_date) -> dict[int, ManifestationResult]
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_KENDRA   = {1, 4, 7, 10}
_TRIKONA  = {1, 5, 9}
_DUSTHANA = {6, 8, 12}


@dataclass
class PromiseLevel:
    house: int
    natal_score: float
    promise_present: bool       # score > 0.5 = some positive promise
    promise_strength: str       # "Strong"/"Moderate"/"Weak"/"Absent"/"Negated"
    key_factors: list[str]
    ceiling: float              # maximum deliverable outcome (0–10 scale)


@dataclass
class ManifestationResult:
    house: int
    promise: PromiseLevel
    dasha_activated: bool
    transit_supported: bool
    manifestation_probability: float  # 0.0–1.0
    manifestation_timing: str         # "Now"/"Soon"/"Future"/"Blocked"
    explanation: str


def compute_house_promise(chart, house: int) -> PromiseLevel:
    """Compute natal promise for a house."""
    from src.calculations.multi_axis_scoring import score_axis
    try:
        ax = score_axis(chart, chart.lagna_sign_index, "D1", "parashari")
        score = ax.scores.get(house, 0.0)
    except Exception:
        score = 0.0

    key_factors = []
    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph = hmap.planet_house
    lord = hmap.house_lord[house - 1]
    lord_house = ph.get(lord, 0)

    if lord_house in _KENDRA | _TRIKONA:
        key_factors.append(f"{lord} (lord) in strong house H{lord_house}")
    if lord_house in _DUSTHANA:
        key_factors.append(f"{lord} (lord) in dusthana H{lord_house}")

    # Benefics/malefics in the house
    in_house = [p for p, h in ph.items() if h == house]
    bens = [p for p in in_house if p in {"Jupiter","Venus","Mercury","Moon"}]
    mals = [p for p in in_house if p in {"Sun","Mars","Saturn","Rahu","Ketu"}]
    if bens: key_factors.append(f"Benefics in house: {bens}")
    if mals: key_factors.append(f"Malefics in house: {mals}")

    if score >= 3.0:
        strength, present, ceiling = "Strong", True, 9.0
    elif score >= 1.5:
        strength, present, ceiling = "Moderate", True, 7.0
    elif score >= 0.5:
        strength, present, ceiling = "Weak", True, 5.0
    elif score >= -0.5:
        strength, present, ceiling = "Absent", False, 3.0
    else:
        strength, present, ceiling = "Negated", False, 1.0

    return PromiseLevel(
        house=house, natal_score=round(score, 3),
        promise_present=present, promise_strength=strength,
        key_factors=key_factors, ceiling=ceiling,
    )


def compute_full_promise(chart, dashas=None,
                          on_date: date | None = None) -> dict[int, ManifestationResult]:
    if on_date is None:
        on_date = date.today()

    results = {}
    active_md_lord = None
    active_ad_lord = None

    if dashas:
        try:
            from src.calculations.vimshottari_dasa import current_dasha
            md, ad = current_dasha(dashas, on_date)
            active_md_lord = md.lord
            active_ad_lord = ad.lord
        except Exception:
            pass

    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    for h in range(1, 13):
        promise = compute_house_promise(chart, h)
        lord = hmap.house_lord[h - 1]
        ph.get(lord, 0)

        # Dasha activation
        dasha_activated = (active_md_lord in {lord, *[p for p,hp in ph.items() if hp==h]} or
                           active_ad_lord in {lord, *[p for p,hp in ph.items() if hp==h]})

        # Transit support (simple: use current date SAV)
        transit_supported = False
        try:
            from src.calculations.av_transit import compute_transit_av_score
            tav = compute_transit_av_score(chart, on_date)
            transit_supported = h in tav.strong_natal_houses or tav.house_sav.get(h,0) >= 28
        except Exception:
            pass

        # Manifestation probability
        if not promise.promise_present:
            prob = 0.05 if dasha_activated else 0.02
            timing = "Blocked"
            expl = f"H{h}: No natal promise (score {promise.natal_score:+.2f}) — dasha cannot create what's absent"
        elif dasha_activated and transit_supported:
            prob = 0.80 if promise.promise_strength == "Strong" else 0.60
            timing = "Now"
            expl = f"H{h}: Promise present + dasha activated + transit support — high manifestation probability"
        elif dasha_activated:
            prob = 0.55 if promise.promise_strength in {"Strong","Moderate"} else 0.35
            timing = "Soon"
            expl = f"H{h}: Promise present + dasha active — manifestation likely, transit support would confirm"
        elif promise.promise_present:
            prob = 0.20
            timing = "Future"
            expl = f"H{h}: Promise exists but awaiting dasha activation"
        else:
            prob = 0.05
            timing = "Blocked"
            expl = f"H{h}: No promise, no activation"

        results[h] = ManifestationResult(
            house=h, promise=promise,
            dasha_activated=dasha_activated,
            transit_supported=transit_supported,
            manifestation_probability=round(prob, 3),
            manifestation_timing=timing,
            explanation=expl,
        )

    return results
