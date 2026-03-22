#!/usr/bin/env python3
"""Fix tests/fixtures/__init__.py. Run from ~/LagnaMaster."""
import os
if not os.path.isfile("requirements.txt"):
    print("ERROR: run from LagnaMaster root"); exit(1)

# Check what's importing INDIA_1947 from fixtures
import subprocess
r = subprocess.run(['grep', '-rn', 'from tests.fixtures', 'tests/'], capture_output=True, text=True)
print("Imports from tests.fixtures:")
print(r.stdout[:500])

content = '''# tests/fixtures/__init__.py
# Common fixtures shared across test modules.

INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
}

# Re-export regression fixtures
from tests.fixtures.regression_fixtures import (  # noqa: E402
    REFERENCE_CHARTS,
    diff_scores,
    load_baseline,
    compute_and_store_baseline,
)
'''

with open("tests/fixtures/__init__.py", "w") as f:
    f.write(content)
print("OK  tests/fixtures/__init__.py")
