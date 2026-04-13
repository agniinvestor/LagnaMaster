# CLAUDE.md — LagnaMaster

## Core Principles (NON-NEGOTIABLE — govern every decision)

1. **Long-term over quick** — evaluate every decision against the 1000+ session roadmap, not this session
2. **Nullify rework** — build controls BEFORE doing work. If a quality dimension exists, the gate must exist before encoding starts
3. **Right over easy** — always choose correct over convenient, even at 10× the effort. No shortcuts. No fake automation.
4. **Controls before work** — governance framework, validation, quality gates must exist BEFORE the work they govern
5. **Measure before claiming** — run the audit, run the scorecard, show the numbers. Never assume it passes.
6. **System enforces, not person** — if a standard matters, it's a code check. Markdown protocols are documentation; code is enforcement.
7. **Radical transparency** — when something is wrong, uncertain, or incomplete, say so immediately. Don't hide problems, optimise reporting, or hope issues self-resolve.
8. **Source fidelity** — record what the text says, not what you think it means. Interpretation goes in commentary, never in predictions or structured fields.
9. **Exhaust the problem before proposing** — when analysing gaps, designing controls, or planning work, assume your first pass is incomplete. Push yourself to find what you're missing before presenting. The user should not have to repeatedly ask "is that everything?" to get a thorough answer.
10. **Close the feedback loop** — when a mistake happens, it must flow through: Pattern → Lesson (lessons_learned.md) → Principle update (if systemic) → Control built (code enforcement) → Governance framework updated. A lesson without a corresponding control is an open loop. An open loop WILL recur.

## Quality Standards (enforced at every tool call)

- NEVER skip steps, cut corners, or artificially cap output. When encoding rules or performing audits, be exhaustive — do not summarize, truncate, or batch-shortcut. If you're tempted to skip something, flag it explicitly instead.
- When asked to do N things, do ALL N things. Do not stop at a subset and claim completion.
- Every rule must have ALL required fields per the V2 schema. Empty fields = incomplete work.

## Honesty & Confidence Calibration

- Do NOT overstate completeness or confidence. If coverage is partial, say so with specific numbers.
- Never inflate self-scores. Show actual numbers and gaps, not optimistic summaries.
- Before claiming any task is "done," list what was NOT checked and what might be missing.
- If uncertain about coverage, say "I checked X of Y" — never "this looks comprehensive" without evidence.
- Do not dismiss audit flags prematurely. Every flag requires investigation before closure.

## Review Protocol

- Never commit or finalize work that requires GPT review without completing that review step first.
- Never skip maker-checker gates. If a review step exists in the workflow, it is mandatory.
- Show ALL rules/items during review, not summaries. Summarized reviews hide errors.
- When presenting work for review, include: (1) what was done, (2) what was NOT done, (3) known gaps.

## Completion Checklist (mandatory before claiming "done")

Before reporting any task as complete, answer ALL of these:
1. What specific items were produced? (count, not description)
2. What was NOT checked or completed?
3. What is the evidence that the work is correct? (test results, not assertion)
4. Were all workflow gates followed? (list each gate and its status)
5. For audits/consolidation: what percentage of relevant files were READ at logic level (not grepped)? If <100%, list what was skipped and why.
6. For claims of "all X resolved": what would prove you wrong? Have you checked for that?

## Session Types (NEVER MIX)

**Governance session:** Build controls, update protocols, add lessons, write tools. No encoding.
**Encoding session:** Read PDF, audit verses, encode rules, push. No framework debates, no tool building, no lessons updates. Use existing infrastructure only.

If an encoding session discovers a gap that needs a new control: NOTE IT and finish encoding. Build the control in the next governance session. Do not stop encoding to build infrastructure.

## Encoding Protocol (MANDATORY — 5 hard gates, no skipping)

```
OCR → [OCR Gate] → Audit → [Audit Gate] → Encode → [Validate Gate] → Ship
```

### Gate 0: OCR Verification (scanned PDFs only)
If source is a scanned PDF, run OCR first (`tesseract input.pdf output -l san+hin+eng pdf`).
Then verify: pick 3 verses spread across the chapter, compare OCR text against the PDF image.
If any verse has material errors (wrong numbers, dropped negations, garbled conditions), fix OCR before proceeding.
Store OCR'd text in `data/ocr/`. Skip this gate for text-based PDFs.

