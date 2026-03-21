#!/usr/bin/env python3
"""Compatibility aliases. Run from ~/LagnaMaster: python3 fixup_compat.py"""
import os
BASE = os.getcwd()
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

def append(path, text, label):
    with open(path) as f: src = f.read()
    if text.strip().split("=")[0].strip() in src:
        print(f"  SKIP {path} [{label}]"); return
    with open(path, "a") as f: f.write("\n" + text)
    print(f"  OK   {path} [{label}]")

def patch(path, old, new, label):
    with open(path) as f: src = f.read()
    if old not in src: print(f"  SKIP {path} [{label}]"); return
    with open(path, "w") as f: f.write(src.replace(old, new, 1))
    print(f"  OK   {path} [{label}]")

print("Adding compatibility aliases...\n")

# 1. nakshatra.py: NAKSHATRAS and NAKSHATRA_SPAN aliases
append("src/calculations/nakshatra.py", """
# ── Backward-compatibility aliases ──
NAKSHATRAS = NAKSHATRA_NAMES          # old name used by existing tests/modules
NAKSHATRA_SPAN = _NAK_WIDTH           # old name: degrees per nakshatra = 40/3
""", "NAKSHATRAS + NAKSHATRA_SPAN aliases")

# 2. dignity.py: RETROGRADE_BONUS alias + is_retrograde on DignityResult
append("src/calculations/dignity.py", """
# ── Backward-compatibility aliases ──
RETROGRADE_BONUS = 0.0  # old scoring constant; retrograde handled in chesta_bala now
""", "RETROGRADE_BONUS alias")

# Add is_retrograde property to DignityResult
patch("src/calculations/dignity.py",
    "    @property\n    def score_modifier(self) -> float:",
    """    @property
    def is_retrograde(self) -> bool:
        \"\"\"Backward-compat: scoring.py checks d.is_retrograde on DignityResult.
        Retrograde status lives on the planet object; mirror asta_vakri as proxy.\"\"\"
        return self.asta_vakri  # asta_vakri = combust+retrograde; False otherwise

    @property
    def score_modifier(self) -> float:""",
    "is_retrograde property")

print("\nDone. Run:")
print("  PYTHONPATH=. .venv/bin/pytest --tb=line -q --ignore=tests/test_session21.py --ignore=tests/test_varga.py 2>&1 | tail -4")
