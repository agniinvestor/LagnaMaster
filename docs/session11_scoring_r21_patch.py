"""
R21 patch for src/scoring.py — Session 11

1. Add import near top:
   from src.calculations.pushkara_navamsha import is_pushkara_navamsha

2. Replace R21 stub block:
   # R21 — Pushkara Navamsha (deferred — stub)
   rules.append(RuleResult(rule="R21", description="Bhavesh in Pushkara Navamsha",
       score=0.0, is_wc=False, triggered=False))

   WITH:
   _bhavesh_pos = chart.planets.get(bhavesh)
   _r21_triggered = (
       _bhavesh_pos is not None
       and is_pushkara_navamsha(_bhavesh_pos.sign_index, _bhavesh_pos.degree_in_sign)
   )
   rules.append(RuleResult(rule="R21", description="Bhavesh in Pushkara Navamsha",
       score=0.5 if _r21_triggered else 0.0, is_wc=False, triggered=_r21_triggered))
"""
