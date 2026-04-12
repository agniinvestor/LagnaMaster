#!/usr/bin/env python3
"""Build transitive reachability set from production entry points.

Walks AST imports starting from entry points, reports unreachable files.
"""
import ast
import os
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

ENTRY_POINTS = [
    SRC / "ui" / "app.py",
    SRC / "api" / "main.py",
    SRC / "worker.py",
]

def resolve_import(module_str: str, from_file: Path) -> list[Path]:
    """Resolve a dotted module string to file path(s) under src/."""
    # Handle relative imports
    parts = module_str.split(".")

    # Try as a direct module file
    candidates = []

    # Absolute: src.X.Y -> src/X/Y.py or src/X/Y/__init__.py
    if parts[0] == "src":
        rel_parts = parts[1:]
    else:
        rel_parts = parts

    # Try as file
    file_path = SRC / "/".join(rel_parts)
    candidates.append(file_path.with_suffix(".py"))
    candidates.append(file_path / "__init__.py")

    # Also try from root
    file_path2 = ROOT / "/".join(parts)
    candidates.append(file_path2.with_suffix(".py"))
    candidates.append(file_path2 / "__init__.py")

    return [c for c in candidates if c.exists()]


def extract_imports(file_path: Path) -> set[str]:
    """Extract all import targets from a Python file using AST."""
    try:
        source = file_path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return set()

    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("src"):
                    modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("src"):
                modules.add(node.module)
            elif node.level and node.level > 0:
                # Relative import - resolve from current package
                pkg_parts = list(file_path.relative_to(ROOT).parent.parts)
                if node.level > 1:
                    pkg_parts = pkg_parts[:-(node.level - 1)]
                if node.module:
                    pkg_parts.append(node.module)
                full_module = ".".join(pkg_parts)
                if full_module.startswith("src"):
                    modules.add(full_module)

    return modules


def build_reachability(entry_points: list[Path]) -> set[Path]:
    """BFS from entry points, following imports transitively."""
    visited = set()
    queue = list(entry_points)

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        if not current.exists():
            continue
        visited.add(current)

        # Also add the __init__.py of the package
        init = current.parent / "__init__.py"
        if init.exists() and init not in visited:
            queue.append(init)

        imports = extract_imports(current)
        for mod in imports:
            resolved = resolve_import(mod, current)
            for r in resolved:
                if r not in visited:
                    queue.append(r)

    return visited


def find_all_src_files() -> set[Path]:
    """Find all .py files under src/, excluding __pycache__."""
    result = set()
    for p in SRC.rglob("*.py"):
        if "__pycache__" not in str(p):
            result.add(p.resolve())
    return result


def find_tools_imports() -> dict[str, list[str]]:
    """Find which src modules are imported by tools/."""
    tools_dir = ROOT / "tools"
    imports = defaultdict(list)
    if not tools_dir.exists():
        return imports
    for py in tools_dir.rglob("*.py"):
        if "__pycache__" in str(py):
            continue
        for mod in extract_imports(py):
            resolved = resolve_import(mod, py)
            for r in resolved:
                imports[str(r.resolve())].append(str(py.relative_to(ROOT)))
    return imports


def find_test_imports() -> dict[str, list[str]]:
    """Find which src modules are imported only by tests/."""
    tests_dir = ROOT / "tests"
    imports = defaultdict(list)
    if not tests_dir.exists():
        return imports
    for py in tests_dir.rglob("*.py"):
        if "__pycache__" in str(py):
            continue
        for mod in extract_imports(py):
            resolved = resolve_import(mod, py)
            for r in resolved:
                imports[str(r.resolve())].append(str(py.relative_to(ROOT)))
    return imports


def main():
    # Build reachability from entry points
    reachable = {p.resolve() for p in build_reachability(ENTRY_POINTS)}
    all_files = find_all_src_files()
    tools_imports = find_tools_imports()
    test_imports = find_test_imports()

    unreachable = all_files - reachable

    # Classify
    entry_point_set = {p.resolve() for p in ENTRY_POINTS}

    print(f"=== REACHABILITY ANALYSIS ===")
    print(f"Total src/ .py files: {len(all_files)}")
    print(f"Reachable from entry points: {len(reachable)}")
    print(f"Unreachable: {len(unreachable)}")
    print()

    # Categorize unreachable
    tools_only = []
    test_only = []
    truly_dead = []

    for f in sorted(unreachable):
        f_str = str(f)
        rel = str(f.relative_to(ROOT))
        in_tools = f_str in tools_imports
        in_tests = f_str in test_imports

        if f in entry_point_set:
            continue  # entry points are roots
        elif in_tools:
            tools_only.append((rel, tools_imports[f_str]))
        elif in_tests:
            test_only.append((rel, test_imports[f_str]))
        else:
            truly_dead.append(rel)

    if tools_only:
        print(f"=== TOOLS_INFRA ({len(tools_only)} files) ===")
        for rel, importers in tools_only:
            print(f"  {rel}")
            for imp in importers[:3]:
                print(f"    <- {imp}")
        print()

    if test_only:
        print(f"=== TEST-ONLY ({len(test_only)} files) ===")
        for rel, importers in test_only:
            print(f"  {rel}")
            for imp in importers[:3]:
                print(f"    <- {imp}")
        print()

    if truly_dead:
        print(f"=== TRULY DEAD ({len(truly_dead)} files) ===")
        for rel in truly_dead:
            print(f"  {rel}")
        print()

    # Summary
    print("=== SUMMARY ===")
    print(f"Reachable:   {len(reachable)}")
    print(f"Tools-only:  {len(tools_only)}")
    print(f"Test-only:   {len(test_only)}")
    print(f"Truly dead:  {len(truly_dead)}")
    print(f"Total:       {len(all_files)}")

    # Also report reachable files for reference
    if "--show-reachable" in sys.argv:
        print("\n=== REACHABLE FILES ===")
        for f in sorted(reachable):
            print(f"  {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
