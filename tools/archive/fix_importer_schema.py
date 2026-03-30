#!/usr/bin/env python3
"""
fix_importer_schema.py — patch tools/adb_xml_importer.py to use birth_data key
then regenerate all fixtures from c_sample.xml
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

p = ROOT / "tools" / "adb_xml_importer.py"
text = p.read_text()

# Fix the key in record_to_fixture
text = text.replace(
    '"birth": {',
    '"birth_data": {',
)

p.write_text(text)
print("  OK  tools/adb_xml_importer.py — 'birth' -> 'birth_data'")

# Regenerate fixtures
import subprocess, sys
result = subprocess.run(
    [sys.executable, "tools/adb_xml_importer.py",
     "adb_sample/c_sample.xml", "--overwrite"],
    capture_output=True, text=True, cwd=ROOT
)
print(result.stdout[-500:] if result.stdout else "")
if result.stderr:
    print(result.stderr[-300:])
print("Done.")
