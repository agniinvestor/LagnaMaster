# Checklist: Adding a New Classical Text

> Q12 evolvability criterion. Adding a new text should require zero computation layer changes.

## Prerequisites

- [ ] PDF/source of the text available in `data/classical_texts/`
- [ ] Verse audit protocol understood (see CLAUDE.md Gate 1-2)
- [ ] V2 builder API understood (see `src/corpus/v2_builder.py`)

## Steps

1. **Create verse audit** → `data/verse_audits/textname_chN_audit.json`
   - Read every sloka + commentary
   - One claim per verse, per granularity rules (docs/ENCODING_GRANULARITY.md)

2. **Review audit** (Gate 2 — mandatory)
   - Does claim count match verse complexity?
   - Are contrary mirrors identified?
   - Run keyword scanner against source text

3. **Create corpus file** → `src/corpus/textname_vN_chN.py`
   - Use `V2ChapterBuilder` with correct source name
   - Source must be in `src/corpus/source_texts.py` VALID_SOURCE_NAMES
   - If new source, add it to source_texts.py first

4. **Encode rules using existing primitives only**
   - Check `src/corpus/feature_registry.py` for available condition types
   - If a needed primitive doesn't exist: STOP, file a feature request
   - Do NOT create new computation modules during encoding

5. **Run validation**
   ```bash
   .venv/bin/python tools/v2_scorecard.py --file src/corpus/textname_vN_chN.py
   .venv/bin/ruff check src/corpus/textname_vN_chN.py
   .venv/bin/pytest tests/ -q --tb=short
   ```

6. **Verify in pipeline**
   ```bash
   .venv/bin/python -m src.pipeline 1947 8 15 0.0 28.6139 77.2090 5.5
   ```
   - New text's rules should appear in corpus_results
   - If text is a new source, it should appear as a convergence channel

7. **Update registry**
   - Add source to `src/corpus/source_texts.py` if new
   - Update `docs/CORPUS_MANIFEST.json` with new file
