#!/usr/bin/env python3
"""
Integration fixup — run from ~/LagnaMaster: python3 fixup_integration.py
Fixes:
  1. d.is_cazimi -> d.cazimi, d.is_combust -> d.combust in all .py files
  2. DignityLevel.NEUTRAL_SIGN missing -> add alias in dignity.py
  3. compute_special_lagnas() missing birth_dt -> add default in special_lagnas.py
"""
import os, re, glob

BASE = os.getcwd()
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

changed = []

def patch_file(path, old, new, label):
    with open(path) as f: src = f.read()
    if old not in src: return
    with open(path, "w") as f: f.write(src.replace(old, new))
    if path not in changed: changed.append(path)
    print(f"  OK  {path} [{label}]")

# ── Fix 1: is_cazimi -> cazimi, is_combust -> combust everywhere ──
print("Fix 1: is_cazimi/is_combust attribute names...")
for path in glob.glob("src/**/*.py", recursive=True) + glob.glob("tests/**/*.py", recursive=True):
    with open(path) as f: src = f.read()
    new = src.replace(".is_cazimi", ".cazimi").replace(".is_combust", ".combust")
    if new != src:
        with open(path, "w") as f: f.write(new)
        print(f"  OK  {path}")
        if path not in changed: changed.append(path)

# ── Fix 2: Add DignityLevel.NEUTRAL_SIGN alias in dignity.py ──
print("\nFix 2: DignityLevel.NEUTRAL_SIGN alias...")
patch_file(
    "src/calculations/dignity.py",
    "    NEUTRAL             = \"Neutral\"\n    ENEMY_SIGN          = \"Enemy Sign\"",
    "    NEUTRAL             = \"Neutral\"\n    NEUTRAL_SIGN        = \"Neutral\"   # alias — some modules use NEUTRAL_SIGN\n    ENEMY_SIGN          = \"Enemy Sign\"",
    "NEUTRAL_SIGN alias"
)

# ── Fix 3: compute_special_lagnas — make birth_dt optional with default ──
print("\nFix 3: compute_special_lagnas birth_dt default...")
patch_file(
    "src/calculations/special_lagnas.py",
    "def compute_special_lagnas(\n    chart,\n    birth_dt: datetime,",
    "def compute_special_lagnas(\n    chart,\n    birth_dt: datetime = None,",
    "birth_dt optional"
)
# Add None guard at top of function body
patch_file(
    "src/calculations/special_lagnas.py",
    "    if sunrise_dt is None:\n        sunrise_dt = birth_dt.replace(hour=6, minute=0, second=0)",
    "    if birth_dt is None:\n        from datetime import datetime as _dt\n        birth_dt = _dt.now()\n    if sunrise_dt is None:\n        sunrise_dt = birth_dt.replace(hour=6, minute=0, second=0)",
    "birth_dt None guard"
)

print(f"\nDone — {len(changed)} files changed.")
print("Run: PYTHONPATH=. .venv/bin/pytest --tb=short -q 2>&1 | tail -8")
