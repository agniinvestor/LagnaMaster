"""
src/calculations/upagrahas_derived.py
Derived upagrahas (sub-planets) from Sun's longitude.
Session 146.

Sources:
  Mantreswara · Phaladeepika Ch.26 v.1-6 (Mandi, derived upagrahas)
  PVRNR · BPHS Ch.25 (Upagraha Sphuta)
  Hora Makaranda (Dhuma and companions)
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DerivedUpagrahas:
    dhuma: float  # Sun + 133°20' = 133.333°
    vyatipata: float  # 360° - Dhuma
    parivesha: float  # Vyatipata + 180°
    indrachapa: float  # 360° - Parivesha
    upaketu: float  # Dhuma + 30°

    @property
    def summary(self) -> dict[str, float]:
        return {
            "Dhuma": round(self.dhuma, 4),
            "Vyatipata": round(self.vyatipata, 4),
            "Parivesha": round(self.parivesha, 4),
            "Indrachapa": round(self.indrachapa, 4),
            "Upaketu": round(self.upaketu, 4),
        }

    @property
    def sign_positions(self) -> dict[str, int]:
        return {name: int(lon / 30) % 12 for name, lon in self.summary.items()}


def compute_derived_upagrahas(sun_longitude: float) -> DerivedUpagrahas:
    """
    Compute 5 derived upagrahas from Sun's sidereal longitude.
    All are pure arithmetic — no additional API calls needed.

    Source: PVRNR · BPHS Ch.25; Hora Makaranda; Phaladeepika Ch.26 v.1-6
    """
    dhuma = (sun_longitude + 133.333) % 360
    vyatipata = (360 - dhuma) % 360
    parivesha = (vyatipata + 180) % 360
    indrachapa = (360 - parivesha) % 360
    upaketu = (dhuma + 30) % 360

    return DerivedUpagrahas(
        dhuma=dhuma,
        vyatipata=vyatipata,
        parivesha=parivesha,
        indrachapa=indrachapa,
        upaketu=upaketu,
    )


def compute_all_upagrahas(chart) -> dict[str, float]:
    """
    Compute all upagrahas (Mandi, Gulika + 5 derived) for a chart.
    Returns dict {name: longitude}.
    """
    result = {}

    # Derived from Sun
    if "Sun" in chart.planets:
        derived = compute_derived_upagrahas(chart.planets["Sun"].longitude)
        result.update(derived.summary)

    # Mandi and Gulika from planetary_state.py (already built)
    upagrahas = getattr(chart, "upagrahas", {})
    if upagrahas:
        result.update({k.title(): v for k, v in upagrahas.items()})

    return result


# Interpretive notes for each upagraha
UPAGRAHA_NOTES: dict[str, str] = {
    "Dhuma": "Smoke — obscuration, chronic disease, prolonged suffering; afflicts house it occupies",
    "Vyatipata": "Fall — extremely inauspicious; activities in its shadow fail",
    "Parivesha": "Halo — moderate affliction; some protection despite negative environment",
    "Indrachapa": "Rainbow — mildly auspicious; temporary pleasures",
    "Upaketu": "Ketu-like — separations, losses, spiritual orientation in its house",
    "Mandi": "Son of Saturn — most malefic upagraha; afflicts H8 matters, death, chronic ill-health",
    "Gulika": "Precedes Mandi — similar malefic quality; poison, negativity",
}
