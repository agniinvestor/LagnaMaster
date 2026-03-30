#!/usr/bin/env python3
"""Fix ruff errors from S161-170 build. Run from ~/LagnaMaster."""
import os, re
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# ── north_indian_chart.py ─────────────────────────────────────────────────────
with open("src/calculations/north_indian_chart.py") as f: s = f.read()
s = s.replace("        text_color = \"black\"\n        sign_color", "        sign_color")
s = s.replace("    row_idx = 0\n    col_idx = 0\n    for idx", "    for idx")
s = s.replace("text_c = \"black\"; stroke = \"black\"; text_c = \"black\"", "stroke = \"black\"")
# Fix text_c on the else line
s = re.sub(r"bg = \"white\"; stroke = \"black\"; text_c = \"black\"\n", 
           "bg = \"white\"; stroke = \"black\"\n", s)
# Remove semicolon from House cells line
s = s.replace("'<!-- House cells with sign numbers -->');", "'<!-- House cells with sign numbers -->')")
with open("src/calculations/north_indian_chart.py", "w") as f: f.write(s)
print("OK  north_indian_chart.py")

# ── kp_cuspal.py ──────────────────────────────────────────────────────────────
with open("src/calculations/kp_cuspal.py") as f: s = f.read()
# Remove unused supporting variable (3 lines)
s = re.sub(
    r"        supporting = KP_EVENT_HOUSES\.get\(\s*\{[^}]+\}\.get\(house, \"\"\), set\(\)\s*\)\s*\n",
    "", s
)
# Fix trailing whitespace on the compute_kp_significators call
s = s.replace("compute_kp_significators(entry.sub_lord, \n                  chart",
              "compute_kp_significators(entry.sub_lord,\n                  chart")
with open("src/calculations/kp_cuspal.py", "w") as f: f.write(s)
print("OK  kp_cuspal.py")

# ── pdf_export.py ─────────────────────────────────────────────────────────────
with open("src/pdf_export.py") as f: s = f.read()
# E741: rename l -> lbl
s = s.replace("for r, l in score_labels.items():", "for r, lbl in score_labels.items():")
s = s.replace("label = l; break", "label = lbl; break")
# F541: remove f prefix from string without placeholders
old = "f'<div style=\"page-break-after:always\"></div></body></html>'"
new =  "'<div style=\"page-break-after:always\"></div></body></html>'"
s = s.replace(old, new)
with open("src/pdf_export.py", "w") as f: f.write(s)
print("OK  pdf_export.py")

# ── regression_fixtures.py ────────────────────────────────────────────────────
with open("tests/fixtures/regression_fixtures.py") as f: s = f.read()
s = s.replace("    import json, os\n", "    import json\n    import os\n")
with open("tests/fixtures/regression_fixtures.py", "w") as f: f.write(s)
print("OK  regression_fixtures.py")

print("\nDone. Run:")
print("  .venv/bin/ruff check src/ tests/ --select E,F,W --ignore E501,E402,E701,E702,F401 2>&1 | tail -3")
print("  git add -A && git commit -m 'fix: ruff W291/F841/E703/E741/F541/E401 in S161-170 files' && git push")
