#!/usr/bin/env python3
"""Read key files. Run from ~/LagnaMaster: python3 read_files.py"""
import os

files = [
    "src/calculations/scoring_v3.py",
    "src/calculations/yogas.py",
    "src/calculations/config_toggles.py",
    "src/calculations/narayana_dasha.py",
    "src/calculations/vargas.py",
]

for f in files:
    if os.path.isfile(f):
        size = os.path.getsize(f)
        with open(f) as fh:
            content = fh.read()
        print(f"\n{'='*60}")
        print(f"FILE: {f} ({size} bytes, {content.count(chr(10))} lines)")
        print('='*60)
        print(content[:3000])
        if len(content) > 3000:
            print(f"\n... [{len(content)-3000} more bytes] ...")
    else:
        print(f"\nNOT FOUND: {f}")