### Gate 1: Verse Audit
Read every sloka + commentary from the PDF/OCR text. Create `data/verse_audits/chN_audit.json` listing every claim per verse. Apply granularity definition (`docs/ENCODING_GRANULARITY.md`) — every distinct condition, exception, contrary, and direction-changing modifier is a separate claim.

### Gate 2: Audit Review (who audits the auditor?)
Before encoding, review the audit file for completeness. Check:
- Does claim count match verse complexity? (simple verse = 1-2 claims, complex = 3-6)
- Are contrary mirrors identified where text says "in contrary situation"?
- Are entity targets noted (father/spouse/children) not defaulted to native?
- Run the keyword scanner from ENCODING_GRANULARITY.md against the source text — any "if/unless/except" without a corresponding audit claim is a gap.

**The audit file is treated as ground truth downstream. Errors here propagate silently through every gate that follows.** This is the highest-leverage review point.

### Gate 3: Encode from Audit
The audit file is the spec. Each claim maps to a rule. When done, run `tools/verse_audit.py --compare` to verify zero unencoded claims.

### Gate 4: Validate (DURING work, not after)
Run `tools/v2_scorecard.py --file <chapter_file>` after completing each chapter file.
Fix all warnings and errors BEFORE moving to the next chapter or committing.
Do not accumulate warnings across files — each file must be clean before proceeding.

Then run full test suite + `ruff check` before commit. All must pass.

A chapter without a verse audit file CANNOT be encoded. The builder blocks with ValueError.
The builder also blocks on entity_target mismatches, mixed-entity rules, and prediction entity mismatches (T1-14 through T1-17).

## Plugin Usage by Session Type

**Encoding sessions — use these plugins:**
- **hookify** — enforce gates as pre-commit hooks (audit file exists, claim count matches, 5 docs updated)
- **code-review** — run on `chN_audit.json` at Gate 2 (review the audit, not the code)
- **commit-commands** — `/commit` to ship
- **security-guidance** — passive background monitoring
- **claude-md-management** — 5-doc update enforcement

**Governance sessions — use these plugins:**
- **superpowers** — `/brainstorm` + `/write-plan` for infrastructure design
- **feature-dev** — multi-agent feature development
- **pr-review-toolkit** — deep PR review for infrastructure changes
- **code-simplifier** — post-refactor cleanup

**Do NOT use in encoding sessions:**
- `/brainstorm` — the source text is the spec, not a design discussion
- `/write-plan` — the audit file is the plan
- `feature-dev` — encoding is not feature development
- `playwright` / `firecrawl` — all docs are local

## Session Protocol (MANDATORY)

**At session START:**
1. Read `docs/ARCHITECTURE_CURRENT_VS_TARGET.md` — the golden source for architecture, gaps, build order, and quality criteria
2. Read `docs/PROJECT_STRATEGY.md` — project state and diagnostics
3. Read `tools/INDEX.md` — know what tools exist. Do NOT rebuild existing tools.
4. If encoding: read `docs/RULE_CONTRACT_V2.md` — the canonical V2 schema
5. Check `lessons_learned.md` for patterns relevant to today's work
6. Verify all controls exist for the work you're about to do (Principle #4)

**At session END:**
1. Did any rework happen this session? (amend commits, fix commits, re-encoding) → Add lesson
2. Did any audit control catch an error? → Add lesson about what the encoding missed
3. Did the user correct you on anything? → Add lesson about what should have been self-caught
4. Update lessons_learned.md with any new entries
5. If a new pattern emerged, update core_principles.md and governance framework

**A lesson without a control is an open loop. Close it before the session ends.**

---

## /cook — Multi-session batch execution

**Usage:** `/cook S195–S200` or `/cook S[X]–S[Y]`

Executes sessions X through Y in sequence within a single conversation.

### Per-session execution order (mandatory)

