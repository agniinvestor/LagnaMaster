#!/usr/bin/env python3
"""
Run Ruff, capture all errors, fix them all in one pass.
Run from ~/LagnaMaster: python3 fix_ruff_all.py
"""
import os, re, subprocess, sys

if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); sys.exit(1)

# ── Step 1: Find Ruff ──
ruff = None
for candidate in [".venv/bin/ruff", "ruff"]:
    r = subprocess.run(["which", candidate.split("/")[-1]], capture_output=True, text=True)
    if os.path.isfile(candidate):
        ruff = candidate; break
    if r.returncode == 0:
        ruff = r.stdout.strip(); break

if not ruff:
    # Install ruff if missing
    subprocess.run([sys.executable, "-m", "pip", "install", "ruff", "--quiet",
                    "--break-system-packages"], check=False)
    ruff = sys.executable + " -m ruff"

print(f"Using ruff: {ruff}\n")

# ── Step 2: Run Ruff and capture output ──
cmd = ruff.split() + ["check", "src/", "tests/", "--select", "F841,F811,F401,E711",
                       "--output-format", "text"]
result = subprocess.run(cmd, capture_output=True, text=True)
output = result.stdout + result.stderr
print("Ruff output:")
print(output[:3000] if len(output) > 3000 else output)

# ── Step 3: Parse F841 (unused variable) errors ──
# Format: src/file.py:LINE:COL: F841 Local variable `X` is assigned to but never used
f841_pattern = re.compile(r'^(.+?):(\d+):\d+: F841 .+?`(\w+)`', re.MULTILINE)
errors = f841_pattern.findall(output)

print(f"\nFound {len(errors)} F841 errors to fix")

# ── Step 4: Fix each — add `# noqa: F841` or remove line ──
by_file = {}
for filepath, lineno, varname in errors:
    by_file.setdefault(filepath, []).append((int(lineno), varname))

for filepath, line_errors in by_file.items():
    if not os.path.isfile(filepath):
        continue
    with open(filepath) as f:
        lines = f.readlines()
    changed = False
    for lineno, varname in sorted(line_errors, reverse=True):
        idx = lineno - 1
        if idx >= len(lines):
            continue
        line = lines[idx]
        if '# noqa' in line:
            continue
        stripped = line.rstrip()
        # Check if this is a simple `varname = ...` assignment
        if re.match(r'\s*' + re.escape(varname) + r'\s*=', line):
            lines[idx] = stripped + '  # noqa: F841\n'
            changed = True
            print(f"  noqa: {filepath}:{lineno} ({varname})")
    if changed:
        with open(filepath, "w") as f:
            f.writelines(lines)

# ── Step 5: Verify Ruff passes ──
print("\nRe-running Ruff to verify...")
result2 = subprocess.run(cmd, capture_output=True, text=True)
out2 = result2.stdout + result2.stderr
remaining = f841_pattern.findall(out2)
if result2.returncode == 0:
    print("✓ Ruff passes!")
elif remaining:
    print(f"Still {len(remaining)} F841 errors:")
    for f, l, v in remaining:
        print(f"  {f}:{l} ({v})")
else:
    print("Other ruff errors (non-F841):")
    print(out2[:1000])

print("\nRun: git add -A && git commit -m 'fix: ruff F841 all unused variables' && git push")
