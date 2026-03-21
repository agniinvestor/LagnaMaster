#!/usr/bin/env python3
"""fixup7. Run from ~/LagnaMaster: python3 fixup7_phases.py"""
import os
with open("tests/test_phase0.py") as f:
    lines = f.readlines()

# Show lines 100-125 so we know exactly what's there
print("Lines 100-125:")
for i, l in enumerate(lines[99:125], 100):
    print(f"{i}: {l}", end="")
