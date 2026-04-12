Encode BPHS chapter $ARGUMENTS into structured prediction rules.

Parse the chapter number from $ARGUMENTS (accept "ch24", "24", "Ch24", etc.). Let N = the chapter number.

---

## ENFORCEMENT RULES (read these FIRST, violate NONE)

- NEVER skip verse-level detail or artificially cap rule counts. Source material dictates all counts.
- NEVER estimate verse or claim counts. Read the chapter, count the verses.
- ALWAYS separate modifiers from primary conditions per ENCODING_GRANULARITY.md.
- ALWAYS include ALL required fields per rule contract schema. No partial rules.
- ALWAYS update all 5 docs at session end. No exceptions.
- If approaching context limits, finish encoding the current chapter before anything else. Do not start side tasks.
- Own all technical decisions. Never ask permission for implementation choices.

---

## STEP 0 — OCR verification (scanned PDFs only)

If the source PDF is a scanned image (not selectable text):
1. Run `tesseract` with appropriate languages (`san+hin+eng`)
2. Pick 3 verses spread across the chapter (start, middle, end)
3. Compare OCR text against the PDF image for each
4. If any verse has material errors (wrong numbers, dropped negations, garbled conditions) — fix OCR before proceeding
5. Store verified OCR text in `data/ocr/`

Skip this step for text-based PDFs where Read tool extracts text correctly.

---

## STEP 1 — Pre-flight (do NOT skip)

Read these files and hold their contents in context:

1. `docs/ENCODING_GRANULARITY.md` — the granularity definition
2. The rule contract schema (find it in src/ — the dataclass or TypedDict that defines a rule)
3. `/Users/harsh/.claude/projects/-Users-harsh/memory/lessons_learned.md`
4. `/Users/harsh/.claude/projects/-Users-harsh/memory/core_principles.md`

After reading, list every required field from the rule contract. Print the field list so the user can see it. Do not proceed until this is done.

---

## STEP 2 — Verse audit

Read the BPHS PDF for chapter N. Create `data/verse_audits/chN_audit.json` listing:
- Every verse (sloka) number in the chapter
- Every distinct claim per verse (predictions, conditions, exceptions, contraries)
- Apply the granularity definition: every distinct condition, exception, contrary, and direction-changing modifier is a separate claim

Print: "Chapter N: X verses, Y claims identified."

This audit file is the encoding spec. No encoding happens without it.

---

## STEP 2B — Audit review (who audits the auditor?)

Before encoding, review the audit file for completeness:
1. Does claim count match verse complexity? (simple verse = 1-2, complex = 3-6)
2. Are contrary mirrors identified where text says "in contrary situation"?
3. Are entity targets noted (father/spouse/children) — not defaulted to native?
4. Scan source text for "if/unless/except/however/relief" — any keyword without a corresponding audit claim is a gap
5. Run `/code-review` on `data/verse_audits/chN_audit.json`

**This is the highest-leverage gate.** Errors in the audit propagate silently through all downstream steps. Fix gaps here, not after encoding.

Print: "Audit review: Y claims confirmed, Z gaps found and fixed."

---

## STEP 3 — Show example rule (WAIT for approval)

Pick ONE verse from the audit that has moderate complexity. Encode it as a complete rule with ALL required fields populated. Show it to the user.

Say: "Here is one example rule with all required fields. Approve to continue, or correct any issues."

**STOP and wait for user response.** Do not proceed to full encoding without approval.

---

## STEP 4 — Encode exhaustively

Encode ALL claims from `data/verse_audits/chN_audit.json`. For every claim:
- Full modifier separation (amplifiers in modifier fields, not merged with conditions)
- Verse-level citations (verse number, not just chapter)
- Every required field from the contract populated
- No artificial cap on rule count — if the audit has 87 claims, produce 87 rules

After encoding, print: "Encoded Z rules from Y claims across X verses."

---

## STEP 5 — Test-driven loop

Run: `.venv/bin/pytest tests/ -x --tb=short`

If any test fails:
1. Read the failure output
2. Fix the rule or test
3. Re-run `.venv/bin/pytest tests/ -x --tb=short`
4. Repeat until ALL tests pass

Then run: `.venv/bin/ruff check src/ tests/`
Fix any lint errors. Re-run until clean.

Do not proceed until both pytest and ruff are green.

---

## STEP 6 — Audit verification

Run both:
- `.venv/bin/python tools/verse_audit.py --compare` — verify zero unencoded claims
- `.venv/bin/python tools/v2_scorecard.py` — quality scoring

Print the results. If verse_audit shows unencoded claims, go back to Step 4 and encode them. Do not proceed with gaps.

---

## STEP 7 — Documentation

Update all 5 docs using the standard update_docs script pattern:
- `docs/CHANGELOG.md`
- `docs/MEMORY.md`
- `docs/SESSION_LOG.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`

All 5. Every time. No exceptions.

---

## STEP 8 — Commit and push

```
git add [specific files only — never git add -A]
git commit -m "feat(chN): encode chapter N — Z rules from X verses

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
```

Pre-push hook will run full pytest + ruff. If it fails, fix and retry.

---

## DONE

Print a summary: chapter number, verse count, claim count, rule count, test status, scorecard result, audit result.
