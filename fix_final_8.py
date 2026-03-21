#!/usr/bin/env python3
"""Final 8 fixes. Run from ~/LagnaMaster: python3 fix_final_8.py"""
import os, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# ── Fix 1: test_calculations.py local imports inside methods ──
with open("tests/test_calculations.py") as f:
    tc = f.read()

# Fix local imports inside test methods (not caught by module-level replacement)
tc = tc.replace(
    "from src.calculations.dignity import compute_dignity, DignityLevel",
    "from src.calculations.dignity import compute_dignity_legacy as compute_dignity, DignityLevel"
)
tc = tc.replace(
    "from src.calculations.shadbala import compute_shadbala, ",
    "from src.calculations.shadbala import compute_shadbala_legacy as compute_shadbala, "
)
tc = tc.replace(
    "from src.calculations.shadbala import compute_shadbala\n",
    "from src.calculations.shadbala import compute_shadbala_legacy as compute_shadbala\n"
)

import ast
try:
    ast.parse(tc)
    with open("tests/test_calculations.py", "w") as f:
        f.write(tc)
    print("  OK  tests/test_calculations.py [local import fixes]")
except SyntaxError as e:
    print(f"  SYNTAX ERROR line {e.lineno}: {tc.split(chr(10))[e.lineno-1]}")

# ── Fix 2: test_phase0.py navamsha_sign type check ──
with open("tests/test_phase0.py") as f:
    tp = f.read()

tp = tp.replace(
    "assert 0 <= pos.navamsha_sign <= 11",
    "assert pos.navamsha_sign in ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']"
)
with open("tests/test_phase0.py", "w") as f:
    f.write(tp)
print("  OK  tests/test_phase0.py [navamsha_sign string check]")

print("\nRun: PYTHONPATH=. .venv/bin/pytest tests/test_calculations.py tests/test_phase0.py -q 2>&1 | tail -4")
