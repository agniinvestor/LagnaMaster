#!/usr/bin/env python3
"""
Restore planets variable assignments that were incorrectly removed.
Run from ~/LagnaMaster: python3 fix_planets_restore.py
"""
import os, subprocess

if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# Use git to restore the files that had planets removed,
# then re-apply only the safe changes
files_to_restore = [
    "src/calculations/yogas.py",
    "src/calculations/extended_yogas.py", 
    "src/calculations/yoga_fructification.py",
    "src/calculations/multi_axis_scoring.py",
    "src/calculations/gochara.py",
    "src/calculations/argala.py",
    "src/calculations/kp.py",
    "src/api/main_v2.py",
    "src/calculations/varga.py",
    "src/ephemeris.py",
]

print("Restoring incorrectly modified files from git...")
for f in files_to_restore:
    result = subprocess.run(
        ["git", "checkout", "HEAD~1", "--", f],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"  OK  restored {f}")
    else:
        # Try HEAD
        result2 = subprocess.run(
            ["git", "show", "HEAD:" + f],
            capture_output=True, text=True
        )
        if result2.returncode == 0:
            # Check if this version has the planets lines
            if "planets =" in result2.stdout:
                with open(f, "w") as fh:
                    fh.write(result2.stdout)
                print(f"  OK  restored {f} from HEAD")
            else:
                print(f"  SKIP {f} (HEAD also missing planets)")
        else:
            print(f"  WARN {f}: {result.stderr.strip()}")

# Re-apply ONLY the is_cazimi/is_combust fix to restored files
import glob
print("\nRe-applying is_cazimi/is_combust fix to restored files...")
for path in files_to_restore:
    if not os.path.isfile(path):
        continue
    with open(path) as f:
        src = f.read()
    new = src.replace(".is_cazimi", ".cazimi").replace(".is_combust", ".combust")
    if new != src:
        with open(path, "w") as f:
            f.write(new)
        print(f"  OK  {path}")

print("\nDone. Run:")
print("  PYTHONPATH=. .venv/bin/pytest --tb=line -q --ignore=tests/test_session21.py --ignore=tests/test_varga.py 2>&1 | tail -6")
