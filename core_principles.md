# Core Principles

> Read this at the START of every session. These are non-negotiable.
> Each one was tested in practice and proven necessary.

---

## The 10 Principles (from CLAUDE.md, validated in session)

1. **Long-term over quick** — evaluate every decision against the 1000+ session roadmap, not this session
2. **Nullify rework** — build controls BEFORE doing work. If a quality dimension exists, the gate must exist before encoding starts
3. **Right over easy** — always choose correct over convenient, even at 10x the effort. No shortcuts. No fake automation. *Validated: the "shortcut-driven path" cost 5-8x more in tokens than doing it right (L007)*
4. **Controls before work** — governance framework, validation, quality gates must exist BEFORE the work they govern
5. **Measure before claiming** — run the audit, run the scorecard, show the numbers. Never assume it passes. *Validated: 117 warnings assumed "expected" were genuine defects (L002)*
6. **System enforces, not person** — if a standard matters, it's a code check. Markdown protocols are documentation; code is enforcement. *Validated: self-detection failed 9/9 times; builder gates catch what I miss (L010)*
7. **Radical transparency** — when something is wrong, uncertain, or incomplete, say so immediately. Don't hide problems, optimise reporting, or hope issues self-resolve
8. **Source fidelity** — record what the text says, not what you think it means. Interpretation goes in commentary, never in predictions or structured fields. *Validated: regex-extracted modifiers are not source fidelity (L003)*
9. **Exhaust the problem before proposing** — when analysing gaps, designing controls, or planning work, assume your first pass is incomplete. Push yourself to find what you're missing before presenting
10. **Close the feedback loop** — when a mistake happens, it must flow through: Pattern → Lesson → Principle update → Control built → Governance framework updated. A lesson without a corresponding control is an open loop

---

## Encoding-Specific Principles (added from S309-S312 session)

11. **Fix now, not later** — when a fixable problem is identified, fix it in the current session. "Future governance session" is deferral. The cost of deferring is always higher than the cost of fixing. *(L001)*

12. **Warnings are defects** — a warning is a defect until proven otherwise. The burden of proof is on dismissal, not on action. Never rationalize a warning as "expected." *(L002)*

13. **One entity, one prediction, one rule** — if a verse predicts something about two different entities, it becomes two rules. 'General' is not a default. The decision rule: "whose life would I examine to verify this prediction?" *(L004, L005)*

14. **Never weaken controls** — when a gate blocks your work, fix the content, not the gate. If the gate has a genuine false positive, that modification is a separate deliberate commit. *(L006)*

15. **The user manages sessions and tokens** — don't propose stopping, don't cite context pressure, don't suggest deferring to a later conversation. Do the work. Let the user decide when to stop. *(L008, L009)*

---

## The 14-Question Encoding Checklist

Before every `b.add()` call:

*Source fidelity:*
1. What does the verse itself say, before any commentary?
2. What does the translator's commentary add beyond the verse?
3. Does the translator restate the verse or add new information?
4. Does the translator disagree with or qualify the verse?
5. Does the translator cite another text? → concordance_texts / divergence_notes

*Entity and granularity:*
6. Whose fate is being predicted? → entity_target
7. Does the verse make claims about a second entity? → split into two rules
8. Is the claim in the prediction field atomic — one entity, one domain, one direction?

*Conditions and modifiers:*
9. Does the commentary add a condition that changes the outcome? → modifier or exception
10. What is the outcome direction and does every word in the description support it?

*Deduplication:*
11. Is this the same configuration as an existing rule? → fingerprint query
12. What verse/page is this from? → verse_ref

*Quality:*
13. Is the prediction falsifiable from a chart?
14. Does the signal_group capture the configuration, not the outcome?

---

## Active Build-Time Gates (V2ChapterBuilder)

| Gate | What it catches | Added |
|------|----------------|-------|
| T1-1 | Invalid condition primitives | Pre-S309 |
| T1-2 | Invalid taxonomy values (domains, direction, intensity) | Pre-S309 |
| T1-3 | Non-canonical planet names | Pre-S309 |
| T1-13 | Generic/short prediction claims | Pre-S309 |
| T1-14 | entity_target vs description subject-verb mismatch | S312 |
| T1-15 | Two entity subjects in one rule → force split | S312 |
| T1-16 | Bundled prediction claims (>60 chars with _and_) | S312 |
| T1-17 | Prediction entity doesn't match entity_target | S312 |
| T1-18 | Invalid modifier effect or too-short condition (<15 chars) | S312 |

---

## Active Hooks

**Pre-commit (Moment 3):**
- Deferral language detection in staged diffs
- Scorecard on staged corpus files

**Pre-push (7 steps):**
1. Full test suite (7,364+ tests)
2. Ruff lint (0 errors)
3. Docs currency (MEMORY.md test count matches live)
4. V2 scorecard on changed corpus files (0 warnings)
5. Rework & lesson detection
6. Corpus maturity dashboard (L0-L5)
7. Doc completeness checks
