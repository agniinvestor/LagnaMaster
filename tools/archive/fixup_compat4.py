#!/usr/bin/env python3
"""Compat4. Run from ~/LagnaMaster: python3 fixup_compat4.py"""
import os
BASE = os.getcwd()
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

def patch(path, old, new, label):
    with open(path) as f: src = f.read()
    if old not in src: print(f"  SKIP {path} [{label}]"); return
    with open(path, "w") as f: f.write(src.replace(old, new, 1))
    print(f"  OK   {path} [{label}]")

def append(path, text, guard, label):
    with open(path) as f: src = f.read()
    if guard in src: print(f"  SKIP {path} [{label}]"); return
    with open(path, "a") as f: f.write("\n" + text)
    print(f"  OK   {path} [{label}]")

print("Applying compat4 fixes...\n")

# ── 1. shadbala.py: wrap compute_all_shadbala result in object with .planets ──
# Old API: result = compute_shadbala(chart); result.planets["Sun"].naisargika
# New API: result = compute_all_shadbala(chart) -> dict[str, ShadbalResult]
# ShadbalResult.naisargika_bala but old tests use .naisargika and .chesta
append("src/calculations/shadbala.py", """
# ── Backward-compatibility wrapper ──
class _ShadbalWrapper:
    \"\"\"Wraps dict[str, ShadbalResult] to expose .planets and old field names.\"\"\"
    def __init__(self, d: dict):
        self._d = d
        self.planets = {k: _ShadbalFieldProxy(v) for k, v in d.items()}
    def __getitem__(self, k): return self.planets[k]
    def items(self): return self.planets.items()
    def keys(self): return self.planets.keys()

class _ShadbalFieldProxy:
    \"\"\"Exposes short field names (.naisargika, .chesta) from ShadbalResult.\"\"\"
    def __init__(self, r: "ShadbalResult"):
        self._r = r
    def __getattr__(self, name):
        # Map short names to full names
        _map = {
            "naisargika": "naisargika_bala",
            "chesta": "chesta_bala",
            "uchcha": "uchcha_bala",
            "dig": "dig_bala",
            "kala": "kala_bala",
            "drik": "drik_bala",
            "sthana": "sthana_bala",
            "ishta": "ishta_bala",
            "kashta": "kashta_bala",
            "total": "total",
        }
        full = _map.get(name, name)
        return getattr(self._r, full)

def compute_shadbala_legacy(planet_or_chart=None, sign_idx: int = 0,
                            degree: float = 0.0, chart=None, birth_dt=None,
                            planet: str = None):
    \"\"\"Old API shim. Handles compute_shadbala(chart) and compute_shadbala(planet, chart).\"\"\"
    if planet_or_chart is not None and hasattr(planet_or_chart, 'planets'):
        return _ShadbalWrapper(compute_all_shadbala(planet_or_chart, birth_dt))
    _planet = planet_or_chart if isinstance(planet_or_chart, str) else planet
    if chart is not None and hasattr(chart, 'planets'):
        return compute_shadbala(_planet, chart, birth_dt)
    # positional legacy: compute_shadbala(planet, sign_idx, degree)
    class _P:
        def __init__(self):
            self.sign_index = sign_idx; self.degree_in_sign = degree
            self.longitude = sign_idx * 30.0 + degree
            self.is_retrograde = False; self.speed = 1.0; self.latitude = 0.0
    class _C:
        def __init__(self):
            self.lagna = 0.0; self.lagna_sign_index = 0
            self.planets = {_planet: _P()}
            sun = _P(); sun.sign_index = 0; sun.longitude = 0.0
            self.planets["Sun"] = sun
    return compute_shadbala(_planet, _C(), birth_dt)
""", "_ShadbalWrapper", "shadbala wrapper + legacy v2")

# Remove old broken legacy shim (it's now duplicated)
patch("src/calculations/shadbala.py",
    """def compute_shadbala_legacy(planet_or_chart=None, sign_idx: int = 0,
                             degree: float = 0.0, chart=None, birth_dt=None,
                             planet: str = None):
    \"\"\"Old API shim. Handles both compute_shadbala(chart) and compute_shadbala(planet, chart).\"\"\"
    # If first arg looks like a chart (has .planets), call compute_all_shadbala
    if planet_or_chart is not None and hasattr(planet_or_chart, 'planets'):
        return compute_all_shadbala(planet_or_chart, birth_dt)
    # Otherwise first arg is planet name
    _planet = planet_or_chart if isinstance(planet_or_chart, str) else planet
    if chart is not None and hasattr(chart, 'planets'):
        return compute_shadbala(_planet, chart, birth_dt)""",
    "# (replaced by _ShadbalWrapper version below)",
    "remove old shadbala legacy")

# ── 2. dignity.py: test_retrograde_bonus_applied ──
# Test checks that a retrograde planet gets a bonus in dignity scoring
# Our is_retrograde property returns asta_vakri (combust+rx) which is False for a plain Rx planet
# Fix: check the planet's own is_retrograde flag when available
patch("src/calculations/dignity.py",
    """    @property
    def is_retrograde(self) -> bool:
        \"\"\"Backward-compat property. Rahu/Ketu always retrograde in Jyotish.\"\"\"
        if self.planet in ("Rahu", "Ketu"):
            return True
        return self.asta_vakri""",
    """    @property
    def is_retrograde(self) -> bool:
        \"\"\"Backward-compat. Rahu/Ketu always Rx; others True if combust+Rx or plain Rx.\"\"\"
        if self.planet in ("Rahu", "Ketu"):
            return True
        # asta_vakri = combust+retrograde. Also check stored _is_retrograde if set.
        return self.asta_vakri or getattr(self, "_is_retrograde", False)""",
    "is_retrograde plain rx")

# ── 3. nakshatra.py: new AttributeError — show what test_sun_ashlesha expects ──
# Likely accessing .longitude or similar on NakshatraPosition
with open("tests/test_calculations.py") as f:
    tc = f.read()
# Find test_sun_ashlesha
import re
m = re.search(r'def test_sun_ashlesha.*?(?=def test_|\Z)', tc, re.DOTALL)
if m:
    print(f"test_sun_ashlesha:\n{m.group(0)[:400]}")

print("\nDone. Run:")
print("  PYTHONPATH=. .venv/bin/pytest tests/test_calculations.py --tb=line -q 2>&1 | tail -10")
