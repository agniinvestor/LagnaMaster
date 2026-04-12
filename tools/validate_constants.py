#!/usr/bin/env python3
"""tools/validate_constants.py — Prevent astrological constant duplication.

Scans src/ for patterns that look like local re-definitions of constants
that should live exclusively in src/data/constants.py.

Exit code 0 = clean, 1 = violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Patterns that indicate a local constant definition.
# Each tuple: (regex, description)
_PATTERNS: list[tuple[str, str]] = [
    (r'_(?:NAT_)?(?:NATURAL_)?BENEFIC\w*\s*[:=]\s*[\{(\[]', "Natural benefic/malefic set"),
    (r'_(?:NAT_)?(?:NATURAL_)?MALEFIC\w*\s*[:=]\s*[\{(\[]', "Natural benefic/malefic set"),
    (r'_?SIGN_LORD\w*\s*[:=]\s*\{', "Sign lord mapping"),
    (r'_?GENTLE_SIGN\w*\s*[:=]\s*[\{(\[]', "Gentle/cruel sign set"),
    (r'_?(?:SPECIAL_ASPECT)\w*\s*[:=]\s*\{', "Special aspect mapping"),
    (r'_?KENDRA\s*[:=]\s*\{', "Kendra house set"),
    (r'_?TRIKONA\s*[:=]\s*\{', "Trikona house set"),
    (r'_?DUSTHANA\s*[:=]\s*\{', "Dusthana house set"),
    (r'_?UPACHAYA\s*[:=]\s*\{', "Upachaya house set"),
    (r'_?DIG_BALA\w*\s*[:=]\s*\{', "Dig Bala mapping"),
    (r'_?STHIR\w*KARAK\w*\s*[:=]\s*\{', "Sthira Karaka mapping"),
    (r'_?EXALT(?:ATION)?_SIGN\w*\s*[:=]\s*\{', "Exaltation sign mapping"),
    (r'_?DEBIL(?:ITATION)?_SIGN\w*\s*[:=]\s*\{', "Debilitation sign mapping"),
    (r'_?SIGN_NAMES\s*[:=]\s*[\[\(]', "Sign name list"),
]

# Files that are allowed to define constants
_ALLOWED = {
    Path("src/data/constants.py"),
}

# Patterns that are suffixed algorithm-specific variants (not duplicates).
# e.g. _SIGN_LORDS_BB (bhava_bala), _SIGN_LORDS_NB (neecha bhanga)
# Also: _SPECIAL_ASPECTS in rule_firing/drig_dasha (different indexing/concept)
# Also: _EXALT_SIGN/_DEBIL_SIGN/_OWN_SIGNS in rule_firing (includes Rahu/Ketu)
_SUFFIXED_OK = re.compile(
    r'_SIGN_LORD\w+_[A-Z]{2,}\b|_SPECIAL_ASPECTS\b|_EXALT_SIGN\b|_DEBIL_SIGN\b|_OWN_SIGNS\b'
)

# Directories to skip
_SKIP_DIRS = {"__pycache__", ".claude", ".git", ".venv", "node_modules"}


def scan(root: Path) -> list[tuple[Path, int, str, str]]:
    """Return list of (file, line_no, matched_text, description) violations."""
    violations: list[tuple[Path, int, str, str]] = []
    src_dir = root / "src"

    for py_file in src_dir.rglob("*.py"):
        if any(part in _SKIP_DIRS for part in py_file.parts):
            continue
        rel = py_file.relative_to(root)
        if rel in _ALLOWED:
            continue

        try:
            text = py_file.read_text()
        except (OSError, UnicodeDecodeError):
            continue

        for i, line in enumerate(text.splitlines(), 1):
            stripped = line.lstrip()
            # Skip comments
            if stripped.startswith("#"):
                continue
            # Skip function-scoped definitions (indented lines)
            if line != stripped:  # line is indented
                continue
            # Skip known suffixed algorithm-specific variants
            if _SUFFIXED_OK.search(stripped):
                continue
            for pattern, desc in _PATTERNS:
                if re.search(pattern, stripped):
                    violations.append((rel, i, stripped[:80], desc))
                    break  # one match per line is enough

    return violations


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    violations = scan(root)

    if not violations:
        print("OK — no astrological constants defined outside src/data/constants.py")
        return 0

    print(f"FAIL — {len(violations)} constant(s) defined outside src/data/constants.py:\n")
    for path, lineno, text, desc in sorted(violations):
        print(f"  {path}:{lineno}  [{desc}]")
        print(f"    {text}")
    print(f"\nAll astrological constants must be defined in src/data/constants.py.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
