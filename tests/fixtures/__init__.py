# tests/fixtures/__init__.py
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
