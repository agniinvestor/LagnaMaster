#!/usr/bin/env python3
"""fixup4 — final fix. Run from ~/LagnaMaster: python3 fixup4_phases.py"""
import os, sys

BASE = os.getcwd()
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); sys.exit(1)

print("Applying fixup4...\n")

# ── Fix 1: dignity.py — swap MT before Exalt using exact installed strings ──
with open("src/calculations/dignity.py") as f:
    src = f.read()

old = """    # Exaltation check
    if planet in EXALT_SIGN and sign_index == EXALT_SIGN[planet]:
        param_deg = PARAMOTCHA_DEGREE[planet]
        if abs(degree_in_sign - param_deg) <= DEEP_EXALT_ORB:
            return DignityLevel.DEEP_EXALT
        return DignityLevel.EXALT

    # Debilitation check (before NB so we can upgrade)
    if planet in DEBIL_SIGN and sign_index == DEBIL_SIGN[planet]:
        if nb_count >= 2:
            return DignityLevel.NEECHA_BHANGA_RAJA  # Uttarakalamrita Ch.4
        if is_debil_cancelled:
            return DignityLevel.NEECHA_BHANGA
        return DignityLevel.DEBIL

    # Mooltrikona (exact BPHS ranges)
    if planet in MOOLTRIKONA_RANGES:
        mt_si, mt_start, mt_end = MOOLTRIKONA_RANGES[planet]
        if sign_index == mt_si and mt_start <= degree_in_sign < mt_end:
            return DignityLevel.MOOLTRIKONA"""

new = """    # Mooltrikona FIRST — takes priority over exaltation (BPHS Ch.3)
    # Moon Taurus 4-30deg and Mercury Virgo 16-20deg are MT, not Exalt
    if planet in MOOLTRIKONA_RANGES:
        mt_si, mt_start, mt_end = MOOLTRIKONA_RANGES[planet]
        if sign_index == mt_si and mt_start <= degree_in_sign < mt_end:
            return DignityLevel.MOOLTRIKONA

    # Exaltation check
    if planet in EXALT_SIGN and sign_index == EXALT_SIGN[planet]:
        param_deg = PARAMOTCHA_DEGREE[planet]
        if abs(degree_in_sign - param_deg) <= DEEP_EXALT_ORB:
            return DignityLevel.DEEP_EXALT
        return DignityLevel.EXALT

    # Debilitation check
    if planet in DEBIL_SIGN and sign_index == DEBIL_SIGN[planet]:
        if nb_count >= 2:
            return DignityLevel.NEECHA_BHANGA_RAJA  # Uttarakalamrita Ch.4
        if is_debil_cancelled:
            return DignityLevel.NEECHA_BHANGA
        return DignityLevel.DEBIL"""

if old in src:
    with open("src/calculations/dignity.py", "w") as f:
        f.write(src.replace(old, new, 1))
    print("  OK   dignity.py [MT before Exalt]")
else:
    print("  FAIL dignity.py — pattern still not found")
    print("       Check lines 289-310 of src/calculations/dignity.py")

# ── Fix 2: test Kemadruma — Pisces(11) IS adjacent to Aries(0); use Gemini(2) ──
# Adjacent signs from Aries(0): Pisces(11) and Taurus(1)
# Kendra from Aries: Aries(0), Cancer(3), Libra(6), Capricorn(9)
# Safe sign: Gemini(2)=H3, Leo(4)=H5, Virgo(5)=H6, Scorpio(7)=H8
# Use Leo (sign 4, longitude 120) — H5 from Aries, not adjacent, not kendra
with open("tests/test_phase0.py") as f:
    tests = f.read()

old_t = """        # Moon in Aries (sign 0). Adjacent signs: Pisces(11), Taurus(1).
        # Kendra from Moon: H1=Aries(0), H4=Cancer(3), H7=Libra(6), H10=Capricorn(9).
        # Place all planets in Pisces (sign 11 = 330) -- H12 from Moon, not adjacent, not kendra.
        chart = make_chart(0.0,  # Aries Lagna
                           Moon=0.0,     # Aries
                           Sun=330.0,    # Pisces -- H12 from Moon, not adjacent, not kendra
                           Mars=330.0,   # Pisces
                           Mercury=330.0,
                           Jupiter=330.0,
                           Venus=330.0,
                           Saturn=330.0,
                           Rahu=40.0, Ketu=220.0)"""

new_t = """        # Moon in Aries (sign 0). Adjacent: Pisces(11), Taurus(1). Kendra: 0,3,6,9.
        # Use Leo (sign 4, lon 120) = H5 from Moon — not adjacent, not kendra.
        chart = make_chart(0.0,  # Aries Lagna
                           Moon=0.0,     # Aries
                           Sun=120.0,    # Leo = H5 from Moon, not adjacent, not kendra
                           Mars=125.0,   # Leo
                           Mercury=122.0,
                           Jupiter=128.0,
                           Venus=130.0,
                           Saturn=135.0,
                           Rahu=40.0, Ketu=220.0)"""

if old_t in tests:
    with open("tests/test_phase0.py", "w") as f:
        f.write(tests.replace(old_t, new_t, 1))
    print("  OK   tests/test_phase0.py [Kemadruma chart — Leo not Pisces]")
else:
    print("  SKIP tests/test_phase0.py [Kemadruma chart] — pattern not found")

print("\nDone. Run:")
print("  PYTHONPATH=. .venv/bin/pytest tests/test_phase0.py -v 2>&1 | tail -15")
