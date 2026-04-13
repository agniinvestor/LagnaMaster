"""
src/calculations/yogas.py
==========================
Detection of major Jyotish yogas (planetary combinations).

Categories:
  - Pancha Mahapurusha  (5 great-person yogas — one per planet)
  - Raj Yoga            (kendra-trikona lord combinations → power/success)
  - Dhana Yoga          (wealth yogas)
  - Lunar Yogas         (Gajakesari, Kemadruma, Chandra-Mangala, Adhi)
  - Solar Yogas         (Budha-Aditya, Vesi/Vasi/Ubhayachari)
  - Negative Yogas      (Shakata, Kemadruma)

Source: BPHS Chapters 36-76; cross-referenced with Excel LEGEND_Yogas sheet.
"""

from __future__ import annotations

from dataclasses import dataclass
from src.ephemeris import BirthChart
from src.calculations.house_lord import compute_house_map, is_kendra
from src.calculations.dignity import EXALT_SIGN as _EXALTATION_SIGN, OWN_SIGNS as _OWN_SIGNS_LIST


# ── Data class ─────────────────────────────────────────────────────────────────


@dataclass
class Yoga:
    name: str
    category: (
        str  # "Pancha Mahapurusha" | "Raj" | "Dhana" | "Lunar" | "Solar" | "Negative"
    )
    nature: str  # "benefic" | "malefic" | "mixed"
    planets: list[str]  # planets forming the yoga
    description: str


# ── Dignity tables ─────────────────────────────────────────────────────────────


_OWN_SIGNS: dict[str, set[int]] = {p: set(s) for p, s in _OWN_SIGNS_LIST.items()}

# Pancha Mahapurusha names
_PM_NAME = {
    "Mars": "Ruchaka",
    "Mercury": "Bhadra",
    "Jupiter": "Hamsa",
    "Venus": "Malavya",
    "Saturn": "Shasha",
}


def _planet_house(pname: str, hmap) -> int:
    return hmap.planet_house[pname]


def _wrap(h: int) -> int:
    return (h - 1) % 12 + 1


# ── Pancha Mahapurusha ────────────────────────────────────────────────────────


def _pancha_mahapurusha(chart: BirthChart, hmap) -> list[Yoga]:
    yogas = []
    for planet, yoga_name in _PM_NAME.items():
        si = chart.planets[planet].sign_index
        ph = _planet_house(planet, hmap)
        in_own_or_exalt = (si in _OWN_SIGNS[planet]) or (
            si == _EXALTATION_SIGN.get(planet)
        )
        if in_own_or_exalt and is_kendra(ph):
            dignity = "exaltation" if si == _EXALTATION_SIGN.get(planet) else "own sign"
            yogas.append(
                Yoga(
                    name=yoga_name,
                    category="Pancha Mahapurusha",
                    nature="benefic",
                    planets=[planet],  # noqa: F841
                    description=(
                        f"{planet} in {dignity} in H{ph} (kendra) → "
                        f"{yoga_name} Yoga: exceptional strength, renowned personality"
                    ),
                )
            )
    return yogas


# ── Raj Yoga ──────────────────────────────────────────────────────────────────


def _raj_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    # Raj Yoga: canonical in scoring_patches.detect_raj_yogas
    # (conjunction + exchange + aspect, with combustion and dusthana cancellation checks)
    return []


# ── Dhana Yogas ────────────────────────────────────────────────────────────────


def _dhana_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    """
    Wealth yogas — lords of H1/2/5/9/11 interacting.
    Classic: H2 lord + H11 lord in same sign; H1+H2 lords conjunct, etc.
    """
    wealth_houses = [1, 2, 5, 9, 11]
    yogas = []
    seen = set()

    lords = {h: hmap.house_lord[h - 1] for h in wealth_houses}

    for i, h1 in enumerate(wealth_houses):
        for h2 in wealth_houses[i + 1 :]:
            l1, l2 = lords[h1], lords[h2]
            if l1 == l2:
                continue
            if chart.planets[l1].sign_index == chart.planets[l2].sign_index:
                pair = tuple(sorted([l1, l2]))
                if pair in seen:
                    continue
                seen.add(pair)
                ph = _planet_house(l1, hmap)
                yogas.append(
                    Yoga(
                        name="Dhana Yoga",
                        category="Dhana",
                        nature="benefic",
                        planets=list(pair),  # noqa: F841
                        description=(
                            f"{l1} (H{h1} lord) + {l2} (H{h2} lord) conjunct in H{ph} "
                            f"→ wealth accumulation, financial prosperity"
                        ),
                    )
                )
    return yogas


# ── Lunar Yogas ────────────────────────────────────────────────────────────────


def _lunar_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    yogas = []
    moon_h = _planet_house("Moon", hmap)

    # Gajakesari, Chandra-Mangala, Adhi Yoga: canonical in yogas_graha.py / yogas_extended.py
    # Kemadruma: canonical in scoring_patches.py (3 conditions + 4 cancellations)

    jup_h = _planet_house("Jupiter", hmap)

    # ── Shakata Yoga (negative): Moon in H6/H8/H12 from Jupiter ──
    dist3 = _wrap(moon_h - jup_h + 1)
    if dist3 in {6, 8, 12}:
        yogas.append(
            Yoga(
                name="Shakata Yoga",
                category="Negative",
                nature="malefic",
                planets=["Moon", "Jupiter"],  # noqa: F841
                description=(
                    f"Moon in H{dist3} from Jupiter → fluctuating fortune, "
                    f"periodic reversal of gains (weakened if Moon is in kendra)"
                ),
            )
        )

    return yogas


