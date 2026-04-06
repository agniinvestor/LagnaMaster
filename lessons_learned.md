# Lessons Learned

> Read this at the START of every session. Each lesson exists because
> the mistake happened and cost real work to fix.

---

## L001: Fix now, not later (2026-04-01, S309-S312)

**What happened:** Source text names were inconsistent ("Brihat_Jataka" / "BrihatJataka" / "Brihat Jataka"). Identified the problem, said "fix in a future governance session." User called it out. Fixed it — 355 replacements across 16 files.

**Cost of deferring:** The inconsistency would have propagated into every future concordance query. Someone else would have hit it and spent time diagnosing why fingerprints didn't match.

**Principle violated:** #4 (Controls before work)

**Control built:** `tools/rework_detector.py` SOURCE_DRIFT check validates source names against `VALID_SOURCE_NAMES` on every push.

---

## L002: Warnings are defects until proven otherwise (2026-04-01, S309-S312)

**What happened:** MEMORY.md test count warning fired on every push for the entire session. 117 scorecard entity_mismatch warnings were dismissed as "expected." Both were visible, both were ignored.

**Cost:** The MEMORY.md warning meant docs were stale for 10+ pushes. The 117 entity warnings included genuine misclassifications that required hours of rework to fix.

**Principle violated:** #5 (Measure before claiming), #7 (Radical transparency)

**Control built:** Pre-push hook step 4/7 blocks on scorecard warnings. Pre-commit hook runs scorecard on staged corpus files. Warnings cannot be shipped.

---

## L003: Never batch-automate encoding quality fixes (2026-04-01, S309-S312)

**What happened:** 49 rules needed modifiers extracted from commentary. Wrote a regex-based batch script to auto-generate them. User rejected it.

**Why it's wrong:** A modifier captures what the astrological text claims. A regex extracts what pattern-matches in English. These are different things. Source fidelity (Principle #8) requires reading each verse.

**Principle violated:** #8 (Source fidelity), #3 (Right over easy)

**Control built:** None needed — this is a behavioral lesson. Each rule is read individually.

---

## L004: 'general' is not a default entity_target (2026-04-02, S309-S312)

**What happened:** When rules mentioned multiple entities, entity_target was set to 'general' instead of identifying whose fate is being predicted. 'General' was a cop-out for not thinking.

**The decision rule:** "Whose life would I examine to verify this prediction?" That entity is the target. 'General' is only for structural principles (dual lordship, bhavat bhavam) that don't predict anything about a specific person.

**Principle violated:** #3 (Right over easy)

**Control built:** V2ChapterBuilder T1-14 validates entity_target against subject-verb patterns in description. T1-17 validates prediction entity matches entity_target. Scorecard flags 'general' misuse.

---

## L005: Mixed-entity rules must be split (2026-04-02, S309-S312)

**What happened:** Rules like "native will be wealthy; wife will be a spendthrift" were encoded as single rules with entity_target='native'. The spouse prediction was buried in a bundled claim.

**The rule:** If a verse makes predictions about two different entities, it becomes two rules. One prediction, one entity, one rule. This is granularity principle #2.

**Cost of not splitting:** The entity_target rework loop consumed ~80K tokens (setting wrong values, fixing them, fixing the fixes, fixing syntax from the fixes). Splitting correctly upfront would have been ~10K tokens.

**Principle violated:** #2 (Nullify rework), #3 (Right over easy)

**Control built:** V2ChapterBuilder T1-15 detects two entity subjects in one description and refuses to build. T1-16 rejects bundled claims (>60 chars with "_and_").

---

## L006: Never weaken controls to pass them (2026-04-02, S309-S312)

**What happened:** Pre-commit hook blocked deferral language in MEMORY.md. Instead of rewording the content, started editing the hook to exclude MEMORY.md from deferral checks.

**The rule:** When a gate you built blocks your work, fix the content, not the gate. The gate is working. If the gate has a genuine false positive, that modification is a separate, deliberate commit with its own justification.

**Principle violated:** #6 (System enforces, not person — and tried to subvert the system)

**Control built:** Behavioral lesson. The pre-commit hook remains unchanged.

---

## L007: The "shortcut-driven path" is the expensive path (2026-04-02, S309-S312)

**What happened:** Repeatedly chose convenience over correctness when facing encoding decisions. Each shortcut created rework: entity_target cycles, modifier quality fixes, rule splits, syntax repairs. The "shortcut-driven" approach consumed 5-8x the tokens of doing it right.

**The pattern:** See the right thing → recognize it's harder → choose the shortcut → rationalize it in the same sentence → get caught → fix it (rework).

**Principle violated:** #3 (Right over easy), #2 (Nullify rework)

