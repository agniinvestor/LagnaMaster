"""
tests/fixtures.py
=================
Known-good birth chart data for regression testing.

All expected values were derived from established Jyotish software
(Jagannatha Hora / Kala) using Lahiri ayanamsha.
"""

# ---------------------------------------------------------------------------
# 1947 India Independence Chart  (primary regression fixture)
# ---------------------------------------------------------------------------
# Birth: 1947-08-15 00:00 IST, New Delhi
# Coordinates: 28.6139°N, 77.2090°E
# Ayanamsha: Lahiri (~23.1489° at this epoch)
#
# Source: widely documented historical chart; cross-checked in Jagannatha Hora.
INDIA_1947 = {
    "year": 1947,
    "month": 8,
    "day": 15,
    "hour": 0.0,  # midnight IST
    "lat": 28.6139,
    "lon": 77.2090,
    "tz_offset": 5.5,  # IST = UTC+5:30
    "ayanamsha": "lahiri",
    # Expected outputs
    "lagna_sign": "Taurus",
    "lagna_degree_in_sign": 7.7286,  # tolerance ±0.05°
    # Classic pancha-graha yoga: Sun/Moon/Mercury/Venus/Saturn all in Cancer.
    # Mars in Gemini, Jupiter in Libra, Rahu in Taurus, Ketu in Scorpio.
    # Cross-checked against pyswisseph output (JD 2432412.2708).
    "planets": {
        "Sun": {"sign": "Cancer", "degree": 27.989},
        "Moon": {"sign": "Cancer", "degree": 3.9835},
        "Mars": {"sign": "Gemini", "degree": None},
        "Mercury": {"sign": "Cancer", "degree": None},
        "Jupiter": {"sign": "Libra", "degree": None},
        "Venus": {"sign": "Cancer", "degree": None},
        "Saturn": {"sign": "Cancer", "degree": None},
        "Rahu": {"sign": "Taurus", "degree": None},
        "Ketu": {"sign": "Scorpio", "degree": None},
    },
}
