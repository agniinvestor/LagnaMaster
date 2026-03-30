---
name: Depth over throughput — no rework
description: Optimize for thorough depth and zero rework, not session count. Poor depth + rework costs more tokens than doing it right once.
type: feedback
---

The objective is THOROUGH DEPTH with ZERO REWORK, not maximizing session throughput.

**Why:** High throughput with poor depth has repeatedly caused rework:
- 36 sessions of corpus rules with no concordance → backfill needed
- 36 sessions with 3/5 docs skipped → backfill needed
- Entire corpus disconnected from scoring engine → future rework
- Rule counts artificially capped to 130 → rules had to be re-expanded
Each rework cycle costs more tokens than doing it correctly once.

**How to apply:**
1. Before starting ANY batch of work, verify the full protocol checklist is being followed
2. Every corpus module must wire into scoring measurement, not just sit as data
3. Every session must update ALL 5 docs, run concordance, validate contract
4. Never skip a protocol step to move faster — the "speed" is illusory
5. If a process step seems slow, build automation for it, don't skip it
6. When in doubt about depth, do MORE not less — undercounting is the recurring failure mode
