---
name: warn-inline-astrological-constants
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: ^src/.*\.py$
  - field: new_text
    operator: regex_match
    pattern: ("Jupiter".*"Venus".*"Mercury"|"Aries".*"Taurus".*"Gemini".*"Cancer"|"Mars":\s*\{?[0-7]|0:\s*"Mars".*1:\s*"Venus")
---

**Inline astrological constant detected in src/**

This looks like a hardcoded planet set, sign list, or sign-lord table that should be imported from a canonical source.

**Check the Canonical Source Map in CLAUDE.md before proceeding:**
- Planet sets (benefic/malefic): `from src.data.constants import NATURAL_BENEFICS, NATURAL_MALEFICS`
- Sign names: `from src.data.constants import SIGN_NAMES`
- Sign lords: `from src.data.constants import SIGN_LORDS`
- Exaltation/debilitation: `from src.data.constants import EXALTATION_SIGN, DEBILITATION_SIGN`
- Own signs: `from src.data.constants import OWN_SIGNS`
- Kendra/Trikona: `from src.data.constants import KENDRA_HOUSES, TRIKONA_HOUSES`

If this is a legitimate new constant not in any canonical source, document why in a comment.
