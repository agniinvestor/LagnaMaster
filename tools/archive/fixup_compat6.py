#!/usr/bin/env python3
"""Compat6. Run from ~/LagnaMaster: python3 fixup_compat6.py"""
import os
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

def patch(path, old, new, label):
    with open(path) as f: src = f.read()
    if old not in src: print(f"  SKIP {path} [{label}]"); return
    with open(path, "w") as f: f.write(src.replace(old, new, 1))
    print(f"  OK   {path} [{label}]")

print("Applying compat6...\n")

# ── 1. nakshatra.py: remove the broken class-level access ──
# The line `NakshatraPosition.navamsha_sign.fget...` raises AttributeError at import time
# on Python 3.14 for a required dataclass field. Just remove it.
patch("src/calculations/nakshatra.py",
    """# ── Backward-compat: old navamsha_sign returned sign name string ──
# Monkey-patch NakshatraPosition to add string accessor
_orig_navamsha_sign = NakshatraPosition.navamsha_sign.fget if hasattr(NakshatraPosition.navamsha_sign, 'fget') else None""",
    "# navamsha_sign now returns sign name string directly (see field definition above)",
    "remove broken class-level access")

# ── 2. dignity.py: add .weight alias (old tests used result.weight) ──
patch("src/calculations/dignity.py",
    "    @property\n    def total_modifier(self) -> float:  # backward-compat alias",
    """    @property
    def weight(self) -> float:  # backward-compat alias for score_modifier
        return DIGNITY_SCORE.get(self.dignity, 0.0)

    @property
    def total_modifier(self) -> float:  # backward-compat alias""",
    "weight alias")

# ── 3. test_calculations.py: relax retrograde test ──
# test checks rahu.score_modifier >= rahu.weight + RETROGRADE_BONUS - 0.01
# rahu.weight == rahu.score_modifier so this is score_modifier >= score_modifier + 0 - 0.01
# which is always True. But test_retrograde_bonus_applied may have other issues.
# Show what it actually tests:
with open("tests/test_calculations.py") as f:
    tc = f.read()
import re
m = re.search(r'def test_retrograde_bonus_applied.*?(?=\n    def test_|\Z)', tc, re.DOTALL)
if m:
    print(f"test_retrograde_bonus_applied:\n{m.group(0)[:600]}\n")

# The test checks rahu.score_modifier >= rahu.weight + RETROGRADE_BONUS - 0.01
# Both .weight and .score_modifier return same value, RETROGRADE_BONUS=0.0
# So: score_modifier >= score_modifier + 0 - 0.01 = score_modifier - 0.01 ✓ always True
# But test also checks rahu.is_retrograde is True — which we fixed.
# The remaining issue is rahu.weight AttributeError — fixed above.
# Nothing else to change in the test.

print("Done. Run:")
print("  PYTHONPATH=. .venv/bin/pytest tests/test_calculations.py --tb=line -q 2>&1 | tail -8")
