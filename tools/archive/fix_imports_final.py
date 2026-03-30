#!/usr/bin/env python3
"""Fix double-as import chains. Run from ~/LagnaMaster: python3 fix_imports_final.py"""
import os, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

with open("tests/test_calculations.py") as f:
    src = f.read()

# Fix all double-as patterns like: import X as X as Y  ->  import X as Y
src = re.sub(
    r'from ([\w.]+) import (\w+)(?: as \2)+ as (\w+)',
    r'from \1 import \2 as \3',
    src
)
# Fix: import X as X as X  (same name triple)
src = re.sub(
    r'from ([\w.]+) import (\w+)(?: as \2)+',
    r'from \1 import \2',
    src
)

import ast
try:
    ast.parse(src)
    with open("tests/test_calculations.py", "w") as f:
        f.write(src)
    print("OK  test_calculations.py — all double-as chains fixed, syntax valid")
except SyntaxError as e:
    print(f"STILL BROKEN line {e.lineno}: {src.split(chr(10))[e.lineno-1]}")

print("\nRun: PYTHONPATH=. .venv/bin/pytest --tb=line -q --ignore=tests/test_session21.py --ignore=tests/test_varga.py 2>&1 | tail -6")
