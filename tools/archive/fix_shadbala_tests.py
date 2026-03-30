#!/usr/bin/env python3
"""Fix shadbala test methods. Run from ~/LagnaMaster: python3 fix_shadbala_tests.py"""
import os, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

with open("tests/test_calculations.py") as f:
    src = f.read()

# Add _sb helper to TestShadbala class
src = src.replace(
    "class TestShadbala:",
    "class TestShadbala:\n"
    "    @staticmethod\n"
    "    def _sb(chart):\n"
    "        from src.calculations.shadbala import compute_shadbala_legacy as _cs\n"
    "        return _cs(chart)\n"
)

# Replace bare compute_shadbala(india_chart) with self._sb(india_chart)
# but NOT the import line itself
lines = src.split("\n")
new_lines = []
for line in lines:
    if "compute_shadbala(india_chart)" in line and "import" not in line and "def _sb" not in line:
        line = line.replace("compute_shadbala(india_chart)", "self._sb(india_chart)")
    new_lines.append(line)
src = "\n".join(new_lines)

# Also fix dignity tests - same pattern
src = src.replace(
    "class TestDignity:",
    "class TestDignity:\n"
    "    @staticmethod\n"
    "    def _dig(planet, **kw):\n"
    "        from src.calculations.dignity import compute_dignity_legacy as _cd\n"
    "        return _cd(planet, **kw)\n"
)
lines = src.split("\n")
new_lines = []
for line in lines:
    if "compute_dignity(" in line and "import" not in line and "def _dig" not in line and "result =" in line:
        line = line.replace("compute_dignity(", "self._dig(")
    new_lines.append(line)
src = "\n".join(new_lines)

import ast
try:
    ast.parse(src)
    with open("tests/test_calculations.py", "w") as f:
        f.write(src)
    print("OK  tests/test_calculations.py fixed")
except SyntaxError as e:
    print(f"SYNTAX ERROR line {e.lineno}: {src.split(chr(10))[e.lineno-1]}")

print("\nRun: PYTHONPATH=. .venv/bin/pytest tests/test_calculations.py -q 2>&1 | tail -4")
