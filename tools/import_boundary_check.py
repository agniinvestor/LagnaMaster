#!/usr/bin/env python3
"""tools/import_boundary_check.py — Enforce architectural layer boundaries.

Validates that no module imports from a higher layer than its own.
Uses src/MODULE_REGISTRY.py for layer assignments.

Exit code 0 = clean, 1 = violations found.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def _module_path_from_file(filepath: Path, root: Path) -> str:
    """Convert file path to dotted module path."""
    rel = filepath.relative_to(root)
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".py", "")
    return ".".join(parts)


def _get_layer(module_path: str) -> int:
    """Return the architectural layer for a module path."""
    if module_path.startswith("src.data."):
        return 1
    if module_path == "src.ephemeris":
        return 2
    if module_path.startswith("src.calculations."):
        return 3
    if module_path.startswith("src.corpus."):
        return 4
    if module_path in ("src.scoring",) or module_path.startswith("src.scoring."):
        return 5
    if module_path.startswith("src.api.") or module_path.startswith("src.ui."):
        return 6
    # src.db*, src.worker, etc. — infrastructure, treat as layer 6
    if module_path.startswith("src."):
        return 6
    return 0  # external package


def _extract_imports(filepath: Path) -> list[tuple[str, int]]:
    """Extract all src.* imports from a Python file. Returns (module_path, line_no)."""
    try:
        tree = ast.parse(filepath.read_text())
    except SyntaxError:
        return []

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("src."):
            # Get the base module (e.g., "src.calculations.dignity")
            imports.append((node.module, node.lineno))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("src."):
                    imports.append((alias.name, node.lineno))
    return imports


def check_boundaries(root: Path) -> list[tuple[str, int, str, int, int]]:
    """Check all src/ files for layer boundary violations.

    Returns list of (source_file, line, imported_module, source_layer, import_layer).
    """
    violations = []
    src_dir = root / "src"

    for py_file in src_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue

        source_mod = _module_path_from_file(py_file, root)
        source_layer = _get_layer(source_mod)

        if source_layer == 0:
            continue

        for imported_mod, lineno in _extract_imports(py_file):
            # Get the top-level module for layer classification
            # e.g., "src.calculations.dignity" → check "src.calculations.dignity"
            import_layer = _get_layer(imported_mod)

            if import_layer == 0:
                continue  # external package

            if import_layer > source_layer:
                violations.append((
                    str(py_file.relative_to(root)),
                    lineno,
                    imported_mod,
                    source_layer,
                    import_layer,
                ))

    return violations


_LAYER_NAMES = {
    1: "data",
    2: "ephemeris",
    3: "calculations",
    4: "corpus",
    5: "scoring",
    6: "api/ui",
}


# Known exceptions — documented architectural decisions
_KNOWN_EXCEPTIONS = {
    # Multi-axis scoring is classified as layer 5 but lives in calculations/
    ("src/calculations/multi_axis_scoring.py", "src.scoring"),
    # Rule firing imports from corpus (needed to get rules + snapshots)
    ("src/calculations/rule_firing.py", "src.corpus.combined_corpus"),
    ("src/calculations/rule_firing.py", "src.corpus.feature_registry"),
    ("src/calculations/rule_firing.py", "src.corpus.snapshot"),
    # Inference uses corpus taxonomy for condition type classification
    ("src/calculations/inference.py", "src.corpus.taxonomy"),
    # Interpretation uses corpus archetypes for planet descriptions
    ("src/calculations/interpretation.py", "src.corpus.planet_archetypes"),
    # Monte carlo is a research tool that naturally imports scoring + worker
    ("src/calculations/monte_carlo.py", "src.worker"),
    ("src/calculations/monte_carlo.py", "src.scoring"),
    # Pushkara navamsha scoring integration
    ("src/calculations/pushkara_navamsha.py", "src.scoring"),
}


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    violations = check_boundaries(root)

    # Filter out known exceptions
    filtered = [
        v for v in violations
        if (v[0], v[2]) not in _KNOWN_EXCEPTIONS
    ]

    if not filtered:
        print(f"OK — all {_count_files(root)} src/ modules respect layer boundaries")
        if violations:
            print(f"  ({len(violations)} known exception(s) documented)")
        return 0

    print(f"FAIL — {len(filtered)} layer boundary violation(s):\n")
    for source, lineno, imported, src_layer, imp_layer in sorted(filtered):
        src_name = _LAYER_NAMES.get(src_layer, f"L{src_layer}")
        imp_name = _LAYER_NAMES.get(imp_layer, f"L{imp_layer}")
        print(f"  {source}:{lineno}")
        print(f"    imports {imported}")
        print(f"    {src_name} (L{src_layer}) → {imp_name} (L{imp_layer}) — upward dependency")
        print()

    return 1


def _count_files(root: Path) -> int:
    return sum(1 for _ in (root / "src").rglob("*.py") if "__pycache__" not in str(_))


if __name__ == "__main__":
    sys.exit(main())
