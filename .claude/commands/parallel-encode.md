# Parallel Agent Encoding with Cross-Validation

Encode multiple BPHS chapters simultaneously using parallel sub-agents. Each chapter gets an independent encoder and auditor; a supervisor reconciles.

## Pre-Flight (MANDATORY)

1. Confirm target chapters with user (e.g., "Ch.25-27")
2. Verify source PDFs exist — check for BPHS volumes in repo root or `data/ocr/`
3. Read `docs/RULE_CONTRACT_V2.md` — this is the schema spec for all agents
4. Read `tools/INDEX.md` — know what tools are available

## Agent Architecture

For EACH chapter, spawn TWO agents in parallel using the Agent tool:

### Agent 1: Encoder
Prompt: "You are encoding BPHS Ch.{N} into the LagnaMaster corpus. Read the BPHS PDF for Ch.{N}, create a verse audit listing every distinct claim per sloka, apply granularity definition from docs/RULE_CONTRACT_V2.md, encode each claim as a V2 rule with ALL mandatory fields, write to src/corpus/bphs_v2_ch{N}.py, run v2_scorecard.py on it. Report: verses read, claims identified, rules encoded, scorecard results."

### Agent 2: Auditor
Prompt: "You are independently auditing BPHS Ch.{N} for completeness. Read the BPHS PDF — do NOT read encoding files first. For every sloka, count conditions, exceptions, entity targets, contrary implications. Apply granularity from docs/RULE_CONTRACT_V2.md. Output JSON: {verse_num, claim_count, claim_descriptions[]}. Report: total verses, total claims, complex verses needing 3+ rules."

## Supervisor Reconciliation (YOU do this)

After both agents return:
1. Compare claim counts — encoder rules vs auditor claims. If >10% gap: investigate.
2. Cross-reference: every auditor claim must have an encoder rule. Missing = encode. Extra = verify source.
3. Run: `PYTHONPATH=. .venv/bin/python tools/validate_rules.py --file src/corpus/bphs_v2_ch{N}.py`
4. Run: `.venv/bin/pytest tests/ -x --tb=short -q`
5. Report per chapter: encoder claims, auditor claims, reconciled count, validation pass/fail.

## Commit
```
encode(S{N}): Ch.{X}-{Y} — {total} rules from {verses} verses (parallel-encoded)
```

## Anti-Patterns
- Encoder reading audit output before finishing = VIOLATION (independence required)
- Auditor reading encoding files = VIOLATION (confirmation bias)
- Skipping reconciliation = VIOLATION
- Committing without validate_rules.py = VIOLATION
