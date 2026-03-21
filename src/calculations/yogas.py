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

from dataclasses import dataclass, field
from src.ephemeris import BirthChart
from src.calculations.house_lord import compute_house_map, is_kendra, is_trikona


# ── Data class ─────────────────────────────────────────────────────────────────

@dataclass
class Yoga:
    name:        str
    category:    str          # "Pancha Mahapurusha" | "Raj" | "Dhana" | "Lunar" | "Solar" | "Negative"
    nature:      str          # "benefic" | "malefic" | "mixed"
    planets:     list[str]    # planets forming the yoga
    description: str


# ── Dignity tables ─────────────────────────────────────────────────────────────

# sign_index → planet that is exalted there
_EXALTATION_SIGN: dict[str, int] = {
    "Sun":     0,   # Aries
    "Moon":    1,   # Taurus
    "Mars":    9,   # Capricorn
    "Mercury": 5,   # Virgo
    "Jupiter": 3,   # Cancer
    "Venus":   11,  # Pisces
    "Saturn":  6,   # Libra
}

# Own signs per planet (sign_index)
_OWN_SIGNS: dict[str, set[int]] = {
    "Sun":     {4},        # Leo
    "Moon":    {3},        # Cancer
    "Mars":    {0, 7},     # Aries, Scorpio
    "Mercury": {2, 5},     # Gemini, Virgo
    "Jupiter": {8, 11},    # Sagittarius, Pisces
    "Venus":   {1, 6},     # Taurus, Libra
    "Saturn":  {9, 10},    # Capricorn, Aquarius
}

