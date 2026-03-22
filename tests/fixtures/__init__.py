# tests/fixtures/__init__.py
# Common fixtures shared across test modules.

INDIA_1947 = {
    "year": 1947, "month": 8, "day": 15,
    "hour": 0.0,
    "lat": 28.6139, "lon": 77.2090,
    "tz_offset": 5.5,
    "ayanamsha": "lahiri",
    # Verified values from JHora 8.0
    "lagna_degree_in_sign": 7.7286,
    "sun_degree_in_sign": 27.99,
    "moon_degree_in_sign": 3.98,
}

# Re-export regression fixtures
from tests.fixtures.regression_fixtures import (  # noqa: E402
    REFERENCE_CHARTS,
    diff_scores,
    load_baseline,
    compute_and_store_baseline,
)
