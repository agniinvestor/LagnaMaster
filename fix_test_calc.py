#!/usr/bin/env python3
"""Fix test_calculations.py import syntax. Run from ~/LagnaMaster."""
import os, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

with open("tests/test_calculations.py") as f:
    src = f.read()

print("Current dignity imports:")
for i, line in enumerate(src.split("\n")):
    if "compute_dignity" in line or "DignityLevel" in line:
        print(f"  {i+1}: {line}")

# Fix: replace all `from ... import compute_dignity_legacy as compute_dignity`
# back to a clean import block that works
src = re.sub(
    r'from src\.calculations\.dignity import compute_dignity_legacy as compute_dignity\b',
    'from src.calculations.dignity import compute_dignity_legacy as compute_dignity  # noqa',
    src
)

# If there are duplicate dignity imports, consolidate
# Find all dignity import lines
dignity_imports = [(i, l) for i, l in enumerate(src.split("\n"))
                   if "from src.calculations.dignity import" in l]
print(f"\nDignity import lines: {len(dignity_imports)}")
for i, l in dignity_imports:
    print(f"  {i+1}: {l}")

# If duplicate compute_dignity imports exist, keep only the legacy one
lines = src.split("\n")
seen_compute_dignity = False
new_lines = []
for line in lines:
    if "from src.calculations.dignity import" in line and "compute_dignity" in line:
        if seen_compute_dignity:
            print(f"  Removing duplicate: {line.strip()}")
            continue
        seen_compute_dignity = True
    new_lines.append(line)

src = "\n".join(new_lines)

# Also fix shadbala similar issue
src = re.sub(
    r'from src\.calculations\.shadbala import compute_shadbala_legacy as compute_shadbala\b',
    'from src.calculations.shadbala import compute_shadbala_legacy as compute_shadbala  # noqa',
    src
)
seen_shadbala = False
new_lines = []
for line in src.split("\n"):
    if "from src.calculations.shadbala import" in line and "compute_shadbala" in line:
        if seen_shadbala:
            continue
        seen_shadbala = True
    new_lines.append(line)
src = "\n".join(new_lines)

with open("tests/test_calculations.py", "w") as f:
    f.write(src)

# Verify syntax
import ast
try:
    ast.parse(src)
    print("\n  OK  test_calculations.py syntax valid")
except SyntaxError as e:
    print(f"\n  SYNTAX ERROR: {e}")
    # Find the problematic lines
    lines = src.split("\n")
    start = max(0, e.lineno - 3)
    end = min(len(lines), e.lineno + 3)
    for i, l in enumerate(lines[start:end], start+1):
        print(f"  {i}: {l}")

print("\nRun: PYTHONPATH=. .venv/bin/pytest tests/test_calculations.py -q 2>&1 | tail -4")
