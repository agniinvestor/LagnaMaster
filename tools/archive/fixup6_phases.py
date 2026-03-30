#!/usr/bin/env python3
"""fixup6. Run from ~/LagnaMaster: python3 fixup6_phases.py"""
import os
BASE = os.getcwd()
path = "tests/test_phase0.py"
with open(path) as f:
    src = f.read()

# The replacement dropped the first line of test_sun_at_paramotcha.
# Insert it back right after the moon_mt_start method.
old = """        assert r.dignity == DignityLevel.DEEP_EXALT

    def test_sun_at_paramotcha(self):"""

new = """        assert r.dignity == DignityLevel.DEEP_EXALT

    def test_sun_at_paramotcha(self):
        \"\"\"Sun at Aries 10deg (Paramotcha) = Uchcha Bala 60.\"\"\"
        from src.calculations.dignity import get_uchcha_bala
        bala = get_uchcha_bala("Sun", 10.0)"""

# Check if test_sun_at_paramotcha body is already there
if 'bala = get_uchcha_bala("Sun", 10.0)' in src:
    print("Already fixed — nothing to do")
else:
    src = src.replace(old, new, 1)
    with open(path, "w") as f:
        f.write(src)
    print("OK  restored test_sun_at_paramotcha body")

print("\nRun: PYTHONPATH=. .venv/bin/pytest tests/test_phase0.py -v 2>&1 | tail -6")
