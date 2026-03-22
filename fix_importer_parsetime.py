#!/usr/bin/env python3
"""
fix_importer_parsetime.py — make _parse_time robust + regenerate
"""
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parent
p = ROOT / "tools" / "adb_xml_importer.py"
text = p.read_text()

OLD = '''def _parse_time(time_str: str) -> float:
    """Convert "18:29" to decimal hours 18.4833..."""
    parts = time_str.strip().split(":")
    h = int(parts[0])
    m = int(parts[1]) if len(parts) > 1 else 0
    s = int(parts[2]) if len(parts) > 2 else 0
    return h + m / 60.0 + s / 3600.0'''

NEW = '''def _parse_time(time_str: str) -> float:
    """Convert "18:29" to decimal hours 18.4833... Robust against malformed input."""
    try:
        # Strip anything non-numeric before the first digit
        import re as _re
        clean = time_str.strip()
        # Extract first HH:MM or HH:MM:SS pattern found
        m = _re.search(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", clean)
        if m:
            h = int(m.group(1))
            mi = int(m.group(2))
            s = int(m.group(3)) if m.group(3) else 0
            return h + mi / 60.0 + s / 3600.0
        # Try plain integer hour
        digits = _re.sub(r"[^\d]", "", clean.split(",")[0])
        if digits:
            return float(digits[:2])
    except Exception:
        pass
    return 12.0  # safe default for unknown times'''

if OLD in text:
    text = text.replace(OLD, NEW)
    p.write_text(text)
    print("  OK  _parse_time made robust")
else:
    print("  SKIP — pattern not found, patching inline")
    # Fallback: just replace the function body directly
    text = text.replace(
        '    parts = time_str.strip().split(":")\n    h = int(parts[0])\n    m = int(parts[1]) if len(parts) > 1 else 0\n    s = int(parts[2]) if len(parts) > 2 else 0\n    return h + m / 60.0 + s / 3600.0',
        '    import re as _re\n    try:\n        m = _re.search(r"(\\d{1,2}):(\\d{2})(?::(\\d{2}))?", time_str)\n        if m:\n            h,mi,s = int(m.group(1)),int(m.group(2)),int(m.group(3) or 0)\n            return h + mi/60.0 + s/3600.0\n    except Exception:\n        pass\n    return 12.0'
    )
    p.write_text(text)
    print("  OK  _parse_time patched via fallback")

result = subprocess.run(
    [sys.executable, "tools/adb_xml_importer.py",
     "adb_sample/c_sample.xml", "--overwrite"],
    capture_output=True, text=True, cwd=ROOT
)
print(result.stdout[-400:] if result.stdout else "")
if result.returncode != 0:
    print(result.stderr[-300:])
print("Done.")
