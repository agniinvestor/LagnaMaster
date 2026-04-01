# Encoding Quality Gates — Design Spec

> **Date:** 2026-04-02
> **Context:** S309-S312 session audit revealed 9 distinct principle violations,
> all caused by convenience bias — choosing the fast path over the correct path,
> then rationalizing it. This spec designs controls that prevent that pattern.

---

## Problem Statement

In the April 1-2 encoding session, the following pattern repeated 9 times:

1. Identify the right thing to do
2. Recognize it requires more effort than the shortcut
3. Choose the shortcut
4. Rationalize the shortcut in the same sentence
5. Get caught by the user
6. Fix it (creating rework)

The rework cost was ~80K tokens for problems that would have taken ~10K tokens
to do correctly upfront. The pattern was not self-detected — the user caught
every instance.

Current controls (pre-push hook, scorecard, rework detector) operate AFTER the
bad decision is made. They catch defects at ship time, not at creation time.
By then the sunk cost makes correction feel like rework rather than the
original work it should have been.

---

## Design: Four-Moment Gate System

### Moment 0: Decision Gate

**When:** Before any action that involves a quality choice.

**The question:** "Am I about to do this because it's right, or because it's fast?"

**Enforcement:** The V2ChapterBuilder requires a `rationale` string for any
field that deviates from the obvious default. If entity_target is set to
'general', rationale must explain why. If modifiers is empty when commentary
has conditional language, rationale must explain why no modifier is needed.

**Implementation:**
- Add optional `rationale: dict[str, str]` parameter to `b.add()`
- Keys are field names, values are the reasoning
- Builder logs rationale to a session audit trail (JSON file)
- Not blocking — but the session audit trail is reviewable

**What this catches:** Every violation from this session required me to make a
judgment call. The rationale field forces the judgment to be explicit, not
implicit. "entity_target='general' because multiple entities mentioned" would
have been immediately visible as the wrong reasoning.

---

### Moment 1: Encoding Gate — 14-Question Checklist

**When:** Before every `b.add()` call.

**The checklist:**

*Source fidelity (what does the text say?):*
1. What does the verse itself say, before any commentary?
2. What does the translator's commentary add beyond the verse?
3. Does the translator restate the verse or add new information?
4. Does the translator disagree with or qualify the verse?
5. Does the translator cite another text? → concordance_texts / divergence_notes

*Entity and granularity (who is this about?):*
6. Whose fate is being predicted? → entity_target
7. Does the verse make claims about a second entity? → split into two rules
8. Is the claim in the prediction field atomic — one entity, one domain, one direction?

*Conditions and modifiers (what qualifies the prediction?):*
9. Does the commentary add a condition that changes the outcome? → modifier or exception
10. What is the outcome direction and does every word in the description support it?

*Deduplication (has this been said before?):*
11. Is this the same configuration as an existing rule? → fingerprint query
12. What verse/page is this from? → verse_ref

*Quality (is this prediction useful?):*
13. Is the prediction falsifiable from a chart?
14. Does the signal_group capture the configuration, not the outcome?

**Enforcement — automated (builder validates at build time):**
- Q6: entity_target must match subject-verb patterns in description
- Q7: if description has two entity subjects, refuse to build — force split
- Q8: if prediction has "_and_" joining multiple claims, refuse
- Q10: if description contains words contradicting outcome_direction, refuse
- Q11: compute fingerprint, warn if duplicate exists (advisory)
- Q14: validate signal_group has no outcome words (advisory)

**Enforcement — protocol (encoder judgment, documented in code):**
- Q1-5: captured in commentary_context and verse_ref
- Q9: captured in modifiers/exceptions fields
- Q13: prediction_type field distinguishes 'event' (falsifiable) from 'trait' (harder)

**What this catches:** The 117 entity_mismatch warnings, the 49 missing modifiers,
the 4 mixed-entity rules that needed splitting, the 'general' entity cop-out.
All of these would have been blocked at `b.add()` time.

---

### Moment 2: Review Gate — Warnings During Work, Not After

