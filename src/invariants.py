"""src/invariants.py — Runtime invariant checker for computed charts.

Validates structural correctness of BirthChart objects after computation.
These invariants must ALWAYS hold — violations indicate bugs in the pipeline.

Usage:
    from src.invariants import check_invariants
    errors = check_invariants(chart)
    if errors:
        raise ValueError(f"Chart invariant violations: {errors}")

Wire into compute pipeline after Layer 3 (calculations) completes.
"""

from __future__ import annotations

from src.data.constants import SIGN_LORDS


def check_invariants(chart) -> list[str]:
    """Check all structural invariants on a computed chart.

    Returns empty list if all invariants hold. Each string describes a violation.
    """
    errors: list[str] = []
    errors.extend(_check_planet_placement(chart))
    errors.extend(_check_lordship_uniqueness(chart))
    errors.extend(_check_dignity_valid(chart))
    errors.extend(_check_house_count(chart))
    errors.extend(_check_lagna_valid(chart))
    return errors


def _check_planet_placement(chart) -> list[str]:
    """INV-1: Every planet must have sign_index in [0, 11] and longitude in [0, 360)."""
    errors = []
    for name, pos in chart.planets.items():
        si = getattr(pos, "sign_index", None)
        if si is None:
            errors.append(f"INV-1: {name} has no sign_index")
            continue
        if not (0 <= si <= 11):
            errors.append(f"INV-1: {name} sign_index={si} not in [0, 11]")
        lon = getattr(pos, "longitude", None)
        if lon is not None and not (0.0 <= lon < 360.0):
            errors.append(f"INV-1: {name} longitude={lon} not in [0, 360)")
        deg = getattr(pos, "degree_in_sign", None)
        if deg is not None and not (0.0 <= deg < 30.0):
            errors.append(f"INV-1: {name} degree_in_sign={deg} not in [0, 30)")
    return errors


def _check_lordship_uniqueness(chart) -> list[str]:
    """INV-2: Each sign has exactly one lord (from SIGN_LORDS)."""
    errors = []
    if len(SIGN_LORDS) != 12:
        errors.append(f"INV-2: SIGN_LORDS has {len(SIGN_LORDS)} entries, expected 12")
    for si in range(12):
        lord = SIGN_LORDS.get(si) if isinstance(SIGN_LORDS, dict) else (SIGN_LORDS[si] if si < len(SIGN_LORDS) else None)
        if not lord:
            errors.append(f"INV-2: sign_index {si} has no lord in SIGN_LORDS")
    return errors


def _check_dignity_valid(chart) -> list[str]:
    """INV-3: If dignity is computed, it must be a valid state."""
    errors = []
    VALID_STATES = {
        "exalted", "own_sign", "moolatrikona", "friend_sign",
        "neutral", "enemy_sign", "debilitated",
    }
    # Check if chart has dignities attribute (only present after dignity computation)
    dignities = getattr(chart, "_dignities", None)
    if dignities is None:
        return []  # Dignity not computed — skip
    for planet, dig in dignities.items():
        state = getattr(dig, "dignity", None)
        if state is not None and state.value not in VALID_STATES:
            errors.append(f"INV-3: {planet} dignity={state.value} not valid")
    return errors


def _check_house_count(chart) -> list[str]:
    """INV-4: Chart must have exactly 7-9 planets (7 classical + Rahu/Ketu optional)."""
    errors = []
    count = len(chart.planets)
    if count < 7:
        errors.append(f"INV-4: chart has {count} planets, expected >= 7")
    if count > 11:
        errors.append(f"INV-4: chart has {count} planets, expected <= 11")
    # Classical planets must be present
    for required in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        if required not in chart.planets:
            errors.append(f"INV-4: missing required planet {required}")
    return errors


def _check_lagna_valid(chart) -> list[str]:
    """INV-5: Lagna sign index must be in [0, 11] and lagna degree consistent."""
    errors = []
    lsi = getattr(chart, "lagna_sign_index", None)
    if lsi is None:
        errors.append("INV-5: chart has no lagna_sign_index")
    elif not (0 <= lsi <= 11):
        errors.append(f"INV-5: lagna_sign_index={lsi} not in [0, 11]")

    lagna = getattr(chart, "lagna", None)
    if lagna is not None:
        if not (0.0 <= lagna < 360.0):
            errors.append(f"INV-5: lagna={lagna} not in [0, 360)")
        elif lsi is not None:
            expected_si = int(lagna / 30) % 12
            if expected_si != lsi:
                errors.append(
                    f"INV-5: lagna={lagna} implies sign_index={expected_si} "
                    f"but lagna_sign_index={lsi}"
                )
    return errors
