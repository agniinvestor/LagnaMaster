---
name: warn-hardcoded-weights
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^src/.*\.py$
  - field: new_text
    operator: regex_match
    pattern: _WEIGHTS\s*=\s*\{|"R\d{2}":\s*[\d.]+
---

**Hardcoded scoring weights detected**

Per the target architecture (ARCHITECTURE_CURRENT_VS_TARGET.md), ALL weights should be
data in the weight store, not hardcoded Python dicts. Rules and their weights are
hypotheses to be empirically tested, not constants.

If this is modifying existing _WEIGHTS during Phase C transition, document the reason.
The target state (G4) moves all weights to a versioned weight store.
