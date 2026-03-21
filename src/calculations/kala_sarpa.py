"""
src/calculations/kala_sarpa.py — Session 105

Kala Sarpa Yoga — modern practitioner convention.

IMPORTANT: This yoga does NOT appear in classical texts (BPHS, Parashara).
It became popular in 20th century practice. It is included here because
virtually every practitioner uses it, labeled clearly as "modern convention."

Definition: All 7 planets (Sun through Saturn) fall between Rahu and Ketu
           in one hemisphere of the chart (counting zodiacally from Rahu to Ketu).

12 types based on which sign Rahu occupies:
  1. Ananta (Rahu in Ar)    2. Kulika (Rahu in Ta)   3. Vasuki (Rahu in Ge)
  4. Shankha (Rahu in Cn)   5. Padma (Rahu in Le)    6. Mahapadma (Rahu in Vi)
  7. Takshaka (Rahu in Li)  8. Karkotaka (Rahu in Sc) 9. Shankhanaad (Rahu in Sg)
  10. Patak (Rahu in Cp)    11. Vishakta (Rahu in Aq) 12. Sheshnaag (Rahu in Pi)

Partial Kala Sarpa: 5-6 planets between Rahu-Ketu (one planet outside).

Note: BPHS does not validate this yoga. Empirical evidence is mixed.
This is included as a "practitioner-expected" feature with appropriate disclaimers.
"""
from __future__ import annotations
from dataclasses import dataclass

_SIGN_NAMES = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
               "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]

_KS_NAMES = [
    "Ananta","Kulika","Vasuki","Shankha","Padma","Mahapadma",
    "Takshaka","Karkotaka","Shankhanaad","Patak","Vishakta","Sheshnaag"
]

_PLANETS_7 = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]


@dataclass
class KalaSarpaResult:
    present: bool
    partial: bool
    yoga_name: str | None
    rahu_sign: str
    ketu_sign: str
    planets_inside: list[str]
    planets_outside: list[str]
    is_reverse: bool     # planets between Ketu and Rahu (Kala Amrita)
    classical_disclaimer: str
    interpretation: str


def compute_kala_sarpa(chart) -> KalaSarpaResult:
    """Detect Kala Sarpa Yoga."""
    rahu_pos = chart.planets.get("Rahu")
    ketu_pos = chart.planets.get("Ketu")

    disclaimer = ("Kala Sarpa Yoga is a modern practitioner convention, "
                  "not found in classical texts (BPHS, Parashara). "
                  "Empirical validation is limited.")

    if not rahu_pos or not ketu_pos:
        return KalaSarpaResult(
            present=False, partial=False, yoga_name=None,
            rahu_sign=_SIGN_NAMES[0], ketu_sign=_SIGN_NAMES[6],
            planets_inside=[], planets_outside=[],
            is_reverse=False, classical_disclaimer=disclaimer,
            interpretation="Cannot detect — Rahu/Ketu positions unavailable",
        )

    rahu_lon = rahu_pos.longitude % 360
    ketu_lon = ketu_pos.longitude % 360

    # Count planets between Rahu and Ketu (going forward in zodiac from Rahu)
    inside = []
    outside = []
    for planet in _PLANETS_7:
        pos = chart.planets.get(planet)
        if not pos:
            continue
        lon = pos.longitude % 360
        # Is this planet between Rahu and Ketu going forward?
        if rahu_lon < ketu_lon:
            in_forward = rahu_lon <= lon <= ketu_lon
        else:
            in_forward = lon >= rahu_lon or lon <= ketu_lon
        if in_forward:
            inside.append(planet)
        else:
            outside.append(planet)

    # Check reverse (Kala Amrita — planets between Ketu and Rahu)
    is_ks = len(outside) == 0 and len(inside) == 7
    is_ka = len(inside) == 0 and len(outside) == 7  # Kala Amrita (reverse)
    partial = (len(inside) >= 5 and len(outside) <= 2) or \
              (len(outside) >= 5 and len(inside) <= 2)
    is_reverse = is_ka

    present = is_ks or is_ka
    yoga_name = _KS_NAMES[rahu_pos.sign_index % 12] if present else None

    if present:
        interp = (f"{'Kala Amrita (reverse) Yoga' if is_reverse else 'Kala Sarpa Yoga'} — "
                  f"{yoga_name}. All planets {'outside' if is_reverse else 'inside'} "
                  f"Rahu-Ketu axis. Note: modern convention, not classical śāstra.")
    elif partial:
        count = max(len(inside), len(outside))
        interp = (f"Partial Kala Sarpa — {count} of 7 planets inside the axis. "
                  "Mild influence by convention. Not classical.")
    else:
        interp = "Kala Sarpa Yoga not present — planets distributed across both hemispheres."

    return KalaSarpaResult(
        present=present, partial=partial, yoga_name=yoga_name,
        rahu_sign=_SIGN_NAMES[rahu_pos.sign_index % 12],
        ketu_sign=_SIGN_NAMES[ketu_pos.sign_index % 12],
        planets_inside=inside, planets_outside=outside,
        is_reverse=is_reverse, classical_disclaimer=disclaimer,
        interpretation=interp,
    )
