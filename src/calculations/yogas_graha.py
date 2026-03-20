"""
src/calculations/yogas_graha.py — Session 53

Graha yogas from YOGA_Graha sheet not yet in extended_yogas.py:
  Saraswati    — Jupiter + Venus + Mercury all in kendra/trikona
  Chandra-Mangal — Moon + Mars conjunct in same sign
  Kahala       — H4 lord and H9 lord in mutual kendra
  Parvata      — H1 and H2 lords both in kendra or trikona

Also adds:
  Budhaditya   — Sun + Mercury in same sign (already in YOGA_Graha)
  Gaja Kesari  — already in yogas.py, verified here

All with dasha weighting (dormant = 0.5×, active = 1.0×).

Public API
----------
  detect_graha_yogas(chart, dashas, on_date) -> list[GrahaYogaResult]
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date

_NAT_BENEFIC = {"Jupiter","Venus","Mercury","Moon"}
_KENDRA    = {1,4,7,10}
_TRIKONA   = {1,5,9}
_STRONG    = _KENDRA | _TRIKONA


@dataclass
class GrahaYogaResult:
    name: str
    planets: list[str]
    present: bool
    score: float
    weighted_score: float
    description: str
    source: str
    dasha_weight: float


def _dasha_weight(planets: list[str], dashas, on_date: date) -> float:
    try:
        from src.calculations.vimshottari_dasa import current_dasha
        md, ad = current_dasha(dashas, on_date)
        if any(p in {md.lord, ad.lord} for p in planets):
            return 1.0
    except Exception:
        pass
    return 0.5


def detect_graha_yogas(chart, dashas=None, on_date: date | None = None
                        ) -> list[GrahaYogaResult]:
    if on_date is None:
        on_date = date.today()

    from src.calculations.house_lord import compute_house_map
    hmap = compute_house_map(chart)
    ph   = hmap.planet_house
    results = []

    def yoga(name, planets, present, score, desc, source):
        dw = _dasha_weight(planets, dashas, on_date) if dashas else 0.5
        results.append(GrahaYogaResult(
            name=name, planets=planets, present=present,
            score=score, weighted_score=round(score*dw, 2),
            description=desc, source=source, dasha_weight=dw,
        ))

    # ── Budhaditya — Sun + Mercury conjunct ────────────────────────────────────
    budha = chart.planets.get("Mercury")
    sun   = chart.planets.get("Sun")
    budhaditya = bool(budha and sun and budha.sign_index == sun.sign_index)
    yoga("Budhaditya Yoga", ["Sun","Mercury"], budhaditya,
         2.0 if budhaditya else 0.0,
         "Sun and Mercury in same sign — sharp intellect, communication skill",
         "BPHS Ch.68; Jataka Parijata Ch.2")

    # ── Saraswati — Jupiter, Venus, Mercury all in kendra/trikona ─────────────
    jup_strong = ph.get("Jupiter",0) in _STRONG
    ven_strong = ph.get("Venus",0) in _STRONG
    mer_strong = ph.get("Mercury",0) in _STRONG
    saraswati = jup_strong and ven_strong and mer_strong
    yoga("Saraswati Yoga", ["Jupiter","Venus","Mercury"], saraswati,
         3.0 if saraswati else 0.0,
         "Jupiter, Venus, Mercury all in kendra/trikona — exceptional learning and eloquence",
         "Uttara Kalamrita Ch.5 v.43")

    # ── Chandra-Mangal — Moon + Mars in same sign ──────────────────────────────
    moon_si = chart.planets["Moon"].sign_index if "Moon" in chart.planets else -1
    mars_si = chart.planets["Mars"].sign_index if "Mars" in chart.planets else -2
    chandra_mangal = moon_si == mars_si
    yoga("Chandra-Mangal Yoga", ["Moon","Mars"], chandra_mangal,
         2.0 if chandra_mangal else 0.0,
         "Moon and Mars conjunct — courage, entrepreneurial wealth, trade",
         "BPHS Ch.68; Saravali Ch.8")

    # ── Kahala — H4 lord and H9 lord in mutual kendra ─────────────────────────
    lord4  = hmap.house_lord[3]
    lord9  = hmap.house_lord[8]
    h4l_h  = ph.get(lord4, 0)
    h9l_h  = ph.get(lord9, 0)
    # Mutual kendra: each sees the other in kendra from itself
    diff49 = abs(h4l_h - h9l_h) % 12
    kahala = diff49 in {0, 3, 6, 9} and h4l_h > 0 and h9l_h > 0
    yoga("Kahala Yoga", [lord4, lord9], kahala,
         2.0 if kahala else 0.0,
         f"H4 lord ({lord4}) and H9 lord ({lord9}) in mutual kendra — bold, courageous, commanding",
         "BPHS Ch.37; Phaladeepika Ch.6")

    # ── Parvata — H1 and H2 lords both in kendra or trikona ──────────────────
    lord1  = hmap.house_lord[0]
    lord2  = hmap.house_lord[1]
    l1_strong = ph.get(lord1, 0) in _STRONG
    l2_strong = ph.get(lord2, 0) in _STRONG
    parvata = l1_strong and l2_strong
    yoga("Parvata Yoga", [lord1, lord2], parvata,
         2.5 if parvata else 0.0,
         f"H1 lord ({lord1}) and H2 lord ({lord2}) both in kendra/trikona — wealthy, famous, learned",
         "BPHS Ch.36")

    # ── Gaja Kesari — Jupiter in kendra from Moon ──────────────────────────────
    moon_h = ph.get("Moon", 0)
    jup_h  = ph.get("Jupiter", 0)
    gk_diff = abs(moon_h - jup_h) % 12
    gaja_kesari = gk_diff in {0,3,6,9} and moon_h > 0 and jup_h > 0
    yoga("Gaja Kesari Yoga", ["Jupiter","Moon"], gaja_kesari,
         3.0 if gaja_kesari else 0.0,
         "Jupiter in kendra from Moon — exceptional intelligence, fame, authority",
         "BPHS Ch.43; Phaladeepika Ch.6")

    return results
