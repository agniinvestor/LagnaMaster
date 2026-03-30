#!/usr/bin/env python3
"""
fix_importer_hour.py — add 'hour' decimal field to birth_data in importer + regenerate
"""
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parent
p = ROOT / "tools" / "adb_xml_importer.py"
text = p.read_text()

# Add hour field after time_type in birth_data dict
text = text.replace(
    '            "time_type": rec.time_type,\n            "time_unknown": rec.time_unknown,',
    '            "time_type": rec.time_type,\n            "hour": round(_parse_time(rec.time_str), 6),\n            "time_unknown": rec.time_unknown,',
)

p.write_text(text)
print("  OK  tools/adb_xml_importer.py — 'hour' field added to birth_data")

result = subprocess.run(
    [sys.executable, "tools/adb_xml_importer.py",
     "adb_sample/c_sample.xml", "--overwrite"],
    capture_output=True, text=True, cwd=ROOT
)
print(result.stdout[-400:] if result.stdout else "")
if result.stderr:
    print(result.stderr[-200:])
print("Done.")
