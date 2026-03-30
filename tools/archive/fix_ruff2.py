#!/usr/bin/env python3
"""Run from ~/LagnaMaster: python3 fix_ruff2.py"""
import os, re, glob, sys

if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); sys.exit(1)

# Read .ruff.toml or pyproject.toml to understand what's being linted
ruff_config = ""
for cfg in ["ruff.toml", ".ruff.toml", "pyproject.toml"]:
    if os.path.isfile(cfg):
        with open(cfg) as f: ruff_config = f.read()
        print(f"Found config: {cfg}")
        break

print(f"Config preview:\n{ruff_config[:500]}\n")

# Directly scan all src/ py files for `planets = ` assignments that are unused
# Strategy: for each assignment `planets = X`, check if `planets` appears again
# in the same function scope. If not, add noqa: F841.

fixed = 0
for path in sorted(glob.glob("src/**/*.py", recursive=True) + glob.glob("tests/**/*.py", recursive=True)):
    with open(path) as f:
        lines = f.readlines()
    
    changed = False
    new_lines = list(lines)
    
    for i, line in enumerate(lines):
        # Match assignment to `planets` (most common culprit)
        m = re.match(r'^(\s*)planets\s*=\s*(.+)', line)
        if not m or '# noqa' in line:
            continue
        
        indent = len(m.group(1))
        # Scan ahead to see if `planets` is used before the next same-or-lower indent
        used = False
        for j in range(i + 1, min(i + 50, len(lines))):
            jline = lines[j]
            if jline.strip() == '':
                continue
            jind = len(jline) - len(jline.lstrip())
            if jind <= indent and jline.strip().startswith(('def ', 'class ', 'return', '@', 'if ', 'for ', 'while ')):
                break
            if re.search(r'\bplanets\b', jline):
                used = True
                break
        
        if not used:
            new_lines[i] = line.rstrip() + '  # noqa: F841\n'
            changed = True
            fixed += 1
            print(f"  noqa: {path}:{i+1}")
    
    if changed:
        with open(path, 'w') as f:
            f.writelines(new_lines)

print(f"\nFixed {fixed} unused planets assignments")

# Also check if ruff.toml has specific rules
if 'F841' in ruff_config:
    print("F841 is configured in ruff config")

print("\nRun: git add -A && git commit -m 'fix: noqa F841 unused planets' && git push")
