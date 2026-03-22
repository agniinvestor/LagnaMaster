"""
src/calculations/pressure_engine.py — LagnaMaster Session 30

The Life Pressure Index — the integrating engine that combines:

    Structural Vulnerability (natal baseline)
  × Dasha Activation Weight
  × Transit Load
  ÷ Resilience Factor
  = PressureIndex(date)  in [0.0, 10.0]

This is the critical missing layer identified in the gap analysis.
Static house scores tell you WHERE life will be strong or weak.
The Pressure Index tells you WHEN those areas will be activated.

Architecture
------------
  1. structural_vulnerability(chart) -> float [0..10]
     Natal baseline: functional malefics, Moon condition, badhaka,
     dusthana interlocking, lajjitadi state.

  2. dasha_activation_weight(chart, dashas, date) -> float [0..2]
     How "activated" is natal vulnerability right now?
     Amplified when MD/AD lords own or occupy dusthanas, are
     badhaka lords, marakas, or functionally malefic.

  3. transit_load(chart, date) -> float [0..2]
     How much real-time malefic pressure is being applied?
     Saturn/Rahu transits over Moon, Lagna, natal malefics.
     Sade Sati amplification.

  4. resilience_factor(chart, date) -> float [0.5..2.0]
     What protective mechanisms are active?
     Jupiter strength, yogakaraka dasha, benefic transits over Lagna.

  5. pressure_index = clamp(vuln × dasha × transit / resilience, 0, 10)

Public API
----------
    compute_pressure_index(chart, dashas, on_date) -> PressurePoint
    compute_pressure_timeline(chart, dashas, birth_date,
                              from_date, to_date, step_months) -> list[PressurePoint]
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class PressurePoint:
    date: date
    pressure_index: float  # 0.0 (tranquil) to 10.0 (crisis)
    label: str  # Tranquil / Mild / Moderate / Elevated / High / Critical
    structural_vulnerability: float
    dasha_activation: float
    transit_load: float
    resilience: float
    # Narrative drivers
    key_drivers: list[str] = field(default_factory=list)
    dasha_note: str = ""
    transit_note: str = ""

    @property
    def is_critical(self) -> bool:
        return self.pressure_index >= 7.5

    @property
    def is_elevated(self) -> bool:
        return self.pressure_index >= 5.0


_LABELS = [
    (8.5, "Critical"),
    (7.0, "High"),
    (5.5, "Elevated"),
    (4.0, "Moderate"),
    (2.5, "Mild"),
    (0.0, "Tranquil"),
]


def _label(score: float) -> str:
    for threshold, label in _LABELS:
        if score >= threshold:
            return label
    return "Tranquil"


# ── Component 1: Structural Vulnerability ────────────────────────────────────


def structural_vulnerability(chart) -> tuple[float, list[str]]:
    """
    Natal baseline pressure score [0..10].
    Higher = more vulnerable chart structure.
    """
    from src.calculations.functional_roles import compute_functional_roles
    from src.calculations.avastha import compute_lajjitadi
    from src.calculations.dignity import compute_all_dignities, DignityLevel
    from src.calculations.house_lord import compute_house_map

    drivers = []
    score = 0.0

    roles = compute_functional_roles(chart)
    hmap = compute_house_map(chart)
    digs = compute_all_dignities(chart)

    # Moon condition (most important psychological indicator)
    moon_pos = chart.planets.get("Moon")
    moon_dig = digs.get("Moon")
    if moon_dig:
        if moon_dig.dignity == DignityLevel.DEBIL:
            score += 2.0
            drivers.append("Moon debilitated")
        elif moon_dig.dignity == DignityLevel.ENEMY_SIGN:
            score += 1.0
            drivers.append("Moon in enemy sign")
        if moon_dig.combust:
            score += 1.5
            drivers.append("Moon combust")

    # Saturn-Moon relationship (chronic stress indicator)
    sat_pos = chart.planets.get("Saturn")
    if moon_pos and sat_pos:
        if moon_pos.sign_index == sat_pos.sign_index:
            score += 2.0
            drivers.append("Saturn conjunct Moon (natal)")
        moon_house = hmap.planet_house.get("Moon", 1)
        sat_house = hmap.planet_house.get("Saturn", 1)
        # Saturn aspects Moon (3rd, 7th, 10th from Saturn)
        for aspect_offset in [3, 7, 10]:
            if (sat_house - 1 + aspect_offset - 1) % 12 + 1 == moon_house:
                score += 1.0
                drivers.append(f"Saturn aspects Moon ({aspect_offset}th aspect)")
                break

    # Badhaka lord placement
    badhaka_lord = roles.badhaka_lord
    if badhaka_lord in hmap.planet_house:
        bl_house = hmap.planet_house[badhaka_lord]
        if bl_house in {1, 4, 7, 10}:
            score += 1.5
            drivers.append(f"Badhaka lord {badhaka_lord} in kendra H{bl_house}")
        elif bl_house in {1}:
            score += 2.0
            drivers.append(f"Badhaka lord {badhaka_lord} in lagna")

    # Functional malefics in H1/H4/H7/H10 (kendras)
    for planet in roles.functional_malefics:
        if planet in hmap.planet_house:
            h = hmap.planet_house[planet]
            if h in {1, 4, 7, 10}:
                score += 0.5
                drivers.append(f"{planet} (func. malefic) in kendra H{h}")

    # Dusthana interlocking
    d6_lord = roles.house_lords.get(6, "")
    d8_lord = roles.house_lords.get(8, "")
    roles.house_lords.get(12, "")
    if d6_lord in hmap.planet_house:
        if hmap.planet_house[d6_lord] in {8, 12}:
            score += 1.0
            drivers.append("H6 lord in H8/H12 (dusthana interlocking)")
    if d8_lord in hmap.planet_house:
        if hmap.planet_house[d8_lord] == 1:
            score += 1.5
            drivers.append("H8 lord in H1 (transformation pressure)")

    # Lajjitadi state of 5th lord
    laj = compute_lajjitadi(chart)
    if laj.state == "Lajjita":
        score += 2.0
        drivers.append(f"5th lord {laj.fifth_lord} Lajjita: {', '.join(laj.triggers)}")
    elif laj.state in {"Kshobhita", "Kshudhita"}:
        score += 1.0
        drivers.append(f"5th lord {laj.fifth_lord} {laj.state}")

    return min(score, 10.0), drivers


# ── Component 2: Dasha Activation Weight ─────────────────────────────────────


def dasha_activation_weight(chart, dashas: list, on_date: date) -> tuple[float, str]:
    """
    How much does the current dasha period amplify natal vulnerability? [0..2]
    """
    from src.calculations.vimshottari_dasa import current_dasha
    from src.calculations.functional_roles import compute_functional_roles
    from src.calculations.house_lord import compute_house_map

    roles = compute_functional_roles(chart)
    hmap = compute_house_map(chart)

    try:
        md, ad = current_dasha(dashas, on_date)
    except Exception:
        return 1.0, "Dasha unavailable"

    weight = 1.0
    notes = []

    for lord, kind in [(md.lord, "MD"), (ad.lord, "AD")]:
        # Functional malefic running dasha
        if lord in roles.functional_malefics:
            weight += 0.25
            notes.append(f"{lord} {kind} is func. malefic")

        # Dasha lord is badhaka lord
        if lord == roles.badhaka_lord:
            weight += 0.4
            notes.append(f"{lord} {kind} is badhaka lord")

        # Dasha lord is maraka lord
        if lord in roles.maraka_lords:
            weight += 0.2
            notes.append(f"{lord} {kind} is maraka lord")

        # Dasha lord placed in dusthana
        if lord in hmap.planet_house and hmap.planet_house[lord] in {6, 8, 12}:
            weight += 0.25
            notes.append(f"{lord} {kind} in dusthana H{hmap.planet_house[lord]}")

        # Yogakaraka running — reduces weight
        if lord in roles.yogakarakas:
            weight -= 0.3
            notes.append(f"{lord} {kind} is yogakaraka (protective)")

    note = (
        f"{md.lord} MD / {ad.lord} AD: {'; '.join(notes)}"
        if notes
        else f"{md.lord} MD / {ad.lord} AD (neutral)"
    )
    return max(0.1, min(weight, 2.0)), note


# ── Component 3: Transit Load ─────────────────────────────────────────────────


def transit_load(chart, on_date: date) -> tuple[float, str]:
    """
    Real-time malefic transit pressure against the natal chart. [0..2]
    """
    from src.calculations.gochara import compute_gochara
    from src.calculations.house_lord import compute_house_map

    compute_house_map(chart)
    moon_natal_si = chart.planets["Moon"].sign_index
    lagna_si = chart.lagna_sign_index

    try:
        gochara = compute_gochara(chart, on_date)
    except Exception:
        return 1.0, "Transit computation unavailable"

    load = 1.0
    notes = []

    # Sade Sati — Saturn transiting Moon signs
    if gochara.sade_sati:
        phase_weight = {"Peak": 0.6, "Rising": 0.3, "Setting": 0.2}.get(
            gochara.sade_sati_phase, 0.2
        )
        load += phase_weight
        notes.append(f"Sade Sati {gochara.sade_sati_phase}")

    # Saturn transiting over Lagna
    sat_transit = gochara.planets.get("Saturn")
    if sat_transit and sat_transit.sign_index == lagna_si:
        load += 0.4
        notes.append("Saturn transiting Lagna")

    # Rahu/Ketu over Moon or Lagna (eclipse axis)
    rahu_transit = gochara.planets.get("Rahu")
    if rahu_transit:
        if rahu_transit.sign_index in {moon_natal_si, lagna_si}:
            load += 0.3
            notes.append("Rahu transiting Moon/Lagna sign")

    # Mars transit over Moon (emotional activation)
    mars_transit = gochara.planets.get("Mars")
    if mars_transit and mars_transit.sign_index == moon_natal_si:
        load += 0.2
        notes.append("Mars transiting natal Moon sign")

    # Multiple malefics in same sign (clustering)
    transit_signs: dict[int, list[str]] = {}
    malefic_planets = ["Saturn", "Mars", "Rahu", "Ketu"]
    for p in malefic_planets:
        tp = gochara.planets.get(p)
        if tp:
            transit_signs.setdefault(tp.sign_index, []).append(p)
    for si, planets in transit_signs.items():
        if len(planets) >= 2:
            load += 0.3
            notes.append(f"Malefic cluster ({', '.join(planets)}) in {_sign_name(si)}")

    note = "; ".join(notes) if notes else "Transits benign"
    return max(0.1, min(load, 2.0)), note


def _sign_name(si: int) -> str:
    names = [
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
    return names[si % 12]


# ── Component 4: Resilience Factor ───────────────────────────────────────────


def resilience_factor(chart, dashas: list, on_date: date) -> tuple[float, str]:
    """
    Protective capacity that divides the raw pressure. [0.5..2.0]
    Higher = more protection (reduces final pressure index).
    """
    from src.calculations.vimshottari_dasa import current_dasha
    from src.calculations.functional_roles import compute_functional_roles
    from src.calculations.shadbala import compute_shadbala
    from src.calculations.gochara import compute_gochara

    roles = compute_functional_roles(chart)
    resilience = 1.0
    notes = []

    # Jupiter strength (primary protector)
    try:
        jup_sb = compute_shadbala("Jupiter", chart)
        if jup_sb.total > 300:
            resilience += 0.3
            notes.append(f"Strong Jupiter ({jup_sb.total:.0f} Virupas)")
        elif jup_sb.total < 150:
            resilience -= 0.2
            notes.append(f"Weak Jupiter ({jup_sb.total:.0f} Virupas)")
    except Exception:
        pass

    # Yogakaraka in dasha
    try:
        md, ad = current_dasha(dashas, on_date)
        if md.lord in roles.yogakarakas or ad.lord in roles.yogakarakas:
            resilience += 0.25
            notes.append("Yogakaraka dasha active")
    except Exception:
        pass

    # Jupiter transiting kendra from natal Moon
    try:
        gochara = compute_gochara(chart, on_date)
        moon_si = chart.planets["Moon"].sign_index
        jup_tr = gochara.planets.get("Jupiter")
        if jup_tr:
            dist = (jup_tr.sign_index - moon_si) % 12 + 1
            if dist in {1, 4, 7, 10}:
                resilience += 0.3
                notes.append("Jupiter in kendra from natal Moon (transit)")
    except Exception:
        pass

    note = "; ".join(notes) if notes else "Standard resilience"
    return max(0.5, min(resilience, 2.0)), note


# ── Public API ────────────────────────────────────────────────────────────────


def compute_pressure_index(
    chart, dashas: list, on_date: Optional[date] = None
) -> PressurePoint:
    """Compute the Life Pressure Index for a single date."""
    if on_date is None:
        on_date = date.today()

    vuln, vuln_drivers = structural_vulnerability(chart)
    dasha_w, dasha_note = dasha_activation_weight(chart, dashas, on_date)
    t_load, transit_note = transit_load(chart, on_date)
    resil, _ = resilience_factor(chart, dashas, on_date)

    raw = (vuln / 10.0) * dasha_w * t_load / resil * 10.0
    final = min(max(raw, 0.0), 10.0)

    return PressurePoint(
        date=on_date,
        pressure_index=round(final, 2),
        label=_label(final),
        structural_vulnerability=round(vuln, 2),
        dasha_activation=round(dasha_w, 2),
        transit_load=round(t_load, 2),
        resilience=round(resil, 2),
        key_drivers=vuln_drivers,
        dasha_note=dasha_note,
        transit_note=transit_note,
    )


def compute_pressure_timeline(
    chart,
    dashas: list,
    from_date: date,
    to_date: date,
    step_months: int = 3,
) -> list[PressurePoint]:
    """
    Compute the Pressure Index across a date range.
    Returns a list of PressurePoint objects at step_months intervals.
    Default step = quarterly (3 months).
    """
    points = []
    current = from_date
    while current <= to_date:
        points.append(compute_pressure_index(chart, dashas, current))
        # Advance by step_months
        month = current.month - 1 + step_months
        year = current.year + month // 12
        month = month % 12 + 1
        try:
            current = current.replace(year=year, month=month)
        except ValueError:
            import calendar

            last_day = calendar.monthrange(year, month)[1]
            current = current.replace(
                year=year, month=month, day=min(current.day, last_day)
            )
    return points
