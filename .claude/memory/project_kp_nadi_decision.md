---
name: KP/Nadi/Lal Kitab Phase 1B decision
description: KP Comprehensive, Nadi texts, and Lal Kitab will be re-encoded in Phase 1B with school_specific fields
type: project
---

KP Comprehensive (~300 rules), Bhrigu/Suka/Dhruva Nadi (~240 rules), and Lal Kitab (~150 rules) will be re-encoded at Phase 1B depth during the Phase 1A re-encode cycle.

**Why:** These are separate school systems that need the `school_specific` dict on RuleRecord (added S305). KP needs sublord/significator/cusp fields. Nadi needs nadi_sequence. Lal Kitab needs house_position (not sign-based) and remedy fields.

**How to apply:** Schedule after primary Parashari texts are re-encoded (BPHS, Brihat Jataka, Phaladeepika). Use school_specific dict for non-Parashari fields rather than extending RuleRecord further.
