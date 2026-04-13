# Architecture Build Session — G1 through G6

## Session type
**Wiring** — build pipeline layers per ARCHITECTURE_CURRENT_VS_TARGET.md. No encoding. No new governance docs.

## Pre-flight (mandatory)

1. Read `docs/ARCHITECTURE_CURRENT_VS_TARGET.md` — the golden source
2. Identify which gap (G1-G6) is next on the critical path
3. Verify all predecessor gaps are complete (G1 before G2, G2 before G3, etc.)
4. Run baseline:
```bash
.venv/bin/pytest tests/ -q --tb=short
.venv/bin/ruff check src/ tests/
PYTHONPATH=. .venv/bin/python tools/ob3_calibrate.py --report 2>&1 | grep 'H[0-9]*: ρ='
```

## Critical path

```
G1 (ChartContext) → G2 (rules to data) → G3 (unified engine) → G4 (weight store) → G5 (convergence) → G6 (temporal) → encoding resumes
```

## Per-gap specification

### G1: ChartContext with 5-tier ordering
- Create `src/calculations/chart_context.py`
- `build_chart_context(chart) → ChartContext` dataclass
- Tier order: positions → lordships → aspects/combustion/friendship → dignity/avasthas → shadbala/func_roles
- Modules accept optional `ctx=` parameter (zero breaking changes)
- Exit: 135+ redundant calls → 1. All tests pass.

### G2: Migrate R01-R24 to corpus
- Create V2 rule records for each of the 26 hardcoded rules
- Each with: structured conditions, BPHS verse citation, predictions[], weight_key
- `evaluate_house_detailed()` becomes thin wrapper or deleted
- Exit: zero hardcoded rules in Python. All rules are data.

### G3: Unified evaluation engine
- Create `evaluate_all_rules(ctx, corpus, weights) → list[EvalResult]`
- EvalResult: rule_id, house, direction, magnitude, verse, predictions[], conditions_met[], confidence
- One engine evaluates ALL rules. scoring.py, multi_axis_scoring.py, rule_firing.py, inference.py → single function
- Exit: one engine, one output type, full traceability.

### G4: Weight store
- Create `src/calculations/weight_store.py`
- Format: {rule_id: {base_weight, empirical_weight, n, ci, contexts{}}}
- Three version axes in output: corpus_version, schema_version, weight_version
- Initial: base_weight from encoding, empirical = base
- Exit: _WEIGHTS dict deleted. Engine reads from store.

### G5: Convergence layer
- Create `converge(eval_results, ctx) → list[ConvergedPrediction]`
- Count independent confirmations across: natal (D1/D9/D10/D12), temporal (MD/AD/PAD), transit, yoga
- Contra-indicators counted separately
- Exit: predictions carry convergence_score + confirmation_sources[]

### G6: Temporal probability
- Create `time_project(converged, ctx) → list[TimedPrediction]`
- Overlay: Vimshottari, Chara, Yogini dashas + transits + varshaphala
- Output: P(event|year) distribution, peak_window, timing_confidence
- Exit: predictions have timing, not just "during Jupiter dasha"

## Ground rules
- One gap at a time. Complete, test, commit.
- Every change test-verified. Run full suite after each gap.
- Do NOT change behavior of existing API endpoints without explicit discussion.
- Do NOT create new governance documents. The architecture doc IS the plan.
- When in doubt about direction, re-read ARCHITECTURE_CURRENT_VS_TARGET.md.

## Quality criteria to maintain (from architecture doc)
- Q7: Runtime invariant check after ChartContext build
- Q9: Benchmark <200ms after G1
- Q10: Reproducibility snapshot after G3
- Q4: Full traceability in EvalResult

## Completion checklist (per gap)
1. What was produced? (specific files, functions, dataclasses)
2. What was NOT done? (honestly)
3. Evidence of correctness? (test output, benchmark numbers)
4. What % of affected files were read at logic level?
5. What would prove this gap is NOT actually closed?
6. Did OB-3 regress?
