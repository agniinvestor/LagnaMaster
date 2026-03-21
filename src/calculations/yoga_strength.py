"""
src/calculations/yoga_strength.py
Yoga strength gradient + missing named yogas (Amala, Vasumati, Sannyasa, etc.)
Sessions 140, 145.

Sources:
  PVRNR · BPHS Ch.36 v.15-20 (Raj Yoga strength gradation)
  Gayatri Devi Vasudev · The Art of Prediction in Astrology Ch.3 (yoga gradient)
  Mantreswara · Phaladeepika Ch.6 v.35-45 (Amala, Mahabhagya, Chamara)
  PVRNR · BPHS Ch.36 v.50-58 (Sannyasa Yogas)
  BV Raman · Three Hundred Important Combinations #163-174 (Sannyasa)
  Saravali Ch.21 (Vasumati Yoga)
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# ─── Yoga Strength Gradient ───────────────────────────────────────────────────

@dataclass
class YogaStrength:
    yoga_name: str
    base_present: bool
    strength_score: float          # 0.0 to 1.0
    strength_label: str            # "Strong" / "Moderate" / "Weak" / "Dormant"
    d9_confirmed: bool
    forming_planets: list[str]
    planet_dignities: dict[str, str]
    cancellation_factors: list[str]
    fructification_note: str       # when it's likely to manifest


def compute_yoga_strength(yoga_name: str, forming_planets: list[str], chart) -> YogaStrength:
    """
    Compute gradient strength for any detected yoga.
    Source: PVRNR · BPHS Ch.36 v.15-20; Gayatri Devi Vasudev, Art of Prediction Ch.3
    """
    if not forming_planets:
        return YogaStrength(yoga_name, False, 0.0, "Absent", False, [], {}, [], "")

    from src.calculations.dignity import compute_dignity, DignityLevel

    total_score = 0.0
    planet_dignities = {}
    cancellation_factors = []

    for planet in forming_planets:
        if planet not in chart.planets:
            continue
        d = compute_dignity(planet, chart)
        dname = d.dignity.value
        planet_dignities[planet] = dname

        # Dignity component (0.0-0.4 per planet)
        dignity_scores = {
            "Deep Exaltation": 0.40, "Exaltation": 0.35,
            "Neecha Bhanga Raja Yoga": 0.30, "Mooltrikona": 0.30,
            "Own Sign": 0.25, "Friendly Sign": 0.15,
            "Neutral": 0.10, "Enemy Sign": 0.05,
            "Neecha Bhanga": 0.08, "Debilitation": 0.0,
        }
        total_score += dignity_scores.get(dname, 0.10)

        # Cancellation factors
        if d.combust and not d.cazimi:
            cancellation_factors.append(f"{planet} combust")
        if d.is_sandhi:
            cancellation_factors.append(f"{planet} Sandhi (junction)")

    # Normalize to 0-1
    max_possible = 0.40 * len(forming_planets)
    strength = min(1.0, total_score / max_possible) if max_possible > 0 else 0.0

    # D9 confirmation: check if any forming planet is Vargottama
    d9_confirmed = any(
        compute_dignity(p, chart).is_vargottama
        for p in forming_planets if p in chart.planets
    )
    if d9_confirmed:
        strength = min(1.0, strength * 1.15)

    # Reduce for cancellations
    strength *= (1.0 - 0.15 * min(3, len(cancellation_factors)))
    strength = max(0.0, strength)

    if strength >= 0.75:  label = "Strong"
    elif strength >= 0.45: label = "Moderate"
    elif strength >= 0.20: label = "Weak"
    else:                  label = "Dormant"

    # Fructification note
    fruct = f"Yoga activates in dasha of {forming_planets[0]} (MD/AD)"
    if d9_confirmed:
        fruct += " — D9 Vargottama confirms high potency"

    return YogaStrength(
        yoga_name=yoga_name,
        base_present=True,
        strength_score=round(strength, 3),
        strength_label=label,
        d9_confirmed=d9_confirmed,
        forming_planets=forming_planets,
        planet_dignities=planet_dignities,
        cancellation_factors=cancellation_factors,
        fructification_note=fruct,
    )


# ─── Missing Named Yogas ──────────────────────────────────────────────────────

@dataclass
class NamedYogaResult:
    name: str
    present: bool
    strength: Optional[YogaStrength]
    planets: list[str]
    description: str
    source: str


def detect_amala_yoga(chart) -> Optional[NamedYogaResult]:
    """
    Amala Yoga: H10 from Lagna AND H10 from Moon occupied only by natural benefics.
    Source: Phaladeepika Ch.6 v.40
    """
    lagna_si = chart.lagna_sign_index
    moon_si  = chart.planets["Moon"].sign_index if "Moon" in chart.planets else lagna_si

    h10_from_lagna = (lagna_si + 9) % 12
    h10_from_moon  = (moon_si  + 9) % 12

    natural_benefics = {"Moon", "Mercury", "Jupiter", "Venus"}
    natural_malefics  = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}

    planets_h10_lagna = [p for p, pd in chart.planets.items() if pd.sign_index == h10_from_lagna]
    planets_h10_moon  = [p for p, pd in chart.planets.items() if pd.sign_index == h10_from_moon]

    all_h10 = set(planets_h10_lagna) | set(planets_h10_moon)

    # No malefics in H10 from either Lagna or Moon
    if all_h10 and not any(p in natural_malefics for p in all_h10):
        benefics_present = [p for p in all_h10 if p in natural_benefics]
        return NamedYogaResult(
            name="Amala Yoga", present=True,
            strength=compute_yoga_strength("Amala Yoga", benefics_present, chart),
            planets=benefics_present,
            description="H10 from Lagna and Moon occupied only by benefics — spotless character, lasting fame",
            source="Phaladeepika Ch.6 v.40",
        )
    return None


def detect_vasumati_yoga(chart) -> Optional[NamedYogaResult]:
    """
    Vasumati Yoga: all natural benefics in upachaya houses (3/6/10/11) from Lagna or Moon.
    Source: PVRNR · BPHS Ch.36; Saravali Ch.21
    """
    lagna_si = chart.lagna_sign_index
    moon_si  = chart.planets["Moon"].sign_index if "Moon" in chart.planets else lagna_si

    natural_benefics = {"Mercury", "Jupiter", "Venus"}  # Moon excluded (it's reference)
    upachaya_offsets = {2, 5, 9, 10}  # 3rd, 6th, 10th, 11th (0-indexed from lagna)

    upachaya_from_lagna = {(lagna_si + o) % 12 for o in upachaya_offsets}
    upachaya_from_moon  = {(moon_si  + o) % 12 for o in upachaya_offsets}

    benefics_in_chart = [p for p in natural_benefics if p in chart.planets]

    all_in_upachaya_lagna = all(
        chart.planets[p].sign_index in upachaya_from_lagna for p in benefics_in_chart
    )
    all_in_upachaya_moon = all(
        chart.planets[p].sign_index in upachaya_from_moon for p in benefics_in_chart
    )

    if benefics_in_chart and (all_in_upachaya_lagna or all_in_upachaya_moon):
        ref = "Lagna" if all_in_upachaya_lagna else "Moon"
        return NamedYogaResult(
            name="Vasumati Yoga", present=True,
            strength=compute_yoga_strength("Vasumati Yoga", benefics_in_chart, chart),
            planets=benefics_in_chart,
            description=f"All benefics in upachaya from {ref} — native accumulates wealth through own efforts",
            source="BPHS Ch.36; Saravali Ch.21",
        )
    return None


def detect_mahabhagya_yoga(chart, is_male: bool = True, is_day_birth: bool = True) -> Optional[NamedYogaResult]:
    """
    Mahabhagya Yoga:
    Male: daytime birth, Sun + Moon + Lagna all in odd signs
    Female: nighttime birth, Sun + Moon + Lagna all in even signs
    Source: Phaladeepika Ch.6 v.35-38
    """
    lagna_si = chart.lagna_sign_index
    sun_si   = chart.planets["Sun"].sign_index  if "Sun"  in chart.planets else -1
    moon_si  = chart.planets["Moon"].sign_index if "Moon" in chart.planets else -1

    if sun_si == -1 or moon_si == -1:
        return None

    # Odd signs (Aries=0, Gemini=2, Leo=4, Libra=6, Sag=8, Aquarius=10): index 0,2,4,6,8,10
    def is_odd_sign(si): return si % 2 == 0  # 0-indexed, so Aries(0) is odd

    if is_male and is_day_birth:
        condition = all(is_odd_sign(si) for si in (lagna_si, sun_si, moon_si))
        condition_desc = "Male, daytime, Sun+Moon+Lagna in odd signs"
    elif not is_male and not is_day_birth:
        condition = all(not is_odd_sign(si) for si in (lagna_si, sun_si, moon_si))
        condition_desc = "Female, nighttime, Sun+Moon+Lagna in even signs"
    else:
        # Partial yoga check (2/3 conditions)
        if is_male:
            met = sum(1 for si in (lagna_si, sun_si, moon_si) if is_odd_sign(si))
        else:
            met = sum(1 for si in (lagna_si, sun_si, moon_si) if not is_odd_sign(si))
        if met == 2:
            condition_desc = "Partial Mahabhagya (2/3 conditions)"
            return NamedYogaResult(
                name="Partial Mahabhagya Yoga", present=True, strength=None,
                planets=["Sun", "Moon"],
                description="2 of 3 Mahabhagya conditions met — partial greatness",
                source="Phaladeepika Ch.6 v.35-38",
            )
        return None

    if condition:
        return NamedYogaResult(
            name="Mahabhagya Yoga", present=True,
            strength=compute_yoga_strength("Mahabhagya Yoga", ["Sun", "Moon"], chart),
            planets=["Sun", "Moon"],
            description=f"{condition_desc} — native of great fortune and noble qualities",
            source="Phaladeepika Ch.6 v.35-38",
        )
    return None


def detect_sannyasa_yogas(chart) -> list[NamedYogaResult]:
    """
    Sannyasa (Renunciation) Yogas: 4+ planets in one sign.
    Different planets produce different renunciation types.
    Source: PVRNR · BPHS Ch.36 v.50-58; BV Raman · Three Hundred Combinations #163-174
    """
    results = []
    sign_planets: dict[int, list[str]] = {}

    for planet, pdata in chart.planets.items():
        si = pdata.sign_index
        sign_planets.setdefault(si, []).append(planet)

    for si, planets in sign_planets.items():
        if len(planets) >= 4:
            # Classify by which planets are involved
            if "Jupiter" in planets:
                yoga_name = "Brahma Sannyasa Yoga"
                desc = "Jupiter among 4+ planets in one sign — highest spiritual renunciation, sage-like"
            elif "Saturn" in planets:
                yoga_name = "Vanaprastha Sannyasa Yoga"
                desc = "Saturn among 4+ planets — practical renunciation, forest-dweller type"
            elif "Moon" in planets:
                yoga_name = "Pravrajya Sannyasa Yoga"
                desc = "Moon among 4+ planets — emotional/devotional renunciation"
            else:
                yoga_name = "Sannyasa Yoga"
                desc = f"{len(planets)} planets in one sign — enforced renunciation or intense focus"

            try:
                ys = compute_yoga_strength(yoga_name, planets, chart)
            except Exception:
                ys = None
            results.append(NamedYogaResult(
                name=yoga_name, present=True,
                strength=ys,
                planets=planets,
                description=desc,
                source="BPHS Ch.36 v.50-58",
            ))

    return results


def detect_chamara_yoga(chart) -> Optional[NamedYogaResult]:
    """
    Chamara Yoga: Lagna lord exalted in Kendra AND aspected by Jupiter.
    Source: Jataka Parijata
    """
    from src.calculations.dignity import compute_dignity, DignityLevel, EXALT_SIGN
    from src.calculations.house_lord import SIGN_LORDS

    lagna_si = chart.lagna_sign_index
    lagna_lord = SIGN_LORDS.get(lagna_si)
    if not lagna_lord or lagna_lord not in chart.planets:
        return None

    d = compute_dignity(lagna_lord, chart)
    if d.dignity not in (DignityLevel.EXALT, DignityLevel.DEEP_EXALT):
        return None

    # Must be in Kendra from Lagna
    ll_si = chart.planets[lagna_lord].sign_index
    house = (ll_si - lagna_si) % 12 + 1
    if house not in (1, 4, 7, 10):
        return None

    # Jupiter must aspect the Lagna lord's house
    if "Jupiter" not in chart.planets:
        return None

    jup_si = chart.planets["Jupiter"].sign_index
    jup_house = (jup_si - lagna_si) % 12 + 1
    from src.calculations.scoring_patches import aspect_hits, get_aspect_strength
    asp_str = get_aspect_strength("Jupiter", aspect_hits(jup_house, house))
    if asp_str == 0:
        return None

    return NamedYogaResult(
        name="Chamara Yoga", present=True,
        strength=compute_yoga_strength("Chamara Yoga", [lagna_lord, "Jupiter"], chart),
        planets=[lagna_lord, "Jupiter"],
        description="Lagna lord exalted in Kendra + Jupiter's aspect — great scholar, respected administrator",
        source="Jataka Parijata",
    )


def detect_all_additional_yogas(chart,
                                 is_male: bool = True,
                                 is_day_birth: bool = True) -> list[NamedYogaResult]:
    """Run all additional yoga detectors and return present ones."""
    results = []
    for detector in [
        lambda: detect_amala_yoga(chart),
        lambda: detect_vasumati_yoga(chart),
        lambda: detect_mahabhagya_yoga(chart, is_male, is_day_birth),
        lambda: detect_chamara_yoga(chart),
    ]:
        r = detector()
        if r and r.present:
            results.append(r)

    results.extend(detect_sannyasa_yogas(chart))
    return results
