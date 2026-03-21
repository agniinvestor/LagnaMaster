#!/usr/bin/env python3
"""Run from ~/LagnaMaster: python3 fix_ruff.py"""
import os, subprocess, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# Run ruff to find the 3 errors
result = subprocess.run(
    [".venv/bin/ruff", "check", "src/", "tests/",
     "--select", "E,F,W", "--ignore", "E501,E402,E701,E702,F401"],
    capture_output=True, text=True
)
print("Ruff output:")
print(result.stdout)
print(result.stderr)

# Also try auto-fix for safe fixes
result2 = subprocess.run(
    [".venv/bin/ruff", "check", "src/", "tests/",
     "--select", "E,F,W", "--ignore", "E501,E402,E701,E702,F401", "--fix"],
    capture_output=True, text=True
)
print("After --fix:")
print(result2.stdout)
print(result2.stderr)

# Re-run to see remaining
result3 = subprocess.run(
    [".venv/bin/ruff", "check", "src/", "tests/",
     "--select", "E,F,W", "--ignore", "E501,E402,E701,E702,F401"],
    capture_output=True, text=True
)
print("Remaining:")
print(result3.stdout or "No errors!")
