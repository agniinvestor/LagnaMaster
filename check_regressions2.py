#!/usr/bin/env python3
"""Run from ~/LagnaMaster: python3 check_regressions2.py"""
import subprocess, os
from collections import defaultdict

result = subprocess.run(
    [".venv/bin/pytest", "--tb=short", "-q", "--no-header"],
    capture_output=True, text=True,
    env={**os.environ, "PYTHONPATH": "."}
)
out = result.stdout + result.stderr

# Collect FAILED lines and the error line immediately after
lines = out.split("\n")
by_file = defaultdict(list)
errors_by_file = defaultdict(set)

for i, line in enumerate(lines):
    if line.startswith("FAILED "):
        test = line[7:].strip()
        file_part = test.split("::")[0]
        by_file[file_part].append(test)
    if line.startswith("ERROR "):
        file_part = line[6:].split("::")[0].strip()
        # get the error type from nearby lines
        for j in range(i, min(i+5, len(lines))):
            if "Error" in lines[j] or "Import" in lines[j]:
                errors_by_file[file_part].add(lines[j].strip()[:100])

print("=== FAILURES BY FILE ===")
for f, tests in sorted(by_file.items()):
    print(f"\n{f} ({len(tests)} failures):")
    for t in tests[:2]:
        print(f"  {t}")
    if len(tests) > 2:
        print(f"  ... +{len(tests)-2} more")

print("\n=== ERRORS BY FILE ===")
for f, errs in sorted(errors_by_file.items()):
    print(f"\n{f}:")
    for e in list(errs)[:2]:
        print(f"  {e}")

# Also show first 3 short tracebacks
print("\n=== FIRST 3 TRACEBACKS ===")
tb_count = 0
in_tb = False
tb_lines = []
for line in lines:
    if line.startswith("_____") or line.startswith("ERROR "):
        if tb_lines and tb_count < 3:
            print("\n".join(tb_lines[-8:]))
            print()
            tb_count += 1
        tb_lines = [line]
        in_tb = True
    elif in_tb:
        tb_lines.append(line)
