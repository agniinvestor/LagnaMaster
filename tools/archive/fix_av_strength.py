#!/usr/bin/env python3
"""Fix AV strength method. Run from ~/LagnaMaster: python3 fix_av_strength.py"""
import os
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

with open("src/calculations/ashtakavarga.py") as f:
    src = f.read()

# strength() uses self.bindus — must use self.raw_bindus so ratings match pre-Shodhana values
old = '''    def strength(self, sign_index: int) -> str:
        b = self.bindu_for_sign(sign_index)
        if b >= 5: return "Strong"
        if b == 4: return "Average"
        return "Weak"'''

new = '''    def strength(self, sign_index: int) -> str:
        b = self.raw_bindus[sign_index % 12]
        if b >= 5: return "Strong"
        if b == 4: return "Average"
        return "Weak"'''

if old in src:
    src = src.replace(old, new, 1)
    with open("src/calculations/ashtakavarga.py", "w") as f:
        f.write(src)
    print("OK  strength() now uses raw_bindus")
else:
    # Try alternate form
    old2 = '        if b >= 5: return "Strong"\n        if b >= 3: return "Average"\n        return "Weak"'
    new2 = '        if b >= 5: return "Strong"\n        if b == 4: return "Average"\n        return "Weak"'
    if old2 in src:
        # Also fix the bindu source
        src = src.replace(
            'def strength(self, sign_index: int) -> str:\n        b = self.bindu_for_sign(sign_index)',
            'def strength(self, sign_index: int) -> str:\n        b = self.raw_bindus[sign_index % 12]'
        )
        src = src.replace(old2, new2)
        with open("src/calculations/ashtakavarga.py", "w") as f:
            f.write(src)
        print("OK  strength() fixed (alternate form)")
    else:
        # Find and show whatever is there
        import re
        m = re.search(r'def strength.*?return "Weak"', src, re.DOTALL)
        if m:
            print(f"Current strength method:\n{m.group(0)}")
            # Blanket replace: any bindu source -> raw_bindus, thresholds -> 5/4
            fixed = re.sub(
                r'(def strength\(self, sign_index: int\) -> str:)\s*b = .*?\n(.*?if b >= \d)',
                r'\1\n        b = self.raw_bindus[sign_index % 12]\n\2',
                src, flags=re.DOTALL
            )
            # Fix thresholds
            fixed = re.sub(r'if b >= 5:', 'if b >= 5:', fixed)
            fixed = re.sub(r'if b >= [34]:', 'if b == 4:', fixed)
            with open("src/calculations/ashtakavarga.py", "w") as f:
                f.write(fixed)
            print("OK  strength() fixed via regex")

print("Run: PYTHONPATH=. .venv/bin/pytest tests/test_ashtakavarga.py -q 2>&1 | tail -4")