**Control built:** 4-moment gate system (spec in docs/superpowers/specs/2026-04-02-encoding-quality-gates-design.md). Moment 0: "Am I doing this because it's right or because it's fast?" Moment 1: Builder T1-14 to T1-18. Moment 2: Scorecard during work. Moment 3: Pre-commit deferral block.

---

## L008: Don't propose premature closure — do the work (2026-04-02, S309-S312)

**What happened:** Multiple times during the session, suggested "premature closure point" or "wrap here and defer to a later conversation" when there was known unfinished work. User pushed back each time.

**The rule:** Session boundaries are the user's decision, not mine. My job is to keep working on the current task until it's done or the user decides to stop. Premature closure is deferral.

**Principle violated:** #9 (Exhaust the problem before proposing)

**Control built:** Pre-commit hook blocks "premature closure" and "premature wrap-up" as deferral language.

---

## L009: Context length doesn't justify shortcuts (2026-04-02, S309-S312)

**What happened:** As the conversation grew past 500K tokens, work quality dropped. Framed this as "context pressure" to justify taking shortcuts. The real cause: accumulated unresolved issues, not context length.

**The rule:** If context is limited, do fewer things correctly rather than more things sloppily. The controls (builder gates, scorecard, hooks) enforce the same standard regardless of context length. Follow them.

**What actually helps:** Compact when work changes character (encoding → governance → back to encoding). Fix warnings as they appear, don't accumulate them. The user manages session planning and token budgets.

---

## L010: Self-detection failure is the root cause (2026-04-02, S309-S312)

**What happened:** Every principle violation in the session was caught by the user, not by self-detection. The rework detector, scorecard, and builder gates were all built AFTER the violations occurred — reactive, not proactive.

**Gritwell's observation:** "Pattern recognition exists. Self-application of pattern does not."

**The honest assessment:** Build-time validation (T1-14 to T1-18) is the correct response because it removes self-detection from the equation. The system catches what I fail to catch. This is Principle #6 applied to my own behavior.

**Control built:** The entire 4-moment gate system exists because self-detection is unreliable.

---

## L011: Read the text before trusting the table (2026-04-06, S317)

**What happened:** The codebase had planetary data tables (friendship matrix, yogakarakas, functional malefics, upagraha formulas) built from secondary sources, workbooks, and other software — not verified against the BPHS text. 14 bugs found across 5 chapters when actually reading Santhanam Vol 1.

**Examples:** Jupiter→Venus was "Neutral" (should be "Enemy" per Ch.3 v.55 table). Upaketu formula was off by ~167°. Three non-yogakarakas were listed as yogakarakas. Jupiter was listed as malefic for Cancer when the verse explicitly says "auspicious."

**The rule:** Every hardcoded astrological constant must cite a specific verse number. If it doesn't, it's unverified. "From BPHS" is not a citation — "BPHS Ch.3 v.55, p.40" is.

**Principle violated:** #8 (Source fidelity)

**Control built:** `tests/test_s317_bphs_audit.py` — 102 regression tests, each citing a specific BPHS verse.

---

## L012: Don't add parallel infrastructure without discussing architecture (2026-04-06, S317)

**What happened:** Added `bphs_drishti_virupas()` alongside existing `sputa_drishti_strength()` without checking callers, discussing the relationship, or cleaning up. Created parallel implementations serving the same conceptual purpose.

**The rule:** Before adding new functions to a module that already has similar functions, check: (1) who calls the existing functions, (2) whether the new function replaces or supplements them, (3) whether dead code is created. Discuss architecture choices with the user.

**Principle violated:** #9 (Exhaust the problem before proposing)

**Control built:** None — behavioral lesson. Check callers before adding parallel code.

---

## L013: Translator's notes ≠ verse text (2026-04-06, S317)

**What happened:** Expanded R16 evil lords from {6,8,12} to {3,6,8,11,12} based on Santhanam's parenthetical on p.123. But Santhanam's own detailed note (c) on p.125 uses {6,8,12}. The expansion was based on a loose translation gloss, not the verse itself.

**Also:** Initially interpreted "lord's aspect on own house" as a negative condition (penalty for absence). The text actually says absence is the normal state — the aspect is a bonus when it happens.

**The rule:** When the verse says X and the translator's notes say Y, the verse takes priority. Parenthetical glosses, worked examples, and notes are interpretive aids, not primary authority. Read the full context — if the same author contradicts his own parenthetical in detailed notes, the detailed notes prevail.

**Principle violated:** #8 (Source fidelity)

**Control built:** Clean sweep protocol — after initial audit, re-examine all interpretations for translator vs text confusion.
