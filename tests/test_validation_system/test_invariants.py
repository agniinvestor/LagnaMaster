"""Universal chart invariants — properties that hold for ANY birth chart."""
import pytest

from src.calculations.nakshatra import nakshatra_position
from src.ephemeris import compute_chart

INVARIANT_CHARTS = [
    {"year": 1947, "month": 8, "day": 15, "hour": 0.0,
     "lat": 28.6139, "lon": 77.2090, "tz_offset": 5.5},
    {"year": 2000, "month": 1, "day": 1, "hour": 12.0,
     "lat": 40.7128, "lon": -74.006, "tz_offset": -5.0},
    {"year": 1985, "month": 6, "day": 21, "hour": 23.5,
     "lat": 64.1466, "lon": -21.9426, "tz_offset": 0.0},
]


@pytest.fixture(params=INVARIANT_CHARTS,
                ids=["india_1947", "nyc_2000", "reykjavik_1985"])
def chart(request):
    return compute_chart(**request.param)


class TestPositionInvariants:
    def test_lagna_in_range(self, chart):
        assert 0 <= chart.lagna < 360

    def test_planet_longitudes_in_range(self, chart):
        for name, pos in chart.planets.items():
            assert 0 <= pos.longitude < 360, f"{name} longitude out of range"

    def test_sign_index_matches_longitude(self, chart):
        for name, pos in chart.planets.items():
            expected_sign = int(pos.longitude // 30)
            assert pos.sign_index == expected_sign, (
                f"{name}: sign_index {pos.sign_index} != "
                f"floor({pos.longitude}/30) = {expected_sign}"
            )

    def test_rahu_ketu_opposite(self, chart):
        rahu = chart.planets["Rahu"].longitude
        ketu = chart.planets["Ketu"].longitude
        diff = abs(rahu - ketu)
        assert abs(diff - 180.0) < 1.0 or abs(diff - 540.0) < 1.0


class TestNakshatraInvariants:
    def test_nakshatra_index_in_range(self, chart):
        for name, pos in chart.planets.items():
            nak = nakshatra_position(pos.longitude)
            assert 0 <= nak.nakshatra_index <= 26, (
                f"{name} nakshatra index {nak.nakshatra_index} out of range"
            )

    def test_pada_in_range(self, chart):
        for name, pos in chart.planets.items():
            nak = nakshatra_position(pos.longitude)
            assert 1 <= nak.pada <= 4, (
                f"{name} pada {nak.pada} out of range"
            )
