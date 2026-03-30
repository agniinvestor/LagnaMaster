---
name: Continuous ML integration — measure as you build
description: Every corpus batch must wire into scoring and get measured before the next batch. No waterfall.
type: feedback
---

Follow Option C: continuous integration of corpus into ML measurement.

Every corpus encoding batch must:
1. Wire new rules into a rule-firing function that evaluates them against charts
2. Run the rule-fire features through the existing feature pipeline
3. Measure whether the new rules add predictive signal (correlation with ADB outcomes)
4. Only proceed to next batch after confirming the current batch adds value

**Why:** The waterfall plan (encode 20,000 rules, THEN measure) risks discovering at S700 that corpus rules don't add predictive value. Measuring incrementally catches this early and lets us adjust granularity, grain, or approach.

**How to apply:**
- Build a `rule_firing.py` module that takes a chart + corpus and returns which rules fire
- Add corpus-match features to `feature_decomp.py` alongside the existing 156 features
- Run OB-3 baseline before each new text encoding begins
- Track r-value change per batch in KPIS.md
