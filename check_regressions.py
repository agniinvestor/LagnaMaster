#!/usr/bin/env python3
"""Run from ~/LagnaMaster: python3 check_regressions.py"""
import subprocess, os
os.chdir(os.path.expanduser("~/LagnaMaster")) if not os.path.isfile("requirements.txt") else None

result = subprocess.run(
    [".venv/bin/pytest", "--tb=line", "-q"],
    capture_output=True, text=True,
    env={**__import__("os").environ, "PYTHONPATH": "."}
)
out = result.stdout + result.stderr

# Show only FAILED lines and their immediate error
lines = out.split("\n")
failures = []
for i, l in enumerate(lines):
    if "FAILED" in l or "ImportError" in l or "AttributeError" in l:
        failures.append(l)

# Group by file
from collections import defaultdict
by_file = defaultdict(list)
for f in failures:
    parts = f.split("::")
    if len(parts) >= 2:
        by_file[parts[0].replace("FAILED ", "")].append("::".join(parts[1:]))
    else:
        by_file["other"].append(f)

print(f"Total failure lines: {len(failures)}\n")
for fname, tests in sorted(by_file.items()):
    print(f"{fname} ({len(tests)} failures)")
    for t in tests[:3]:
        print(f"    {t}")
    if len(tests) > 3:
        print(f"    ... and {len(tests)-3} more")