1. Read `docs/ROADMAP.md` entry for this session (deliverable, guardrails, status)
2. Read only the files listed in that session's RELEVANT SIGNATURES
3. Write all tests to `tests/test_s[N]_*.py` — ALL FAILING before any implementation
4. Implement until `ruff check src/ tests/` = 0 errors and all new tests pass
5. Run `.venv/bin/python update_docs_s[N].py` (create it if it doesn't exist)
6. `git add` exactly the files created/modified + docs → `git commit` → `git push`

### Context inheritance (token efficiency)

- **Same conversation:** skip re-reading `docs/MEMORY.md`, `docs/CHANGELOG.md`,
  `docs/SESSION_LOG.md` — use conversation context already in scope
- **Fresh conversation (cold start):** read `docs/MEMORY.md` (current state) +
  `docs/ROADMAP.md` (next session entry) before starting S[X]

### Autonomy rules

- Own every technical decision. Tests pass + ruff 0 + pre-push hook green = ships.
- Never ask permission for implementation choices.
- **On blocker:** reduce scope to what passes, commit that, record blocker in
  CHANGELOG and MEMORY under "Known Issues", continue to next session.
- **On guardrail conflict:** note in commit message + CHANGELOG, do not skip or violate.

### Standard commit format

```
feat(S[N]): [one-line description]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Standard update_docs_s[N].py contract

Every session must produce an `update_docs_s[N].py` that patches:
- `docs/CHANGELOG.md` — new session entry (Three-Lens format)
- `docs/MEMORY.md` — test count, session progress line, Next session pointer
- `docs/SESSION_LOG.md` — session entry under correct Phase heading
- `docs/ROADMAP.md` — mark session ✅
- `docs/ARCHITECTURE.md` — new module entries if files were created

### Ship definition

A session is shipped when:
1. All new tests pass
2. `ruff check src/ tests/` = 0 errors
3. Pre-push hook passes (runs full pytest + ruff automatically)
4. `git push` succeeds

---

## Project context

- **Repo:** `github.com/agniinvestor/LagnaMaster`
- **Engine:** `v3.0.0` | **Python:** 3.14 | **Ephemeris:** pyswisseph JPL DE431
- **Venv:** `.venv/` — use `.venv/bin/pytest`, `.venv/bin/ruff`, `.venv/bin/python`
- **Test runner:** `pytest tests/ -q --tb=short`
- **Guardrails:** `docs/GUARDRAILS.md` — read the entry for any guardrail cited in ROADMAP
- **Pre-push hook:** `.git/hooks/pre-push` — runs full suite before every push
- **India 1947 fixture:** used in integration tests across many sessions
  ```python
  compute_chart(year=1947, month=8, day=15, hour=0.0,
                lat=28.6139, lon=77.2090, tz_offset=5.5)
  # Lagna: Taurus | Moon: Pushya (Saturn MD) | H2 score: negative
  ```

---

## Canonical Source Map (DO NOT duplicate — import from these)

When a calculation exists in multiple files, one is canonical and others delegate.
Before implementing any astrological calculation, check this map. If it exists, import — don't rewrite.

| Calculation | Canonical module | Delegates/imports from it |
|---|---|---|
| **Constants: signs, nakshatras, exaltation, lords** | `src/data/constants.py` | nakshatra.py, rule_firing.py, ishta_kashta.py, longevity.py, scoring_patches.py |
| **Dignity (exalt/debil/own/MT/combustion/uchcha bala)** | `src/calculations/dignity.py` | rule_firing.py, divisional_charts.py, sapta_varga.py, ishta_kashta.py |
| **All varga sign computations (D2–D12, D60)** | `src/calculations/varga.py` | divisional_charts.py, sapta_varga.py, drekkana_variants.py, nakshatra.py |
| **Scoring (house score, rule evaluation)** | `src/calculations/multi_axis_scoring.py` | scoring.py (thin wrapper) |
| **Aspect strength (sputa drishti)** | `src/calculations/sputa_drishti.py` | scoring_patches.py, rule_firing.py |
| **Chara Karakas (7/8 planet ranking)** | `src/calculations/chara_karaka_config.py` | chara_karak.py (wraps as list[CharaKarak]) |
| **Karakamsha (D9 of Atmakaraka)** | `src/calculations/multi_lagna.py:compute_karakamsha` | karakamsha_analysis.py |
| **Nabhasa Yogas (32 BPHS Ch.35)** | `src/calculations/nabhasa_yogas.py` | yogas_extended.py (wraps as YogaResult) |
| **Longevity (Pindayu/Nisargayu/Amsayu)** | `src/calculations/longevity.py` | ayurdaya.py (composite wrapper only) |
| **Graha Yuddha (planetary war)** | `src/calculations/graha_yuddha.py` | planet_effectiveness.py |
| **Tarabala/Chandrabala (transit quality)** | `src/calculations/transit_quality_advanced.py` | (detailed model; muhurtha_complete.py has independent binary model for muhurtha) |
| **Vimshopaka (16-varga Shodasavarga)** | `src/calculations/divisional_charts.py` | scoring_v3.py |
| **Vimshopak (7-varga Sapta Varga)** | `src/calculations/sapta_varga.py` | app.py (UI) |
| **Derived house arithmetic** | `src/calculations/derived_house.py` | (all bhavat-bhavam goes here) |
| **Functional malefics (hardcoded per-lagna table)** | `src/calculations/functional_dignity.py:KNOWN_FUNCTIONAL_MALEFICS` | multi_axis_scoring.py, pressure_engine.py, dominance_engine.py, upaya.py |
| **Functional classification (canonical BPHS Ch.34)** | `src/calculations/functional_dignity.py:compute_functional_classifications` | functional_roles.py (wraps as FunctionalRoles) |
| **Functional roles (dynamic computation)** | `src/calculations/functional_roles.py:compute_functional_roles` | multi_axis_scoring.py, pressure_engine.py, yoga_fructification.py |
| **House map (whole-sign)** | `src/calculations/house_lord.py:compute_house_map` | (many consumers; multi_lagna._build_frame is the multi-lagna variant) |
| **Naisargika friendship** | `src/calculations/dignity.py:_NAISARGIKA` | panchadha_maitri.py (delegates for naisargika_relation) |
| **Neecha Bhanga (6 conditions)** | `src/calculations/dignity.py:compute_dignity` | extended_yogas.py (delegates for detect_neecha_bhanga) |
| **Arudha Pada (generic)** | `src/calculations/argala.py:compute_arudha` | upapada_lagna.py, special_lagnas.py |
| **Yoga result type** | `src/calculations/extended_yogas.py:YogaResult` | yogas_graha.py, yogas_extended.py, rule_plugin.py, yoga_strength.py |
| **Gajakesari/Budhaditya/Chandra-Mangala** | `src/calculations/yogas_graha.py` | (canonical graha yoga detections) |
| **Vesi/Vasi/Ubhayachari/Adhi** | `src/calculations/yogas_extended.py` | (canonical surya/chandra yoga detections) |
| **Kemadruma/Raj Yoga** | `src/calculations/scoring_patches.py` | (canonical, with full conditions + cancellations) |
| **Amala/Vasumati/Mahabhagya** | `src/calculations/yoga_strength.py` | (canonical, with strength grading) |
| **Rashi Drishti (Jaimini)** | `src/calculations/jaimini_rashi_drishti.py` | stronger_of_two.py |
| **Source text registry** | `src/corpus/source_texts.py` | v2_builder.py |
| **Rule schema (V2)** | `docs/RULE_CONTRACT_V2.md` | v2_builder.py enforces |

**Convention:** canonical modules have `_canonical` naming in imports or docstrings saying "delegates to X".
If you add a new calculation, add it to this map. If you find a calculation not in this map, check for duplicates before writing.

---

## What NOT to do

- Do not re-read `docs/MEMORY.md` mid-batch (stale relative to conversation context)
- Do not add features beyond the ROADMAP deliverable
- Do not modify `_WEIGHTS` tables in `multi_axis_scoring.py` unless the session
  explicitly targets scoring recalibration (breaks regression snapshots)
- Do not `git add -A` — always add specific files to avoid committing stale scripts
- Do not skip the pre-push hook (`--no-verify`)
- Do not create new tools without checking `tools/INDEX.md` first — if a tool exists, use it
- Do not define rule fields outside `docs/RULE_CONTRACT_V2.md` — it is the single source of truth
- Do not guess corpus structure — check `docs/CORPUS_MANIFEST.json` for file inventory
- Do not rebuild infrastructure that exists. Read INDEX.md. If confused, grep before writing.
- Do not reimplement calculations that have a canonical source. Check the Canonical Source Map above. Import, don't rewrite.
