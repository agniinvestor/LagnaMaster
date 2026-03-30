#!/usr/bin/env python3
"""Run from ~/LagnaMaster: python3 fix_av_and_lint.py"""
import os, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# Fix 1: ashtakavarga.py strength() — use self.bindus with correct thresholds
with open("src/calculations/ashtakavarga.py") as f: src = f.read()
# Replace any variant of strength() that uses raw_bindus OR wrong thresholds
src = re.sub(
    r'def strength\(self, sign_index: int\) -> str:\s*b = .*?\n(\s*if b >= 5.*?return "Weak")',
    lambda m: 'def strength(self, sign_index: int) -> str:\n        b = self.bindus[sign_index % 12]\n        if b >= 5: return "Strong"\n        if b == 4: return "Average"\n        return "Weak"',
    src, flags=re.DOTALL
)
with open("src/calculations/ashtakavarga.py", "w") as f: f.write(src)
print("OK  ashtakavarga.py strength() uses self.bindus with 5/4 thresholds")

# Fix 2: planet_avasthas.py — remove unused `summary` variable
with open("src/calculations/planet_avasthas.py") as f: src = f.read()
# The `summary` variable in compute_avasthas is assigned but never used after
src = src.replace(
    '    summary = f"{bala.value} ({bala_avastha.__doc__.split(chr(10))[0].strip()[:20]})"',
    '    # summary removed (Ruff F841 — unused variable)'
)
with open("src/calculations/planet_avasthas.py", "w") as f: f.write(src)
print("OK  planet_avasthas.py removed unused summary variable")

print("\nRun: PYTHONPATH=. .venv/bin/pytest tests/test_ashtakavarga.py -q 2>&1 | tail -4")
