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
    "planets": {
        "Sun":     {"sign": "Cancer",  "degree": 27.99},
        "Moon":    {"sign": "Cancer",  "degree": 3.98},
        "Mars":    {"sign": "Gemini",  "degree": 22.0},
        "Mercury": {"sign": "Cancer",  "degree": 20.0},
        "Jupiter": {"sign": "Libra",   "degree": 6.0},
        "Venus":   {"sign": "Cancer",  "degree": 16.0},
        "Saturn":  {"sign": "Cancer",  "degree": 26.0},
        "Rahu":    {"sign": "Taurus",  "degree": 8.0},
        "Ketu":    {"sign": "Scorpio", "degree": 8.0},
    },
}

# Re-export regression fixtures
from tests.fixtures.regression_fixtures import (  # noqa: E402
    REFERENCE_CHARTS,
    diff_scores,
    load_baseline,
    compute_and_store_baseline,
)

from tests.fixtures.diverse_chart_fixtures import ALL_FIXTURES, fixture_count  # noqa: E402
