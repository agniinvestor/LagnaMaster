---
name: Exhaustiveness over round numbers
description: Never trim corpus rules to hit a target count — encode every sutra-level rule the text contains
type: feedback
---

Do NOT constrain rule counts to round numbers (e.g., 130 per session). Encode every discrete rule the text contains at sutra-level depth. If a session produces 142 rules, that's 142 rules. The session boundary is a convenience for commit granularity, not a cap on content.

**Why:** The entire Phase 1B scope correction was driven by discovering we were undercounting by 10x. Trimming rules to fit a neat number is the exact same mistake — thematic-summary counting instead of sutra-level counting. The user explicitly called this out as redoing our own work.

**How to apply:** When building corpus modules, let the text dictate the rule count. Update coverage map estimates to actuals after encoding. Never delete valid rules to hit a target. If a chapter produces more rules than estimated, that's a better estimate, not an error.