# Pancha Mahapurusha names
_PM_NAME = {
    "Mars":    "Ruchaka",
    "Mercury": "Bhadra",
    "Jupiter": "Hamsa",
    "Venus":   "Malavya",
    "Saturn":  "Shasha",
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
        in_own_or_exalt = (si in _OWN_SIGNS[planet]) or (si == _EXALTATION_SIGN.get(planet))
        if in_own_or_exalt and is_kendra(ph):
            dignity = "exaltation" if si == _EXALTATION_SIGN.get(planet) else "own sign"
            yogas.append(Yoga(
                name=yoga_name,
                category="Pancha Mahapurusha",
                nature="benefic",
                planets=[planet],  # noqa: F841
                description=(
                    f"{planet} in {dignity} in H{ph} (kendra) → "
                    f"{yoga_name} Yoga: exceptional strength, renowned personality"
                ),
            ))
    return yogas


# ── Raj Yoga ──────────────────────────────────────────────────────────────────

def _raj_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    """
    Kendra lord (H1/4/7/10) + Trikona lord (H1/5/9) in the same sign.
    H1 lord is both kendra and trikona — creates yoga only when paired with
    another pure kendra or pure trikona lord.
    Dusthana lord (H6/8/12) involvement invalidates the yoga.
    """
    kendra_houses  = {1, 4, 7, 10}
    trikona_houses = {1, 5, 9}
    dusthana_lords = {hmap.house_lord[h - 1] for h in (6, 8, 12)}

    yogas = []
    seen  = set()

    for kh in kendra_houses:
        for th in trikona_houses:
            if kh == th:
                continue
            k_lord = hmap.house_lord[kh - 1]
            t_lord = hmap.house_lord[th - 1]
            if k_lord == t_lord:
                continue
            # Skip if either lord also rules a dusthana (weakens yoga)
            if k_lord in dusthana_lords or t_lord in dusthana_lords:
                continue
            # Yoga forms if they conjunct (same sign)
            if chart.planets[k_lord].sign_index == chart.planets[t_lord].sign_index:
                pair = tuple(sorted([k_lord, t_lord]))
                if pair in seen:
                    continue
                seen.add(pair)
                ph = _planet_house(k_lord, hmap)
                yogas.append(Yoga(
                    name="Raj Yoga",
                    category="Raj",
                    nature="benefic",
                    planets=list(pair),  # noqa: F841
                    description=(
                        f"{k_lord} (H{kh} lord) + {t_lord} (H{th} lord) conjunct in H{ph} "
                        f"→ authority, career success, recognition"
                    ),
                ))
    return yogas


# ── Dhana Yogas ────────────────────────────────────────────────────────────────

def _dhana_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    """
    Wealth yogas — lords of H1/2/5/9/11 interacting.
    Classic: H2 lord + H11 lord in same sign; H1+H2 lords conjunct, etc.
    """
    wealth_houses = [1, 2, 5, 9, 11]
    yogas = []
    seen  = set()

    lords = {h: hmap.house_lord[h - 1] for h in wealth_houses}

    for i, h1 in enumerate(wealth_houses):
        for h2 in wealth_houses[i + 1:]:
            l1, l2 = lords[h1], lords[h2]
            if l1 == l2:
                continue
            if chart.planets[l1].sign_index == chart.planets[l2].sign_index:
                pair = tuple(sorted([l1, l2]))
                if pair in seen:
                    continue
                seen.add(pair)
                ph = _planet_house(l1, hmap)
                yogas.append(Yoga(
                    name="Dhana Yoga",
                    category="Dhana",
                    nature="benefic",
                    planets=list(pair),  # noqa: F841
                    description=(
                        f"{l1} (H{h1} lord) + {l2} (H{h2} lord) conjunct in H{ph} "
                        f"→ wealth accumulation, financial prosperity"
                    ),
                ))
    return yogas


# ── Lunar Yogas ────────────────────────────────────────────────────────────────

def _lunar_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    yogas = []
    moon_si = chart.planets["Moon"].sign_index
    moon_h  = _planet_house("Moon", hmap)

    # ── Gajakesari: Jupiter in kendra from Moon ──
    jup_h = _planet_house("Jupiter", hmap)
    dist  = (_wrap(jup_h - moon_h + 1))   # houses from Moon to Jupiter
    if dist in {1, 4, 7, 10}:
        yogas.append(Yoga(
            name="Gajakesari Yoga",
            category="Lunar",
            nature="benefic",
            planets=["Moon", "Jupiter"],
            description=(
                f"Jupiter in H{jup_h} is H{dist} from Moon (H{moon_h}) — "
                f"wisdom, prosperity, fame, generous character"
            ),
        ))

    # ── Chandra-Mangala: Moon-Mars conjunction ──
    mars_si = chart.planets["Mars"].sign_index
    if moon_si == mars_si:
        yogas.append(Yoga(
            name="Chandra-Mangala Yoga",
            category="Lunar",
            nature="mixed",
            planets=["Moon", "Mars"],
            description=(
                f"Moon + Mars conjunct in H{moon_h} → "
                f"drive, wealth through effort, potential emotional volatility"
            ),
        ))

    # ── Adhi Yoga: Jupiter/Venus/Mercury in H6/H7/H8 from Moon ──
    adhi_planets = []
    for planet in ("Jupiter", "Venus", "Mercury"):
        p_h   = _planet_house(planet, hmap)
        dist2 = _wrap(p_h - moon_h + 1)
        if dist2 in {6, 7, 8}:
            adhi_planets.append(planet)
    if len(adhi_planets) >= 2:
        yogas.append(Yoga(
            name="Adhi Yoga",
            category="Lunar",
            nature="benefic",
            planets=adhi_planets,
            description=(
                f"{', '.join(adhi_planets)} in H6/H7/H8 from Moon → "
                f"leadership, comfort, longevity, defeat of enemies"
            ),
        ))

    # ── Kemadruma (negative): Moon has no planet in adjacent sign (H2/H12 from Moon) ──
    prev_si = (moon_si - 1) % 12
    next_si = (moon_si + 1) % 12
    non_luminaries = [p for p in chart.planets if p not in ("Sun", "Moon", "Rahu", "Ketu")]
    adjacent_planets = [
        p for p in non_luminaries
        if chart.planets[p].sign_index in (prev_si, next_si)
    ]
    if not adjacent_planets:
        yogas.append(Yoga(
            name="Kemadruma Yoga",
            category="Negative",
            nature="malefic",
            planets=["Moon"],
            description=(
                f"Moon in H{moon_h} has no planets in adjacent signs — "
                f"isolation, hardship, instability (mitigated if Moon is in kendra or aspects benefics)"
            ),
        ))

    # ── Shakata Yoga (negative): Moon in H6/H8/H12 from Jupiter ──
    dist3 = _wrap(moon_h - jup_h + 1)
    if dist3 in {6, 8, 12}:
        yogas.append(Yoga(
            name="Shakata Yoga",
            category="Negative",
            nature="malefic",
            planets=["Moon", "Jupiter"],  # noqa: F841
            description=(
                f"Moon in H{dist3} from Jupiter → fluctuating fortune, "
                f"periodic reversal of gains (weakened if Moon is in kendra)"
            ),
        ))

    return yogas


# ── Solar Yogas ────────────────────────────────────────────────────────────────

def _solar_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    yogas = []
    sun_si = chart.planets["Sun"].sign_index
    sun_h  = _planet_house("Sun", hmap)

    # ── Budha-Aditya: Sun + Mercury conjunct (not combust within 3°) ──
    merc_si = chart.planets["Mercury"].sign_index
    if sun_si == merc_si:
        # Check if Mercury is close enough to be severely combust (within 3°)
        orb = abs(chart.planets["Sun"].degree_in_sign - chart.planets["Mercury"].degree_in_sign)
        if orb > 3.0:
            yogas.append(Yoga(
                name="Budha-Aditya Yoga",
                category="Solar",
                nature="benefic",
                planets=["Sun", "Mercury"],
                description=(
                    f"Sun + Mercury conjunct in H{sun_h} (orb {orb:.1f}°) → "
                    f"sharp intellect, communication skills, political acumen"
                ),
            ))

    # ── Vesi/Vasi/Ubhayachari ──
    prev_si = (sun_si - 1) % 12
    next_si = (sun_si + 1) % 12
    planets_before = [
        p for p, pos in chart.planets.items()
        if p not in ("Sun", "Moon", "Rahu", "Ketu")
        and pos.sign_index == prev_si
    ]
    planets_after = [
        p for p, pos in chart.planets.items()
        if p not in ("Sun", "Moon", "Rahu", "Ketu")
        and pos.sign_index == next_si
    ]
    if planets_before and planets_after:
        yogas.append(Yoga(
            name="Ubhayachari Yoga",
            category="Solar",
            nature="benefic",
            planets=planets_before + planets_after,
            description=(
                "Planets on both sides of Sun → "
                "royal bearing, balanced and authoritative personality"
            ),
        ))
    elif planets_after:
        yogas.append(Yoga(
            name="Vesi Yoga",
            category="Solar",
            nature="benefic",
            planets=planets_after,
            description=(
                f"{', '.join(planets_after)} in H{_wrap(sun_h+1)} (2nd from Sun) → "
                f"wealthy, virtuous, good memory"
            ),
        ))
    elif planets_before:
        yogas.append(Yoga(
            name="Vasi Yoga",
            category="Solar",
            nature="benefic",
            planets=planets_before,  # noqa: F841
            description=(
                f"{', '.join(planets_before)} in H{_wrap(sun_h-1)} (12th from Sun) → "
                f"industrious, respected, favours from authority"
            ),
        ))

    return yogas


# ── Special Yogas ──────────────────────────────────────────────────────────────

def _special_yogas(chart: BirthChart, hmap) -> list[Yoga]:
    yogas = []

    # ── Pancha-Graha Yoga: 5+ planets in one sign ──
    from collections import Counter
    sign_count = Counter(p.sign_index for pname, p in chart.planets.items()
                         if pname not in ("Rahu", "Ketu"))
    for si, count in sign_count.items():
        if count >= 5:
            planets_in = [
                pname for pname, pos in chart.planets.items()
                if pos.sign_index == si and pname not in ("Rahu", "Ketu")
            ]
            from src.ephemeris import SIGNS
            yogas.append(Yoga(
                name="Pancha-Graha Yoga",
                category="Special",
                nature="mixed",
                planets=planets_in,
                description=(
                    f"{count} planets in {SIGNS[si]} → extraordinary concentration of energy; "
                    f"intense focus on that house's themes; rare and powerful combination"
                ),
            ))

    # ── Guru-Chandala: Jupiter + Rahu conjunct ──
    if chart.planets["Jupiter"].sign_index == chart.planets["Rahu"].sign_index:
        jup_h = _planet_house("Jupiter", hmap)
        yogas.append(Yoga(
            name="Guru-Chandala Yoga",
            category="Negative",
            nature="malefic",
            planets=["Jupiter", "Rahu"],
            description=(
                f"Jupiter + Rahu conjunct in H{jup_h} → "
                f"unconventional beliefs, challenges with teachers/tradition "
                f"(can also indicate foreign wisdom if well-placed)"
            ),
        ))

    # ── Neecha Bhanga Raj Yoga: debilitated planet with cancellation in kendra ──
    _DEBILITATION: dict[str, int] = {
        "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11,
        "Jupiter": 9, "Venus": 5, "Saturn": 0,
    }
    for planet, debil_si in _DEBILITATION.items():
        if chart.planets[planet].sign_index == debil_si:
            # Check if lord of debilitation sign is in kendra
            from src.calculations.house_lord import sign_lord
            debil_sign_lord = sign_lord(debil_si)
            if debil_sign_lord in hmap.planet_house:
                dl_house = hmap.planet_house[debil_sign_lord]
                if is_kendra(dl_house):
                    yogas.append(Yoga(
                        name="Neecha Bhanga Raj Yoga",
                        category="Raj",
                        nature="benefic",
                        planets=[planet, debil_sign_lord],  # noqa: F841
                        description=(
                            f"{planet} debilitated but {debil_sign_lord} "
                            f"(debilitation lord) in kendra H{dl_house} → "
                            f"cancellation of debilitation, rise after setbacks"
                        ),
                    ))

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
        "Pancha Mahapurusha": 0, "Raj": 1, "Dhana": 2,
        "Lunar": 3, "Solar": 4, "Special": 5, "Negative": 6,
    }
    _NATURE_ORDER = {"benefic": 0, "mixed": 1, "malefic": 2}
    all_yogas.sort(key=lambda y: (
        _CATEGORY_ORDER.get(y.category, 9),
        _NATURE_ORDER.get(y.nature, 9),
    ))
    return all_yogas
