"""
src/calculations/pitr_dosha.py — Session 107

Pitr Dosha (Pitru/Ancestral debt) — modern practitioner convention.

IMPORTANT: Classical texts do not define "Pitr Dosha" as a distinct yoga.
The concept derives from interpretations of the 9th house (father/dharma),
Sun (father/ancestors), Rahu, and the 5th house. It is included here
because practitioners widely reference it. Labeled accordingly.

Modern practitioner criteria (consensus, not classical):
  1. Sun in 9th house with malefic influence
  2. 9th lord afflicted by Rahu/Ketu
  3. Sun conjunct Rahu in any house
  4. 5th lord afflicted + 9th lord weak
  5. Saturn in 9th with Rahu aspect

Severity: Strong / Moderate / Mild / Not present
"""

from __future__ import annotations
from dataclasses import dataclass

_NAT_MALEF = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
_DISCLAIMER = (
    "Pitr Dosha is a modern practitioner convention, not defined "
    "in classical texts (BPHS, Parashara). Included as a practitioner-"
    "expected feature. Classical basis: 9th house/Sun affliction analysis."
)


@dataclass
class PitrDoshaResult:
    present: bool
    severity: str  # "Strong"/"Moderate"/"Mild"/"Not present"
    triggers: list[str]  # which criteria triggered
    classical_disclaimer: str
    suggested_consideration: str  # (not a remedy prescription)


def compute_pitr_dosha(chart) -> PitrDoshaResult:
    """Detect Pitr Dosha by modern practitioner criteria."""
    from src.calculations.house_lord import compute_house_map

    hmap = compute_house_map(chart)
    ph = hmap.planet_house

    triggers = []

    # Criterion 1: Sun in 9th house
    sun_h = ph.get("Sun", 0)
    if sun_h == 9:
        malefics_with_sun = [p for p in _NAT_MALEF if p != "Sun" and ph.get(p) == 9]
        if malefics_with_sun:
            triggers.append(f"Sun in H9 with malefics {malefics_with_sun}")

    # Criterion 2: 9th lord afflicted by Rahu/Ketu
    lord9 = hmap.house_lord[8]
    lord9_h = ph.get(lord9, 0)
    rahu_h = ph.get("Rahu", 0)
    ketu_h = ph.get("Ketu", 0)
    if lord9_h in {rahu_h, ketu_h} or rahu_h == lord9_h:
        triggers.append(f"9th lord {lord9} conjunct Rahu/Ketu")

    # Criterion 3: Sun conjunct Rahu
    if sun_h == rahu_h and sun_h > 0:
        triggers.append("Sun conjunct Rahu — grahan yoga on ancestral significator")

    # Criterion 4: 5th lord weak + 9th lord in dusthana
    lord5 = hmap.house_lord[4]
    lord5_h = ph.get(lord5, 0)
    if lord9_h in {6, 8, 12} and lord5_h in {6, 8, 12}:
        triggers.append(f"Both 5th lord ({lord5}) and 9th lord ({lord9}) in dusthana")

    # Criterion 5: Saturn in 9th
    saturn_h = ph.get("Saturn", 0)
    if saturn_h == 9 and rahu_h in {3, 6, 9, 12}:
        triggers.append("Saturn in H9 with Rahu in dusthana/kendra — ancestral burden")

    n = len(triggers)
    if n >= 3:
        severity = "Strong"
    elif n == 2:
        severity = "Moderate"
    elif n == 1:
        severity = "Mild"
    else:
        severity = "Not present"
    present = n >= 1

    consideration = ""
    if present:
        consideration = (
            "Consider ancestral memorial practices (Pitru Tarpana/Shraddha) "
            "as a general dharmic act — irrespective of chart. "
            "Consult a practitioner for specific guidance."
        )

    return PitrDoshaResult(
        present=present,
        severity=severity,
        triggers=triggers,
        classical_disclaimer=_DISCLAIMER,
        suggested_consideration=consideration,
    )
