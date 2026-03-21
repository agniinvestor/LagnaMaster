#!/usr/bin/env python3
"""fixup3 — final two fixes. Run: python3 fixup3_phases.py"""
import os, sys

BASE = os.getcwd()
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); sys.exit(1)

print("Applying fixup3...\n")

# ── Read dignity.py and show the relevant section ──
with open("src/calculations/dignity.py") as f:
    lines = f.readlines()

# Find _get_dignity_level and print lines around it
for i, line in enumerate(lines):
    if "_get_dignity_level" in line and "def " in line:
        print(f"Found _get_dignity_level at line {i+1}")
        print("Lines {}-{}:".format(i+1, i+30))
        for j, l in enumerate(lines[i:i+30], i+1):
            print(f"  {j}: {l}", end="")
        break