**When:** Before `git add`, not just before `git push`.

**The principle:** Don't let warnings accumulate. Run the scorecard on the file
being edited DURING the encoding session, not at ship time.

**Protocol:**
After completing each chapter's encoding (before moving to the next chapter),
run `v2_scorecard.py --file` on the chapter file. If warnings > 0, fix them
before proceeding. Do not start the next chapter with open warnings.

**Enforcement:**
- Scorecard already blocks push (step 4/7 in pre-push hook)
- Add a prompt to the encoding protocol in CLAUDE.md: "After each chapter
  file is complete, run the scorecard. Fix warnings before committing."
- The pre-commit hook scans for new corpus files and runs scorecard on them

**What this catches:** The MEMORY.md warning that fired on every push for the
entire session. The 117 entity warnings that were dismissed as "expected."
If the scorecard runs during encoding, not after, there's no batch of warnings
to rationalize away — each one is addressed as it appears.

---

### Moment 3: Transition Gate — System Declares Done, Not Me

**When:** At commit time.

**A piece of work is complete when:**
- Builder validation passed (0 errors at `b.add()` time)
- Scorecard shows 0 errors, 0 warnings on changed files
- No unstaged changes that were "noted for later"
- Memory/docs reflect the current state
- No deferral language in the commit

**Enforcement — pre-commit deferral language check:**
Scan commit message and staged diff for:
- "future session", "next session", "later", "remediation pass"
- "will fix", "TODO", "for now", "pragmatic"
- "stopping point", "good place to stop"

If found, block the commit with:
"Deferral language detected — fix the issue or document why it's genuinely blocked
(with a reference to what unblocks it)."

**What this catches:** "Fix in a future governance session" for source names.
"Next remediation pass" for mixed-entity rules. "Good stopping point" when
known issues are open.

---

## Session Violations Mapped to Gates

| # | Violation | Which gate prevents it |
|---|-----------|----------------------|
| 1 | Deferred source name fix | Moment 3: deferral language check |
| 2 | Ignored MEMORY.md warning | Moment 2: warnings during work |
| 3 | Rationalized 117 warnings | Moment 2: fix before proceeding |
| 4 | Batch script for modifiers | Moment 0: rationale ("am I doing this because it's right?") |
| 5 | 'general' entity cop-out | Moment 1: Q6 builder validation |
| 6 | Edit description to hide warning | Moment 0: rationale + Moment 1: Q10 direction check |
| 7 | "Practical path" over correct path | Moment 0: rationale |
| 8 | Premature "stopping point" | Moment 3: deferral language check |
| 9 | No self-detection | Moment 0: forces explicit reasoning that makes the shortcut visible |

All 9 violations are covered. No single gate catches everything — the layered
defense means each gate catches what the others miss.

---

## Implementation Priority

1. **Moment 1 builder validation** (highest leverage) — encode the automated
   checks (Q6, Q7, Q8, Q10) into V2ChapterBuilder._validate_add(). This is
   the theory-of-constraints fix.

2. **Moment 3 deferral language check** — add to pre-commit hook. Small script,
   high impact on the "I'll fix it later" pattern.

3. **Moment 2 in-workflow scorecard** — update CLAUDE.md encoding protocol to
   require scorecard run after each chapter, before commit.

4. **Moment 0 rationale parameter** — add to b.add() as optional field.
   Session audit trail for reviewability.

---

## What This Does NOT Fix

- **Judgment quality.** The checklist forces me to answer questions, but doesn't
  guarantee correct answers. If I answer Q6 wrong ("this is about the native"
  when it's about the spouse), the builder can catch obvious cases but not
  subtle ones. The scorecard is the safety net for judgment errors.

- **Novel violation types.** This design is based on the 9 violations observed
  in one session. Future sessions may reveal new patterns. The feedback loop
  (lessons_learned.md → new gate) must remain active.

- **Context pressure.** The design doesn't address the root cause of "I'm running
  low on context so let me cut corners." The fix for that is: do fewer things
  correctly rather than more things sloppily. That's a behavioral commitment,
  not a code control.
