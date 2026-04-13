# Checklist: Adding a New Astrological School

> Q12 evolvability criterion. Adding a new school should only require school-specific modules where that school differs from Parashari.

## Prerequisites

- [ ] Understand which concepts differ from Parashari
- [ ] Source texts for the school available

## Steps

1. **Identify differing concepts**
   - Which calculations are different? (e.g., house system, aspects, dasha)
   - Which are the same? (Parashari defaults apply)

2. **Create school-specific modules** (only for differences)
   - Place in `src/calculations/` with `{school}_` prefix
   - Example: `src/calculations/kp_sublord.py` for KP sub-lord theory
   - Each module MUST import shared primitives from canonical sources (see CLAUDE.md Canonical Source Map)

3. **Add school to weight tables**
   - `src/corpus/scoring_rules.py` → `SCHOOL_WEIGHTS["{school}"]`
   - `src/corpus/scoring_rules.py` → `YOGAKARAKA_MULTIPLIER["{school}"]`

4. **Register school in configuration**
   - Add to `src/calculations/calc_config.py` if it exists
   - Add school-specific rules to corpus with `school="{school}"`

5. **Test**
   ```bash
   .venv/bin/python -c "
   from src.pipeline import run_pipeline
   r = run_pipeline(year=1985, month=3, day=15, hour=10.5,
                    lat=28.61, lon=77.21, tz_offset=5.5, school='{school}')
   print(f'School {school}: {len(r.predictions)} predictions')
   "
   .venv/bin/pytest tests/ -q --tb=short
   ```

6. **Update MODULE_REGISTRY**
   - Register new school-specific modules in `src/MODULE_REGISTRY.py`
   - Add `_VERIFICATION` tag to each new module