# ── Solar Yogas ────────────────────────────────────────────────────────────────


def _solar_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    # Budhaditya: canonical in yogas_graha.py (with combust filter)
    # Vesi/Vasi/Ubhayachari: canonical in yogas_extended.detect_surya_yogas
    return []


# ── Special Yogas ──────────────────────────────────────────────────────────────


def _special_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    yogas = []

    # ── Pancha-Graha Yoga: 5+ planets in one sign ──
    from collections import Counter

    sign_count = Counter(
        p.sign_index
        for pname, p in chart.planets.items()
        if pname not in ("Rahu", "Ketu")
    )
    for si, count in sign_count.items():
        if count >= 5:
            planets_in = [
                pname
                for pname, pos in chart.planets.items()
                if pos.sign_index == si and pname not in ("Rahu", "Ketu")
            ]
            from src.ephemeris import SIGNS

            yogas.append(
                Yoga(
                    name="Pancha-Graha Yoga",
                    category="Special",
                    nature="mixed",
                    planets=planets_in,
                    description=(
                        f"{count} planets in {SIGNS[si]} → extraordinary concentration of energy; "
                        f"intense focus on that house's themes; rare and powerful combination"
                    ),
                )
            )

    # ── Guru-Chandala: Jupiter + Rahu conjunct ──
    if chart.planets["Jupiter"].sign_index == chart.planets["Rahu"].sign_index:
        jup_h = _planet_house("Jupiter", hmap)
        yogas.append(
            Yoga(
                name="Guru-Chandala Yoga",
                category="Negative",
                nature="malefic",
                planets=["Jupiter", "Rahu"],  # noqa: F841
                description=(
                    f"Jupiter + Rahu conjunct in H{jup_h} → "
                    f"unconventional beliefs, challenges with teachers/tradition "
                    f"(can also indicate foreign wisdom if well-placed)"
                ),
            )
        )

    # ── Neecha Bhanga Raj Yoga: debilitated planet with cancellation in kendra ──
    _DEBILITATION: dict[str, int] = {
        "Sun": 6,
        "Moon": 7,
        "Mars": 3,
        "Mercury": 11,
        "Jupiter": 9,
        "Venus": 5,
        "Saturn": 0,
    }
    for planet, debil_si in _DEBILITATION.items():
        if chart.planets[planet].sign_index == debil_si:
            # Check if lord of debilitation sign is in kendra
            from src.calculations.house_lord import sign_lord

            debil_sign_lord = sign_lord(debil_si)
            if debil_sign_lord in hmap.planet_house:
                dl_house = hmap.planet_house[debil_sign_lord]
                if is_kendra(dl_house):
                    yogas.append(
                        Yoga(
                            name="Neecha Bhanga Raj Yoga",
                            category="Raj",
                            nature="benefic",
                            planets=[planet, debil_sign_lord],  # noqa: F841
                            description=(
                                f"{planet} debilitated but {debil_sign_lord} "
                                f"(debilitation lord) in kendra H{dl_house} → "
                                f"cancellation of debilitation, rise after setbacks"
                            ),
                        )
                    )

    return yogas


# ── Public API ────────────────────────────────────────────────────────────────


def detect_yogas(chart: BirthChart) -> list[Yoga]:
    """
    Detect all major Jyotish yogas in the chart.

    Returns list of Yoga objects sorted by category priority:
    Pancha Mahapurusha → Raj → Dhana → Lunar → Solar → Special → Negative
    """
    hmap = compute_house_map(chart)

    all_yogas: list[Yoga] = []
    all_yogas += _pancha_mahapurusha(chart, hmap)
    all_yogas += _raj_yogas(chart, hmap)
    all_yogas += _dhana_yogas(chart, hmap)
    all_yogas += _lunar_yogas(chart, hmap)
    all_yogas += _solar_yogas(chart, hmap)
    all_yogas += _special_yogas(chart, hmap)

    # Sort: benefic before malefic, then by category
    _CATEGORY_ORDER = {
        "Pancha Mahapurusha": 0,
        "Raj": 1,
        "Dhana": 2,
        "Lunar": 3,
        "Solar": 4,
        "Special": 5,
        "Negative": 6,
    }
    _NATURE_ORDER = {"benefic": 0, "mixed": 1, "malefic": 2}
    all_yogas.sort(
        key=lambda y: (
            _CATEGORY_ORDER.get(y.category, 9),
            _NATURE_ORDER.get(y.nature, 9),
        )
    )
    return all_yogas


# NBRY surfacing S145
def get_nbry_yogas(chart):
    try:
        from src.calculations.shadbala_patches import extract_nbry_yogas

        return extract_nbry_yogas(chart)
    except ImportError:
        return []
