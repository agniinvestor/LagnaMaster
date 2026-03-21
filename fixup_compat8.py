#!/usr/bin/env python3
"""Compat8. Run from ~/LagnaMaster: python3 fixup_compat8.py"""
import os
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# Fix NAKSHATRAS_FULL: third element must be is_ganda_mool bool, not span
with open("src/calculations/nakshatra.py") as f:
    src = f.read()

old = 'NAKSHATRAS_FULL = [(NAKSHATRA_NAMES[i], NAKSHATRA_LORDS[i], _NAK_WIDTH) for i in range(27)]'
new = 'NAKSHATRAS_FULL = [(NAKSHATRA_NAMES[i], NAKSHATRA_LORDS[i], NAKSHATRA_NAMES[i] in GANDA_MOOL) for i in range(27)]'

if old in src:
    with open("src/calculations/nakshatra.py", "w") as f:
        f.write(src.replace(old, new, 1))
    print("  OK  NAKSHATRAS_FULL third element = is_ganda_mool bool")
else:
    print("  SKIP — pattern not found")

# Also check test expected set — it includes Shatabhisha which is NOT classical Ganda Mool
# Classical GANDA_MOOL per BPHS = junction of nakshatra and rashi = Ashwini/Ashlesha/Magha/Jyeshtha/Mula/Revati
# Update test to match our GANDA_MOOL constant exactly
with open("tests/test_calculations.py") as f:
    tc = f.read()

tc = tc.replace(
    '{"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula",\n                    "Shatabhisha", "Revati"}',
    '{"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}'
)
tc = tc.replace(
    '{"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Shatabhisha", "Revati"}',
    '{"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}'
)

with open("tests/test_calculations.py", "w") as f:
    f.write(tc)
print("  OK  test expected set = 6 classical Ganda Mool nakshatras")

print("\nRun: PYTHONPATH=. .venv/bin/pytest tests/test_calculations.py -q 2>&1 | tail -4")
