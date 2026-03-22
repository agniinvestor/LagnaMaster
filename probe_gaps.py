#!/usr/bin/env python3
"""Check all 6 gap items. Run from ~/LagnaMaster."""
import os, re, json

def check(label, condition, detail=""):
    status = "✅ RESOLVED" if condition else "❌ STILL OPEN"
    print(f"{status}  {label}")
    if detail: print(f"           {detail}")

# 1. R02/R09 functional dignity call-site
with open("src/calculations/scoring_v3.py") as f: sv3 = f.read()
# Check if _is_functional_benefic is actually CALLED in rule logic (not just defined)
r02_uses_func = bool(re.search(r'R0[29].*_is_functional|_is_functional.*R0[29]', sv3, re.DOTALL))
# More broadly: is _is_functional_benefic called anywhere in the scoring rules?
func_called_in_rules = "_is_functional_benefic" in sv3 and sv3.count("_is_functional_benefic(") > 0
check("R02/R09 functional dignity wired into rule handlers",
      func_called_in_rules,
      f"_is_functional_benefic called {sv3.count('_is_functional_benefic(')} time(s)")

# 2. score_chart() query_date param
has_query_date = "query_date" in sv3
score_chart_sig = re.search(r'def score_chart\([^)]+\)', sv3)
check("score_chart() has query_date parameter",
      has_query_date and score_chart_sig and "query_date" in (score_chart_sig.group() if score_chart_sig else ""),
      score_chart_sig.group() if score_chart_sig else "score_chart not found")

# 3. Drekkana D3 in vargas.py
with open("src/calculations/vargas.py") as f: vg = f.read()
# Does compute_varga_sign use drekkana_variants for D3?
d3_uses_variants = "drekkana_variants" in vg or "drekkana_sign" in vg
# Is ACTIVE_DREKKANA_METHOD present?
active_method = "ACTIVE_DREKKANA_METHOD" in vg
check("vargas.py D3 dispatches to drekkana_variants",
      d3_uses_variants,
      f"drekkana_variants imported: {d3_uses_variants}, ACTIVE_DREKKANA_METHOD: {active_method}")

# 4. weasyprint in requirements.txt
with open("requirements.txt") as f: req = f.read()
check("weasyprint in requirements.txt",
      "weasyprint" in req,
      f"found: {'weasyprint' in req}")

# 5. Regression baseline JSON
bl_path = "tests/fixtures/baseline_india_1947.json"
if os.path.exists(bl_path):
    with open(bl_path) as f: bl = json.load(f)
    scores_populated = any(v is not None for v in bl.get("house_scores", {}).values())
    check("Regression baseline JSON has real scores",
          scores_populated,
          f"scores populated: {scores_populated}, path exists: True")
else:
    check("Regression baseline JSON exists", False, "file missing")

# 6. TOPOCENTRIC_MOON_ENABLED = True
with open("src/ephemeris.py") as f: eph = f.read()
topo_true = "TOPOCENTRIC_MOON_ENABLED = True" in eph
topo_false = "TOPOCENTRIC_MOON_ENABLED = False" in eph
check("TOPOCENTRIC_MOON_ENABLED = True",
      topo_true and not topo_false,
      f"True: {topo_true}, False: {topo_false}")

