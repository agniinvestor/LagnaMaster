#!/usr/bin/env python3
"""
Fixup script — patches 6 issues in files already installed by install_phases.py
Run from ~/LagnaMaster:  python3 fixup_phases.py
"""
import os, sys

BASE = os.getcwd()

if not os.path.isfile("requirements.txt"):
    print("ERROR: run from the LagnaMaster repo root")
    sys.exit(1)


def patch(rel, old, new, label=""):
    path = os.path.join(BASE, rel)
    with open(path) as f:
        src = f.read()
    if old not in src:
        print(f"  SKIP {rel} [{label}]")
        return
    with open(path, "w") as f:
        f.write(src.replace(old, new, 1))
    print(f"  OK   {rel} [{label}]")


SL = (
    '{0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun",'
    ' 5: "Mercury", 6: "Venus", 7: "Mars", 8: "Jupiter",'
    ' 9: "Saturn", 10: "Saturn", 11: "Jupiter"}'
)

print("Applying fixups...\n")

patch("src/calculations/dignity.py",
      '    # ── Exaltation check ──\n    if planet in EXALT_SIGN and sign_index == EXALT_SIGN[planet]:',
      '    # ── Mooltrikona FIRST (MT wins over exaltation for same sign, BPHS Ch.3) ──\n    if planet in MOOLTRIKONA_RANGES:\n        mt_si, mt_start, mt_end = MOOLTRIKONA_RANGES[planet]\n        if sign_index == mt_si and mt_start <= degree_in_sign < mt_end:\n            return DignityLevel.MOOLTRIKONA\n\n    # ── Exaltation check ──\n    if planet in EXALT_SIGN and sign_index == EXALT_SIGN[planet]:',
      "MT before Exalt")

patch("src/calculations/dignity.py",
      '    # ── Mooltrikona (exact BPHS ranges) ──\n    if planet in MOOLTRIKONA_RANGES:\n        mt_si, mt_start, mt_end = MOOLTRIKONA_RANGES[planet]\n        if sign_index == mt_si and mt_start <= degree_in_sign < mt_end:\n            return DignityLevel.MOOLTRIKONA\n\n    # ── Own sign',
      '    # ── Own sign',
      "remove duplicate MT block")

patch("src/calculations/dignity.py",
      "from src.calculations.house_lord import SIGN_LORDS",
      "_SIGN_LORDS_NB = " + SL,
      "NB import")

patch("src/calculations/dignity.py",
      "debil_lord = SIGN_LORDS.get(debil_sign)",
      "debil_lord = _SIGN_LORDS_NB.get(debil_sign)",
      "NB lord lookup")

patch("src/calculations/scoring_patches.py",
      "from src.calculations.house_lord import SIGN_LORDS",
      "_SIGN_LORDS_SP = " + SL,
      "SP import")

patch("src/calculations/scoring_patches.py",
      "lagna_lord = SIGN_LORDS.get(lagna_si)",
      "lagna_lord = _SIGN_LORDS_SP.get(lagna_si)",
      "SP lord lookup")

patch("src/calculations/bhava_bala.py",
      "from src.calculations.house_lord import compute_house_map, SIGN_LORDS",
      "from src.calculations.house_lord import compute_house_map\n    _SIGN_LORDS_BB = " + SL,
      "BB import")

patch("src/calculations/bhava_bala.py",
      "house_lord = SIGN_LORDS.get(house_sign)",
      "house_lord = _SIGN_LORDS_BB.get(house_sign)",
      "BB lord lookup")

patch("src/calculations/pratyantar_dasha.py",
      "pd_years = md_years * ad_years * pd_lord_years / (120.0 * 120.0)",
      "pd_years = ad_years * pd_lord_years / 120.0",
      "PD formula")

patch("tests/test_phase0.py",
      "assert nakshatra_index(40.0) == 2  # Krittika",
      "assert nakshatra_index(40.0) == 3  # Rohini",
      "nak 40.0")

patch("tests/test_phase0.py",
      "assert nakshatra_index(39.9999) == 1  # Bharani",
      "assert nakshatra_index(39.9999) == 2  # Krittika",
      "nak 39.9999")

patch("tests/test_phase0.py",
      "assert nakshatra_index(80.0) == 5  # Ardra",
      "assert nakshatra_index(80.0) == 6  # Punarvasu",
      "nak 80.0")

print("\nDone. Run:")
print("  PYTHONPATH=. .venv/bin/pytest tests/test_phase0.py -v 2>&1 | tail -25")
